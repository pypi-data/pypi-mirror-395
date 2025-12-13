"""
Day8 - POLY 批次：多项式和高阶特征构建
构建基于特征的非线性关系特征，包括：
1. 二次项特征：金额二次项、比率二次项、时间二次项等
2. 三次项特征：关键特征三次项、交互三次项等
3. 交互多项式特征：二元交互、三元交互、条件多项式等
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
# POLY特征构建核心函数
# ----------------------------
def build_poly_features(tr_main: pd.DataFrame, te_main: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """构建POLY批次特征"""
    
    print("[INFO] 开始构建POLY批次特征...")
    
    # 复制数据
    tr_poly = tr_main.copy()
    te_poly = te_main.copy()
    
    # 1. 二次项特征
    print("[INFO] 构建二次项特征...")
    tr_poly, te_poly = build_quadratic_features(tr_poly, te_poly)
    
    # 2. 三次项特征
    print("[INFO] 构建三次项特征...")
    tr_poly, te_poly = build_cubic_features(tr_poly, te_poly)
    
    # 3. 交互多项式特征
    print("[INFO] 构建交互多项式特征...")
    tr_poly, te_poly = build_interaction_poly_features(tr_poly, te_poly)
    
    # 4. 特征清理和优化
    print("[INFO] 特征清理和优化...")
    tr_poly, te_poly = clean_and_optimize_features(tr_poly, te_poly)
    
    print(f"[INFO] POLY特征构建完成，训练集: {tr_poly.shape}, 测试集: {te_poly.shape}")
    
    return tr_poly, te_poly

def build_quadratic_features(tr_main: pd.DataFrame, te_main: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """构建二次项特征"""
    
    # 金额二次项特征
    if 'raw_loan' in tr_main.columns:
        tr_main['poly_loan_squared'] = tr_main['raw_loan'] ** 2
        te_main['poly_loan_squared'] = te_main['raw_loan'] ** 2
        
        tr_main['poly_loan_squared_log'] = safe_log1p(tr_main['poly_loan_squared'])
        te_main['poly_loan_squared_log'] = safe_log1p(te_main['poly_loan_squared'])
    
    if 'raw_balance' in tr_main.columns:
        tr_main['poly_balance_squared'] = tr_main['raw_balance'] ** 2
        te_main['poly_balance_squared'] = te_main['raw_balance'] ** 2
        
        tr_main['poly_balance_squared_log'] = safe_log1p(tr_main['poly_balance_squared'])
        te_main['poly_balance_squared_log'] = safe_log1p(te_main['poly_balance_squared'])
    
    if 'bank_income_sum' in tr_main.columns:
        tr_main['poly_income_squared'] = tr_main['bank_income_sum'] ** 2
        te_main['poly_income_squared'] = te_main['bank_income_sum'] ** 2
        
        tr_main['poly_income_squared_log'] = safe_log1p(tr_main['poly_income_squared'])
        te_main['poly_income_squared_log'] = safe_log1p(te_main['poly_income_squared'])
    
    # 比率二次项特征
    if 'utilization' in tr_main.columns:
        tr_main['poly_utilization_squared'] = tr_main['utilization'] ** 2
        te_main['poly_utilization_squared'] = te_main['utilization'] ** 2
    
    if 'DTI' in tr_main.columns:
        tr_main['poly_dti_squared'] = tr_main['DTI'] ** 2
        te_main['poly_dti_squared'] = te_main['DTI'] ** 2
    
    if 'buffer_months' in tr_main.columns:
        tr_main['poly_buffer_squared'] = tr_main['buffer_months'] ** 2
        te_main['poly_buffer_squared'] = te_main['buffer_months'] ** 2
    
    # 时间二次项特征
    if 'history_len_days' in tr_main.columns:
        tr_main['poly_history_squared'] = tr_main['history_len_days'] ** 2
        te_main['poly_history_squared'] = te_main['history_len_days'] ** 2
    
    if 'rec_minus_issue_days' in tr_main.columns:
        tr_main['poly_issue_squared'] = tr_main['rec_minus_issue_days'] ** 2
        te_main['poly_issue_squared'] = te_main['rec_minus_issue_days'] ** 2
    
    # 银行流水二次项特征
    if 'bank_expense_sum' in tr_main.columns:
        tr_main['poly_expense_squared'] = tr_main['bank_expense_sum'] ** 2
        te_main['poly_expense_squared'] = te_main['bank_expense_sum'] ** 2
        
        tr_main['poly_expense_squared_log'] = safe_log1p(tr_main['poly_expense_squared'])
        te_main['poly_expense_squared_log'] = safe_log1p(te_main['poly_expense_squared'])
    
    if 'bank_net_sum' in tr_main.columns:
        tr_main['poly_net_squared'] = tr_main['bank_net_sum'] ** 2
        te_main['poly_net_squared'] = te_main['bank_net_sum'] ** 2
        
        tr_main['poly_net_squared_log'] = safe_log1p(tr_main['poly_net_squared'])
        te_main['poly_net_squared_log'] = safe_log1p(te_main['poly_net_squared'])
    
    return tr_main, te_main

def build_cubic_features(tr_main: pd.DataFrame, te_main: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """构建三次项特征"""
    
    # 关键特征三次项
    if 'raw_loan' in tr_main.columns:
        tr_main['poly_loan_cubed'] = tr_main['raw_loan'] ** 3
        te_main['poly_loan_cubed'] = te_main['raw_loan'] ** 3
        
        tr_main['poly_loan_cubed_log'] = safe_log1p(tr_main['poly_loan_cubed'])
        te_main['poly_loan_cubed_log'] = safe_log1p(te_main['poly_loan_cubed'])
    
    if 'utilization' in tr_main.columns:
        tr_main['poly_utilization_cubed'] = tr_main['utilization'] ** 3
        te_main['poly_utilization_cubed'] = te_main['utilization'] ** 3
    
    if 'DTI' in tr_main.columns:
        tr_main['poly_dti_cubed'] = tr_main['DTI'] ** 3
        te_main['poly_dti_cubed'] = te_main['DTI'] ** 3
    
    # 交互三次项
    if 'raw_loan' in tr_main.columns and 'utilization' in tr_main.columns:
        tr_main['poly_loan_utilization_cubed'] = (tr_main['raw_loan'] * tr_main['utilization']) ** 3
        te_main['poly_loan_utilization_cubed'] = (te_main['raw_loan'] * te_main['utilization']) ** 3
    
    if 'bank_income_sum' in tr_main.columns and 'bank_expense_sum' in tr_main.columns:
        tr_main['poly_income_expense_cubed'] = (tr_main['bank_income_sum'] * tr_main['bank_expense_sum']) ** 3
        te_main['poly_income_expense_cubed'] = (te_main['bank_income_sum'] * te_main['bank_expense_sum']) ** 3
    
    # 信用等级三次项
    if 'level_ord' in tr_main.columns:
        tr_main['poly_level_cubed'] = tr_main['level_ord'] ** 3
        te_main['poly_level_cubed'] = te_main['level_ord'] ** 3
    
    return tr_main, te_main

def build_interaction_poly_features(tr_main: pd.DataFrame, te_main: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """构建交互多项式特征"""
    
    # 二元交互特征
    if 'raw_loan' in tr_main.columns and 'utilization' in tr_main.columns:
        tr_main['poly_loan_utilization'] = tr_main['raw_loan'] * tr_main['utilization']
        te_main['poly_loan_utilization'] = te_main['raw_loan'] * te_main['utilization']
        
        tr_main['poly_loan_utilization_log'] = safe_log1p(tr_main['poly_loan_utilization'])
        te_main['poly_loan_utilization_log'] = safe_log1p(te_main['poly_loan_utilization'])
    
    if 'bank_income_sum' in tr_main.columns and 'history_len_days' in tr_main.columns:
        tr_main['poly_income_history'] = tr_main['bank_income_sum'] * tr_main['history_len_days']
        te_main['poly_income_history'] = te_main['bank_income_sum'] * te_main['history_len_days']
        
        tr_main['poly_income_history_log'] = safe_log1p(tr_main['poly_income_history'])
        te_main['poly_income_history_log'] = safe_log1p(te_main['poly_income_history'])
    
    if 'raw_career' in tr_main.columns and 'raw_balance' in tr_main.columns:
        tr_main['poly_career_balance'] = tr_main['raw_career'] * tr_main['raw_balance']
        te_main['poly_career_balance'] = te_main['raw_career'] * te_main['raw_balance']
        
        tr_main['poly_career_balance_log'] = safe_log1p(tr_main['poly_career_balance'])
        te_main['poly_career_balance_log'] = safe_log1p(te_main['poly_career_balance'])
    
    # 三元交互特征
    if 'raw_loan' in tr_main.columns and 'utilization' in tr_main.columns and 'history_len_days' in tr_main.columns:
        tr_main['poly_loan_utilization_history'] = tr_main['raw_loan'] * tr_main['utilization'] * tr_main['history_len_days']
        te_main['poly_loan_utilization_history'] = te_main['raw_loan'] * te_main['utilization'] * te_main['history_len_days']
        
        tr_main['poly_loan_utilization_history_log'] = safe_log1p(tr_main['poly_loan_utilization_history'])
        te_main['poly_loan_utilization_history_log'] = safe_log1p(te_main['poly_loan_utilization_history'])
    
    if 'bank_income_sum' in tr_main.columns and 'raw_career' in tr_main.columns and 'raw_balance' in tr_main.columns:
        tr_main['poly_income_career_balance'] = tr_main['bank_income_sum'] * tr_main['raw_career'] * tr_main['raw_balance']
        te_main['poly_income_career_balance'] = te_main['bank_income_sum'] * te_main['raw_career'] * te_main['raw_balance']
        
        tr_main['poly_income_career_balance_log'] = safe_log1p(tr_main['poly_income_career_balance'])
        te_main['poly_income_career_balance_log'] = safe_log1p(te_main['poly_income_career_balance'])
    
    # 条件多项式特征
    if 'utilization' in tr_main.columns and 'raw_loan' in tr_main.columns:
        # 高利用率贷款
        high_utilization = tr_main['utilization'] > tr_main['utilization'].quantile(0.8)
        tr_main['poly_high_risk_loan'] = np.where(high_utilization, tr_main['raw_loan'] ** 2, 0)
        
        high_utilization_te = te_main['utilization'] > te_main['utilization'].quantile(0.8)
        te_main['poly_high_risk_loan'] = np.where(high_utilization_te, te_main['raw_loan'] ** 2, 0)
    
    if 'DTI' in tr_main.columns and 'utilization' in tr_main.columns:
        # 低收入高利用率
        low_income_high_util = (tr_main['DTI'] > tr_main['DTI'].quantile(0.8)) & (tr_main['utilization'] > tr_main['utilization'].quantile(0.8))
        tr_main['poly_low_income_utilization'] = np.where(low_income_high_util, tr_main['DTI'] * tr_main['utilization'], 0)
        
        low_income_high_util_te = (te_main['DTI'] > te_main['DTI'].quantile(0.8)) & (te_main['utilization'] > te_main['utilization'].quantile(0.8))
        te_main['poly_low_income_utilization'] = np.where(low_income_high_util_te, te_main['DTI'] * te_main['utilization'], 0)
    
    # 时间相关交互特征
    if 'time_weekend_ratio' in tr_main.columns and 'bank_income_sum' in tr_main.columns:
        tr_main['poly_weekend_income'] = tr_main['time_weekend_ratio'] * tr_main['bank_income_sum']
        te_main['poly_weekend_income'] = te_main['time_weekend_ratio'] * te_main['bank_income_sum']
    
    if 'time_weekday_entropy' in tr_main.columns and 'bank_expense_sum' in tr_main.columns:
        tr_main['poly_weekday_expense'] = tr_main['time_weekday_entropy'] * tr_main['bank_expense_sum']
        te_main['poly_weekday_expense'] = te_main['time_weekday_entropy'] * te_main['bank_expense_sum']
    
    # 信用相关交互特征
    if 'level_ord' in tr_main.columns and 'bank_income_sum' in tr_main.columns:
        tr_main['poly_credit_income'] = tr_main['level_ord'] * tr_main['bank_income_sum']
        te_main['poly_credit_income'] = te_main['level_ord'] * te_main['bank_income_sum']
        
        tr_main['poly_credit_income_log'] = safe_log1p(tr_main['poly_credit_income'])
        te_main['poly_credit_income_log'] = safe_log1p(te_main['poly_credit_income'])
    
    if 'level_ord' in tr_main.columns and 'bank_expense_sum' in tr_main.columns:
        tr_main['poly_credit_expense'] = tr_main['level_ord'] * tr_main['bank_expense_sum']
        te_main['poly_credit_expense'] = te_main['level_ord'] * te_main['bank_expense_sum']
        
        tr_main['poly_credit_expense_log'] = safe_log1p(tr_main['poly_credit_expense'])
        te_main['poly_credit_expense_log'] = safe_log1p(te_main['poly_credit_expense'])
    
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
    parser = argparse.ArgumentParser(description="Day8 POLY特征构建")
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
    ensure_dir(f"{args.out_dir}/poly")
    ensure_dir(f"{args.out_dir}/merge")
    
    print(f"[INFO] 开始Day8 POLY特征构建...")
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
    
    # 构建POLY特征
    tr_poly, te_poly = build_poly_features(tr_main, te_main)
    
    # 保存特征
    print("[INFO] 保存POLY特征...")
    tr_poly.to_csv(f"{args.out_dir}/poly/features_poly_train.csv", index=False)
    te_poly.to_csv(f"{args.out_dir}/poly/features_poly_test.csv", index=False)
    
    # 合并特征
    print("[INFO] 合并特征...")
    tr_merged = tr_poly.copy()
    te_merged = te_poly.copy()
    
    tr_merged.to_csv(f"{args.out_dir}/merge/poly_merged_train.csv", index=False)
    te_merged.to_csv(f"{args.out_dir}/merge/poly_merged_test.csv", index=False)

    
    print(f"[INFO] Day8 POLY特征构建完成！")
    print(f"[INFO] 输出文件:")
    print(f"  - 训练特征: {args.out_dir}/poly/features_poly_train.csv")
    print(f"  - 测试特征: {args.out_dir}/poly/features_poly_test.csv")
    print(f"  - 合并训练: {args.out_dir}/merge/poly_merged_train.csv")
    print(f"  - 合并测试: {args.out_dir}/merge/poly_merged_test.csv")

if __name__ == "__main__":
    main()

