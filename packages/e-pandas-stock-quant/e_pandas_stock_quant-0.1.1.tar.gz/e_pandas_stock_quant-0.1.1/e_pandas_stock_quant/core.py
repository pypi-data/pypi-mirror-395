import pandas as pd
import numpy as np
import os
import glob
from sklearn.linear_model import LinearRegression
from tqdm import tqdm
import multiprocessing as mp
from multiprocessing import Pool, Manager, cpu_count
import warnings
warnings.filterwarnings('ignore')



def cal_trend_f1(df):
    """计算日内基础量价关系特征"""
    features = {}

    # 确保数据按分钟排序（使用正确的时间格式排序）
    df['time_obj'] = pd.to_datetime(df['time'], format='%H:%M')
    df = df.sort_values(by='time_obj')

    # 当日收盘价/当日开盘价-1
    if len(df) > 0:
        open_price = df['price'].iloc[0]
        close_price = df['price'].iloc[-1]
        features['日内整体涨跌1'] = close_price / open_price - 1 if open_price != 0 else 0
    else:
        features['日内整体涨跌1'] = 0

    # 当日开盘价/当日收盘价-1
    if len(df) > 0:
        open_price = df['price'].iloc[0]
        close_price = df['price'].iloc[-1]
        features['日内整体涨跌2'] = open_price / close_price - 1 if close_price != 0 else 0
    else:
        features['日内整体涨跌2'] = 0

    # 当日收盘价
    features['当日收盘价'] = df['price'].iloc[-1] if len(df) > 0 else 0

    # 每日均价
    total_volume = df['volume'].sum()
    avg_price = (df['price'] * df['volume']).sum() / total_volume if total_volume != 0 else 0
    features['每日均价'] = df['volume'].mean()

    # 每日Vwap
    vwap = avg_price
    features['每日Vwap'] = vwap

    # 14:55-15:00Vwap/每日Vwap
    end_df = df[(df['time_obj'].dt.time >= pd.to_datetime('14:55', format='%H:%M').time()) &
                (df['time_obj'].dt.time <= pd.to_datetime('15:00', format='%H:%M').time())]
    end_total_volume = end_df['volume'].sum()
    end_vwap = (end_df['price'] * end_df['volume']).sum() / end_total_volume if end_total_volume != 0 else 0
    features['尾盘拉抬_打压线索'] = end_vwap / vwap if vwap != 0 and not np.isnan(vwap) else 0

    # 每日总成交量
    features['每日总成交量'] = total_volume

    # 每日总成交额
    features['每日总成交额'] = (df['price'] * df['volume']).sum()

    # 每日涨跌幅
    if len(df) > 0:
        open_price = df['price'].iloc[0]
        close_price = df['price'].iloc[-1]
        features['每日涨跌幅'] = (close_price - open_price) / open_price if open_price != 0 else 0
    else:
        features['每日涨跌幅'] = 0

    # 添加开盘价、最高价、最低价特征，用于后续计算振幅
    if len(df) > 0:
        features['当日开盘价'] = df['price'].iloc[0]
        features['当日收盘价'] = df['price'].iloc[-1]
        features['当日最高价'] = df['price'].max()
        features['当日最低价'] = df['price'].min()
        # 计算真实振幅
        daily_amplitude = (df['price'].max() - df['price'].min()) / df['price'].iloc[0] if df['price'].iloc[
                                                                                               0] != 0 else 0
        features['每日振幅'] = daily_amplitude
    else:
        features['当日开盘价'] = 0
        features['当日收盘价'] = 0
        features['当日最高价'] = 0
        features['当日最低价'] = 0
        features['每日振幅'] = 0

    # 每日最高价_每日Vwap
    features['每日最高价_每日Vwap'] = df['price'].max() / vwap if vwap != 0 and not np.isnan(vwap) else 0

    # 每日最低价_每日Vwap
    features['每日最低价_每日Vwap'] = df['price'].min() / vwap if vwap != 0 and not np.isnan(vwap) else 0

    # 每日价格中位数_每日Vwap
    features['每日价格中位数_每日Vwap'] = df['price'].median() / vwap if vwap != 0 and not np.isnan(vwap) else 0

    # 每日价格标准差_每日Vwap
    price_std = df['price'].std()
    features['每日价格标准差_每日Vwap'] = price_std / vwap if vwap != 0 and not np.isnan(vwap) else 0

    # 计算分钟级涨跌幅和持续时间特征
    if len(df) > 1:
        # 计算每分钟的涨跌幅（相对于前一分钟）
        df['price_change_pct'] = df['price'].pct_change()

        # 计算达到不同阈值的持续时间（连续超过阈值的分钟数）
        # 交易时间内股价涨跌幅≥±9.7%持续时间
        mask_97 = (df['price_change_pct'].abs() >= 0.01)
        features['交易时间内股价涨跌幅≥±9.7%持续时间'] = mask_97.sum()  # 以分钟为单位

        # 交易时间内股价涨跌幅≥±19.7%持续时间
        mask_197 = (df['price_change_pct'].abs() >= 0.03)
        features['交易时间内股价涨跌幅≥±19.7%持续时间'] = mask_197.sum()  # 以分钟为单位

        # 交易时间内股价涨跌幅≥±4.7%持续时间
        mask_47 = (df['price_change_pct'].abs() >= 0.05)
        features['交易时间内股价涨跌幅≥±4.7%持续时间'] = mask_47.sum()  # 以分钟为单位

        # 计算达到不同阈值的触及次数（跨越阈值的次数）
        # 交易时间内股价涨跌幅≥±9.7%触及次数
        threshold_97_crossings = 0
        prev_price_change = df['price_change_pct'].iloc[0] if not pd.isna(df['price_change_pct'].iloc[0]) else 0
        for i in range(1, len(df)):
            curr_price_change = df['price_change_pct'].iloc[i] if not pd.isna(df['price_change_pct'].iloc[i]) else 0
            if abs(curr_price_change) >= 0.01:
                threshold_97_crossings += 1
        features['交易时间内股价涨跌幅≥±9.7%触及次数'] = threshold_97_crossings

        # 交易时间内涨跌幅≥±19.7%触及次数
        threshold_197_crossings = 0
        for i in range(len(df)):
            curr_price_change = df['price_change_pct'].iloc[i] if not pd.isna(df['price_change_pct'].iloc[i]) else 0
            if abs(curr_price_change) >= 0.03:
                threshold_197_crossings += 1
        features['交易时间内涨跌幅≥±19.7%触及次数'] = threshold_197_crossings

        # 交易时间内涨跌幅≥±4.7%触及次数
        threshold_47_crossings = 0
        for i in range(len(df)):
            curr_price_change = df['price_change_pct'].iloc[i] if not pd.isna(df['price_change_pct'].iloc[i]) else 0
            if abs(curr_price_change) >= 0.05:
                threshold_47_crossings += 1
        features['交易时间内涨跌幅≥±4.7%触及次数'] = threshold_47_crossings
    else:
        # 如果数据点少于2个，无法计算涨跌幅
        features['交易时间内股价涨跌幅≥±9.7%持续时间'] = 0
        features['交易时间内股价涨跌幅≥±19.7%持续时间'] = 0
        features['交易时间内股价涨跌幅≥±4.7%持续时间'] = 0
        features['交易时间内股价涨跌幅≥±9.7%触及次数'] = 0
        features['交易时间内涨跌幅≥±19.7%触及次数'] = 0
        features['交易时间内涨跌幅≥±4.7%触及次数'] = 0

    return features


