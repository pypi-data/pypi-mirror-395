# -*- coding: utf-8 -*-
"""
Day4 - MUL 批次：Target Encoding和WOE编码特征构建
构建基于Target Encoding和WOE编码的特征，包括类别变量的不同表征方式
与基线特征合并后输出，供后续特征工程使用
"""
import os, json, argparse, numpy as np, pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score

DEF_BASE_TRAIN = "./day4/out/sub/train_features_Day4_sub.csv"
DEF_BASE_TEST  = "./day4/out/sub/test_features_Day4_sub.csv"
DEF_TRAIN_MAIN = "../data/train/train.csv"
DEF_TEST_MAIN  = "../data/testaa/testaa.csv"

def ensure_dir(p): os.makedirs(p, exist_ok=True)
def rank01(a):
    s = pd.Series(a)
    r = s.rank(method="average").to_numpy()
    if r.max()==r.min(): return np.zeros_like(r, dtype=float)
    return (r-r.min())/(r.max()-r.min())

def load_baseline(base_train, base_test, train_main_path):
    tr = pd.read_csv(base_train)
    te = pd.read_csv(base_test)
    if "label" not in tr.columns:
        lab = pd.read_csv(train_main_path)[["id","label"]]
        tr = tr.merge(lab, on="id", how="left")
    return tr, te

# --------- OOF Target Encoding / WOE （稳妥版） ---------
def oof_mean_encoding(train, test, y, cols, n_splits=5, seed=42, min_cnt=50, global_smooth=100):
    """对每个单列/双列组合做 OOF mean，带平滑: (sum + prior*alpha)/(cnt + alpha)，alpha=global_smooth"""
    tr = train.copy(); te = test.copy()
    te_out = {}
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=seed)
    prior = y.mean()
    for col in cols:
        name = f"mul_te__{'__'.join(col) if isinstance(col,tuple) else col}"
        oof = np.zeros(len(tr)); te_pred = np.zeros(len(te))
        # 预先分桶
        if isinstance(col, tuple):
            key_tr = tr[list(col)].astype(str).agg("||".join, axis=1)
            key_te = te[list(col)].astype(str).agg("||".join, axis=1)
        else:
            key_tr = tr[col].astype(str); key_te = te[col].astype(str)
        for tr_idx, va_idx in skf.split(tr, y):
            k_tr, k_va = key_tr.iloc[tr_idx], key_tr.iloc[va_idx]
            y_tr = y.iloc[tr_idx]
            grp = pd.concat([k_tr.reset_index(drop=True), y_tr.reset_index(drop=True)], axis=1)
            grp.columns = ["key","y"]
            ss = grp.groupby("key")["y"].agg(["sum","count"])
            # 最小样本过滤 + 平滑
            valid = ss["count"] >= min_cnt
            ss["te"] = (ss["sum"] + prior*global_smooth) / (ss["count"] + global_smooth)
            mp = ss.loc[valid, "te"].to_dict()
            oof[va_idx] = [mp.get(k, prior) for k in k_va]
        # test 用全量拟合
        grp_all = pd.concat([key_tr.reset_index(drop=True), y.reset_index(drop=True)], axis=1)
        grp_all.columns = ["key","y"]
        ss_all = grp_all.groupby("key")["y"].agg(["sum","count"])
        valid_all = ss_all["count"] >= min_cnt
        ss_all["te"] = (ss_all["sum"] + prior*global_smooth) / (ss_all["count"] + global_smooth)
        mp_all = ss_all.loc[valid_all,"te"].to_dict()
        te_pred = np.array([mp_all.get(k, prior) for k in key_te])
        tr[name] = oof; te_out[name] = te_pred
    te_out = pd.DataFrame({"id": te["id"], **te_out})
    return tr[["id"]+[c for c in tr.columns if c.startswith("mul_te__")]], te_out

def woe_encoding(train, test, y, cols, min_cnt=50, clip=5.0):
    """简单 WOE（全量），小样本跳过；加裁剪避免极端"""
    import numpy as np
    tr = train.copy().reset_index(drop=True)
    te = test.copy().reset_index(drop=True)
    y = pd.Series(y).reset_index(drop=True)              # 确保对齐
    assert len(tr) == len(y), "woe_encoding: train 与 y 行数不一致"

    out_tr = {"id": tr["id"].values}
    out_te = {"id": te["id"].values}

    for col in cols:
        name = f"mul_woe__{col}"
        # 把特征转成 key，并确保 y 列存在且命名为 'y'
        g = pd.concat(
            [
                tr[[col]].astype(str).rename(columns={col: "key"}).reset_index(drop=True),
                pd.Series(y.values, name="y")
            ],
            axis=1
        )
        tab = g.groupby("key")["y"].agg(["sum", "count"])
        tab["good"] = tab["count"] - tab["sum"]

        # 过滤极小样本的分组，避免 WOE 极端
        tab = tab[(tab["sum"] >= min_cnt / 2) & (tab["good"] >= min_cnt / 2)].copy()

        # 加一点平滑并做裁剪，避免 log 爆炸
        tab["rate_bad"]  = (tab["sum"]  + 1.0) / (tab["count"] + 2.0)
        tab["rate_good"] = (tab["good"] + 1.0) / (tab["count"] + 2.0)
        tab["woe"] = np.log(np.clip(tab["rate_bad"] / tab["rate_good"], 1e-6, 1e6))
        tab["woe"] = tab["woe"].clip(-clip, clip)

        mp = tab["woe"].to_dict()
        out_tr[name] = tr[col].astype(str).map(mp).fillna(0.0).values
        out_te[name] = te[col].astype(str).map(mp).fillna(0.0).values

    return pd.DataFrame(out_tr), pd.DataFrame(out_te)

