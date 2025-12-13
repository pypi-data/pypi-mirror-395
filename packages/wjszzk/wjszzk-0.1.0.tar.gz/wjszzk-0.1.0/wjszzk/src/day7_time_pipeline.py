# -*- coding: utf-8 -*-
"""
Day7 - TIME 批次：时间序列特征构建
构建基于时间维度的深度特征，包括：
1) 时间序列特征：趋势、周期性、季节性、波动性
2) 用户行为模式：交易习惯、时间偏好、金额分布模式
3) 交互时间特征：不同时间窗口的统计特征
4) 风险时间特征：异常时间模式、风险时间点
与基线特征合并后输出，供后续特征工程使用
"""
import os, json, argparse, numpy as np, pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score
from scipy import stats
from datetime import datetime, timedelta

# --------- 默认路径 ---------
DEF_BASE_TRAIN = "./out/add_out/merged/add_merged_train.csv"
DEF_BASE_TEST  = "./out/add_out/merged/add_merged_test.csv"
DEF_TRAIN_MAIN = "../data/train/train.csv"
DEF_TRAIN_BANK = "../data/train/train_bank_statement.csv"
DEF_TEST_MAIN  = "../data/testaa/testaa.csv"
DEF_TEST_BANK  = "../data/testaa/testaa_bank_statement.csv"

# --------- 工具函数 ---------
def ensure_dir(p): os.makedirs(p, exist_ok=True)

def rank01(a):
    s = pd.Series(a)
    r = s.rank(method="average").to_numpy()
    if r.max() == r.min(): return np.zeros_like(r, dtype=float)
    return (r - r.min()) / (r.max() - r.min())

