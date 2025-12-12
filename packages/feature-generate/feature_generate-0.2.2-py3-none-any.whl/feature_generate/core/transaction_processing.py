import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_transaction_features(df):
    """
    从交易流水数据中提取基础特征

    参数:
        df: 交易流水DataFrame，包含['id', 'time', 'direction', 'amount']列

    返回:
        交易特征DataFrame
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
    """计算高级交易统计特征（完整版，对齐 jupyter 代码）
    参数:
        df: 交易流水DataFrame，包含 ['id', 'time', 'direction', 'amount']
    返回:
        高级交易特征DataFrame，index='id'
    """
    import pandas as pd
    import numpy as np
    from datetime import timedelta
    
    df = df.copy()
    
    # 转换时间列
    try:
        df['date'] = pd.to_datetime(df['time'], unit='s').dt.date
    except Exception as e:
        print(f"日期转换错误: {e}")
        df['date'] = pd.to_datetime(df['time'], errors='coerce').dt.date
    
    # 过滤无效日期
    df = df[df['date'].notna()]
    if df.empty:
        return pd.DataFrame()

    # 提取年月日
    df['year'] = pd.to_datetime(df['date']).dt.year
    df['month'] = pd.to_datetime(df['date']).dt.month
    df['day'] = pd.to_datetime(df['date']).dt.day

    # 确定交易方向（注意：jupyter 中 direction=0 是 inflow，1 是 outflow）
    df['inflow'] = df['amount'].where(df['direction'] == 0, 0)
    df['outflow'] = df['amount'].where(df['direction'] == 1, 0)

    grouped = df.groupby('id')
    result = pd.DataFrame()
    current_time = df['date'].max()

    for id_val, group in grouped:
        total_inflow = group['inflow'].sum()
        total_outflow = group['outflow'].sum()
        net_flow = total_inflow - total_outflow
        total_transactions = len(group)

        valid_dates = group['date'].dropna()
        if valid_dates.empty:
            continue
        min_date = valid_dates.min()
        max_date = valid_dates.max()
        duration_days = (max_date - min_date).days if min_date != max_date else 1

        # 按日/月/年聚合
        daily_stats = group.groupby('date').agg({'inflow': 'sum', 'outflow': 'sum'}).reset_index()
        monthly_stats = group.groupby(['year', 'month']).agg({'inflow': 'sum', 'outflow': 'sum'}).reset_index()
        yearly_stats = group.groupby('year').agg({'inflow': 'sum', 'outflow': 'sum'}).reset_index()

        # 构建完整特征行
        row = {
            'id': id_val,
            'total_inflow': total_inflow,
            'total_outflow': total_outflow,
            'net_flow': net_flow,
            'total_transactions': total_transactions,
            'first_transaction_date': min_date,
            'last_transaction_date': max_date,
            'duration_days': duration_days,
            
            # 日级别统计
            'avg_daily_inflow': daily_stats['inflow'].mean() if not daily_stats.empty else 0,
            'avg_daily_outflow': daily_stats['outflow'].mean() if not daily_stats.empty else 0,
            'max_daily_inflow': daily_stats['inflow'].max() if not daily_stats.empty else 0,
            'max_daily_outflow': daily_stats['outflow'].max() if not daily_stats.empty else 0,
            'min_daily_inflow': daily_stats['inflow'].min() if not daily_stats.empty else 0,
            'min_daily_outflow': daily_stats['outflow'].min() if not daily_stats.empty else 0,
            'std_daily_inflow': daily_stats['inflow'].std() if not daily_stats.empty and len(daily_stats) > 1 else 0,
            'std_daily_outflow': daily_stats['outflow'].std() if not daily_stats.empty and len(daily_stats) > 1 else 0,

            # 月级别统计
            'avg_monthly_inflow': monthly_stats['inflow'].mean() if not monthly_stats.empty else 0,
            'avg_monthly_outflow': monthly_stats['outflow'].mean() if not monthly_stats.empty else 0,
            'max_monthly_inflow': monthly_stats['inflow'].max() if not monthly_stats.empty else 0,
            'max_monthly_outflow': monthly_stats['outflow'].max() if not monthly_stats.empty else 0,
            'min_monthly_inflow': monthly_stats['inflow'].min() if not monthly_stats.empty else 0,
            'min_monthly_outflow': monthly_stats['outflow'].min() if not monthly_stats.empty else 0,
            'std_monthly_inflow': monthly_stats['inflow'].std() if not monthly_stats.empty and len(monthly_stats) > 1 else 0,
            'std_monthly_outflow': monthly_stats['outflow'].std() if not monthly_stats.empty and len(monthly_stats) > 1 else 0,

            # 年级别统计
            'avg_yearly_inflow': yearly_stats['inflow'].mean() if not yearly_stats.empty else 0,
            'avg_yearly_outflow': yearly_stats['outflow'].mean() if not yearly_stats.empty else 0,
            'max_yearly_inflow': yearly_stats['inflow'].max() if not yearly_stats.empty else 0,
            'max_yearly_outflow': yearly_stats['outflow'].max() if not yearly_stats.empty else 0,
            'min_yearly_inflow': yearly_stats['inflow'].min() if not yearly_stats.empty else 0,
            'min_yearly_outflow': yearly_stats['outflow'].min() if not yearly_stats.empty else 0,
            'std_yearly_inflow': yearly_stats['inflow'].std() if not yearly_stats.empty and len(yearly_stats) > 1 else 0,
            'std_yearly_outflow': yearly_stats['outflow'].std() if not yearly_stats.empty and len(yearly_stats) > 1 else 0,

            # 比率
            'inflow_outflow_ratio': total_inflow / total_outflow if total_outflow > 0 else 0,
            'outflow_inflow_ratio': total_outflow / total_inflow if total_inflow > 0 else 0,
        }

        # 最近3个月统计
        try:
            three_months_ago = max_date - timedelta(days=90)
            recent_data = group[group['date'] >= three_months_ago]
            if len(recent_data) > 0:
                row.update({
                    'recent_3m_inflow': recent_data['inflow'].sum(),
                    'recent_3m_outflow': recent_data['outflow'].sum(),
                    'recent_3m_net_flow': recent_data['inflow'].sum() - recent_data['outflow'].sum(),
                    'recent_3m_avg_inflow': recent_data['inflow'].mean(),
                    'recent_3m_avg_outflow': recent_data['outflow'].mean(),
                })
            else:
                row.update({
                    'recent_3m_inflow': 0,
                    'recent_3m_outflow': 0,
                    'recent_3m_net_flow': 0,
                    'recent_3m_avg_inflow': 0,
                    'recent_3m_avg_outflow': 0,
                })
        except Exception as e:
            row.update({
                'recent_3m_inflow': 0,
                'recent_3m_outflow': 0,
                'recent_3m_net_flow': 0,
                'recent_3m_avg_inflow': 0,
                'recent_3m_avg_outflow': 0,
            })

        # 同比（YoY）
        try:
            one_year_ago = max_date - timedelta(days=365)
            year_ago_data = group[(group['date'] >= one_year_ago) & (group['date'] < max_date)]
            if len(year_ago_data) > 0:
                year_ago_inflow = year_ago_data['inflow'].sum()
                year_ago_outflow = year_ago_data['outflow'].sum()
                row.update({
                    'yoy_inflow_change': (total_inflow - year_ago_inflow) / year_ago_inflow if year_ago_inflow > 0 else 0,
                    'yoy_outflow_change': (total_outflow - year_ago_outflow) / year_ago_outflow if year_ago_outflow > 0 else 0,
                })
            else:
                row.update({'yoy_inflow_change': 0, 'yoy_outflow_change': 0})
        except:
            row.update({'yoy_inflow_change': 0, 'yoy_outflow_change': 0})

        # 环比（MoM）
        try:
            last_month = max_date - timedelta(days=30)
            two_months_ago = max_date - timedelta(days=60)
            last_month_data = group[(group['date'] >= two_months_ago) & (group['date'] < last_month)]
            if len(last_month_data) > 0:
                last_month_inflow = last_month_data['inflow'].sum()
                last_month_outflow = last_month_data['outflow'].sum()
                row.update({
                    'mom_inflow_change': (total_inflow - last_month_inflow) / last_month_inflow if last_month_inflow > 0 else 0,
                    'mom_outflow_change': (total_outflow - last_month_outflow) / last_month_outflow if last_month_outflow > 0 else 0,
                })
            else:
                row.update({'mom_inflow_change': 0, 'mom_outflow_change': 0})
        except:
            row.update({'mom_inflow_change': 0, 'mom_outflow_change': 0})

        # 交易频率
        row.update({
            'transaction_frequency': total_transactions / duration_days if duration_days > 0 else 0,
            'inflow_frequency': len(group[group['inflow'] > 0]) / duration_days if duration_days > 0 else 0,
            'outflow_frequency': len(group[group['outflow'] > 0]) / duration_days if duration_days > 0 else 0,
        })

        # 分布指标（偏度/峰度）
        row.update({
            'inflow_skewness': group['inflow'].skew() if len(group) > 1 else 0,
            'outflow_skewness': group['outflow'].skew() if len(group) > 1 else 0,
            'inflow_kurtosis': group['inflow'].kurtosis() if len(group) > 1 else 0,
            'outflow_kurtosis': group['outflow'].kurtosis() if len(group) > 1 else 0,
        })

        result = pd.concat([result, pd.DataFrame([row])], ignore_index=True)

    # 处理异常值
    if not result.empty:
        result = result.replace([np.inf, -np.inf], 0).fillna(0)
        result.set_index('id', inplace=True)
    
    return result