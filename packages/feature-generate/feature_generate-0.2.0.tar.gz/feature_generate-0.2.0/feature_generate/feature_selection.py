import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

def select_features_by_importance(X, y, threshold=0):
    """
    基于随机森林特征重要性选择特征
    select_features_by_importance(X, y, threshold=0)
    参数:
        X: 特征DataFrame
        y: 目标变量
        threshold: 重要性阈值，低于此值的特征将被移除

    返回:
        选中的特征列表
    """
    # 训练随机森林
    clf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    clf.fit(X, y)

    # 获取特征重要性
    importance = pd.DataFrame({
        'feature': X.columns,
        'importance': clf.feature_importances_
    }).sort_values('importance', ascending=False)

    # 选择重要特征
    selected_features = importance[importance['importance'] >= threshold]['feature'].tolist()

    return selected_features, importance