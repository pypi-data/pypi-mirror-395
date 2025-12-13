import xarray as xr
import pandas as pd
import numpy as np
import os
import shutil
import datetime as dt
import sys
import torch
import astropy.units as u

from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec
from astropy.coordinates import get_sun, EarthLocation, AltAz
from astropy.time import Time
from datetime import datetime, timedelta
from typing import List, Tuple, Dict, Union, Optional


def convert_numeric_to_float32(df, inplace=False):
    """
    参数:
        inplace (bool): 是否原地修改 DataFrame
    """
    num_cols = df.select_dtypes(include=['int', 'float']).columns
    if not inplace:
        df = df.copy()
    df[num_cols] = df[num_cols].astype(np.float32)
    return df


def find_nearest_lon_lat(lon, lat, lon_to, lat_to):
    # 计算所有 lon_to, lat_to 与目标 lon, lat 的距离
    lon_dist = np.abs(lon_to - lon)
    lat_dist = np.abs(lat_to - lat)

    # 找到最近的经度和纬度的索引
    lon_index = np.argmin(lon_dist)
    lat_index = np.argmin(lat_dist)

    # 获取最近的 lon 和 lat 值
    nearest_lon = lon_to[lon_index]
    nearest_lat = lat_to[lat_index]

    return nearest_lon, nearest_lat


def extract_from_dataarray_dict(dataarray_dict, results, rename_method={"lon": "lon_to", "lat": "lat_to"}):

    results = convert_numeric_to_float32(results)

    for key, value in dataarray_dict.items():
        value = value.to_dataframe().reset_index()
        value = value.rename(columns=rename_method)
        value = value.sort_values(by=[rename_method['lon'], rename_method['lat']])
        value = value.loc[:, [rename_method['lon'], rename_method['lat'], key]]
        value = convert_numeric_to_float32(value)

        # results.to_csv("/data/_project_zxt/Ph.D/_asian_visibility_retrieval/test1.csv", index=False)
        # value.to_csv("/data/_project_zxt/Ph.D/_asian_visibility_retrieval/test2.csv", index=False)

        results = pd.merge_asof(
            results,
            value,
            on=rename_method['lon'],
            by=rename_method['lat'],
            direction='nearest'
        )
        # results.to_csv("/data/_project_zxt/Ph.D/_asian_visibility_retrieval/test3.csv", index=False)

    return results


def update_folder(folder_path):

    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        os.makedirs(folder_path)
    else:
        os.makedirs(folder_path)


def convert_datetime_to_str(time):

    year = str(time.year).zfill(4)
    month = str(time.month).zfill(2)
    day = str(time.day).zfill(2)
    hour = str(time.hour).zfill(2)
    minute = str(time.minute).zfill(2)

    return year, month, day, hour, minute

def convert_list_to_datetime(date_list):
    # 根据列表长度决定如何处理
    if len(date_list) == 3:  # 年月日
        year, month, day = date_list
        return datetime(year=year, month=month, day=day)
    elif len(date_list) == 4:  # 年月日时
        year, month, day, hour = date_list
        return datetime(year=year, month=month, day=day, hour=hour)
    elif len(date_list) == 5:  # 年月日时分
        year, month, day, hour, minute = date_list
        return datetime(year=year, month=month, day=day, hour=hour, minute=minute)
    else:
        raise ValueError("输入的列表长度不支持，请提供长度为 3（年月日）、4（年月日时）或 5（年月日时分）的列表")


def generate_single_hour_window(date, past_len=6, future_len=6, interval=3):

    past_hours = [date - timedelta(hours=interval * i) for i in range(past_len)][::-1]

    future_hours = [date + timedelta(hours=interval * (i+1)) for i in range(future_len)]

    return past_hours, future_hours


def generate_hour_windows(start_date, end_date, past_len=6, future_len=6, interval=3):
    """
    Generate past and future time windows for a date range.

    Args:
        start_date (datetime): Start of the date range
        end_date (datetime): End of the date range
        past_len (int): Number of past time steps
        future_len (int): Number of future time steps
        interval (int): Time interval between steps in hours

    Returns:
        dict: Dictionary with 'past_times' and 'future_times' lists of time windows
    """
    time_windows = {"past_times": [], "future_times": []}

    current_date = start_date
    while current_date <= end_date:
        past_times, future_times = generate_single_hour_window(current_date, past_len, future_len, interval)
        time_windows["past_times"].append(past_times)
        time_windows["future_times"].append(future_times)

        current_date += timedelta(hours=1)

    return time_windows

