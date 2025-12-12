import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def process_time_features(df, time_cols=None):
    """
    处理时间特征，将Unix时间戳转换为datetime对象并提取时间组件

    参数:
        df: pandas DataFrame
        time_cols: 时间列名列表

    返回:
        处理后的DataFrame
    """
    df = df.copy()
    if time_cols is None:
        time_cols = ['issue_time', 'record_time', 'history_time']

    existing_time_cols = [col for col in time_cols if col in df.columns]

    for col in existing_time_cols:
        # 转换时间戳
        df[col] = pd.to_datetime(df[col], unit='s', errors='coerce')

        # 提取时间组件
        df[f'{col}_year'] = df[col].dt.year
        df[f'{col}_month'] = df[col].dt.month
        df[f'{col}_year_month'] = df[col].dt.strftime('%Y-%m')
        df[f'{col}_time'] = df[col].dt.time

    # 将 time 对象列转换为秒数（用于后续 create_dual_features）
    time_cols_to_seconds = ['issue_time_time', 'record_time_time', 'history_time_time']
    for col in time_cols_to_seconds:
        if col in df.columns:
            try:
                df[col] = pd.to_timedelta(df[col]).dt.total_seconds().fillna(0).astype(int)
            except Exception as e:
                print(f"Warning: Failed to convert {col} to seconds: {e}")
                df[col] = 0
    return df

def calculate_time_deltas(df):
    """
    计算关键时间差特征

    参数:
        df: pandas DataFrame

    返回:
        增加时间差特征的DataFrame
    """
    df = df.copy()

    # 确保时间列为datetime类型
    for col in ['issue_time', 'record_time', 'history_time']:
        if col in df.columns and not pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # 计算处理时长(秒)
    if 'record_time' in df.columns and 'issue_time' in df.columns:
        process_duration = df['record_time'] - df['issue_time']
        df['process_duration_seconds'] = process_duration.dt.total_seconds()
        df['process_duration_days'] = process_duration.dt.days

    # 计算用户历史时长(秒)
    if 'issue_time' in df.columns and 'history_time' in df.columns:
        user_history_duration = df['issue_time'] - df['history_time']
        df['user_history_duration_seconds'] = user_history_duration.dt.total_seconds()
        df['user_history_duration_days'] = user_history_duration.dt.days

    return df