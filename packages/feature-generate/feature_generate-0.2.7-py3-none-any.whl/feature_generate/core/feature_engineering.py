
import pandas as pd
import numpy as np
def add_time_numeric_features(df):
    time_cols = ['issue_time', 'record_time', 'history_time']
    for col in time_cols:
        if col in df.columns:
            dt_series = pd.to_datetime(df[col], errors='coerce')
            # 已有 numeric（秒级时间戳）
            df[f'{col}_numeric'] = dt_series.astype('int64') // 10**9
            # 已有 year_month
            df[f'{col}_year_month_numeric'] = dt_series.dt.year * 100 + dt_series.dt.month
            # 🔥 新增：_time → HHMM 格式（如 1430 表示 14:30）
            df[f'{col}_time'] = dt_series.dt.hour * 100 + dt_series.dt.minute  # 注意：这里叫 _time，不是 _time_numeric
    
    # 交易日期
    for date_col in ['first_transaction_date', 'last_transaction_date']:
        if date_col in df.columns:
            dt_series = pd.to_datetime(df[date_col], errors='coerce')
            df[f'{date_col}_numeric'] = dt_series.astype('int64') // 10**9
    
    return df
def add_ratio_features(df):
    """添加比率特征"""
    ratios = [
        ('balance', 'balance_limit', 'utilization_rate'),
        ('loan', 'balance_limit', 'loan_ratio'),
        ('total_accounts', 'balance_accounts', 'account_ratio'),
        ('duration_days', 'term', 'duration_ratio'),
    ]
    for num, den, name in ratios:
        if num in df.columns and den in df.columns:
            # 强制转换为数值类型，避免 Categorical 错误
            num_series = pd.to_numeric(df[num], errors='coerce')
            den_series = pd.to_numeric(df[den], errors='coerce')
            df[name] = num_series / (den_series + 1e-5)
   
   # 近似月供
    if 'loan' in df.columns and 'term' in df.columns:
        loan_num = pd.to_numeric(df['loan'], errors='coerce')
        term_num = pd.to_numeric(df['term'], errors='coerce')
        df['approx_monthly_payment'] = loan_num / (term_num + 1e-5)

    # 余额比率
    if 'balance' in df.columns and 'balance_limit' in df.columns:
        balance_num = pd.to_numeric(df['balance'], errors='coerce')
        limit_num = pd.to_numeric(df['balance_limit'], errors='coerce')
        df['balance_ratio'] = balance_num / (limit_num + 1e-5)
        return df

def add_custom_encodings(df):
    """添加自定义编码"""
    if 'level' in df.columns:
        df['level_char'] = df['level'].astype(str).str[0]
        df['level_numeric'] = df['level_char'].map({'A':1,'B':2,'C':3,'D':4,'E':5}).fillna(0)
    
    # 在 add_custom_encodings 或 process_categorical_features 中
    if 'level' in df.columns:
        level_map = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5}
        df['level_num'] = df['level'].map(level_map).fillna(0)
    return df