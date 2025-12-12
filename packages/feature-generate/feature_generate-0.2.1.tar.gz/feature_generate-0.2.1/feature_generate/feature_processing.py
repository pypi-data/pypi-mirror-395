def feature_engineering_from_origin(df, non_feat_cols = ['id', 'label', 'sample_type']):
    new_df = df.copy()
    
    #1.时间-一元特征
    time_cols = ['issue_time', 'record_time', 'history_time']
    for col in time_cols:
        # 将秒数转换为datetime类型
        new_df[col] = pd.to_datetime(new_df[col], unit='s')
        new_df[col + '_year'] = new_df[col].dt.year
        new_df[col + '_year_month'] = new_df[col].dt.strftime('%Y-%m')
        new_df[col + '_month'] = new_df[col].dt.month
        new_df[col + '_time'] = new_df[col].dt.time

    #2.时间-二元特征
    record_issue_diff = new_df['record_time'] - new_df['issue_time']
    issue_history_diff = new_df['issue_time'] - new_df['history_time']
    new_df['record_issue_seconds'] = record_issue_diff.dt.total_seconds()
    new_df['issue_history_seconds'] = issue_history_diff.dt.total_seconds()
    new_df['record_issue_days'] = record_issue_diff.dt.days
    new_df['issue_history_days'] = issue_history_diff.dt.days
    
    for col in time_cols:
        new_df[col] = new_df[col].dt.strftime('%Y-%m-%d')

    #3.非时间-一元特征
    new_df['interest_rate_squared']=new_df['interest_rate']*new_df['interest_rate'] # =interest_rate_2
    # new_df['term_str'] = new_df['term_str'] #
    new_df['level_t1'] = new_df['level'].str[0] 
    new_df['level_num']=new_df['level'].str[1].astype(int)
    
    new_df['zipcode_1'] = new_df['zip_code'].astype(str).str[0] # =zipcode1
    new_df['zipcode_12'] = new_df['zip_code'].astype(str).str[0:2] #
    new_df['zipcode_3456'] = new_df['zip_code'].astype(str).str[2:6] # =zipcode3_6
    new_df['zipcode_13456'] = new_df['zip_code'].astype(str).str[0] + new_df['zip_code'].astype(str).str[2:6] # =zipcode13_6

    #4.一元特征转换categorical类型
    convert_cols = [col for col in new_df.columns if col not in non_feat_cols]
    new_df[convert_cols] = new_df[convert_cols].apply(lambda v: pd.to_numeric(v, errors='coerce').fillna(v))
    ori_numeric_feats = new_df[convert_cols].select_dtypes(include=[np.number]).columns.tolist()
    for col in ori_numeric_feats:
        new_df[col + '_str'] = new_df[col].round(2).astype(str) + '_' #数值加_,变成枚举型
    
    #5非时间-二元特征
    new_df['approx_monthly_payment'] = new_df['loan'] / new_df['term']
    
    new_df['loan_ratio'] = new_df['loan']/(new_df['balance_limit']+ 1e-6)
    new_df['loan_ratio2']=new_df['loan']/(new_df['balance']+ 1e-6)

    new_df['account_ratio']=new_df['balance']/new_df['total_accounts']
    new_df['account_ratio']=new_df['balance']/new_df['total_accounts']
    new_df['account_ratio2']=new_df['balance']/new_df['balance_accounts']
    new_df['account_ratio2']=new_df['balance']/new_df['balance_accounts']
    new_df['account_ratio3']=new_df['balance_limit']/new_df['total_accounts']
    new_df['account_ratio3']=new_df['balance_limit']/new_df['total_accounts']
    new_df['account_ratio4']=new_df['balance_limit']/new_df['balance_accounts']
    new_df['account_ratio4']=new_df['balance_limit']/new_df['balance_accounts']

    new_df['utilization_rate'] = new_df['balance'] / (new_df['balance_limit'] + 1e-6)
    new_df['remain_balance']=new_df['balance_limit']-new_df['balance'] # =limit_balance
    new_df['loan_x_ir']=new_df['loan']*new_df['interest_rate'] # =loan_interest_rate

    new_df['loan_per_r_i_day']=new_df['loan']/(new_df['record_issue_days']+ 1e-6) # =duration_ratio
    new_df['loan_per_i_h_day']=new_df['loan']/(new_df['issue_history_days']+ 1e-6) # =duration_ratio2
    
    new_df['balance_x_ir'] = new_df['balance']*new_df['interest_rate'] # =bal_int
    new_df['balance_x_ir_x_issue'] = new_df['issue_time_year']*new_df['balance_x_ir'] # =issue_bal
    new_df['balimit_x_ir'] = new_df['balance_limit']*new_df['interest_rate'] # =limit_int

    return new_df