def cal_trend_f2(current_data, historical_data):
    """为单个交易日计算跨交易日趋势与惯性特征"""
    features = {}

    # 获取当前交易日的数据
    current_day = current_data['day']

    # 如果没有历史数据（第一个交易日）
    if not historical_data or len(historical_data) == 0:
        # 1. 距离上一交易日的自然日间隔（第0个自然日填0）
        features['距离上一交易日的自然日间隔'] = 0

        # 其他需要历史数据的特征设为0（避免NaN）
        excel_defined_features = [
            '跳空幅度', '每日涨跌幅', '每日振幅',
            '交易时间内股价涨跌幅≥±9.7%持续时间',
            '交易时间内股价涨跌幅≥±19.7%持续时间',
            '交易时间内股价涨跌幅≥±4.7%持续时间',
            '交易时间内股价涨跌幅≥±9.7%触及次数',
            '交易时间内涨跌幅≥±19.7%触及次数',
            '交易时间内涨跌幅≥±4.7%触及次数',
            '最近3个交易日累计涨跌幅绝对值',
            '最近5个交易日累计涨跌幅绝对值',
            '最近3个交易日累计涨跌幅',
            '最近5个交易日累计涨跌幅',
            '最近3个交易日累计振幅',
            '最近5个交易日累计振幅',
            '累积至当日连续上涨天数',
            '累积至当日连续下跌天数',
            '当日总成交量/前一交易日总成交量',
            '(近3日日均总成交量)/(前5日日均总成交量)',
            '近5个交易日每日涨跌幅标准差',
            '近10个交易日每日涨跌幅标准差',
            '近5个交易日收盘价线性回归斜率',
            '近5个交易日收盘价线性回归R^2',
            '对近10个交易日收盘价线性回归斜率',
            '近10个交易日收盘价线性回归R^2',
            '近5个交易日 分钟涨跌幅≥±1% 的次数均值',
            '累积至当日 每日涨跌幅≥±4.7%的连续天数',
            '累积至当日 每日涨跌幅≥±9.7%的连续天数',
            '累积至当日 每日涨跌幅≥±19.7%的连续天数',
            '近5个交易日每日Vwap标准差',
            '近10个交易日每日Vwap标准差',
            '近5个交易日每日Vwap线性回归斜率',
            '近5个交易日每日Vwap线性回归R^2',
            '对近10个交易日每日Vwap线性回归斜率',
            '近10个交易日每日Vwap线性回归R^2',
            '近5个交易日每日总成交额标准差',
            '近10个交易日每日总成交额标准差',
            '近5个交易日每日总成交额回归斜率',
            '近5个交易日每日总成交额回归R^2',
            '对近10个交易日每日总成交额线性回归斜率',
            '近10个交易日每日总成交额线性回归R^2',
            '近5个交易日每日振幅标准差',
            '近10个交易日每日涨跌幅绝对值的标准差',
            '近5个交易日每日振幅线性回归斜率',
            '近5个交易日每日涨跌幅绝对值线性回归R^2',
            '近10个交易日每日振幅线性回归斜率',
            '近10个交易日每日涨跌幅绝对值线性回归R^2'
        ]

        for feat in excel_defined_features:
            features[feat] = 0  # 使用0而不是NaN作为默认值

        return features

    # 获取上一交易日的数据
    previous_data = historical_data[-1]
    previous_day = previous_data['day']

    # 1. 距离上一交易日的自然日间隔
    features['距离上一交易日的自然日间隔'] = current_day - previous_day

    # 2. 跳空幅度 (今日第一笔价格-上一交易日最后一笔价格)/上一交易日收盘价
    # 使用开盘价代替第一笔价格，收盘价代替最后一笔价格
    if '当日收盘价' in previous_data and not np.isnan(previous_data['当日收盘价']) and previous_data[
        '当日收盘价'] != 0 and '当日开盘价' in current_data and not np.isnan(current_data['当日开盘价']) and \
            current_data['当日开盘价'] != 0:
        # 假设开盘价是当日收盘价（这里需要更好的估算）
        jump_gap = current_data['当日开盘价'] / previous_data['当日收盘价'] - 1  # 简化处理，实际需要分钟级数据
        features['跳空幅度'] = jump_gap
    else:
        features['跳空幅度'] = 0

    # Get daily amplitude from the intraday features

    if '当日收盘价' in previous_data and not np.isnan(previous_data['当日收盘价']) and previous_data[
        '当日收盘价'] != 0 and '当日收盘价' in current_data and not np.isnan(current_data['当日收盘价']) and \
            current_data['当日收盘价'] != 0:
        # 假设开盘价是当日收盘价（这里需要更好的估算）
        j_gap = current_data['当日收盘价'] / previous_data['当日收盘价'] - 1  # 简化处理，实际需要分钟级数据
        features['每日涨跌幅'] = j_gap
    else:
        features['每日涨跌幅'] = 0

    # 4. 每日振幅 (当日最高价-当日最低价)/当日开盘价
    # Get daily amplitude from the intraday features
    if '当日开盘价' in current_data and '当日最高价' in current_data and '当日最低价' in current_data:
        open_price = current_data['当日开盘价']
        high_price = current_data['当日最高价']
        low_price = current_data['当日最低价']
        if open_price != 0 and not np.isnan(open_price):
            daily_range = (high_price - low_price) / open_price
            features['每日振幅'] = daily_range
        else:
            features['每日振幅'] = 0
    else:
        # If specific amplitude-related features are not available, calculate from other available data
        # For now set to 0, but we should enhance calculate_intraday_basic_features to compute these
        features['每日振幅'] = 0

    # 5-7. 交易时间内股价涨跌幅≥±X%持续时间
    # 从日内特征中获取计算好的值
    if '交易时间内股价涨跌幅≥±9.7%持续时间' in current_data and not np.isnan(
            current_data['交易时间内股价涨跌幅≥±9.7%持续时间']):
        features['交易时间内股价涨跌幅≥±9.7%持续时间'] = current_data['交易时间内股价涨跌幅≥±9.7%持续时间']
    else:
        features['交易时间内股价涨跌幅≥±9.7%持续时间'] = 0

    if '交易时间内股价涨跌幅≥±19.7%持续时间' in current_data and not np.isnan(
            current_data['交易时间内股价涨跌幅≥±19.7%持续时间']):
        features['交易时间内股价涨跌幅≥±19.7%持续时间'] = current_data['交易时间内股价涨跌幅≥±19.7%持续时间']
    else:
        features['交易时间内股价涨跌幅≥±19.7%持续时间'] = 0

    if '交易时间内股价涨跌幅≥±4.7%持续时间' in current_data and not np.isnan(
            current_data['交易时间内股价涨跌幅≥±4.7%持续时间']):
        features['交易时间内股价涨跌幅≥±4.7%持续时间'] = current_data['交易时间内股价涨跌幅≥±4.7%持续时间']
    else:
        features['交易时间内股价涨跌幅≥±4.7%持续时间'] = 0

    # 8-10. 交易时间内股价涨跌幅≥±X%触及次数 (已从日内特征中计算)
    # 从日内特征中获取计算好的值
    if '交易时间内股价涨跌幅≥±9.7%触及次数' in current_data and not np.isnan(
            current_data['交易时间内股价涨跌幅≥±9.7%触及次数']):
        features['交易时间内股价涨跌幅≥±9.7%触及次数'] = current_data['交易时间内股价涨跌幅≥±9.7%触及次数']
    else:
        features['交易时间内股价涨跌幅≥±9.7%触及次数'] = 0

    if '交易时间内涨跌幅≥±19.7%触及次数' in current_data and not np.isnan(
            current_data['交易时间内涨跌幅≥±19.7%触及次数']):
        features['交易时间内涨跌幅≥±19.7%触及次数'] = current_data['交易时间内涨跌幅≥±19.7%触及次数']
    else:
        features['交易时间内涨跌幅≥±19.7%触及次数'] = 0

    if '交易时间内涨跌幅≥±4.7%触及次数' in current_data and not np.isnan(
            current_data['交易时间内涨跌幅≥±4.7%触及次数']):
        features['交易时间内涨跌幅≥±4.7%触及次数'] = current_data['交易时间内涨跌幅≥±4.7%触及次数']
    else:
        features['交易时间内涨跌幅≥±4.7%触及次数'] = 0

    # 获取历史数据用于计算其他特征
    # 取当前交易日及之前的所有历史数据
    all_historical_data = historical_data + [current_data]

    # 提取每日涨跌幅、收盘价、Vwap、总成交额等数据
    daily_returns = []
    closing_prices = []
    vwap_values = []
    total_turnovers = []
    daily_ranges = []  # 真实的每日振幅

    for data in all_historical_data:
        if '每日涨跌幅' in data and not np.isnan(data['每日涨跌幅']):
            daily_returns.append(data['每日涨跌幅'])
        if '当日收盘价' in data and not np.isnan(data['当日收盘价']):
            closing_prices.append(data['当日收盘价'])
        if '每日Vwap' in data and not np.isnan(data['每日Vwap']):
            vwap_values.append(data['每日Vwap'])
        if '每日总成交额' in data and not np.isnan(data['每日总成交额']):
            total_turnovers.append(data['每日总成交额'])
        if '每日振幅' in data and not np.isnan(data['每日振幅']):
            daily_ranges.append(data['每日振幅'])
        else:
            daily_ranges.append(0)  # 如果没有振幅数据，则为0

    # 11-16. 最近N个交易日累计涨跌幅和涨跌幅绝对值、振幅
    if len(daily_returns) >= 3:
        features['最近3个交易日累计涨跌幅绝对值'] = sum([abs(r) for r in daily_returns[-3:]])
        features['最近3个交易日累计涨跌幅'] = sum(daily_returns[-3:])
    else:
        features['最近3个交易日累计涨跌幅绝对值'] = 0
        features['最近3个交易日累计涨跌幅'] = 0

    if len(daily_returns) >= 5:
        features['最近5个交易日累计涨跌幅绝对值'] = sum([abs(r) for r in daily_returns[-5:]])
        features['最近5个交易日累计涨跌幅'] = sum(daily_returns[-5:])
    else:
        features['最近5个交易日累计涨跌幅绝对值'] = 0
        features['最近5个交易日累计涨跌幅'] = 0

    if len(daily_ranges) >= 3:
        features['最近3个交易日累计振幅'] = sum([r for r in daily_ranges[-3:]])
    else:
        features['最近3个交易日累计振幅'] = sum([r for r in daily_ranges])

    if len(daily_ranges) >= 5:
        features['最近5个交易日累计振幅'] = sum([r for r in daily_ranges[-5:]])
    else:
        features['最近5个交易日累计振幅'] = sum([r for r in daily_ranges])

    # 17-18. 累积至当日连续上涨/下跌天数
    consecutive_up = 0
    consecutive_down = 0
    for r in reversed(daily_returns):
        if r > 0:
            consecutive_up += 1
            consecutive_down = 0
        elif r < 0:
            consecutive_down += 1
            consecutive_up = 0
        else:
            break
    features['累积至当日连续上涨天数'] = consecutive_up
    features['累积至当日连续下跌天数'] = consecutive_down

    # 19. 当日总成交量/前一交易日总成交量
    if '每日总成交量' in previous_data and '每日总成交量' in current_data:
        if previous_data['每日总成交量'] != 0 and not np.isnan(previous_data['每日总成交量']):
            volume_ratio = current_data['每日总成交量'] / previous_data['每日总成交量']
            features['当日总成交量/前一交易日总成交量'] = volume_ratio
        else:
            features['当日总成交量/前一交易日总成交量'] = 1
    else:
        features['当日总成交量/前一交易日总成交量'] = 1

    # 20. (近3日日均总成交量)/(前5日日均总成交量)
    if len(all_historical_data) >= 5:
        recent_3_days_volume = [data['每日总成交量'] for data in all_historical_data[-3:] if
                                '每日总成交量' in data and not np.isnan(data['每日总成交量'])]
        previous_5_days_volume = [data['每日总成交量'] for data in all_historical_data[-5:-3] if
                                  '每日总成交量' in data and not np.isnan(data['每日总成交量'])]

        if recent_3_days_volume and previous_5_days_volume:
            avg_recent_3 = sum(recent_3_days_volume) / len(recent_3_days_volume)
            avg_previous_5 = sum(previous_5_days_volume) / len(previous_5_days_volume)
            if avg_previous_5 != 0:
                features['(近3日日均总成交量)/(前5日日均总成交量)'] = avg_recent_3 / avg_previous_5
            else:
                features['(近3日日均总成交量)/(前5日日均总成交量)'] = 1
        else:
            features['(近3日日均总成交量)/(前5日日均总成交量)'] = 1
    else:
        features['(近3日日均总成交量)/(前5日日均总成交量)'] = 1

    # 21-22. 近N个交易日每日涨跌幅标准差
    if len(daily_returns) >= 5:
        features['近5个交易日每日涨跌幅标准差'] = np.std(daily_returns[-5:]) if len(daily_returns[-5:]) > 1 else 0
    else:
        features['近5个交易日每日涨跌幅标准差'] = 0

    if len(daily_returns) >= 10:
        features['近10个交易日每日涨跌幅标准差'] = np.std(daily_returns[-10:]) if len(daily_returns[-10:]) > 1 else 0
    else:
        features['近10个交易日每日涨跌幅标准差'] = 0

    # 23-26. 收盘价线性回归斜率和R^2
    if len(closing_prices) >= 5:
        X = np.array(range(len(closing_prices[-5:]))).reshape(-1, 1)
        y = np.array(closing_prices[-5:])
        # 过滤掉NaN值
        valid_indices = ~np.isnan(y)
        if np.sum(valid_indices) > 1:
            X_valid = X[valid_indices]
            y_valid = y[valid_indices]
            model = LinearRegression().fit(X_valid, y_valid)
            features['近5个交易日收盘价线性回归斜率'] = model.coef_[0]
            features['近5个交易日收盘价线性回归R^2'] = model.score(X_valid, y_valid)
        else:
            features['近5个交易日收盘价线性回归斜率'] = 0
            features['近5个交易日收盘价线性回归R^2'] = 0
    else:
        features['近5个交易日收盘价线性回归斜率'] = 0
        features['近5个交易日收盘价线性回归R^2'] = 0

    if len(closing_prices) >= 10:
        X = np.array(range(len(closing_prices[-10:]))).reshape(-1, 1)
        y = np.array(closing_prices[-10:])
        # 过滤掉NaN值
        valid_indices = ~np.isnan(y)
        if np.sum(valid_indices) > 1:
            X_valid = X[valid_indices]
            y_valid = y[valid_indices]
            model = LinearRegression().fit(X_valid, y_valid)
            features['对近10个交易日收盘价线性回归斜率'] = model.coef_[0]
            features['近10个交易日收盘价线性回归R^2'] = model.score(X_valid, y_valid)
        else:
            features['对近10个交易日收盘价线性回归斜率'] = 0
            features['近10个交易日收盘价线性回归R^2'] = 0
    else:
        features['对近10个交易日收盘价线性回归斜率'] = 0
        features['近10个交易日收盘价线性回归R^2'] = 0

    # 27. 近5个交易日 分钟涨跌幅≥±1% 的次数均值
    features['近5个交易日 分钟涨跌幅≥±1% 的次数均值'] = 0  # 需要分钟级数据

    # 28-30. 累积至当日 每日涨跌幅≥±X%的连续天数
    # 计算连续满足条件的天数
    consecutive_47 = 0
    consecutive_97 = 0
    consecutive_197 = 0

    for r in reversed(daily_returns):
        if abs(r) >= 0.047:
            consecutive_47 += 1
        else:
            break

    for r in reversed(daily_returns):
        if abs(r) >= 0.097:
            consecutive_97 += 1
        else:
            break

    for r in reversed(daily_returns):
        if abs(r) >= 0.197:
            consecutive_197 += 1
        else:
            break

    features['累积至当日 每日涨跌幅≥±4.7%的连续天数'] = consecutive_47
    features['累积至当日 每日涨跌幅≥±9.7%的连续天数'] = consecutive_97
    features['累积至当日 每日涨跌幅≥±19.7%的连续天数'] = consecutive_197

    # 31-32. 近N个交易日每日Vwap标准差
    if len(vwap_values) >= 5:
        features['近5个交易日每日Vwap标准差'] = np.std(vwap_values[-5:]) if len(vwap_values[-5:]) > 1 else 0
    else:
        features['近5个交易日每日Vwap标准差'] = 0

    if len(vwap_values) >= 10:
        features['近10个交易日每日Vwap标准差'] = np.std(vwap_values[-10:]) if len(vwap_values[-10:]) > 1 else 0
    else:
        features['近10个交易日每日Vwap标准差'] = 0

    # 33-36. 每日Vwap线性回归斜率和R^2
    if len(vwap_values) >= 5:
        X = np.array(range(len(vwap_values[-5:]))).reshape(-1, 1)
        y = np.array(vwap_values[-5:])
        # 过滤掉NaN值
        valid_indices = ~np.isnan(y)
        if np.sum(valid_indices) > 1:
            X_valid = X[valid_indices]
            y_valid = y[valid_indices]
            model = LinearRegression().fit(X_valid, y_valid)
            features['近5个交易日每日Vwap线性回归斜率'] = model.coef_[0]
            features['近5个交易日每日Vwap线性回归R^2'] = model.score(X_valid, y_valid)
        else:
            features['近5个交易日每日Vwap线性回归斜率'] = 0
            features['近5个交易日每日Vwap线性回归R^2'] = 0
    else:
        features['近5个交易日每日Vwap线性回归斜率'] = 0
        features['近5个交易日每日Vwap线性回归R^2'] = 0

    if len(vwap_values) >= 10:
        X = np.array(range(len(vwap_values[-10:]))).reshape(-1, 1)
        y = np.array(vwap_values[-10:])
        # 过滤掉NaN值
        valid_indices = ~np.isnan(y)
        if np.sum(valid_indices) > 1:
            X_valid = X[valid_indices]
            y_valid = y[valid_indices]
            model = LinearRegression().fit(X_valid, y_valid)
            features['对近10个交易日每日Vwap线性回归斜率'] = model.coef_[0]
            features['近10个交易日每日Vwap线性回归R^2'] = model.score(X_valid, y_valid)
        else:
            features['对近10个交易日每日Vwap线性回归斜率'] = 0
            features['近10个交易日每日Vwap线性回归R^2'] = 0
    else:
        features['对近10个交易日每日Vwap线性回归斜率'] = 0
        features['近10个交易日每日Vwap线性回归R^2'] = 0

    # 37-38. 近N个交易日每日总成交额标准差
    if len(total_turnovers) >= 5:
        features['近5个交易日每日总成交额标准差'] = np.std(total_turnovers[-5:]) if len(total_turnovers[-5:]) > 1 else 0
    else:
        features['近5个交易日每日总成交额标准差'] = 0

    if len(total_turnovers) >= 10:
        features['近10个交易日每日总成交额标准差'] = np.std(total_turnovers[-10:]) if len(
            total_turnovers[-10:]) > 1 else 0
    else:
        features['近10个交易日每日总成交额标准差'] = 0

    # 39-42. 每日总成交额回归分析
    if len(total_turnovers) >= 5:
        X = np.array(range(len(total_turnovers[-5:]))).reshape(-1, 1)
        y = np.array(total_turnovers[-5:])
        # 过滤掉NaN值
        valid_indices = ~np.isnan(y)
        if np.sum(valid_indices) > 1:
            X_valid = X[valid_indices]
            y_valid = y[valid_indices]
            model = LinearRegression().fit(X_valid, y_valid)
            features['近5个交易日每日总成交额回归斜率'] = model.coef_[0]
            features['近5个交易日每日总成交额回归R^2'] = model.score(X_valid, y_valid)
        else:
            features['近5个交易日每日总成交额回归斜率'] = 0
            features['近5个交易日每日总成交额回归R^2'] = 0
    else:
        features['近5个交易日每日总成交额回归斜率'] = 0
        features['近5个交易日每日总成交额回归R^2'] = 0

    if len(total_turnovers) >= 10:
        X = np.array(range(len(total_turnovers[-10:]))).reshape(-1, 1)
        y = np.array(total_turnovers[-10:])
        # 过滤掉NaN值
        valid_indices = ~np.isnan(y)
        if np.sum(valid_indices) > 1:
            X_valid = X[valid_indices]
            y_valid = y[valid_indices]
            model = LinearRegression().fit(X_valid, y_valid)
            features['对近10个交易日每日总成交额线性回归斜率'] = model.coef_[0]
            features['近10个交易日每日总成交额线性回归R^2'] = model.score(X_valid, y_valid)
        else:
            features['对近10个交易日每日总成交额线性回归斜率'] = 0
            features['近10个交易日每日总成交额线性回归R^2'] = 0
    else:
        features['对近10个交易日每日总成交额线性回归斜率'] = 0
        features['近10个交易日每日总成交额线性回归R^2'] = 0

    # 43. 近5个交易日每日振幅标准差
    if len(daily_ranges) >= 5:
        valid_ranges = [r for r in daily_ranges[-5:] if not np.isnan(r)]
        if valid_ranges:
            features['近5个交易日每日振幅标准差'] = np.std(valid_ranges) if len(valid_ranges) > 1 else 0
        else:
            features['近5个交易日每日振幅标准差'] = 0
    else:
        features['近5个交易日每日振幅标准差'] = 0

    # 44. 近10个交易日每日涨跌幅绝对值的标准差
    if len(daily_returns) >= 10:
        abs_returns = [abs(r) for r in daily_returns[-10:]]
        features['近10个交易日每日涨跌幅绝对值的标准差'] = np.std(abs_returns) if len(abs_returns) > 1 else 0
    else:
        features['近10个交易日每日涨跌幅绝对值的标准差'] = 0

    # 45-48. 每日振幅和涨跌幅绝对值线性回归
    if len(daily_ranges) >= 5:
        valid_ranges = [r for r in daily_ranges[-5:] if not np.isnan(r)]
        if len(valid_ranges) > 1:
            X = np.array(range(len(valid_ranges))).reshape(-1, 1)
            y = np.array(valid_ranges)
            model = LinearRegression().fit(X, y)
            features['近5个交易日每日振幅线性回归斜率'] = model.coef_[0]
            features['近5个交易日每日涨跌幅绝对值线性回归R^2'] = model.score(X, y)
        else:
            features['近5个交易日每日振幅线性回归斜率'] = 0
            features['近5个交易日每日涨跌幅绝对值线性回归R^2'] = 0
    else:
        features['近5个交易日每日振幅线性回归斜率'] = 0
        features['近5个交易日每日涨跌幅绝对值线性回归R^2'] = 0

    if len(daily_ranges) >= 10:
        valid_ranges = [r for r in daily_ranges[-10:] if not np.isnan(r)]
        if len(valid_ranges) > 1:
            X = np.array(range(len(valid_ranges))).reshape(-1, 1)
            y = np.array(valid_ranges)
            model = LinearRegression().fit(X, y)
            features['近10个交易日每日振幅线性回归斜率'] = model.coef_[0]
            features['近10个交易日每日涨跌幅绝对值线性回归R^2'] = model.score(X, y)
        else:
            features['近10个交易日每日振幅线性回归斜率'] = 0
            features['近10个交易日每日涨跌幅绝对值线性回归R^2'] = 0
    else:
        features['近10个交易日每日振幅线性回归斜率'] = 0
        features['近10个交易日每日涨跌幅绝对值线性回归R^2'] = 0

    return features



