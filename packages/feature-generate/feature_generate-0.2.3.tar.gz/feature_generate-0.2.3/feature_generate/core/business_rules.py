def add_business_flag_features(df):
    """添加业务规则标志特征：bq, bq2, bq3"""
    import pandas as pd
    df = df.copy()
    
    # bq: 流水模式分类
    df['bq'] = '0'
    df.loc[(df['total_inflow'] == 0) & (df['total_outflow'] != 0), 'bq'] = '1'
    df.loc[(df['total_inflow'] != 0) & (df['total_outflow'] == 0), 'bq'] = '2'
    df.loc[(df['total_inflow'] != 0) & (df['total_outflow'] != 0), 'bq'] = '3'
    
    # bq2: 是否无交易记录（first_transaction_date == '9999-12-31'）
    df['bq2'] = df['first_transaction_date'].apply(
        lambda x: 0 if str(x) == '9999-12-31' else 1
    )
    
    # bq3: 邮编首位是否为 '6'
    df['bq3'] = df['zip_code'].astype(str).str[0].apply(
        lambda x: 1 if x == '6' else 0
    )
    
    return df