def generate_datetime_list(start_date, end_date, interval=1, resolution="hour"):

    times_ = []

    if resolution == "hour":
        current_date = start_date
        while current_date <= end_date:
            times_.append(current_date)
            current_date += timedelta(hours=interval)


    return times_


def seq2seq_timeseries(
        init_time: datetime,
        past_len: int = 6,
        future_len: int = 6,
        interval: int = 3,
        rolling_num: Optional[int] = None
) -> Dict[str, List[datetime]]:
    """
    生成初始时间序列和预报时间序列

    参数:
        init_time: 初始时刻，格式如datetime(2015, 1, 1, 1, 30)
        past_len: 初始时间序列的长度（包含init_time本身）
        future_len: 未来时间序列的长度（从init_time往后）
        interval: 时间间隔（小时）
        rolling_num: 滚动预报次数，None表示不滚动，整数表示滚动次数

    返回:
        dict: 包含初始时间序列和预报时间序列的字典
    """

    # 生成初始时间序列（包含init_time本身）
    # 例如past_len=6，则包含：t-5*interval, t-4*interval, ..., t-1*interval, t
    past_times = [init_time - timedelta(hours=interval * i)
                  for i in range(past_len-1, -1, -1)]

    # 生成未来时间序列
    if rolling_num is None or rolling_num <= 1:
        # 单次预报：从init_time+interval开始，生成future_len个时间点
        future_times = [init_time + timedelta(hours=interval * (i+1))
                        for i in range(future_len)]
    else:
        # 滚动预报：生成连续的future_len * rolling_num个时间点
        future_times = []

        # 第一个时间点是 init_time + interval
        current_time = init_time + timedelta(hours=interval)

        for roll in range(rolling_num):
            # 生成当前滚动窗口的future_len个时间点
            for i in range(future_len):
                future_times.append(current_time)
                current_time += timedelta(hours=interval)

    result = {
        "init_time": init_time,
        "past_times": past_times,     # 长度 = past_len
        "future_times": future_times, # 长度 = future_len * (rolling_num or 1)
        "rolling_num": rolling_num if rolling_num else 0
    }

    return result


def mask_tensor(tensor, mask=None, channel_index=None, dtype=None):
    """
    对张量 [b, t, c, h, w] 的指定 channel 应用 [h, w] 维度的 mask，其他 channel 不变。

    Args:
        tensor (torch.Tensor): 输入张量，形状 [b, t, c, h, w]
        mask (torch.Tensor, optional): 掩码张量，形状 [h, w]
        channel_index (list, optional): 需要应用 mask 的 channel 索引，其他 channel 不变
        dtype: 张量的数据类型（如果提供）

    Returns:
        torch.Tensor: 应用 mask 后的张量
    """
    # 如果 mask 为 None，加载默认 mask
    if mask is None:
        mask = torch.tensor(np.load("/data/_project_zxt/Ph.D/_asian_forecast/data/mask.npy"), dtype=dtype)

    # 确保 mask 在正确设备上并转换为指定 dtype
    mask = mask.to(tensor.device, non_blocking=True).to(dtype if dtype is not None else tensor.dtype)

    # 检查 mask 形状是否匹配 [h, w]
    if mask.shape != tensor.shape[3:5]:
        raise ValueError(f"Mask shape {mask.shape} does not match tensor [h, w] shape {tensor.shape[3:5]}")

    # 创建输出张量，复制输入张量
    masked_tensor = tensor.clone()

    # 如果提供了 channel_index，仅对指定 channel 应用 mask
    if channel_index is not None:
        # 扩展 mask 到 [1, 1, 1, h, w]
        mask = mask.view(1, 1, 1, mask.shape[0], mask.shape[1])
        # 对指定 channel 应用 mask
        for c in channel_index:
            masked_tensor[:, :, c, :, :] = masked_tensor[:, :, c, :, :] * mask

    return masked_tensor


def encode_month(months):
    """
    对月份数组进行循环编码（周期12）。

    参数:
    months: numpy数组或列表，值在1-12。

    返回:
    month_sin, month_cos: 两个numpy数组。
    """
    months = np.asarray(months)  # 确保是numpy数组
    # 使用 (months - 1) 使1月从0开始
    month_sin = np.sin(2 * np.pi * (months - 1) / 12)
    month_cos = np.cos(2 * np.pi * (months - 1) / 12)
    return month_sin, month_cos

