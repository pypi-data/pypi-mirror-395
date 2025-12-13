"""
day3_features.py - 基础特征工程模块
构建银行信贷违约预测的基础特征集，包括：
1) 主表基础特征：时间特征、原始数值、对数变换、比率特征
2) 银行流水特征：月度聚合统计、结构趋势特征
3) 交叉特征：DTI、月供压力等业务指标
4) 类别特征：One-Hot编码处理
"""

import argparse, os
import numpy as np
import pandas as pd

EPS = 1e-12

# -----------------------------
# utils
# -----------------------------
def to_month(ts):
    # Unix 秒 -> month 编码（用 Period 保证和成交月一一对应）
    return pd.to_datetime(ts, unit="s").dt.to_period("M").astype(str)

def safe_div(a, b):
    return np.where(np.asarray(b)==0, np.nan, np.asarray(a)/np.asarray(b))

def p95(x):
    return np.nanpercentile(x, 95) if len(x) else np.nan

# -----------------------------
# 主表块（补齐 Raw/Time + OHE(dummy_na) + 比率/对数）
# -----------------------------
def build_main_block(df_main: pd.DataFrame, is_train: bool):
    df = df_main.copy()

    # --- 时间特征（补齐 S1 的四列）
    df["issue_year"]  = pd.to_datetime(df["issue_time"], unit="s").dt.year
    df["issue_month"] = pd.to_datetime(df["issue_time"], unit="s").dt.month
    df["record_year"]  = pd.to_datetime(df["record_time"], unit="s").dt.year
    df["record_month"] = pd.to_datetime(df["record_time"], unit="s").dt.month

    # --- 原始数值直通（补齐 S1 的 8 列）
    raw_cols = [
        "career","interest_rate","loan","term",
        "total_accounts","balance_accounts","balance_limit","balance"
    ]
    for c in raw_cols:
        rc = "raw_" + c
        df[rc] = df[c]

    # --- 对数 & 比率 & 时长
    df["log1p_loan"]         = np.log1p(df["loan"].clip(lower=0))
    df["log1p_balance"]      = np.log1p(df["balance"].clip(lower=0))
    df["log1p_balance_limit"]= np.log1p(df["balance_limit"].clip(lower=0))

    df["utilization"]        = safe_div(df["balance"], df["balance_limit"])
    df["acct_used_ratio"]    = safe_div(df["balance_accounts"], df["total_accounts"])
    df["avg_balance_per_acct"]= safe_div(df["balance"], df["total_accounts"])
    df["avg_limit_per_acct"]  = safe_div(df["balance_limit"], df["total_accounts"])

    df["history_len_days"]      = (df["record_time"] - df["history_time"]) / (24*3600)
    df["rec_minus_issue_days"]  = (df["record_time"] - df["issue_time"]) / (24*3600)

    # --- level 有序编码（S1 用有序数值）
    #  level 是有序类别，直接从原始 level 映射/提取数字部分
    if "level_ord" in df.columns:
        level_ord = df["level_ord"]
    else:
        # 尝试把字母映射为序号：A<B<...；找不到就用类别 codes
        lev = df["level"].astype("string")
        # 仅取字母的序：A->0,B->1,... （失败则回退到 category.codes）
        mask = lev.str.len() > 0
        tmp = pd.Series(np.nan, index=lev.index, dtype="float")
        tmp.loc[mask] = lev.loc[mask].str[0].str.upper().map({chr(65+i): i for i in range(26)})
        if tmp.notna().any():
            level_ord = tmp.fillna(tmp.median())
        else:
            level_ord = lev.astype("category").cat.codes
    df["level_ord"] = level_ord

    # --- OHE（dummy_na=True，保留 *_nan 列；列名对齐 S1：title_0.0… + title_nan）
    def ohe_with_nan(s, prefix):
        d = pd.get_dummies(s, prefix=prefix, dummy_na=True, dtype=int)
        # 把 NaN 列名从 prefix_nan 保持为 *_nan（pandas 默认就是这样的）
        return d

    ohe_title       = ohe_with_nan(df["title"], "title")
    ohe_residence   = ohe_with_nan(df["residence"], "residence")
    ohe_term        = ohe_with_nan(df["term"], "term")
    ohe_syndicated  = ohe_with_nan(df["syndicated"], "syndicated")
    ohe_installment = ohe_with_nan(df["installment"], "installment")

    # --- zip 频次（S1 里是 zip_freq）
    df["zip_freq"] = df["zip_code"].astype("category").map(df["zip_code"].value_counts()).fillna(0).astype(float)

    # --- 汇总
    keep_main = [
        "id",
        "log1p_loan","log1p_balance","log1p_balance_limit",
        "utilization","acct_used_ratio","avg_balance_per_acct","avg_limit_per_acct",
        "history_len_days","rec_minus_issue_days","level_ord",
        "issue_year","issue_month","record_year","record_month",
        "raw_career","raw_interest_rate","raw_loan","raw_term",
        "raw_total_accounts","raw_balance_accounts","raw_balance_limit","raw_balance",
        "zip_freq"
    ]
    if is_train and "label" in df.columns:
        keep_main = ["label"] + keep_main

    main_block = df[keep_main].copy()
    main_block = pd.concat(
        [main_block, ohe_title, ohe_residence, ohe_term, ohe_syndicated, ohe_installment],
        axis=1
    )

    return main_block

