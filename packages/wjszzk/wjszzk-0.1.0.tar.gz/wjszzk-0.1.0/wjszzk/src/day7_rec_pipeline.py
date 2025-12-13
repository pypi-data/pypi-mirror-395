"""
Day7 - REC (Recency & Robustness) 特征批次
构建基于时间近因性和鲁棒性的特征，包括：
1) 时间近因性特征：最近N月活跃度、交易频率、金额趋势
2) 鲁棒性特征：异常值处理、稳定性指标、风险缓冲
3) 行为模式特征：交易习惯、时间偏好、金额分布
与基线特征合并后输出，供后续特征工程使用
"""


import os
import json
import argparse
import numpy as np
import pandas as pd
from collections import defaultdict

# ----------------------------
# 小工具
# ----------------------------
def ensure_dir(p: str):
    os.makedirs(p, exist_ok=True)

def read_csv(path: str):
    return pd.read_csv(path)

def month_floor(s: pd.Series):
    dt = pd.to_datetime(s, errors="coerce")
    return pd.to_datetime(dt.dt.to_period("M").dt.to_timestamp())

def rank01(x: np.ndarray):
    r = pd.Series(x).rank(method="average").to_numpy()
    return (r - r.min()) / max(1e-12, (r.max() - r.min()))

# ----------------------------
# 月度表：按 id, month 聚合出 income / expense / net / txn_count / max_amt
# ----------------------------
def monthly_table(bank_df: pd.DataFrame) -> pd.DataFrame:
    if len(bank_df) == 0:
        return pd.DataFrame(columns=["id","month","income_sum","expense_sum","net_sum","txn_count","max_amt"])
    tmp = bank_df.copy()
    # 猜测字段：id, amount, time（或 date）
    # 兼容 time/date 两种命名
    if "time" in tmp.columns:
        tmp["month"] = month_floor(tmp["time"])
    elif "date" in tmp.columns:
        tmp["month"] = month_floor(tmp["date"])
    else:
        raise ValueError("bank_statement 必须包含 time 或 date 列")

    amt = tmp["amount"].astype(float)
    tmp["income"]  = np.where(amt > 0,  amt, 0.0)
    tmp["expense"] = np.where(amt < 0, -amt, 0.0)
    tmp["net"]     = amt

    g = tmp.groupby(["id","month"], as_index=False).agg(
        income_sum = ("income","sum"),
        expense_sum= ("expense","sum"),
        net_sum    = ("net","sum"),
        txn_count  = ("amount","size"),
        max_amt    = ("amount", lambda x: np.max(np.abs(x)) if len(x) else 0.0),
    )
    return g

# ----------------------------
# Day7-REC 新特征构建（核心）
# ----------------------------
def build_rec_features(tr_main, te_main, tr_bank, te_bank) -> tuple[pd.DataFrame, pd.DataFrame]:
    mtr = monthly_table(tr_bank)
    mte = monthly_table(te_bank)

    def _per_id_feats(m: pd.DataFrame) -> pd.DataFrame:
        if len(m) == 0:
            return pd.DataFrame(columns=["id"])  # 空
        m = m.sort_values(["id","month"])
        feats = []

        for uid, g in m.groupby("id", sort=False):
            inc = g["income_sum"].to_numpy()
            exp = g["expense_sum"].to_numpy()
            net = g["net_sum"].to_numpy()

            k = len(g)
            # 1) 近因加权（指数衰减）
            #    w_t = decay^(T-1-t), decay取0.8；越近月权重越大
            idx = np.arange(k)
            w = (0.8 ** (k - 1 - idx)).astype(float)
            w /= max(1e-12, w.sum())
            ew_inc = float((inc * w).sum())
            ew_exp = float((exp * w).sum())
            ew_net = float((net * w).sum())

            # 2) 零占比 + 正负净值占比
            zero_inc_share = float(np.mean(inc <= 1e-9))
            zero_exp_share = float(np.mean(exp <= 1e-9))
            pos_net_share  = float(np.mean(net >  1e-9))
            neg_net_share  = float(np.mean(net < -1e-9))

            # 3) 最长正/负净值连续月数
            def longest_streak(x, cond):
                best = cur = 0
                for v in x:
                    if cond(v):
                        cur += 1
                        best = max(best, cur)
                    else:
                        cur = 0
                return best
            streak_pos = int(longest_streak(net, lambda v: v > 1e-9))
            streak_neg = int(longest_streak(net, lambda v: v < -1e-9))

            # 4) 环比波动（MAD/mean）
            def mad_over_mean(arr):
                if len(arr) <= 1:
                    return 0.0
                diff = np.diff(arr)
                mad = np.mean(np.abs(diff))
                mean = np.mean(np.abs(arr)) + 1e-9
                return float(mad / mean)
            mom_inc_mad = mad_over_mean(inc)
            mom_exp_mad = mad_over_mean(exp)
            mom_net_mad = mad_over_mean(net)

            # 5) 近3月 vs 全局
            last3 = slice(max(0, k-3), k)
            r_income = float(np.mean(inc[last3]) / (np.mean(inc) + 1e-9))
            r_expense= float(np.mean(exp[last3]) / (np.mean(exp) + 1e-9))
            r_net    = float(np.mean(net[last3]) / (np.mean(net) + 1e-9))

            feats.append({
                "id": uid,
                "day7_ew_income": ew_inc,
                "day7_ew_expense": ew_exp,
                "day7_ew_net": ew_net,
                "day7_zero_income_share": zero_inc_share,
                "day7_zero_expense_share": zero_exp_share,
                "day7_pos_net_share": pos_net_share,
                "day7_neg_net_share": neg_net_share,
                "day7_streak_pos": streak_pos,
                "day7_streak_neg": streak_neg,
                "day7_mom_income_mad": mom_inc_mad,
                "day7_mom_expense_mad": mom_exp_mad,
                "day7_mom_net_mad": mom_net_mad,
                "day7_r3_overall_income": r_income,
                "day7_r3_overall_expense": r_expense,
                "day7_r3_overall_net": r_net,
                "day7_months_active": k,
            })

        return pd.DataFrame(feats)

    ftr = _per_id_feats(mtr)
    fte = _per_id_feats(mte)

    # 补齐 id，避免 merge 丢行
    ftr = tr_main[["id"]].merge(ftr, on="id", how="left").fillna(0.0)
    fte = te_main[["id"]].merge(fte, on="id", how="left").fillna(0.0)
    return ftr, fte



