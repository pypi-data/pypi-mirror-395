import warnings
#>>A
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold
# 模型开关
HAS_XGB = True
HAS_CTB = True
HAS_RF = True
TOP_K=3
import lightgbm as lgb
import xgboost as xgb
from catboost import CatBoostClassifier
from sklearn.ensemble import  RandomForestClassifier
def train_models(X, y, T, features, cat_cols):
    """训练多个模型并进行预测"""
    def _compute_spw(y):
        n_pos = int(y.sum())
        n_neg = int(len(y) - n_pos)
        spw = max(n_neg / max(n_pos, 1), 1.0)
        return spw, n_pos, n_neg

    scale_pos_weight, n_pos, n_neg = _compute_spw(y)
    print(f"[Info] Pos={int(n_pos)}, Neg={int(n_neg)}, scale_pos_weight={scale_pos_weight:.3f}")
    # 5折 OOF 训练
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    oof_lgb = np.zeros(len(X))
    oof_xgb = np.zeros(len(X)) if HAS_XGB else None
    oof_ctb = np.zeros(len(X)) if HAS_CTB else None
    oof_rf = np.zeros(len(X)) if HAS_RF else None
    pred_lgb = np.zeros(len(T))
    pred_xgb = np.zeros(len(T)) if HAS_XGB else None
    pred_ctb = np.zeros(len(T)) if HAS_CTB else None
    pred_rf = np.zeros(len(T)) if HAS_RF else None
    fi_list = []
    # 候选模型列表
    candidates = {'LGB': [], 'XGB': [], 'CTB': [], 'RF': []}

    for fold, (tr_idx, val_idx) in enumerate(skf.split(X, y), 1):
        X_tr, X_va = X.iloc[tr_idx][features], X.iloc[val_idx][features]
        y_tr, y_va = y.iloc[tr_idx], y.iloc[val_idx]
        print(f'fold x {fold}', len(X_tr), len(X_va), len(y_tr), len(y_va))

        # LightGBM - 使用LGBMClassifier
        spw = _compute_spw(y_tr)[0] * 0.5
        lgb_model = lgb.LGBMClassifier( objective="binary", metric="auc",
            boosting_type='gbdt',  learning_rate=0.009,num_leaves=165,
            max_depth=-1, min_child_samples=45,  # 对应min_data_in_leaf
            feature_fraction=0.62, bagging_fraction=0.9,
            bagging_freq=3,reg_alpha=0.001,  reg_lambda=2.41,  # 对应lambda_l1,lambda_l2
            min_split_gain=0.84,  # 对应min_gain_to_split
            scale_pos_weight=spw,
            random_state=42 + fold,
            n_jobs=-1,
            n_estimators=2000  # 对应num_boost_round
        )
        lgb_model.fit(
            X_tr, y_tr,
            eval_set=[(X_tr, y_tr), (X_va, y_va)],
            eval_metric='auc',
            callbacks=[lgb.early_stopping(stopping_rounds=200, verbose=False)],
            categorical_feature=cat_cols or None
        )
        oof_lgb[val_idx] = lgb_model.predict_proba(X_va)[:, 1]
        auc_l = roc_auc_score(y_va, oof_lgb[val_idx])
        candidates['LGB'].append((auc_l, fold, lgb_model))
        print(f"[Fold {fold}] LGB AUC={auc_l:.5f}")
        # XGBoost - 使用XGBClassifier
        if HAS_XGB:
            xgb_model = xgb.XGBClassifier(
                objective="binary:logistic",
                eval_metric="auc",tree_method="hist",
                learning_rate=0.007,  max_depth=7,
                subsample=0.76,  colsample_bytree=0.83,
                min_child_weight=13.11, reg_alpha=0.027,
                reg_lambda=0.028, gamma=1.17,
                scale_pos_weight=spw,
                random_state=42 + fold,
                n_jobs=-1,  # 对应nthread
                n_estimators=2000,  # 对应num_boost_round
                early_stopping_rounds=200
            )
            xgb_model.fit(
                X_tr, y_tr,
                eval_set=[(X_tr, y_tr), (X_va, y_va)],
                verbose=False  # 对应verbose_eval
            )
            oof_xgb[val_idx] = xgb_model.predict_proba(X_va)[:, 1]
            auc_x = roc_auc_score(y_va, oof_xgb[val_idx])
            candidates['XGB'].append((auc_x, fold, xgb_model))
            print(f"[Fold {fold}] XGB AUC={auc_x:.5f}")
        # CatBoost
        if HAS_CTB:
            cat_idx = [features.index(c) for c in cat_cols if c in features]
            ctb_model = CatBoostClassifier(
                loss_function='Logloss',
                eval_metric='AUC',  learning_rate=0.03,
                early_stopping_rounds=200, iterations=2000,
                max_depth=7,l2_leaf_reg=6, random_seed=42 + fold,
                verbose=False
            )
            ctb_model.fit(
                X_tr, y_tr,
                eval_set=(X_va, y_va),
                cat_features=cat_idx,
                use_best_model=True
            )
            oof_ctb[val_idx] = ctb_model.predict_proba(X_va)[:, 1]
            auc_c = roc_auc_score(y_va, oof_ctb[val_idx])
            candidates['CTB'].append((auc_c, fold, ctb_model))
            print(f"[Fold {fold}] CTB AUC={auc_c:.5f}")

        # Random Forest
        if HAS_RF:
            rf_model = RandomForestClassifier(
                n_estimators=900, min_samples_split=2, min_samples_leaf=1,
                max_features="sqrt", class_weight="balanced",
                oob_score=True, n_jobs=-1,
                random_state=42 + fold,
                verbose=0
            )
            rf_model.fit(X_tr, y_tr)
            oof_rf[val_idx] = rf_model.predict_proba(X_va)[:, 1]
            auc_rf = roc_auc_score(y_va, oof_rf[val_idx])
            candidates['RF'].append((auc_rf, fold, rf_model))
            print(f"[Fold {fold}] RF AUC={auc_rf:.5f}")

    # 选择最佳模型进行预测
    def select_topk_models(model_name, candidates_list, predict_func):
        sorted_candidates = sorted(candidates_list, key=lambda x: x[0], reverse=True)
        topk = sorted_candidates[:min(TOP_K, len(sorted_candidates))]
        predictions = []
        for auc, fold, model in topk:
            predictions.append(predict_func(model))
        return np.mean(np.vstack(predictions), axis=0)
    # 预测函数
    def model_predict(model):   return model.predict_proba(T[features])[:, 1]
    # 生成最终预测
    pred_lgb = select_topk_models('LGB', candidates['LGB'], model_predict)
    if HAS_XGB:  pred_xgb = select_topk_models('XGB', candidates['XGB'], model_predict)
    if HAS_CTB:  pred_ctb = select_topk_models('CTB', candidates['CTB'], model_predict)
    if HAS_RF:   pred_rf = select_topk_models('RF', candidates['RF'], model_predict)
    # OOF 评估
    def pr_auc(name, oof):
        auc = roc_auc_score(y, oof)
        print(f"[OOF] {name} AUC = {auc:.6f}")
        return auc
    pr_auc("LGB", oof_lgb)
    pr_auc("XGB", oof_xgb) if HAS_XGB else None
    pr_auc("CTB", oof_ctb) if HAS_CTB else None
    pr_auc("RF", oof_rf) if HAS_RF else None
    return oof_lgb, oof_xgb, oof_ctb, oof_rf, pred_lgb, pred_xgb, pred_ctb, pred_rf
