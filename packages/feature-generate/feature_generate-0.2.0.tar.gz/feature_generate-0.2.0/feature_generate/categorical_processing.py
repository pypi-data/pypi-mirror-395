import pandas as pd
import numpy as np

def process_categorical_features(df, categorical_cols=None):
    """
    example:
   df_train=create_dual_features(df_train, numeric_to_cat_cols=num_to_cat, cat_to_numeric_cols=cat_to_num)
   df_test=create_dual_features(df_test, numeric_to_cat_cols=num_to_cat, cat_to_numeric_cols=cat_to_num)
    """
    df = df.copy()

    if categorical_cols is None:
        categorical_cols = ['title', 'residence', 'career', 'term',
                           'syndicated', 'installment', 'level']

    existing_cols = [col for col in categorical_cols if col in df.columns]

    for col in existing_cols:
        # 填充缺失值
        df[col] = df[col].fillna('special_value')
        # 转换为category类型
        df[col] = df[col].astype('category')

    return df

def create_dual_features(df, numeric_to_cat_cols=None, cat_to_numeric_cols=None):
    """
    为指定列创建数值和分类两个版本的特征

    参数:
        df: pandas DataFrame
        numeric_to_cat_cols: 需要从数值转换为分类的列名列表
        cat_to_numeric_cols: 需要从分类转换为数值的列名列表

    返回:
        增加双重特征的DataFrame
    """
    df = df.copy()

    # 数值转分类
    if numeric_to_cat_cols:
        for col in numeric_to_cat_cols:
            if col in df.columns:
                new_col_name = f"{col}_category"
                df[new_col_name] = df[col].astype(str)

    # 分类转数值
    if cat_to_numeric_cols:
        for col in cat_to_numeric_cols:
            if col in df.columns:
                new_col_name = f"{col}_numeric"
                if pd.api.types.is_numeric_dtype(df[col]):
                    df[new_col_name] = df[col]
                else:
                    df[new_col_name] = pd.to_numeric(df[col], errors='coerce')

    return df