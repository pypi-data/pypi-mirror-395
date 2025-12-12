import pandas as pd

def process_zipcode_features(df, zip_code_col='zip_code'):
    """
    example：
    df_processed=preprocess_dataframe(df_train_1, 
                         zip_code_col='zip_code',
                         categorical_cols=None,
                         time_cols=None,
                         drop_single_value_cols=True)
    df_processed_test=preprocess_dataframe(df_test_1, 
                         zip_code_col='zip_code',
                         categorical_cols=None,
                         time_cols=None,
                         drop_single_value_cols=True)
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