# 定义特征计算函数
def cal_minute_f1(df):
    """计算日内分钟级量价关系特征"""
    features = {}

    # 确保数据按分钟排序（使用正确的时间格式排序）
    df['time_obj'] = pd.to_datetime(df['time'], format='%H:%M')
    df = df.sort_values(by='time_obj')

    # 计算分钟涨跌幅
    df['price_change'] = df['price'].pct_change()
    df.iloc[0, df.columns.get_loc('price_change')] = 0  # 第一笔交易的涨跌幅为0

    # 1. 分钟涨跌幅标准差
    features['分钟涨跌幅标准差'] = df['price_change'].std()

    # 2. 分钟涨跌幅偏度
    features['分钟涨跌幅偏度'] = df['price_change'].skew()

    # 3. 分钟涨跌幅峰度
    features['分钟涨跌幅峰度'] = df['price_change'].kurtosis()

    # 4. √(∑(分钟涨跌幅^2)) - 已实现波动率
    realized_volatility = np.sqrt((df['price_change'] ** 2).sum())
    features['已实现波动率'] = realized_volatility

    # 5. 当日最大分钟涨跌幅
    features['当日最大分钟涨跌幅'] = df['price_change'].max()

    # 6. 当日最小分钟涨跌幅
    features['当日最小分钟涨跌幅'] = df['price_change'].min()

    # 7-8. 当日分钟级涨跌幅持续为正/负的最长分钟间隔及对应成交量占比
    # 过滤掉涨跌幅为0的数据
    df_nonzero = df[df['price_change'] != 0].copy()

    if len(df_nonzero) > 0:
        # 标记涨跌幅符号
        df_nonzero['sign'] = np.sign(df_nonzero['price_change'])

        # 计算连续正/负涨跌幅的最长间隔
        positive_intervals = []
        negative_intervals = []
        current_positive_start = None
        current_negative_start = None

        for idx, row in df_nonzero.iterrows():
            sign = row['sign']
            if sign > 0:  # 正涨跌幅
                if current_positive_start is None:
                    current_positive_start = idx
                if current_negative_start is not None:
                    negative_intervals.append(idx - current_negative_start)
                    current_negative_start = None
            else:  # 负涨跌幅
                if current_negative_start is None:
                    current_negative_start = idx
                if current_positive_start is not None:
                    positive_intervals.append(idx - current_positive_start)
                    current_positive_start = None

        # 处理最后一个区间
        if current_positive_start is not None:
            positive_intervals.append(len(df_nonzero) - current_positive_start)
        if current_negative_start is not None:
            negative_intervals.append(len(df_nonzero) - current_negative_start)

        # 计算最长间隔
        max_positive_interval = max(positive_intervals) if positive_intervals else 0
        max_negative_interval = max(negative_intervals) if negative_intervals else 0

        features['最长正涨跌幅分钟间隔'] = max_positive_interval
        features['最长负涨跌幅分钟间隔'] = max_negative_interval

        # 计算对应成交量占比
        total_volume = df['volume'].sum()
        if total_volume != 0:
            if max_positive_interval > 0:
                # 找到最长正涨跌幅区间对应的成交量
                positive_volume = df_nonzero[df_nonzero['sign'] > 0]['volume'].sum()
                features['最长正涨跌幅分钟间隔对应成交量占比'] = positive_volume / total_volume
            else:
                features['最长正涨跌幅分钟间隔对应成交量占比'] = 0

            if max_negative_interval > 0:
                # 找到最长负涨跌幅区间对应的成交量
                negative_volume = df_nonzero[df_nonzero['sign'] < 0]['volume'].sum()
                features['最长负涨跌幅分钟间隔对应成交量占比'] = negative_volume / total_volume
            else:
                features['最长负涨跌幅分钟间隔对应成交量占比'] = 0
        else:
            features['最长正涨跌幅分钟间隔对应成交量占比'] = 0
            features['最长负涨跌幅分钟间隔对应成交量占比'] = 0
    else:
        features['最长正涨跌幅分钟间隔'] = 0
        features['最长负涨跌幅分钟间隔'] = 0
        features['最长正涨跌幅分钟间隔对应成交量占比'] = 0
        features['最长负涨跌幅分钟间隔对应成交量占比'] = 0

    # 9. 分钟涨跌幅绝对值均值
    features['分钟涨跌幅绝对值均值'] = df['price_change'].abs().mean()

    # 10. 分钟涨跌幅绝对值标准差
    features['分钟涨跌幅绝对值标准差'] = df['price_change'].abs().std()

    # 11. 分钟涨跌幅上下波动不对称比率
    positive_changes = df['price_change'][df['price_change'] > 0]
    negative_changes = df['price_change'][df['price_change'] < 0]
    avg_positive = positive_changes.mean() if len(positive_changes) > 0 else 0
    avg_negative = negative_changes.mean() if len(negative_changes) > 0 else 0
    features['分钟涨跌幅上下波动不对称比率'] = abs(avg_positive / avg_negative) if avg_negative != 0 else np.nan

    # 12. 上下波动切换次数
    # 统计涨跌幅符号切换次数
    sign_changes = 0
    prev_sign = None
    for change in df['price_change']:
        if change != 0:
            current_sign = np.sign(change)
            if prev_sign is not None and current_sign != prev_sign:
                sign_changes += 1
            prev_sign = current_sign
    features['上下波动切换次数'] = sign_changes

    # 13. 尾盘波动放大线索 (14:30-15:00涨跌幅标准差/全天涨跌幅标准差)
    tail_df = df[df['time_obj'].dt.time >= pd.to_datetime('14:30', format='%H:%M').time()]
    if len(tail_df) > 1:
        tail_std = tail_df['price_change'].std()
        all_std = df['price_change'].std()
        features['尾盘波动放大线索'] = tail_std / all_std if all_std != 0 else np.nan
    else:
        features['尾盘波动放大线索'] = np.nan

    # 14. 开盘波动放大线索 (9:30-10:00涨跌幅标准差/全天涨跌幅标准差)
    open_df = df[(df['time_obj'].dt.time >= pd.to_datetime('9:30', format='%H:%M').time()) &
                 (df['time_obj'].dt.time <= pd.to_datetime('10:00', format='%H:%M').time())]
    if len(open_df) > 1:
        open_std = open_df['price_change'].std()
        all_std = df['price_change'].std()
        features['开盘波动放大线索'] = open_std / all_std if all_std != 0 else np.nan
    else:
        features['开盘波动放大线索'] = np.nan

    return features