# -----------------------------
# 银行流水（月度聚合 -> 跨期统计 + 结构/趋势 7 列）
# -----------------------------
def build_bank_block(df_bank: pd.DataFrame):
    if df_bank is None or len(df_bank)==0:
        # 按 S1 的列集合返回空框架
        cols = [
            "id",
            "bank_income_sum","bank_income_mean","bank_income_std","bank_income_p95",
            "bank_expense_sum","bank_expense_mean","bank_expense_std","bank_expense_p95",
            "bank_net_sum","bank_net_mean","bank_net_std",
            "bank_txn_count_m","bank_months_active","bank_income_share","bank_big_txn_share",
            # 7 个结构/趋势/跨期均值
            "bank_avg_income_over_period","bank_avg_expense_over_period",
            "bank_expense_over_income","bank_neg_periods",
            "bank_net_first","bank_net_last","bank_net_trend_simple",
        ]
        return pd.DataFrame(columns=cols)

    b = df_bank.copy()
    b["month"] = to_month(b["time"])
    # 每条交易做符号
    b["income"]  = np.where(b["direction"]==0, b["amount"], 0.0)
    b["expense"] = np.where(b["direction"]==1, b["amount"], 0.0)
    b["net"]     = b["income"] - b["expense"]

    # --- 先到“月”粒度
    per_mon = b.groupby(["id","month"]).agg(
        income_sum = ("income","sum"),
        expense_sum= ("expense","sum"),
        net_sum    = ("net","sum"),
        txn_cnt    = ("amount","size"),
        income_p95 = ("income", p95),
        expense_p95= ("expense", p95),
        # 这里也给出当月均值 & std，后面跨期再汇总
        income_mean=("income","mean"),
        expense_mean=("expense","mean"),
        net_mean    =("net","mean"),
        income_std = ("income","std"),
        expense_std= ("expense","std"),
        net_std    = ("net","std"),
    ).reset_index()

    # --- 跨期（按 S1 口径）
    g = per_mon.groupby("id")

    bank = g.agg(
        bank_income_sum = ("income_sum","sum"),
        bank_expense_sum= ("expense_sum","sum"),
        bank_net_sum    = ("net_sum","sum"),

        bank_income_mean=("income_sum","mean"),
        bank_expense_mean=("expense_sum","mean"),
        bank_net_mean    =("net_sum","mean"),

        bank_income_std = ("income_sum","std"),
        bank_expense_std= ("expense_sum","std"),
        bank_net_std    = ("net_sum","std"),

        bank_txn_count_m=("txn_cnt","sum"),
        bank_months_active=("month","nunique"),

        bank_income_p95 = ("income_sum", p95),
        bank_expense_p95= ("expense_sum", p95),
    ).reset_index()

    # 结构指标
    bank["bank_income_share"] = safe_div(
        bank["bank_income_sum"], bank["bank_income_sum"] + bank["bank_expense_sum"] + EPS
    )
    # 大额比例（用每月95分位判定“是否大额”，占比）
    big_flag = (per_mon["expense_sum"] > per_mon.groupby("id")["expense_sum"].transform(p95)).astype(int)
    big_rate = per_mon.assign(big=big_flag).groupby("id")["big"].mean().reindex(bank["id"]).values
    bank["bank_big_txn_share"] = big_rate

    # S1 缺失的 7 列（补齐）
    bank["bank_avg_income_over_period"]  = safe_div(bank["bank_income_sum"], bank["bank_months_active"])
    bank["bank_avg_expense_over_period"] = safe_div(bank["bank_expense_sum"], bank["bank_months_active"])
    bank["bank_expense_over_income"]     = safe_div(bank["bank_expense_sum"], bank["bank_income_sum"])

    # 首末值与趋势（按月份排序后取 net_sum 的首/末与简单斜率）
    def first_last_trend(dfm):
        dfm = dfm.sort_values("month")
        y = dfm["net_sum"].values
        if len(y)==0:
            return pd.Series({"first":np.nan,"last":np.nan,"trend":np.nan})
        first = y[0]
        last  = y[-1]
        # 简单趋势： (last - first) / max(1, n-1)
        trend = (last - first) / max(1, len(y)-1)
        return pd.Series({"first":first,"last":last,"trend":trend})

    flt = per_mon.groupby("id").apply(first_last_trend).reset_index()
    bank = bank.merge(
        flt.rename(columns={"first":"bank_net_first","last":"bank_net_last","trend":"bank_net_trend_simple"}),
        on="id", how="left"
    )

    # 负净额期数
    neg_cnt = (per_mon["net_sum"] < 0).groupby(per_mon["id"]).sum()
    bank["bank_neg_periods"] = bank["id"].map(neg_cnt).fillna(0).astype(float)

    # 缺失填补
    fill0 = [
        "bank_income_sum","bank_expense_sum","bank_net_sum",
        "bank_txn_count_m","bank_months_active",
        "bank_neg_periods"
    ]
    bank[fill0] = bank[fill0].fillna(0)

    return bank

