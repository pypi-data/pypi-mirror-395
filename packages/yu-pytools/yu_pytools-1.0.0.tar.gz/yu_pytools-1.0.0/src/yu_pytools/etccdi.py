# -*-coding:utf-8 -*-
'''
@Author:  Haoran Yu
@Contact: yuhaoran251@mails.ucas.ac.cn
@Date: 2025/12/5 18:25
@Version: 2.1
@Copyright: Copyright (c) 2025 Haoran Yu
@Author: Haoran Yu
@Desc: 极端气候指标计算函数库
'''
import numpy as np
import xarray as xr
from tqdm import tqdm
import warnings
from datetime import datetime, timedelta
"""======================================================辅助函数======================================================"""
"""======================================================辅助函数======================================================"""
"""======================================================辅助函数======================================================"""
"""======================================================辅助函数======================================================"""
"""======================================================辅助函数======================================================"""
"""======================================"""
#通用数据校验与时间转换函数如下
def _convert_time_to_datetime(pr):
    """
    内部辅助函数：将任意格式的time维度转换为datetime64[D]（日分辨率）
    新增兼容：cftime类型、带时分秒的字符串（如2070-01-01 12:00:00）
    支持的输入格式：
    - cftime类型（DatetimeNoLeap/Datetime360Day等）
    - 数值型：YYYYMMDD、年+日序、时间戳
    - 字符串型：YYYY-MM-DD、YYYYMMDD、YYYY-MM-DD HH:MM:SS
    - datetime64：直接标准化为日分辨率
    """
    time_vals = pr.time.values
    time_dim = pr.time

    # 新增：处理cftime类型（气象数据核心兼容）
    try:
        from cftime import DatetimeNoLeap, Datetime360Day, DatetimeGregorian
        # 检测cftime类型并转换为datetime
        if isinstance(time_vals[0], (DatetimeNoLeap, Datetime360Day, DatetimeGregorian)):
            parsed_times = []
            for t in time_vals:
                # 提取年月日，忽略时分秒
                parsed = datetime(t.year, t.month, t.day)
                parsed_times.append(np.datetime64(parsed))
            pr = pr.assign_coords(time=np.array(parsed_times, dtype='datetime64[D]'))
            return pr
    except ImportError:
        pass  # 未安装cftime，不影响其他格式

    # 情况1：已为datetime64类型 → 标准化为日分辨率
    if np.issubdtype(time_vals.dtype, np.datetime64):
        pr = pr.assign_coords(time=time_dim.dt.floor('D'))
        return pr

    # 情况2：数值型（YYYYMMDD / 年+日序 / 时间戳）
    elif np.issubdtype(time_vals.dtype, np.number):
        parsed_times = []
        for val in time_vals:
            val = float(val)
            # YYYYMMDD格式（如20700101）
            if 19000101 <= val <= 21001231:
                val_int = int(val)
                year = val_int // 10000
                month = (val_int // 100) % 100
                day = val_int % 100
                try:
                    parsed = datetime(year, month, day)
                except ValueError:
                    raise ValueError(f"无效的日期数值: {val}（格式应为YYYYMMDD）")
            # 年+日序格式（如2070.001）
            elif 1900 <= val < 2100:
                year = int(val)
                doy = int(round((val - year) * 1000))
                if doy < 1 or doy > 366:
                    raise ValueError(f"无效的日序数值: {val}（日序应在1-366之间）")
                parsed = datetime(year, 1, 1) + timedelta(days=doy - 1)
            # 时间戳（秒/毫秒）
            elif val > 1e9:
                if val > 1e12:
                    val = val / 1000
                parsed = datetime.fromtimestamp(val)
            else:
                raise ValueError(f"无法解析数值型时间: {val}")
            parsed_times.append(np.datetime64(parsed))

    # 情况3：字符串型（含带时分秒的格式）
    else:
        parsed_times = []
        time_strs = [str(t).strip() for t in time_vals]
        # 新增：支持带时分秒的格式（YYYY-MM-DD HH:MM:SS）
        date_formats = [
            '%Y-%m-%d %H:%M:%S',  # 带时分秒
            '%Y-%m-%d',  # 仅日期
            '%Y/%m/%d',
            '%Y%m%d',
            '%Y.%m.%d'
        ]

        for s in time_strs:
            parsed = None
            for fmt in date_formats:
                try:
                    parsed = datetime.strptime(s, fmt)
                    break
                except:
                    continue
            if not parsed:
                # 兜底：截取日期部分再尝试
                try:
                    date_part = s.split(' ')[0]  # 去掉时分秒
                    parsed = datetime.strptime(date_part, '%Y-%m-%d')
                except:
                    raise ValueError(
                        f"无法解析字符串时间: {s}\n"
                        "支持格式：YYYY-MM-DD HH:MM:SS、YYYY-MM-DD、YYYYMMDD、YYYY/MM/DD"
                    )
            parsed_times.append(np.datetime64(parsed))

    # 替换为标准datetime64[D]（日分辨率）
    pr = pr.assign_coords(time=np.array(parsed_times, dtype='datetime64[D]'))
    return pr
"""======================================"""
#检查数据格式与逐日特征
def check_data(pr):
    """
    通用降水数据校验函数（含自动时间类型转换）
    :param pr: xarray.DataArray - 待校验的降水数据
    :return: xarray.DataArray - 校验并转换后的降水数据（time为datetime64[D]格式）
    :raises ValueError: 数据校验失败时抛出异常
    """
    # 1. 基础类型校验
    if not isinstance(pr, xr.DataArray):
        raise ValueError(f"输入数据必须是xarray.DataArray类型，当前类型: {type(pr)}")

    # 2. 降水变量名校验（支持气象常用命名）
    valid_var_names = ['pr', 'pre', 'precipitation', 'rain', 'prec', 'tp']
    var_name = pr.name.lower() if pr.name else ''
    if var_name not in valid_var_names:
        raise ValueError(
            f"无效的降水变量名: '{pr.name}'，支持的变量名: {', '.join(valid_var_names)}"
        )

    # 3. time维度存在性校验
    if 'time' not in pr.dims:
        raise ValueError("输入数据必须包含'time'维度")

    # 4. 核心：自动转换time维度为datetime64[D]格式
    pr = _convert_time_to_datetime(pr)

    # 5. 逐日数据校验（基于datetime64计算时间间隔）
    time_vals = pr.time.values
    if len(time_vals) < 2:
        raise ValueError("time维度数据量不足，至少需要2个时间点验证逐日特征")

    time_diff = np.diff(time_vals)
    day_diff = np.timedelta64(1, 'D')
    # 允许1%的非逐日间隔（处理闰年/数据缺失）
    daily_ratio = np.sum(time_diff == day_diff) / len(time_diff)
    if daily_ratio < 0.99:
        raise ValueError(
            f"输入数据非标准逐日数据！仅{daily_ratio * 100:.1f}%的时间间隔为1天\n"
            f"时间间隔统计：最小={np.min(time_diff)}, 最大={np.max(time_diff)}, 均值={np.mean(time_diff)}"
        )

    # 6. 年份范围有效性校验
    years = pr.time.dt.year.values
    min_year, max_year = np.min(years), np.max(years)
    if min_year > max_year:
        raise ValueError(f"无效的年份范围: 最小年份={min_year}, 最大年份={max_year}")

    return pr
"""======================================"""
#计算连续天数辅助函数
def _max_consecutive_true(arr):
    """辅助：计算一维布尔数组中最长连续True长度（用于CDD/CWD）"""
    if arr.dtype != bool:
        arr = arr.astype(bool)

    if arr.ndim == 1:
        max_len, cur_len = 0, 0
        for val in arr:
            cur_len = cur_len + 1 if val else 0
            max_len = max(max_len, cur_len)
        return np.float32(max_len)

    # 高维数组处理（time轴为首维）
    stacked = np.moveaxis(arr, 0, -1)
    out_shape = stacked.shape[:-1]
    result = np.zeros(out_shape, dtype=np.float32)

    it = np.nditer(result, flags=['multi_index'], op_flags=['writeonly'])
    while not it.finished:
        idx = it.multi_index
        series = stacked[idx]
        max_len, cur_len = 0, 0
        for val in series:
            cur_len = cur_len + 1 if val else 0
            max_len = max(max_len, cur_len)
        it[0] = max_len
        it.iternext()

    return result
"""======================================"""
#辅助：计算变异系数（CV=标准差/均值，忽略非正值）
def _calculate_cv(data):

    valid_data = data[data > 0]
    if len(valid_data) < 2:  # 至少2个有效数据才计算
        return np.nan

    mean = np.mean(valid_data)
    std = np.std(valid_data, ddof=1)  # 样本标准差（除以n-1）
    return std / mean if mean != 0 else np.nan
"""======================================================主要函数======================================================"""
"""======================================================主要函数======================================================"""
"""======================================================主要函数======================================================"""
"""======================================================主要函数======================================================"""
"""======================================================主要函数======================================================"""
"""======================================================主要函数======================================================"""
"""======================================================主要函数======================================================"""
# ====================== 降水变率计算函数 ======================
# ====================== 降水变率计算函数 ======================
# ====================== 降水变率计算函数 ======================
# ====================== 降水变率计算函数 ======================
# ====================== 降水变率计算函数 ======================
# ====================== 降水变率计算函数 ======================
def CV_daily(pr):
    """计算逐年的日降水变异系数（忽略非正值）"""
    pr = check_data(pr)  # 自动完成时间转换
    print("计算逐年日降水变异系数 (CV_daily)")

    years = np.unique(pr.time.dt.year)
    cv_results = []
    year_labels = []

    for year in tqdm(years, desc="CV_daily"):
        year_data = pr.sel(time=pr.time.dt.year == year)
        if len(year_data) < 5:  # 数据量不足跳过
            cv_results.append(np.nan)
        else:
            cv_results.append(_calculate_cv(year_data.values))
        year_labels.append(int(year))

    return xr.DataArray(
        cv_results,
        coords={'year': year_labels},
        dims=['year'],
        name='CV_daily'
    )


def CV_June(pr):
    """计算逐年6月降水变异系数（忽略非正值）"""
    pr = check_data(pr)
    print("计算逐年6月降水变异系数 (CV_June)")

    years = np.unique(pr.time.dt.year)
    cv_results = []
    year_labels = []

    for year in tqdm(years, desc="CV_June"):
        jun_data = pr.sel(time=(pr.time.dt.year == year) & (pr.time.dt.month == 6))
        if len(jun_data) < 5:  # 6月至少5个有效数据
            cv_results.append(np.nan)
        else:
            cv_results.append(_calculate_cv(jun_data.values))
        year_labels.append(int(year))

    return xr.DataArray(
        cv_results,
        coords={'year': year_labels},
        dims=['year'],
        name='CV_June'
    )


def CV_July(pr):
    """计算逐年7月降水变异系数（忽略非正值）"""
    pr = check_data(pr)
    print("计算逐年7月降水变异系数 (CV_July)")

    years = np.unique(pr.time.dt.year)
    cv_results = []
    year_labels = []

    for year in tqdm(years, desc="CV_July"):
        jul_data = pr.sel(time=(pr.time.dt.year == year) & (pr.time.dt.month == 7))
        if len(jul_data) < 5:
            cv_results.append(np.nan)
        else:
            cv_results.append(_calculate_cv(jul_data.values))
        year_labels.append(int(year))

    return xr.DataArray(
        cv_results,
        coords={'year': year_labels},
        dims=['year'],
        name='CV_July'
    )


def CV_August(pr):
    """计算逐年8月降水变异系数（忽略非正值）"""
    pr = check_data(pr)
    print("计算逐年8月降水变异系数 (CV_August)")

    years = np.unique(pr.time.dt.year)
    cv_results = []
    year_labels = []

    for year in tqdm(years, desc="CV_August"):
        aug_data = pr.sel(time=(pr.time.dt.year == year) & (pr.time.dt.month == 8))
        if len(aug_data) < 5:
            cv_results.append(np.nan)
        else:
            cv_results.append(_calculate_cv(aug_data.values))
        year_labels.append(int(year))

    return xr.DataArray(
        cv_results,
        coords={'year': year_labels},
        dims=['year'],
        name='CV_August'
    )


def CV_Summer(pr):
    """计算逐年夏季（6-8月）降水变异系数（忽略非正值）"""
    pr = check_data(pr)
    print("计算逐年夏季（6-8月）降水变异系数 (CV_Summer)")

    years = np.unique(pr.time.dt.year)
    cv_results = []
    year_labels = []

    for year in tqdm(years, desc="CV_Summer"):
        summer_data = pr.sel(
            time=(pr.time.dt.year == year) & (pr.time.dt.month.isin([6, 7, 8]))
        )
        if len(summer_data) < 15:  # 夏季至少15个有效数据
            cv_results.append(np.nan)
        else:
            cv_results.append(_calculate_cv(summer_data.values))
        year_labels.append(int(year))

    return xr.DataArray(
        cv_results,
        coords={'year': year_labels},
        dims=['year'],
        name='CV_Summer'
    )


# ====================== 基础降水指数 ======================
# ====================== 基础降水指数 ======================
# ====================== 基础降水指数 ======================
# ====================== 基础降水指数 ======================
# ====================== 基础降水指数 ======================
# ====================== 基础降水指数 ======================
def PRCPTOT(pr):
    """逐年年总降水量（PRCPTOT）"""
    pr = check_data(pr)
    print("计算年总降水量 (PRCPTOT)")

    years = np.unique(pr.time.dt.year)
    result_list = []
    year_labels = []

    for year in tqdm(years, desc="PRCPTOT"):
        year_data = pr.sel(time=pr.time.dt.year == year)
        if len(year_data) < 30:
            continue
        annual_sum = year_data.sum(dim='time').astype(np.float32).compute()
        result_list.append(annual_sum)
        year_labels.append(int(year))

    if not result_list:
        return None
    return xr.concat(result_list, dim='year').assign_coords(year=year_labels)


def R1mm_d(pr):
    """逐年≥1mm降水日数（R1mm_d）"""
    pr = check_data(pr)
    print("计算年≥1mm降水日数 (R1mm_d)")

    years = np.unique(pr.time.dt.year)
    result_list = []
    year_labels = []

    for year in tqdm(years, desc="R1mm_d"):
        year_data = pr.sel(time=pr.time.dt.year == year)
        if len(year_data) < 30:
            continue
        wet_days = (year_data >= 1.0).sum(dim='time').astype(np.float32).compute()
        result_list.append(wet_days)
        year_labels.append(int(year))

    if not result_list:
        return None
    return xr.concat(result_list, dim='year').assign_coords(year=year_labels)


def SDII(pr):
    """逐年简单降水强度（SDII=年总降水量/年湿日数）"""
    pr = check_data(pr)
    print("计算年简单降水强度 (SDII)")

    years = np.unique(pr.time.dt.year)
    result_list = []
    year_labels = []

    for year in tqdm(years, desc="SDII"):
        year_data = pr.sel(time=pr.time.dt.year == year)
        if len(year_data) < 30:
            continue
        annual_sum = year_data.sum(dim='time')
        wet_days = (year_data >= 1.0).sum(dim='time')
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            sdii = (annual_sum / wet_days).where(wet_days > 0)
        result_list.append(sdii.astype(np.float32).compute())
        year_labels.append(int(year))

    if not result_list:
        return None
    return xr.concat(result_list, dim='year').assign_coords(year=year_labels)


def RX1DAY(pr):
    """逐年最大日降水量（RX1DAY）"""
    pr = check_data(pr)
    print("计算年最大日降水量 (RX1DAY)")

    years = np.unique(pr.time.dt.year)
    result_list = []
    year_labels = []

    for year in tqdm(years, desc="RX1DAY"):
        year_data = pr.sel(time=pr.time.dt.year == year)
        if len(year_data) < 30:
            continue
        max_precip = year_data.max(dim='time').astype(np.float32).compute()
        result_list.append(max_precip)
        year_labels.append(int(year))

    if not result_list:
        return None
    return xr.concat(result_list, dim='year').assign_coords(year=year_labels)


def CDD(pr):
    """逐年最大连续干日数（CDD，<1mm为干日）"""
    pr = check_data(pr)
    print("计算年最大连续干日数 (CDD)")

    years = np.unique(pr.time.dt.year)
    result_list = []
    year_labels = []

    for year in tqdm(years, desc="CDD"):
        year_data = pr.sel(time=pr.time.dt.year == year)
        if len(year_data) < 30:
            continue
        dry_mask = (year_data < 1.0).values
        max_cdd = xr.apply_ufunc(
            _max_consecutive_true,
            dry_mask,
            input_core_dims=[['time']],
            output_core_dims=[[]],
            vectorize=True,
            dask='parallelized',
            output_dtypes=[np.float32]
        ).compute()
        result_list.append(max_cdd)
        year_labels.append(int(year))

    if not result_list:
        return None
    return xr.concat(result_list, dim='year').assign_coords(year=year_labels)


def CWD(pr):
    """逐年最大连续湿日数（CWD，≥1mm为湿日）"""
    pr = check_data(pr)
    print("计算年最大连续湿日数 (CWD)")

    years = np.unique(pr.time.dt.year)
    result_list = []
    year_labels = []

    for year in tqdm(years, desc="CWD"):
        year_data = pr.sel(time=pr.time.dt.year == year)
        if len(year_data) < 30:
            continue
        wet_mask = (year_data >= 1.0).values
        max_cwd = xr.apply_ufunc(
            _max_consecutive_true,
            wet_mask,
            input_core_dims=[['time']],
            output_core_dims=[[]],
            vectorize=True,
            dask='parallelized',
            output_dtypes=[np.float32]
        ).compute()
        result_list.append(max_cwd)
        year_labels.append(int(year))

    if not result_list:
        return None
    return xr.concat(result_list, dim='year').assign_coords(year=year_labels)


# ====================== 固定阈值降水指数 ======================
# ====================== 固定阈值降水指数 ======================
# ====================== 固定阈值降水指数 ======================
# ====================== 固定阈值降水指数 ======================
# ====================== 固定阈值降水指数 ======================
# ====================== 固定阈值降水指数 ======================
# 固定阈值通用计算函数
def _calc_threshold_precip(pr, threshold, metric_name, func_name):
    pr = check_data(pr)
    print(f"计算≥{threshold}mm降水{metric_name} ({func_name})")

    years = np.unique(pr.time.dt.year)
    result_list = []
    year_labels = []

    for year in tqdm(years, desc=func_name):
        year_data = pr.sel(time=pr.time.dt.year == year)
        if len(year_data) < 30:
            continue
        threshold_data = year_data.where(year_data >= threshold, 0)
        total = threshold_data.sum(dim='time').astype(np.float32).compute()
        result_list.append(total)
        year_labels.append(int(year))

    if not result_list:
        return None
    return xr.concat(result_list, dim='year').assign_coords(year=year_labels)


def _calc_threshold_days(pr, threshold, metric_name, func_name):
    pr = check_data(pr)
    print(f"计算≥{threshold}mm降水{metric_name} ({func_name})")

    years = np.unique(pr.time.dt.year)
    result_list = []
    year_labels = []

    for year in tqdm(years, desc=func_name):
        year_data = pr.sel(time=pr.time.dt.year == year)
        if len(year_data) < 30:
            continue
        days = (year_data >= threshold).sum(dim='time').astype(np.float32).compute()
        result_list.append(days)
        year_labels.append(int(year))

    if not result_list:
        return None
    return xr.concat(result_list, dim='year').assign_coords(year=year_labels)


def _calc_threshold_intensity(pr, threshold, metric_name, func_name):
    pr = check_data(pr)
    print(f"计算≥{threshold}mm降水{metric_name} ({func_name})")

    years = np.unique(pr.time.dt.year)
    result_list = []
    year_labels = []

    for year in tqdm(years, desc=func_name):
        year_data = pr.sel(time=pr.time.dt.year == year)
        if len(year_data) < 30:
            continue
        threshold_mask = year_data >= threshold
        total = year_data.where(threshold_mask).sum(dim='time')
        days = threshold_mask.sum(dim='time')
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            intensity = (total / days).where(days > 0)
        result_list.append(intensity.astype(np.float32).compute())
        year_labels.append(int(year))

    if not result_list:
        return None
    return xr.concat(result_list, dim='year').assign_coords(year=year_labels)


def R10_p(pr):
    """逐年≥10mm降水总量（R10p）"""
    return _calc_threshold_precip(pr, 10.0, '总量', 'R10_p')

def R10_d(pr):
    """逐年≥10mm降水日数（R10d）"""
    return _calc_threshold_days(pr, 10.0, '日数', 'R10_d')

def R10_i(pr):
    """逐年≥10mm降水强度（R10i=总量/日数）"""
    return _calc_threshold_intensity(pr, 10.0, '强度', 'R10_i')

def R20_p(pr):
    """逐年≥20mm降水总量（R20p）"""
    return _calc_threshold_precip(pr, 20.0, '总量', 'R20_p')

def R20_d(pr):
    """逐年≥20mm降水日数（R20d）"""
    return _calc_threshold_days(pr, 20.0, '日数', 'R20_d')

def R20_i(pr):
    """逐年≥20mm降水强度（R20i=总量/日数）"""
    return _calc_threshold_intensity(pr, 20.0, '强度', 'R20_i')

def R25_p(pr):
    """逐年≥25mm降水总量（R25p）"""
    return _calc_threshold_precip(pr, 25.0, '总量', 'R25_p')

def R25_d(pr):
    """逐年≥25mm降水日数（R25d）"""
    return _calc_threshold_days(pr, 25.0, '日数', 'R25_d')

def R25_i(pr):
    """逐年≥25mm降水强度（R25i=总量/日数）"""
    return _calc_threshold_intensity(pr, 25.0, '强度', 'R25_i')

def R50_p(pr):
    """逐年≥50mm降水总量（R50p）"""
    return _calc_threshold_precip(pr, 50.0, '总量', 'R50_p')

def R50_d(pr):
    """逐年≥50mm降水日数（R50d）"""
    return _calc_threshold_days(pr, 50.0, '日数', 'R50_d')

def R50_i(pr):
    """逐年≥50mm降水强度（R50i=总量/日数）"""
    return _calc_threshold_intensity(pr, 50.0, '强度', 'R50_i')
# ====================== 百分位阈值降水指数 ======================
# ====================== 百分位阈值降水指数 ======================
# ====================== 百分位阈值降水指数 ======================
# ====================== 百分位阈值降水指数 ======================
# ====================== 百分位阈值降水指数 ======================
# ====================== 百分位阈值降水指数 ======================
# 百分位阈值通用计算函数
def _calculate_percentile_threshold(baseline_pr, percentile):
    """计算基准期的百分位阈值（仅考虑≥1mm的湿日）"""
    baseline_pr = check_data(baseline_pr)
    wet_days = baseline_pr.where(baseline_pr >= 1.0).values
    wet_days = wet_days[~np.isnan(wet_days)]

    if len(wet_days) == 0:
        raise ValueError(f"基准期数据中无有效湿日（≥1mm），无法计算{percentile}百分位阈值")

    return np.percentile(wet_days, percentile)


def _calc_percentile_precip(pr, baseline_pr, percentile, metric_name, func_name):
    pr = check_data(pr)
    threshold = _calculate_percentile_threshold(baseline_pr, percentile)
    print(f"计算{percentile}百分位降水{metric_name} ({func_name}) - 阈值={threshold:.2f}mm")

    years = np.unique(pr.time.dt.year)
    result_list = []
    year_labels = []

    for year in tqdm(years, desc=func_name):
        year_data = pr.sel(time=pr.time.dt.year == year)
        if len(year_data) < 30:
            continue
        wet_mask = year_data >= 1.0
        percentile_mask = year_data > threshold
        total = year_data.where(wet_mask & percentile_mask, 0).sum(dim='time').astype(np.float32).compute()
        result_list.append(total)
        year_labels.append(int(year))

    if not result_list:
        return None
    return xr.concat(result_list, dim='year').assign_coords(year=year_labels)


def _calc_percentile_days(pr, baseline_pr, percentile, metric_name, func_name):
    pr = check_data(pr)
    threshold = _calculate_percentile_threshold(baseline_pr, percentile)
    print(f"计算{percentile}百分位降水{metric_name} ({func_name}) - 阈值={threshold:.2f}mm")

    years = np.unique(pr.time.dt.year)
    result_list = []
    year_labels = []

    for year in tqdm(years, desc=func_name):
        year_data = pr.sel(time=pr.time.dt.year == year)
        if len(year_data) < 30:
            continue
        wet_mask = year_data >= 1.0
        percentile_mask = year_data > threshold
        days = (wet_mask & percentile_mask).sum(dim='time').astype(np.float32).compute()
        result_list.append(days)
        year_labels.append(int(year))

    if not result_list:
        return None
    return xr.concat(result_list, dim='year').assign_coords(year=year_labels)


def _calc_percentile_intensity(pr, baseline_pr, percentile, metric_name, func_name):
    pr = check_data(pr)
    threshold = _calculate_percentile_threshold(baseline_pr, percentile)
    print(f"计算{percentile}百分位降水{metric_name} ({func_name}) - 阈值={threshold:.2f}mm")

    years = np.unique(pr.time.dt.year)
    result_list = []
    year_labels = []

    for year in tqdm(years, desc=func_name):
        year_data = pr.sel(time=pr.time.dt.year == year)
        if len(year_data) < 30:
            continue
        wet_mask = year_data >= 1.0
        percentile_mask = year_data > threshold
        total = year_data.where(wet_mask & percentile_mask).sum(dim='time')
        days = (wet_mask & percentile_mask).sum(dim='time')
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            intensity = (total / days).where(days > 0)
        result_list.append(intensity.astype(np.float32).compute())
        year_labels.append(int(year))

    if not result_list:
        return None
    return xr.concat(result_list, dim='year').assign_coords(year=year_labels)

def R95p_p(pr, baseline_pr):
    """逐年95百分位降水总量（基于基准期数据计算阈值）"""
    return _calc_percentile_precip(pr, baseline_pr, 95, '总量', 'R95p_p')


def R95p_d(pr, baseline_pr):
    """逐年95百分位降水日数（基于基准期数据计算阈值）"""
    return _calc_percentile_days(pr, baseline_pr, 95, '日数', 'R95p_d')


def R95p_i(pr, baseline_pr):
    """逐年95百分位降水强度（基于基准期数据计算阈值）"""
    return _calc_percentile_intensity(pr, baseline_pr, 95, '强度', 'R95p_i')


def R99p_p(pr, baseline_pr):
    """逐年99百分位降水总量（基于基准期数据计算阈值）"""
    return _calc_percentile_precip(pr, baseline_pr, 99, '总量', 'R99p_p')


def R99p_d(pr, baseline_pr):
    """逐年99百分位降水日数（基于基准期数据计算阈值）"""
    return _calc_percentile_days(pr, baseline_pr, 99, '日数', 'R99p_d')


def R99p_i(pr, baseline_pr):
    """逐年99百分位降水强度（基于基准期数据计算阈值）"""
    return _calc_percentile_intensity(pr, baseline_pr, 99, '强度', 'R99p_i')
