import pandas as pd
import numpy as np
import os

def remove_duplicate_columns(df):
    """
    去除DataFrame中完全相同的列，保留第一次出现的列
   emove_duplicate_columns(df)
   查找包含NaN值的列并返回统计信息
   find_nan_columns(df)

    """
    columns_to_keep = []
    seen_hashes = set()

    for col in df.columns:
        # col_hash = hash(tuple(df[col].apply(lambda v: pd.to_numeric(v, errors='coerce')).fillna(0)))
        col_hash = hash(tuple(pd.to_numeric(df[col], errors='coerce').fillna(0)))
        if col_hash not in seen_hashes:
            columns_to_keep.append(col)
            seen_hashes.add(col_hash)

    return df[columns_to_keep]

def find_nan_columns(df):
    """
    查找包含NaN值的列并返回统计信息

    参数:
        df: pandas DataFrame

    返回:
        DataFrame包含缺失值统计
    """
    nan_counts = df.isnull().sum()
    nan_ratios = df.isnull().mean()

    nan_columns = pd.DataFrame({
        'column': nan_counts.index,
        'missing_count': nan_counts.values,
        'missing_ratio': nan_ratios.values
    })

    return nan_columns[nan_columns['missing_count'] > 0].sort_values(
        'missing_ratio', ascending=False
    ).reset_index(drop=True)

def load_data(train_path, test_path):
    """
    加载训练和测试数据

    参数:
        train_path: 训练数据路径
        test_path: 测试数据路径

    返回:
        训练和测试DataFrame
    """
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)
    return train_df, test_df

def save_submission(ids, predictions, output_dir, auc_score):
    """
    保存预测结果为提交文件

    参数:
        ids: 样本ID列表
        predictions: 预测概率
        output_dir: 输出目录
        auc_score: 模型AUC分数

    返回:
        保存的文件路径
    """
    os.makedirs(output_dir, exist_ok=True)
    submission = pd.DataFrame({
        'id': ids,
        'label': predictions
    })

    filename = f'submission_auc_{auc_score:.6f}.csv'
    filepath = os.path.join(output_dir, filename)
    submission.to_csv(filepath, index=False)
    return filepath