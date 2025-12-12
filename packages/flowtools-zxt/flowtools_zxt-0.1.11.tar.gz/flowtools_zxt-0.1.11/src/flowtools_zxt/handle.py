import pandas as pd
import numpy as np
import xarray as xr
import warnings
import smbclient
import os

from datetime import datetime, timedelta
from io import BytesIO

warnings.filterwarnings("ignore")


def get_dem(
        lon=None,
        lat=None,
        vars=["z"],
        get_values=False,
        interp_lon=None,
        interp_lat=None,
        add_arounds=False,
        file_path="/mnt/external_disk0/Auxiliary_data/etopo2_new.nc",
):
    """
    获取地形高程数据(DEM)

    参数:
        lon: 经度(可选)
        lat: 纬度(可选)
        vars: 变量列表(默认为["dem"])
        get_values: 是否返回数值而非DataArray(默认为False)
        interp_lon: 插值经度(可选)
        interp_lat: 插值纬度(可选)
        add_arounds: 是否添加周边网格数据(默认为False)

    返回:
        包含DEM数据的字典
    """
    # 1. 扩展变量列表
    extended_vars = []
    for var in vars:
        extended_vars.append(var)
        if add_arounds:
            extended_vars.extend([f"{var}_{i}" for i in range(1, 9)])

    # 2. 构建完整字典
    data_dict = {}
    for var in extended_vars:
        if "_" in var:
            base_var, shift_idx = var.split("_")
            shift_idx = int(shift_idx)
            shifts = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            lon_shift, lat_shift = shifts[shift_idx - 1]
        else:
            base_var = var
            lon_shift, lat_shift = 0, 0

        # 加载并重命名DataArray
        if base_var not in data_dict:
            with xr.open_dataset(file_path) as f:
                data_dict[base_var] = f[base_var].rename({'x': 'lon', 'y': 'lat'}).rename(base_var)

        # 应用偏移
        if lon_shift != 0 or lat_shift != 0:
            data_dict[var] = data_dict[base_var].shift(
                lon=lon_shift, lat=lat_shift, fill_value=np.nan
            ).rename(var)
        else:
            data_dict[var] = data_dict[base_var].rename(var)

    # 3. 应用插值
    if interp_lon is not None and interp_lat is not None:
        for var, da in data_dict.items():
            data_dict[var] = da.interp(lon=interp_lon, lat=interp_lat)

    # 4. 提取结果
    result = {}
    if lon is not None and lat is not None:
        for var, da in data_dict.items():
            result[var] = da.sel(lon=lon, lat=lat, method="nearest")
            if get_values:
                result[var] = result[var].values
    else:
        for var, da in data_dict.items():
            result[var] = da.values if get_values else da

    return result