def cal_minute_f2(df):
    """计算停牌识别特征"""
    features = {}

    # 确保数据按分钟排序（使用正确的时间格式排序）
    df['time_obj'] = pd.to_datetime(df['time'], format='%H:%M')
    df = df.sort_values(by='time_obj')

    # 将时间转换为分钟数（相对于9:30）
    df['minutes_from_start'] = df['time_obj'].apply(lambda x: (x.hour - 9) * 60 + x.minute - 30)

    # 1. （240-当日实际交易分钟数）/240
    actual_trading_minutes = df['time'].nunique()
    features['停牌比例_全天'] = (240 - actual_trading_minutes) / 240 if 240 != 0 else 0

    # 2. （121-（上午9:30-11:30实际有交易的分钟数））/121
    morning_df = df[(df['time_obj'].dt.time >= pd.to_datetime('9:30', format='%H:%M').time()) &
                    (df['time_obj'].dt.time <= pd.to_datetime('11:30', format='%H:%M').time())]
    morning_trading_minutes = morning_df['time'].nunique()
    features['停牌比例_上午'] = (121 - morning_trading_minutes) / 121 if 121 != 0 else 0

    # 3. 13:00起首笔成交时间与13:00差值（分钟）
    afternoon_df = df[(df['time_obj'].dt.time >= pd.to_datetime('13:00', format='%H:%M').time())]
    if len(afternoon_df) > 0:
        first_afternoon_time = afternoon_df['time_obj'].iloc[0]
        afternoon_start = pd.to_datetime('13:00', format='%H:%M')
        features['下午首笔成交延迟'] = (first_afternoon_time - afternoon_start).total_seconds() / 60
    else:
        features['下午首笔成交延迟'] = np.nan

    # 4. 首笔成交时间与9:30差值（分钟）
    if len(df) > 0:
        first_trade_time = df['time_obj'].iloc[0]
        market_open = pd.to_datetime('9:30', format='%H:%M')
        features['开盘首笔成交延迟'] = (first_trade_time - market_open).total_seconds() / 60
    else:
        features['开盘首笔成交延迟'] = np.nan

    # 5-6. 早盘和午盘最大缺口（分钟的间隔）
    def find_max_gap(time_series, start_time, end_time):
        """计算指定时间段内的最大交易缺口"""
        if len(time_series) == 0:
            return 0

        # 过滤时间段内的数据
        filtered_times = time_series[(time_series >= start_time) & (time_series <= end_time)]
        if len(filtered_times) <= 1:
            return 0

        # 计算相邻时间点的间隔
        gaps = np.diff(filtered_times)
        return gaps.max() if len(gaps) > 0 else 0

    # 早盘最大缺口（9:30-11:30）
    morning_times = morning_df['minutes_from_start'].values if len(morning_df) > 0 else np.array([])
    features['早盘最大缺口'] = find_max_gap(morning_times, 0, 120)

    # 午盘最大缺口（13:00-15:00）
    afternoon_times = afternoon_df['minutes_from_start'].values if len(afternoon_df) > 0 else np.array([])
    features['午盘最大缺口'] = find_max_gap(afternoon_times, 180, 300)

    # 7. 上午和下午交易分钟数比值
    afternoon_trading_minutes = afternoon_df['time'].nunique()
    features[
        '下午交易分钟数_上午交易分钟数'] = afternoon_trading_minutes / morning_trading_minutes if morning_trading_minutes != 0 else np.nan

    # 8. 最大连续无交易分钟数
    if len(df) > 1:
        # 计算相邻交易时间的间隔
        time_diffs = df['minutes_from_start'].diff().dropna()
        max_no_trade_gap = time_diffs.max() if len(time_diffs) > 0 else 0
        features['最大连续无交易分钟数'] = max_no_trade_gap
    else:
        features['最大连续无交易分钟数'] = 0

    # 9. 交易活跃分钟占比（交易分钟数/理论交易分钟数）
    features['交易活跃分钟占比'] = actual_trading_minutes / 240 if 240 != 0 else 0

    # 10. 早盘交易活跃度（早盘交易分钟数/理论早盘交易分钟数）
    features['早盘交易活跃度'] = morning_trading_minutes / 121 if 121 != 0 else 0

    # 11. 午盘交易活跃度（午盘交易分钟数/理论午盘交易分钟数）
    features['午盘交易活跃度'] = afternoon_trading_minutes / 119 if 119 != 0 else 0

    # 12. 早盘与午盘交易活跃度差异
    features['早盘午盘交易活跃度差异'] = features['早盘交易活跃度'] - features['午盘交易活跃度']

    return features


