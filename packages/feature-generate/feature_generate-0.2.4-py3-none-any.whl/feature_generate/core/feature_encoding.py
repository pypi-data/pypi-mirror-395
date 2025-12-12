def add_str_columns(df, columns_to_convert):
    """将指定列转换为字符串类型，并添加 '_str' 后缀的新列"""
    import pandas as pd
    df_new = df.copy()
    
    for col in columns_to_convert:
        if col not in df_new.columns:
            print(f"警告：列 '{col}' 不存在于DataFrame中，已跳过。")
            continue
        new_col_name = f"{col}_str"
        df_new[new_col_name] = df_new[col].astype(str)
        print(f"成功创建新列 '{new_col_name}'")
    
    return df_new