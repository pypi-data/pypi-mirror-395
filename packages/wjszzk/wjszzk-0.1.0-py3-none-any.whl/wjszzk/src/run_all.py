"""
#!/usr/bin/env bash
set -euo pipefail

#!/usr/bin/env bash
features_out_dir="../temp_data/features"
result_out_dir="../result"
train_dir="../init_data/初赛A榜数据集/train"
test_dir="../init_data/初赛B榜数据集/testab"

train_main=$train_dir"/train.csv"
train_bank=$train_dir"/train_bank_statement.csv"
test_main=$test_dir"/testab.csv"
test_bank=$test_dir"/testab_bank_statement.csv"


echo "开始构建S1特征..."
echo "=================================================="
python3 day3_features.py \
  --train_main $train_main \
  --train_bank $train_bank \
  --test_main  $test_main \
  --test_bank  $test_bank \
  --out_train  $features_out_dir/s1batch/train_features_S1.csv \
  --out_test   $features_out_dir/s1batch/test_features_S1.csv

echo "开始构建ADD特征..."
echo "=================================================="
python3 day4_add_pipeline.py \
  --base_train $features_out_dir/s1batch/train_features_S1.csv \
  --base_test  $features_out_dir/s1batch/test_features_S1.csv \
  --train_main $train_main \
  --train_bank $train_bank \
  --test_main  $test_main \
  --test_bank  $test_bank \
  --out_root   $features_out_dir/add_out \
  --seed 42

echo "开始构建MUL特征..."
echo "=================================================="
python3 day4_mul_pipeline.py \
  --base_train $features_out_dir/add_out/merged/add_merged_train.csv \
  --base_test  $features_out_dir/add_out/merged/add_merged_test.csv \
  --train_main $train_main \
  --test_main  $test_main \
  --out_root   $features_out_dir/mul_out \
  --seed 42

echo "开始构建TIME特征..."
echo "=================================================="
python3 day7_time_pipeline.py \
  --base_train $features_out_dir/mul_out/merged/mul_merged_train.csv \
  --base_test  $features_out_dir/mul_out/merged/mul_merged_test.csv \
  --train_main $train_main \
  --train_bank $train_bank \
  --test_main  $test_main \
  --test_bank  $test_bank \
  --out_root   $features_out_dir/time_out \
  --seed 42 

echo "开始构建REC特征..."
echo "=================================================="
python3 day7_rec_pipeline.py \
  --base_train $features_out_dir/time_out/merged/time_merged_train.csv \
  --base_test  $features_out_dir/time_out/merged/time_merged_test.csv \
  --train_main $train_main \
  --test_main  $test_main \
  --train_bank $train_bank \
  --test_bank  $test_bank \
  --out_dir   $features_out_dir/rec_out \
  --seed 42 

echo "开始构建BINS特征..."
echo "=================================================="
python3 day7_bins_pipeline.py \
  --base_train $features_out_dir/rec_out/merged/rec_merged_train.csv \
  --base_test  $features_out_dir/rec_out/merged/rec_merged_test.csv \
  --train_main $train_main \
  --test_main  $test_main \
  --out_dir   $features_out_dir/bins_out \
  --seed 42 

echo "开始构建CROSS特征..."
echo "=================================================="
python3 day8_cross_pipeline.py \
  --base_train $features_out_dir/bins_out/merged/bins_merged_train.csv \
  --base_test  $features_out_dir/bins_out/merged/bins_merged_test.csv \
  --train_main $train_main \
  --test_main  $test_main \
  --train_bank $train_bank \
  --test_bank  $test_bank \
  --out_dir   $features_out_dir/cross_out \
  --seed 42 

echo "开始构建RATIO特征..."
echo "=================================================="
python3 day8_ratio_pipeline.py \
  --base_train $features_out_dir/cross_out/merge/cross_merged_train.csv \
  --base_test  $features_out_dir/cross_out/merge/cross_merged_test.csv \
  --train_main $train_main \
  --test_main  $test_main \
  --train_bank $train_bank \
  --test_bank  $test_bank \
  --out_dir   $features_out_dir/ratio_out \
  --seed 42

echo "开始构建LAG特征..."
echo "=================================================="
python3 day8_lag_pipeline.py \
  --base_train $features_out_dir/ratio_out/merge/ratio_merged_train.csv \
  --base_test  $features_out_dir/ratio_out/merge/ratio_merged_test.csv \
  --train_main $train_main \
  --test_main  $test_main \
  --train_bank $train_bank \
  --test_bank  $test_bank \
  --out_dir   $features_out_dir/lag_out \
  --seed 42

echo "开始构建CLUSTER特征..."
echo "=================================================="
python3 day8_cluster_pipeline.py \
  --base_train $features_out_dir/lag_out/merge/lag_merged_train.csv \
  --base_test  $features_out_dir/lag_out/merge/lag_merged_test.csv \
  --train_main $train_main \
  --test_main  $test_main \
  --train_bank $train_bank \
  --test_bank  $test_bank \
  --out_dir   $features_out_dir/cluster_out \
  --seed 42

echo "开始构建POLY特征..."
echo "=================================================="
python3 day8_poly_pipeline.py \
  --base_train $features_out_dir/cluster_out/merge/cluster_merged_train.csv \
  --base_test  $features_out_dir/cluster_out/merge/cluster_merged_test.csv \
  --train_main $train_main \
  --test_main  $test_main \
  --train_bank $train_bank \
  --test_bank  $test_bank \
  --out_dir   $features_out_dir/poly_out \
  --seed 42


# Day11 业务批次（按需启用）
echo "开始构建AFFORD特征..."
echo "=================================================="   
python3 day11_afford_pipeline.py \
  --base_train $features_out_dir/poly_out/merge/poly_merged_train.csv \
  --base_test  $features_out_dir/poly_out/merge/poly_merged_test.csv \
  --out_root   $features_out_dir/day11_afford_out \
  --seed 42

echo "开始构建INCOME特征..."
echo "=================================================="
python3 day11_income_stab_pipeline.py \
  --base_train $features_out_dir/day11_afford_out/merged/afford_merged_train.csv \
  --base_test  $features_out_dir/day11_afford_out/merged/afford_merged_test.csv \
  --out_root   $features_out_dir/day11_income_out \
  --seed 42

echo "开始构建EXPENSE特征..."
echo "=================================================="
python3 day11_expense_structure_pipeline.py \
  --base_train $features_out_dir/day11_income_out/merged/income_merged_train.csv \
  --base_test  $features_out_dir/day11_income_out/merged/income_merged_test.csv \
  --out_root   $features_out_dir/day11_expense_out \
  --seed 42

echo "开始构建CREDIT特征..."
echo "=================================================="
python3 day11_credit_behavior_pipeline.py \
  --base_train $features_out_dir/day11_expense_out/merged/expense_merged_train.csv \
  --base_test  $features_out_dir/day11_expense_out/merged/expense_merged_test.csv \
  --out_root   $features_out_dir/day11_credit_out \
  --seed 42

echo "开始构建SHOCK特征..."
echo "=================================================="
python3 day11_liquidity_shock_pipeline.py \
  --base_train $features_out_dir/day11_credit_out/merged/credit_merged_train.csv \
  --base_test  $features_out_dir/day11_credit_out/merged/credit_merged_test.csv \
  --out_root   $features_out_dir/day11_shock_out \
  --seed 42
  
echo "开始构建BHV特征..."
echo "=================================================="
python3 day11_behavior_flags_pipeline.py \
  --base_train $features_out_dir/day11_shock_out/merged/shock_merged_train.csv \
  --base_test  $features_out_dir/day11_shock_out/merged/shock_merged_test.csv \
  --out_root   $features_out_dir/day11_bhv_out \
  --seed 42

echo "开始构建GEO特征..."
echo "=================================================="
python3 day11_geo_cohort_pipeline.py \
  --base_train $features_out_dir/day11_bhv_out/merged/bhv_merged_train.csv \
  --base_test  $features_out_dir/day11_bhv_out/merged/bhv_merged_test.csv \
  --out_root   $features_out_dir/day11_geo_out \
  --seed 42

echo "开始构建TEAM特征..."
echo "=================================================="
python3 day11_team_features_pipeline.py \
    --base_train $features_out_dir/day11_geo_out/merged/geo_merged_train.csv \
    --base_test $features_out_dir/day11_geo_out/merged/geo_merged_test.csv \
    --train_main $train_main \
    --test_main $test_main \
    --out_root $features_out_dir/day11_team_out \
    --bank_train $train_bank \
    --bank_test $test_bank \
    --seed 42


echo "开始训练..."
echo "=================================================="
python3 train.py $train_dir ./model

echo "开始测试..."
echo "=================================================="
python3 test.py $test_dir ../result

"""