def safe_div(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    b = np.where(b==0, np.nan, b)
    out = a / b
    return np.nan_to_num(out, nan=0.0, posinf=0.0, neginf=0.0)
def load_baseline(base_train, base_test, train_main_path):
    tr = pd.read_csv(base_train)
    te = pd.read_csv(base_test)
    if "label" not in tr.columns:
        lab = pd.read_csv(train_main_path)[["id","label"]]
        tr = tr.merge(lab, on="id", how="left")
    return tr, te

# --------- 时间序列特征构建 ---------
def build_time_features(train_main, test_main, train_bank, test_bank):
    """构建时间序列特征"""
    
    # 1. 银行流水时间特征
    def extract_bank_time_features(bank_df):
        if bank_df is None or len(bank_df) == 0:
            return pd.DataFrame({"id": []})
        
        df = bank_df.copy()
        df["time_dt"] = pd.to_datetime(df["time"], unit="s", utc=True).dt.tz_convert(None)
        df["date"] = df["time_dt"].dt.date
        df["hour"] = df["time_dt"].dt.hour
        df["day_of_week"] = df["time_dt"].dt.dayofweek
        df["day_of_month"] = df["time_dt"].dt.day
        df["month"] = df["time_dt"].dt.month
        df["quarter"] = df["time_dt"].dt.quarter
        df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)
        df["is_month_end"] = (df["day_of_month"] >= 25).astype(int)
        df["is_month_start"] = (df["day_of_month"] <= 5).astype(int)
        
        # 交易时间分布特征
        time_features = []
        for id_val in df["id"].unique():
            user_df = df[df["id"] == id_val]
            if len(user_df) == 0:
                continue
                
            features = {"id": id_val}
            
            # 时间偏好特征
            features["avg_hour"] = user_df["hour"].mean()
            features["std_hour"] = user_df["hour"].std()
            features["weekend_ratio"] = user_df["is_weekend"].mean()
            features["month_end_ratio"] = user_df["is_month_end"].mean()
            features["month_start_ratio"] = user_df["is_month_start"].mean()
            
            # 交易频率特征
            features["txn_per_day"] = len(user_df) / user_df["date"].nunique() if user_df["date"].nunique() > 0 else 0
            features["active_days"] = user_df["date"].nunique()
            features["total_days"] = (user_df["time_dt"].max() - user_df["time_dt"].min()).days + 1
            features["density"] = features["active_days"] / features["total_days"] if features["total_days"] > 0 else 0
            
            # 时间间隔特征
            user_df_sorted = user_df.sort_values("time_dt")
            if len(user_df_sorted) > 1:
                time_diffs = user_df_sorted["time_dt"].diff().dt.total_seconds() / 3600  # 小时
                features["avg_interval_hours"] = time_diffs.mean()
                features["std_interval_hours"] = time_diffs.std()
                features["min_interval_hours"] = time_diffs.min()
                features["max_interval_hours"] = time_diffs.max()
            else:
                features["avg_interval_hours"] = 0
                features["std_interval_hours"] = 0
                features["min_interval_hours"] = 0
                features["max_interval_hours"] = 0
            
            # 周期性特征
            features["weekday_preference"] = user_df["day_of_week"].mode().iloc[0] if len(user_df["day_of_week"].mode()) > 0 else 0
            features["hour_preference"] = user_df["hour"].mode().iloc[0] if len(user_df["hour"].mode()) > 0 else 0
            
            # 时间波动性
            features["hour_entropy"] = stats.entropy(user_df["hour"].value_counts()) if len(user_df["hour"].value_counts()) > 1 else 0
            features["weekday_entropy"] = stats.entropy(user_df["day_of_week"].value_counts()) if len(user_df["day_of_week"].value_counts()) > 1 else 0
            
            time_features.append(features)
        
        return pd.DataFrame(time_features)
    
    # 2. 金额时间模式特征
    def extract_amount_time_patterns(bank_df):
        if bank_df is None or len(bank_df) == 0:
            return pd.DataFrame({"id": []})
        
        df = bank_df.copy()
        df["time_dt"] = pd.to_datetime(df["time"], unit="s", utc=True).dt.tz_convert(None)
        df["hour"] = df["time_dt"].dt.hour
        df["day_of_week"] = df["time_dt"].dt.dayofweek
        df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)
        
        amount_features = []
        for id_val in df["id"].unique():
            user_df = df[df["id"] == id_val]
            if len(user_df) == 0:
                continue
                
            features = {"id": id_val}
            
            # 工作日vs周末金额模式
            weekday_df = user_df[user_df["is_weekend"] == 0]
            weekend_df = user_df[user_df["is_weekend"] == 1]
            
            features["weekday_avg_amount"] = weekday_df["amount"].mean() if len(weekday_df) > 0 else 0
            features["weekend_avg_amount"] = weekend_df["amount"].mean() if len(weekend_df) > 0 else 0
            features["weekend_weekday_ratio"] = safe_div(features["weekend_avg_amount"], features["weekday_avg_amount"])
            
            # 不同时段的金额模式
            morning_df = user_df[user_df["hour"].between(6, 11)]
            afternoon_df = user_df[user_df["hour"].between(12, 17)]
            evening_df = user_df[user_df["hour"].between(18, 23)]
            night_df = user_df[(user_df["hour"] >= 0) & (user_df["hour"] <= 5)]
            
            features["morning_avg_amount"] = morning_df["amount"].mean() if len(morning_df) > 0 else 0
            features["afternoon_avg_amount"] = afternoon_df["amount"].mean() if len(afternoon_df) > 0 else 0
            features["evening_avg_amount"] = evening_df["amount"].mean() if len(evening_df) > 0 else 0
            features["night_avg_amount"] = night_df["amount"].mean() if len(night_df) > 0 else 0
            
            # 金额时间波动性
            features["amount_hour_corr"] = user_df["amount"].corr(user_df["hour"]) if len(user_df) > 1 else 0
            features["amount_weekday_corr"] = user_df["amount"].corr(user_df["day_of_week"]) if len(user_df) > 1 else 0
            
            amount_features.append(features)
        
        return pd.DataFrame(amount_features)
    
    # 3. 趋势和季节性特征
    def extract_trend_seasonal_features(bank_df):
        if bank_df is None or len(bank_df) == 0:
            return pd.DataFrame({"id": []})
        
        df = bank_df.copy()
        df["time_dt"] = pd.to_datetime(df["time"], unit="s", utc=True).dt.tz_convert(None)
        df["month"] = df["time_dt"].dt.to_period("M").astype(str)
        
        trend_features = []
        for id_val in df["id"].unique():
            user_df = df[df["id"] == id_val]
            if len(user_df) == 0:
                continue
                
            features = {"id": id_val}
            
            # 按月聚合
            monthly = user_df.groupby("month").agg({
                "amount": ["sum", "mean", "std", "count"],
                "direction": "sum"  # 支出次数
            }).reset_index()
            monthly.columns = ["month", "amount_sum", "amount_mean", "amount_std", "txn_count", "expense_count"]
            monthly["income_count"] = monthly["txn_count"] - monthly["expense_count"]
            monthly["expense_ratio"] = safe_div(monthly["expense_count"], monthly["txn_count"])
            
            if len(monthly) > 1:
                # 趋势特征
                x = np.arange(len(monthly))
                for col in ["amount_sum", "amount_mean", "txn_count", "expense_ratio"]:
                    y = monthly[col].values
                    if np.std(y) > 0:
                        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
                        features[f"trend_{col}_slope"] = slope
                        features[f"trend_{col}_r2"] = r_value ** 2
                    else:
                        features[f"trend_{col}_slope"] = 0
                        features[f"trend_{col}_r2"] = 0
                
                # 季节性特征（月度波动）
                features["monthly_amount_cv"] = monthly["amount_sum"].std() / monthly["amount_sum"].mean() if monthly["amount_sum"].mean() > 0 else 0
                features["monthly_txn_cv"] = monthly["txn_count"].std() / monthly["txn_count"].mean() if monthly["txn_count"].mean() > 0 else 0
                
                # 最近vs历史对比
                recent_months = monthly.tail(3)
                historical_months = monthly.iloc[:-3] if len(monthly) > 3 else monthly
                
                if len(recent_months) > 0 and len(historical_months) > 0:
                    features["recent_vs_hist_amount"] = safe_div(recent_months["amount_sum"].mean(), historical_months["amount_sum"].mean())
                    features["recent_vs_hist_txn"] = safe_div(recent_months["txn_count"].mean(), historical_months["txn_count"].mean())
                else:
                    features["recent_vs_hist_amount"] = 1.0
                    features["recent_vs_hist_txn"] = 1.0
            else:
                # 单月数据，设置默认值
                for col in ["amount_sum", "amount_mean", "txn_count", "expense_ratio"]:
                    features[f"trend_{col}_slope"] = 0
                    features[f"trend_{col}_r2"] = 0
                features["monthly_amount_cv"] = 0
                features["monthly_txn_cv"] = 0
                features["recent_vs_hist_amount"] = 1.0
                features["recent_vs_hist_txn"] = 1.0
            
            trend_features.append(features)
        
        return pd.DataFrame(trend_features)
    
    # 4. 风险时间模式特征
    def extract_risk_time_patterns(bank_df):
        if bank_df is None or len(bank_df) == 0:
            return pd.DataFrame({"id": []})
        
        df = bank_df.copy()
        df["time_dt"] = pd.to_datetime(df["time"], unit="s", utc=True).dt.tz_convert(None)
        df["hour"] = df["time_dt"].dt.hour
        df["day_of_week"] = df["time_dt"].dt.dayofweek
        
        risk_features = []
        for id_val in df["id"].unique():
            user_df = df[df["id"] == id_val]
            if len(user_df) == 0:
                continue
                
            features = {"id": id_val}
            
            # 异常时间交易
            features["late_night_ratio"] = (user_df["hour"].between(23, 5)).mean()  # 深夜交易比例
            features["early_morning_ratio"] = (user_df["hour"].between(0, 6)).mean()  # 凌晨交易比例
            
            # 高频交易时段
            hour_counts = user_df["hour"].value_counts()
            features["peak_hour_ratio"] = hour_counts.max() / len(user_df) if len(user_df) > 0 else 0
            
            # 交易时间集中度
            features["hour_concentration"] = (hour_counts ** 2).sum() / (len(user_df) ** 2) if len(user_df) > 0 else 0
            
            # 连续交易模式
            user_df_sorted = user_df.sort_values("time_dt")
            if len(user_df_sorted) > 1:
                time_diffs = user_df_sorted["time_dt"].diff().dt.total_seconds() / 60  # 分钟
                features["consecutive_txn_ratio"] = (time_diffs < 5).mean()  # 5分钟内连续交易比例
                features["rapid_txn_ratio"] = (time_diffs < 1).mean()  # 1分钟内连续交易比例
            else:
                features["consecutive_txn_ratio"] = 0
                features["rapid_txn_ratio"] = 0
            
            risk_features.append(features)
        
        return pd.DataFrame(risk_features)
    
    # 5. 主表时间特征
    def extract_main_time_features(main_df):
        df = main_df.copy()
        features = df[["id"]].copy()
        
        # 时间差特征
        if "issue_time" in df.columns and "record_time" in df.columns:
            features["issue_to_record_days"] = (df["record_time"] - df["issue_time"]) / (24 * 3600)
            features["issue_to_record_hours"] = (df["record_time"] - df["issue_time"]) / 3600
        
        if "history_time" in df.columns and "record_time" in df.columns:
            features["history_to_record_days"] = (df["record_time"] - df["history_time"]) / (24 * 3600)
            features["history_to_record_hours"] = (df["record_time"] - df["history_time"]) / 3600
        
        # 时间窗口特征
        if "issue_time" in df.columns:
            issue_dt = pd.to_datetime(df["issue_time"], unit="s")
            features["issue_hour"] = issue_dt.dt.hour
            features["issue_day_of_week"] = issue_dt.dt.dayofweek
            features["issue_month"] = issue_dt.dt.month
            features["issue_quarter"] = issue_dt.dt.quarter
            features["issue_is_weekend"] = issue_dt.dt.dayofweek.isin([5, 6]).astype(int)
        
        if "record_time" in df.columns:
            record_dt = pd.to_datetime(df["record_time"], unit="s")
            features["record_hour"] = record_dt.dt.hour
            features["record_day_of_week"] = record_dt.dt.dayofweek
            features["record_month"] = record_dt.dt.month
            features["record_quarter"] = record_dt.dt.quarter
            features["record_is_weekend"] = record_dt.dt.dayofweek.isin([5, 6]).astype(int)
        
        return features
    
    # 构建所有时间特征
    print("[TIME] Building bank time features...")
    tr_bank_time = extract_bank_time_features(train_bank)
    te_bank_time = extract_bank_time_features(test_bank)
    
    print("[TIME] Building amount time patterns...")
    tr_amount_time = extract_amount_time_patterns(train_bank)
    te_amount_time = extract_amount_time_patterns(test_bank)
    
    print("[TIME] Building trend seasonal features...")
    tr_trend = extract_trend_seasonal_features(train_bank)
    te_trend = extract_trend_seasonal_features(test_bank)
    
    print("[TIME] Building risk time patterns...")
    tr_risk = extract_risk_time_patterns(train_bank)
    te_risk = extract_risk_time_patterns(test_bank)
    
    print("[TIME] Building main time features...")
    tr_main_time = extract_main_time_features(train_main)
    te_main_time = extract_main_time_features(test_main)
    
    # 合并所有特征
    print("[TIME] Merging all time features...")
    tr_time = tr_bank_time.merge(tr_amount_time, on="id", how="outer")\
                         .merge(tr_trend, on="id", how="outer")\
                         .merge(tr_risk, on="id", how="outer")\
                         .merge(tr_main_time, on="id", how="outer")
    
    te_time = te_bank_time.merge(te_amount_time, on="id", how="outer")\
                         .merge(te_trend, on="id", how="outer")\
                         .merge(te_risk, on="id", how="outer")\
                         .merge(te_main_time, on="id", how="outer")
    
    # 添加time_前缀
    time_cols = [c for c in tr_time.columns if c != "id"]
    tr_time = tr_time.rename(columns={c: f"time_{c}" for c in time_cols})
    te_time = te_time.rename(columns={c: f"time_{c}" for c in time_cols})
    
    # 填充缺失值
    tr_time = tr_time.fillna(0.0)
    te_time = te_time.fillna(0.0)
    
    return tr_time, te_time