# 定义特征计算函数
def cal_basic_f1(df):
    """计算日内基础量价关系特征"""
    features = {}

    # 确保数据按分钟排序（使用正确的时间格式排序）
    df['time_obj'] = pd.to_datetime(df['time'], format='%H:%M')
    df = df.sort_values(by='time_obj')

    # 当日收盘价/当日开盘价-1
    if len(df) > 0:
        open_price = df['price'].iloc[0]
        close_price = df['price'].iloc[-1]
        features['日内整体涨跌1'] = close_price / open_price - 1 if open_price != 0 else np.nan
    else:
        features['日内整体涨跌1'] = np.nan

    # 当日开盘价/当日收盘价-1
    if len(df) > 0:
        open_price = df['price'].iloc[0]
        close_price = df['price'].iloc[-1]
        features['日内整体涨跌2'] = open_price / close_price - 1 if close_price != 0 else np.nan
    else:
        features['日内整体涨跌2'] = np.nan

    # 当日收盘价
    features['当日收盘价'] = df['price'].iloc[-1] if len(df) > 0 else np.nan

    # 每日均价
    total_volume = df['volume'].sum()
    avg_price = (df['price'] * df['volume']).sum() / total_volume if total_volume != 0 else np.nan
    features['每日均价'] = df['price'].mean()

    # 每日Vwap
    vwap = avg_price
    features['每日Vwap'] = vwap

    # 14:55-15:00Vwap/每日Vwap
    end_df = df[(df['time_obj'].dt.time >= pd.to_datetime('14:55', format='%H:%M').time()) &
                (df['time_obj'].dt.time <= pd.to_datetime('15:00', format='%H:%M').time())]
    end_total_volume = end_df['volume'].sum()
    end_vwap = (end_df['price'] * end_df['volume']).sum() / end_total_volume if end_total_volume != 0 else np.nan
    features['尾盘拉抬_打压线索'] = end_vwap / vwap if vwap != 0 and not np.isnan(vwap) else np.nan

    # 每日总成交量
    features['每日总成交量'] = total_volume

    # 每日总成交额
    features['每日总成交额'] = (df['price'] * df['volume']).sum()

    # 分钟成交量均值
    features['分钟成交量均值'] = df['volume'].mean()

    # 分钟成交量中位数
    features['分钟成交量中位数'] = df['volume'].median()

    # 分钟成交量标准差
    features['分钟成交量标准差'] = df['volume'].std()

    # 成交量离散度
    mean_volume = df['volume'].mean()
    features['成交量离散度'] = df['volume'].std() / mean_volume if mean_volume != 0 else np.nan

    # 分钟最大成交量
    features['分钟最大成交量'] = df['volume'].max()

    # 成交是否集中1 (最大成交量/平均成交量)
    features['成交是否集中1'] = features['分钟最大成交量'] / mean_volume if mean_volume != 0 else np.nan

    # 分钟成交额均值
    df['turnover'] = df['price'] * df['volume']
    features['分钟成交额均值'] = df['turnover'].mean()

    # 分钟成交额中位数
    features['分钟成交额中位数'] = df['turnover'].median()

    # 分钟成交额标准差
    features['分钟成交额标准差'] = df['turnover'].std()

    # 成交额离散度
    mean_turnover = df['turnover'].mean()
    features['成交额离散度'] = df['turnover'].std() / mean_turnover if mean_turnover != 0 else np.nan

    # 分钟最大成交额
    features['分钟最大成交额'] = df['turnover'].max()

    # 成交是否集中2 (最大成交额/平均成交额)
    features['成交是否集中2'] = features['分钟最大成交额'] / mean_turnover if mean_turnover != 0 else np.nan

    # 尾盘成交集中度 (14:30-15:00成交额/总成交额)
    tail_df = df[df['time_obj'].dt.time >= pd.to_datetime('14:30', format='%H:%M').time()]
    tail_turnover = tail_df['turnover'].sum()
    total_turnover = df['turnover'].sum()
    features['尾盘成交集中度'] = tail_turnover / total_turnover if total_turnover != 0 else np.nan

    # 午休断点变动 ((13:00价格-11:30价格)/11:30价格)
    morning_end_df = df[df['time_obj'].dt.time <= pd.to_datetime('11:30', format='%H:%M').time()]
    afternoon_start_df = df[df['time_obj'].dt.time >= pd.to_datetime('13:00', format='%H:%M').time()]
    if len(morning_end_df) > 0 and len(afternoon_start_df) > 0:
        morning_end_price = morning_end_df['price'].iloc[-1]
        afternoon_start_price = afternoon_start_df['price'].iloc[0]
        features['午休断点变动'] = (
                                               afternoon_start_price - morning_end_price) / morning_end_price if morning_end_price != 0 else np.nan
    else:
        features['午休断点变动'] = np.nan

    # 以成交额/波动率近似流动性 (总成交额/价格标准差)
    price_std = df['price'].std()
    features['以成交额_波动率近似流动性'] = total_turnover / price_std if price_std != 0 else np.nan

    # 开盘成交集中度1 (9:30-9:40成交额/总成交额)
    open_df = df[(df['time_obj'].dt.time >= pd.to_datetime('9:30', format='%H:%M').time()) &
                 (df['time_obj'].dt.time <= pd.to_datetime('9:40', format='%H:%M').time())]
    open_turnover = open_df['turnover'].sum()
    features['开盘成交集中度1'] = open_turnover / total_turnover if total_turnover != 0 else np.nan

    # 开盘成交集中度2 (9:40-10:00成交额/总成交额)
    open2_df = df[(df['time_obj'].dt.time > pd.to_datetime('9:40', format='%H:%M').time()) &
                  (df['time_obj'].dt.time <= pd.to_datetime('10:00', format='%H:%M').time())]
    open2_turnover = open2_df['turnover'].sum()
    features['开盘成交集中度2'] = open2_turnover / total_turnover if total_turnover != 0 else np.nan

    # 开盘断点变动 ((9:31价格-9:30价格)/9:30价格)
    open_start_df = df[df['time_obj'].dt.time == pd.to_datetime('9:30', format='%H:%M').time()]
    open_next_df = df[df['time_obj'].dt.time == pd.to_datetime('9:31', format='%H:%M').time()]
    if len(open_start_df) > 0 and len(open_next_df) > 0:
        open_start_price = open_start_df['price'].iloc[0]
        open_next_price = open_next_df['price'].iloc[0]
        features['开盘断点变动'] = (
                                               open_next_price - open_start_price) / open_start_price if open_start_price != 0 else np.nan
    else:
        features['开盘断点变动'] = np.nan

    # 跳空后的延续/回补 (暂时无法计算，需要前一天数据)
    features['跳空后的延续_回补'] = np.nan

    # 开盘交易集中度 (9:30-10:00成交量/总成交量)
    open_volume = (open_df['volume'].sum() + open2_df['volume'].sum())
    features['开盘交易集中度'] = open_volume / total_volume if total_volume != 0 else np.nan

    # 每日最高价/每日Vwap
    features['每日最高价_每日Vwap'] = df['price'].max() / vwap if vwap != 0 and not np.isnan(vwap) else np.nan

    # 每日价格中位数/每日Vwap
    features['每日价格中位数_每日Vwap'] = df['price'].median() / vwap if vwap != 0 and not np.isnan(vwap) else np.nan

    # 每日价格偏度
    features['每日价格偏度'] = df['price'].skew()

    # 每日最低价/每日Vwap
    features['每日最低价_每日Vwap'] = df['price'].min() / vwap if vwap != 0 and not np.isnan(vwap) else np.nan

    # 每日价格标准差/每日Vwap
    price_std = df['price'].std()
    features['每日价格标准差_每日Vwap'] = price_std / vwap if vwap != 0 and not np.isnan(vwap) else np.nan

    return features


