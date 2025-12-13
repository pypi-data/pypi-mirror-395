#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day8 - RATIO 批次：比率和比例特征构建
构建基于现有数值特征的比值关系特征，包括：
1. 财务比率特征：债务覆盖率、流动性比率、效率比率等
2. 时间比率特征：活跃度比率、交易密度比率、趋势稳定性比率等
3. 风险比率特征：违约风险比率、信用风险比率、行为风险比率等
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

def clip_extreme_values(x: pd.Series, lower_percentile: float = 0.01, upper_percentile: float = 0.99) -> pd.Series:
    """截断极端值"""
    lower = x.quantile(lower_percentile)
    upper = x.quantile(upper_percentile)
    return x.clip(lower=lower, upper=upper)


# ----------------------------
# RATIO特征构建核心函数
# ----------------------------
def build_ratio_features(tr_main: pd.DataFrame, te_main: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """构建RATIO批次特征"""
    
    print("[INFO] 开始构建RATIO批次特征...")
    
    # 复制数据
    tr_ratio = tr_main.copy()
    te_ratio = te_main.copy()
    
    # 1. 财务比率特征
    print("[INFO] 构建财务比率特征...")
    tr_ratio, te_ratio = build_financial_ratio_features(tr_ratio, te_ratio)
    
    # 2. 时间比率特征
    print("[INFO] 构建时间比率特征...")
    tr_ratio, te_ratio = build_time_ratio_features(tr_ratio, te_ratio)
    
    # 3. 风险比率特征
    print("[INFO] 构建风险比率特征...")
    tr_ratio, te_ratio = build_risk_ratio_features(tr_ratio, te_ratio)
    
    # 4. 特征清理和优化
    print("[INFO] 特征清理和优化...")
    tr_ratio, te_ratio = clean_and_optimize_features(tr_ratio, te_ratio)
    
    print(f"[INFO] RATIO特征构建完成，训练集: {tr_ratio.shape}, 测试集: {te_ratio.shape}")
    
    return tr_ratio, te_ratio

def build_financial_ratio_features(tr_main: pd.DataFrame, te_main: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """构建财务比率特征"""
    
    # 债务覆盖率
    if 'raw_loan' in tr_main.columns and 'bank_income_sum' in tr_main.columns:
        tr_main['ratio_debt_coverage'] = safe_divide(tr_main['raw_loan'], tr_main['bank_income_sum'], 0)
        te_main['ratio_debt_coverage'] = safe_divide(te_main['raw_loan'], te_main['bank_income_sum'], 0)
        
        tr_main['ratio_debt_coverage_log'] = safe_log1p(tr_main['ratio_debt_coverage'])
        te_main['ratio_debt_coverage_log'] = safe_log1p(te_main['ratio_debt_coverage'])
    
    # 收入覆盖率
    if 'installment_amt' in tr_main.columns and 'bank_income_sum' in tr_main.columns:
        tr_main['ratio_income_coverage'] = safe_divide(tr_main['installment_amt'], tr_main['bank_income_sum'], 0)
        te_main['ratio_income_coverage'] = safe_divide(te_main['installment_amt'], te_main['bank_income_sum'], 0)
    
    # 流动性比率
    if 'raw_balance' in tr_main.columns and 'raw_loan' in tr_main.columns:
        tr_main['ratio_liquidity'] = safe_divide(tr_main['raw_balance'], tr_main['raw_loan'], 0)
        te_main['ratio_liquidity'] = safe_divide(te_main['raw_balance'], te_main['raw_loan'], 0)
    
    # 快速比率
    if 'raw_balance' in tr_main.columns and 'installment_amt' in tr_main.columns:
        tr_main['ratio_quick_ratio'] = safe_divide(tr_main['raw_balance'], tr_main['installment_amt'], 0)
        te_main['ratio_quick_ratio'] = safe_divide(te_main['raw_balance'], te_main['installment_amt'], 0)
    
    # 效率比率
    if 'bank_income_sum' in tr_main.columns and 'raw_balance' in tr_main.columns:
        tr_main['ratio_asset_turnover'] = safe_divide(tr_main['bank_income_sum'], tr_main['raw_balance'], 0)
        te_main['ratio_asset_turnover'] = safe_divide(te_main['bank_income_sum'], te_main['raw_balance'], 0)
    
    # 应收账款周转率
    if 'bank_income_sum' in tr_main.columns and 'bank_expense_sum' in tr_main.columns:
        tr_main['ratio_receivables_turnover'] = safe_divide(tr_main['bank_income_sum'], tr_main['bank_expense_sum'], 1)
        te_main['ratio_receivables_turnover'] = safe_divide(te_main['bank_income_sum'], te_main['bank_expense_sum'], 1)
    
    # 净额比率
    if 'bank_net_sum' in tr_main.columns and 'bank_income_sum' in tr_main.columns:
        tr_main['ratio_net_income'] = safe_divide(tr_main['bank_net_sum'], tr_main['bank_income_sum'], 0)
        te_main['ratio_net_income'] = safe_divide(te_main['bank_net_sum'], te_main['bank_income_sum'], 0)
    
    # 支出收入比
    if 'bank_expense_sum' in tr_main.columns and 'bank_income_sum' in tr_main.columns:
        tr_main['ratio_expense_income'] = safe_divide(tr_main['bank_expense_sum'], tr_main['bank_income_sum'], 1)
        te_main['ratio_expense_income'] = safe_divide(te_main['bank_expense_sum'], te_main['bank_income_sum'], 1)
    
    return tr_main, te_main

def build_time_ratio_features(tr_main: pd.DataFrame, te_main: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """构建时间比率特征"""
    
    # 活跃度比率
    if 'bank_months_active' in tr_main.columns and 'history_len_days' in tr_main.columns:
        tr_main['ratio_active_months'] = safe_divide(tr_main['bank_months_active'] * 30, tr_main['history_len_days'], 0)
        te_main['ratio_active_months'] = safe_divide(te_main['bank_months_active'] * 30, te_main['history_len_days'], 0)
    
    # 一致性比率
    if 'bank_months_active' in tr_main.columns and 'time_total_days' in tr_main.columns:
        tr_main['ratio_consistent_months'] = safe_divide(tr_main['bank_months_active'] * 30, tr_main['time_total_days'], 0)
        te_main['ratio_consistent_months'] = safe_divide(te_main['bank_months_active'] * 30, te_main['time_total_days'], 0)
    
    # 交易密度比率
    if 'bank_txn_count_m' in tr_main.columns and 'bank_months_active' in tr_main.columns:
        tr_main['ratio_txn_density'] = safe_divide(tr_main['bank_txn_count_m'], tr_main['bank_months_active'], 0)
        te_main['ratio_txn_density'] = safe_divide(te_main['bank_txn_count_m'], te_main['bank_months_active'], 0)
    
    # 金额密度比率
    if 'bank_income_sum' in tr_main.columns and 'bank_months_active' in tr_main.columns:
        tr_main['ratio_amount_density'] = safe_divide(tr_main['bank_income_sum'], tr_main['bank_months_active'], 0)
        te_main['ratio_amount_density'] = safe_divide(te_main['bank_income_sum'], te_main['bank_months_active'], 0)
    
    # 趋势稳定性比率
    if 'time_trend_amount_sum_r2' in tr_main.columns:
        tr_main['ratio_trend_stability'] = tr_main['time_trend_amount_sum_r2']
        te_main['ratio_trend_stability'] = te_main['time_trend_amount_sum_r2']
    
    # 波动性控制比率
    if 'time_monthly_amount_cv' in tr_main.columns:
        tr_main['ratio_volatility_control'] = 1.0 / (1.0 + tr_main['time_monthly_amount_cv'])
        te_main['ratio_volatility_control'] = 1.0 / (1.0 + te_main['time_monthly_amount_cv'])
    
    # 时间效率比率
    if 'time_active_days' in tr_main.columns and 'time_total_days' in tr_main.columns:
        tr_main['ratio_time_efficiency'] = safe_divide(tr_main['time_active_days'], tr_main['time_total_days'], 0)
        te_main['ratio_time_efficiency'] = safe_divide(te_main['time_active_days'], te_main['time_total_days'], 0)
    
    return tr_main, te_main

def build_risk_ratio_features(tr_main: pd.DataFrame, te_main: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """构建风险比率特征"""
    
    # 违约风险比率
    if 'DTI' in tr_main.columns and 'utilization' in tr_main.columns:
        tr_main['ratio_default_risk'] = tr_main['DTI'] * tr_main['utilization']
        te_main['ratio_default_risk'] = te_main['DTI'] * te_main['utilization']
    
    # 逾期风险比率
    if 'buffer_months' in tr_main.columns:
        tr_main['ratio_overdue_risk'] = 1.0 / (1.0 + tr_main['buffer_months'])
        te_main['ratio_overdue_risk'] = 1.0 / (1.0 + te_main['buffer_months'])
    
    # 信用风险比率
    if 'level_ord' in tr_main.columns and 'utilization' in tr_main.columns:
        tr_main['ratio_credit_risk'] = safe_divide(tr_main['level_ord'], tr_main['utilization'], 0)
        te_main['ratio_credit_risk'] = safe_divide(te_main['level_ord'], te_main['utilization'], 0)
    
    # 行为风险比率
    if 'bank_expense_over_income' in tr_main.columns:
        tr_main['ratio_behavior_risk'] = tr_main['bank_expense_over_income']
        te_main['ratio_behavior_risk'] = te_main['bank_expense_over_income']
    
    # 流动性风险比率
    if 'ratio_liquidity' in tr_main.columns:
        tr_main['ratio_liquidity_risk'] = 1.0 / (1.0 + tr_main['ratio_liquidity'])
        te_main['ratio_liquidity_risk'] = 1.0 / (1.0 + te_main['ratio_liquidity'])
    
    # 收入稳定性比率
    if 'bank_income_std' in tr_main.columns and 'bank_income_mean' in tr_main.columns:
        tr_main['ratio_income_stability'] = safe_divide(tr_main['bank_income_mean'], tr_main['bank_income_std'], 0)
        te_main['ratio_income_stability'] = safe_divide(te_main['bank_income_sum'], te_main['bank_income_std'], 0)
    
    # 支出稳定性比率
    if 'bank_expense_std' in tr_main.columns and 'bank_expense_mean' in tr_main.columns:
        tr_main['ratio_expense_stability'] = safe_divide(tr_main['bank_expense_mean'], tr_main['bank_expense_std'], 0)
        te_main['ratio_expense_stability'] = safe_divide(te_main['bank_expense_mean'], te_main['bank_expense_std'], 0)
    
    # 综合风险评分
    risk_features = ['ratio_default_risk', 'ratio_overdue_risk', 'ratio_credit_risk', 'ratio_behavior_risk']
    available_risk_features = [f for f in risk_features if f in tr_main.columns]
    
    if len(available_risk_features) > 0:
        tr_main['ratio_comprehensive_risk'] = tr_main[available_risk_features].mean(axis=1)
        te_main['ratio_comprehensive_risk'] = te_main[available_risk_features].mean(axis=1)
    
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
    parser = argparse.ArgumentParser(description="Day8 RATIO特征构建")
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
    ensure_dir(f"{args.out_dir}/ratio")
    ensure_dir(f"{args.out_dir}/merge")
    
    print(f"[INFO] 开始Day8 RATIO特征构建...")
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
    
    # 构建RATIO特征
    tr_ratio, te_ratio = build_ratio_features(tr_main, te_main)
    
    # 保存特征
    print("[INFO] 保存RATIO特征...")
    tr_ratio.to_csv(f"{args.out_dir}/ratio/features_ratio_train.csv", index=False)
    te_ratio.to_csv(f"{args.out_dir}/ratio/features_ratio_test.csv", index=False)
    
    # 合并特征
    print("[INFO] 合并特征...")
    tr_merged = tr_ratio.copy()
    te_merged = te_ratio.copy()
    
    tr_merged.to_csv(f"{args.out_dir}/merge/ratio_merged_train.csv", index=False)
    te_merged.to_csv(f"{args.out_dir}/merge/ratio_merged_test.csv", index=False)
    

    
    print(f"[INFO] Day8 RATIO特征构建完成！")
    print(f"[INFO] 输出文件:")
    print(f"  - 训练特征: {args.out_dir}/ratio/features_ratio_train.csv")
    print(f"  - 测试特征: {args.out_dir}/ratio/features_ratio_test.csv")
    print(f"  - 合并训练: {args.out_dir}/merge/ratio_merged_train.csv")
    print(f"  - 合并测试: {args.out_dir}/merge/ratio_merged_test.csv")

if __name__ == "__main__":
    main()

