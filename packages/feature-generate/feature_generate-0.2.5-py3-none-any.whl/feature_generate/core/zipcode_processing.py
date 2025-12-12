import pandas as pd

def process_zipcode_features(df, zip_code_col='zip_code'):
    """
    处理邮政编码特征，生成前两位、前四位和完整编码特征

    参数:
        df: pandas DataFrame
        zip_code_col: 邮政编码列名

    返回:
        处理后的DataFrame
    """
    df = df.copy()
    if zip_code_col in df.columns:
        df['zip_code_first_two'] = df[zip_code_col].astype(str).str[:2]
        df['zip_code_first_four'] = df[zip_code_col].astype(str).str[:4]
        df['zip_code_all_six'] = df[zip_code_col].astype(str)
        # 新增衍生特征
        df['zipcode3_6'] = df[zip_code_col].astype(str).str[2:6]
        df['zipcode13_6'] = df[zip_code_col].astype(str).str[0] + df[zip_code_col].astype(str).str[2:6]
        df['zipcode1'] = df[zip_code_col].astype(str).str[0]
    return df