# ----------------------------
# 主流程
# ----------------------------
def main():
    parser = argparse.ArgumentParser()
    # 原始数据（与 add 一致）
    parser.add_argument("--train_main", type=str, default="../data/train/train.csv")
    parser.add_argument("--test_main",  type=str, default="../data/testaa/testaa.csv")
    parser.add_argument("--train_bank", type=str, default="../data/train/train_bank_statement.csv")
    parser.add_argument("--test_bank",  type=str, default="../data/testaa/testaa_bank_statement.csv")
    # 基线大表（与 add/mul 一致，默认接 Day4_sub）
    parser.add_argument("--base_train", type=str, default="./day4/out/sub/train_features_Day4_sub.csv")
    parser.add_argument("--base_test",  type=str, default="./day4/out/sub/test_features_Day4_sub.csv")
    # 输出目录（与 add/mul 风格保持一致的子结构）
    parser.add_argument("--out_dir", type=str, default="./day7/out")
    
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    # 目录
    dir_rec   = os.path.join(args.out_dir, "rec");    ensure_dir(dir_rec)
    dir_merge = os.path.join(args.out_dir, "merged");  ensure_dir(dir_merge)
    dir_eval  = os.path.join(args.out_dir, "eval");   ensure_dir(dir_eval)

    print("== [1/3] 读取数据 ==")
    tr_main = read_csv(args.train_main)
    te_main = read_csv(args.test_main)
    tr_bank = read_csv(args.train_bank)
    te_bank = read_csv(args.test_bank)
    base_tr = read_csv(args.base_train)
    base_te = read_csv(args.base_test)

    print("== [2/3] 构建 Day7-REC 新特征 ==")
    rec_tr, rec_te = build_rec_features(tr_main, te_main, tr_bank, te_bank)
    rec_tr.to_csv(os.path.join(dir_rec, "features_rec_train.csv"), index=False)
    rec_te.to_csv(os.path.join(dir_rec, "features_rec_test.csv"),  index=False)
    print(f"Saved: {os.path.join(dir_rec, 'features_rec_train.csv')}  /  {os.path.join(dir_rec, 'features_rec_test.csv')}")

    print("== [3/3] 与基线合并 ==")
    add_cols = [c for c in rec_tr.columns if c != "id"]
    merged_tr = base_tr.merge(rec_tr, on="id", how="left")
    merged_te = base_te.merge(rec_te, on="id", how="left")
    merged_tr[add_cols] = merged_tr[add_cols].fillna(0.0)
    merged_te[add_cols] = merged_te[add_cols].fillna(0.0)
    merged_tr.to_csv(os.path.join(dir_merge, "rec_merged_train.csv"), index=False)
    merged_te.to_csv(os.path.join(dir_merge, "rec_merged_test.csv"), index=False)
    print(f"Saved: {os.path.join(dir_merge, 'rec_merged_train.csv')}  /  {os.path.join(dir_merge, 'rec_merged_test.csv')}")


    print("== DONE Day7-REC ==")

if __name__ == "__main__":
    main()