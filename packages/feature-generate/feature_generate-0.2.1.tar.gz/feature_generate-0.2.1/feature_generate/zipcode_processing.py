def preprocess_dataframe(df, 
                         zip_code_col='zip_code',
                         categorical_cols=None,
                         time_cols=None,
                         drop_single_value_cols=True):
    """
   example:
   df_processed=preprocess_dataframe(df_train_1, 
                         zip_code_col='zip_code',
                         categorical_cols=None,
                         time_cols=None,
                         drop_single_value_cols=True)
    """
    df_processed = df.copy()
    

    if zip_code_col in df_processed.columns:
        df_processed['zip_code_first_two'] = df_processed[zip_code_col].astype(str).str[:2]
        df_processed['zip_code_first_four'] = df_processed[zip_code_col].astype(str).str[:4]
        df_processed['zip_code_all_six'] = df_processed[zip_code_col].astype(str)
    
    
    if categorical_cols is None:
        categorical_cols = ['title', 'residence', 'career', 'term', 'syndicated', 'installment', 'level']
    
    existing_categorical_cols = [col for col in categorical_cols if col in df_processed.columns]
    for col in existing_categorical_cols:
        df_processed[col] = df_processed[col].fillna('special_value').astype('category')
   
    
    if drop_single_value_cols:
        cols_to_drop = []
        for col in df_processed.columns:
            if df_processed[col].nunique() == 1:
                cols_to_drop.append(col)
        
        if cols_to_drop:
            print(f"删除只有一个唯一值的列: {cols_to_drop}")
            df_processed = df_processed.drop(cols_to_drop, axis=1)
    
    
    if time_cols is None:
        time_cols = ['issue_time', 'record_time', 'history_time']
    existing_time_cols = [col for col in time_cols if col in df_processed.columns]
    
    for col in existing_time_cols:
        df_processed[col] = pd.to_datetime(df_processed[col], unit='s')
        df_processed[col + '_year'] = df_processed[col].dt.year
        df_processed[col + '_year_month'] = df_processed[col].dt.strftime('%Y-%m')
        df_processed[col + '_month'] = df_processed[col].dt.month
        df_processed[col + '_time'] = df_processed[col].dt.time
    
    return df_processed