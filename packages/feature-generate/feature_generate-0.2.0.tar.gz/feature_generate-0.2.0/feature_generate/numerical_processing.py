import pandas as pd
import numpy as np

def process_numerical_features(df):
    """
    example:
    process_numerical_features(df)
    
    """
    df = df.copy()

    # 查找含NaN的列
    nan_counts = df.isnull().sum()
    nan_columns = nan_counts[nan_counts > 0].index.tolist()

    # 填充数值列
    for col in nan_columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(0)

    return df

def create_financial_ratios(df):
    """
    创建金融相关比率特征

    参数:
        df: pandas DataFrame

    返回:
        增加金融特征的DataFrame
    """
    df = df.copy()

    # 额度使用率
    if 'balance' in df.columns and 'balance_limit' in df.columns:
        df['utilization_rate'] = df['balance'] / (df['balance_limit'] + 1e-6)
        df['utilization_rate'] = df['utilization_rate'].replace([np.inf, -np.inf], 1000)

    # 账户比率
    if 'balance' in df.columns and 'total_accounts' in df.columns:
        df['account_ratio'] = df['balance'] / (df['total_accounts'] + 1e-6)
        df['account_ratio'] = df['account_ratio'].replace([np.inf, -np.inf], 0)

    if 'balance' in df.columns and 'balance_accounts' in df.columns:
        df['account_ratio2'] = df['balance'] / (df['balance_accounts'] + 1e-6)
        df['account_ratio2'] = df['account_ratio2'].replace([np.inf, -np.inf], 0)

    if 'balance_limit' in df.columns and 'total_accounts' in df.columns:
        df['account_ratio3'] = df['balance_limit'] / (df['total_accounts'] + 1e-6)
        df['account_ratio3'] = df['account_ratio3'].replace([np.inf, -np.inf], 0)

    if 'balance_limit' in df.columns and 'balance_accounts' in df.columns:
        df['account_ratio4'] = df['balance_limit'] / (df['balance_accounts'] + 1e-6)
        df['account_ratio4'] = df['account_ratio4'].replace([np.inf, -np.inf], 0)

    # 贷款相关比率
    if 'loan' in df.columns and 'balance_limit' in df.columns:
        df['loan_ratio'] = df['loan'] / (df['balance_limit'] + 1e-6)
        df['loan_ratio'] = df['loan_ratio'].replace([np.inf, -np.inf], 0)

    if 'loan' in df.columns and 'balance' in df.columns:
        df['loan_ratio2'] = df['loan'] / (df['balance'] + 1e-6)
        df['loan_ratio2'] = df['loan_ratio2'].replace([np.inf, -np.inf], 0)

    # 利率相关特征
    if 'interest_rate' in df.columns:
        df['interest_rate_2'] = df['interest_rate'] * 2
        df['interest_rate_cat'] = df['interest_rate'].astype(str)

    # 余额与限额差
    if 'balance_limit' in df.columns and 'balance' in df.columns:
        df['limit_balance'] = df['balance_limit'] - df['balance']

    # 余额与利率乘积
    if 'balance' in df.columns and 'interest_rate' in df.columns:
        df['bal_int'] = df['balance'] * df['interest_rate']

    if 'balance_limit' in df.columns and 'interest_rate' in df.columns:
        df['limit_int'] = df['balance_limit'] * df['interest_rate']

    # 贷款与利率乘积
    if 'loan' in df.columns and 'interest_rate' in df.columns:
        df['loan_interest_rate'] = df['loan'] * df['interest_rate']

    # 期限相关特征
    if 'loan' in df.columns and 'term' in df.columns:
        df['approx_monthly_payment'] = df['loan'] / (df['term'] + 1e-6)

    # 时长比率
    if 'loan' in df.columns and 'process_duration_days' in df.columns:
        df['duration_ratio'] = df['loan'] / (df['process_duration_days'] + 1e-6)

    if 'loan' in df.columns and 'user_history_duration_days' in df.columns:
        df['duration_ratio2'] = df['loan'] / (df['user_history_duration_days'] + 1e-6)

    # 余额比率
    if 'balance' in df.columns and 'balance_limit' in df.columns:
        df['balance_ratio'] = df['balance'] / (df['balance_limit'] + 1e-6)
        df['balance_ratio'] = df['balance_ratio'].replace([np.inf, -np.inf], 1000)

    return df