def get_cra_surface_meteos(
        year=None,
        month=None,
        day=None,
        hour=None,
        lon=None,
        lat=None,
        vars=["t2m", "sh2", "u10", "v10"],
        get_values=True,
        interp_lon=None,
        interp_lat=None,
        add_arounds=False,
        file_structure="/data/CRA/surface/{YYYY}/{YYYYMMDD}/ART_ATM_GLB_0P10_6HOR_SANL_{YYYYMMDDHH}.grib2"
):
    """
    通用化的气象数据获取函数

    Parameters:
    file_structure: 文件路径模板，支持以下占位符：
        {YYYY} - 4位年份
        {YY} - 2位年份
        {MM} - 2位月份
        {DD} - 2位日期
        {HH} - 2位小时
        {YYYYMMDD} - 8位日期
        {YYYYMMDDHH} - 10位日期时间
    """

    # 1. 构建文件路径
    if file_structure:
        # 确保输入是整数
        year = int(year) if year else datetime.now().year
        month = int(month) if month else 1
        day = int(day) if day else 1
        hour = int(hour) if hour else 0

        # 替换占位符
        file_path = file_structure.format(
            YYYY=year,
            YY=str(year)[-2:],
            MM=f"{month:02d}",
            DD=f"{day:02d}",
            HH=f"{hour:02d}",
            YYYYMMDD=f"{year}{month:02d}{day:02d}",
            YYYYMMDDHH=f"{year}{month:02d}{day:02d}{hour:02d}"
        )
    else:
        # 使用原来的固定路径（向后兼容）
        file_path = f"/data/CRA/surface/{year}/{year}{month:02d}{day:02d}/ART_ATM_GLB_0P10_6HOR_SANL_{year}{month:02d}{day:02d}{hour:02d}.grib2"

    # 2. 检查文件是否存在
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"数据文件不存在: {file_path}")

    # 3. 扩展变量列表
    extended_vars = []
    for var in vars:
        extended_vars.append(var)
        if add_arounds:
            extended_vars.extend([f"{var}_{i}" for i in range(1, 9)])

    # 4. 构建完整字典
    data_dict = {}
    f1 = xr.open_dataset(file_path, backend_kwargs={'indexpath': '', 'filter_by_keys': {'typeOfLevel': 'heightAboveGround', 'level': 2}})
    f2 = xr.open_dataset(file_path, backend_kwargs={'indexpath': '', 'filter_by_keys': {'typeOfLevel': 'heightAboveGround', 'level': 10}})

    for var in extended_vars:
        # 解析变量名和偏移量
        if "_" in var:
            base_var, shift_idx = var.split("_")
            shift_idx = int(shift_idx)
            shifts = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            lon_shift, lat_shift = shifts[shift_idx - 1]
        else:
            base_var = var
            lon_shift, lat_shift = 0, 0

        # 加载并重命名DataArray
        if base_var not in data_dict:
            if base_var[:3] in ["t2m", "sh2"]:
                data_dict[base_var] = f1[base_var].rename({'longitude': 'lon','latitude': 'lat'}).rename(base_var)
            elif base_var[:3] in ["u10", "v10"]:
                data_dict[base_var] = f2[base_var].rename({'longitude': 'lon','latitude': 'lat'}).rename(base_var)

        # 应用偏移
        if lon_shift != 0 or lat_shift != 0:
            data_dict[var] = data_dict[base_var].shift(
                lon=lon_shift, lat=lat_shift, fill_value=np.nan
            ).rename(var)
        else:
            # 确保原始数据使用正确的名称
            data_dict[var] = data_dict[base_var].rename(var)

    # 5. 应用插值
    if interp_lon is not None and interp_lat is not None:
        for var, da in data_dict.items():
            data_dict[var] = da.interp(lon=interp_lon, lat=interp_lat)

    # 6. 提取结果
    result = {}
    if lon is not None and lat is not None:
        for var, da in data_dict.items():
            result[var] = da.sel(lon=lon, lat=lat, method="nearest")
            if get_values:
                result[var] = result[var].values
    else:
        for var, da in data_dict.items():
            result[var] = da.values if get_values else da

    return result



