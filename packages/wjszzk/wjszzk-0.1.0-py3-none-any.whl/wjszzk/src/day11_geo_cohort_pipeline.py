#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day11 - GEO_COHORT 地域对照（业务特征）
输入：包含主表+基础流水聚合的大表
输出：out/day11_geo_out/features_geo_{train,test}.csv 与 merged/geo_merged_{train,test}.csv

前缀：geo_*
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


def add_group_stats(df: pd.DataFrame, group_cols, target_cols, prefix: str) -> pd.DataFrame:
    out = df.copy()
    g = out.groupby(group_cols)
    for t in target_cols:
        if t not in out.columns:
            continue
        mean = g[t].transform("mean")
        med = g[t].transform("median")
        std = g[t].transform("std").fillna(0)
        out[f"{prefix}_{t}_gmean"] = mean
        out[f"{prefix}_{t}_gmedian"] = med
        out[f"{prefix}_{t}_gz"] = (out[t].astype(float) - mean) / (std.replace(0, np.nan))
        out[f"{prefix}_{t}_rel"] = safe_div(out[t], med.replace(0, np.nan))
        out[f"{prefix}_{t}_rank"] = g[t].rank(method="average").div(g[t].transform("count").replace(0, np.nan))
    return out


def build_geo(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    # 准备群体键：zip_h3, career, level_m（若缺失则回退）
    if "zip_code" in out.columns:
        out["geo_zip_h3"] = out["zip_code"].astype(str).str[:3]
    else:
        out["geo_zip_h3"] = "UNK"
    if "career" in out.columns:
        out["geo_career"] = out["career"].astype(str)
    else:
        out["geo_career"] = "UNK"
    if "level" in out.columns:
        out["geo_level_m"] = out["level"].astype(str).str[:1]
    else:
        out["geo_level_m"] = "U"

    group_cols = ["geo_zip_h3", "geo_career", "geo_level_m"]
    targets = [
        "installment_amt",
        "bank_income_mean", "bank_expense_mean", "bank_net_mean",
        "utilization", "DTI",
    ]
    out = add_group_stats(out, group_cols, targets, prefix="geo")

    return out


def main():
    ap = argparse.ArgumentParser(description="Day11 GEO_COHORT 特征构建")
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

    tr_o = build_geo(tr)
    te_o = build_geo(te)

    tr_o.to_csv(f"{args.out_root}/features/features_geo_train.csv", index=False)
    te_o.to_csv(f"{args.out_root}/features/features_geo_test.csv", index=False)

    tr_o.to_csv(f"{args.out_root}/merged/geo_merged_train.csv", index=False)
    te_o.to_csv(f"{args.out_root}/merged/geo_merged_test.csv", index=False)

    print("[OK] Day11 GEO_COHORT 构建完成")


if __name__ == "__main__":
    main()