# -----------------------------
# 交叉块
# -----------------------------
def build_cross_block(df_feat: pd.DataFrame):
    df = df_feat.copy()

    # installment 月供
    df["installment_amt"] = safe_div(
        df["loan"] * (df["interest_rate"]/100.0) / 12.0, 
        1.0
    )

    # 收入代理（
    fallback = safe_div(df["bank_income_sum"], df["bank_months_active"])
    proxy = df["bank_income_mean"].where(df["bank_income_mean"].notna(), fallback)
    df["monthly_income_proxy"] = proxy

    # DTI / buffer / net_over_installment（S1 命名）
    df["DTI"]                = safe_div(df["installment_amt"], df["monthly_income_proxy"])
    df["buffer_months"]      = safe_div(df["monthly_income_proxy"], df["installment_amt"])
    df["net_over_installment"]= safe_div(df["bank_net_mean"], df["installment_amt"])

    keep = ["id","installment_amt","monthly_income_proxy","DTI","buffer_months","net_over_installment"]
    return df[keep].copy()

# -----------------------------
# 组成最终 S1 列表
# -----------------------------
def assemble_s1_like(train_main, test_main, train_bank, test_bank, is_train):
    main_tr  = build_main_block(train_main, is_train=True)   if is_train else None
    main_te  = build_main_block(test_main,  is_train=False)

    bank_tr  = build_bank_block(train_bank) if is_train else None
    bank_te  = build_bank_block(test_bank)

    if is_train:
        tr = main_tr.merge(bank_tr, on="id", how="left")
        # 交叉要用原始主表数值（loan/interest_rate/term 等）
        tr_cross = build_cross_block(train_main.merge(bank_tr, on="id", how="left"))
        tr = tr.merge(tr_cross, on="id", how="left")
    te = main_te.merge(bank_te, on="id", how="left")
    te_cross = build_cross_block(test_main.merge(bank_te, on="id", how="left"))
    te = te.merge(te_cross, on="id", how="left")


    # 主体列
    s1_order = [
        # main *
        "id",
        "log1p_loan","log1p_balance","log1p_balance_limit",
        "utilization","acct_used_ratio","avg_balance_per_acct","avg_limit_per_acct",
        "history_len_days","rec_minus_issue_days","level_ord",
        # OHE（含 *_nan）
        # bank *
        "bank_income_sum","bank_income_mean","bank_income_std","bank_income_p95",
        "bank_expense_sum","bank_expense_mean","bank_expense_std","bank_expense_p95",
        "bank_net_sum","bank_net_mean","bank_net_std",
        "bank_txn_count_m","bank_months_active","bank_income_share","bank_big_txn_share",
        # 7 个补齐列
        "bank_avg_income_over_period","bank_avg_expense_over_period",
        "bank_expense_over_income","bank_neg_periods",
        "bank_net_first","bank_net_last","bank_net_trend_simple",
        # cross *
        "installment_amt","monthly_income_proxy","DTI","buffer_months","net_over_installment",
        # raw & time *
        "issue_year","issue_month","record_year","record_month",
        "raw_career","raw_interest_rate","raw_loan","raw_term",
        "raw_total_accounts","raw_balance_accounts","raw_balance_limit","raw_balance",
        # zip
        "zip_freq",
    ]

    def order_cols(df, is_train):
        cols = list(df.columns)
        head = ["label"] if (is_train and "label" in cols) else []
        # 保留存在的 s1_order，然后拼接剩余（比如 OHE 的 title_0.0…）
        body = [c for c in s1_order if c in cols]
        rest = [c for c in cols if c not in head + body]
        return df[head + body + rest].copy()

    if is_train:
        tr = order_cols(tr, True)
    te = order_cols(te, False)
    return tr if is_train else None, te