def get_cra_surface_80m_meteos(
        year=None,
        month=None,
        day=None,
        hour=None,
        lon=None,
        lat=None,
        vars=["UGRD", "VGRD", "PRES", "PWAT", "SPFH", "TMP"],
        get_values=True,
        interp_lon=None,
        interp_lat=None,
        add_arounds=False,
        file_structure="/data2/CRA/surface_80m/{YYYY}/{YYYYMM}/{YYYYMMDD}/ART_ATM_GLB_0P10_1HOR_ANAL_{YYYYMMDDHH}_{VAR}.grib2"
):
    """
    通用化的80米高度气象数据获取函数

    Parameters:
    file_structure: 文件路径模板，支持以下占位符：
        {YYYY} - 4位年份
        {MM} - 2位月份
        {DD} - 2位日期
        {HH} - 2位小时
        {YYYYMM} - 6位年月
        {YYYYMMDD} - 8位日期
        {YYYYMMDDHH} - 10位日期时间
        {VAR} - 变量名（会自动映射）
    """

    # 变量名映射字典
    var_dict = {
        "PRES": "pres",
        "PWAT": "pwat",
        "SPFH": "q",
        "TMP": "t",
        "UGRD": "u",
        "VGRD": "v"
    }

    # 1. 扩展变量列表
    extended_vars = []
    for var in vars:
        extended_vars.append(var)
        if add_arounds:
            extended_vars.extend([f"{var}_{i}" for i in range(1, 9)])

    # 2. 构建完整字典
    data_dict = {}

    # 确保输入是整数
    year = int(year) if year else datetime.now().year
    month = int(month) if month else 1
    day = int(day) if day else 1
    hour = int(hour) if hour else 0

    for var in extended_vars:
        # 解析变量名和偏移量
        if "_" in var:
            base_var, shift_idx = var.split("_")
            shift_idx = int(shift_idx)
            shifts = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            lon_shift, lat_shift = shifts[shift_idx - 1]
        else:
            base_var = var
            lon_shift, lat_shift = 0, 0

        # 加载并重命名DataArray
        if base_var not in data_dict:
            # 构建文件路径
            if file_structure:
                file_path = file_structure.format(
                    YYYY=year,
                    MM=f"{month:02d}",
                    DD=f"{day:02d}",
                    HH=f"{hour:02d}",
                    YYYYMM=f"{year}{month:02d}",
                    YYYYMMDD=f"{year}{month:02d}{day:02d}",
                    YYYYMMDDHH=f"{year}{month:02d}{day:02d}{hour:02d}",
                    VAR=base_var  # 注意：这里是原始变量名，不是映射后的
                )
            else:
                # 使用原来的固定路径（向后兼容）
                file_path = f"/data2/CRA/surface_80m/{year}/{year}{month:02d}/{year}{month:02d}{day:02d}/ART_ATM_GLB_0P10_1HOR_ANAL_{year}{month:02d}{day:02d}{hour:02d}_{base_var}.grib2"

            # 检查文件是否存在
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"数据文件不存在: {file_path}")

            # 打开文件并读取数据
            with xr.open_dataset(file_path, backend_kwargs={'indexpath': ''}) as f:
                # 使用映射后的变量名读取数据
                mapped_var_name = var_dict[base_var]
                data_dict[base_var] = f[mapped_var_name].rename({'longitude': 'lon','latitude': 'lat'}).rename(base_var)

        # 应用偏移
        if lon_shift != 0 or lat_shift != 0:
            data_dict[var] = data_dict[base_var].shift(
                lon=lon_shift, lat=lat_shift, fill_value=np.nan
            ).rename(var)
        else:
            # 确保原始数据使用正确的名称
            data_dict[var] = data_dict[base_var].rename(var)

    # 3. 应用插值
    if interp_lon is not None and interp_lat is not None:
        for var, da in data_dict.items():
            data_dict[var] = da.interp(lon=interp_lon, lat=interp_lat)

    # 4. 提取结果
    result = {}
    if lon is not None and lat is not None:
        for var, da in data_dict.items():
            result[var] = da.sel(lon=lon, lat=lat, method="nearest")
            if get_values:
                result[var] = result[var].values
    else:
        for var, da in data_dict.items():
            result[var] = da.values if get_values else da

    return result