def cal_basic_f2(df):
    """计算日内分钟级量价关系特征"""
    features = {}

    # 确保数据按分钟排序（使用正确的时间格式排序）
    df['time_obj'] = pd.to_datetime(df['time'], format='%H:%M')
    df = df.sort_values(by='time_obj')

    # 计算分钟涨跌幅
    df['price_change'] = df['price'].pct_change()
    df.iloc[0, df.columns.get_loc('price_change')] = 0  # 第一笔交易的涨跌幅为0

    # 1. 分钟涨跌幅标准差
    features['分钟涨跌幅标准差'] = df['price_change'].std()

    # 2. 分钟涨跌幅偏度
    features['分钟涨跌幅偏度'] = df['price_change'].skew()

    # 3. 分钟涨跌幅峰度
    features['分钟涨跌幅峰度'] = df['price_change'].kurtosis()

    # 4. √(∑(分钟涨跌幅^2)) - 已实现波动率
    realized_volatility = np.sqrt((df['price_change'] ** 2).sum())
    features['已实现波动率'] = realized_volatility

    # 5. 当日最大分钟涨跌幅
    features['当日最大分钟涨跌幅'] = df['price_change'].max()

    # 6. 当日最小分钟涨跌幅
    features['当日最小分钟涨跌幅'] = df['price_change'].min()

    # 7-8. 当日分钟级涨跌幅持续为正/负的最长分钟间隔及对应成交量占比
    # 过滤掉涨跌幅为0的数据
    df_nonzero = df[df['price_change'] != 0].copy()

    if len(df_nonzero) > 0:
        # 标记涨跌幅符号
        df_nonzero['sign'] = np.sign(df_nonzero['price_change'])

        # 计算连续正/负涨跌幅的最长间隔
        positive_intervals = []
        negative_intervals = []
        current_positive_start = None
        current_negative_start = None

        for idx, row in df_nonzero.iterrows():
            sign = row['sign']
            if sign > 0:  # 正涨跌幅
                if current_positive_start is None:
                    current_positive_start = idx
                if current_negative_start is not None:
                    negative_intervals.append(idx - current_negative_start)
                    current_negative_start = None
            else:  # 负涨跌幅
                if current_negative_start is None:
                    current_negative_start = idx
                if current_positive_start is not None:
                    positive_intervals.append(idx - current_positive_start)
                    current_positive_start = None

        # 处理最后一个区间
        if current_positive_start is not None:
            positive_intervals.append(len(df_nonzero) - current_positive_start)
        if current_negative_start is not None:
            negative_intervals.append(len(df_nonzero) - current_negative_start)

        # 计算最长间隔
        max_positive_interval = max(positive_intervals) if positive_intervals else 0
        max_negative_interval = max(negative_intervals) if negative_intervals else 0

        features['最长正涨跌幅分钟间隔'] = max_positive_interval
        features['最长负涨跌幅分钟间隔'] = max_negative_interval

        # 计算对应成交量占比
        total_volume = df['volume'].sum()
        if total_volume != 0:
            if max_positive_interval > 0:
                # 找到最长正涨跌幅区间对应的成交量
                positive_volume = df_nonzero[df_nonzero['sign'] > 0]['volume'].sum()
                features['最长正涨跌幅分钟间隔对应成交量占比'] = positive_volume / total_volume
            else:
                features['最长正涨跌幅分钟间隔对应成交量占比'] = 0

            if max_negative_interval > 0:
                # 找到最长负涨跌幅区间对应的成交量
                negative_volume = df_nonzero[df_nonzero['sign'] < 0]['volume'].sum()
                features['最长负涨跌幅分钟间隔对应成交量占比'] = negative_volume / total_volume
            else:
                features['最长负涨跌幅分钟间隔对应成交量占比'] = 0
        else:
            features['最长正涨跌幅分钟间隔对应成交量占比'] = 0
            features['最长负涨跌幅分钟间隔对应成交量占比'] = 0
    else:
        features['最长正涨跌幅分钟间隔'] = 0
        features['最长负涨跌幅分钟间隔'] = 0
        features['最长正涨跌幅分钟间隔对应成交量占比'] = 0
        features['最长负涨跌幅分钟间隔对应成交量占比'] = 0

    # 9. 分钟涨跌幅绝对值均值
    features['分钟涨跌幅绝对值均值'] = df['price_change'].abs().mean()

    # 10. 分钟涨跌幅绝对值标准差
    features['分钟涨跌幅绝对值标准差'] = df['price_change'].abs().std()

    # 11. 分钟涨跌幅上下波动不对称比率
    positive_changes = df['price_change'][df['price_change'] > 0]
    negative_changes = df['price_change'][df['price_change'] < 0]
    avg_positive = positive_changes.mean() if len(positive_changes) > 0 else 0
    avg_negative = negative_changes.mean() if len(negative_changes) > 0 else 0
    features['分钟涨跌幅上下波动不对称比率'] = abs(avg_positive / avg_negative) if avg_negative != 0 else np.nan

    # 12. 上下波动切换次数
    # 统计涨跌幅符号切换次数
    sign_changes = 0
    prev_sign = None
    for change in df['price_change']:
        if change != 0:
            current_sign = np.sign(change)
            if prev_sign is not None and current_sign != prev_sign:
                sign_changes += 1
            prev_sign = current_sign
    features['上下波动切换次数'] = sign_changes

    # 13. 尾盘波动放大线索 (14:30-15:00涨跌幅标准差/全天涨跌幅标准差)
    tail_df = df[df['time_obj'].dt.time >= pd.to_datetime('14:30', format='%H:%M').time()]
    if len(tail_df) > 1:
        tail_std = tail_df['price_change'].std()
        all_std = df['price_change'].std()
        features['尾盘波动放大线索'] = tail_std / all_std if all_std != 0 else np.nan
    else:
        features['尾盘波动放大线索'] = np.nan

    # 14. 开盘波动放大线索 (9:30-10:00涨跌幅标准差/全天涨跌幅标准差)
    open_df = df[(df['time_obj'].dt.time >= pd.to_datetime('9:30', format='%H:%M').time()) &
                 (df['time_obj'].dt.time <= pd.to_datetime('10:00', format='%H:%M').time())]
    if len(open_df) > 1:
        open_std = open_df['price_change'].std()
        all_std = df['price_change'].std()
        features['开盘波动放大线索'] = open_std / all_std if all_std != 0 else np.nan
    else:
        features['开盘波动放大线索'] = np.nan

    return features


def cal_basic_f3(df):
    """计算停牌识别特征"""
    features = {}

    # 确保数据按分钟排序（使用正确的时间格式排序）
    df['time_obj'] = pd.to_datetime(df['time'], format='%H:%M')
    df = df.sort_values(by='time_obj')

    # 将时间转换为分钟数（相对于9:30）
    df['minutes_from_start'] = df['time_obj'].apply(lambda x: (x.hour - 9) * 60 + x.minute - 30)

    # 1. （240-当日实际交易分钟数）/240
    actual_trading_minutes = df['time'].nunique()
    features['停牌比例_全天'] = (240 - actual_trading_minutes) / 240 if 240 != 0 else 0

    # 2. （121-（上午9:30-11:30实际有交易的分钟数））/121
    morning_df = df[(df['time_obj'].dt.time >= pd.to_datetime('9:30', format='%H:%M').time()) &
                    (df['time_obj'].dt.time <= pd.to_datetime('11:30', format='%H:%M').time())]
    morning_trading_minutes = morning_df['time'].nunique()
    features['停牌比例_上午'] = (121 - morning_trading_minutes) / 121 if 121 != 0 else 0

    # 3. 13:00起首笔成交时间与13:00差值（分钟）
    afternoon_df = df[(df['time_obj'].dt.time >= pd.to_datetime('13:00', format='%H:%M').time())]
    if len(afternoon_df) > 0:
        first_afternoon_time = afternoon_df['time_obj'].iloc[0]
        afternoon_start = pd.to_datetime('13:00', format='%H:%M')
        features['下午首笔成交延迟'] = (first_afternoon_time - afternoon_start).total_seconds() / 60
    else:
        features['下午首笔成交延迟'] = np.nan

    # 4. 首笔成交时间与9:30差值（分钟）
    if len(df) > 0:
        first_trade_time = df['time_obj'].iloc[0]
        market_open = pd.to_datetime('9:30', format='%H:%M')
        features['开盘首笔成交延迟'] = (first_trade_time - market_open).total_seconds() / 60
    else:
        features['开盘首笔成交延迟'] = np.nan

    # 5-6. 早盘和午盘最大缺口（分钟的间隔）
    def find_max_gap(time_series, start_time, end_time):
        """计算指定时间段内的最大交易缺口"""
        if len(time_series) == 0:
            return 0

        # 过滤时间段内的数据
        filtered_times = time_series[(time_series >= start_time) & (time_series <= end_time)]
        if len(filtered_times) <= 1:
            return 0

        # 计算相邻时间点的间隔
        gaps = np.diff(filtered_times)
        return gaps.max() if len(gaps) > 0 else 0

    # 早盘最大缺口（9:30-11:30）
    morning_times = morning_df['minutes_from_start'].values if len(morning_df) > 0 else np.array([])
    features['早盘最大缺口'] = find_max_gap(morning_times, 0, 120)

    # 午盘最大缺口（13:00-15:00）
    afternoon_times = afternoon_df['minutes_from_start'].values if len(afternoon_df) > 0 else np.array([])
    features['午盘最大缺口'] = find_max_gap(afternoon_times, 180, 300)

    # 7. 上午和下午交易分钟数比值
    afternoon_trading_minutes = afternoon_df['time'].nunique()
    features[
        '下午交易分钟数_上午交易分钟数'] = afternoon_trading_minutes / morning_trading_minutes if morning_trading_minutes != 0 else np.nan

    # 8. 最大连续无交易分钟数
    if len(df) > 1:
        # 计算相邻交易时间的间隔
        time_diffs = df['minutes_from_start'].diff().dropna()
        max_no_trade_gap = time_diffs.max() if len(time_diffs) > 0 else 0
        features['最大连续无交易分钟数'] = max_no_trade_gap
    else:
        features['最大连续无交易分钟数'] = 0

    # 9. 交易活跃分钟占比（交易分钟数/理论交易分钟数）
    features['交易活跃分钟占比'] = actual_trading_minutes / 240 if 240 != 0 else 0

    # 10. 早盘交易活跃度（早盘交易分钟数/理论早盘交易分钟数）
    features['早盘交易活跃度'] = morning_trading_minutes / 121 if 121 != 0 else 0

    # 11. 午盘交易活跃度（午盘交易分钟数/理论午盘交易分钟数）
    features['午盘交易活跃度'] = afternoon_trading_minutes / 119 if 119 != 0 else 0

    # 12. 早盘与午盘交易活跃度差异
    features['早盘午盘交易活跃度差异'] = features['早盘交易活跃度'] - features['午盘交易活跃度']

    return features



