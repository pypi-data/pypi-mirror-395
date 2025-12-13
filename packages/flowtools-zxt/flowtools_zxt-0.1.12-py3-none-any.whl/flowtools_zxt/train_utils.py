import os
import pandas as pd
import numpy as np
import torch
import torch.distributed as dist
import datetime
import sys
import pytz
import warnings
import argparse
from tqdm import tqdm

warnings.filterwarnings("ignore")


def set_baseline_time(time_region = 'Asia/Shanghai'):
    beijing_tz = pytz.timezone(time_region)


def init_distributed_mode(args):
    if 'RANK' in os.environ and 'WORLD_SIZE' in os.environ:
        args.rank = int(os.environ["RANK"])
        args.world_size = int(os.environ['WORLD_SIZE'])
        args.gpu = int(os.environ['LOCAL_RANK'])
    elif 'SLURM_PROCID' in os.environ:
        args.rank = int(os.environ['SLURM_PROCID'])
        args.gpu = args.rank % torch.cuda.device_count()
    else:
        print('Not using distributed mode')
        args.distributed = False
        return

    args.distributed = True

    torch.cuda.set_device(args.gpu)
    args.dist_backend = 'nccl'  # 通信后端，nvidia GPU推荐使用NCCL
    print('| distributed init (rank {}): {}'.format(
        args.rank, args.dist_url), flush=True)
    dist.init_process_group(backend=args.dist_backend, timeout=datetime.timedelta(seconds=3600*6))
    dist.barrier()


def cleanup():
    dist.destroy_process_group()


def is_dist_avail_and_initialized():
    """检查是否支持分布式环境"""
    if not dist.is_available():
        return False
    if not dist.is_initialized():
        return False
    return True


def get_world_size():
    if not is_dist_avail_and_initialized():
        return 1
    return dist.get_world_size()


def get_rank():
    if not is_dist_avail_and_initialized():
        return 0
    return dist.get_rank()


def is_main_process():
    return get_rank() == 0


def reduce_value(value, average=True):
    world_size = get_world_size()
    if world_size < 2:  # 单GPU的情况
        return value

    with torch.no_grad():
        dist.all_reduce(value)
        if average:
            value /= world_size
        return value

class EarlyStopping:
    def __init__(self, patience=3):
        self.patience = patience
        self.counter = 0
        self.best_loss = None
        self.should_stop = False

    def step(self, val_loss):
        if self.best_loss is None:
            self.best_loss = val_loss
        elif val_loss > self.best_loss:
            self.counter += 1
            if self.counter >= self.patience:
                self.should_stop = True
        else:
            self.best_loss = val_loss
            self.counter = 0


def get_dtype(dtype_str):
    """获取对应的dtype"""
    dtype_map = {
        "bf16": torch.bfloat16,
        "fp16": torch.float16,
        "fp32": torch.float32
    }
    return dtype_map.get(dtype_str, torch.float32)

def update_mean_loss(current_mean, new_loss, step):
    """更新平均损失"""
    return (current_mean * step + new_loss.detach().to(torch.float32)) / (step + 1)


def train(model_engine, data_loader, local_device, local_rank, epoch, loss_function,
          global_train_loss, dtype_, iteration_strategy=None, lr_getter=None,
          loss_reducer=None, progress_desc_formatter=None):
    """
    通用训练函数 - 策略模式

    参数:
        iteration_strategy: 迭代策略函数，接收 (data, device, dtype) 返回 (outputs, loss)
    """
    mean_loss = 0

    # 默认策略：data["x"] 作为输入，data["y"] 作为目标
    if iteration_strategy is None:
        def iteration_strategy(data, device, dtype, model, loss_fn):
            x = data["x"].to(device, non_blocking=True).to(dtype)
            y = data["y"].to(device, non_blocking=True).to(dtype)
            outputs = model(x)
            loss = loss_fn(outputs, y)
            return outputs, loss

    # 默认的进度条描述格式化函数
    if progress_desc_formatter is None:
        def progress_desc_formatter(epoch, lr, mean_loss, global_loss):
            lr_str = f"lr:{round(lr, 8)}" if lr is not None else "lr:None"
            return f"[{datetime.datetime.now(beijing_tz).strftime('%Y-%m-%d %H:%M:%S')}] " \
                   f"[epoch:{epoch} {lr_str}] train mean loss {mean_loss:.6f} | {global_loss}"

    # 默认的学习率获取函数
    if lr_getter is None:
        def lr_getter(model_engine):
            return model_engine.optimizer.param_groups[0]['lr']

    # 默认的损失归约函数
    if loss_reducer is None:
        loss_reducer = reduce_value

    # 获取dtype
    dtype = get_dtype(dtype_)

    # 在进程0中打印训练进度
    if local_rank == 0:
        data_loader = tqdm(data_loader, file=sys.stdout)

    for step, data in enumerate(data_loader):
        # 使用策略函数处理数据并计算损失
        outputs, loss = iteration_strategy(data, local_device, dtype, model_engine, loss_function)

        # DeepSpeed 反向传播和优化步骤
        model_engine.backward(loss)
        model_engine.step()

        # 损失值处理和记录
        loss = loss_reducer(loss)
        mean_loss = update_mean_loss(mean_loss, loss, step)

        # 在进程0中打印平均 loss
        if local_rank == 0:
            current_lr = lr_getter(model_engine)
            desc = progress_desc_formatter(epoch, current_lr, mean_loss.item(), global_train_loss)
            data_loader.desc = desc

        if not torch.isfinite(loss):
            print('WARNING: non-finite loss, ending training ', loss)
            sys.exit(1)

    return mean_loss.item()


@torch.no_grad()
def evaluate(model_engine, data_loader, local_device, local_rank, epoch, loss_function,
             global_test_loss, dtype_, iteration_strategy=None, loss_reducer=None,
             progress_desc_formatter=None):
    """
    通用验证函数 - 策略模式
    """
    model_engine.eval()
    mean_loss = 0

    # 默认策略
    if iteration_strategy is None:
        def iteration_strategy(data, device, dtype, model, loss_fn):
            x = data["x"].to(device, non_blocking=True).to(dtype)
            y = data["y"].to(device, non_blocking=True).to(dtype)
            outputs = model(x)
            loss = loss_fn(outputs, y)
            return outputs, loss

    # 默认的进度条描述格式化函数
    if progress_desc_formatter is None:
        def progress_desc_formatter(epoch, lr, mean_loss, global_loss):
            return f"[{datetime.datetime.now(beijing_tz).strftime('%Y-%m-%d %H:%M:%S')}] " \
                   f"[epoch:{epoch} lr:None] test mean loss {mean_loss:.6f} | {global_loss}"

    # 默认的损失归约函数
    if loss_reducer is None:
        def loss_reducer(loss):
            return reduce_value(loss, average=True)

    # 获取dtype
    dtype = get_dtype(dtype_)

    # 在进程0中打印验证进度
    if is_main_process():
        data_loader = tqdm(data_loader, file=sys.stdout)

    for step, data in enumerate(data_loader):
        # 使用策略函数处理数据并计算损失
        outputs, loss = iteration_strategy(data, local_device, dtype, model_engine, loss_function)

        loss = loss_reducer(loss)
        mean_loss = update_mean_loss(mean_loss, loss, step)

        # 在进程0中打印平均 loss
        if is_main_process():
            desc = progress_desc_formatter(epoch, None, mean_loss.item(), global_test_loss)
            data_loader.desc = desc

    return mean_loss.item()