def get_cra_atmos_meteos(
        year=None,
        month=None,
        day=None,
        hour=None,
        lon=None,
        lat=None,
        vars=["RH", "UGRD", "VGRD", "HGT", "SPFH", "TMP"],
        pressure_levels=["1000", "900", "800", "700", "600", "500"],
        get_values=True,
        interp_lon=None,
        interp_lat=None,
        add_arounds=False,
        file_structure="/data2/CRA/atmos/{YYYY}/{YYYYMM}/{YYYYMMDD}/ART_ATM_GLB_0P10_1HOR_ANAL_{YYYYMMDDHH}_{VAR}.grib2"
):
    """
    通用化的大气层气象数据获取函数

    Parameters:
    file_structure: 文件路径模板，支持以下占位符：
        {YYYY} - 4位年份
        {MM} - 2位月份
        {DD} - 2位日期
        {HH} - 2位小时
        {YYYYMM} - 6位年月
        {YYYYMMDD} - 8位日期
        {YYYYMMDDHH} - 10位日期时间
        {VAR} - 变量名（会自动映射）
    """

    # 变量名映射字典
    var_dict = {
        "HGT": "gh",
        "SPFH": "q",
        "TMP": "t",
        "UGRD": "u",
        "VGRD": "v",
        "RH": "r",
    }

    # 1. 构建扩展变量列表，仅包含带压力水平的变量
    extended_vars = []
    for var in vars:
        for level in pressure_levels:
            extended_vars.append(f"{var}_{level}")
        if add_arounds:
            for level in pressure_levels:
                extended_vars.extend([f"{var}_{level}_{i}" for i in range(1, 9)])

    # 2. 构建数据字典
    data_dict = {}

    # 确保输入是整数
    year = int(year) if year else datetime.now().year
    month = int(month) if month else 1
    day = int(day) if day else 1
    hour = int(hour) if hour else 0

    for var in extended_vars:
        # 解析变量名、压力水平和可能的偏移量
        parts = var.split("_")
        if len(parts) == 3:  # 例如 u_1000_1
            base_var, level, shift_idx = parts
            shift_idx = int(shift_idx)
            shifts = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            lon_shift, lat_shift = shifts[shift_idx - 1]
        else:  # 例如 u_1000
            base_var, level = parts
            lon_shift, lat_shift = 0, 0

        # 加载基础变量数据（仅加载一次）
        if base_var not in data_dict:
            # 构建文件路径
            if file_structure:
                file_path = file_structure.format(
                    YYYY=year,
                    MM=f"{month:02d}",
                    DD=f"{day:02d}",
                    HH=f"{hour:02d}",
                    YYYYMM=f"{year}{month:02d}",
                    YYYYMMDD=f"{year}{month:02d}{day:02d}",
                    YYYYMMDDHH=f"{year}{month:02d}{day:02d}{hour:02d}",
                    VAR=base_var  # 原始变量名
                )
            else:
                # 使用原来的固定路径（向后兼容）
                file_path = f"/data2/CRA/atmos/{year}/{year}{month:02d}/{year}{month:02d}{day:02d}/ART_ATM_GLB_0P10_1HOR_ANAL_{year}{month:02d}{day:02d}{hour:02d}_{base_var}.grib2"

            # 检查文件是否存在
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"数据文件不存在: {file_path}")

            # 打开文件并读取数据
            with xr.open_dataset(file_path, backend_kwargs={'indexpath': ''}) as f:
                # 使用映射后的变量名读取数据
                mapped_var_name = var_dict[base_var]
                data_dict[base_var] = f[mapped_var_name].rename({'longitude': 'lon', 'latitude': 'lat'})

        # 提取特定压力水平的数据
        da = data_dict[base_var].sel(isobaricInhPa=level).rename(var)

        # 应用偏移
        if lon_shift != 0 or lat_shift != 0:
            data_dict[var] = da.shift(lon=lon_shift, lat=lat_shift, fill_value=np.nan).rename(var)
        else:
            data_dict[var] = da

    # 移除临时存储的基础变量（不带压力水平）
    for var in vars:
        if var in data_dict:
            del data_dict[var]

    # 3. 应用插值
    if interp_lon is not None and interp_lat is not None:
        for var, da in data_dict.items():
            data_dict[var] = da.interp(lon=interp_lon, lat=interp_lat)

    # 4. 提取结果
    result = {}
    if lon is not None and lat is not None:
        for var, da in data_dict.items():
            result[var] = da.sel(lon=lon, lat=lat, method="nearest")
            if get_values:
                result[var] = result[var].values
    else:
        for var, da in data_dict.items():
            result[var] = da.values if get_values else da

    return result