def fast_scan_select(baseline_oof, y, add_tr_df, min_gain=0.0002, max_keep=20):
    base_r = rank01(baseline_oof)
    cand_cols = [c for c in add_tr_df.columns if c!="id"]
    gains = []
    for c in cand_cols:
        r = rank01(add_tr_df[c].to_numpy())
        best, best_w = -1.0, None
        for w in np.arange(0.05, 0.55, 0.05):
            auc = roc_auc_score(y, base_r + w*r)
            if auc > best:
                best, best_w = auc, float(w)
        gains.append((c, best - roc_auc_score(y, base_r), best_w, best))
    gains = sorted(gains, key=lambda x: x[3], reverse=True)
    selected, weights = [], []
    cur = base_r.copy(); cur_auc = roc_auc_score(y, cur)
    for c, _, w, _auc in gains:
        r = rank01(add_tr_df[c].to_numpy())
        try_auc = roc_auc_score(y, cur + w*r)
        if try_auc - cur_auc >= min_gain:
            selected.append(c); weights.append(w)
            cur = cur + w*r; cur_auc = try_auc
        if len(selected)>=max_keep: break
    report = pd.DataFrame(gains, columns=["feature","delta_vs_base","best_weight","cand_auc"])
    return selected, weights, cur_auc, report

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base_train", default=DEF_BASE_TRAIN)
    ap.add_argument("--base_test",  default=DEF_BASE_TEST)
    ap.add_argument("--train_main", default=DEF_TRAIN_MAIN)
    ap.add_argument("--test_main",  default=DEF_TEST_MAIN)
    ap.add_argument("--out_root",   default="./day4")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    dir_mul  = os.path.join(args.out_root, "mul_out"); ensure_dir(dir_mul)
    dir_merge= os.path.join(args.out_root, "merged");  ensure_dir(dir_merge)
    dir_scan = os.path.join(args.out_root, "scan");    ensure_dir(dir_scan)
    dir_final= os.path.join(args.out_root, "final");   ensure_dir(dir_final)

    # 读取基线
    base_tr, base_te = load_baseline(args.base_train, args.base_test, args.train_main)
    y = base_tr["label"].astype(int)
    base_feat_cols = [c for c in base_tr.columns if c not in ["id","label"]]

    tr_main = pd.read_csv(args.train_main)
    te_main = pd.read_csv(args.test_main)

    # 准备可编码列（稳妥：低基数）
    # title, residence, term 本身在 S1 就是 OHE；这里用 TE/WOE（不同表征）+ 少量组合
    # zip_code 先做 prefix2 降维
    for df in (tr_main, te_main):
        if "zip_code" in df.columns:
            df["zip_prefix2"] = df["zip_code"].astype(str).str[:2]
        else:
            df["zip_prefix2"] = "NA"

    single_cols = [c for c in ["title","residence","term","zip_prefix2"] if c in tr_main.columns]
    combo_cols  = []
    if all(c in tr_main.columns for c in ["title","term"]): combo_cols.append(("title","term"))
    if all(c in tr_main.columns for c in ["residence","term"]): combo_cols.append(("residence","term"))
    if all(c in tr_main.columns for c in ["zip_prefix2","title"]): combo_cols.append(("zip_prefix2","title"))

    te_tr, te_te = oof_mean_encoding(tr_main[["id"]+list(set(sum(([list(c) if isinstance(c,tuple) else [c] for c in single_cols+combo_cols]), [])))],
                                     te_main[["id"]+list(set(sum(([list(c) if isinstance(c,tuple) else [c] for c in single_cols+combo_cols]), [])))],
                                     y, single_cols+combo_cols, n_splits=5, seed=args.seed, min_cnt=50, global_smooth=100)
    woe_tr, woe_te = woe_encoding(tr_main[["id"]+single_cols], te_main[["id"]+single_cols], y,
                                  single_cols, min_cnt=50, clip=4.0)

    mul_tr = te_tr.merge(woe_tr, on="id", how="left").fillna(0.0)
    mul_te = te_te.merge(woe_te, on="id", how="left").fillna(0.0)
    mul_tr.to_csv(os.path.join(dir_mul, "features_mul_train.csv"), index=False)
    mul_te.to_csv(os.path.join(dir_mul, "features_mul_test.csv"), index=False)

    # 与基线拼接
    add_cols = [c for c in mul_tr.columns if c!="id"]
    tr_merged = base_tr.merge(mul_tr, on="id", how="left")
    te_merged = base_te.merge(mul_te, on="id", how="left")
    tr_merged[add_cols] = tr_merged[add_cols].fillna(0.0)
    te_merged[add_cols] = te_merged[add_cols].fillna(0.0)
    tr_merged.to_csv(os.path.join(dir_merge, "mul_merged_train.csv"), index=False)
    te_merged.to_csv(os.path.join(dir_merge, "mul_merged_test.csv"), index=False)

    print("== DONE MUL ==")

if __name__ == "__main__":
    main()