import pandas as pd
import numpy as np
import time
from catboost import CatBoostClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score
from .utils import save_submission

class CatBoostTrainer:
    """
    CatBoost模型训练器，支持分层K折交叉验证
    """

    def __init__(self, params=None, n_splits=10, seeds=None, output_dir='results'):
        """
        初始化训练器

        参数:
            params: CatBoost参数字典
            n_splits: 交叉验证折数
            seeds: 随机种子列表
            output_dir: 结果输出目录
        """
        self.params = params or {
            'learning_rate': 0.0327,
            'depth': 8,
            'l2_leaf_reg': 6.83,
            'subsample': 0.9566,
            'colsample_bylevel': 0.9180,
            'min_data_in_leaf': 3,
            'max_ctr_complexity': 7,
            'n_estimators': 2000,
            'eval_metric': 'AUC',
            'early_stopping_rounds': 400,
            'verbose': 200,
            'thread_count': -1
        }
        self.n_splits = n_splits
        self.seeds = seeds or [42, 1023, 2048, 2098, 3031]
        self.output_dir = output_dir
        self.models = []
        self.feature_importances = None
        self.final_auc = None

    def train(self, X, y, categorical_features=None, stratify_key=None):
        """
        训练模型

        参数:
            X: 特征DataFrame
            y: 目标变量
            categorical_features: 类别特征列表
            stratify_key: 分层键列名

        返回:
            交叉验证预测概率
        """
        start_time = time.time()
        oof_predictions = np.zeros(len(X))
        self.feature_importances = pd.DataFrame({'feature': X.columns, 'importance': 0})

        # 为分层准备
        if stratify_key is None:
            stratify_key = y

        # 多种子训练
        for seed in self.seeds:
            skf = StratifiedKFold(n_splits=self.n_splits, shuffle=True, random_state=seed)

            for fold, (train_idx, valid_idx) in enumerate(skf.split(X, stratify_key)):
                print(f"Seed {seed}, Fold {fold+1}/{self.n_splits}")

                # 划分数据
                X_train, y_train = X.iloc[train_idx], y.iloc[train_idx]
                X_valid, y_valid = X.iloc[valid_idx], y.iloc[valid_idx]

                # 训练模型
                model = CatBoostClassifier(
                    random_state=seed,
                    **self.params
                )
                model.fit(
                    X_train,
                    y_train,
                    eval_set=(X_valid, y_valid),
                    cat_features=categorical_features,
                    verbose=self.params.get('verbose', 200)
                )

                # 预测验证集
                valid_preds = model.predict_proba(X_valid)[:, 1]
                oof_predictions[valid_idx] += valid_preds / len(self.seeds)

                # 累积特征重要性
                fold_importance = pd.DataFrame({
                    'feature': X.columns,
                    'importance': model.feature_importances_
                })
                self.feature_importances = self.feature_importances.merge(
                    fold_importance, on='feature', suffixes=('', f'_fold{fold}')
                )
                self.feature_importances['importance'] += fold_importance['importance'] / (self.n_splits * len(self.seeds))

                # 保存模型
                self.models.append(model)

        # 计算最终AUC
        self.final_auc = roc_auc_score(y, oof_predictions)
        training_time = time.time() - start_time

        print(f"Training completed in {training_time:.2f} seconds")
        print(f"Final OOF AUC: {self.final_auc:.6f}")

        return oof_predictions

    def predict(self, X):
        """
        预测新数据

        参数:
            X: 特征DataFrame

        返回:
            预测概率
        """
        if not self.models:
            raise ValueError("No models trained. Call train() first.")

        predictions = np.zeros(len(X))

        for model in self.models:
            predictions += model.predict_proba(X)[:, 1]

        return predictions / len(self.models)

    def save_results(self, test_ids, test_predictions):
        """
        保存预测结果

        参数:
            test_ids: 测试集ID
            test_predictions: 测试集预测概率

        返回:
            保存的文件路径
        """
        return save_submission(
            test_ids,
            test_predictions,
            self.output_dir,
            self.final_auc
        )

    def get_feature_importance(self):
        """
        获取特征重要性

        返回:
            特征重要性DataFrame
        """
        if self.feature_importances is None:
            raise ValueError("Feature importance not calculated. Call train() first.")

        return self.feature_importances.sort_values('importance', ascending=False)