def get_gem_emissions(
        year=None,
        month=None,
        lon=None,
        lat=None,
        vars=["BC", "CO", "CO2", "NOx", "OC", "PM10", "PM25", "SO2", "TSP"],
        get_values=True,
        interp_lon=None,
        interp_lat=None,
        add_arounds=False,
        file_structure="/mnt/external_disk0/GEMS/nc_month/{VAR}/tot/GEMS_tot_{VAR}_{YYYY}_monthly.nc"
):
    """
    通用化的GEMS排放数据获取函数

    Parameters:
    file_structure: 文件路径模板，支持以下占位符：
        {YYYY} - 4位年份
        {MM} - 2位月份
        {VAR} - 变量名
    """

    # 确保输入是整数
    year = int(year) if year else datetime.now().year
    month = int(month) if month else 1

    # 年份限制（保持原有逻辑）
    if year >= 2019:
        year = 2019

    # 1. 扩展变量列表
    extended_vars = []
    for var in vars:
        extended_vars.append(var)
        if add_arounds:
            extended_vars.extend([f"{var}_{i}" for i in range(1, 9)])

    # 2. 构建完整字典
    data_dict = {}
    for var in extended_vars:
        if "_" in var:
            base_var, shift_idx = var.split("_")
            shift_idx = int(shift_idx)
            shifts = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            lon_shift, lat_shift = shifts[shift_idx - 1]
        else:
            base_var = var
            lon_shift, lat_shift = 0, 0

        # 加载并重命名DataArray
        if base_var not in data_dict:
            # 构建文件路径
            if file_structure:
                file_path = file_structure.format(
                    YYYY=year,
                    MM=f"{month:02d}",
                    VAR=base_var
                )
            else:
                # 使用原来的固定路径（向后兼容）
                file_path = f"/mnt/external_disk0/GEMS/nc_month/{base_var}/tot/GEMS_tot_{base_var}_{year}_monthly.nc"

            # 检查文件是否存在
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"排放数据文件不存在: {file_path}")

            # 打开文件并读取数据
            with xr.open_dataset(file_path) as f:
                # 这里重命名DataArray
                data_dict[base_var] = f["emission"][month - 1].rename({'lon': 'lon','lat': 'lat'}).rename(base_var)

        # 应用偏移
        if lon_shift != 0 or lat_shift != 0:
            data_dict[var] = data_dict[base_var].shift(
                lon=lon_shift, lat=lat_shift, fill_value=np.nan
            ).rename(var)  # 偏移后的DataArray也重命名
        else:
            # 确保原始数据使用正确的名称
            data_dict[var] = data_dict[base_var].rename(var)

    # 3. 应用插值
    if interp_lon is not None and interp_lat is not None:
        for var, da in data_dict.items():
            data_dict[var] = da.interp(lon=interp_lon, lat=interp_lat)

    # 4. 提取结果
    result = {}
    if lon is not None and lat is not None:
        for var, da in data_dict.items():
            result[var] = da.sel(lon=lon, lat=lat, method="nearest")
            if get_values:
                result[var] = result[var].values
    else:
        for var, da in data_dict.items():
            result[var] = da.values if get_values else da

    return result


