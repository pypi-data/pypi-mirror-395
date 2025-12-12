import pandas as pd
import numpy as np

def create_stratification_features(df):
    """
    创建用于分层抽样的特征
    create_stratification_features(df)
    参数:
        df: pandas DataFrame

    返回:
        增加分层特征的DataFrame
    """
    df = df.copy()

    # 流水存在性特征
    if 'total_inflow' in df.columns and 'total_outflow' in df.columns:
        conditions = [
            (df['total_inflow'] == 0) & (df['total_outflow'] == 0),
            (df['total_inflow'] == 0) & (df['total_outflow'] != 0),
            (df['total_inflow'] != 0) & (df['total_outflow'] == 0),
            (df['total_inflow'] != 0) & (df['total_outflow'] != 0)
        ]
        choices = ['0', '1', '2', '3']
        df['bq'] = pd.Series(np.select(conditions, choices, default='3'), index=df.index)

    # 交易日期存在性
    if 'first_transaction_date' in df.columns:
        df['bq2'] = df['first_transaction_date'].apply(
            lambda x: 0 if str(x) == '9999-12-31' else 1
        )

    # 邮编区域特征
    if 'zip_code' in df.columns:
        df['bq3'] = df['zip_code'].astype(str).str[0].apply(
            lambda x: 1 if x == '6' else 0
        )

    # 创建复合分层键
    if 'bq' in df.columns and 'label' in df.columns:
        df['stratify_key'] = df['bq'].astype(str) + '_' + df['label'].astype(str)

    return df