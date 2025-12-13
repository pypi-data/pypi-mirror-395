#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day11 - EXPENSE_STRUCTURE 支出结构（业务特征）
输入：包含主表+基础流水聚合的大表
输出：out/day11_expense_out/features_expense_{train,test}.csv 与 merged/expense_merged_{train,test}.csv

前缀：expstr_*
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


def build_expense_structure(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    exp_sum = out.get("bank_expense_sum", pd.Series(0.0, index=out.index))
    exp_mean = out.get("bank_expense_mean", pd.Series(0.0, index=out.index))
    months_active = out.get("bank_months_active", pd.Series(0.0, index=out.index))
    inc_mean = out.get("bank_income_mean", pd.Series(0.0, index=out.index))

    # 刚性支出代理：以近似规则逼近（若有更细交易结构，可替换为周期性相似金额识别）
    # 这里用“支出均值中较稳定部分”的比例来做 proxy：稳定度=1/(1+CV)，刚性=mean * 稳定度
    if "bank_expense_std" in out.columns and "bank_expense_mean" in out.columns:
        cv = safe_div(out["bank_expense_std"], out["bank_expense_mean"].abs() + 1e-9)
        stability = 1.0 / (1.0 + cv)
        rigid = out["bank_expense_mean"].astype(float) * stability
    else:
        rigid = exp_mean.astype(float) * 0.6
    out["expstr_rigid_expense_proxy"] = rigid

    # 可支配空间：收入均值 - 刚性支出
    out["expstr_disposable_proxy"] = inc_mean.astype(float) - out["expstr_rigid_expense_proxy"].astype(float)

    # 消费结构：大额/小额的粗略比例（无法直接访问明细时，用均值密度近似）
    out["expstr_expense_per_active_month"] = safe_div(exp_sum, months_active)

    # 工作日/周末/夜间偏置若有（复用 time_*）
    if "time_weekend_ratio" in out.columns:
        out["expstr_weekend_bias"] = out["time_weekend_ratio"].astype(float)
    else:
        out["expstr_weekend_bias"] = 0.0
    if "time_late_night_ratio" in out.columns:
        out["expstr_late_night_bias"] = out["time_late_night_ratio"].astype(float)
    else:
        out["expstr_late_night_bias"] = 0.0

    # 支出波动
    if "bank_expense_std" in out.columns and "bank_expense_mean" in out.columns:
        out["expstr_expense_cv"] = safe_div(out["bank_expense_std"], out["bank_expense_mean"].abs() + 1e-9)
    else:
        out["expstr_expense_cv"] = 0.0

    # 稳健裁剪
    num_cols = [c for c in out.columns if out[c].dtype.kind in ("i", "u", "f") and c not in ("id", "label")]
    for c in num_cols:
        q01, q99 = out[c].quantile(0.01), out[c].quantile(0.99)
        out[c] = out[c].clip(q01, q99)

    return out


def main():
    ap = argparse.ArgumentParser(description="Day11 EXPENSE_STRUCTURE 特征构建")
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

    tr_o = build_expense_structure(tr)
    te_o = build_expense_structure(te)

    tr_o.to_csv(f"{args.out_root}/features/features_expense_train.csv", index=False)
    te_o.to_csv(f"{args.out_root}/features/features_expense_test.csv", index=False)

    tr_o.to_csv(f"{args.out_root}/merged/expense_merged_train.csv", index=False)
    te_o.to_csv(f"{args.out_root}/merged/expense_merged_test.csv", index=False)

    print("[OK] Day11 EXPENSE_STRUCTURE 构建完成")


if __name__ == "__main__":
    main()


