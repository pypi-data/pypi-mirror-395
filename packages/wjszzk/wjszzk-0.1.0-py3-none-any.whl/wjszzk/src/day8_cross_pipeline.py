#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day8 - CROSS 批次：交叉组合特征构建
构建基于现有特征的深度交互和组合特征，包括：
1. 主表交叉特征：职业×贷款、信用等级×财务等
2. 银行流水交叉特征：收入支出比率、交易效率等
3. 跨表交叉特征：主表×流水、信用×行为等
与基线特征合并后输出，供后续特征工程使用
"""

import os
import json
import argparse
import numpy as np
import pandas as pd
from collections import defaultdict
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

def woe_encode(x: pd.Series, y: pd.Series, min_samples: int = 10) -> pd.Series:
    """WOE编码，用于分类变量"""
    try:
        from sklearn.preprocessing import LabelEncoder
        le = LabelEncoder()
        x_encoded = le.fit_transform(x.fillna('MISSING'))
        
        # 计算WOE
        woe_dict = {}
        for val in np.unique(x_encoded):
            if val == -1:  # 缺失值
                continue
            pos_count = np.sum((x_encoded == val) & (y == 1))
            neg_count = np.sum((x_encoded == val) & (y == 0))
            
            if pos_count >= min_samples and neg_count >= min_samples:
                pos_rate = pos_count / np.sum(y == 1)
                neg_rate = neg_count / np.sum(y == 0)
                woe = np.log(pos_rate / neg_rate) if pos_rate > 0 and neg_rate > 0 else 0
                woe_dict[val] = woe
            else:
                woe_dict[val] = 0
        
        # 应用WOE编码
        result = pd.Series(index=x.index, dtype=float)
        for val in np.unique(x_encoded):
            if val in woe_dict:
                result[x_encoded == val] = woe_dict[val]
            else:
                result[x_encoded == val] = 0
        
        return result
    except:
        # 如果WOE编码失败，返回原始值
        return x.astype('category').cat.codes

# ----------------------------
# CROSS特征构建核心函数
# ----------------------------
def build_cross_features(tr_main: pd.DataFrame, te_main: pd.DataFrame, 
                        tr_bank: pd.DataFrame, te_bank: pd.DataFrame,
                        y: np.ndarray = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    """构建CROSS批次特征"""
    
    print("[INFO] 开始构建CROSS批次特征...")
    
    # 合并主表和银行流水数据
    tr_merged = tr_main.copy()
    te_merged = te_main.copy()
    
    # 1. 主表交叉特征
    print("[INFO] 构建主表交叉特征...")
    tr_merged, te_merged = build_main_cross_features(tr_merged, te_merged)
    
    # 2. 银行流水交叉特征
    print("[INFO] 构建银行流水交叉特征...")
    tr_merged, te_merged = build_bank_cross_features(tr_merged, te_merged, tr_bank, te_bank)
    
    # 3. 跨表交叉特征
    print("[INFO] 构建跨表交叉特征...")
    tr_merged, te_merged = build_cross_table_features(tr_merged, te_merged, tr_bank, te_bank, y)
    
    # 4. 特征清理和优化
    print("[INFO] 特征清理和优化...")
    tr_merged, te_merged = clean_and_optimize_features(tr_merged, te_merged)
    
    print(f"[INFO] CROSS特征构建完成，训练集: {tr_merged.shape}, 测试集: {te_merged.shape}")
    
    return tr_merged, te_merged

def build_main_cross_features(tr_main: pd.DataFrame, te_main: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """构建主表交叉特征"""
    
    # 职业×贷款特征
    if 'raw_career' in tr_main.columns and 'raw_loan' in tr_main.columns:
        tr_main['cross_career_loan_ratio'] = safe_divide(tr_main['raw_loan'], tr_main['raw_career'], 0)
        te_main['cross_career_loan_ratio'] = safe_divide(te_main['raw_loan'], te_main['raw_career'], 0)
        
        tr_main['cross_career_loan_log'] = safe_log1p(tr_main['cross_career_loan_ratio'])
        te_main['cross_career_loan_log'] = safe_log1p(te_main['cross_career_loan_ratio'])
    
    # 职业×利率特征
    if 'raw_career' in tr_main.columns and 'raw_interest_rate' in tr_main.columns:
        tr_main['cross_career_interest_ratio'] = safe_divide(tr_main['raw_interest_rate'], tr_main['raw_career'], 0)
        te_main['cross_career_interest_ratio'] = safe_divide(te_main['raw_interest_rate'], te_main['raw_career'], 0)
    
    # 信用等级×财务特征
    if 'level_ord' in tr_main.columns and 'utilization' in tr_main.columns:
        tr_main['cross_level_utilization'] = tr_main['level_ord'] * tr_main['utilization']
        te_main['cross_level_utilization'] = te_main['level_ord'] * te_main['utilization']
        
        tr_main['cross_level_utilization_ratio'] = safe_divide(tr_main['level_ord'], tr_main['utilization'], 0)
        te_main['cross_level_utilization_ratio'] = safe_divide(te_main['level_ord'], te_main['utilization'], 0)
    
    if 'level_ord' in tr_main.columns and 'DTI' in tr_main.columns:
        tr_main['cross_level_dti'] = tr_main['level_ord'] * tr_main['DTI']
        te_main['cross_level_dti'] = te_main['level_ord'] * te_main['DTI']
    
    if 'level_ord' in tr_main.columns and 'buffer_months' in tr_main.columns:
        tr_main['cross_level_buffer'] = tr_main['level_ord'] * tr_main['buffer_months']
        te_main['cross_level_buffer'] = te_main['level_ord'] * te_main['buffer_months']
    
    # 时间×金额特征
    if 'history_len_days' in tr_main.columns and 'raw_loan' in tr_main.columns:
        tr_main['cross_time_loan_ratio'] = safe_divide(tr_main['raw_loan'], tr_main['history_len_days'], 0)
        te_main['cross_time_loan_ratio'] = safe_divide(te_main['raw_loan'], te_main['history_len_days'], 0)
    
    if 'rec_minus_issue_days' in tr_main.columns and 'raw_balance' in tr_main.columns:
        tr_main['cross_time_balance_ratio'] = safe_divide(tr_main['raw_balance'], tr_main['rec_minus_issue_days'], 0)
        te_main['cross_time_balance_ratio'] = safe_divide(te_main['raw_balance'], te_main['rec_minus_issue_days'], 0)
    
    # 贷款×余额特征
    if 'raw_loan' in tr_main.columns and 'raw_balance' in tr_main.columns:
        tr_main['cross_loan_balance_ratio'] = safe_divide(tr_main['raw_loan'], tr_main['raw_balance'], 0)
        te_main['cross_loan_balance_ratio'] = safe_divide(te_main['raw_loan'], te_main['raw_balance'], 0)
        
        tr_main['cross_loan_balance_diff'] = tr_main['raw_loan'] - tr_main['raw_balance']
        te_main['cross_loan_balance_diff'] = te_main['raw_loan'] - te_main['raw_balance']
    
    # 利率×期限特征
    if 'raw_interest_rate' in tr_main.columns and 'raw_term' in tr_main.columns:
        tr_main['cross_interest_term'] = tr_main['raw_interest_rate'] * tr_main['raw_term']
        te_main['cross_interest_term'] = te_main['raw_interest_rate'] * te_main['raw_term']
        
        tr_main['cross_interest_term_ratio'] = safe_divide(tr_main['raw_interest_rate'], tr_main['raw_term'], 0)
        te_main['cross_interest_term_ratio'] = safe_divide(te_main['raw_interest_rate'], te_main['raw_term'], 0)
    
    return tr_main, te_main

def build_bank_cross_features(tr_main: pd.DataFrame, te_main: pd.DataFrame,
                            tr_bank: pd.DataFrame, te_bank: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """构建银行流水交叉特征"""
    
    # 收入支出比率特征
    if 'bank_income_sum' in tr_main.columns and 'bank_expense_sum' in tr_main.columns:
        tr_main['cross_income_expense_ratio'] = safe_divide(tr_main['bank_income_sum'], tr_main['bank_expense_sum'], 1)
        te_main['cross_income_expense_ratio'] = safe_divide(te_main['bank_income_sum'], te_main['bank_expense_sum'], 1)
        
        tr_main['cross_income_expense_diff'] = tr_main['bank_income_sum'] - tr_main['bank_expense_sum']
        te_main['cross_income_expense_diff'] = te_main['bank_income_sum'] - te_main['bank_expense_sum']
        
        tr_main['cross_income_expense_log_ratio'] = safe_log1p(tr_main['cross_income_expense_ratio'])
        te_main['cross_income_expense_log_ratio'] = safe_log1p(te_main['cross_income_expense_ratio'])
    
    # 交易频率×金额特征
    if 'bank_txn_count_m' in tr_main.columns and 'bank_income_sum' in tr_main.columns:
        tr_main['cross_txn_amount_efficiency'] = safe_divide(tr_main['bank_income_sum'], tr_main['bank_txn_count_m'], 0)
        te_main['cross_txn_amount_efficiency'] = safe_divide(te_main['bank_income_sum'], te_main['bank_txn_count_m'], 0)
    
    if 'bank_txn_count_m' in tr_main.columns and 'bank_expense_sum' in tr_main.columns:
        tr_main['cross_txn_expense_efficiency'] = safe_divide(tr_main['bank_expense_sum'], tr_main['bank_txn_count_m'], 0)
        te_main['cross_txn_expense_efficiency'] = safe_divide(te_main['bank_expense_sum'], te_main['bank_txn_count_m'], 0)
    
    # 时间模式×金额特征
    if 'time_weekend_ratio' in tr_main.columns and 'bank_income_sum' in tr_main.columns:
        tr_main['cross_time_amount_efficiency'] = tr_main['time_weekend_ratio'] * tr_main['bank_income_sum']
        te_main['cross_time_amount_efficiency'] = te_main['time_weekend_ratio'] * te_main['bank_income_sum']
    
    if 'time_weekend_weekday_ratio' in tr_main.columns and 'bank_expense_sum' in tr_main.columns:
        tr_main['cross_weekend_weekday_efficiency'] = tr_main['time_weekend_weekday_ratio'] * tr_main['bank_expense_sum']
        te_main['cross_weekend_weekday_efficiency'] = te_main['time_weekend_weekday_ratio'] * te_main['bank_expense_sum']
    
    # 净额相关特征
    if 'bank_net_sum' in tr_main.columns and 'bank_income_sum' in tr_main.columns:
        tr_main['cross_net_income_ratio'] = safe_divide(tr_main['bank_net_sum'], tr_main['bank_income_sum'], 0)
        te_main['cross_net_income_ratio'] = safe_divide(te_main['bank_net_sum'], te_main['bank_income_sum'], 0)
    
    if 'bank_net_sum' in tr_main.columns and 'bank_expense_sum' in tr_main.columns:
        tr_main['cross_net_expense_ratio'] = safe_divide(tr_main['bank_net_sum'], tr_main['bank_expense_sum'], 0)
        te_main['cross_net_expense_ratio'] = safe_divide(te_main['bank_net_sum'], te_main['bank_expense_sum'], 0)
    
    # 波动性×金额特征
    if 'bank_income_std' in tr_main.columns and 'bank_income_mean' in tr_main.columns:
        tr_main['cross_income_cv'] = safe_divide(tr_main['bank_income_std'], tr_main['bank_income_mean'], 0)
        te_main['cross_income_cv'] = safe_divide(te_main['bank_income_std'], te_main['bank_income_mean'], 0)
    
    if 'bank_expense_std' in tr_main.columns and 'bank_expense_mean' in tr_main.columns:
        tr_main['cross_expense_cv'] = safe_divide(tr_main['bank_expense_std'], tr_main['bank_expense_mean'], 0)
        te_main['cross_expense_cv'] = safe_divide(te_main['bank_expense_std'], te_main['bank_expense_mean'], 0)
    
    return tr_main, te_main

def build_cross_table_features(tr_main: pd.DataFrame, te_main: pd.DataFrame,
                             tr_bank: pd.DataFrame, te_bank: pd.DataFrame,
                             y: np.ndarray = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    """构建跨表交叉特征"""
    
    # 主表×流水特征
    if 'raw_loan' in tr_main.columns and 'bank_income_sum' in tr_main.columns:
        tr_main['cross_main_bank_income_ratio'] = safe_divide(tr_main['raw_loan'], tr_main['bank_income_sum'], 0)
        te_main['cross_main_bank_income_ratio'] = safe_divide(te_main['raw_loan'], te_main['bank_income_sum'], 0)
        
        tr_main['cross_main_bank_income_log_ratio'] = safe_log1p(tr_main['cross_main_bank_income_ratio'])
        te_main['cross_main_bank_income_log_ratio'] = safe_log1p(te_main['cross_main_bank_income_ratio'])
    
    if 'raw_loan' in tr_main.columns and 'bank_expense_sum' in tr_main.columns:
        tr_main['cross_main_bank_expense_ratio'] = safe_divide(tr_main['raw_loan'], tr_main['bank_expense_sum'], 0)
        te_main['cross_main_bank_expense_ratio'] = safe_divide(te_main['raw_loan'], te_main['bank_expense_sum'], 0)
    
    if 'installment_amt' in tr_main.columns and 'bank_income_sum' in tr_main.columns:
        tr_main['cross_installment_income_ratio'] = safe_divide(tr_main['installment_amt'], tr_main['bank_income_sum'], 0)
        te_main['cross_installment_income_ratio'] = safe_divide(te_main['installment_amt'], te_main['bank_income_sum'], 0)
    
    # 信用×行为特征
    if 'level_ord' in tr_main.columns and 'bank_income_sum' in tr_main.columns:
        tr_main['cross_credit_income_score'] = tr_main['level_ord'] * np.log1p(tr_main['bank_income_sum'])
        te_main['cross_credit_income_score'] = te_main['level_ord'] * np.log1p(te_main['bank_income_sum'])
    
    if 'level_ord' in tr_main.columns and 'bank_expense_sum' in tr_main.columns:
        tr_main['cross_credit_expense_score'] = tr_main['level_ord'] * np.log1p(tr_main['bank_expense_sum'])
        te_main['cross_credit_expense_score'] = te_main['level_ord'] * np.log1p(te_main['bank_expense_sum'])
    
    # 债务×收入特征
    if 'DTI' in tr_main.columns and 'bank_income_sum' in tr_main.columns:
        tr_main['cross_dti_income_ratio'] = safe_divide(tr_main['DTI'], np.log1p(tr_main['bank_income_sum']), 0)
        te_main['cross_dti_income_ratio'] = safe_divide(te_main['DTI'], np.log1p(te_main['bank_income_sum']), 0)
    
    if 'utilization' in tr_main.columns and 'bank_income_sum' in tr_main.columns:
        tr_main['cross_utilization_income_ratio'] = safe_divide(tr_main['utilization'], np.log1p(tr_main['bank_income_sum']), 0)
        te_main['cross_utilization_income_ratio'] = safe_divide(te_main['utilization'], np.log1p(te_main['bank_income_sum']), 0)
    
    # 时间×行为特征
    if 'history_len_days' in tr_main.columns and 'bank_txn_count_m' in tr_main.columns:
        tr_main['cross_history_txn_density'] = safe_divide(tr_main['bank_txn_count_m'], tr_main['history_len_days'], 0)
        te_main['cross_history_txn_density'] = safe_divide(te_main['bank_txn_count_m'], te_main['history_len_days'], 0)
    
    if 'rec_minus_issue_days' in tr_main.columns and 'bank_months_active' in tr_main.columns:
        tr_main['cross_issue_rec_txn_density'] = safe_divide(tr_main['bank_months_active'], tr_main['rec_minus_issue_days'], 0)
        te_main['cross_issue_rec_txn_density'] = safe_divide(te_main['bank_months_active'], te_main['rec_minus_issue_days'], 0)
    
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
    parser = argparse.ArgumentParser(description="Day8 CROSS特征构建")
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
    ensure_dir(f"{args.out_dir}/cross")
    ensure_dir(f"{args.out_dir}/merge")
    
    print(f"[INFO] 开始Day8 CROSS特征构建...")
    print(f"[INFO] 输出目录: {args.out_dir}")
    
    # 读取基础特征
    try:
        print(f"[INFO] 读取训练特征: {args.base_train}")
        print(f"[INFO] 读取测试特征: {args.base_test}")
        
        tr_main = read_csv(args.base_train)
        te_main = read_csv(args.base_test)
        
        # 读取银行流水数据
        tr_bank = read_csv(args.train_bank)
        te_bank = read_csv(args.test_bank)
        
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
    
    # 构建CROSS特征
    tr_cross, te_cross = build_cross_features(tr_main, te_main, tr_bank, te_bank, y)
    
    # 保存特征
    print("[INFO] 保存CROSS特征...")
    tr_cross.to_csv(f"{args.out_dir}/cross/features_cross_train.csv", index=False)
    te_cross.to_csv(f"{args.out_dir}/cross/features_cross_test.csv", index=False)
    
    # 合并特征
    print("[INFO] 合并特征...")
    tr_merged = tr_cross.copy()
    te_merged = te_cross.copy()
    
    tr_merged.to_csv(f"{args.out_dir}/merge/cross_merged_train.csv", index=False)
    te_merged.to_csv(f"{args.out_dir}/merge/cross_merged_test.csv", index=False)

    
    print(f"[INFO] Day8 CROSS特征构建完成！")
    print(f"[INFO] 输出文件:")
    print(f"  - 训练特征: {args.out_dir}/cross/features_cross_train.csv")
    print(f"  - 测试特征: {args.out_dir}/cross/features_cross_test.csv")
    print(f"  - 合并训练: {args.out_dir}/merge/cross_merged_train.csv")
    print(f"  - 合并测试: {args.out_dir}/merge/cross_merged_test.csv")

if __name__ == "__main__":
    main()
