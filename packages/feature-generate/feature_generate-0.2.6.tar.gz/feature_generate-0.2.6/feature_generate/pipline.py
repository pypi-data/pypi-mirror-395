# your_package/pipeline.py

import pandas as pd

# 导入所有已修复的模块（依赖 __init__.py 或正确包结构）
from .core.feature_engineering import add_time_numeric_features, add_ratio_features, add_custom_encodings
from .core.zipcode_processing import process_zipcode_features
from .core.time_processing import process_time_features
from .core.categorical_processing import process_categorical_features, create_dual_features
from .core.transation_processing import create_transaction_features, calculate_transaction_stats
from .core.business_rules import add_business_flag_features
from .core.feature_encoding import add_str_columns


class FeaturePipeline:
    def __init__(self):
        self.cat_to_numeric_cols = [
            'career', 'issue_time', 'record_time', 'history_time', 'level',
            'issue_time_year_month', 'issue_time_time',
            'record_time_year_month', 'record_time_time',
            'history_time_year_month', 'history_time_time',
            'first_transaction_date', 'last_transaction_date'
        ]
        self.str_cols = [
            'title', 'career', 'zip_code', 'residence', 'loan', 'term', 'interest_rate',
            'issue_time', 'syndicated', 'installment', 'record_time', 'history_time',
            'total_accounts', 'balance_accounts', 'balance_limit', 'balance', 'level'
        ]

    def _merge_with_transaction_features(self, main_df, trans_df):
    # 分别从原始 trans_df 提取两类特征
        time_features = create_transaction_features(trans_df)
        stat_features = calculate_transaction_stats(trans_df)

            # === 关键调试信息 ===
        print("\n🔍 time_features 列名:")
        print(time_features.columns.tolist())
        print("前3行:")
        print(time_features.head(3))

        print("\n🔍 stat_features 列名:")
        print(stat_features.columns.tolist())
        print("前3行:")
        print(stat_features.head(3))
        # ===================

        # 合并（假设都有 'user_id'）
        trans_features = time_features.merge(stat_features, on='id', how='outer')
    
        return main_df.merge(trans_features, on='id', how='left')
    def run(self, main_train_path, main_test_path, trans_train_path, trans_test_path):
        """
        输入：4个CSV路径
        输出：(train_df, test_df)，已完成170维特征工程
        """
        # 加载数据（注意：这里只做 pd.read_csv，不处理路径存在性）
        train_main = pd.read_csv(main_train_path)
        test_main = pd.read_csv(main_test_path)
        train_trans = pd.read_csv(trans_train_path)
        test_trans = pd.read_csv(trans_test_path)

        # 🔥 关键修复：强制转换时间列为 datetime
        time_cols = ['issue_time', 'record_time', 'history_time']
        for col in time_cols:
            if col in train_main.columns:
                train_main[col] = pd.to_datetime(train_main[col], errors='coerce')
            if col in test_main.columns:
                test_main[col] = pd.to_datetime(test_main[col], errors='coerce')
        
        # 合并交易特征
        train_df = self._merge_with_transaction_features(train_main, train_trans)
        test_df = self._merge_with_transaction_features(test_main, test_trans)

        # 统一特征工程
        # 替换为：
        train_df = add_str_columns(train_df, self.str_cols)
        train_df = process_zipcode_features(train_df)
        train_df = process_time_features(train_df)
        train_df = process_categorical_features(train_df)
        train_df = add_business_flag_features(train_df)
        train_df = add_time_numeric_features(train_df)
        train_df = add_ratio_features(train_df)
        train_df = add_custom_encodings(train_df)
        train_df = create_dual_features(train_df, numeric_to_cat_cols=None, cat_to_numeric_cols=self.cat_to_numeric_cols)

        test_df = add_str_columns(test_df, self.str_cols)
        test_df = process_zipcode_features(test_df)
        test_df = process_time_features(test_df)
        test_df = process_categorical_features(test_df)
        test_df = add_business_flag_features(test_df)
        test_df = add_time_numeric_features(test_df)
        test_df = add_ratio_features(test_df)
        test_df = add_custom_encodings(test_df)
        test_df = create_dual_features(test_df, numeric_to_cat_cols=None, cat_to_numeric_cols=self.cat_to_numeric_cols)
        return train_df, test_df