def get_cams_chms(
        year=None,
        month=None,
        day=None,
        hour=None,
        lon=None,
        lat=None,
        vars=["PM10", "PM25", "AOD"],
        get_values=True,
        interp_lon=None,
        interp_lat=None,
        add_arounds=False,
        add_tag=True,
        file_structure_fcst00H="/mnt/external_disk0/ECMWF-CAMS/fcst-00H/{YYYY}-{MM}-{DD}.grib",
        file_structure_fcst12H="/mnt/external_disk0/ECMWF-CAMS/fcst-12H/{YYYY}-{MM}-{DD}.grib"
):
    """
    通用化的CAMS数据获取函数

    Parameters:
    file_structure_fcst00H: 00时预报文件路径模板
    file_structure_fcst12H: 12时预报文件路径模板
    支持以下占位符：
        {YYYY} - 4位年份
        {MM} - 2位月份
        {DD} - 2位日期
        {HH} - 2位小时
    """

    # 确保输入是整数
    year = int(year) if year else datetime.now().year
    month = int(month) if month else 1
    day = int(day) if day else 1
    hour = int(hour) if hour else 0

    current_date = datetime(year=year, month=month, day=day, hour=hour)

    # 1. 扩展变量列表
    extended_vars = []
    for var in vars:
        extended_vars.append(var)
        if add_arounds:
            extended_vars.extend([f"{var}_{i}" for i in range(1, 9)])

    # 2. 构建完整字典
    data_dict = {}
    for var in extended_vars:
        # 解析变量名和偏移量
        if "_" in var:  # 处理带偏移的后缀
            base_var, shift_idx = var.split("_")
            shift_idx = int(shift_idx)
            shifts = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            lon_shift, lat_shift = shifts[shift_idx - 1]
        else:
            base_var = var
            lon_shift, lat_shift = 0, 0

        # 加载数据（每个基础变量只加载一次）
        base_var_key = f"{base_var}_cams" if add_tag else base_var
        if base_var_key not in data_dict:

            # 文件读取逻辑
            if 6 <= hour <= 17:
                # 06-17时使用当天00Z预报
                if file_structure_fcst00H:
                    file_path = file_structure_fcst00H.format(
                        YYYY=year,
                        MM=f"{month:02d}",
                        DD=f"{day:02d}",
                        HH=f"{hour:02d}"
                    )
                else:
                    file_path = f"/mnt/external_disk0/ECMWF-CAMS/fcst-00H/{year}-{month:02d}-{day:02d}.grib"
                step = hour  # 06时对应第6小时，07时对应第7小时，以此类推
            else:
                # 18时-次日05时使用12Z预报
                if 18 <= hour <= 23:
                    # 当天18-23时使用当天12Z预报
                    if file_structure_fcst12H:
                        file_path = file_structure_fcst12H.format(
                            YYYY=year,
                            MM=f"{month:02d}",
                            DD=f"{day:02d}",
                            HH=f"{hour:02d}"
                        )
                    else:
                        file_path = f"/mnt/external_disk0/ECMWF-CAMS/fcst-12H/{year}-{month:02d}-{day:02d}.grib"
                    step = hour - 12  # 18时对应第6小时，19时对应第7小时，以此类推
                else:
                    # 00-05时使用前一天12Z预报
                    prev_date = current_date - timedelta(days=1)
                    if file_structure_fcst12H:
                        file_path = file_structure_fcst12H.format(
                            YYYY=prev_date.year,
                            MM=f"{prev_date.month:02d}",
                            DD=f"{prev_date.day:02d}",
                            HH=f"{hour:02d}"
                        )
                    else:
                        file_path = f"/mnt/external_disk0/ECMWF-CAMS/fcst-12H/{prev_date.year}-{prev_date.month:02d}-{prev_date.day:02d}.grib"
                    step = hour + 12  # 00时对应第12小时，01时对应第13小时，以此类推

            # 检查文件是否存在
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"CAMS数据文件不存在: {file_path}")

            # 直接打开文件
            f = xr.open_dataset(file_path, backend_kwargs={'indexpath': ''})
            f = f.rename({"pm10": "PM10", "pm2p5": "PM25", "aod550": "AOD", "gtco3": "columnO3", "tchcho": "columnCH2O", "tcno2": "columnNO2"})
            f = f.isel(step=step)

            # 修正坐标名称并重命名 DataArray
            new_name = f"{base_var}_cams" if add_tag else base_var
            da = f[base_var].rename({'longitude': 'lon', 'latitude': 'lat'}).rename(new_name)
            if base_var.startswith("PM") or base_var.startswith("column"):
                da = da * 1e9
                m = da.max().item()
                if da.max().item() == 0:
                    raise ValueError(f"CAMS初始场全为0（bug），因此跳过")

            data_dict[new_name] = da

        # 应用偏移（如果需要）
        if lon_shift != 0 or lat_shift != 0:
            new_name = f"{var}_cams" if add_tag else var
            data_dict[new_name] = data_dict[base_var_key].shift(
                lon=lon_shift, lat=lat_shift, fill_value=np.nan
            ).rename(new_name)

    # 3. 应用插值
    if interp_lon is not None and interp_lat is not None:
        for var, da in list(data_dict.items()):  # 使用 list 避免运行时修改字典
            data_dict[var] = da.interp(lon=interp_lon, lat=interp_lat)

    # 4. 提取结果
    result = {}
    if lon is not None and lat is not None:
        # 提取特定点的数据
        for var, da in data_dict.items():
            point_data = da.sel(lon=lon, lat=lat, method="nearest")
            result[var] = point_data.values if get_values else point_data
    else:
        # 提取全部数据
        for var, da in data_dict.items():
            result[var] = da.values if get_values else da

    return result


