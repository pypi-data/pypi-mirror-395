#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day11 - INCOME_STAB 收入来源与稳定性（业务特征）
输入：同 AFFORD，基于包含主表+基础流水聚合的大表
输出：out/day11_income_out/features_income_{train,test}.csv 与 merged/income_merged_{train,test}.csv

避免与既有前缀重复：使用 incstab_* 前缀。
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


def build_income_stab(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    # 可获得的收入聚合
    inc_sum = out.get("bank_income_sum", pd.Series(0.0, index=out.index))
    inc_mean = out.get("bank_income_mean", pd.Series(0.0, index=out.index))
    months_active = out.get("bank_months_active", pd.Series(0.0, index=out.index))

    # 发薪规律性：有收入的月份占比（若仅有 months_active，近似用 months_active/总月数；这里用自身近似）
    out["incstab_income_months_share"] = safe_div(months_active, np.maximum(months_active, 6))

    # 收入稳定性（CV 代理）：若已有 bank_income_std/mean 则用；否则用简单 proxy
    if "bank_income_std" in out.columns and "bank_income_mean" in out.columns:
        out["incstab_income_cv"] = safe_div(out["bank_income_std"], out["bank_income_mean"].abs() + 1e-9)
    else:
        out["incstab_income_cv"] = 0.0

    # 收入密度（单位活跃月）：
    out["incstab_income_per_active_month"] = safe_div(inc_sum, months_active)

    # 近-远期对比代理：若有 bank_net_first/last/mean，可以做趋势方向性
    if {"bank_net_first", "bank_net_last"}.issubset(out.columns):
        out["incstab_net_trend_sign"] = np.sign(out["bank_net_last"].astype(float) - out["bank_net_first"].astype(float))
    else:
        out["incstab_net_trend_sign"] = 0.0

    # 工时合理性代理：若有 time_weekday_preference / time_hour_preference 之类，可组合；此处提供保底占位
    if "time_weekend_ratio" in out.columns:
        out["incstab_weekend_income_bias"] = out["time_weekend_ratio"].astype(float)
    else:
        out["incstab_weekend_income_bias"] = 0.0

    # 稳健裁剪
    num_cols = [c for c in out.columns if out[c].dtype.kind in ("i", "u", "f") and c not in ("id", "label")]
    for c in num_cols:
        q01, q99 = out[c].quantile(0.01), out[c].quantile(0.99)
        out[c] = out[c].clip(q01, q99)

    return out


def main():
    ap = argparse.ArgumentParser(description="Day11 INCOME_STAB 特征构建")
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

    tr_o = build_income_stab(tr)
    te_o = build_income_stab(te)

    tr_o.to_csv(f"{args.out_root}/features/features_income_train.csv", index=False)
    te_o.to_csv(f"{args.out_root}/features/features_income_test.csv", index=False)

    tr_o.to_csv(f"{args.out_root}/merged/income_merged_train.csv", index=False)
    te_o.to_csv(f"{args.out_root}/merged/income_merged_test.csv", index=False)

    print("[OK] Day11 INCOME_STAB 构建完成")


if __name__ == "__main__":
    main()


