#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day8 - CLUSTER 批次：聚类和分组特征构建
构建基于用户行为模式的相似性特征，包括：
1. 行为聚类特征：交易模式聚类、时间偏好聚类、风险偏好聚类等
2. 财务聚类特征：收入支出聚类、债务负担聚类、稳定性聚类等
3. 组合聚类特征：综合行为聚类、风险等级聚类等
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
# CLUSTER特征构建核心函数
# ----------------------------
def build_cluster_features(tr_main: pd.DataFrame, te_main: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """构建CLUSTER批次特征"""
    
    print("[INFO] 开始构建CLUSTER批次特征...")
    
    # 复制数据
    tr_cluster = tr_main.copy()
    te_cluster = te_main.copy()
    
    # 1. 行为聚类特征
    print("[INFO] 构建行为聚类特征...")
    tr_cluster, te_cluster = build_behavior_cluster_features(tr_cluster, te_cluster)
    
    # 2. 财务聚类特征
    print("[INFO] 构建财务聚类特征...")
    tr_cluster, te_cluster = build_financial_cluster_features(tr_cluster, te_cluster)
    
    # 3. 组合聚类特征
    print("[INFO] 构建组合聚类特征...")
    tr_cluster, te_cluster = build_comprehensive_cluster_features(tr_cluster, te_cluster)
    
    # 4. 特征清理和优化
    print("[INFO] 特征清理和优化...")
    tr_cluster, te_cluster = clean_and_optimize_features(tr_cluster, te_cluster)
    
    print(f"[INFO] CLUSTER特征构建完成，训练集: {tr_cluster.shape}, 测试集: {te_cluster.shape}")
    
    return tr_cluster, te_cluster

def build_behavior_cluster_features(tr_main: pd.DataFrame, te_main: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """构建行为聚类特征"""
    
    # 交易模式聚类
    if 'bank_txn_count_m' in tr_main.columns and 'bank_income_sum' in tr_main.columns:
        # 交易频率×金额效率
        tr_main['cluster_txn_pattern'] = safe_divide(tr_main['bank_income_sum'], tr_main['bank_txn_count_m'], 0)
        te_main['cluster_txn_pattern'] = safe_divide(te_main['bank_income_sum'], te_main['bank_txn_count_m'], 0)
        
        # 标准化
        tr_main['cluster_txn_pattern'] = (tr_main['cluster_txn_pattern'] - tr_main['cluster_txn_pattern'].mean()) / tr_main['cluster_txn_pattern'].std()
        te_main['cluster_txn_pattern'] = (te_main['cluster_txn_pattern'] - te_main['cluster_txn_pattern'].mean()) / te_main['cluster_txn_pattern'].std()
        
        # 分箱聚类
        tr_main['cluster_txn_pattern_bin'] = pd.qcut(tr_main['cluster_txn_pattern'], q=5, labels=False, duplicates='drop')
        te_main['cluster_txn_pattern_bin'] = pd.qcut(te_main['cluster_txn_pattern'], q=5, labels=False, duplicates='drop')
    
    # 金额模式聚类
    if 'bank_income_sum' in tr_main.columns and 'bank_expense_sum' in tr_main.columns:
        # 收入支出比率
        tr_main['cluster_amount_pattern'] = safe_divide(tr_main['bank_income_sum'], tr_main['bank_expense_sum'], 1)
        te_main['cluster_amount_pattern'] = safe_divide(te_main['bank_income_sum'], te_main['bank_expense_sum'], 1)
        
        # 标准化
        tr_main['cluster_amount_pattern'] = (tr_main['cluster_amount_pattern'] - tr_main['cluster_amount_pattern'].mean()) / tr_main['cluster_amount_pattern'].std()
        te_main['cluster_amount_pattern'] = (te_main['cluster_amount_pattern'] - te_main['cluster_amount_pattern'].mean()) / te_main['cluster_amount_pattern'].std()
        
        # 分箱聚类
        tr_main['cluster_amount_pattern_bin'] = pd.qcut(tr_main['cluster_amount_pattern'], q=5, labels=False, duplicates='drop')
        te_main['cluster_amount_pattern_bin'] = pd.qcut(te_main['cluster_amount_pattern'], q=5, labels=False, duplicates='drop')
    
    # 时间偏好聚类
    if 'time_weekend_ratio' in tr_main.columns and 'time_weekday_entropy' in tr_main.columns:
        # 周末偏好×时间熵
        tr_main['cluster_time_preference'] = tr_main['time_weekend_ratio'] * tr_main['time_weekday_entropy']
        te_main['cluster_time_preference'] = te_main['time_weekend_ratio'] * te_main['time_weekday_entropy']
        
        # 标准化
        tr_main['cluster_time_preference'] = (tr_main['cluster_time_preference'] - tr_main['cluster_time_preference'].mean()) / tr_main['cluster_time_preference'].std()
        te_main['cluster_time_preference'] = (te_main['cluster_time_preference'] - te_main['cluster_time_preference'].mean()) / te_main['cluster_time_preference'].std()
        
        # 分箱聚类
        tr_main['cluster_time_preference_bin'] = pd.qcut(tr_main['cluster_time_preference'], q=5, labels=False, duplicates='drop')
        te_main['cluster_time_preference_bin'] = pd.qcut(te_main['cluster_time_preference'], q=5, labels=False, duplicates='drop')
    
    # 频率偏好聚类
    if 'time_active_days' in tr_main.columns and 'time_total_days' in tr_main.columns:
        # 活跃度比率
        tr_main['cluster_frequency_preference'] = safe_divide(tr_main['time_active_days'], tr_main['time_total_days'], 0)
        te_main['cluster_frequency_preference'] = safe_divide(te_main['time_active_days'], te_main['time_total_days'], 0)
        
        # 标准化
        tr_main['cluster_frequency_preference'] = (tr_main['cluster_frequency_preference'] - tr_main['cluster_frequency_preference'].mean()) / tr_main['cluster_frequency_preference'].std()
        te_main['cluster_frequency_preference'] = (te_main['cluster_frequency_preference'] - te_main['cluster_frequency_preference'].mean()) / te_main['cluster_frequency_preference'].std()
        
        # 分箱聚类
        tr_main['cluster_frequency_preference_bin'] = pd.qcut(tr_main['cluster_frequency_preference'], q=5, labels=False, duplicates='drop')
        te_main['cluster_frequency_preference_bin'] = pd.qcut(te_main['cluster_frequency_preference'], q=5, labels=False, duplicates='drop')
    
    return tr_main, te_main

def build_financial_cluster_features(tr_main: pd.DataFrame, te_main: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """构建财务聚类特征"""
    
    # 收入支出聚类
    if 'bank_income_sum' in tr_main.columns and 'bank_expense_sum' in tr_main.columns:
        # 净收入比率
        tr_main['cluster_income_expense_profile'] = safe_divide(tr_main['bank_income_sum'] - tr_main['bank_expense_sum'], tr_main['bank_income_sum'], 0)
        te_main['cluster_income_expense_profile'] = safe_divide(te_main['bank_income_sum'] - te_main['bank_expense_sum'], te_main['bank_income_sum'], 0)
        
        # 标准化
        tr_main['cluster_income_expense_profile'] = (tr_main['cluster_income_expense_profile'] - tr_main['cluster_income_expense_profile'].mean()) / tr_main['cluster_income_expense_profile'].std()
        te_main['cluster_income_expense_profile'] = (te_main['cluster_income_expense_profile'] - te_main['cluster_income_expense_profile'].mean()) / te_main['cluster_income_expense_profile'].std()
        
        # 分箱聚类
        tr_main['cluster_income_expense_profile_bin'] = pd.qcut(tr_main['cluster_income_expense_profile'], q=5, labels=False, duplicates='drop')
        te_main['cluster_income_expense_profile_bin'] = pd.qcut(te_main['cluster_income_expense_profile'], q=5, labels=False, duplicates='drop')
    
    # 现金流聚类
    if 'bank_net_sum' in tr_main.columns and 'bank_income_sum' in tr_main.columns:
        # 净现金流比率
        tr_main['cluster_cash_flow_profile'] = safe_divide(tr_main['bank_net_sum'], tr_main['bank_income_sum'], 0)
        te_main['cluster_cash_flow_profile'] = safe_divide(te_main['bank_net_sum'], te_main['bank_income_sum'], 0)
        
        # 标准化
        tr_main['cluster_cash_flow_profile'] = (tr_main['cluster_cash_flow_profile'] - tr_main['cluster_cash_flow_profile'].mean()) / tr_main['cluster_cash_flow_profile'].std()
        te_main['cluster_cash_flow_profile'] = (te_main['cluster_cash_flow_profile'] - te_main['cluster_cash_flow_profile'].mean()) / te_main['cluster_cash_flow_profile'].std()
        
        # 分箱聚类
        tr_main['cluster_cash_flow_profile_bin'] = pd.qcut(tr_main['cluster_cash_flow_profile'], q=5, labels=False, duplicates='drop')
        te_main['cluster_cash_flow_profile_bin'] = pd.qcut(te_main['cluster_cash_flow_profile'], q=5, labels=False, duplicates='drop')
    
    # 债务负担聚类
    if 'DTI' in tr_main.columns and 'utilization' in tr_main.columns:
        # 综合债务负担
        tr_main['cluster_debt_profile'] = tr_main['DTI'] * tr_main['utilization']
        te_main['cluster_debt_profile'] = te_main['DTI'] * te_main['utilization']
        
        # 标准化
        tr_main['cluster_debt_profile'] = (tr_main['cluster_debt_profile'] - tr_main['cluster_debt_profile'].mean()) / tr_main['cluster_debt_profile'].std()
        te_main['cluster_debt_profile'] = (te_main['cluster_debt_profile'] - te_main['cluster_debt_profile'].mean()) / te_main['cluster_debt_profile'].std()
        
        # 分箱聚类
        tr_main['cluster_debt_profile_bin'] = pd.qcut(tr_main['cluster_debt_profile'], q=5, labels=False, duplicates='drop')
        te_main['cluster_debt_profile_bin'] = pd.qcut(te_main['cluster_debt_profile'], q=5, labels=False, duplicates='drop')
    
    # 信用聚类
    if 'level_ord' in tr_main.columns and 'buffer_months' in tr_main.columns:
        # 信用等级×缓冲月数
        tr_main['cluster_credit_profile'] = tr_main['level_ord'] * tr_main['buffer_months']
        te_main['cluster_credit_profile'] = te_main['level_ord'] * te_main['buffer_months']
        
        # 标准化
        tr_main['cluster_credit_profile'] = (tr_main['cluster_credit_profile'] - tr_main['cluster_credit_profile'].mean()) / tr_main['cluster_credit_profile'].std()
        te_main['cluster_credit_profile'] = (te_main['cluster_credit_profile'] - te_main['cluster_credit_profile'].mean()) / te_main['cluster_credit_profile'].std()
        
        # 分箱聚类
        tr_main['cluster_credit_profile_bin'] = pd.qcut(tr_main['cluster_credit_profile'], q=5, labels=False, duplicates='drop')
        te_main['cluster_credit_profile_bin'] = pd.qcut(te_main['cluster_credit_profile'], q=5, labels=False, duplicates='drop')
    
    # 稳定性聚类
    if 'time_monthly_amount_cv' in tr_main.columns and 'time_monthly_txn_cv' in tr_main.columns:
        # 金额和交易量的稳定性
        tr_main['cluster_stability_profile'] = 1.0 / (1.0 + tr_main['time_monthly_amount_cv'] + tr_main['time_monthly_txn_cv'])
        te_main['cluster_stability_profile'] = 1.0 / (1.0 + te_main['time_monthly_amount_cv'] + te_main['time_monthly_txn_cv'])
        
        # 标准化
        tr_main['cluster_stability_profile'] = (tr_main['cluster_stability_profile'] - tr_main['cluster_stability_profile'].mean()) / tr_main['cluster_stability_profile'].std()
        te_main['cluster_stability_profile'] = (te_main['cluster_stability_profile'] - te_main['cluster_stability_profile'].mean()) / te_main['cluster_stability_profile'].std()
        
        # 分箱聚类
        tr_main['cluster_stability_profile_bin'] = pd.qcut(tr_main['cluster_stability_profile'], q=5, labels=False, duplicates='drop')
        te_main['cluster_stability_profile_bin'] = pd.qcut(te_main['cluster_stability_profile'], q=5, labels=False, duplicates='drop')
    
    return tr_main, te_main

def build_comprehensive_cluster_features(tr_main: pd.DataFrame, te_main: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """构建组合聚类特征"""
    
    # 综合行为聚类
    behavior_features = ['cluster_txn_pattern', 'cluster_amount_pattern', 'cluster_time_preference', 'cluster_frequency_preference']
    available_behavior_features = [f for f in behavior_features if f in tr_main.columns]
    
    if len(available_behavior_features) > 0:
        # 计算综合行为得分
        tr_main['cluster_comprehensive_behavior'] = tr_main[available_behavior_features].mean(axis=1)
        te_main['cluster_comprehensive_behavior'] = te_main[available_behavior_features].mean(axis=1)
        
        # 标准化
        tr_main['cluster_comprehensive_behavior'] = (tr_main['cluster_comprehensive_behavior'] - tr_main['cluster_comprehensive_behavior'].mean()) / tr_main['cluster_comprehensive_behavior'].std()
        te_main['cluster_comprehensive_behavior'] = (te_main['cluster_comprehensive_behavior'] - te_main['cluster_comprehensive_behavior'].mean()) / te_main['cluster_comprehensive_behavior'].std()
        
        # 分箱聚类
        tr_main['cluster_comprehensive_behavior_bin'] = pd.qcut(tr_main['cluster_comprehensive_behavior'], q=5, labels=False, duplicates='drop')
        te_main['cluster_comprehensive_behavior_bin'] = pd.qcut(te_main['cluster_comprehensive_behavior'], q=5, labels=False, duplicates='drop')
    
    # 用户分段聚类
    financial_features = ['cluster_income_expense_profile', 'cluster_cash_flow_profile', 'cluster_debt_profile', 'cluster_credit_profile']
    available_financial_features = [f for f in financial_features if f in tr_main.columns]
    
    if len(available_financial_features) > 0:
        # 计算用户分段得分
        tr_main['cluster_user_segment'] = tr_main[available_financial_features].mean(axis=1)
        te_main['cluster_user_segment'] = te_main[available_financial_features].mean(axis=1)
        
        # 标准化
        tr_main['cluster_user_segment'] = (tr_main['cluster_user_segment'] - tr_main['cluster_user_segment'].mean()) / tr_main['cluster_user_segment'].std()
        te_main['cluster_user_segment'] = (te_main['cluster_user_segment'] - te_main['cluster_user_segment'].mean()) / te_main['cluster_user_segment'].std()
        
        # 分箱聚类
        tr_main['cluster_user_segment_bin'] = pd.qcut(tr_main['cluster_user_segment'], q=5, labels=False, duplicates='drop')
        te_main['cluster_user_segment_bin'] = pd.qcut(te_main['cluster_user_segment'], q=5, labels=False, duplicates='drop')
    
    # 风险等级聚类
    risk_features = ['cluster_debt_profile', 'cluster_stability_profile']
    available_risk_features = [f for f in risk_features if f in tr_main.columns]
    
    if len(available_risk_features) > 0:
        # 计算风险等级得分
        tr_main['cluster_risk_level'] = tr_main[available_risk_features].mean(axis=1)
        te_main['cluster_risk_level'] = te_main[available_risk_features].mean(axis=1)
        
        # 标准化
        tr_main['cluster_risk_level'] = (tr_main['cluster_risk_level'] - tr_main['cluster_risk_level'].mean()) / tr_main['cluster_risk_level'].std()
        te_main['cluster_risk_level'] = (te_main['cluster_risk_level'] - te_main['cluster_risk_level'].mean()) / te_main['cluster_risk_level'].std()
        
        # 分箱聚类
        tr_main['cluster_risk_level_bin'] = pd.qcut(tr_main['cluster_risk_level'], q=5, labels=False, duplicates='drop')
        te_main['cluster_risk_level_bin'] = pd.qcut(te_main['cluster_risk_level'], q=5, labels=False, duplicates='drop')
    
    # 信用等级聚类
    credit_features = ['cluster_credit_profile', 'cluster_stability_profile']
    available_credit_features = [f for f in credit_features if f in tr_main.columns]
    
    if len(available_credit_features) > 0:
        # 计算信用等级得分
        tr_main['cluster_credit_grade'] = tr_main[available_credit_features].mean(axis=1)
        te_main['cluster_credit_grade'] = te_main[available_credit_features].mean(axis=1)
        
        # 标准化
        tr_main['cluster_credit_grade'] = (tr_main['cluster_credit_grade'] - tr_main['cluster_credit_grade'].mean()) / tr_main['cluster_credit_grade'].std()
        te_main['cluster_credit_grade'] = (te_main['cluster_credit_grade'] - te_main['cluster_credit_grade'].mean()) / te_main['cluster_credit_grade'].std()
        
        # 分箱聚类
        tr_main['cluster_credit_grade_bin'] = pd.qcut(tr_main['cluster_credit_grade'], q=5, labels=False, duplicates='drop')
        te_main['cluster_credit_grade_bin'] = pd.qcut(te_main['cluster_credit_grade'], q=5, labels=False, duplicates='drop')
    
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
    parser = argparse.ArgumentParser(description="Day8 CLUSTER特征构建")
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
    ensure_dir(f"{args.out_dir}/cluster")
    ensure_dir(f"{args.out_dir}/merge")
    
    print(f"[INFO] 开始Day8 CLUSTER特征构建...")
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
    
    # 构建CLUSTER特征
    tr_cluster, te_cluster = build_cluster_features(tr_main, te_main)
    
    # 保存特征
    print("[INFO] 保存CLUSTER特征...")
    tr_cluster.to_csv(f"{args.out_dir}/cluster/features_cluster_train.csv", index=False)
    te_cluster.to_csv(f"{args.out_dir}/cluster/features_cluster_test.csv", index=False)
    
    # 合并特征
    print("[INFO] 合并特征...")
    tr_merged = tr_cluster.copy()
    te_merged = te_cluster.copy()
    
    tr_merged.to_csv(f"{args.out_dir}/merge/cluster_merged_train.csv", index=False)
    te_merged.to_csv(f"{args.out_dir}/merge/cluster_merged_test.csv", index=False)
    
    
    print(f"[INFO] Day8 CLUSTER特征构建完成！")
    print(f"[INFO] 输出文件:")
    print(f"  - 训练特征: {args.out_dir}/cluster/features_cluster_train.csv")
    print(f"  - 测试特征: {args.out_dir}/cluster/features_cluster_test.csv")
    print(f"  - 合并训练: {args.out_dir}/merge/cluster_merged_train.csv")
    print(f"  - 合并测试: {args.out_dir}/merge/cluster_merged_test.csv")

if __name__ == "__main__":
    main()