# --------- 主流程 ---------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base_train", default=DEF_BASE_TRAIN)
    ap.add_argument("--base_test",  default=DEF_BASE_TEST)
    ap.add_argument("--train_main", default=DEF_TRAIN_MAIN)
    ap.add_argument("--train_bank", default=DEF_TRAIN_BANK)
    ap.add_argument("--test_main",  default=DEF_TEST_MAIN)
    ap.add_argument("--test_bank",  default=DEF_TEST_BANK)
    ap.add_argument("--out_root",   default="./out")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    dir_time  = os.path.join(args.out_root, "time_out"); ensure_dir(dir_time)
    dir_merge = os.path.join(args.out_root, "merged");   ensure_dir(dir_merge)
    dir_scan  = os.path.join(args.out_root, "scan");     ensure_dir(dir_scan)
    dir_final = os.path.join(args.out_root, "final");    ensure_dir(dir_final)

    # 1) 读取基线
    base_tr, base_te = load_baseline(args.base_train, args.base_test, args.train_main)
    y = base_tr["label"].astype(int)
    base_feat_cols = [c for c in base_tr.columns if c not in ["id","label"]]

    # 2) 读原始数据
    tr_main = pd.read_csv(args.train_main)
    te_main = pd.read_csv(args.test_main)
    tr_bank = pd.read_csv(args.train_bank)
    te_bank = pd.read_csv(args.test_bank)

    # 3) 构建 TIME 新特征
    time_tr, time_te = build_time_features(tr_main, te_main, tr_bank, te_bank)
    time_tr.to_csv(os.path.join(dir_time, "features_time_train.csv"), index=False)
    time_te.to_csv(os.path.join(dir_time, "features_time_test.csv"), index=False)

    # 4) 与基线拼接
    time_cols = [c for c in time_tr.columns if c != "id"]
    tr_merged = base_tr.merge(time_tr, on="id", how="left")
    te_merged = base_te.merge(time_te, on="id", how="left")
    tr_merged[time_cols] = tr_merged[time_cols].fillna(0.0)
    te_merged[time_cols] = te_merged[time_cols].fillna(0.0)
    tr_merged.to_csv(os.path.join(dir_merge, "time_merged_train.csv"), index=False)
    te_merged.to_csv(os.path.join(dir_merge, "time_merged_test.csv"), index=False)


    print("== DONE TIME ==")

if __name__ == "__main__":
    main()