from sklearn.linear_model import LogisticRegression
def ensemble_predictions(oof_list, pred_list, y):
    """集成多个模型的预测结果"""
    meta_features = [oof for oof in oof_list if oof is not None]
    test_meta = [pred for pred in pred_list if pred is not None]
    META = np.vstack(meta_features).T
    TEST_META = np.vstack(test_meta).T
    # Logistic 回归二层
    meta_lr = LogisticRegression(
        solver="liblinear",class_weight="balanced",C=1.0,random_state=42
    )
    meta_lr.fit(META, y)
    oof_meta = meta_lr.predict_proba(META)[:, 1]
    auc_meta = roc_auc_score(y, oof_meta)
    print(f"[OOF] META-LR AUC = {auc_meta:.6f}")
    pred_meta = meta_lr.predict_proba(TEST_META)[:, 1]
    # Rank Averaging
    def rank_avg(preds: np.ndarray) -> np.ndarray:
        R = []
        for i in range(preds.shape[0]):
            r = pd.Series(preds[i]).rank(method="average") / preds.shape[1]
            R.append(r.values)
        R = np.vstack(R)
        return R.mean(axis=0)
    oof_stack = np.vstack(meta_features)
    oof_rank = rank_avg(oof_stack)
    auc_rank = roc_auc_score(y, oof_rank)
    print(f"[OOF] Rank-Average AUC = {auc_rank:.6f}")
    test_rank = rank_avg(np.vstack(test_meta))
    # 最终融合
    final_pred = 0.5 * pred_meta + 0.5 * test_rank
    return final_pred