## 函数2：基于交易流水衍生特征
def calculate_transaction_features(df, id_col='id', time_col='time', 
                                  amount_col='amount', direction_col='direction'):
    """
    计算交易数据的各种特征（时间精度到年月日）
    
    参数:
    df: 包含交易数据的DataFrame
    id_col: 用户ID列名
    time_col: 时间列名（Unix时间戳）
    amount_col: 金额列名
    direction_col: 交易方向列名（0表示流入，1表示流出）
    
    返回:
    包含每个ID的各种交易特征的DataFrame
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
            # 'total_transactions': total_transactions,
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
            'inflow_total_ratio': total_inflow / total_outflow if total_outflow > 0 else 0,
            # 'outflow_inflow_ratio': total_outflow / total_inflow if total_inflow > 0 else 0,
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

#########基于交易流水的衍生，总交易次数、进出账比例等等。
## 函数3：基于交易流水衍生特征补充
def create_transaction_features(df,id_col='id', time_col='time', 
                                  amount_col='amount', direction_col='direction'):
    """
    从交易流水数据中提取统计特征
    
    Parameters:
    df: DataFrame with columns ['id', 'time', 'direction', 'amount']
        direction: 1表示进账(inflow), 0表示出账(outflow)
    """
    df_processed = df.copy()
    # 确保时间戳为datetime类型
    df_processed[time_col] = pd.to_datetime(df_processed[time_col], unit='s')
    
    # 按客户id分组
    grouped = df_processed.groupby(id_col)
    
    # 初始化特征 DataFrame
    features = pd.DataFrame(index=df_processed[id_col].unique())
    features.index.name = id_col
    
    # 1. 基本统计特征
    # 总交易次数
    features['total_transactions'] = grouped.size()
    
    # 进账次数和出账次数
    features['inflow_count'] = grouped[direction_col].apply(lambda x: (x == 1).sum())
    features['outflow_count'] = grouped[direction_col].apply(lambda x: (x == 0).sum())
    
    # 进账出账比例
    features['inflow_outflow_ratio'] = features['inflow_count'] / (features['outflow_count'] + 1e-5)
    
    # 进出账金额统计
    inflow_df = df_processed[df_processed[direction_col] == 1]
    outflow_df = df_processed[df_processed[direction_col] == 0]
    
    inflow_amount = inflow_df.groupby(id_col)[amount_col].sum()
    outflow_amount = outflow_df.groupby(id_col)[amount_col].sum()
    
    features['total_inflow_amount'] = inflow_amount
    features['total_outflow_amount'] = outflow_amount
    features['net_cash_flow'] = features['total_inflow_amount'] - features['total_outflow_amount']
    features['inflow_outflow_amount_ratio'] = features['total_inflow_amount'] / (features['total_outflow_amount'] + 1e-5)
    
    # 2. 金额统计特征
    amount_stats = grouped[amount_col].agg(['mean', 'std', 'min', 'max', 'median'])
    amount_stats.columns = ['amount_mean', 'amount_std', 'amount_min', 'amount_max', 'amount_median']
    features = features.join(amount_stats)
    
    # 金额变异系数（标准差/均值）
    features['amount_coefficient_of_variation'] = features['amount_std'] / (features['amount_mean'] + 1e-5)
    
    # 进出账分别的金额统计
    inflow_amount_stats = inflow_df.groupby(id_col)[amount_col].agg(['mean', 'std', 'max'])
    inflow_amount_stats.columns = ['inflow_amount_mean', 'inflow_amount_std', 'inflow_amount_max']
    features = features.join(inflow_amount_stats)
    
    outflow_amount_stats = outflow_df.groupby(id_col)[amount_col].agg(['mean', 'std', 'max'])
    outflow_amount_stats.columns = ['outflow_amount_mean', 'outflow_amount_std', 'outflow_amount_max']
    features = features.join(outflow_amount_stats)
    
    # 3. 时间相关特征
    # 交易时间跨度（天）
    features['transaction_time_span_days'] = grouped[time_col].apply(lambda x: (x.max() - x.min()).days)
    
    # 日均交易次数
    features['daily_avg_transactions'] = features['total_transactions'] / (features['transaction_time_span_days'] + 1e-5)
    
    # 最近一次交易距今的时间
    current_time = df_processed[time_col].max()
    features['days_since_last_transaction'] = grouped[time_col].apply(lambda x: (current_time - x.max()).days)
    
    # 第一次交易距今的时间
    features['days_since_first_transaction'] = grouped[time_col].apply(lambda x: (current_time - x.min()).days)
    
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
    
    features['max_consecutive_inflow'] = grouped[direction_col].apply(max_consecutive_inflow)
    
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
    
    features['max_consecutive_outflow'] = grouped[direction_col].apply(max_consecutive_outflow)
    
    # 5. 交易金额的偏度和峰度
    features['amount_skewness'] = grouped[amount_col].apply(lambda x: x.skew())
    features['amount_kurtosis'] = grouped[amount_col].apply(lambda x: x.kurtosis())
    
    # 6. 交易周期性特征
    # 提取星期几的信息
    df_processed['day_of_week'] = df_processed[time_col].dt.dayofweek
    weekly_counts = df_processed.groupby([id_col, 'day_of_week']).size().unstack(fill_value=0)
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
    recent_df = df_processed[df_processed[time_col] >= recent_cutoff]
    recent_grouped = recent_df.groupby(id_col)
    
    features['recent_30d_transactions'] = recent_grouped.size()
    features['recent_30d_inflow_count'] = recent_grouped[direction_col].apply(lambda x: (x == 1).sum())
    features['recent_30d_outflow_count'] = recent_grouped[direction_col].apply(lambda x: (x == 0).sum())
    features['recent_30d_net_cash_flow'] = recent_grouped.apply(lambda x: x[x[direction_col] == 1][amount_col].sum() - 
                                                              x[x[direction_col] == 0][amount_col].sum())
    
    # 填充缺失值（对于最近30天无交易的客户）
    features.fillna({
        'recent_30d_transactions': 0,
        'recent_30d_inflow_count': 0,
        'recent_30d_outflow_count': 0,
        'recent_30d_net_cash_flow': 0
    }, inplace=True)
    
    return features