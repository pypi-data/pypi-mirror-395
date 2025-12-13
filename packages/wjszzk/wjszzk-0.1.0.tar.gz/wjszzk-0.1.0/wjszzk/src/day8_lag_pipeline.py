#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day8 - LAG 批次：滞后和滑动窗口特征构建
构建基于时间序列的延迟效应特征，包括：
1. 滞后特征：1-3期滞后、季节性滞后、年度滞后等
2. 滑动窗口特征：3期滑动平均、6期滑动统计、12期滑动趋势等
3. 变化率特征：环比变化、同比变化、累积变化等
与基线特征合并后输出，供后续特征工程使用
"""

import os
import json
import argparse
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

# ----------------------------
# 工具函数
# ----------------------------
def ensure_dir(p: str):
    os.makedirs(p, exist_ok=True)

def read_csv(path: str):
    return pd.read_csv(path)

def safe_divide(a: pd.Series, b: pd.Series, fill_value: float = 0.0) -> pd.Series:
    """安全除法，避免除零错误"""
    return np.where(b != 0, a / b, fill_value)

def safe_log1p(x: pd.Series) -> pd.Series:
    """安全的log1p变换"""
    return np.log1p(np.abs(x))


# ----------------------------
# LAG特征构建核心函数
# ----------------------------
def build_lag_features(tr_main: pd.DataFrame, te_main: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """构建LAG批次特征"""
    
    print("[INFO] 开始构建LAG批次特征...")
    
    # 复制数据
    tr_lag = tr_main.copy()
    te_lag = te_main.copy()
    
    # 1. 滞后特征
    print("[INFO] 构建滞后特征...")
    tr_lag, te_lag = build_lag_features_core(tr_lag, te_lag)
    
    # 2. 滑动窗口特征
    print("[INFO] 构建滑动窗口特征...")
    tr_lag, te_lag = build_rolling_features(tr_lag, te_lag)
    
    # 3. 变化率特征
    print("[INFO] 构建变化率特征...")
    tr_lag, te_lag = build_change_rate_features(tr_lag, te_lag)
    
    # 4. 特征清理和优化
    print("[INFO] 特征清理和优化...")
    tr_lag, te_lag = clean_and_optimize_features(tr_lag, te_lag)
    
    print(f"[INFO] LAG特征构建完成，训练集: {tr_lag.shape}, 测试集: {te_lag.shape}")
    
    return tr_lag, te_lag

def build_lag_features_core(tr_main: pd.DataFrame, te_main: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """构建滞后特征"""
    
    # 基于银行流水数据的滞后特征
    lag_features = ['bank_income_sum', 'bank_expense_sum', 'bank_net_sum', 'bank_txn_count_m']
    
    for feature in lag_features:
        if feature in tr_main.columns:
            # 1期滞后
            tr_main[f'lag_{feature}_1m'] = tr_main[feature].shift(1)
            te_main[f'lag_{feature}_1m'] = te_main[feature].shift(1)
            
            # 2期滞后
            tr_main[f'lag_{feature}_2m'] = tr_main[feature].shift(2)
            te_main[f'lag_{feature}_2m'] = te_main[feature].shift(2)
            
            # 3期滞后
            tr_main[f'lag_{feature}_3m'] = tr_main[feature].shift(3)
            te_main[f'lag_{feature}_3m'] = te_main[feature].shift(3)
            
            # 季节性滞后（3个月）
            tr_main[f'lag_{feature}_3m_seasonal'] = tr_main[feature].shift(3)
            te_main[f'lag_{feature}_3m_seasonal'] = te_main[feature].shift(3)
            
            # 年度滞后（12个月）
            tr_main[f'lag_{feature}_12m'] = tr_main[feature].shift(12)
            te_main[f'lag_{feature}_12m'] = te_main[feature].shift(12)
    
    # 基于时间特征的滞后
    time_features = ['time_weekend_ratio', 'time_weekday_entropy', 'time_consecutive_txn_ratio']
    
    for feature in time_features:
        if feature in tr_main.columns:
            # 1期滞后
            tr_main[f'lag_{feature}_1m'] = tr_main[feature].shift(1)
            te_main[f'lag_{feature}_1m'] = te_main[feature].shift(1)
            
            # 3期滞后
            tr_main[f'lag_{feature}_3m'] = tr_main[feature].shift(3)
            te_main[f'lag_{feature}_3m'] = te_main[feature].shift(3)
    
    return tr_main, te_main

def build_rolling_features(tr_main: pd.DataFrame, te_main: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """构建滑动窗口特征"""
    
    # 基于银行流水数据的滑动窗口特征
    rolling_features = ['bank_income_sum', 'bank_expense_sum', 'bank_net_sum', 'bank_txn_count_m']
    
    for feature in rolling_features:
        if feature in tr_main.columns:
            # 3期滑动平均
            tr_main[f'rolling_{feature}_3m_mean'] = tr_main[feature].rolling(window=3, min_periods=1).mean()
            te_main[f'rolling_{feature}_3m_mean'] = te_main[feature].rolling(window=3, min_periods=1).mean()
            
            # 3期滑动标准差
            tr_main[f'rolling_{feature}_3m_std'] = tr_main[feature].rolling(window=3, min_periods=1).std()
            te_main[f'rolling_{feature}_3m_std'] = te_main[feature].rolling(window=3, min_periods=1).std()
            
            # 6期滑动平均
            tr_main[f'rolling_{feature}_6m_mean'] = tr_main[feature].rolling(window=6, min_periods=1).mean()
            te_main[f'rolling_{feature}_6m_mean'] = te_main[feature].rolling(window=6, min_periods=1).mean()
            
            # 6期滑动标准差
            tr_main[f'rolling_{feature}_6m_std'] = tr_main[feature].rolling(window=6, min_periods=1).std()
            te_main[f'rolling_{feature}_6m_std'] = te_main[feature].rolling(window=6, min_periods=1).std()
            
            # 6期滑动最大值
            tr_main[f'rolling_{feature}_6m_max'] = tr_main[feature].rolling(window=6, min_periods=1).max()
            te_main[f'rolling_{feature}_6m_max'] = te_main[feature].rolling(window=6, min_periods=1).max()
            
            # 6期滑动最小值
            tr_main[f'rolling_{feature}_6m_min'] = tr_main[feature].rolling(window=6, min_periods=1).min()
            te_main[f'rolling_{feature}_6m_min'] = te_main[feature].rolling(window=6, min_periods=1).min()
            
            # 12期滑动平均
            tr_main[f'rolling_{feature}_12m_mean'] = tr_main[feature].rolling(window=12, min_periods=1).mean()
            te_main[f'rolling_{feature}_12m_mean'] = te_main[feature].rolling(window=12, min_periods=1).mean()
            
            # 12期滑动趋势（简单线性回归斜率）
            tr_main[f'rolling_{feature}_12m_trend'] = calculate_rolling_trend(tr_main[feature], window=12)
            te_main[f'rolling_{feature}_12m_trend'] = calculate_rolling_trend(te_main[feature], window=12)
    
    # 基于时间特征的滑动窗口
    time_rolling_features = ['time_weekend_ratio', 'time_weekday_entropy']
    
    for feature in time_rolling_features:
        if feature in tr_main.columns:
            # 3期滑动平均
            tr_main[f'rolling_{feature}_3m_mean'] = tr_main[feature].rolling(window=3, min_periods=1).mean()
            te_main[f'rolling_{feature}_3m_mean'] = te_main[feature].rolling(window=3, min_periods=1).mean()
            
            # 6期滑动平均
            tr_main[f'rolling_{feature}_6m_mean'] = tr_main[feature].rolling(window=6, min_periods=1).mean()
            te_main[f'rolling_{feature}_6m_mean'] = te_main[feature].rolling(window=6, min_periods=1).mean()
    
    return tr_main, te_main

def calculate_rolling_trend(series: pd.Series, window: int = 12) -> pd.Series:
    """计算滑动窗口的趋势（线性回归斜率）"""
    def linear_trend(x):
        if len(x) < 2:
            return 0.0
        try:
            # 简单的线性趋势计算
            n = len(x)
            x_coords = np.arange(n)
            slope = (n * np.sum(x_coords * x) - np.sum(x_coords) * np.sum(x)) / (n * np.sum(x_coords**2) - np.sum(x_coords)**2)
            return slope if not np.isnan(slope) else 0.0
        except:
            return 0.0
    
    return series.rolling(window=window, min_periods=2).apply(linear_trend, raw=True)

def build_change_rate_features(tr_main: pd.DataFrame, te_main: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """构建变化率特征"""
    
    # 基于银行流水数据的变化率特征
    change_features = ['bank_income_sum', 'bank_expense_sum', 'bank_net_sum', 'bank_txn_count_m']
    
    for feature in change_features:
        if feature in tr_main.columns:
            # 环比变化（1期）
            tr_main[f'pct_change_{feature}_1m'] = tr_main[feature].pct_change(periods=1)
            te_main[f'pct_change_{feature}_1m'] = te_main[feature].pct_change(periods=1)
            
            # 环比变化（3期）
            tr_main[f'pct_change_{feature}_3m'] = tr_main[feature].pct_change(periods=3)
            te_main[f'pct_change_{feature}_3m'] = te_main[feature].pct_change(periods=3)
            
            # 同比变化（12期）
            tr_main[f'pct_change_{feature}_12m'] = tr_main[feature].pct_change(periods=12)
            te_main[f'pct_change_{feature}_12m'] = te_main[feature].pct_change(periods=12)
            
            # 累积变化（6期）
            tr_main[f'cumsum_{feature}_6m'] = tr_main[feature].rolling(window=6, min_periods=1).sum()
            te_main[f'cumsum_{feature}_6m'] = te_main[feature].rolling(window=6, min_periods=1).sum()
            
            # 累积变化（12期）
            tr_main[f'cumsum_{feature}_12m'] = tr_main[feature].rolling(window=12, min_periods=1).sum()
            te_main[f'cumsum_{feature}_12m'] = te_main[feature].rolling(window=12, min_periods=1).sum()
    
    # 基于时间特征的变化率
    time_change_features = ['time_weekend_ratio', 'time_weekday_entropy']
    
    for feature in time_change_features:
        if feature in tr_main.columns:
            # 环比变化
            tr_main[f'pct_change_{feature}_1m'] = tr_main[feature].pct_change(periods=1)
            te_main[f'pct_change_{feature}_1m'] = te_main[feature].pct_change(periods=1)
            
            # 累积变化
            tr_main[f'cumsum_{feature}_6m'] = tr_main[feature].rolling(window=6, min_periods=1).sum()
            te_main[f'cumsum_{feature}_6m'] = te_main[feature].rolling(window=6, min_periods=1).sum()
    
    return tr_main, te_main

def clean_and_optimize_features(tr_main: pd.DataFrame, te_main: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """特征清理和优化"""
    
    # 处理无穷大值
    tr_main = tr_main.replace([np.inf, -np.inf], np.nan)
    te_main = te_main.replace([np.inf, -np.inf], np.nan)
    
    # 处理异常值（超过99.9%分位数的值）
    for col in tr_main.columns:
        if col in ['id', 'label']:
            continue
        if tr_main[col].dtype in ['float64', 'float32', 'int64', 'int32']:
            q99 = tr_main[col].quantile(0.999)
            q01 = tr_main[col].quantile(0.001)
            tr_main[col] = tr_main[col].clip(lower=q01, upper=q99)
            te_main[col] = te_main[col].clip(lower=q01, upper=q99)
    
    # 填充缺失值
    for col in tr_main.columns:
        if col in ['id', 'label']:
            continue
        if tr_main[col].isnull().sum() > 0:
            if tr_main[col].dtype in ['float64', 'float32']:
                median_val = tr_main[col].median()
                tr_main[col] = tr_main[col].fillna(median_val)
                te_main[col] = te_main[col].fillna(median_val)
            else:
                mode_val = tr_main[col].mode().iloc[0] if len(tr_main[col].mode()) > 0 else 0
                tr_main[col] = tr_main[col].fillna(mode_val)
                te_main[col] = te_main[col].fillna(mode_val)
    
    return tr_main, te_main

# ----------------------------
# 主流程
# ----------------------------
def main():
    parser = argparse.ArgumentParser(description="Day8 LAG特征构建")
    parser.add_argument("--base_train", type=str, required=True,
                       help="基础训练特征文件路径")
    parser.add_argument("--base_test", type=str, required=True,
                       help="基础测试特征文件路径")
    parser.add_argument("--train_main", type=str, required=True,
                       help="训练集主表文件路径")
    parser.add_argument("--test_main", type=str, required=True,
                       help="测试集主表文件路径")
    parser.add_argument("--train_bank", type=str, required=True,
                       help="训练集银行流水文件路径")
    parser.add_argument("--test_bank", type=str, required=True,
                       help="测试集银行流水文件路径")
    parser.add_argument("--out_dir", type=str, required=True,
                       help="输出目录")
    parser.add_argument("--seed", type=int, default=42,
                       help="随机种子")
    
    args = parser.parse_args()
    
    # 设置随机种子
    np.random.seed(args.seed)
    
    # 确保目录存在
    ensure_dir(args.out_dir)
    ensure_dir(f"{args.out_dir}/lag")
    ensure_dir(f"{args.out_dir}/merge")
    
    print(f"[INFO] 开始Day8 LAG特征构建...")
    print(f"[INFO] 输出目录: {args.out_dir}")
    
    # 读取基础特征
    try:
        print(f"[INFO] 读取训练特征: {args.base_train}")
        print(f"[INFO] 读取测试特征: {args.base_test}")
        
        tr_main = read_csv(args.base_train)
        te_main = read_csv(args.base_test)
        
    except Exception as e:
        print(f"[ERROR] 读取基础特征失败: {e}")
        return
    
    print(f"[INFO] 训练集形状: {tr_main.shape}")
    print(f"[INFO] 测试集形状: {te_main.shape}")
    
    # 提取标签
    y = None
    if 'label' in tr_main.columns:
        y = tr_main['label'].values
        print(f"[INFO] 标签分布: {np.bincount(y)}")
    
    # 构建LAG特征
    tr_lag, te_lag = build_lag_features(tr_main, te_main)
    
    # 保存特征
    print("[INFO] 保存LAG特征...")
    tr_lag.to_csv(f"{args.out_dir}/lag/features_lag_train.csv", index=False)
    te_lag.to_csv(f"{args.out_dir}/lag/features_lag_test.csv", index=False)
    
    # 合并特征
    print("[INFO] 合并特征...")
    tr_merged = tr_lag.copy()
    te_merged = te_lag.copy()
    
    tr_merged.to_csv(f"{args.out_dir}/merge/lag_merged_train.csv", index=False)
    te_merged.to_csv(f"{args.out_dir}/merge/lag_merged_test.csv", index=False)

    
    print(f"[INFO] Day8 LAG特征构建完成！")
    print(f"[INFO] 输出文件:")
    print(f"  - 训练特征: {args.out_dir}/lag/features_lag_train.csv")
    print(f"  - 测试特征: {args.out_dir}/lag/features_lag_test.csv")
    print(f"  - 合并训练: {args.out_dir}/merge/lag_merged_train.csv")
    print(f"  - 合并测试: {args.out_dir}/merge/lag_merged_test.csv")

if __name__ == "__main__":
    main()

