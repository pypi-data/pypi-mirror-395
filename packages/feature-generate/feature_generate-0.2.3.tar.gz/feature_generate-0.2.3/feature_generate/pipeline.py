# your_package/pipeline.py

from .core.zipcode_processing import process_zipcode_features
from .core.time_processing import process_time_features
from .core.categorical_processing import process_categorical_features
from .core.transaction_processing import create_transaction_features, calculate_transaction_stats
from .core.business_rules import add_business_flag_features
from .core.feature_encoding import add_str_columns
from .core.categorical_processing import create_dual_features  # 确保该函数存在


class FeaturePipeline:
    def __init__(self, config=None):
        self.config = config or {}

    def run(self, df):
        """
        执行完整的特征工程流水线，还原 Jupyter 中 170 个特征
        """
        import pandas as pd
        df = df.copy()

        # 1. 邮编特征
        df = process_zipcode_features(df)

        # 2. 时间特征（包含 _time 转秒）
        df = process_time_features(df)

        # 3. 分类特征基础处理（填充、转 category）
        df = process_categorical_features(df)

        # 4. 交易特征（基础 + 高级统计）
        df = create_transaction_features(df)
        df = calculate_transaction_stats(df)  # 确保此函数输出 min_daily_inflow 等

        # 5. 业务规则特征（bq, bq2, bq3）
        df = add_business_flag_features(df)

        # 6. 创建 _numeric 双重特征（用于 LightGBM 等）
        cat_to_numeric_cols = [
            'career', 'issue_time', 'record_time', 'history_time', 'level',
            'issue_time_year_month', 'issue_time_time',
            'record_time_year_month', 'record_time_time',
            'history_time_year_month', 'history_time_time',
            'first_transaction_date', 'last_transaction_date'
        ]
        df = create_dual_features(
            df,
            numeric_to_cat_cols=None,
            cat_to_numeric_cols=cat_to_numeric_cols
        )

        # 7. 添加字符串副本（_str 列）
        str_cols = [
            'title', 'career', 'zip_code', 'residence', 'loan', 'term', 'interest_rate',
            'issue_time', 'syndicated', 'installment', 'record_time', 'history_time',
            'total_accounts', 'balance_accounts', 'balance_limit', 'balance', 'level'
        ]
        df = add_str_columns(df, str_cols)

        return df