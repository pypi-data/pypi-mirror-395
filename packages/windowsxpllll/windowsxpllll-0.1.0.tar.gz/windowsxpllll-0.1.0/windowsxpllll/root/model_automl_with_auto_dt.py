import os

import optuna
import pandas as pd
import numpy as np
import yaml
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.inspection import permutation_importance
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.covariance import empirical_covariance
from scipy import stats
import warnings
warnings.filterwarnings('ignore')


def load_data(file_path):
    """加载数据"""
    data = pd.read_csv(file_path)
    return data


def decision_tree_binning_objective(trial, X, y, n_splits=5):
    """决策树分箱参数优化的目标函数"""
    # 建议参数范围
    max_depth = trial.suggest_int('max_depth', 2, 8)
    min_samples_leaf = trial.suggest_float('min_samples_leaf', 0.01, 0.2)
    
    # 使用当前参数进行分箱
    X_binned = X.copy()
    for col in X.columns:
        dt = DecisionTreeClassifier(max_depth=max_depth, min_samples_leaf=min_samples_leaf, random_state=42)
        dt.fit(X[[col]], y)
        bins = np.sort(dt.tree_.threshold[dt.tree_.threshold != -2])
        if len(bins) > 0:
            X_binned[col] = np.digitize(X[col], bins)
    
    # 使用分箱后的数据训练XGB模型并评估AUC
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    auc_scores = []
    
    for train_index, val_index in skf.split(X_binned, y):
        X_train, X_val = X_binned.iloc[train_index], X_binned.iloc[val_index]
        y_train, y_val = y.iloc[train_index], y.iloc[val_index]
        
        # 训练模型
        model = XGBClassifier(random_state=42, eval_metric='auc')
        model.fit(X_train, y_train)
        
        # 预测并计算AUC
        y_pred_proba = model.predict_proba(X_val)[:, 1]
        auc = roc_auc_score(y_val, y_pred_proba)
        auc_scores.append(auc)
    
    return np.mean(auc_scores)


def tune_decision_tree_binning(X, y, n_trials=10):
    """使用Optuna优化决策树分箱参数"""
    print("开始决策树分箱参数调优...")
    
    study = optuna.create_study(direction="maximize", sampler=optuna.samplers.TPESampler(seed=42))
    study.optimize(lambda trial: decision_tree_binning_objective(trial, X, y), n_trials=n_trials)
    
    print(f"\n决策树分箱最佳参数: {study.best_params}")
    print(f"最佳AUC: {study.best_value:.4f}")
    
    return study.best_params


def decision_tree_binning(X, y, max_depth=3, min_samples_leaf=0.05, tune_params=False, n_trials=10):
    """使用决策树对连续型变量进行分箱，支持参数调优"""
    # 如果需要调优参数
    if tune_params:
        best_params = tune_decision_tree_binning(X, y, n_trials=n_trials)
        max_depth = best_params['max_depth']
        min_samples_leaf = best_params['min_samples_leaf']
    
    X_binned = X.copy()
    for col in X.columns:
        dt = DecisionTreeClassifier(max_depth=max_depth, min_samples_leaf=min_samples_leaf, random_state=42)
        dt.fit(X[[col]], y)
        bins = np.sort(dt.tree_.threshold[dt.tree_.threshold != -2])
        if len(bins) > 0:
            X_binned[col] = np.digitize(X[col], bins)
    return X_binned


def remove_highly_correlated_features(X, threshold=0.95):
    """移除相关性过高的特征"""
    corr_matrix = X.corr().abs()
    upper_triangle = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    to_drop = [column for column in upper_triangle.columns if any(upper_triangle[column] > threshold)]
    X_filtered = X.drop(to_drop, axis=1)
    return X_filtered, to_drop


def evaluate_feature_importance(X, y, n_splits=5):
    """评估特征有效性"""
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    feature_importances = []
    permutation_importances = []
    
    for train_index, val_index in skf.split(X, y):
        X_train, X_val = X.iloc[train_index], X.iloc[val_index]
        y_train, y_val = y.iloc[train_index], y.iloc[val_index]
        
        # 训练模型
        model = XGBClassifier(random_state=42, eval_metric='auc')
        model.fit(X_train, y_train)
        
        # 特征重要性
        feature_importances.append(model.feature_importances_)
        
        # 排列重要性
        perm_result = permutation_importance(model, X_val, y_val, n_repeats=10, random_state=42, scoring='roc_auc')
        permutation_importances.append(perm_result.importances_mean)
    
    # 计算平均特征重要性
    avg_importance = np.mean(feature_importances, axis=0)
    avg_permutation_importance = np.mean(permutation_importances, axis=0)
    
    # 创建特征重要性DataFrame
    feature_importance_df = pd.DataFrame({
        'feature': X.columns,
        'importance': avg_importance,
        'permutation_importance': avg_permutation_importance
    })
    
    # 按重要性排序
    feature_importance_df = feature_importance_df.sort_values('importance', ascending=False)
    
    return feature_importance_df


def preprocess_data(data, use_binning=True, use_corr_filter=False, corr_threshold=0.95, evaluate_importance=False, tune_binning_params=False, binning_trials=10):
    """特征处理"""
    # 分离特征和目标变量
    # 假设最后一列是目标变量，命名为label
    X = data.iloc[:, :-1]
    y = data.iloc[:, -1]
    
    print(f"原始特征数量: {X.shape[1]}")
    
    # 1. 使用决策树分箱
    if use_binning:
        X = decision_tree_binning(X, y, tune_params=tune_binning_params, n_trials=binning_trials)
        print(f"决策树分箱后特征数量: {X.shape[1]}")
    
    # 2. 移除高相关性特征
    removed_features = []
    if use_corr_filter:
        X, removed_features = remove_highly_correlated_features(X, corr_threshold)
        print(f"移除高相关性特征后数量: {X.shape[1]}, 移除了 {len(removed_features)} 个特征")
    
    # 3. 特征有效性评估
    if evaluate_importance:
        feature_importance_df = evaluate_feature_importance(X, y)
        print("\n特征重要性评估结果（前20个）:")
        print(feature_importance_df.head(20))
        
        # 保存特征重要性结果
        feature_importance_df.to_csv('feature_importance.csv', index=False)
        print("\n特征重要性结果已保存到 feature_importance.csv")
    
    # 特征标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y, X.columns


