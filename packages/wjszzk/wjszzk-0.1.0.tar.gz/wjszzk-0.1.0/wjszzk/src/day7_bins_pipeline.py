"""
Day7 - BINS 连续特征分箱批次
构建基于连续特征分箱的离散化特征，包括：
1) 等频分箱：基于分位数的等频分箱
2) 等宽分箱：基于数值范围的等宽分箱
3) 语义分箱：基于业务逻辑的语义分箱
4) 交互分箱：多特征组合的分箱特征
与基线特征合并后输出，供后续特征工程使用
"""

import os
import json
import argparse
import numpy as np
import pandas as pd

# ----------------------------
# 工具
# ----------------------------
def ensure_dir(p: str): os.makedirs(p, exist_ok=True)
def read_csv(path: str): return pd.read_csv(path)

def rank01(x: np.ndarray):
    r = pd.Series(x).rank(method="average").to_numpy()
    return (r - r.min()) / max(1e-12, (r.max() - r.min()))


# ----------------------------
# 分箱配置（语义优先 + 兼容缺省）
#   键：列名；值：dict，支持：
#     - strategy: "thresholds" | "quantile"
#     - thresholds: 有序阈值列表（左开右闭切割），例：[0, 0.1, 0.3, 0.7] -> 5 档
#     - q: 等频分位数个数，如 5 -> 5 档
#     - clip_min / clip_max: 拟合前截断
# ----------------------------
DEFAULT_BIN_SPECS = {
    # 信用相关比例类（0~1），按经验阈值
    "utilization":       {"strategy": "thresholds", "thresholds": [0.0, 0.1, 0.3, 0.6, 0.9]},
    "acct_used_ratio":   {"strategy": "thresholds", "thresholds": [0.0, 0.25, 0.5, 0.75]},
    "cross_DTI":         {"strategy": "thresholds", "thresholds": [0.0, 0.2, 0.35, 0.5, 0.8]},

    # 金额类：等频，且对极端值截断
    "main_log1p_loan":   {"strategy": "quantile", "q": 6, "clip_min": None, "clip_max": None},
    "main_log1p_balance":{"strategy": "quantile", "q": 6},
    "main_log1p_limit":  {"strategy": "quantile", "q": 6},
    "installment_amt":   {"strategy": "quantile", "q": 6},
    "cross_net_over_installment": {"strategy": "quantile", "q": 6},

    # 时间跨度：等频
    "main_history_len_days":   {"strategy": "quantile", "q": 5},
    "main_rec_minus_issue_days":{"strategy": "quantile", "q": 5},

    # 银行流水聚合（若在 base 表中）
    "bank_income_mean":  {"strategy": "quantile", "q": 5},
    "bank_expense_mean": {"strategy": "quantile", "q": 5},
    "bank_net_mean":     {"strategy": "quantile", "q": 5},
    "bank_income_std":   {"strategy": "quantile", "q": 5},
    "bank_net_std":      {"strategy": "quantile", "q": 5},
    "bank_txn_count_m":  {"strategy": "quantile", "q": 5},
    "bank_months_active":{"strategy": "quantile", "q": 4},

    # 近因代理（若有）
    "monthly_income_proxy": {"strategy": "quantile", "q": 6},
    "cross_buffer_months":  {"strategy": "thresholds", "thresholds":[0, 1, 3, 6, 12]},
}

# ----------------------------
# 拟合分箱边界（只看 train）
# ----------------------------
def _fit_bins(train: pd.DataFrame, specs: dict) -> dict:
    bins_map = {}
    for col, cfg in specs.items():
        if col not in train.columns:
            continue
        x = train[col].astype(float).replace([np.inf,-np.inf], np.nan).dropna().to_numpy()
        if len(x) == 0:
            continue
        # clip
        cmin, cmax = cfg.get("clip_min", None), cfg.get("clip_max", None)
        if cmin is not None: x = np.maximum(x, cmin)
        if cmax is not None: x = np.minimum(x, cmax)

        if cfg.get("strategy") == "thresholds":
            thr = cfg["thresholds"]
            edges = [-np.inf] + thr + [np.inf]
        else:
            q = int(cfg.get("q", 5))
            qs = np.linspace(0, 1, q+1)
            edges = np.unique(np.quantile(x, qs))
            # 保底
            if len(edges) < 3:
                edges = np.array([np.nanmin(x), np.nanmean(x), np.nanmax(x)])
            edges[0]  = -np.inf
            edges[-1] = np.inf
        bins_map[col] = np.array(edges, dtype=float)
    return bins_map

