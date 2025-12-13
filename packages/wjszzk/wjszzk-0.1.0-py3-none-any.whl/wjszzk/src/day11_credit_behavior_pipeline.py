#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day11 - CREDIT_BEHAVIOR 授信与使用行为（业务特征）
输入：包含主表+基础流水聚合的大表
输出：out/day11_credit_out/features_credit_{train,test}.csv 与 merged/credit_merged_{train,test}.csv

前缀：credbeh_*
"""

import os
import argparse
import numpy as np
import pandas as pd


def ensure_dir(p: str):
    os.makedirs(p, exist_ok=True)


def read_csv(p: str) -> pd.DataFrame:
    return pd.read_csv(p)


def safe_div(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    return np.where(b != 0, a / b, 0.0)


def build_credit_behavior(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    bal_limit = out.get("raw_balance_limit", out.get("balance_limit", pd.Series(0.0, index=out.index)))
    bal = out.get("raw_balance", out.get("balance", pd.Series(0.0, index=out.index)))
    total_accts = out.get("raw_total_accounts", out.get("total_accounts", pd.Series(0.0, index=out.index)))
    used_accts = out.get("raw_balance_accounts", out.get("balance_accounts", pd.Series(0.0, index=out.index)))
    loan_raw = out.get("raw_loan", out.get("loan", pd.Series(0.0, index=out.index)))
    interest = out.get("raw_interest_rate", out.get("interest_rate", pd.Series(0.0, index=out.index)))
    term = out.get("raw_term", out.get("term", pd.Series(0.0, index=out.index)))

    # 利用率与账户使用行为
    out["credbeh_utilization"] = safe_div(bal, bal_limit)
    out["credbeh_acct_used_ratio"] = safe_div(used_accts, total_accts)
    out["credbeh_avg_balance_per_acct"] = safe_div(bal, total_accts)

    # 授信变化速率代理（issue->record 时间上不可直接得出，给出保底代理）
    # 仍保证与既有 utilization 等基础列名不重复
    out["credbeh_util_over_acct_ratio"] = safe_div(out["credbeh_utilization"], out["credbeh_acct_used_ratio"] + 1e-9)

    # 贷款规模与授信结构耦合
    out["credbeh_loan_over_limit"] = safe_div(loan_raw, bal_limit)
    out["credbeh_loan_over_balance"] = safe_div(loan_raw, bal)

    # 利率/期限暴露与职业/居住地交互（业务暴露）
    if "level_ord" in out.columns:
        out["credbeh_level_term_exposure"] = out["level_ord"].astype(float) * (term.astype(float))
        out["credbeh_level_rate_exposure"] = out["level_ord"].astype(float) * (interest.astype(float))
    else:
        out["credbeh_level_term_exposure"] = term.astype(float)
        out["credbeh_level_rate_exposure"] = interest.astype(float)

    # 稳健裁剪
    num_cols = [c for c in out.columns if out[c].dtype.kind in ("i", "u", "f") and c not in ("id", "label")]
    for c in num_cols:
        q01, q99 = out[c].quantile(0.01), out[c].quantile(0.99)
        out[c] = out[c].clip(q01, q99)

    return out


def main():
    ap = argparse.ArgumentParser(description="Day11 CREDIT_BEHAVIOR 特征构建")
    ap.add_argument("--base_train", required=True)
    ap.add_argument("--base_test", required=True)
    ap.add_argument("--out_root", required=True)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    np.random.seed(args.seed)
    ensure_dir(args.out_root)
    ensure_dir(f"{args.out_root}/features")
    ensure_dir(f"{args.out_root}/merged")

    tr = read_csv(args.base_train)
    te = read_csv(args.base_test)

    tr_o = build_credit_behavior(tr)
    te_o = build_credit_behavior(te)

    tr_o.to_csv(f"{args.out_root}/features/features_credit_train.csv", index=False)
    te_o.to_csv(f"{args.out_root}/features/features_credit_test.csv", index=False)

    tr_o.to_csv(f"{args.out_root}/merged/credit_merged_train.csv", index=False)
    te_o.to_csv(f"{args.out_root}/merged/credit_merged_test.csv", index=False)

    print("[OK] Day11 CREDIT_BEHAVIOR 构建完成")


if __name__ == "__main__":
    main()


