#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day11 - LIQUIDITY_SHOCK 流动性与抗冲击能力（业务特征）
输入：包含主表+基础流水聚合的大表
输出：out/day11_shock_out/features_shock_{train,test}.csv 与 merged/shock_merged_{train,test}.csv

前缀：shock_*
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


def build_shock(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    inc_mean = out.get("bank_income_mean", pd.Series(0.0, index=out.index)).astype(float)
    exp_mean = out.get("bank_expense_mean", pd.Series(0.0, index=out.index)).astype(float)
    net_mean = out.get("bank_net_mean", (inc_mean - exp_mean)).astype(float)
    inst = out.get("installment_amt", pd.Series(0.0, index=out.index)).astype(float)

    # 压测场景：收入下调、支出上调
    scenarios = [
        (0.90, 1.10),
        (0.80, 1.20),
    ]
    for i, (inc_down, exp_up) in enumerate(scenarios, start=1):
        inc_s = inc_mean * inc_down
        exp_s = exp_mean * exp_up
        net_s = inc_s - exp_s
        out[f"shock_s{i}_net_minus_install"] = net_s - inst
        out[f"shock_s{i}_cover_ratio"] = safe_div(net_s, inst)

    # 最坏场景
    out["shock_worst_net_minus_install"] = np.minimum(
        out["shock_s1_net_minus_install"], out["shock_s2_net_minus_install"]
    )
    out["shock_worst_cover_ratio"] = np.minimum(
        out["shock_s1_cover_ratio"], out["shock_s2_cover_ratio"]
    )

    # 资金空窗：距最近入账天数（若无 time_* 列，提供0占位）
    if "time_active_days" in out.columns and "time_total_days" in out.columns:
        out["shock_time_efficiency"] = safe_div(out["time_active_days"], out["time_total_days"])  # 辅助指标
    else:
        out["shock_time_efficiency"] = 0.0

    # 连续负月代理：若有 bank_neg_periods 列可直接复用
    if "bank_neg_periods" in out.columns:
        out["shock_neg_periods"] = out["bank_neg_periods"].astype(float)
    else:
        out["shock_neg_periods"] = 0.0

    # 稳健裁剪
    num_cols = [c for c in out.columns if out[c].dtype.kind in ("i", "u", "f") and c not in ("id", "label")]
    for c in num_cols:
        q01, q99 = out[c].quantile(0.01), out[c].quantile(0.99)
        out[c] = out[c].clip(q01, q99)

    return out


def main():
    ap = argparse.ArgumentParser(description="Day11 LIQUIDITY_SHOCK 特征构建")
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

    tr_o = build_shock(tr)
    te_o = build_shock(te)

    tr_o.to_csv(f"{args.out_root}/features/features_shock_train.csv", index=False)
    te_o.to_csv(f"{args.out_root}/features/features_shock_test.csv", index=False)

    tr_o.to_csv(f"{args.out_root}/merged/shock_merged_train.csv", index=False)
    te_o.to_csv(f"{args.out_root}/merged/shock_merged_test.csv", index=False)

    print("[OK] Day11 LIQUIDITY_SHOCK 构建完成")


if __name__ == "__main__":
    main()