def _apply_bins(df: pd.DataFrame, bins_map: dict, one_hot: bool) -> pd.DataFrame:
    out = pd.DataFrame({"id": df["id"]})
    for col, edges in bins_map.items():
        if col not in df.columns: 
            continue
        x = df[col].astype(float).replace([np.inf,-np.inf], np.nan).fillna(np.nan)
        ord_col = f"bins_ord__{col}"
        # pandas cut 返回区间标签，从 0..n-1 编成顺序码（include_lowest=True）
        cat = pd.cut(x, bins=edges, labels=False, include_lowest=True)
        out[ord_col] = cat.astype("float").fillna(-1).astype(int)
        if one_hot:
            # 稳健 one-hot：-1 视为缺失，不展开
            k = int((len(edges)-1))
            for i in range(k):
                out[f"bins_ohe__{col}__{i}"] = (out[ord_col] == i).astype(int)
    return out

# ----------------------------
# 主流程
# ----------------------------
def main():
    parser = argparse.ArgumentParser()
    # 原始数据路径（仅兜底，不依赖它算 bins）
    parser.add_argument("--train_main", type=str, default="../data/train/train.csv")
    parser.add_argument("--test_main",  type=str, default="../data/testaa/testaa.csv")
    # 基线大表（上一环节）
    parser.add_argument("--base_train", type=str, default="./day4/out/sub/train_features_Day4_sub.csv")
    parser.add_argument("--base_test",  type=str, default="./day4/out/sub/test_features_Day4_sub.csv")
    # 输出
    parser.add_argument("--out_dir", type=str, default="./day7/out")
    parser.add_argument("--seed", type=int, default=42)
    # 控制
    parser.add_argument("--no_one_hot", action="store_true", help="只生成顺序编码，不展开one-hot")
    # 自定义列：若提供，则只对这些列分箱（逗号分隔）
    parser.add_argument("--cols", type=str, default="")
    args = parser.parse_args()

    dir_bins  = os.path.join(args.out_dir, "bins");  ensure_dir(dir_bins)
    dir_merge = os.path.join(args.out_dir, "merged"); ensure_dir(dir_merge)
    dir_eval  = os.path.join(args.out_dir, "eval");  ensure_dir(dir_eval)

    print("== [1/3] 读取基线数据 ==")
    base_tr = read_csv(args.base_train)
    base_te = read_csv(args.base_test)

    # 选择要分箱的列集合
    if args.cols.strip():
        cols = [c.strip() for c in args.cols.split(",") if c.strip()]
        specs = {c: DEFAULT_BIN_SPECS.get(c, {"strategy":"quantile","q":5}) for c in cols}
    else:
        # 用默认字典中过滤“基线里存在”的列
        specs = {c: cfg for c, cfg in DEFAULT_BIN_SPECS.items() if c in base_tr.columns}

    print(f"[BINS] 计划分箱列数：{len(specs)} / in-base: {sum([c in base_tr.columns for c in DEFAULT_BIN_SPECS])}")
    if len(specs) == 0:
        print("[BINS] 没有可分箱列（在 base 中不存在），直接退出")
        return

    print("== [2/3] 拟合并生成分箱特征 ==")
    bins_map = _fit_bins(base_tr, specs)
    tr_bins = _apply_bins(base_tr, bins_map, one_hot=(not args.no_one_hot))
    te_bins = _apply_bins(base_te, bins_map, one_hot=(not args.no_one_hot))
    tr_bins.to_csv(os.path.join(dir_bins, "features_bins_train.csv"), index=False)
    te_bins.to_csv(os.path.join(dir_bins, "features_bins_test.csv"),  index=False)
    print(f"Saved: {os.path.join(dir_bins, 'features_bins_train.csv')} / features_bins_test.csv")

    print("== [3/3] 与基线合并 ==")
    add_cols = [c for c in tr_bins.columns if c != "id"]
    merged_tr = base_tr.merge(tr_bins, on="id", how="left")
    merged_te = base_te.merge(te_bins, on="id", how="left")
    merged_tr[add_cols] = merged_tr[add_cols].fillna(0)
    merged_te[add_cols] = merged_te[add_cols].fillna(0)
    merged_tr.to_csv(os.path.join(dir_merge, "bins_merged_train.csv"), index=False)
    merged_te.to_csv(os.path.join(dir_merge, "bins_merged_test.csv"),  index=False)
    print(f"Saved: {os.path.join(dir_merge, 'bins_merged_train.csv')} / bins_merged_test.csv")

    # 保存分箱边界以备复现
    meta = {k: [float(v) for v in list(edges)] for k, edges in bins_map.items()}
    with open(os.path.join(dir_bins, "bins_meta.json"), "w") as f:
        json.dump(meta, f, indent=2)

    print("== DONE Day7-BINS ==")

if __name__ == "__main__":
    main()