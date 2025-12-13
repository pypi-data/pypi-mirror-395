"""
# 银行信贷违约二分类项目

这是一个基于银行流水数据的机器学习二分类预测项目，通过构建大量特征工程来训练模型并预测测试数据。
本项目由中信银行-融信之智队三名参赛队员队员：王高升、肖普、张泽坤协力完成。

## 项目概述

### 任务类型
- **任务**: 二分类预测
- **目标**: 基于用户的基本信息和银行流水数据，预测用户的信用风险
- **评估指标**: ROC-AUC

### 数据来源
- **主表数据**: 用户基本信息（职业、贷款金额、利率、信用等级等）
- **银行流水**: 用户的银行交易记录（收入、支出、时间等）

## B榜结果复现步骤

### 1. 环境准备
Python 3.12.7 版本，pip 依赖见 `doc/requirements.txt`（最小可复现集）。如需完整环境快照，可使用 `doc/requirements-full.txt`。
```bash
# 安装依赖（根据项目需要）
pip install -r requirements.txt
# 或使用完整环境快照（可选）
# pip install -r equirements-full.txt
```

### 2. 提交要求运行train和test脚本
```bash
# 进入项目目录
cd code

# 按照提交要求运行train和test脚本
# train脚本
python3 train.py ../init_data/初赛A榜数据集/train ./model
# test脚本
python3 test.py ../init_data/初赛B榜数据集/testab ../result
```
为了保证按要求运行train和test的指令能够跑通，我们提前在temp_data目录下放入了生成好的最终特征文件。
如有需要可以执行其他步骤来从原始数据逐步生成特征。

### 3. 运行完整流程
```bash
# 进入项目目录
cd code

# 运行完整流程
bash run_all.sh
```
如果数据路径有任何变化，可以通过修改run_all.sh里的参数配置来更换。

run_all.sh 包含了由多批次特征生成脚本组成的特征生成环节、双模型训练融合环节和比赛测试数据预测环节。
如需单独复现特征生成、模型训练或者测试数据预测过程，可以注释掉其他部分之后再运行run_all.sh。

### 4. 单独执行特征工程
```bash
# 进入项目目录
cd code

# 运行特征生成流程
bash run_features.sh
```
run_features和run_all唯一的区别在于删除了train和test的代码

时间有限，代码没有特别优化，特征生成是按顺序一个个脚本跑批传递的，需要耗费点时间。
若需要每一步特征生成，可以把run_features.sh里的具体步骤单独运行,但建议按顺序逐一生成。

## 输出文件

### 特征文件
- `temp_data/features`全部流程特征的中间结果都在目录下对应文件夹内。
目前提交版本已附上一份已生成好的特征数据，以便于直接运行train test脚本来复现。
如有需要可以重新运行来复刻生成特征，执行脚本见run_features.sh。


### 模型文件
- `code/model` - LightGBM、XGBoost的模型参数、以及融合参数



## 方案思路与实现细节

### 赛题理解与解决思路
- **问题定义**: 基于主表信息与银行流水行为数据的二分类违约预测，评价指标为 ROC-AUC，侧重排序能力。
- **总体策略**: 构建分批次、模块化的特征工程体系，覆盖基础属性、时间行为、稳定性、分箱、交叉、比率、滞后与业务口径特征；在模型侧采用树模型（LightGBM/XGBoost）进行 5 折分层交叉验证训练，并以 OOF 排序融合得到稳健预测。

### 作品核心优势
- **系统化特征体系**: 从通用统计到时间模式、从工程分箱到业务口径，形成极大量的多层次、可复现的特征流水线。
- **稳健的训练**: 双模型、离散小网格搜索、5 折分层 OOF 与早停，保证单模型的稳定泛化能力。
- **强力融合（多折均值 + Rank 融合）**: 先做“折内均值”提升单模型稳健性，再基于 OOF 的 rank 权重搜索做“双模型”融合，充分挖掘互补性，效果亮眼且可复现。

### 实现过程（步骤说明）
- **特征工程（day3～day11特征脚本）**:
  - 按批次流水线自下而上构建：S1/ADD/MUL/TIME/REC/BINS/CROSS/RATIO/LAG/CLUSTER/POLY 与 Day11 业务口径；最终通过 `day11_team_features_pipeline.py` 汇总为 `team_merged_{train,test}.csv`。
- **模型构建（train.py）**:
  - LightGBM：学习率 0.03，叶子数/叶最小样本/采样比例等多组网格组合；早停 300。
  - XGBoost：`tree_method=hist`，学习率 0.03，不同的深度/最小样本/采样/正则组合；早停 300。
- **模型训练（train.py）**:
  - 5 折分层交叉验证，遍历预设网格；按 OOF AUC 选择每个模型的最优超参组合。
  - 训练完成后，保存每折模型与训练元信息（特征列顺序、参数、融合权重等）。
- **模型评估（train.py）**:
  - 使用 OOF 计算单模型 AUC；对 LGB 与 XGB 的 OOF 进行 rank 归一化，网格化搜索融合权重 \(w\in[0.50,0.80], step=0.05\) 以最大化 OOF AUC。
- **模型预测（test.py）**:
  - 加载保存的每折模型，对测试集分别推理并取折均值；按最优权重对两模型 rank 分数进行线性融合，输出结果文件。


## 特征工程架构

### 1. S1批次特征 (day3_features.py)
**基础特征构建**，包含：

#### 主表特征
- **时间特征**: `issue_year/month`, `record_year/month`
- **原始数值**: `raw_career`, `raw_interest_rate`, `raw_loan`, `raw_term` 等
- **对数变换**: `log1p_loan`, `log1p_balance`, `log1p_balance_limit`
- **比率特征**: `utilization`, `acct_used_ratio`, `avg_balance_per_acct`
- **时间差**: `history_len_days`, `rec_minus_issue_days`
- **有序编码**: `level_ord`
- **One-Hot编码**: `title_*`, `residence_*`, `term_*`, `syndicated_*`, `installment_*`
- **频次特征**: `zip_freq`

#### 银行流水特征
- **基础统计**: `bank_income_sum/mean/std/p95`, `bank_expense_sum/mean/std/p95`
- **净额特征**: `bank_net_sum/mean/std`
- **交易统计**: `bank_txn_count_m`, `bank_months_active`
- **结构指标**: `bank_income_share`, `bank_big_txn_share`
- **趋势特征**: `bank_net_first`, `bank_net_last`, `bank_net_trend_simple`
- **跨期特征**: `bank_avg_income_over_period`, `bank_avg_expense_over_period`
- **风险指标**: `bank_expense_over_income`, `bank_neg_periods`

#### 交叉特征
- **月供计算**: `installment_amt`
- **收入代理**: `monthly_income_proxy`
- **债务指标**: `DTI`, `buffer_months`, `net_over_installment`

### 2. ADD批次特征 (day4_add_pipeline.py)
**加法特征增强**，通过以下方式构建新特征：
- 基于原始数据的统计特征
- 银行流水的聚合特征
- 时间序列特征
- 交互特征

### 3. MUL批次特征 (day4_mul_pipeline.py)
**乘法特征增强**，通过特征间的乘法交互构建新特征。

### 4. TIME批次特征 (day7_time_pipeline.py)
**时间序列特征 + 用户行为模式特征**，专注于时间维度的深度挖掘：

#### 银行流水时间特征
- **时间偏好**: `time_avg_hour`, `time_std_hour`, `time_weekend_ratio`
- **交易频率**: `time_txn_per_day`, `time_active_days`, `time_density`
- **时间间隔**: `time_avg_interval_hours`, `time_std_interval_hours`
- **周期性**: `time_weekday_preference`, `time_hour_preference`
- **时间波动性**: `time_hour_entropy`, `time_weekday_entropy`

#### 金额时间模式特征
- **工作日vs周末**: `time_weekday_avg_amount`, `time_weekend_avg_amount`, `time_weekend_weekday_ratio`
- **时段模式**: `time_morning_avg_amount`, `time_afternoon_avg_amount`, `time_evening_avg_amount`, `time_night_avg_amount`
- **时间相关性**: `time_amount_hour_corr`, `time_amount_weekday_corr`

#### 趋势和季节性特征
- **趋势特征**: `time_trend_amount_sum_slope`, `time_trend_txn_count_slope`, `time_trend_expense_ratio_slope`
- **季节性**: `time_monthly_amount_cv`, `time_monthly_txn_cv`
- **最近vs历史**: `time_recent_vs_hist_amount`, `time_recent_vs_hist_txn`

#### 风险时间模式特征
- **异常时间**: `time_late_night_ratio`, `time_early_morning_ratio`
- **高频交易**: `time_peak_hour_ratio`, `time_hour_concentration`
- **连续交易**: `time_consecutive_txn_ratio`, `time_rapid_txn_ratio`

#### 主表时间特征
- **时间差**: `time_issue_to_record_days`, `time_history_to_record_days`
- **时间窗口**: `time_issue_hour`, `time_issue_is_weekend`, `time_record_hour`, `time_record_is_weekend`

### 5. REC批次特征 (day7_rec_pipeline.py)
**近因加权特征 + 稳健性特征**，专注于时间衰减和模式稳定性：

#### 近因加权特征
- **指数衰减加权**: `day7_ew_income`, `day7_ew_expense`, `day7_ew_net` (基于0.8衰减因子)
- **时间权重**: 越近的月份权重越大，捕捉用户最新行为模式

#### 稳健性特征
- **零值占比**: `day7_zero_inc_share`, `day7_zero_exp_share` (收入/支出为零的月份占比)
- **净值分布**: `day7_pos_net_share`, `day7_neg_net_share` (正负净值的月份占比)
- **波动性指标**: 基于月度数据的稳定性评估

#### 时间模式特征
- **月度聚合**: 按月份聚合收入、支出、净额、交易次数、最大金额
- **趋势稳定性**: 捕捉用户财务行为的长期稳定性

### 6. BINS批次特征 (day7_bins_pipeline.py)
**连续特征分箱特征**，将连续变量转换为离散特征：

#### 信用相关比例分箱
- **利用率分箱**: `utilization_bins` (0-0.1, 0.1-0.3, 0.3-0.6, 0.6-0.9, 0.9+)
- **账户使用率分箱**: `acct_used_ratio_bins` (0-0.25, 0.25-0.5, 0.5-0.75, 0.75+)
- **债务收入比分箱**: `cross_DTI_bins` (0-0.2, 0.2-0.35, 0.35-0.5, 0.5-0.8, 0.8+)

#### 金额特征分箱
- **贷款金额分箱**: `main_log1p_loan_bins` (6等频分箱)
- **余额分箱**: `main_log1p_balance_bins`, `main_log1p_limit_bins` (6等频分箱)
- **月供分箱**: `installment_amt_bins` (6等频分箱)
- **净额月供比分箱**: `cross_net_over_installment_bins` (6等频分箱)

#### 时间特征分箱
- **历史长度分箱**: `main_history_len_days_bins` (5等频分箱)
- **记录发行时间差分箱**: `main_rec_minus_issue_days_bins` (5等频分箱)

#### 银行流水分箱
- **收入统计分箱**: `bank_income_mean_bins`, `bank_income_std_bins` (5等频分箱)
- **支出统计分箱**: `bank_expense_mean_bins`, `bank_expense_std_bins` (5等频分箱)
- **净额统计分箱**: `bank_net_mean_bins`, `bank_net_std_bins` (5等频分箱)
- **交易活跃度分箱**: `bank_txn_count_m_bins`, `bank_months_active_bins` (4-5等频分箱)

#### 分箱策略
- **语义优先**: 信用相关比例使用经验阈值分箱
- **等频分箱**: 金额和时间特征使用等频分箱
- **极端值处理**: 支持截断处理，避免异常值影响分箱质量
- **输出格式**: 支持顺序编码(ordinal)和独热编码(one-hot)两种输出

### 7.CROSS批次特征 (day8_cross_pipeline.py)
主表交叉特征: 职业×贷款、信用等级×财务、时间×金额等
银行流水交叉特征: 收入支出比率、交易效率、时间模式×金额等
跨表交叉特征: 主表×流水、信用×行为、债务×收入等


### 8.RATIO批次特征 (day8_ratio_pipeline.py)
财务比率特征: 债务覆盖率、流动性比率、效率比率等
时间比率特征: 活跃度比率、交易密度比率、趋势稳定性比率等
风险比率特征: 违约风险比率、信用风险比率、行为风险比率等


### 9.LAG批次特征 (day8_lag_pipeline.py)
滞后特征: 1-3期滞后、季节性滞后、年度滞后等
滑动窗口特征: 3期滑动平均、6期滑动统计、12期滑动趋势等
变化率特征: 环比变化、同比变化、累积变化等


### 10.CLUSTER批次特征 (day8_cluster_pipeline.py)
行为聚类特征: 交易模式聚类、时间偏好聚类、频率偏好聚类等
财务聚类特征: 收入支出聚类、现金流聚类、债务负担聚类等
组合聚类特征: 综合行为聚类、用户分段聚类、风险等级聚类等

### 11.POLY批次特征 (day8_poly_pipeline.py)
二次项特征: 金额二次项、比率二次项、时间二次项等
三次项特征: 关键特征三次项、交互三次项等
交互多项式特征: 二元交互、三元交互、条件多项式等


### 12～20中间批次特征最终未采纳

### 21.Day11-AFFORD 偿付能力与月供压力 (day11_afford_pipeline.py)
业务口径：月供覆盖、缓冲与最坏覆盖。
- 关键列：`aff_cover_1m/3m/6m`, `aff_buffer_months_1m/3m/6m`, `aff_min_cover`, `aff_net_minus_install_*`, `aff_install_over_limit`, `aff_install_over_loan`


### 22.Day11-INCOME_STAB 收入来源与稳定性 (day11_income_stab_pipeline.py)
业务口径：收入出现规律、密度与稳定性。
- 关键列：`incstab_income_months_share`, `incstab_income_cv`, `incstab_income_per_active_month`, `incstab_net_trend_sign`, `incstab_weekend_income_bias`


### 23.Day11-EXPENSE_STRUCTURE 支出结构 (day11_expense_structure_pipeline.py)
业务口径：刚性支出代理、可支配空间与支出波动。
- 关键列：`expstr_rigid_expense_proxy`, `expstr_disposable_proxy`, `expstr_expense_per_active_month`, `expstr_weekend_bias`, `expstr_late_night_bias`, `expstr_expense_cv`


### 24.Day11-CREDIT_BEHAVIOR 授信与使用行为 (day11_credit_behavior_pipeline.py)
业务口径：额度使用、账户使用与贷款-授信耦合、等级暴露。
- 关键列：`credbeh_utilization`, `credbeh_acct_used_ratio`, `credbeh_avg_balance_per_acct`, `credbeh_util_over_acct_ratio`, `credbeh_loan_over_limit`, `credbeh_loan_over_balance`, `credbeh_level_term_exposure`, `credbeh_level_rate_exposure`


### 25.Day11-LIQUIDITY_SHOCK 流动性与抗冲击能力 (day11_liquidity_shock_pipeline.py)
业务口径：收入下调/支出上调的压测最坏覆盖。
- 关键列：`shock_s1_*`, `shock_s2_*`, `shock_worst_net_minus_install`, `shock_worst_cover_ratio`, `shock_time_efficiency`, `shock_neg_periods`


### 26.Day11-BEHAVIOR_FLAGS 行为风险信号 (day11_behavior_flags_pipeline.py)
业务口径：末期突变、密度下降、不活跃、连续负月、临近大额支出风险。
- 关键列：`bhvflag_recent_amount_drop`, `bhvflag_density_drop`, `bhvflag_low_activity`, `bhvflag_many_neg_periods`, `bhvflag_large_expense_risk`


### 27.Day11-GEO_COHORT 地域对照 (day11_geo_cohort_pipeline.py)
业务口径：同 zip_h3 × career × level_m 群体的相对位置与偏离。
- 关键列：`geo_*_gmean/gmedian/gz/rel/rank`（针对 `installment_amt`, `bank_income_mean`, `bank_expense_mean`, `bank_net_mean`, `utilization`, `DTI`）


### 28.Day11-TEAM_FEATURES 团队特征工程 (day11_team_features_pipeline.py)
业务口径：整合团队的特征工程工作，包括主表通用特征和银行流水特征。
- 基础分解特征：`team_basic_level_m`, `team_basic_zip_h3`, `team_basic_issue_year`
- 月供计算特征：`team_payment_monthly`（基于贷款金额、期限、利率）
- 时间差异特征：`team_time_issue_to_record`, `team_time_history_to_issue`, `team_time_record_to_max`
- 信用额度比率：`team_credit_balance_ratio`, `team_credit_utilization`, `team_credit_total_utilization`
- 交互特征：`team_interaction_loan_term`, `team_interaction_risk_score`, `team_interaction_rate_level`
- 地理风险特征：`team_geo_zip_level`, `team_geo_zip_career`, `team_geo_career_title`
- 银行流水特征：`team_transaction_income_months_6m`, `team_transaction_deficit_months_6m`, `team_transaction_risk_flag`


## 模型训练方法

### 模型与超参
- **LightGBM**: `objective=binary`, `learning_rate=0.03`, `max_depth=-1`, `n_estimators=5000`, `bagging_freq=1`；小网格（离散组合）如下：
  - 组合A：`num_leaves=48, min_data_in_leaf=60, feature_fraction=0.7, bagging_fraction=0.8, reg_alpha=0.5, reg_lambda=5.0`
  - 组合B：`num_leaves=64, min_data_in_leaf=80, feature_fraction=0.7, bagging_fraction=0.8, reg_alpha=0.5, reg_lambda=5.0`
  - 组合C：`num_leaves=96, min_data_in_leaf=120, feature_fraction=0.7, bagging_fraction=0.8, reg_alpha=0.5, reg_lambda=5.0`
- **XGBoost**: `objective=binary:logistic`, `eval_metric=auc`, `tree_method=hist`, `eta=0.03`；小网格（离散组合）如下：
  - 组合A：`max_depth=6, min_child_weight=20, subsample=0.8, colsample_bytree=0.7, reg_lambda=5.0, reg_alpha=0.5`
  - 组合B：`max_depth=5, min_child_weight=20, subsample=0.8, colsample_bytree=0.7, reg_lambda=5.0, reg_alpha=0.5`
  - 组合C：`max_depth=7, min_child_weight=30, subsample=0.7, colsample_bytree=0.6, reg_lambda=10.0, reg_alpha=1.0`
- **特征处理**: 丢弃 `id/label`；`object` 列转 `category.codes`；添加 `is_bank_statement` 特征（由是否在银行流水表出现决定）。

### 训练与 OOF
- **交叉验证**: 5 折分层交叉验证，`seed=42`；每个模型对各自网格组合训练，按 OOF AUC 选择最佳组合。
- **早停**: 两个模型均使用 300 轮早停，防过拟合。
- **模型持久化**: 保存每折最优模型（LGB `lgb_fold{i}.txt`，XGB `xgb_fold{i}.json`）及 `meta.json`（特征列顺序、超参、融合权重等）。

### 双模型融合
- **折内平均（单模型）**: 对于选中的最优组合，保存 5 折模型；推理时对每个模型分别预测并取折均值，得到该模型在测试集上的均值分数。
- **融合方式（双模型）**: Rank 融合。将 LGB 与 XGB 的 OOF 分数各自做 rank-0-1 归一化；在 \(w\in[0.50,0.80], step=0.05\) 的权重网格上搜索、最大化 OOF AUC，得到最佳权重 `best_lgb_weight=w`。
- **测试集融合**: 将“折均值后的 LGB 分数”和“折均值后的 XGB 分数”各自做 rank-0-1 归一化，再按 `w` 做线性加权，得到最终提交分数。

### 预测与提交
- 预测脚本会加载保存的折模型与融合权重，对齐特征列顺序后推理并融合，最终输出 `result.csv`。

"""


