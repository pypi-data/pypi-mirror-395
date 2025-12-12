import pandas as pd
import numpy as np
from .core import (
    process_zipcode_features,
    process_time_features,
    calculate_time_deltas,
    create_transaction_features,
    calculate_transaction_stats,
    process_categorical_features,
    create_dual_features,
    process_numerical_features,
    create_financial_ratios,
    create_stratification_features,
    select_features_by_importance
)
from .utils import remove_duplicate_columns, find_nan_columns

class FeaturePipeline:
    """
    完整的特征工程流水线
    """

    def __init__(self, config=None):
        """
        初始化特征流水线

        参数:
            config: 配置字典，包含各种处理参数
        """
        self.config = config or {}
        self.selected_features = None
        self.feature_importance = None
        self.categorical_cols = self.config.get('categorical_cols', [
            'title', 'career', 'residence', 'term',
            'syndicated', 'installment', 'level'
        ])
        self.time_cols = self.config.get('time_cols', [
            'issue_time', 'record_time', 'history_time'
        ])
        self.numeric_to_cat_cols = self.config.get('numeric_to_cat_cols', [
            'title', 'zip_code', 'residence', 'term', 'syndicated', 'installment',
            'zip_code_first_two', 'zip_code_first_four'
        ])
        self.cat_to_numeric_cols = self.config.get('cat_to_numeric_cols', [
            'career', 'level', 'issue_time', 'record_time', 'history_time'
        ])

    def preprocess_main_data(self, df):
        """
        预处理主数据

        参数:
            df: 主数据DataFrame

        返回:
            预处理后的DataFrame
        """
        # 处理邮政编码
        df = process_zipcode_features(df)

        # 处理时间特征
        df = process_time_features(df, self.time_cols)

        # 处理分类变量
        df = process_categorical_features(df, self.categorical_cols)

        # 计算时间差
        df = calculate_time_deltas(df)

        return df

    def preprocess_transaction_data(self, df):
        """
        预处理交易流水数据

        参数:
            df: 交易流水DataFrame

        返回:
            交易特征DataFrame
        """
        # 基础交易特征
        basic_features = create_transaction_features(df)

        # 高级交易统计
        advanced_stats = calculate_transaction_stats(df)

        # 合并特征
        if not advanced_stats.empty:
            transaction_features = advanced_stats.merge(
                basic_features, on='id', how='left'
            )
        else:
            transaction_features = basic_features

        return transaction_features

    def create_additional_features(self, df):
        """
        创建额外特征

        参数:
            df: DataFrame

        返回:
            增加特征的DataFrame
        """
        # 金融比率
        df = create_financial_ratios(df)

        # 双重特征
        df = create_dual_features(
            df,
            self.numeric_to_cat_cols,
            self.cat_to_numeric_cols
        )

        # 分层特征
        df = create_stratification_features(df)

        return df

    def process_data(self, main_df, transaction_df=None):
        """
        完整处理数据

        参数:
            main_df: 主数据DataFrame
            transaction_df: 交易流水DataFrame (可选)

        返回:
            处理后的DataFrame
        """
        # 预处理主数据
        processed_df = self.preprocess_main_data(main_df.copy())

        # 处理交易数据（如果提供）
        if transaction_df is not None:
            transaction_features = self.preprocess_transaction_data(transaction_df.copy())
            processed_df = processed_df.merge(
                transaction_features.reset_index(),
                on='id',
                how='left'
            )

        # 创建额外特征
        processed_df = self.create_additional_features(processed_df)

        # 处理缺失值
        processed_df = process_numerical_features(processed_df)

        # 去除重复列
        processed_df = remove_duplicate_columns(processed_df)

        return processed_df

    def fit_transform(self, X_train, y_train, X_test=None):
        """
        拟合并转换训练数据，可选转换测试数据

        参数:
            X_train: 训练特征
            y_train: 训练标签
            X_test: 测试特征 (可选)

        返回:
            转换后的训练和测试数据
        """
        # 特征选择
        self.selected_features, self.feature_importance = select_features_by_importance(
            X_train, y_train, threshold=0
        )

        # 应用特征选择
        X_train_selected = X_train[self.selected_features]

        if X_test is not None:
            # 确保测试集有相同的特征
            missing_cols = set(self.selected_features) - set(X_test.columns)
            for col in missing_cols:
                X_test[col] = 0

            X_test_selected = X_test[self.selected_features]
            return X_train_selected, X_test_selected

        return X_train_selected

    def transform(self, X):
        """
        转换新数据

        参数:
            X: 要转换的数据

        返回:
            转换后的数据
        """
        if self.selected_features is None:
            raise ValueError("Pipeline not fitted yet. Call fit_transform first.")

        # 确保所有特征存在
        missing_cols = set(self.selected_features) - set(X.columns)
        for col in missing_cols:
            X[col] = 0

        return X[self.selected_features]