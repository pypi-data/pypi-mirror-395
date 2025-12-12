def calculate_transaction_features(df, id_col='id', time_col='time', 
                                  amount_col='amount', direction_col='direction'):
    """
   example:
   result=calculate_transaction_features(df_train_2, id_col='id', time_col='time', 
                                  amount_col='amount', direction_col='direction')
   result_test=calculate_transaction_features(df_test_2, id_col='id', time_col='time', 
                                  amount_col='amount', direction_col='direction')
    """
    # 创建数据副本以避免修改原始数据
    df_processed = df.copy()
    
    # 转换时间列为日期格式，只保留日期部分
    try:
        # 转换Unix时间戳为datetime，然后提取日期
        df_processed['date'] = pd.to_datetime(df_processed[time_col], unit='s').dt.date
    except Exception as e:
        print(f"日期转换错误: {e}")
        # 尝试其他处理方式
        df_processed['date'] = pd.to_datetime(df_processed[time_col], errors='coerce').dt.date
    
    # 过滤掉无效的日期值
    df_processed = df_processed[df_processed['date'].notna()]
    
    # 如果没有有效日期数据，直接返回空DataFrame
    if df_processed.empty:
        return pd.DataFrame()
    
    # 提取年、月、日
    df_processed['year'] = pd.to_datetime(df_processed['date']).dt.year
    df_processed['month'] = pd.to_datetime(df_processed['date']).dt.month
    df_processed['day'] = pd.to_datetime(df_processed['date']).dt.day

    # 计算流入和流出金额（使用向量化操作替代apply，提高效率）
    df_processed['inflow'] = df_processed[amount_col].where(df_processed[direction_col] == 0, 0)
    df_processed['outflow'] = df_processed[amount_col].where(df_processed[direction_col] == 1, 0)

    # 按ID分组
    grouped = df_processed.groupby(id_col)

    # 创建结果DataFrame
    result = pd.DataFrame()

    # 对于每个ID，计算各种指标
    for id_val, group in grouped:
        # 基本统计
        total_inflow = group['inflow'].sum()
        total_outflow = group['outflow'].sum()
        net_flow = total_inflow - total_outflow
        total_transactions = len(group)
        
        # 日期相关统计（确保日期有效）
        valid_dates = group['date'].dropna()
        if valid_dates.empty:
            # 如果没有有效日期，跳过该ID
            continue
            
        min_date = valid_dates.min()
        max_date = valid_dates.max()
        duration_days = (max_date - min_date).days if min_date != max_date else 1  # 避免除以0
        
        # 按年统计
        yearly_stats = group.groupby('year').agg({
            'inflow': 'sum',
            'outflow': 'sum'
        }).reset_index()
        
        # 按月统计
        monthly_stats = group.groupby(['year', 'month']).agg({
            'inflow': 'sum',
            'outflow': 'sum'
        }).reset_index()
        
        # 按日统计
        daily_stats = group.groupby('date').agg({
            'inflow': 'sum',
            'outflow': 'sum'
        }).reset_index()
        
        # 创建一行结果
        row = {
            id_col: id_val,
            'total_inflow': total_inflow,
            'total_outflow': total_outflow,
            'net_flow': net_flow,
            'total_transactions': total_transactions,
            'first_transaction_date': min_date,
            'last_transaction_date': max_date,
            'duration_days': duration_days,
            'avg_daily_inflow': daily_stats['inflow'].mean() if not daily_stats.empty else 0,
            'avg_daily_outflow': daily_stats['outflow'].mean() if not daily_stats.empty else 0,
            'max_daily_inflow': daily_stats['inflow'].max() if not daily_stats.empty else 0,
            'max_daily_outflow': daily_stats['outflow'].max() if not daily_stats.empty else 0,
            'min_daily_inflow': daily_stats['inflow'].min() if not daily_stats.empty else 0,
            'min_daily_outflow': daily_stats['outflow'].min() if not daily_stats.empty else 0,
            'std_daily_inflow': daily_stats['inflow'].std() if not daily_stats.empty else 0,
            'std_daily_outflow': daily_stats['outflow'].std() if not daily_stats.empty else 0,
            'avg_monthly_inflow': monthly_stats['inflow'].mean() if not monthly_stats.empty else 0,
            'avg_monthly_outflow': monthly_stats['outflow'].mean() if not monthly_stats.empty else 0,
            'max_monthly_inflow': monthly_stats['inflow'].max() if not monthly_stats.empty else 0,
            'max_monthly_outflow': monthly_stats['outflow'].max() if not monthly_stats.empty else 0,
            'min_monthly_inflow': monthly_stats['inflow'].min() if not monthly_stats.empty else 0,
            'min_monthly_outflow': monthly_stats['outflow'].min() if not monthly_stats.empty else 0,
            'std_monthly_inflow': monthly_stats['inflow'].std() if not monthly_stats.empty else 0,
            'std_monthly_outflow': monthly_stats['outflow'].std() if not monthly_stats.empty else 0,
            'avg_yearly_inflow': yearly_stats['inflow'].mean() if not yearly_stats.empty else 0,
            'avg_yearly_outflow': yearly_stats['outflow'].mean() if not yearly_stats.empty else 0,
            'max_yearly_inflow': yearly_stats['inflow'].max() if not yearly_stats.empty else 0,
            'max_yearly_outflow': yearly_stats['outflow'].max() if not yearly_stats.empty else 0,
            'min_yearly_inflow': yearly_stats['inflow'].min() if not yearly_stats.empty else 0,
            'min_yearly_outflow': yearly_stats['outflow'].min() if not yearly_stats.empty else 0,
            'std_yearly_inflow': yearly_stats['inflow'].std() if not yearly_stats.empty else 0,
            'std_yearly_outflow': yearly_stats['outflow'].std() if not yearly_stats.empty else 0,
            'inflow_outflow_ratio': total_inflow / total_outflow if total_outflow > 0 else 0,
            'outflow_inflow_ratio': total_outflow / total_inflow if total_inflow > 0 else 0,
        }
        
        # 计算最近3个月的统计
        try:
            three_months_ago = max_date - timedelta(days=90)
            # 确保比较的是同类型
            recent_data = group[group['date'].apply(lambda x: x >= three_months_ago)]
            
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
            print(f"计算最近3个月统计时出错: {e}")
            row.update({
                'recent_3m_inflow': 0,
                'recent_3m_outflow': 0,
                'recent_3m_net_flow': 0,
                'recent_3m_avg_inflow': 0,
                'recent_3m_avg_outflow': 0,
            })
        
        # 计算同比变化（与一年前相比）
        try:
            one_year_ago = max_date - timedelta(days=365)
            next_year = one_year_ago + timedelta(days=365)
            year_ago_data = group[group['date'].apply(lambda x: one_year_ago <= x < next_year)]
            
            if len(year_ago_data) > 0:
                year_ago_inflow = year_ago_data['inflow'].sum()
                year_ago_outflow = year_ago_data['outflow'].sum()
                row.update({
                    'yoy_inflow_change': (total_inflow - year_ago_inflow) / year_ago_inflow if year_ago_inflow > 0 else 0,
                    'yoy_outflow_change': (total_outflow - year_ago_outflow) / year_ago_outflow if year_ago_outflow > 0 else 0,
                })
            else:
                row.update({
                    'yoy_inflow_change': 0,
                    'yoy_outflow_change': 0,
                })
        except Exception as e:
            print(f"计算同比变化时出错: {e}")
            row.update({
                'yoy_inflow_change': 0,
                'yoy_outflow_change': 0,
            })
        
        # 计算环比变化（与上个月相比）
        try:
            last_month = max_date - timedelta(days=30)
            two_months_ago = max_date - timedelta(days=60)
            last_month_data = group[group['date'].apply(lambda x: two_months_ago <= x < last_month)]
            
            if len(last_month_data) > 0:
                last_month_inflow = last_month_data['inflow'].sum()
                last_month_outflow = last_month_data['outflow'].sum()
                row.update({
                    'mom_inflow_change': (total_inflow - last_month_inflow) / last_month_inflow if last_month_inflow > 0 else 0,
                    'mom_outflow_change': (total_outflow - last_month_outflow) / last_month_outflow if last_month_outflow > 0 else 0,
                })
            else:
                row.update({
                    'mom_inflow_change': 0,
                    'mom_outflow_change': 0,
                })
        except Exception as e:
            print(f"计算环比变化时出错: {e}")
            row.update({
                'mom_inflow_change': 0,
                'mom_outflow_change': 0,
            })
        
        # 添加交易频率指标
        row.update({
            'transaction_frequency': total_transactions / duration_days if duration_days > 0 else 0,
            'inflow_frequency': len(group[group['inflow'] > 0]) / duration_days if duration_days > 0 else 0,
            'outflow_frequency': len(group[group['outflow'] > 0]) / duration_days if duration_days > 0 else 0,
        })
        
        # 添加金额分布指标
        row.update({
            'inflow_skewness': group['inflow'].skew() if len(group) > 1 else 0,
            'outflow_skewness': group['outflow'].skew() if len(group) > 1 else 0,
            'inflow_kurtosis': group['inflow'].kurtosis() if len(group) > 1 else 0,
            'outflow_kurtosis': group['outflow'].kurtosis() if len(group) > 1 else 0,
        })
        
        # 将结果添加到DataFrame
        result = pd.concat([result, pd.DataFrame([row])], ignore_index=True)

    # 处理无穷大和NaN值
    result = result.replace([np.inf, -np.inf], 0)
    result = result.fillna(0)

    # 设置ID为索引
    if not result.empty and id_col in result.columns:
        result.set_index(id_col, inplace=True)

    return result
