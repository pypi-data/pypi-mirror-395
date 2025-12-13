#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day11 - AFFORD 偿付能力与月供压力（业务特征）
输入：建议基于包含主表+基础流水聚合后的大表（如 time_out/poly_out 等最终表）
输出：out/day11_afford_out/features_afford_{train,test}.csv 及 merged/afford_merged_{train,test}.csv

避免与既有前缀重复：使用 aff_* 前缀。
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


def build_afford_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    # 需要的基础列：installment_amt, bank_income_sum/mean, bank_expense_sum/mean, bank_net_mean
    # 若缺失则尽量回退
    inc_mean = out.get("bank_income_mean", out.get("bank_income_sum", pd.Series(0, index=out.index)))
    exp_mean = out.get("bank_expense_mean", out.get("bank_expense_sum", pd.Series(0, index=out.index)))
    net_mean = out.get("bank_net_mean", inc_mean.astype(float) - exp_mean.astype(float))

    # 近1/3/6月均值代理：若没有窗口列，则用 mean 近似；便于与已有 TIME/REC 共存
    # 这里不造通用统计列，仅按业务口径命名
    out["aff_inc_mean_1m"] = inc_mean
    out["aff_inc_mean_3m"] = inc_mean
    out["aff_inc_mean_6m"] = inc_mean
    out["aff_exp_mean_1m"] = exp_mean
    out["aff_exp_mean_3m"] = exp_mean
    out["aff_exp_mean_6m"] = exp_mean
    out["aff_net_mean_1m"] = net_mean
    out["aff_net_mean_3m"] = net_mean
    out["aff_net_mean_6m"] = net_mean

    inst = out.get("installment_amt", pd.Series(0.0, index=out.index))

    # 覆盖与压力
    for k in ("1m", "3m", "6m"):
        out[f"aff_cover_{k}"] = safe_div(out[f"aff_net_mean_{k}"], inst)
        out[f"aff_install_share_{k}"] = safe_div(inst, out[f"aff_inc_mean_{k}"])
        out[f"aff_buffer_months_{k}"] = safe_div(out[f"aff_inc_mean_{k}"], inst)
        out[f"aff_net_minus_install_{k}"] = out[f"aff_net_mean_{k}"] - inst

    # 最小覆盖能力（保守口径）
    out["aff_min_cover"] = np.minimum.reduce([
        out["aff_cover_1m"].astype(float),
        out["aff_cover_3m"].astype(float),
        out["aff_cover_6m"].astype(float),
    ])

    # 授信相关压力
    bal_limit = out.get("raw_balance_limit", out.get("balance_limit", pd.Series(0.0, index=out.index)))
    loan_raw = out.get("raw_loan", out.get("loan", pd.Series(0.0, index=out.index)))
    out["aff_install_over_limit"] = safe_div(inst, bal_limit)
    out["aff_install_over_loan"] = safe_div(inst, loan_raw)

    # 稳健裁剪
    num_cols = [c for c in out.columns if out[c].dtype.kind in ("i", "u", "f") and c not in ("id", "label")]
    for c in num_cols:
        q01, q99 = out[c].quantile(0.01), out[c].quantile(0.99)
        out[c] = out[c].clip(q01, q99)

    return out


def main():
    ap = argparse.ArgumentParser(description="Day11 AFFORD 特征构建")
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

    tr_o = build_afford_features(tr)
    te_o = build_afford_features(te)

    tr_o.to_csv(f"{args.out_root}/features/features_afford_train.csv", index=False)
    te_o.to_csv(f"{args.out_root}/features/features_afford_test.csv", index=False)

    tr_o.to_csv(f"{args.out_root}/merged/afford_merged_train.csv", index=False)
    te_o.to_csv(f"{args.out_root}/merged/afford_merged_test.csv", index=False)

    print("[OK] Day11 AFFORD 构建完成")


if __name__ == "__main__":
    main()