def encode_hour(hours):
    """
    对小时数组进行循环编码（周期24）。

    参数:
    hours: numpy数组或列表，值在0-23。

    返回:
    hour_sin, hour_cos: 两个numpy数组。
    """
    hours = np.asarray(hours)
    hour_sin = np.sin(2 * np.pi * hours / 24)
    hour_cos = np.cos(2 * np.pi * hours / 24)
    return hour_sin, hour_cos

def encode_yday(month, day, year=2023):
    """
    计算年积日（年中日）并进行编码

    参数:
    month: 月份 (1-12)
    day: 日期 (1-31)
    year: 年份（用于判断闰年，默认2023）

    返回:
    yday: 年积日 (1-365或366)
    yday_norm: 归一化年积日 [0, 1]
    yday_sin, yday_cos: 循环编码
    """
    month = np.asarray(month)
    day = np.asarray(day)

    # 每月的天数（考虑闰年）
    month_days = np.array([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        month_days[1] = 29  # 闰年2月29天

    # 计算每个日期的年积日
    yday = np.zeros_like(month, dtype=float)
    for i in range(len(month)):
        m = month[i] - 1  # 转换为0-based索引
        if m > 0:
            yday[i] = np.sum(month_days[:m]) + day[i]
        else:
            yday[i] = day[i]

    # 归一化
    total_days = 366 if month_days[1] == 29 else 365
    yday_norm = (yday - 1) / (total_days - 1)  # [0, 1]

    # 循环编码
    yday_rad = 2 * np.pi * (yday - 1) / total_days
    yday_sin = np.sin(yday_rad)
    yday_cos = np.cos(yday_rad)

    return yday, yday_sin, yday_cos


def calculate_solar_elevation(month, day, hour, lat, lon):
    """
    计算太阳高度角（世界时）

    参数:
    month: 月份 (1-12), 一维ndarray
    day: 日期 (1-31), 一维ndarray
    hour: 小时 (0-23), 一维ndarray
    lat: 纬度 (度), 一维ndarray
    lon: 经度 (度), 一维ndarray

    返回:
    太阳高度角 (度), 一维ndarray
    """
    # 转换为弧度
    lat_rad = np.radians(lat)

    # 计算儒略日
    n = np.floor(275 * month / 9) - 2 * np.floor((month + 9) / 12) + day - 30

    # 计算太阳赤纬 (δ)
    # 使用近似公式: δ = 23.45 * sin(360/365 * (284 + n) * π/180)
    delta = np.radians(23.45 * np.sin(np.radians(360 * (284 + n) / 365)))

    # 计算时角 (ω)
    # 世界时转换为地方时
    local_hour = hour + lon / 15.0
    # 计算时角 (正午为0度，每小时15度)
    omega = np.radians(15 * (local_hour - 12))

    # 计算太阳高度角 (α)
    # sin(α) = sin(φ)sin(δ) + cos(φ)cos(δ)cos(ω)
    sin_alpha = (np.sin(lat_rad) * np.sin(delta) +
                 np.cos(lat_rad) * np.cos(delta) * np.cos(omega))

    # 确保值在有效范围内 [-1, 1]
    sin_alpha = np.clip(sin_alpha, -1.0, 1.0)

    # 计算太阳高度角 (弧度转角度)
    alpha = np.degrees(np.arcsin(sin_alpha))

    return alpha


def encode_spherical(lat, lon, radius=1.0):
    """
    将球面坐标转换为3D笛卡尔坐标

    参数:
    lat: 纬度 (-90 to 90)
    lon: 经度 (-180 to 180)
    radius: 球体半径 (默认1.0)

    返回:
    x, y, z: 3D笛卡尔坐标
    """
    lat = np.asarray(lat)
    lon = np.asarray(lon)

    # 转换为弧度
    lat_rad = np.radians(lat)
    lon_rad = np.radians(lon)

    # 计算3D坐标
    x = radius * np.cos(lat_rad) * np.cos(lon_rad)
    y = radius * np.cos(lat_rad) * np.sin(lon_rad)
    z = radius * np.sin(lat_rad)

    return x, y, z





if __name__ == "__main__":

    # dtype = torch.bfloat16
    # # 构造张量 [1, 2, 10, 435, 815]
    # tensor = torch.randn(1, 2, 10, 435, 815, dtype=dtype)
    #
    # # 指定保留的 channel 索引
    # channel_index = [0, 1, 4, 5]  # 保留 channel 0, 1, 4, 5，其他置为 0
    #
    # # 应用 mask
    # masked_tensor = mask_tensor(tensor, mask=None, channel_index=channel_index, dtype=dtype)
    #
    # # 可视化：选择 batch=0, time=0 的几个 channel 的 [h, w] 数据
    # fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    #
    # # 原张量（channel 0）
    # axes[0].imshow(tensor[0, 0, 0].cpu().to(torch.float16).numpy(), cmap='viridis')
    # axes[0].set_title("Original Tensor (b=0, t=0, c=0)")
    # axes[0].axis('off')
    #
    #
    # # Mask 后的张量（channel 0）
    # axes[1].imshow(masked_tensor[0, 0, 0].to(torch.float16).cpu().numpy(), cmap='viridis')
    # axes[1].set_title("Masked Tensor (b=0, t=0, c=0)")
    # axes[1].axis('off')
    #
    # plt.tight_layout()
    # plt.show()

    # # 测试编码函数
    #
    # def test_solar_elevation_functions():
    #     """
    #     测试太阳高度角计算函数和编码函数的有效性
    #     """
    #     # 创建测试数据
    #     np.random.seed(42)  # 设置随机种子以确保可重复性
    #
    #     # 生成一年的数据
    #     months = np.tile(np.arange(1, 13), 24)  # 每个月
    #     days = np.random.randint(1, 32, len(months))  # 随机日期
    #     hours = np.repeat(np.arange(0, 24), 12)  # 每个小时
    #
    #     # 固定位置：北京
    #     lat_beijing = 39.9
    #     lon_beijing = 116.4
    #     lats = np.full(len(months), lat_beijing)
    #     lons = np.full(len(months), lon_beijing)
    #
    #     # 计算太阳高度角
    #     elevations = calculate_solar_elevation(months, days, hours, lats, lons)
    #
    #     # 编码时间特征
    #     month_sin, month_cos = encode_month(months)
    #     day_norm = encode_day(days, months)
    #     hour_sin, hour_cos = encode_hour(hours)
    #
    #     # 创建图形
    #     fig = plt.figure(figsize=(15, 12))
    #     gs = GridSpec(3, 2, figure=fig)
    #
    #     # 1. 太阳高度角随时间变化
    #     ax1 = fig.add_subplot(gs[0, 0])
    #     time_index = np.arange(len(elevations))
    #     ax1.scatter(time_index, elevations, alpha=0.6, s=10)
    #     ax1.set_xlabel('时间索引')
    #     ax1.set_ylabel('太阳高度角 (°)')
    #     ax1.set_title('北京地区太阳高度角随时间变化')
    #     ax1.grid(True, alpha=0.3)
    #
    #     # 2. 按月份分组的太阳高度角
    #     ax2 = fig.add_subplot(gs[0, 1])
    #     monthly_avg = []
    #     monthly_std = []
    #     for month in range(1, 13):
    #         mask = months == month
    #         monthly_avg.append(np.mean(elevations[mask]))
    #         monthly_std.append(np.std(elevations[mask]))
    #
    #     ax2.bar(range(1, 13), monthly_avg, yerr=monthly_std,
    #             alpha=0.7, capsize=5)
    #     ax2.set_xlabel('月份')
    #     ax2.set_ylabel('平均太阳高度角 (°)')
    #     ax2.set_title('各月份太阳高度角统计')
    #     ax2.set_xticks(range(1, 13))
    #     ax2.grid(True, alpha=0.3)
    #
    #     # 3. 按小时分组的太阳高度角
    #     ax3 = fig.add_subplot(gs[1, 0])
    #     hourly_avg = []
    #     hourly_std = []
    #     for hour in range(0, 24):
    #         mask = hours == hour
    #         hourly_avg.append(np.mean(elevations[mask]))
    #         hourly_std.append(np.std(elevations[mask]))
    #
    #     ax3.bar(range(0, 24), hourly_avg, yerr=hourly_std,
    #             alpha=0.7, capsize=5)
    #     ax3.set_xlabel('小时 (UTC)')
    #     ax3.set_ylabel('平均太阳高度角 (°)')
    #     ax3.set_title('各小时太阳高度角统计')
    #     ax3.set_xticks(range(0, 24, 2))
    #     ax3.grid(True, alpha=0.3)
    #
    #     # 4. 编码特征的分布
    #     ax4 = fig.add_subplot(gs[1, 1])
    #     ax4.scatter(month_sin, month_cos, c=months, alpha=0.6, cmap='hsv')
    #     ax4.set_xlabel('Month Sin')
    #     ax4.set_ylabel('Month Cos')
    #     ax4.set_title('月份循环编码分布')
    #     ax4.grid(True, alpha=0.3)
    #     plt.colorbar(ax4.scatter(month_sin, month_cos, c=months, alpha=0.6, cmap='hsv'),
    #                  ax=ax4, label='月份')
    #
    #     # 5. 小时编码特征
    #     ax5 = fig.add_subplot(gs[2, 0])
    #     ax5.scatter(hour_sin, hour_cos, c=hours, alpha=0.6, cmap='viridis')
    #     ax5.set_xlabel('Hour Sin')
    #     ax5.set_ylabel('Hour Cos')
    #     ax5.set_title('小时循环编码分布')
    #     ax5.grid(True, alpha=0.3)
    #     plt.colorbar(ax5.scatter(hour_sin, hour_cos, c=hours, alpha=0.6, cmap='viridis'),
    #                  ax=ax5, label='小时')
    #
    #     # 6. 日期归一化分布
    #     ax6 = fig.add_subplot(gs[2, 1])
    #     ax6.hist(day_norm, bins=30, alpha=0.7, edgecolor='black')
    #     ax6.set_xlabel('归一化日期')
    #     ax6.set_ylabel('频次')
    #     ax6.set_title('日期归一化分布')
    #     ax6.grid(True, alpha=0.3)
    #
    #     plt.tight_layout()
    #     plt.savefig("test1.png")
    #     # plt.show()
    #
    #     # 打印统计信息
    #     print("=" * 50)
    #     print("测试结果统计:")
    #     print(f"数据点数量: {len(elevations)}")
    #     print(f"太阳高度角范围: {elevations.min():.2f}° - {elevations.max():.2f}°")
    #     print(f"太阳高度角均值: {elevations.mean():.2f}°")
    #     print(f"太阳高度角标准差: {elevations.std():.2f}°")
    #     print(f"正午时间(12:00 UTC)太阳高度角: {elevations[hours == 12].mean():.2f}°")
    #
    #     # 验证特殊日期
    #     print("\n特殊日期验证:")
    #     # 夏至 (6月21日)
    #     summer_mask = (months == 6) & (days == 21) & (hours == 12)
    #     if np.any(summer_mask):
    #         print(f"夏至正午太阳高度角: {elevations[summer_mask][0]:.2f}°")
    #
    #     # 冬至 (12月22日)
    #     winter_mask = (months == 12) & (days == 22) & (hours == 12)
    #     if np.any(winter_mask):
    #         print(f"冬至正午太阳高度角: {elevations[winter_mask][0]:.2f}°")
    #
    # def test_multiple_locations():
    #     """
    #     测试不同地理位置的太阳高度角
    #     """
    #     # 测试不同城市
    #     cities = {
    #         '北京': (39.9, 116.4),
    #         '上海': (31.2, 121.5),
    #         '广州': (23.1, 113.3),
    #         '哈尔滨': (45.8, 126.6),
    #         '乌鲁木齐': (43.8, 87.6)
    #     }
    #
    #     # 夏至正午
    #     month = np.array([6])
    #     day = np.array([21])
    #     hour = np.array([12])
    #
    #     fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    #
    #     latitudes = []
    #     elevations = []
    #     city_names = []
    #
    #     for city, (lat, lon) in cities.items():
    #         lat_arr = np.array([lat])
    #         lon_arr = np.array([lon])
    #
    #         elevation = calculate_solar_elevation(month, day, hour, lat_arr, lon_arr)
    #
    #         latitudes.append(lat)
    #         elevations.append(elevation[0])
    #         city_names.append(city)
    #
    #         print(f"{city}: 纬度 {lat}°, 夏至正午太阳高度角 {elevation[0]:.2f}°")
    #
    #     # 绘制纬度与太阳高度角的关系
    #     ax[0].scatter(latitudes, elevations)
    #     for i, city in enumerate(city_names):
    #         ax[0].annotate(city, (latitudes[i], elevations[i]), xytext=(5, 5),
    #                        textcoords='offset points')
    #     ax[0].set_xlabel('纬度 (°)')
    #     ax[0].set_ylabel('太阳高度角 (°)')
    #     ax[0].set_title('不同纬度夏至正午太阳高度角')
    #     ax[0].grid(True, alpha=0.3)
    #
    #     # 绘制理论曲线 (夏至太阳直射北回归线23.5°N)
    #     theoretical_lats = np.linspace(0, 90, 100)
    #     theoretical_elev = 90 - np.abs(theoretical_lats - 23.5)
    #     ax[0].plot(theoretical_lats, theoretical_elev, 'r--', alpha=0.7, label='理论值')
    #     ax[0].legend()
    #
    #     # 测试不同季节
    #     seasons = {
    #         '春分(3.21)': (3, 21),
    #         '夏至(6.21)': (6, 21),
    #         '秋分(9.23)': (9, 23),
    #         '冬至(12.22)': (12, 22)
    #     }
    #
    #     beijing_lat = np.array([39.9])
    #     beijing_lon = np.array([116.4])
    #     hour_test = np.array([12])
    #
    #     season_elevations = []
    #     season_names = []
    #
    #     for season, (m, d) in seasons.items():
    #         month_test = np.array([m])
    #         day_test = np.array([d])
    #
    #         elevation = calculate_solar_elevation(month_test, day_test, hour_test,
    #                                               beijing_lat, beijing_lon)
    #
    #         season_elevations.append(elevation[0])
    #         season_names.append(season)
    #
    #         print(f"北京 {season}: 太阳高度角 {elevation[0]:.2f}°")
    #
    #     # 绘制不同季节的太阳高度角
    #     ax[1].bar(season_names, season_elevations, alpha=0.7)
    #     ax[1].set_xlabel('季节')
    #     ax[1].set_ylabel('太阳高度角 (°)')
    #     ax[1].set_title('北京不同季节正午太阳高度角')
    #     ax[1].grid(True, alpha=0.3)
    #     plt.xticks(rotation=45)
    #
    #     plt.tight_layout()
    #     # plt.show()
    #     plt.savefig("test2.png")
    # def test_solar_elevation_cst():
    #     """使用CST时间测试太阳高度角"""
    #
    #     print("=" * 50)
    #     print("使用CST时间测试太阳高度角")
    #     print("=" * 50)
    #
    #     # 测试不同城市夏至正午（CST时间12:00 = UTC时间4:00）
    #     cities = {
    #         '北京': (39.9, 116.4),
    #         '上海': (31.2, 121.5),
    #         '广州': (23.1, 113.3),
    #         '哈尔滨': (45.8, 126.6),
    #         '乌鲁木齐': (43.8, 87.6)
    #     }
    #
    #     month = np.array([6])
    #     day = np.array([21])
    #     hour_utc = np.array([4])  # CST 12:00 = UTC 4:00
    #
    #     for city, (lat, lon) in cities.items():
    #         lat_arr = np.array([lat])
    #         lon_arr = np.array([lon])
    #
    #         elevation = calculate_solar_elevation(month, day, hour_utc, lat_arr, lon_arr)
    #
    #         # 理论值计算：夏至太阳直射北回归线23.5°N
    #         theoretical = 90 - abs(lat - 23.5)
    #
    #         print(f"{city}: 纬度 {lat}°, 太阳高度角 {elevation[0]:.2f}°, 理论值 {theoretical:.2f}°")
    #
    # def test_beijing_seasonal():
    #     """测试北京不同季节的正午太阳高度角"""
    #
    #     print("\n" + "=" * 50)
    #     print("北京不同季节正午太阳高度角")
    #     print("=" * 50)
    #
    #     seasons = {
    #         '春分(3.21)': (3, 21),
    #         '夏至(6.21)': (6, 21),
    #         '秋分(9.23)': (9, 23),
    #         '冬至(12.22)': (12, 22)
    #     }
    #
    #     beijing_lat = np.array([39.9])
    #     beijing_lon = np.array([116.4])
    #     hour_utc = np.array([4])  # CST 12:00 = UTC 4:00
    #
    #     for season, (m, d) in seasons.items():
    #         month_test = np.array([m])
    #         day_test = np.array([d])
    #
    #         elevation = calculate_solar_elevation(month_test, day_test, hour_utc,
    #                                               beijing_lat, beijing_lon)
    #
    #         print(f"{season}: 太阳高度角 {elevation[0]:.2f}°")
    #
    # def test_daily_variation():
    #     """测试一天中太阳高度角的变化"""
    #
    #     # 北京夏至日
    #     month = np.array([6])
    #     day = np.array([21])
    #     lat = np.array([39.9])
    #     lon = np.array([116.4])
    #
    #     # 生成UTC时间0-23小时（对应CST时间8:00-次日7:00）
    #     hours_utc = np.arange(0, 24)
    #     elevations = []
    #
    #     for hour in hours_utc:
    #         elev = calculate_solar_elevation(month, day, np.array([hour]), lat, lon)
    #         elevations.append(elev[0])
    #
    #     # 绘制图表
    #     plt.figure(figsize=(12, 6))
    #
    #     # UTC时间
    #     plt.subplot(1, 2, 1)
    #     plt.plot(hours_utc, elevations, 'b-', linewidth=2)
    #     plt.axhline(0, color='gray', linestyle='--', alpha=0.5)
    #     plt.xlabel('UTC时间 (小时)')
    #     plt.ylabel('太阳高度角 (°)')
    #     plt.title('北京夏至日太阳高度角变化（UTC时间）')
    #     plt.grid(True, alpha=0.3)
    #
    #     # 转换为CST时间显示
    #     plt.subplot(1, 2, 2)
    #     cst_hours = [(h + 8) % 24 for h in hours_utc]  # UTC+8
    #     plt.plot(cst_hours, elevations, 'r-', linewidth=2)
    #     plt.axhline(0, color='gray', linestyle='--', alpha=0.5)
    #     plt.xlabel('CST时间 (小时)')
    #     plt.ylabel('太阳高度角 (°)')
    #     plt.title('北京夏至日太阳高度角变化（CST时间）')
    #     plt.grid(True, alpha=0.3)
    #
    #     plt.tight_layout()
    #     plt.show()
    #
    #     # 找到正午时间（太阳高度角最大时）
    #     max_elevation = max(elevations)
    #     max_index = elevations.index(max_elevation)
    #     print(f"\n最高太阳高度角: {max_elevation:.2f}°")
    #     print(f"对应UTC时间: {max_index}:00")
    #     print(f"对应CST时间: {(max_index + 8) % 24}:00")
    #
    # test_solar_elevation_functions()
    # test_multiple_locations()
    # test_solar_elevation_cst()
    # test_beijing_seasonal()
    # # test_daily_variation()
    #
    #
    #
    # def test_encode_lat_lon():
    #     """测试经纬度编码函数"""
    #
    #     # 测试数据
    #     test_points = [
    #         (0, 0),        # 赤道，本初子午线
    #         (39.9, 116.4), # 北京
    #         (31.2, 121.5), # 上海
    #         (23.1, 113.3), # 广州
    #         (45.8, 126.6), # 哈尔滨
    #         (-33.9, 151.2), # 悉尼
    #         (40.7, -74.0), # 纽约
    #         (51.5, -0.1),  # 伦敦
    #         (-23.5, -46.6), # 圣保罗
    #         (90, 0),       # 北极
    #         (-90, 0)       # 南极
    #     ]
    #
    #     print("经纬度编码测试:")
    #     print("=" * 60)
    #
    #     for i, (lat, lon) in enumerate(test_points):
    #         lat_arr = np.array([lat])
    #         lon_arr = np.array([lon])
    #
    #         encoded = encode_lat_lon(lat_arr, lon_arr)
    #
    #         print(f"点 {i+1}: 纬度 {lat:6.1f}°, 经度 {lon:6.1f}°")
    #         print(f"  归一化: lat={encoded['lat_norm'][0]:.3f}, lon={encoded['lon_norm'][0]:.3f}")
    #         print(f"  循环编码: lat_sin={encoded['lat_sin'][0]:.3f}, lat_cos={encoded['lat_cos'][0]:.3f}")
    #         print(f"            lon_sin={encoded['lon_sin'][0]:.3f}, lon_cos={encoded['lon_cos'][0]:.3f}")
    #         print(f"  半球: {'北半球' if encoded['hemisphere'][0] == 1 else '南半球'}")
    #         print("-" * 40)
    #
    # def visualize_lat_lon_encoding():
    #     """可视化经纬度编码效果"""
    #
    #     # 创建网格数据
    #     lats = np.linspace(-90, 90, 100)
    #     lons = np.linspace(-180, 180, 100)
    #     lat_grid, lon_grid = np.meshgrid(lats, lons)
    #
    #     # 编码
    #     encoded = encode_lat_lon(lat_grid.flatten(), lon_grid.flatten())
    #
    #     # 重塑为2D数组用于可视化
    #     lat_norm_2d = encoded['lat_norm'].reshape(100, 100)
    #     lon_norm_2d = encoded['lon_norm'].reshape(100, 100)
    #     lat_sin_2d = encoded['lat_sin'].reshape(100, 100)
    #     lat_cos_2d = encoded['lat_cos'].reshape(100, 100)
    #     lon_sin_2d = encoded['lon_sin'].reshape(100, 100)
    #     lon_cos_2d = encoded['lon_cos'].reshape(100, 100)
    #
    #     # 绘制
    #     fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    #
    #     # 归一化纬度
    #     im1 = axes[0, 0].imshow(lat_norm_2d, extent=[-180, 180, -90, 90],
    #                             cmap='viridis', aspect='auto')
    #     axes[0, 0].set_title('Normalized Latitude')
    #     axes[0, 0].set_xlabel('Longitude')
    #     axes[0, 0].set_ylabel('Latitude')
    #     plt.colorbar(im1, ax=axes[0, 0])
    #
    #     # 归一化经度
    #     im2 = axes[0, 1].imshow(lon_norm_2d, extent=[-180, 180, -90, 90],
    #                             cmap='viridis', aspect='auto')
    #     axes[0, 1].set_title('Normalized Longitude')
    #     axes[0, 1].set_xlabel('Longitude')
    #     axes[0, 1].set_ylabel('Latitude')
    #     plt.colorbar(im2, ax=axes[0, 1])
    #
    #     # 纬度正弦编码
    #     im3 = axes[0, 2].imshow(lat_sin_2d, extent=[-180, 180, -90, 90],
    #                             cmap='coolwarm', aspect='auto')
    #     axes[0, 2].set_title('Latitude Sine Encoding')
    #     axes[0, 2].set_xlabel('Longitude')
    #     axes[0, 2].set_ylabel('Latitude')
    #     plt.colorbar(im3, ax=axes[0, 2])
    #
    #     # 纬度余弦编码
    #     im4 = axes[1, 0].imshow(lat_cos_2d, extent=[-180, 180, -90, 90],
    #                             cmap='coolwarm', aspect='auto')
    #     axes[1, 0].set_title('Latitude Cosine Encoding')
    #     axes[1, 0].set_xlabel('Longitude')
    #     axes[1, 0].set_ylabel('Latitude')
    #     plt.colorbar(im4, ax=axes[1, 0])
    #
    #     # 经度正弦编码
    #     im5 = axes[1, 1].imshow(lon_sin_2d, extent=[-180, 180, -90, 90],
    #                             cmap='coolwarm', aspect='auto')
    #     axes[1, 1].set_title('Longitude Sine Encoding')
    #     axes[1, 1].set_xlabel('Longitude')
    #     axes[1, 1].set_ylabel('Latitude')
    #     plt.colorbar(im5, ax=axes[1, 1])
    #
    #     # 经度余弦编码
    #     im6 = axes[1, 2].imshow(lon_cos_2d, extent=[-180, 180, -90, 90],
    #                             cmap='coolwarm', aspect='auto')
    #     axes[1, 2].set_title('Longitude Cosine Encoding')
    #     axes[1, 2].set_xlabel('Longitude')
    #     axes[1, 2].set_ylabel('Latitude')
    #     plt.colorbar(im6, ax=axes[1, 2])
    #
    #     plt.tight_layout()
    #     plt.show()
    #
    # test_encode_lat_lon()
    # visualize_lat_lon_encoding()


    results = seq2seq_timeseries(
        init_time=datetime(2015, 1, 1, 22, 30),
        past_len=6,
        future_len=6,
        interval=3,
        rolling_num=5,
    )

    print("debug")