def load_search_space(config_path):
    """加载搜索空间配置"""
    with open(config_path, "r") as f:
        search_space = yaml.safe_load(f)
    return search_space


def objective(trial, X, y, search_space, n_splits=5):
    """Optuna优化目标函数"""
    # 根据搜索空间生成参数
    params = {"random_state": 42, "eval_metric": "auc"}

    for param_name, config in search_space.items():
        dist_type = config["distribution"]
        low = config["low"]
        high = config["high"]

        if dist_type == "int":
            params[param_name] = trial.suggest_int(param_name, low, high)
        elif dist_type == "float":
            params[param_name] = trial.suggest_float(param_name, low, high)
        elif dist_type == "uniform":
            params[param_name] = trial.suggest_float(param_name, low, high, log=False)
        elif dist_type == "loguniform":
            params[param_name] = trial.suggest_float(param_name, low, high, log=True)

    # 5折交叉验证
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    auc_scores = []

    for train_index, val_index in skf.split(X, y):
        X_train, X_val = X[train_index], X[val_index]
        y_train, y_val = y[train_index], y[val_index]

        # parameters that is not to be tuned
        default_params = {
            "objective": "binary:logistic",
        }

        model = XGBClassifier(**default_params, **params)
        model.fit(X_train, y_train)

        y_pred_proba = model.predict_proba(X_val)[:, 1]
        auc = roc_auc_score(y_val, y_pred_proba)
        auc_scores.append(auc)

    return np.mean(auc_scores)


def tune_hyperparameters(X, y, search_space, n_trials=50, n_splits=5):
    """使用Optuna进行超参数调优"""
    print("开始超参数调优...")

    study = optuna.create_study(direction="maximize", sampler=optuna.samplers.TPESampler(seed=42))
    study.optimize(lambda trial: objective(trial, X, y, search_space, n_splits), n_trials=n_trials)

    print(f"\n最佳参数: {study.best_params}")
    print(f"最佳AUC: {study.best_value:.4f}")

    return study.best_params


def train_model_with_cv(X, y, n_splits=5, **kwargs):
    """使用5折交叉验证训练模型"""
    # 创建5折交叉验证对象
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)

    auc_scores = []

    # 打印参数信息
    print(f"使用参数: {', '.join([f'{k}={v}' for k, v in kwargs.items()])}")

    # 进行5折交叉验证
    for fold, (train_index, val_index) in enumerate(skf.split(X, y)):
        print(f"第 {fold+1} 折交叉验证")

        # 分割数据
        X_train, X_val = X[train_index], X[val_index]
        y_train, y_val = y[train_index], y[val_index]

        # parameters that is not to be tuned
        default_params = {
            "objective": "binary:logistic",
        }

        # 训练模型
        model = XGBClassifier(random_state=42, eval_metric="auc", **default_params, **kwargs)
        model.fit(X_train, y_train)

        # 预测概率
        y_pred_proba = model.predict_proba(X_val)[:, 1]

        # 计算AUC
        auc = roc_auc_score(y_val, y_pred_proba)
        auc_scores.append(auc)
        print(f"第 {fold+1} 折 AUC: {auc:.4f}")

    # 计算平均AUC
    avg_auc = np.mean(auc_scores)
    print(f"\n平均 AUC: {avg_auc:.4f}")

    return avg_auc, auc_scores


def main(tune_hyper=False, n_trials=50, evaluate_importance=False, tune_binning_params=True, binning_trials=10):
    """主函数"""
    # 数据文件路径
    file_path = "./optimal_model_data.csv"

    # 检查数据文件是否存在
    if not os.path.exists(file_path):
        print(f"错误: 数据文件 {file_path} 不存在！")
        print("请确保数据文件存在于当前目录，或修改代码中的file_path变量。")
        return None, None

    # 检查配置文件是否存在
    config_path = os.path.join(os.path.dirname(__file__), "xgb_search_space.yaml")
    if tune_hyper and not os.path.exists(config_path):
        print(f"错误: 配置文件 {config_path} 不存在！")
        return None, None

    # 加载数据
    print("加载数据...")
    data = load_data(file_path)

    # 特征处理
    print("特征处理...")
    X, y, feature_names = preprocess_data(data, 
                                         evaluate_importance=evaluate_importance,
                                         tune_binning_params=tune_binning_params,
                                         binning_trials=binning_trials)

    if tune_hyper:
        # 加载搜索空间
        search_space = load_search_space(config_path)

        # 超参数调优
        best_params = tune_hyperparameters(X, y, search_space, n_trials=n_trials)

        # 使用最佳参数训练模型
        print("\n使用最佳参数进行最终模型训练...")
        avg_auc, auc_scores = train_model_with_cv(X, y, **best_params)
    else:
        # 使用默认参数训练模型
        print("开始5折交叉验证训练...")
        avg_auc, auc_scores = train_model_with_cv(X, y)

    return avg_auc, auc_scores


if __name__ == "__main__":
    # 开启超参数调优，默认50次试验
    main(tune_hyper=True, n_trials=50)