def cal_suspension_f1(df):
    """计算日内基础量价关系特征"""
    features = {}

    # 确保数据按分钟排序（使用正确的时间格式排序）
    df['time_obj'] = pd.to_datetime(df['time'], format='%H:%M')
    df = df.sort_values(by='time_obj')

    # 当日收盘价/当日开盘价-1
    if len(df) > 0:
        open_price = df['price'].iloc[0]
        close_price = df['price'].iloc[-1]
        features['日内整体涨跌1'] = close_price / open_price - 1 if open_price != 0 else np.nan
    else:
        features['日内整体涨跌1'] = np.nan

    # 当日开盘价/当日收盘价-1
    if len(df) > 0:
        open_price = df['price'].iloc[0]
        close_price = df['price'].iloc[-1]
        features['日内整体涨跌2'] = open_price / close_price - 1 if close_price != 0 else np.nan
    else:
        features['日内整体涨跌2'] = np.nan

    # 当日收盘价
    features['当日收盘价'] = df['price'].iloc[-1] if len(df) > 0 else np.nan

    # 每日均价
    total_volume = df['volume'].sum()
    avg_price = (df['price'] * df['volume']).sum() / total_volume if total_volume != 0 else np.nan
    features['每日均价'] = avg_price

    # 每日Vwap
    vwap = avg_price
    features['每日Vwap'] = vwap

    # 14:55-15:00Vwap/每日Vwap
    end_df = df[(df['time_obj'].dt.time >= pd.to_datetime('14:55', format='%H:%M').time()) &
                (df['time_obj'].dt.time <= pd.to_datetime('15:00', format='%H:%M').time())]
    end_total_volume = end_df['volume'].sum()
    end_vwap = (end_df['price'] * end_df['volume']).sum() / end_total_volume if end_total_volume != 0 else np.nan
    features['尾盘拉抬_打压线索'] = end_vwap / vwap if vwap != 0 and not np.isnan(vwap) else np.nan

    # 每日总成交量
    features['每日总成交量'] = total_volume

    # 每日总成交额
    features['每日总成交额'] = (df['price'] * df['volume']).sum()

    # 分钟成交量均值
    features['分钟成交量均值'] = df['volume'].mean()

    # 分钟成交量中位数
    features['分钟成交量中位数'] = df['volume'].median()

    # 分钟成交量标准差
    features['分钟成交量标准差'] = df['volume'].std()

    # 成交量离散度
    mean_volume = df['volume'].mean()
    features['成交量离散度'] = df['volume'].std() / mean_volume if mean_volume != 0 else np.nan

    # 分钟最大成交量
    features['分钟最大成交量'] = df['volume'].max()

    # 成交是否集中1 (最大成交量/平均成交量)
    features['成交是否集中1'] = features['分钟最大成交量'] / mean_volume if mean_volume != 0 else np.nan

    # 分钟成交额均值
    df['turnover'] = df['price'] * df['volume']
    features['分钟成交额均值'] = df['turnover'].mean()

    # 分钟成交额中位数
    features['分钟成交额中位数'] = df['turnover'].median()

    # 分钟成交额标准差
    features['分钟成交额标准差'] = df['turnover'].std()

    # 成交额离散度
    mean_turnover = df['turnover'].mean()
    features['成交额离散度'] = df['turnover'].std() / mean_turnover if mean_turnover != 0 else np.nan

    # 分钟最大成交额
    features['分钟最大成交额'] = df['turnover'].max()

    # 成交是否集中2 (最大成交额/平均成交额)
    features['成交是否集中2'] = features['分钟最大成交额'] / mean_turnover if mean_turnover != 0 else np.nan

    # 尾盘成交集中度 (14:30-15:00成交额/总成交额)
    tail_df = df[df['time_obj'].dt.time >= pd.to_datetime('14:30', format='%H:%M').time()]
    tail_turnover = tail_df['turnover'].sum()
    total_turnover = df['turnover'].sum()
    features['尾盘成交集中度'] = tail_turnover / total_turnover if total_turnover != 0 else np.nan

    # 午休断点变动 ((13:00价格-11:30价格)/11:30价格)
    morning_end_df = df[df['time_obj'].dt.time <= pd.to_datetime('11:30', format='%H:%M').time()]
    afternoon_start_df = df[df['time_obj'].dt.time >= pd.to_datetime('13:00', format='%H:%M').time()]
    if len(morning_end_df) > 0 and len(afternoon_start_df) > 0:
        morning_end_price = morning_end_df['price'].iloc[-1]
        afternoon_start_price = afternoon_start_df['price'].iloc[0]
        features['午休断点变动'] = (
                                               afternoon_start_price - morning_end_price) / morning_end_price if morning_end_price != 0 else np.nan
    else:
        features['午休断点变动'] = np.nan

    # 以成交额/波动率近似流动性 (总成交额/价格标准差)
    price_std = df['price'].std()
    features['以成交额_波动率近似流动性'] = total_turnover / price_std if price_std != 0 else np.nan

    # 开盘成交集中度1 (9:30-9:40成交额/总成交额)
    open_df = df[(df['time_obj'].dt.time >= pd.to_datetime('9:30', format='%H:%M').time()) &
                 (df['time_obj'].dt.time <= pd.to_datetime('9:40', format='%H:%M').time())]
    open_turnover = open_df['turnover'].sum()
    features['开盘成交集中度1'] = open_turnover / total_turnover if total_turnover != 0 else np.nan

    # 开盘成交集中度2 (9:40-10:00成交额/总成交额)
    open2_df = df[(df['time_obj'].dt.time > pd.to_datetime('9:40', format='%H:%M').time()) &
                  (df['time_obj'].dt.time <= pd.to_datetime('10:00', format='%H:%M').time())]
    open2_turnover = open2_df['turnover'].sum()
    features['开盘成交集中度2'] = open2_turnover / total_turnover if total_turnover != 0 else np.nan

    # 开盘断点变动 ((9:31价格-9:30价格)/9:30价格)
    open_start_df = df[df['time_obj'].dt.time == pd.to_datetime('9:30', format='%H:%M').time()]
    open_next_df = df[df['time_obj'].dt.time == pd.to_datetime('9:31', format='%H:%M').time()]
    if len(open_start_df) > 0 and len(open_next_df) > 0:
        open_start_price = open_start_df['price'].iloc[0]
        open_next_price = open_next_df['price'].iloc[0]
        features['开盘断点变动'] = (
                                               open_next_price - open_start_price) / open_start_price if open_start_price != 0 else np.nan
    else:
        features['开盘断点变动'] = np.nan

    # 跳空后的延续/回补 (暂时无法计算，需要前一天数据)
    features['跳空后的延续_回补'] = np.nan

    # 开盘交易集中度 (9:30-10:00成交量/总成交量)
    open_volume = (open_df['volume'].sum() + open2_df['volume'].sum())
    features['开盘交易集中度'] = open_volume / total_volume if total_volume != 0 else np.nan

    # 每日最高价/每日Vwap
    features['每日最高价_每日Vwap'] = df['price'].max() / vwap if vwap != 0 and not np.isnan(vwap) else np.nan

    # 每日价格中位数/每日Vwap
    features['每日价格中位数_每日Vwap'] = df['price'].median() / vwap if vwap != 0 and not np.isnan(vwap) else np.nan

    # 每日价格偏度
    features['每日价格偏度'] = df['price'].skew()

    # 每日最低价/每日Vwap
    features['每日最低价_每日Vwap'] = df['price'].min() / vwap if vwap != 0 and not np.isnan(vwap) else np.nan

    # 每日价格标准差/每日Vwap
    price_std = df['price'].std()
    features['每日价格标准差_每日Vwap'] = price_std / vwap if vwap != 0 and not np.isnan(vwap) else np.nan

    return features


