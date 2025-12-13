# -*- coding: utf-8 -*-
"""
Day4 - ADD 批次：银行流水延展统计特征构建
构建银行流水的延展统计特征，包括最近N月统计、趋势特征、变异系数等
与基线特征合并后输出，供后续特征工程使用
"""
import os, json, argparse, numpy as np, pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score

# --------- 默认路径 ---------
DEF_BASE_TRAIN = "./day4/out/sub/train_features_Day4_sub.csv"
DEF_BASE_TEST  = "./day4/out/sub/test_features_Day4_sub.csv"
DEF_TRAIN_MAIN = "../data/train/train.csv"
DEF_TRAIN_BANK = "../data/train/train_bank_statement.csv"
DEF_TEST_MAIN  = "../data/testaa/testaa.csv"
DEF_TEST_BANK  = "../data/testaa/testaa_bank_statement.csv"

# --------- 工具 ---------
def ensure_dir(p): os.makedirs(p, exist_ok=True)
def rank01(a):
    s = pd.Series(a)
    r = s.rank(method="average").to_numpy()
    if r.max() == r.min(): return np.zeros_like(r, dtype=float)
    return (r - r.min()) / (r.max() - r.min())

def safe_div(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    b = np.where(b==0, np.nan, b)
    out = a / b
    return np.nan_to_num(out, nan=0.0, posinf=0.0, neginf=0.0)

# --------- 读入基线 ---------
def load_baseline(base_train, base_test, train_main_path):
    tr = pd.read_csv(base_train)
    te = pd.read_csv(base_test)
    if "label" not in tr.columns:
        lab = pd.read_csv(train_main_path)[["id","label"]]
        tr = tr.merge(lab, on="id", how="left")
    return tr, te

# --------- 流水按月聚合（一次性向量化，很快） ---------
def monthly_agg(bank_df):
    if bank_df is None or len(bank_df)==0:
        return pd.DataFrame({"id":[], "month":[], "income_sum":[], "expense_sum":[], "net_sum":[], "txn_cnt":[]})
    df = bank_df.copy()
    # 统一列名：假定有 id, time(Unix秒), direction(0入1出), amount
    df["time_dt"] = pd.to_datetime(df["time"], unit="s", utc=True).dt.tz_convert(None)
    df["month"]   = df["time_dt"].dt.to_period("M").astype(str)
    inc = df[df["direction"]==0].groupby(["id","month"])["amount"].sum().rename("income_sum")
    exp = df[df["direction"]==1].groupby(["id","month"])["amount"].sum().rename("expense_sum")
    cnt = df.groupby(["id","month"])["amount"].count().rename("txn_cnt")
    per = pd.concat([inc, exp, cnt], axis=1).fillna(0.0)
    per["net_sum"] = per["income_sum"] - per["expense_sum"]
    per = per.reset_index()
    return per

# --------- 生成 ADD 新特征（不与基线重复的“稳健增强”） ---------
def build_add_features(train_main, test_main, train_bank, test_bank):
    # 仅用流水的延展统计 + 少量主表鲁棒比率
    per_tr  = monthly_agg(train_bank)
    per_te  = monthly_agg(test_bank)
    def last_k(per, k):
        # 取每个 id 最近 k 个自然月（按 month 字符排序近似；数据本身是统一时序，不会颠倒）
        if per.empty: return pd.DataFrame({"id":[]})
        per_sorted = per.copy()
        # 用 year*12+month 做序数
        ym = pd.to_datetime(per_sorted["month"]+"-01")
        per_sorted["ym_ord"] = ym.dt.year*12 + ym.dt.month
        per_sorted = per_sorted.sort_values(["id","ym_ord"])
        # 取末尾 k 行再 groupby id 汇总
        def take_tail(df):
            tail = df.tail(k)
            return pd.Series({
                f"add_inc_sum_last{k}":  tail["income_sum"].sum(),
                f"add_exp_sum_last{k}":  tail["expense_sum"].sum(),
                f"add_net_sum_last{k}":  tail["net_sum"].sum(),
                f"add_inc_mean_last{k}": tail["income_sum"].mean(),
                f"add_exp_mean_last{k}": tail["expense_sum"].mean(),
                f"add_net_mean_last{k}": tail["net_sum"].mean(),
                f"add_txn_cnt_last{k}":  tail["txn_cnt"].sum(),
            })
        g = per_sorted.groupby("id").apply(take_tail).reset_index()
        return g

    def slope_feats(per):
        if per.empty: return pd.DataFrame({"id":[]})
        per2 = per.copy()
        ym = pd.to_datetime(per2["month"]+"-01")
        per2["t"] = (ym.dt.year*12 + ym.dt.month) - (ym.dt.year.min()*12 + ym.dt.month.min())
        def linfit(df):
            t = df["t"].to_numpy()
            out = {}
            for col in ["income_sum","expense_sum","net_sum"]:
                y = df[col].to_numpy()
                if len(t)>=2 and np.std(t)>0 and np.std(y)>0:
                    a, b = np.polyfit(t, y, 1)
                else:
                    a = 0.0
                out[f"add_slope_{col}"] = a
            return pd.Series(out)
        return per2.groupby("id").apply(linfit).reset_index()

    def cv_feats(per):
        if per.empty: return pd.DataFrame({"id":[]})
        def f(df):
            out={}
            for col in ["income_sum","expense_sum","net_sum"]:
                m = df[col].mean(); s=df[col].std()
                out[f"add_cv_{col}"] = (s/m) if (m and m!=0) else 0.0
            out["add_neg_month_share"] = (df["net_sum"]<0).mean()
            return pd.Series(out)
        return per.groupby("id").apply(f).reset_index()

    tr_last3 = last_k(per_tr, 3)
    tr_last6 = last_k(per_tr, 6)
    te_last3 = last_k(per_te, 3)
    te_last6 = last_k(per_te, 6)

    tr_slope  = slope_feats(per_tr);  te_slope  = slope_feats(per_te)
    tr_cv     = cv_feats(per_tr);     te_cv     = cv_feats(per_te)

    # 主表鲁棒比率（不重复 S1 原列名）
    def robust_main(main):
        df = main.copy()
        out = df[["id"]].copy()
        # 这些原始列在主表：balance, balance_limit, loan, installment（installment 是 0/1?
        # 保险起见都做存在性判断
        for a,b,name in [
            ("balance","balance_limit","add_utilization_rb"),
            ("loan",   "balance_limit","add_loan_to_limit"),
        ]:
            if a in df.columns and b in df.columns:
                out[name] = safe_div(df[a], df[b]+1e-6)
        return out

    tr_main_rb = robust_main(train_main)
    te_main_rb = robust_main(test_main)

    add_tr = tr_main_rb.merge(tr_last3, on="id", how="left")\
                       .merge(tr_last6, on="id", how="left")\
                       .merge(tr_slope,  on="id", how="left")\
                       .merge(tr_cv,     on="id", how="left")
    add_te = te_main_rb.merge(te_last3, on="id", how="left")\
                       .merge(te_last6, on="id", how="left")\
                       .merge(te_slope,  on="id", how="left")\
                       .merge(te_cv,     on="id", how="left")
    add_tr = add_tr.fillna(0.0); add_te = add_te.fillna(0.0)
    return add_tr, add_te

# --------- 快速扫描（基于 OOF 级别的加权秩融合，极快） ---------
def fast_scan_select(baseline_oof, y, add_tr_df, min_gain=0.0002, max_keep=20):
    base_r = rank01(baseline_oof)
    cand_cols = [c for c in add_tr_df.columns if c!="id"]
    gains = []
    for c in cand_cols:
        r = rank01(add_tr_df[c].to_numpy())
        best, best_w = -1.0, None
        for w in np.arange(0.05, 0.55, 0.05):
            auc = roc_auc_score(y, base_r + w*r)
            if auc > best:
                best, best_w = auc, float(w)
        gains.append((c, best - roc_auc_score(y, base_r), best_w, best))
    gains = sorted(gains, key=lambda x: x[3], reverse=True)

    # 贪心：逐个加入，只有在在当前组合上仍有 >= min_gain 才收
    selected, weights = [], []
    cur = base_r.copy()
    cur_auc = roc_auc_score(y, cur)
    for c, _, w, _auc in gains:
        r = rank01(add_tr_df[c].to_numpy())
        try_auc = roc_auc_score(y, cur + w*r)
        if try_auc - cur_auc >= min_gain:
            selected.append(c); weights.append(w)
            cur = cur + w*r
            cur_auc = try_auc
            if len(selected) >= max_keep: break

    report = pd.DataFrame(gains, columns=["feature","delta_vs_base","best_weight","cand_auc"])
    return selected, weights, cur_auc, report

# --------- 主流程 ---------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base_train", default=DEF_BASE_TRAIN)
    ap.add_argument("--base_test",  default=DEF_BASE_TEST)
    ap.add_argument("--train_main", default=DEF_TRAIN_MAIN)
    ap.add_argument("--train_bank", default=DEF_TRAIN_BANK)
    ap.add_argument("--test_main",  default=DEF_TEST_MAIN)
    ap.add_argument("--test_bank",  default=DEF_TEST_BANK)
    ap.add_argument("--out_root",   default="./day4")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    dir_add  = os.path.join(args.out_root, "add_out"); ensure_dir(dir_add)
    dir_merge= os.path.join(args.out_root, "merged");  ensure_dir(dir_merge)
    dir_scan = os.path.join(args.out_root, "scan");    ensure_dir(dir_scan)
    dir_final= os.path.join(args.out_root, "final");   ensure_dir(dir_final)

    # 1) 读取基线
    base_tr, base_te = load_baseline(args.base_train, args.base_test, args.train_main)
    y = base_tr["label"].astype(int)
    base_feat_cols = [c for c in base_tr.columns if c not in ["id","label"]]

    # 2) 读原始数据
    tr_main = pd.read_csv(args.train_main)
    te_main = pd.read_csv(args.test_main)
    tr_bank = pd.read_csv(args.train_bank)
    te_bank = pd.read_csv(args.test_bank)

    # 3) 构建 ADD 新特征
    add_tr, add_te = build_add_features(tr_main, te_main, tr_bank, te_bank)
    add_tr.to_csv(os.path.join(dir_add, "features_add_train.csv"), index=False)
    add_te.to_csv(os.path.join(dir_add, "features_add_test.csv"), index=False)

    # 4) 与基线拼接（避免重名：只保留 add_* 前缀）
    add_cols = [c for c in add_tr.columns if c!="id"]
    tr_merged = base_tr.merge(add_tr, on="id", how="left")
    te_merged = base_te.merge(add_te, on="id", how="left")
    tr_merged[add_cols] = tr_merged[add_cols].fillna(0.0)
    te_merged[add_cols] = te_merged[add_cols].fillna(0.0)
    tr_merged.to_csv(os.path.join(dir_merge, "add_merged_train.csv"), index=False)
    te_merged.to_csv(os.path.join(dir_merge, "add_merged_test.csv"), index=False)
    
    print("== DONE ADD ==")

if __name__ == "__main__":
    main()