# -----------------------------
# CLI
# -----------------------------
def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train_main", required=True)
    ap.add_argument("--test_main", required=True)
    ap.add_argument("--train_bank", required=True)
    ap.add_argument("--test_bank", required=True)
    ap.add_argument("--out_train", required=True)
    ap.add_argument("--out_test", required=True)
    return ap.parse_args()

def main():
    args = parse_args()

    tr_main = pd.read_csv(args.train_main)
    te_main = pd.read_csv(args.test_main)
    tr_bank = pd.read_csv(args.train_bank)
    te_bank = pd.read_csv(args.test_bank)

    # 产出与 S1 对齐的特征
    tr_feat, te_feat = assemble_s1_like(tr_main, te_main, tr_bank, te_bank, is_train=True)

    # cols = 'main_avg_limit_per_acct'
    keep = [c for c in tr_feat.columns if c != "avg_limit_per_acct"]
    tr_feat = tr_feat[keep]
    keep2 = [c for c in te_feat.columns if c != "avg_limit_per_acct"]
    te_feat = te_feat[keep2]

    out_dir = os.path.dirname(args.out_train)
    if out_dir:  # 只有目录部分不为空才创建
        os.makedirs(out_dir, exist_ok=True)

    tr_feat.to_csv(args.out_train, index=False)
    te_feat.to_csv(args.out_test,  index=False)
    print(f"[OK] Saved:\n  {args.out_train}\n  {args.out_test}")

if __name__ == "__main__":
    main()