def cal_suspension_f2(df):
    """计算停牌识别特征"""
    features = {}

    # 确保数据按分钟排序（使用正确的时间格式排序）
    df['time_obj'] = pd.to_datetime(df['time'], format='%H:%M')
    df = df.sort_values(by='time_obj')

    # 将时间转换为分钟数（相对于9:30）
    df['minutes_from_start'] = df['time_obj'].apply(lambda x: (x.hour - 9) * 60 + x.minute - 30)

    # 1. （240-当日实际交易分钟数）/240
    actual_trading_minutes = df['time'].nunique()
    features['停牌比例_全天'] = (240 - actual_trading_minutes) / 240 if 240 != 0 else 0

    # 2. （121-（上午9:30-11:30实际有交易的分钟数））/121
    morning_df = df[(df['time_obj'].dt.time >= pd.to_datetime('9:30', format='%H:%M').time()) &
                    (df['time_obj'].dt.time <= pd.to_datetime('11:30', format='%H:%M').time())]
    morning_trading_minutes = morning_df['time'].nunique()
    features['停牌比例_上午'] = (121 - morning_trading_minutes) / 121 if 121 != 0 else 0

    # 3. 13:00起首笔成交时间与13:00差值（分钟）
    afternoon_df = df[(df['time_obj'].dt.time >= pd.to_datetime('13:00', format='%H:%M').time())]
    if len(afternoon_df) > 0:
        first_afternoon_time = afternoon_df['time_obj'].iloc[0]
        afternoon_start = pd.to_datetime('13:00', format='%H:%M')
        features['下午首笔成交延迟'] = (first_afternoon_time - afternoon_start).total_seconds() / 60
    else:
        features['下午首笔成交延迟'] = np.nan

    # 4. 首笔成交时间与9:30差值（分钟）
    if len(df) > 0:
        first_trade_time = df['time_obj'].iloc[0]
        market_open = pd.to_datetime('9:30', format='%H:%M')
        features['开盘首笔成交延迟'] = (first_trade_time - market_open).total_seconds() / 60
    else:
        features['开盘首笔成交延迟'] = np.nan

    # 5-6. 早盘和午盘最大缺口（分钟的间隔）
    def find_max_gap(time_series, start_time, end_time):
        """计算指定时间段内的最大交易缺口"""
        if len(time_series) == 0:
            return 0

        # 过滤时间段内的数据
        filtered_times = time_series[(time_series >= start_time) & (time_series <= end_time)]
        if len(filtered_times) <= 1:
            return 0

        # 计算相邻时间点的间隔
        gaps = np.diff(filtered_times)
        return gaps.max() if len(gaps) > 0 else 0

    # 早盘最大缺口（9:30-11:30）
    morning_times = morning_df['minutes_from_start'].values if len(morning_df) > 0 else np.array([])
    features['早盘最大缺口'] = find_max_gap(morning_times, 0, 120)

    # 午盘最大缺口（13:00-15:00）
    afternoon_times = afternoon_df['minutes_from_start'].values if len(afternoon_df) > 0 else np.array([])
    features['午盘最大缺口'] = find_max_gap(afternoon_times, 180, 300)

    # 7. 上午和下午交易分钟数比值
    afternoon_trading_minutes = afternoon_df['time'].nunique()
    features[
        '下午交易分钟数_上午交易分钟数'] = afternoon_trading_minutes / morning_trading_minutes if morning_trading_minutes != 0 else np.nan

    # 8. 最大连续无交易分钟数
    if len(df) > 1:
        # 计算相邻交易时间的间隔
        time_diffs = df['minutes_from_start'].diff().dropna()
        max_no_trade_gap = time_diffs.max() if len(time_diffs) > 0 else 0
        features['最大连续无交易分钟数'] = max_no_trade_gap
    else:
        features['最大连续无交易分钟数'] = 0

    # 9. 交易活跃分钟占比（交易分钟数/理论交易分钟数）
    features['交易活跃分钟占比'] = actual_trading_minutes / 240 if 240 != 0 else 0

    # 10. 早盘交易活跃度（早盘交易分钟数/理论早盘交易分钟数）
    features['早盘交易活跃度'] = morning_trading_minutes / 121 if 121 != 0 else 0

    # 11. 午盘交易活跃度（午盘交易分钟数/理论午盘交易分钟数）
    features['午盘交易活跃度'] = afternoon_trading_minutes / 119 if 119 != 0 else 0

    # 12. 早盘与午盘交易活跃度差异
    features['早盘午盘交易活跃度差异'] = features['早盘交易活跃度'] - features['午盘交易活跃度']

    return features


def cal_suspension_f3(df):
    """计算日内分钟级量价关系特征"""
    features = {}

    # 确保数据按分钟排序（使用正确的时间格式排序）
    df['time_obj'] = pd.to_datetime(df['time'], format='%H:%M')
    df = df.sort_values(by='time_obj')

    # 计算分钟涨跌幅
    df['price_change'] = df['price'].pct_change()
    df.iloc[0, df.columns.get_loc('price_change')] = 0  # 第一笔交易的涨跌幅为0

    # 1. 分钟涨跌幅标准差
    features['分钟涨跌幅标准差'] = df['price_change'].std()

    # 2. 分钟涨跌幅偏度
    features['分钟涨跌幅偏度'] = df['price_change'].skew()

    # 3. 分钟涨跌幅峰度
    features['分钟涨跌幅峰度'] = df['price_change'].kurtosis()

    # 4. √(∑(分钟涨跌幅^2)) - 已实现波动率
    realized_volatility = np.sqrt((df['price_change'] ** 2).sum())
    features['已实现波动率'] = realized_volatility

    # 5. 当日最大分钟涨跌幅
    features['当日最大分钟涨跌幅'] = df['price_change'].max()

    # 6. 当日最小分钟涨跌幅
    features['当日最小分钟涨跌幅'] = df['price_change'].min()

    # 7-8. 当日分钟级涨跌幅持续为正/负的最长分钟间隔及对应成交量占比
    # 过滤掉涨跌幅为0的数据
    df_nonzero = df[df['price_change'] != 0].copy()

    if len(df_nonzero) > 0:
        # 标记涨跌幅符号
        df_nonzero['sign'] = np.sign(df_nonzero['price_change'])

        # 计算连续正/负涨跌幅的最长间隔
        positive_intervals = []
        negative_intervals = []
        current_positive_start = None
        current_negative_start = None

        for idx, row in df_nonzero.iterrows():
            sign = row['sign']
            if sign > 0:  # 正涨跌幅
                if current_positive_start is None:
                    current_positive_start = idx
                if current_negative_start is not None:
                    negative_intervals.append(idx - current_negative_start)
                    current_negative_start = None
            else:  # 负涨跌幅
                if current_negative_start is None:
                    current_negative_start = idx
                if current_positive_start is not None:
                    positive_intervals.append(idx - current_positive_start)
                    current_positive_start = None

        # 处理最后一个区间
        if current_positive_start is not None:
            positive_intervals.append(len(df_nonzero) - current_positive_start)
        if current_negative_start is not None:
            negative_intervals.append(len(df_nonzero) - current_negative_start)

        # 计算最长间隔
        max_positive_interval = max(positive_intervals) if positive_intervals else 0
        max_negative_interval = max(negative_intervals) if negative_intervals else 0

        features['最长正涨跌幅分钟间隔'] = max_positive_interval
        features['最长负涨跌幅分钟间隔'] = max_negative_interval

        # 计算对应成交量占比
        total_volume = df['volume'].sum()
        if total_volume != 0:
            if max_positive_interval > 0:
                # 找到最长正涨跌幅区间对应的成交量
                positive_volume = df_nonzero[df_nonzero['sign'] > 0]['volume'].sum()
                features['最长正涨跌幅分钟间隔对应成交量占比'] = positive_volume / total_volume
            else:
                features['最长正涨跌幅分钟间隔对应成交量占比'] = 0

            if max_negative_interval > 0:
                # 找到最长负涨跌幅区间对应的成交量
                negative_volume = df_nonzero[df_nonzero['sign'] < 0]['volume'].sum()
                features['最长负涨跌幅分钟间隔对应成交量占比'] = negative_volume / total_volume
            else:
                features['最长负涨跌幅分钟间隔对应成交量占比'] = 0
        else:
            features['最长正涨跌幅分钟间隔对应成交量占比'] = 0
            features['最长负涨跌幅分钟间隔对应成交量占比'] = 0
    else:
        features['最长正涨跌幅分钟间隔'] = 0
        features['最长负涨跌幅分钟间隔'] = 0
        features['最长正涨跌幅分钟间隔对应成交量占比'] = 0
        features['最长负涨跌幅分钟间隔对应成交量占比'] = 0

    # 9. 分钟涨跌幅绝对值均值
    features['分钟涨跌幅绝对值均值'] = df['price_change'].abs().mean()

    # 10. 分钟涨跌幅绝对值标准差
    features['分钟涨跌幅绝对值标准差'] = df['price_change'].abs().std()

    # 11. 分钟涨跌幅上下波动不对称比率
    positive_changes = df['price_change'][df['price_change'] > 0]
    negative_changes = df['price_change'][df['price_change'] < 0]
    avg_positive = positive_changes.mean() if len(positive_changes) > 0 else 0
    avg_negative = negative_changes.mean() if len(negative_changes) > 0 else 0
    features['分钟涨跌幅上下波动不对称比率'] = abs(avg_positive / avg_negative) if avg_negative != 0 else np.nan

    # 12. 上下波动切换次数
    # 统计涨跌幅符号切换次数
    sign_changes = 0
    prev_sign = None
    for change in df['price_change']:
        if change != 0:
            current_sign = np.sign(change)
            if prev_sign is not None and current_sign != prev_sign:
                sign_changes += 1
            prev_sign = current_sign
    features['上下波动切换次数'] = sign_changes

    # 13. 尾盘波动放大线索 (14:30-15:00涨跌幅标准差/全天涨跌幅标准差)
    tail_df = df[df['time_obj'].dt.time >= pd.to_datetime('14:30', format='%H:%M').time()]
    if len(tail_df) > 1:
        tail_std = tail_df['price_change'].std()
        all_std = df['price_change'].std()
        features['尾盘波动放大线索'] = tail_std / all_std if all_std != 0 else np.nan
    else:
        features['尾盘波动放大线索'] = np.nan

    # 14. 开盘波动放大线索 (9:30-10:00涨跌幅标准差/全天涨跌幅标准差)
    open_df = df[(df['time_obj'].dt.time >= pd.to_datetime('9:30', format='%H:%M').time()) &
                 (df['time_obj'].dt.time <= pd.to_datetime('10:00', format='%H:%M').time())]
    if len(open_df) > 1:
        open_std = open_df['price_change'].std()
        all_std = df['price_change'].std()
        features['开盘波动放大线索'] = open_std / all_std if all_std != 0 else np.nan
    else:
        features['开盘波动放大线索'] = np.nan

    return features