# def get_retrieval(
#         year=None,
#         month=None,
#         day=None,
#         hour=None,
#         lon=None,
#         lat=None,
#         vars=["VIS"],
#         get_values=True,
#         interp_lon=None,
#         interp_lat=None,
#         add_arounds=False
# ):
#
#     # 1. 扩展变量列表
#     extended_vars = []
#     for var in vars:
#         extended_vars.append(var)
#         if add_arounds:
#             extended_vars.extend([f"{var}_{i}" for i in range(1, 9)])
#
#     # 2. 构建完整字典
#     data_dict = {}
#     for var in extended_vars:
#         # 解析变量名和偏移量
#         if "_" in var:
#             base_var, shift_idx = var.split("_")
#             shift_idx = int(shift_idx)
#             shifts = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
#             lon_shift, lat_shift = shifts[shift_idx - 1]
#         else:
#             base_var = var
#             lon_shift, lat_shift = 0, 0
#
#         # 加载并重命名DataArray
#         if base_var not in data_dict:
#             file_path = f"/mnt/external_disk0/Asian_VIS/data_ensemble/{year}{month:02d}{day:02d}{hour:02d}.nc"
#             with xr.open_dataset(file_path) as f:
#                 # 使用原始变量名作为DataArray名称
#                 # data_dict[base_var] = f[base_var+"_sigma08"].rename(base_var)
#                 data_dict[base_var] = f[base_var].rename(base_var)
#
#         # 应用偏移
#         if lon_shift != 0 or lat_shift != 0:
#             data_dict[var] = data_dict[base_var].shift(
#                 lon=lon_shift, lat=lat_shift, fill_value=np.nan
#             ).rename(var)
#         else:
#             # 确保原始数据使用正确的名称
#             data_dict[var] = data_dict[base_var].rename(var)
#
#     # 3. 应用插值
#     if interp_lon is not None and interp_lat is not None:
#         for var, da in data_dict.items():
#             data_dict[var] = da.interp(lon=interp_lon, lat=interp_lat)
#
#     # 4. 提取结果
#     result = {}
#     if lon is not None and lat is not None:
#         for var, da in data_dict.items():
#             result[var] = da.sel(lon=lon, lat=lat, method="nearest")
#             if get_values:
#                 result[var] = result[var].values
#     else:
#         for var, da in data_dict.items():
#             result[var] = da.values if get_values else da
#
#     return result


