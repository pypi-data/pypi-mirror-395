import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_transaction_features(df):
    """
    create_transaction_features(df
    df_train_2['time'] = df_train_2['time'].apply(lambda v: datetime.fromtimestamp(v) if v != None and len(str(v)) == 10 else None)
   train_transaction_features = create_transaction_features(df_train_2)
   df_test_2['time'] = df_test_2['time'].apply(lambda v: datetime.fromtimestamp(v) if v != None and len(str(v)) == 10 else None)
    train_transaction_features_test = create_transaction_features(df_test_2)
  result=calculate_transaction_features(df_train_2, id_col='id', time_col='time', 
                                  amount_col='amount', direction_col='direction')
   result_test=calculate_transaction_features(df_test_2, id_col='id', time_col='time', 
                                  amount_col='amount', direction_col='direction')

    """
    df = df.copy()
    # 确保时间戳正确
    df['time'] = pd.to_datetime(df['time'], unit='s',errors='coerce')
    print('=============looking time create_transaction_features===========')
    print(df['time'].head(5))

    # 按客户分组
    grouped = df.groupby('id')
    features = pd.DataFrame(index=df['id'].unique())
    features.index.name = 'id'

    # 1. 基本统计
    features['total_transactions'] = grouped.size()
    features['inflow_count'] = grouped['direction'].apply(lambda x: (x == 1).sum())
    features['outflow_count'] = grouped['direction'].apply(lambda x: (x == 0).sum())
    features['inflow_outflow_ratio'] = features['inflow_count'] / (features['outflow_count'] + 1e-5)

    # 2. 金额统计
    inflow_df = df[df['direction'] == 1]
    outflow_df = df[df['direction'] == 0]

    features['total_inflow_amount'] = inflow_df.groupby('id')['amount'].sum()
    features['total_outflow_amount'] = outflow_df.groupby('id')['amount'].sum()
    features['net_cash_flow'] = features['total_inflow_amount'] - features['total_outflow_amount']
    features['inflow_outflow_amount_ratio'] = features['total_inflow_amount'] / (features['total_outflow_amount'] + 1e-5)

    # 3. 金额分布
    amount_stats = grouped['amount'].agg(['mean', 'std', 'min', 'max', 'median'])
    amount_stats.columns = ['amount_mean', 'amount_std', 'amount_min', 'amount_max', 'amount_median']
    features = features.join(amount_stats)

    # 4. 时间特征
    current_time = df['time'].max()
    features['transaction_time_span_days'] = grouped['time'].apply(lambda x: (x.max() - x.min()).days)
    features['daily_avg_transactions'] = features['total_transactions'] / (features['transaction_time_span_days'] + 1e-5)
    features['days_since_last_transaction'] = grouped['time'].apply(lambda x: (current_time - x.max()).days)
    features['days_since_first_transaction'] = grouped['time'].apply(lambda x: (current_time - x.min()).days)

    # 5. 连续交易模式
    def max_consecutive(directions, target_val):
        max_count = 0
        current_count = 0
        for d in directions:
            if d == target_val:
                current_count += 1
                max_count = max(max_count, current_count)
            else:
                current_count = 0
        return max_count

    features['max_consecutive_inflow'] = grouped['direction'].apply(lambda x: max_consecutive(x, 1))
    features['max_consecutive_outflow'] = grouped['direction'].apply(lambda x: max_consecutive(x, 0))

    # 6. 周期性特征
    df['day_of_week'] = df['time'].dt.dayofweek
    print('==================')
    print(df['day_of_week'].head(5))
    print(df['time'].head(5))
    weekly_counts = df.groupby(['id', 'day_of_week']).size().unstack(fill_value=0)
    print(f'looking====length of weekly_counts:{weekly_counts.shape}')
    print(f'looking====columns of weekly_counts:{weekly_counts.columns}')
    weekly_counts.columns = ['monday_count', 'tuesday_count', 'wednesday_count',
                             'thursday_count', 'friday_count', 'saturday_count', 'sunday_count']
    features = features.join(weekly_counts)

    features['weekend_transaction_ratio'] = (features['saturday_count'] + features['sunday_count']) / (features['total_transactions'] + 1e-5)
    features['weekday_transaction_ratio'] = 1 - features['weekend_transaction_ratio']

    # 7. 近期交易特征
    recent_cutoff = current_time - pd.Timedelta(days=30)
    recent_df = df[df['time'] >= recent_cutoff]
    recent_grouped = recent_df.groupby('id')

    features['recent_30d_transactions'] = recent_grouped.size()
    features['recent_30d_inflow_count'] = recent_grouped['direction'].apply(lambda x: (x == 1).sum())
    features['recent_30d_outflow_count'] = recent_grouped['direction'].apply(lambda x: (x == 0).sum())
    features['recent_30d_net_cash_flow'] = recent_grouped.apply(
        lambda x: x[x['direction'] == 1]['amount'].sum() - x[x['direction'] == 0]['amount'].sum()
    )

    # 填充缺失值
    features.fillna({
        'recent_30d_transactions': 0,
        'recent_30d_inflow_count': 0,
        'recent_30d_outflow_count': 0,
        'recent_30d_net_cash_flow': 0
    }, inplace=True)

    return features.reset_index()

