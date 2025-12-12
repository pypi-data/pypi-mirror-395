import numpy as np
import pandas as pd
import time
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score
from catboost import CatBoostClassifier


def train_catboost(
    df3,
    final_select,
    categorical_cols_2,
    best_para=None,
    sample_type_col='sample_type',
    id_col='id',
    label_col='label',
    trans_count_col='total_trans',  # 用于 has_flow 判断
    n_seeds=5,
    n_splits=10,
    random_seeds=None,
    output_prefix='submission'
):
    """
    使用 CatBoost 进行带复合分层（has_flow + label）的多种子交叉验证训练。

    Parameters:
    ----------
    df3 : pd.DataFrame
        包含 'sample_type'（值为 'train'/'test'）、'id'、'label' 等列的完整数据。
    final_select : list of str
        用于训练的特征列名列表。
    categorical_cols_2 : list of str
        类别型特征列名列表。
    best_para : dict or None
        CatBoost 超参数。若为 None，则使用内置默认参数。
    sample_type_col : str, default='sample_type'
        标识训练/测试集的列名。
    id_col : str, default='id'
        ID 列名。
    label_col : str, default='label'
        标签列名。
    trans_count_col : str, default='total_trans'
        用于判断是否有流水的列（>0 表示有流水）。
    n_seeds : int, default=5
        随机种子数量。
    n_splits : int, default=10
        每个 seed 的 KFold 折数。
    random_seeds : list of int or None
        自定义随机种子列表。若为 None，则使用 [42, 1023, 2048, 2098, 3031]。
    output_prefix : str, default='submission'
        提交文件前缀。

    Returns:
    -------
    submit : pd.DataFrame
        提交结果 DataFrame，包含 ['id', 'label']。
    oof_probs : np.ndarray
        训练集 OOF 预测概率。
    feat_imp_df : pd.DataFrame
        特征重要性。
    cv_aucs : list
        各 seed 的 CV AUC。
['level_t1','level', 'zipcode_1','zipcode_12','zipcode_3456','zipcode_13456','title_str',
 'career_str','zip_code_str','residence_str','loan_str','term_str','interest_rate_str','syndicated_str','installment_str',
 'total_accounts_str','balance_accounts_str','balance_limit_str','balance_str','issue_time_year_str','issue_time_month_str',
 'record_time_year_str','record_time_month_str','history_time_year_str','history_time_month_str','record_issue_seconds_str',
 'issue_history_seconds_str','record_issue_days_str','issue_history_days_str','interest_rate_squared_str','level_num_str',
 'zipcode_1_str','zipcode_12_str','zipcode_3456_str','zipcode_13456_str', 'first_transaction_date',
'last_transaction_date','issue_time','history_time','record_time','issue_time_year_month','record_time_year_month','history_time_year_month']

    """

    # ---------- 默认参数 ----------
    if best_para is None:
        best_para = {
            'learning_rate': 0.16271598652217544,
            'depth': 5,
            'l2_leaf_reg': 6.831264232199583,
            'subsample': 0.9566308452472696,
            'colsample_bylevel': 0.9179883705565977,
            'min_data_in_leaf': 3,
            'max_ctr_complexity': 7,
            'n_estimators': 2000
        }

    if random_seeds is None:
        random_seeds = [42, 1023, 2048, 2098, 3031]
    else:
        assert len(random_seeds) == n_seeds, f"random_seeds 长度应为 {n_seeds}"

    # ---------- 数据准备 ----------
    train_df = df3[df3[sample_type_col] == "train"].reset_index(drop=True)
    test_df2 = df3[df3[sample_type_col] == "test"].reset_index(drop=True)

    # 生成 has_flow
    train_df['has_flow'] = (train_df[trans_count_col] != 0).astype(int)
    test_df2['has_flow'] = (test_df2[trans_count_col] != 0).astype(int)

    # 复合分层键
    train_df['stratify_key'] = train_df['has_flow'].astype(str) + '_' + train_df[label_col].astype(str)

    # 打印分布（可选，生产环境可注释）
    print("训练集有无流水分布：")
    print(train_df['has_flow'].value_counts(normalize=True).round(3))
    print("\n训练集label分布：")
    print(train_df[label_col].value_counts(normalize=True).round(3))
    print("\n训练集复合分层键分布：")
    print(train_df['stratify_key'].value_counts(normalize=True).round(3))

    # ---------- 特征配置 ----------
    cols = final_select.copy()
    if 'has_flow' not in cols:
        cols.append('has_flow')

    cate_cols = categorical_cols_2.copy()
    if 'has_flow' not in cate_cols:
        cate_cols.append('has_flow')

    print(f'特征数量：{len(cols)}')
    print(f'类别特征数量：{len(cate_cols)}')

    # ---------- 初始化 ----------
    oof_probs = np.zeros(len(train_df))
    test_probs = np.zeros(len(test_df2))
    feat_imp_df = pd.DataFrame({'feat': cols, 'imp': 0})
    cv_aucs = []

    train_start = time.time()

    # ---------- 多种子交叉验证 ----------
    for seed in random_seeds:
        oof_seed = np.zeros(len(train_df))
        skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=seed)

        for fold, (trn_idx, val_idx) in enumerate(skf.split(train_df, train_df['stratify_key'])):
            print(f'\n--------------------- Seed {seed} - Fold {fold} ---------------------')

            trn_x = train_df[cols].iloc[trn_idx].reset_index(drop=True)
            trn_y = train_df[label_col].values[trn_idx]
            val_x = train_df[cols].iloc[val_idx].reset_index(drop=True)
            val_y = train_df[label_col].values[val_idx]

            clf = CatBoostClassifier(
                eval_metric='AUC',
                random_state=seed,
                **best_para
            )
            clf.fit(
                trn_x, trn_y,
                eval_set=[(val_x, val_y)],
                cat_features=cate_cols,
                early_stopping_rounds=400,
                verbose=200
            )

            # 特征重要性累积
            feat_imp_df['imp'] += clf.feature_importances_ / (n_splits * len(random_seeds))

            # 预测
            val_pred = clf.predict_proba(val_x)[:, 1]
            oof_seed[val_idx] = val_pred
            test_probs += clf.predict_proba(test_df2[cols])[:, 1] / (len(random_seeds) * n_splits)

        # 当前 seed 的 AUC
        auc_seed = roc_auc_score(train_df[label_col], oof_seed)
        cv_aucs.append(auc_seed)
        oof_probs += oof_seed / len(random_seeds)
        print(f'Seed {seed} CV AUC: {auc_seed:.6f}')

    # ---------- 最终评估 ----------
    final_auc = round(roc_auc_score(train_df[label_col], oof_probs), 6)
    print(f'\n最终 OOF AUC: {final_auc}')
    print(f'各 seed AUC: {[round(x, 6) for x in cv_aucs]}')
    print(f'总耗时: {time.time() - train_start:.2f}秒')

    # ---------- 生成提交文件 ----------
    submit = pd.DataFrame({
        id_col: test_df2[id_col],
        'label': test_probs
    })

    filename = f"{output_prefix}_auc_{final_auc}.csv"
    submit[[id_col, 'label']].to_csv(filename, index=False)
    print(f'提交文件已保存: {filename}')

    # ---------- 返回结果 ----------
    return submit, oof_probs, feat_imp_df.sort_values('imp', ascending=False), cv_aucs