def get_geos_asm(
        year=None,
        month=None,
        day=None,
        hour=None,
        minute=None,
        lon=None,
        lat=None,
        get_values=True,
        interp_lon=None,
        interp_lat=None,
        file_structure="/mnt/external_disk1/GOES-FP/GEOS.fp.asm.{type}/GEOS.fp.asm.{type}.{YYYYMMDD}_{HHMM}.V01.hdf",
        vars={
            "tavg3_2d_aer_Nx": ['BCEXTTAU', 'BCSMASS', 'DUEXTTAU', 'DUSMASS', 'OCEXTTAU',
                                'OCSMASS', 'SO4SMASS', 'SSEXTTAU', 'SSSMASS', 'SUEXTTAU',
                                'TOTEXTTAU', 'TOTSCATAU'],
            "tavg1_2d_flx_Nx": ['QLML', 'TLML', 'ULML', 'VLML', 'PRECTOT'],
            "tavg3_3d_asm_Nv": {"var": ["QV", "SLP", "T", "U", "V"],
                                "level": [45, 48, 51, 53, 56, 60, 63, 68, 72]}
        }
):
    """
    简化的GEOS数据获取函数，支持字典格式的变量配置
    """
    # 确保输入是整数
    year = int(year) if year else datetime.now().year
    month = int(month) if month else 1
    day = int(day) if day else 1
    hour = int(hour) if hour else 0
    minute = int(minute) if minute else 0

    # 构建数据字典
    data_dict = {}

    for data_type, var_config in vars.items():
        # 构建文件路径
        file_path = file_structure.format(
            type=data_type,
            YYYY=year,
            MM=f"{month:02d}",
            DD=f"{day:02d}",
            HH=f"{hour:02d}",
            MIN=f"{minute:02d}",
            YYYYMMDD=f"{year}{month:02d}{day:02d}",
            HHMM=f"{hour:02d}{minute:02d}"
        )

        # 检查文件是否存在
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"GEOS数据文件不存在: {file_path}")

        # 打开文件并读取数据
        with xr.open_dataset(file_path) as f:
            # 处理字典格式的变量配置
            if isinstance(var_config, dict) and "var" in var_config:
                var_list = var_config["var"]
                levels = var_config.get("level", None)

                for var in var_list:
                    if var in f.variables:
                        # 重命名坐标以保持一致性
                        da = f[var]

                        # 检查是否有高度维度
                        if 'lev' in da.dims:
                            # 处理有高度层的数据
                            target_levels = levels if levels is not None else da.lev.values

                            for lev in target_levels:
                                # 选择特定高度层
                                da_lev = da.sel(lev=lev)
                                # 创建变量_高度的键名
                                key = f"{var}_{int(lev)}"
                                data_dict[key] = da_lev
                        else:
                            # 没有高度层的变量直接存储
                            data_dict[var] = da
            else:
                # 向后兼容：处理列表格式的变量配置
                for var in var_config:
                    if var in f.variables:
                        da = f[var]
                        data_dict[var] = da

    # 应用插值（如果需要）
    if interp_lon is not None and interp_lat is not None:
        for var, da in data_dict.items():
            data_dict[var] = da.interp(lon=interp_lon, lat=interp_lat)

    # 提取结果
    result = {}
    if lon is not None and lat is not None:
        for var, da in data_dict.items():
            result[var] = da.sel(lon=lon, lat=lat, method="nearest")
            if get_values:
                result[var] = result[var].values
    else:
        for var, da in data_dict.items():
            result[var] = da.values if get_values else da

    return result




if __name__ == "__main__":

    interp_lon = np.arange(70, 140.1, 0.1)
    interp_lat = np.arange(10, 50.1, 0.1)

    # # 测试气象场数据读取
    # data = get_cra_surface_meteos(
    #     2013,
    #     1,
    #     1,
    #     0,
    #     lon=None,
    #     lat=None,
    #     get_values=False,
    #     add_arounds=False,
    #     interp_lon=interp_lon,
    #     interp_lat=interp_lat,
    #     file_structure="/data/CRA/surface/{YYYY}/{YYYYMMDD}/ART_ATM_GLB_0P10_6HOR_SANL_{YYYYMMDDHH}.grib2",
    # )
    #
    # data = get_cra_surface_80m_meteos(
    #     2013,
    #     1,
    #     1,
    #     12,
    #     lon=None,
    #     lat=None,
    #     get_values=False,
    #     add_arounds=False,
    #     interp_lon=interp_lon,
    #     interp_lat=interp_lat,
    #     file_structure="/data2/CRA/surface_80m/{YYYY}/{YYYYMM}/{YYYYMMDD}/ART_ATM_GLB_0P10_1HOR_ANAL_{YYYYMMDDHH}_{VAR}.grib2",
    # )

    # # 测试排放数据读取
    # data = get_gem_emissions(1980, 1, lon=100, lat=50, get_values=True, interp_lon=interp_lon, interp_lat=interp_lat, add_arounds=True)

    # # 测试化学场数据读取
    # data = get_cma_chms(2023, 1, 1, 1, lon=None, lat=None, get_values=True, add_arounds=True, add_tag=True)

    # # 测试CAMS化学场数据读取
    # data = get_cams_chms(2016, 7, 2, 7, lon=None, lat=None, get_values=True, add_arounds=True, add_tag=True)

    # # 测试反演场
    # data = get_retrieval(2018, 1, 1, 0, lon=None, lat=None, get_values=True, add_arounds=True)

    # # 测试气象场数据读取
    # data = get_cra_atmos_meteos(2013, 1, 1, 0, lon=None, lat=None, get_values=False, add_arounds=False, interp_lon=interp_lon, interp_lat=interp_lat)

    # 测试读取GEOS-FP数据
    data = get_geos_asm(
        2015, 1, 1, 1, 30,
        get_values=False
    )

    print("debug")