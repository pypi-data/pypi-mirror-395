#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提交制式训练脚本：
用法：
  python3 train.py trainSetDir modelPath

说明：
- 仅接受两个位置参数：训练数据根目录、模型保存目录；其余路径与参数全部写死，保证复现初赛结果。
- 训练阶段会：
  1) 读取最终特征表（硬编码为 temp_data/features/day11_team_out/team_merged_{train,test}.csv，自动相对项目根路径解析）
  2) 基于 trainSetDir 与固定测试集目录为样本添加 is_bank_statement 特征
  3) 复刻现有 LGB 与 XGB 的网格 + 5 折 CV 训练，并在循环中保存“候选网格对应每折模型”
  4) 选出单模型最优网格（以 OOF AUC 最大），保存“最优网格下每折模型”与融合所需权重
  5) 将必要的元信息（特征列顺序、参数、融合权重等）保存到 modelPath

注意：本脚本为比赛提交版。
"""

import os
import sys
import argparse
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score


# ----------------------------
# 常量（写死，相对路径保证复现实验）
# ----------------------------
FEATURE_DIR = os.path.join("..", "temp_data", "features", "day11_team_out", "merged")
TRAIN_FEAT = os.path.join(FEATURE_DIR, "team_merged_train.csv")
TEST_FEAT  = os.path.join(FEATURE_DIR, "team_merged_test.csv")

# 固定测试集银行流水路径（按初赛B榜目录结构），相对 code/ 目录
FIXED_TEST_BANK_PATH = os.path.join("..", "init_data", "初赛B榜数据集", "testab", "testab_bank_statement.csv")

N_SPLITS = 5
SEEDS = [42]


# ----------------------------
# 辅助函数（与 code/train.py 一致的列处理）
# ----------------------------
def _select_X(df: pd.DataFrame) -> pd.DataFrame:
    X = df.drop(columns=[c for c in ['id','label'] if c in df.columns]).copy()
    for c in X.columns:
        if X[c].dtype == 'object':
            X[c] = X[c].astype('category').cat.codes
    return X

def rank_norm(a: np.ndarray) -> np.ndarray:
    s = pd.Series(a)
    r = s.rank(method="average").to_numpy()
    return (r - r.min()) / (r.max() - r.min() + 1e-12)

def add_bank_statement_feature(train_df: pd.DataFrame, test_df: pd.DataFrame,
                               train_bank_statement_path: str, test_bank_statement_path: str):
    # 训练集
    if train_bank_statement_path and os.path.exists(train_bank_statement_path):
        train_bank_data = pd.read_csv(train_bank_statement_path)
        train_users_with_bank = set(train_bank_data['id'].unique())
        train_df['is_bank_statement'] = train_df['id'].isin(train_users_with_bank).astype(int)
    else:
        train_df['is_bank_statement'] = 0
    # 测试集
    if test_bank_statement_path and os.path.exists(test_bank_statement_path):
        test_bank_data = pd.read_csv(test_bank_statement_path)
        test_users_with_bank = set(test_bank_data['id'].unique())
        test_df['is_bank_statement'] = test_df['id'].isin(test_users_with_bank).astype(int)
    else:
        test_df['is_bank_statement'] = 0
    return train_df, test_df


# ----------------------------
# 训练（同时缓存候选网格的折内模型）
# ----------------------------
def train_lgbm_cv_with_models(X, y, X_test):
    try:
        import lightgbm as lgb
    except Exception as e:
        print(f"[LGB] import error -> skip LGB: {e}")
        return None

    grids = [
        dict(num_leaves=48, min_data_in_leaf=60, feature_fraction=0.7, bagging_fraction=0.8, reg_alpha=0.5, reg_lambda=5.0),
        dict(num_leaves=64, min_data_in_leaf=80, feature_fraction=0.7, bagging_fraction=0.8, reg_alpha=0.5, reg_lambda=5.0),
        dict(num_leaves=96, min_data_in_leaf=120, feature_fraction=0.7, bagging_fraction=0.8, reg_alpha=0.5, reg_lambda=5.0),
    ]

    best = {'auc':-1,'params':None,'oof':None,'pred':None,'grid_idx':None,'fold_models':None}
    for gi, p in enumerate(grids):
        params = dict(
            objective='binary', boosting_type='gbdt', learning_rate=0.03, max_depth=-1,
            n_estimators=5000, bagging_freq=1, num_leaves=p['num_leaves'],
            min_data_in_leaf=p['min_data_in_leaf'], feature_fraction=p['feature_fraction'],
            bagging_fraction=p['bagging_fraction'], reg_alpha=p['reg_alpha'], reg_lambda=p['reg_lambda']
        )
        oof_all = np.zeros(len(X)); pred_all = np.zeros(len(X_test))
        fold_models = []
        for seed in SEEDS:
            skf = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=seed)
            for fold,(tr,va) in enumerate(skf.split(X,y),1):
                dtr = lgb.Dataset(X.iloc[tr], label=y.iloc[tr])
                dva = lgb.Dataset(X.iloc[va], label=y.iloc[va])
                model = lgb.train(
                    params, dtr, valid_sets=[dtr,dva], valid_names=['train','valid'],
                    num_boost_round=20000,
                    callbacks=[lgb.early_stopping(300, verbose=False), lgb.log_evaluation(100)],
                )
                oof_all[va] = model.predict(X.iloc[va], num_iteration=model.best_iteration)
                pred_all += model.predict(X_test, num_iteration=model.best_iteration) / (N_SPLITS*len(SEEDS))
                fold_models.append(model)
                print(f"[LGB Grid {gi} Fold {fold}] AUC={roc_auc_score(y.iloc[va], oof_all[va]):.6f}")
        auc = roc_auc_score(y, oof_all)
        print(f"[LGB] grid combo AUC={auc:.6f} params={params}")
        if auc>best['auc']:
            best = {'auc':auc,'params':params,'oof':oof_all,'pred':pred_all,'grid_idx':gi,'fold_models':fold_models}
    print(f"Best LGB OOF AUC = {best['auc']:.6f}")
    return best


def _xgb_predict(bst, d):
    if hasattr(bst, "best_iteration") and bst.best_iteration is not None:
        return bst.predict(d, iteration_range=(0, bst.best_iteration+1))
    if hasattr(bst, "best_ntree_limit") and getattr(bst, "best_ntree_limit", None):
        return bst.predict(d, ntree_limit=bst.best_ntree_limit)
    return bst.predict(d)


def train_xgb_cv_with_models(X, y, X_test):
    import xgboost as xgb
    grids = [
        dict(eta=0.03, max_depth=6, min_child_weight=20, subsample=0.8, colsample_bytree=0.7, reg_lambda=5.0, reg_alpha=0.5),
        dict(eta=0.03, max_depth=5, min_child_weight=20, subsample=0.8, colsample_bytree=0.7, reg_lambda=5.0, reg_alpha=0.5),
        dict(eta=0.03, max_depth=7, min_child_weight=30, subsample=0.7, colsample_bytree=0.6, reg_lambda=10.0, reg_alpha=1.0),
    ]
    best = {'auc':-1,'params':None,'oof':None,'pred':None,'grid_idx':None,'fold_models':None}
    fnames = list(map(str, X.columns))
    for gi, p in enumerate(grids):
        params = dict(objective='binary:logistic', eval_metric='auc', tree_method='hist',
                      eta=p['eta'], max_depth=p['max_depth'], min_child_weight=p['min_child_weight'],
                      subsample=p['subsample'], colsample_bytree=p['colsample_bytree'],
                      reg_lambda=p['reg_lambda'], reg_alpha=p['reg_alpha'])
        oof_all = np.zeros(len(X)); pred_all = np.zeros(len(X_test))
        fold_models = []
        for seed in SEEDS:
            params['seed']=int(seed)
            skf = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=seed)
            for fold,(tr,va) in enumerate(skf.split(X,y),1):
                dtr = xgb.DMatrix(X.iloc[tr], label=y.iloc[tr], feature_names=fnames)
                dva = xgb.DMatrix(X.iloc[va], label=y.iloc[va], feature_names=fnames)
                dte = xgb.DMatrix(X_test, feature_names=fnames)
                bst = xgb.train(params, dtr, num_boost_round=6000, evals=[(dva,'valid')],
                                early_stopping_rounds=300, verbose_eval=False)
                oof_all[va] = _xgb_predict(bst, dva)
                pred_all += _xgb_predict(bst, dte) / (N_SPLITS*len(SEEDS))
                fold_models.append(bst)
                print(f"[XGB Grid {gi} Fold {fold}] AUC={roc_auc_score(y.iloc[va], oof_all[va]):.6f}")
        auc = roc_auc_score(y, oof_all)
        print(f"[XGB] grid combo AUC={auc:.6f} params={params}")
        if auc>best['auc']:
            best = {'auc':auc,'params':params,'oof':oof_all,'pred':pred_all,'grid_idx':gi,'fold_models':fold_models}
    print(f"Best XGB OOF AUC = {best['auc']:.6f}")
    return best


# ----------------------------
# 主逻辑
# ----------------------------
def main():
    parser = argparse.ArgumentParser(description='训练脚本：仅两个必填位置参数')
    parser.add_argument('trainSetDir', type=str, help='训练数据加载根路径')
    parser.add_argument('modelPath', type=str, help='模型存放路径')
    args = parser.parse_args()

    train_set_dir = args.trainSetDir
    model_dir = args.modelPath
    os.makedirs(model_dir, exist_ok=True)

    # 读取特征
    print(">> 加载特征...")
    train = pd.read_csv(TRAIN_FEAT)
    test  = pd.read_csv(TEST_FEAT)
    assert 'label' in train.columns and 'id' in test.columns

    # 添加银行流水衍生标记
    print(">> 添加银行流水特征...")
    train_bank_path = os.path.join(train_set_dir, 'train_bank_statement.csv')
    test_bank_path  = FIXED_TEST_BANK_PATH
    train, test = add_bank_statement_feature(train, test, train_bank_path, test_bank_path)

    # 准备特征矩阵
    y = train['label'].astype(int)
    X = _select_X(train)
    X_test = _select_X(test)
    feature_names = list(X.columns)

    print(f"特征数: {X.shape[1]} | 训练样本: {len(train)} | 测试样本: {len(test)}")

    # 训练 LGB / XGB（保存候选网格对应折模型）
    print(">> Training LightGBM grid...")
    best_lgb = train_lgbm_cv_with_models(X, y, X_test)

    print(">> Training XGBoost grid...")
    best_xgb = train_xgb_cv_with_models(X, y, X_test)

    # rank 融合（复刻逻辑，基于 OOF 搜索最优 LGB 权重）
    oof_l = best_lgb['oof'] if best_lgb else None
    oof_x = best_xgb['oof']
    weights = np.arange(0.50, 0.80 + 1e-12, 0.05)

    if oof_l is None:
        blend_auc, best_w = roc_auc_score(y, oof_x), 0.0
    else:
        rl = rank_norm(oof_l); rx = rank_norm(oof_x)
        best_auc, best_w = -1, None
        for w in weights:
            s = w*rl + (1-w)*rx
            auc = roc_auc_score(y, s)
            if auc>best_auc:
                best_auc, best_w = auc, float(w)
        blend_auc = best_auc

    print(f">> Blend OOF AUC (rank) = {blend_auc:.6f} | best LGB weight = {best_w:.2f}")

    # 持久化：保存“最优网格下的每折模型”与元信息
    # LGB 模型
    if best_lgb is not None and best_lgb['fold_models']:
        for i, m in enumerate(best_lgb['fold_models'], start=1):
            out_path = os.path.join(model_dir, f"lgb_fold{i}.txt")
            try:
                m.save_model(out_path)
            except Exception as e:
                print(f"[WARN] 保存 LGB 模型失败 fold={i}: {e}")

    # XGB 模型
    if best_xgb is not None and best_xgb['fold_models']:
        for i, bst in enumerate(best_xgb['fold_models'], start=1):
            out_path = os.path.join(model_dir, f"xgb_fold{i}.json")
            try:
                bst.save_model(out_path)
            except Exception as e:
                print(f"[WARN] 保存 XGB 模型失败 fold={i}: {e}")

    # 元信息
    meta = {
        'n_splits': N_SPLITS,
        'seeds': SEEDS,
        'feature_names': feature_names,
        'lgb': {
            'best_auc': float(best_lgb['auc']) if best_lgb else None,
            'params': best_lgb['params'] if best_lgb else None,
            'grid_idx': int(best_lgb['grid_idx']) if best_lgb and best_lgb['grid_idx'] is not None else None,
            'model_files': [f"lgb_fold{i}.txt" for i in range(1, N_SPLITS*len(SEEDS)+1)] if best_lgb else []
        },
        'xgb': {
            'best_auc': float(best_xgb['auc']) if best_xgb else None,
            'params': best_xgb['params'] if best_xgb else None,
            'grid_idx': int(best_xgb['grid_idx']) if best_xgb and best_xgb['grid_idx'] is not None else None,
            'model_files': [f"xgb_fold{i}.json" for i in range(1, N_SPLITS*len(SEEDS)+1)] if best_xgb else []
        },
        'blend': {
            'type': 'rank_weighted',
            'best_lgb_weight': float(best_w),
        },
        'paths': {
            'train_feat': TRAIN_FEAT,
            'test_feat': TEST_FEAT,
        }
    }
    with open(os.path.join(model_dir, 'meta.json'), 'w') as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    print("\n>> 训练已完成，模型与元信息已保存到:")
    print("   ", model_dir)


if __name__ == '__main__':
    main()


