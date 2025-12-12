import pandas as pd
from your_package import FeaturePipeline, CatBoostTrainer
from your_package.utils import load_data

# 1. 加载数据
train_main, test_main = load_data('init_data/train.csv', 'init_data/testab.csv')
train_trans, test_trans = load_data('init_data/train_bank_statement.csv', 'init_data/testab_bank_statement.csv')

# 2. 配置特征流水线
pipeline_config = {
    'categorical_cols': ['title', 'residence', 'career', 'term', 'syndicated', 'installment', 'level'],
    'time_cols': ['issue_time', 'record_time', 'history_time'],
    'numeric_to_cat_cols': ['zip_code_first_two', 'zip_code_first_four'],
    'cat_to_numeric_cols': ['career', 'level']
}

pipeline = FeaturePipeline(pipeline_config)

# 3. 处理数据
train_processed = pipeline.process_data(train_main, train_trans)
test_processed = pipeline.process_data(test_main, test_trans)

# 4. 准备训练数据
X_train = train_processed.drop(['id', 'label', 'sample_type'], axis=1, errors='ignore')
y_train = train_processed['label']
X_test = test_processed.drop(['id', 'sample_type'], axis=1, errors='ignore')

# 5. 特征选择
X_train_selected, X_test_selected = pipeline.fit_transform(X_train, y_train, X_test)

# 6. 配置并训练模型
trainer = CatBoostTrainer(
    output_dir='results',
    categorical_features=[col for col in X_train_selected.columns 
                          if X_train_selected[col].dtype.name == 'category']
)

# 添加分层特征
train_processed = trainer.add_stratification_features(train_processed)
stratify_key = train_processed['stratify_key']

# 训练模型
oof_predictions = trainer.train(
    X_train_selected, 
    y_train,
    stratify_key=stratify_key
)

# 7. 预测并保存结果
test_predictions = trainer.predict(X_test_selected)
submission_path = trainer.save_results(test_processed['id'], test_predictions)

print(f"Submission saved to: {submission_path}")
print(f"Feature importance saved to: results/feature_importance.csv")
trainer.get_feature_importance().to_csv('results/feature_importance.csv', index=False)