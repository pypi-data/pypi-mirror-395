#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提交制式测试脚本：
用法：
  python3 test.py testSetDir resultPath

说明：
- 仅接受两个位置参数：测试数据根目录（仅用于定位模型目录或流水）、结果保存目录；其余路径与参数全部写死。
- 加载训练脚本保存的模型（LightGBM / XGBoost 每折模型）与融合权重，基于固定的特征表进行推理，输出 result.csv。
"""

import os
import sys
import argparse
import json
import numpy as np
import pandas as pd


# 相对 code/ 目录的固定特征路径
FEATURE_DIR = os.path.join("..", "temp_data", "features", "day11_team_out", "merged")
TEST_FEAT  = os.path.join(FEATURE_DIR, "team_merged_test.csv")
# 固定测试集银行流水路径（按初赛B榜目录结构），相对 code/ 目录
TEST_BANK_PATH = os.path.join("..", "init_data", "初赛B榜数据集", "testab", "testab_bank_statement.csv")


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


def add_bank_statement_feature_test(test_df: pd.DataFrame, test_bank_statement_path: str) -> pd.DataFrame:
    if test_bank_statement_path and os.path.exists(test_bank_statement_path):
        test_bank_data = pd.read_csv(test_bank_statement_path)
        test_users_with_bank = set(test_bank_data['id'].unique())
        test_df['is_bank_statement'] = test_df['id'].isin(test_users_with_bank).astype(int)
    else:
        test_df['is_bank_statement'] = 0
    return test_df


def load_models(model_dir: str, meta: dict):
    models = {'lgb': [], 'xgb': []}
    # LGB
    try:
        import lightgbm as lgb
        for fname in meta.get('lgb', {}).get('model_files', []):
            path = os.path.join(model_dir, fname)
            if os.path.exists(path):
                models['lgb'].append(lgb.Booster(model_file=path))
    except Exception as e:
        print(f"[WARN] 无法加载 LightGBM: {e}")
    # XGB
    try:
        import xgboost as xgb
        for fname in meta.get('xgb', {}).get('model_files', []):
            path = os.path.join(model_dir, fname)
            if os.path.exists(path):
                bst = xgb.Booster()
                bst.load_model(path)
                models['xgb'].append(bst)
    except Exception as e:
        print(f"[WARN] 无法加载 XGBoost: {e}")
    return models


def predict(models: dict, X_test: pd.DataFrame, feature_names: list, weight_lgb: float) -> np.ndarray:
    # 对齐列顺序
    X_test = X_test[feature_names]

    preds_lgb = None
    if models['lgb']:
        import lightgbm as lgb
        p = np.zeros(len(X_test))
        for m in models['lgb']:
            p += m.predict(X_test, num_iteration=m.best_iteration) / len(models['lgb'])
        preds_lgb = p

    preds_xgb = None
    if models['xgb']:
        import xgboost as xgb
        dte = xgb.DMatrix(X_test, feature_names=list(map(str, X_test.columns)))
        p = np.zeros(len(X_test))
        for bst in models['xgb']:
            if hasattr(bst, "best_iteration") and bst.best_iteration is not None:
                p += bst.predict(dte, iteration_range=(0, bst.best_iteration+1)) / len(models['xgb'])
            elif hasattr(bst, "best_ntree_limit") and getattr(bst, "best_ntree_limit", None):
                p += bst.predict(dte, ntree_limit=bst.best_ntree_limit) / len(models['xgb'])
            else:
                p += bst.predict(dte) / len(models['xgb'])
        preds_xgb = p

    # rank 融合（与训练一致）
    if preds_lgb is None:
        return preds_xgb
    if preds_xgb is None:
        return preds_lgb
    return weight_lgb * rank_norm(preds_lgb) + (1.0 - weight_lgb) * rank_norm(preds_xgb)


def main():
    parser = argparse.ArgumentParser(description='测试脚本：仅两个必填位置参数')
    parser.add_argument('testSetDir', type=str, help='测试数据加载根路径或模型目录')
    parser.add_argument('resultPath', type=str, help='结果生成路径')
    args = parser.parse_args()

    test_set_dir = args.testSetDir
    result_dir = args.resultPath
    os.makedirs(result_dir, exist_ok=True)

    # 加载元信息：优先使用 testSetDir；否则尝试常见备选目录
    candidates = [
        test_set_dir,
        os.path.join(os.getcwd(), 'models'),
        os.path.join(os.getcwd(), 'model'),
        os.path.join(os.getcwd(), 'result'),
        os.path.join(os.getcwd(), 'saved_models'),
    ]
    model_dir = None
    meta_path = None
    for d in candidates:
        p = os.path.join(d, 'meta.json')
        if os.path.exists(p):
            model_dir = d
            meta_path = p
            break
    if meta_path is None:
        print("未找到模型元信息(meta.json)，请将模型目录作为 testSetDir 传入或放置于 ./models 下")
        sys.exit(1)

    with open(meta_path, 'r') as f:
        meta = json.load(f)

    # 读取特征并补齐与训练一致的衍生列
    test = pd.read_csv(TEST_FEAT)
    test = add_bank_statement_feature_test(test, TEST_BANK_PATH)
    X_test = _select_X(test)

    # 加载模型
    models = load_models(model_dir, meta)
    weight_lgb = float(meta.get('blend', {}).get('best_lgb_weight', 0.0))
    feature_names = meta.get('feature_names', list(X_test.columns))

    # 预测
    pred = predict(models, X_test, feature_names, weight_lgb)

    # 输出 result.csv
    out_path = os.path.join(result_dir, 'result.csv')
    pd.DataFrame({'id': test['id'], 'label': pred}).to_csv(out_path, index=False)
    print("已保存:", out_path)


if __name__ == '__main__':
    main()


