#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day11 - BEHAVIOR_FLAGS 行为风险信号（业务特征）
输入：包含主表+基础流水聚合的大表
输出：out/day11_bhv_out/features_bhv_{train,test}.csv 与 merged/bhv_merged_{train,test}.csv

前缀：bhvflag_*
"""

import os
import argparse
import numpy as np
import pandas as pd


def ensure_dir(p: str):
    os.makedirs(p, exist_ok=True)


def read_csv(p: str) -> pd.DataFrame:
    return pd.read_csv(p)


def build_bhv(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    # 末期突变代理：有 time_recent_vs_hist_amount 列则复用；否则以 bank_* 近似
    if "time_recent_vs_hist_amount" in out.columns:
        out["bhvflag_recent_amount_drop"] = -out["time_recent_vs_hist_amount"].astype(float)
    else:
        # 用 net_last - net_mean 近似下跌
        if {"bank_net_last", "bank_net_mean"}.issubset(out.columns):
            out["bhvflag_recent_amount_drop"] = (out["bank_net_mean"].astype(float) - out["bank_net_last"].astype(float))
        else:
            out["bhvflag_recent_amount_drop"] = 0.0

    # 交易密度突变：无 time_* 时提供占位
    if {"time_active_days", "time_total_days"}.issubset(out.columns):
        ratio = (out["time_active_days"].astype(float) / (out["time_total_days"].astype(float) + 1e-9))
        out["bhvflag_density_drop"] = (ratio.median() - ratio).clip(lower=0)
    else:
        out["bhvflag_density_drop"] = 0.0

    # 不活跃标记：若 bank_months_active 很低
    if "bank_months_active" in out.columns:
        out["bhvflag_low_activity"] = (out["bank_months_active"].astype(float) < 2).astype(int)
    else:
        out["bhvflag_low_activity"] = 0

    # 连续负月代理（复用）
    if "bank_neg_periods" in out.columns:
        out["bhvflag_many_neg_periods"] = (out["bank_neg_periods"].astype(float) >= 2).astype(int)
    else:
        out["bhvflag_many_neg_periods"] = 0

    # 临近大额支出风险（无明细则用 bank_expense_p95 近似占位）
    if "bank_expense_p95" in out.columns:
        out["bhvflag_large_expense_risk"] = (out["bank_expense_p95"].astype(float) > out["bank_expense_p95"].median()).astype(int)
    else:
        out["bhvflag_large_expense_risk"] = 0

    return out


def main():
    ap = argparse.ArgumentParser(description="Day11 BEHAVIOR_FLAGS 特征构建")
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

    tr_o = build_bhv(tr)
    te_o = build_bhv(te)

    tr_o.to_csv(f"{args.out_root}/features/features_bhv_train.csv", index=False)
    te_o.to_csv(f"{args.out_root}/features/features_bhv_test.csv", index=False)

    tr_o.to_csv(f"{args.out_root}/merged/bhv_merged_train.csv", index=False)
    te_o.to_csv(f"{args.out_root}/merged/bhv_merged_test.csv", index=False)

    print("[OK] Day11 BEHAVIOR_FLAGS 构建完成")


if __name__ == "__main__":
    main()


