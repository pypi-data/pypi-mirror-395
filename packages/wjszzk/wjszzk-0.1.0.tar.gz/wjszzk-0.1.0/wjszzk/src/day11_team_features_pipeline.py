#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day11 Team Features Pipeline
整合团队的其他特征工程工作，包括主表通用特征和银行流水特征
输入：
  - base_train/base_test: 上一批输出的大表（作为基表，用于最终合并）
  - train_main/test_main: 原始主表（用于计算 team_* 特征）
  - bank_train/bank_test: 原始流水表（可选，用于补充交易侧特征）
输出：out/day11_team_out/features_team_{train,test}.csv 及 merged/team_merged_{train,test}.csv

避免与既有前缀重复：使用 team_* 前缀。
"""

import os
import argparse
import numpy as np
import pandas as pd
import warnings
from datetime import datetime, timedelta
import math

warnings.filterwarnings('ignore')

def ensure_dir(p: str):
    os.makedirs(p, exist_ok=True)

def read_csv(p: str) -> pd.DataFrame:
    return pd.read_csv(p)

def safe_div(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    return np.where(b != 0, a / b, 0.0)

def level_2_num(x):
    try:
        if pd.isna(x) or x == '':
            return np.nan
        level_dict = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5}
        num = level_dict.get(str(x)[0], np.nan)
        digit = pd.to_numeric(str(x)[1:2], errors='coerce')
        if pd.isna(num) or pd.isna(digit):
            return np.nan
        return num + float(digit) * 0.2
    except Exception:
        return np.nan

def time_sub(dt1, dt2, method="months"):
    try:
        a = datetime.strptime(str(dt1), "%Y%m%d")
        b = datetime.strptime(str(dt2), "%Y%m%d")
        if method == "months":
            days = (b - a).days
            return 0.5 if days <= 15 else round(days / 30, 1)
        elif method == "years":
            days = (b - a).days
            return 0.5 if days <= 180 else round(days / 365, 1)
        else:
            days = (b - a).days
            return 1 if days <= 1 else round(days, 1)
    except Exception:
        return np.nan

def yg_func(a, b, c):
    try:
        a = float(a) if pd.notna(a) else np.nan
        b = int(b) if pd.notna(b) else 0
        c = float(c) if pd.notna(c) else np.nan
        if pd.isna(a) or pd.isna(c) or b == 0:
            return np.nan
        y = c / 12.0 / 100.0
        denom = (1 + y) ** b - 1
        if y <= 0 or denom == 0:
            return np.nan
        return round((a * y * (1 + y) ** b) / denom, 2)
    except Exception:
        return np.nan

def count_debet_months(df, period):
    try:
        debet_months = 0
        if period != 1:
            seen = df["ym"].dropna().unique().tolist()
            num = period - len(seen)
            for ym in seen:
                tmp = df.loc[df["ym"] == ym, ["direction", "amount"]].values.tolist()
                if len(tmp) == 2:
                    a, b = tmp
                    if a[1] - b[1] <= 0:
                        debet_months += 1
                elif len(tmp) == 1:
                    a = tmp[0]
                    if a[0] == 1:
                        debet_months += 1
            debet_months += max(num, 0)
        else:
            v0 = df.loc[df["direction"] == 0, "amount"].sum()
            v1 = df.loc[df["direction"] == 1, "amount"].sum()
            if v1 - v0 >= 0:
                debet_months = 1
        return debet_months
    except Exception:
        return period

def _series_or_default(df: pd.DataFrame, col: str, default_val=np.nan):
    if col in df.columns:
        return df[col]
    return pd.Series([default_val] * len(df), index=df.index)

def generate_team_features_main(main_df: pd.DataFrame) -> pd.DataFrame:
    out = main_df.copy()

    level_s = _series_or_default(out, "level", np.nan)
    zip_s   = _series_or_default(out, "zip_code", np.nan)
    issue_s = _series_or_default(out, "issue_time", np.nan)
    record_s= _series_or_default(out, "record_time", issue_s)

    out["team_basic_level_m"] = level_s.astype(str).str[0].where(level_s.notna(), np.nan)
    out["team_basic_zip_h3"] = zip_s.astype(str).str[:3].where(zip_s.notna(), np.nan)
    out["team_basic_zip_h2"] = zip_s.astype(str).str[:2].where(zip_s.notna(), np.nan)
    out["team_basic_issue_year"] = issue_s.astype(str).str[:4].where(issue_s.notna(), np.nan)

    loan_s = _series_or_default(out, "loan", np.nan)
    term_s = _series_or_default(out, "term", 0)
    rate_s = _series_or_default(out, "interest_rate", np.nan)
    out["team_payment_monthly"] = pd.concat([loan_s, term_s, rate_s], axis=1).apply(lambda x: yg_func(x[0], x[1], x[2]), axis=1)

    out["team_time_issue_to_record"] = pd.concat([issue_s, record_s], axis=1).apply(lambda x: time_sub(x[0], x[1]), axis=1)
    out["team_time_history_to_issue"] = pd.concat([_series_or_default(out, "history_time", issue_s), issue_s], axis=1).apply(lambda x: time_sub(x[0], x[1], "years"), axis=1)
    out["team_time_record_to_max"] = record_s.apply(lambda x: time_sub(x, record_s.max()))

    bal_acct  = _series_or_default(out, "balance_accounts", 0.0)
    tot_acct  = _series_or_default(out, "total_accounts", 0.0)
    bal_limit = _series_or_default(out, "balance_limit", 0.0)
    balance   = _series_or_default(out, "balance", 0.0)

    out["team_credit_balance_ratio"] = safe_div(bal_acct, tot_acct + 1)
    out["team_credit_balance_avg"]   = safe_div(bal_limit, bal_acct + 1)
    out["team_credit_utilization"]   = safe_div(balance, bal_limit + 1)
    out["team_credit_income_ratio"]  = safe_div(balance, loan_s.fillna(0) + 1)
    out["team_credit_total_utilization"] = safe_div(balance, bal_acct + 1)

    out["team_interaction_loan_term"] = (np.log(loan_s.fillna(0) + 1) * (term_s.fillna(0)) / 10000).round(2)
    level_val = level_s.apply(level_2_num)
    out["team_interaction_level_value"] = level_val
    out["team_interaction_risk_score"] = (
        safe_div(term_s.fillna(0), out["team_time_issue_to_record"].fillna(0) + 1) *
        level_val.fillna(0) * np.log(out["team_payment_monthly"].fillna(0) + 1)
    ).round(2)
    out["team_interaction_rate_level"] = rate_s.fillna(0) * level_val.fillna(0)
    out["team_interaction_installment_history"] = safe_div(out["team_payment_monthly"].fillna(0), out["team_time_issue_to_record"].fillna(0) + 1)
    out["team_interaction_loan_accounts"] = safe_div(np.log(loan_s.fillna(0) + 1), bal_acct + 1)
    out["team_interaction_rate_loan"] = np.log(loan_s.fillna(0) + 1) * rate_s.fillna(0)

    out["team_geo_zip_level"] = (out["team_basic_zip_h3"].astype(str) + "_" + out["team_basic_level_m"].astype(str))
    out["team_geo_zip_residence"] = (out["team_basic_zip_h3"].astype(str) + "_" + _series_or_default(out, "residence", "nan").astype(str))
    out["team_geo_zip_career"] = (out["team_basic_zip_h3"].astype(str) + "_" + _series_or_default(out, "career", "nan").astype(str))
    out["team_geo_zip_title"] = (out["team_basic_zip_h3"].astype(str) + "_" + _series_or_default(out, "title", "nan").astype(str))
    out["team_geo_zip_year"] = (out["team_basic_zip_h2"].astype(str) + "_" + out["team_basic_issue_year"].astype(str))
    out["team_geo_career_title"] = (_series_or_default(out, "career", "nan").astype(str) + "_" + _series_or_default(out, "title", "nan").astype(str))

    for col in [
        "team_geo_zip_level", "team_geo_zip_residence", "team_geo_zip_career",
        "team_geo_zip_title", "team_geo_zip_year", "team_geo_career_title"
    ]:
        out[col] = out[col].astype('category').cat.codes

    team_cols = [c for c in out.columns if c.startswith('team_')]
    for col in team_cols:
        if out[col].dtype.kind in ("i", "u", "f"):
            out[col] = out[col].replace([np.inf, -np.inf], np.nan)
            out[col] = out[col].fillna(out[col].median())

    return out[['id'] + team_cols] if 'id' in out.columns else out[team_cols]

def generate_team_features_transaction(transaction_data: pd.DataFrame) -> pd.DataFrame:
    required_cols = ['id', 'time', 'direction', 'amount', 'record_time']
    if any(c not in transaction_data.columns for c in required_cols):
        return pd.DataFrame()

    df = transaction_data.copy()
    df["ym"] = df["time"].astype(str).str[:6]

    deal_list = []
    for i in df["id"].dropna().unique():
        part = df.loc[df["id"] == i]
        if part.empty:
            continue
        max_time = part["record_time"].iloc[0]
        if pd.isna(max_time):
            continue
        try:
            h30_time  = (datetime.strptime(str(max_time), "%Y%m%d") - timedelta(days=30)).strftime("%Y%m%d")
            h90_time  = (datetime.strptime(str(max_time), "%Y%m%d") - timedelta(days=90)).strftime("%Y%m%d")
            h180_time = (datetime.strptime(str(max_time), "%Y%m%d") - timedelta(days=180)).strftime("%Y%m%d")
            empty_time = (datetime.strptime(str(max_time), "%Y%m%d") - datetime.strptime(str(part["time"].max()), "%Y%m%d")).days

            part1 = part.loc[part["time"] >= h30_time]
            part2 = part.loc[part["time"] >= h90_time]
            part3 = part.loc[part["time"] >= h180_time]

            if not part3.empty:
                real_max_time = part3["time"].max()
                real_min_time = part3["time"].min()
                months = math.ceil(max(round((datetime.strptime(str(real_max_time), "%Y%m%d") - datetime.strptime(str(real_min_time), "%Y%m%d")).days/30, 2),1))
            else:
                months = 0

            part3_0 = len(set([t[4:6] for t in part3.loc[part3["direction"] == 0, "time"]])) if not part3.empty else 0
            part1_0 = len(set([t[4:6] for t in part1.loc[part1["direction"] == 0, "time"]])) if not part1.empty else 0

            if not part3.empty:
                tmp3 = part3[["ym","direction","amount"]].groupby(["ym","direction"]).agg({"amount":sum}).reset_index()
                debet_6m = count_debet_months(tmp3, 6)
            else:
                debet_6m = 6
            if not part2.empty:
                tmp2 = part2[["ym","direction","amount"]].groupby(["ym","direction"]).agg({"amount":sum}).reset_index()
                debet_3m = count_debet_months(tmp2, 3)
            else:
                debet_3m = 3
            if not part1.empty:
                tmp1 = part1[["ym","direction","amount"]].groupby(["ym","direction"]).agg({"amount":sum}).reset_index()
                debet_1m = count_debet_months(tmp1, 1)
            else:
                debet_1m = 1

            amount_0 = round((part3.loc[part3["direction"] == 0, "amount"].sum())/6,2) if not part3.empty else 0
            amount_1 = round((part3.loc[part3["direction"] == 1, "amount"].sum())/6,2) if not part3.empty else 0
            amount_sub1 = amount_0 - amount_1

            amount_2 = round((part2.loc[part2["direction"] == 0, "amount"].sum())/3,2) if not part2.empty else 0
            amount_3 = round((part2.loc[part2["direction"] == 1, "amount"].sum())/3,2) if not part2.empty else 0
            amount_sub2 = amount_2 - amount_3

            amount_4 = round((part1.loc[part1["direction"] == 0, "amount"].sum())/1,2) if not part1.empty else 0
            amount_5 = round((part1.loc[part1["direction"] == 1, "amount"].sum())/1,2) if not part1.empty else 0
            amount_sub3 = amount_4 - amount_5

            if (amount_sub3 <= 0) and (amount_sub2 <= 0) and (amount_sub1 <= 0):
                less_flag = 10
            elif (amount_sub3 <= 0) and (amount_sub2 <= 0) and (amount_sub1 > 0):
                less_flag = 8
            elif (amount_sub3 <= amount_sub2) and (amount_sub2 <= amount_sub1):
                less_flag = 6 if amount_sub3 <= 0 else 4
            elif (amount_sub3 >= amount_sub2) and (amount_sub2 >= amount_sub1):
                less_flag = 1
            else:
                less_flag = 2

            m6_b0_num = part3.loc[(part3["direction"]==0) & (part3["amount"]>1300)].shape[0] if not part3.empty else 0
            m3_b0_num = part2.loc[(part2["direction"]==0) & (part2["amount"]>1300)].shape[0] if not part2.empty else 0
            m3_b1_num = part2.loc[(part2["direction"]==1) & (part2["amount"]>1300)].shape[0] if not part2.empty else 0

            deal_list.append([i, empty_time, part3_0, debet_6m, part1_0, debet_1m, months,
                              amount_0, amount_1, amount_sub1, amount_sub3, less_flag,
                              m6_b0_num, m3_b0_num, m3_b1_num])
        except Exception:
            continue

    if not deal_list:
        return pd.DataFrame()

    return pd.DataFrame(deal_list, columns=[
        "id", "team_transaction_empty_days", "team_transaction_income_months_6m",
        "team_transaction_deficit_months_6m", "team_transaction_income_months_1m",
        "team_transaction_deficit_months_1m", "team_transaction_coverage_months",
        "team_transaction_avg_income_6m", "team_transaction_avg_expense_6m",
        "team_transaction_net_income_6m", "team_transaction_net_income_1m",
        "team_transaction_risk_flag", "team_transaction_large_income_6m",
        "team_transaction_large_income_3m", "team_transaction_large_expense_3m"
    ])

def build_team_features_from_raw(main_df: pd.DataFrame, bank_df: pd.DataFrame | None) -> pd.DataFrame:
    main_feats = generate_team_features_main(main_df)
    if bank_df is not None and not bank_df.empty:
        bank_feats = generate_team_features_transaction(bank_df)
        if not bank_feats.empty:
            # 左连接回到 main（按 id）
            main_feats = pd.merge(main_feats, bank_feats, on='id', how='left') if 'id' in main_feats.columns else main_feats
    return main_feats

def main():
    ap = argparse.ArgumentParser(description="Day11 TEAM_FEATURES 特征构建")
    ap.add_argument("--base_train", required=True, help="上一批次合并训练表")
    ap.add_argument("--base_test", required=True, help="上一批次合并测试表")
    ap.add_argument("--train_main", required=True, help="原始主表-训练集")
    ap.add_argument("--test_main", required=True, help="原始主表-测试集")
    ap.add_argument("--out_root", required=True, help="输出根目录")
    ap.add_argument("--bank_train", help="原始流水-训练集")
    ap.add_argument("--bank_test", help="原始流水-测试集")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    np.random.seed(args.seed)
    ensure_dir(args.out_root)
    ensure_dir(f"{args.out_root}/features")
    ensure_dir(f"{args.out_root}/merged")

    # 读取基表
    base_tr = read_csv(args.base_train)
    base_te = read_csv(args.base_test)

    # 读取原始主表与流水
    tr_main = read_csv(args.train_main)
    te_main = read_csv(args.test_main)
    tr_bank = read_csv(args.bank_train) if args.bank_train and os.path.exists(args.bank_train) else None
    te_bank = read_csv(args.bank_test)  if args.bank_test  and os.path.exists(args.bank_test)  else None

    # 从原始数据构建 team_* 特征
    tr_team = build_team_features_from_raw(tr_main, tr_bank)
    te_team = build_team_features_from_raw(te_main, te_bank)

    team_cols = [c for c in tr_team.columns if c.startswith('team_')]

    # 保存纯特征
    tr_team[['id'] + team_cols if 'id' in tr_team.columns else team_cols].to_csv(f"{args.out_root}/features/features_team_train.csv", index=False)
    te_team[['id'] + team_cols if 'id' in te_team.columns else team_cols].to_csv(f"{args.out_root}/features/features_team_test.csv", index=False)

    # 与基表合并
    tr_merged = pd.merge(base_tr, tr_team, on='id', how='left') if 'id' in base_tr.columns else base_tr
    te_merged = pd.merge(base_te, te_team, on='id', how='left') if 'id' in base_te.columns else base_te

    tr_merged.to_csv(f"{args.out_root}/merged/team_merged_train.csv", index=False)
    te_merged.to_csv(f"{args.out_root}/merged/team_merged_test.csv", index=False)

    # 元数据
    meta = {
        "feature_count": len(team_cols),
        "feature_prefix": "team_",
        "description": "团队特征：由原始主表+流水计算，随后与基表按id合并",
        "features": team_cols,
        "train_shape": tr_merged.shape,
        "test_shape": te_merged.shape
    }
    import json
    with open(f"{args.out_root}/meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print("[OK] Day11 TEAM_FEATURES 构建完成")

if __name__ == "__main__":
    main()