def calculate_transaction_stats(df):
    """
    计算高级交易统计特征

    参数:
        df: 交易流水DataFrame

    返回:
        高级交易特征DataFrame
    """
    df = df.copy()
    # 转换时间列
    try:
        df['date'] = pd.to_datetime(df['time'], unit='s').dt.date
    except:
        df['date'] = pd.to_datetime(df['time'], errors='coerce').dt.date

    # 过滤无效日期
    df = df[df['date'].notna()]
    if df.empty:
        return pd.DataFrame()

    # 提取日期组件
    df['year'] = pd.to_datetime(df['date']).dt.year
    df['month'] = pd.to_datetime(df['date']).dt.month
    df['day'] = pd.to_datetime(df['date']).dt.day

    # 确定交易方向
    df['inflow'] = df['amount'].where(df['direction'] == 0, 0)
    df['outflow'] = df['amount'].where(df['direction'] == 1, 0)

    # 按ID分组
    grouped = df.groupby('id')
    result = pd.DataFrame()

    current_time = df['date'].max()

    for id_val, group in grouped:
        # 基础统计
        total_inflow = group['inflow'].sum()
        total_outflow = group['outflow'].sum()
        net_flow = total_inflow - total_outflow
        total_transactions = len(group)

        # 日期范围
        min_date = group['date'].min()
        max_date = group['date'].max()
        duration_days = (max_date - min_date).days if min_date != max_date else 1

        # 按时间粒度聚合
        daily_stats = group.groupby('date').agg({'inflow': 'sum', 'outflow': 'sum'})
        monthly_stats = group.groupby(['year', 'month']).agg({'inflow': 'sum', 'outflow': 'sum'})
        yearly_stats = group.groupby('year').agg({'inflow': 'sum', 'outflow': 'sum'})

        # 构建特征行
        row = {
            'id': id_val,
            'total_inflow': total_inflow,
            'total_outflow': total_outflow,
            'net_flow': net_flow,
            'total_transactions': total_transactions,
            'first_transaction_date': min_date,
            'last_transaction_date': max_date,
            'duration_days': duration_days,
            'avg_daily_inflow': daily_stats['inflow'].mean() if not daily_stats.empty else 0,
            'avg_daily_outflow': daily_stats['outflow'].mean() if not daily_stats.empty else 0,
            # ... [其他特征保持与原始代码一致]
        }

        # 添加到结果
        result = pd.concat([result, pd.DataFrame([row])], ignore_index=True)

    # 处理异常值
    result = result.replace([np.inf, -np.inf], 0).fillna(0)

    if not result.empty and 'id' in result.columns:
        result.set_index('id', inplace=True)

    return result