import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore') 
def create_transaction_features(df):
    """
    example:
    train_transaction_features_test = create_transaction_features(df_test_2)
    """
    
    # 确保时间戳为datetime类型
    df['time'] = pd.to_datetime(df['time'],unit='s')
    
    # 按客户id分组
    grouped = df.groupby('id')
    
    # 初始化特征 DataFrame
    features = pd.DataFrame(index=df['id'].unique())
    features.index.name = 'id'
    
    # 1. 基本统计特征
    # 总交易次数
    features['total_transactions'] = grouped.size()
    
    # 进账次数和出账次数
    features['inflow_count'] = grouped['direction'].apply(lambda x: (x == 1).sum())
    features['outflow_count'] = grouped['direction'].apply(lambda x: (x == 0).sum())
    
    # 进账出账比例
    features['inflow_outflow_ratio'] = features['inflow_count'] / (features['outflow_count'] + 1e-5)
    
    # 进出账金额统计
    inflow_df = df[df['direction'] == 1]
    outflow_df = df[df['direction'] == 0]
    
    inflow_amount = inflow_df.groupby('id')['amount'].sum()
    outflow_amount = outflow_df.groupby('id')['amount'].sum()
    
    features['total_inflow_amount'] = inflow_amount
    features['total_outflow_amount'] = outflow_amount
    features['net_cash_flow'] = features['total_inflow_amount'] - features['total_outflow_amount']
    features['inflow_outflow_amount_ratio'] = features['total_inflow_amount'] / (features['total_outflow_amount'] + 1e-5)
    
    # 2. 金额统计特征
    amount_stats = grouped['amount'].agg(['mean', 'std', 'min', 'max', 'median'])
    amount_stats.columns = ['amount_mean', 'amount_std', 'amount_min', 'amount_max', 'amount_median']
    features = features.join(amount_stats)
    
    # 金额变异系数（标准差/均值）
    features['amount_coefficient_of_variation'] = features['amount_std'] / (features['amount_mean'] + 1e-5)
    
    # 进出账分别的金额统计
    inflow_amount_stats = inflow_df.groupby('id')['amount'].agg(['mean', 'std', 'max'])
    inflow_amount_stats.columns = ['inflow_amount_mean', 'inflow_amount_std', 'inflow_amount_max']
    features = features.join(inflow_amount_stats)
    
    outflow_amount_stats = outflow_df.groupby('id')['amount'].agg(['mean', 'std', 'max'])
    outflow_amount_stats.columns = ['outflow_amount_mean', 'outflow_amount_std', 'outflow_amount_max']
    features = features.join(outflow_amount_stats)
    
    # 3. 时间相关特征
    # 交易时间跨度（天）
    features['transaction_time_span_days'] = grouped['time'].apply(lambda x: (x.max() - x.min()).days)
    
    # 日均交易次数
    features['daily_avg_transactions'] = features['total_transactions'] / (features['transaction_time_span_days'] + 1e-5)
    
    # 最近一次交易距今的时间
    current_time = df['time'].max()
    features['days_since_last_transaction'] = grouped['time'].apply(lambda x: (current_time - x.max()).days)
    
    # 第一次交易距今的时间
    features['days_since_first_transaction'] = grouped['time'].apply(lambda x: (current_time - x.min()).days)
    
    # 4. 进出账模式特征
    # 最大连续进账次数
    def max_consecutive_inflow(directions):
        max_count = 0
        current_count = 0
        for d in directions:
            if d == 1:  # 进账
                current_count += 1
                max_count = max(max_count, current_count)
            else:
                current_count = 0
        return max_count
    
    features['max_consecutive_inflow'] = grouped['direction'].apply(max_consecutive_inflow)
    
    # 最大连续出账次数
    def max_consecutive_outflow(directions):
        max_count = 0
        current_count = 0
        for d in directions:
            if d == 0:  # 出账
                current_count += 1
                max_count = max(max_count, current_count)
            else:
                current_count = 0
        return max_count
    
    features['max_consecutive_outflow'] = grouped['direction'].apply(max_consecutive_outflow)
    
    # 5. 交易金额的偏度和峰度
    features['amount_skewness'] = grouped['amount'].apply(lambda x: x.skew())
    features['amount_kurtosis'] = grouped['amount'].apply(lambda x: x.kurtosis())
    
    # 6. 交易周期性特征
    # 提取星期几的信息
    df['day_of_week'] = df['time'].dt.dayofweek
    weekly_counts = df.groupby(['id', 'day_of_week']).size().unstack(fill_value=0)
    weekly_counts.columns = [
        'monday_count', 'tuesday_count', 'wednesday_count', 
        'thursday_count', 'friday_count', 'saturday_count', 'sunday_count'
    ]
    features = features.join(weekly_counts)
    
    # 周末交易比例
    features['weekend_transaction_ratio'] = (features['saturday_count'] + features['sunday_count']) / (features['total_transactions'] + 1e-5)
    
    # 工作日交易比例
    features['weekday_transaction_ratio'] = 1 - features['weekend_transaction_ratio']
    
    # 7. 时间窗口特征（最近30天）
    recent_cutoff = current_time - pd.Timedelta(days=30)
    recent_df = df[df['time'] >= recent_cutoff]
    recent_grouped = recent_df.groupby('id')
    
    features['recent_30d_transactions'] = recent_grouped.size()
    features['recent_30d_inflow_count'] = recent_grouped['direction'].apply(lambda x: (x == 1).sum())
    features['recent_30d_outflow_count'] = recent_grouped['direction'].apply(lambda x: (x == 0).sum())
    features['recent_30d_net_cash_flow'] = recent_grouped.apply(lambda x: x[x['direction'] == 1]['amount'].sum() - 
                                                              x[x['direction'] == 0]['amount'].sum())
    
    # 填充缺失值（对于最近30天无交易的客户）
    features.fillna({
        'recent_30d_transactions': 0,
        'recent_30d_inflow_count': 0,
        'recent_30d_outflow_count': 0,
        'recent_30d_net_cash_flow': 0
    }, inplace=True)
    
    return features