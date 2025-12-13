import os
import yaml
import pandas as pd
import numpy as np
import warnings
import optuna
import pickle
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score, accuracy_score, f1_score, precision_score, recall_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler

# 导入自定义模块
from src.model_automl import load_search_space, tune_hyperparameters
from src.feature_processor import FeatureProcessor
from src.model_ensemble import ModelEnsemble
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier

# 忽略警告
warnings.filterwarnings('ignore')


def load_config(config_path):
    """加载配置文件"""
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config

def run_full_pipeline(X_train, y_train, X_val, y_val, config, fold_index):
    """运行完整流程（每一折）
    
    参数:
    X_train: 训练集特征
    y_train: 训练集标签
    X_val: 验证集特征
    y_val: 验证集标签
    config: 配置文件
    fold_index: 折索引
    
    返回:
    fold_results: 该折的模型结果
    feature_processor: 训练好的特征处理器
    trained_models: 训练好的模型字典
    model_ensemble: 模型融合对象
    """
    print(f"\n{'='*60}")
    print(f"第 {fold_index+1} 折交叉验证")
    print(f"{'='*60}")
    
    print(f"训练集形状: {X_train.shape}, 验证集形状: {X_val.shape}")
    
    # 1. 特征处理
    print("1. 执行特征处理...")
    
    # 初始化特征处理器
    feature_processor = FeatureProcessor(config)
    
    # 处理训练数据
    X_train_processed = feature_processor.process(X_train, y_train)
    
    # 将处理规则应用到验证数据
    X_val_processed = feature_processor.apply(X_val)
    
    print(f"   特征处理完成，训练集形状: {X_train_processed.shape}, 验证集形状: {X_val_processed.shape}")
    
    # 2. 模型训练和评估
    print("2. 模型训练和评估...")
    models_config = config.get("models", [])
    fold_results = {}
    trained_models = {}
    model_ensemble = None
    
    for model_config in models_config:
        model_name = model_config["name"]
        if not model_config.get("enable", True):
            continue
        
        print(f"\n   处理模型: {model_name}")
        
        # 检查是否启用automl
        automl_config = model_config.get("automl", {})
        automl_enable = automl_config.get("enable", False)
        
        if automl_enable:
            print(f"   启用AutoML超参数调优...")
            # 加载搜索空间
            search_space_path = automl_config.get("search_space_path")
            if not os.path.isabs(search_space_path):
                search_space_path = os.path.join(os.path.dirname(__file__), search_space_path)
            
            search_space = load_search_space(search_space_path)
            
            # 超参数调优
            best_params = tune_hyperparameters(
                X_train_processed, y_train, 
                search_space, 
                n_trials=automl_config.get("n_trials", 50), 
                model_type=model_name.lower()
            )
            
            # 使用最佳参数创建模型
            print(f"   使用最佳参数训练模型...")
        else:
            # 使用默认参数
            best_params = model_config.get("params", {})
            print(f"   使用默认参数训练模型...")
        
        # 创建和训练模型
        if model_name.lower() == "xgboost":
            model = XGBClassifier(
                objective="binary:logistic",
                eval_metric="auc",
                random_state=config.get("data", {}).get("random_state", 42),
                verbose=False,
                **best_params
            )
        elif model_name.lower() == "lightgbm":
            model = LGBMClassifier(
                objective="binary",
                metric="auc",
                random_state=config.get("data", {}).get("random_state", 42),
                **best_params
            )
        elif model_name.lower() == "catboost":
            model = CatBoostClassifier(
                objective="Logloss",
                eval_metric="AUC",
                random_state=config.get("data", {}).get("random_state", 42),
                # verbose=False,
                **best_params
            )
        else:
            print(f"   不支持的模型类型: {model_name}")
            continue
        
        model.fit(X_train_processed, y_train)
        
        # 将训练好的模型添加到trained_models字典
        trained_models[model_name] = model
        
        # 评估模型
        print(f"   评估模型...")
        y_pred_proba = model.predict_proba(X_val_processed)[:, 1]
        y_pred = (y_pred_proba >= 0.5).astype(int)
        
        auc = roc_auc_score(y_val, y_pred_proba)
        accuracy = accuracy_score(y_val, y_pred)
        f1 = f1_score(y_val, y_pred)
        precision = precision_score(y_val, y_pred)
        recall = recall_score(y_val, y_pred)
        
        print(f"   模型: {model_name}")
        print(f"   AUC: {auc:.4f}, Accuracy: {accuracy:.4f}, F1: {f1:.4f}")
        print(f"   Precision: {precision:.4f}, Recall: {recall:.4f}")
        
        # 保存结果
        fold_results[model_name] = {
            "auc": auc,
            "accuracy": accuracy,
            "f1": f1,
            "precision": precision,
            "recall": recall,
            "best_params": best_params
        }
    
    # 模型融合
    model_ensemble = None
    ensemble_config = config.get("ensemble", {})
    if ensemble_config.get("enable", False):
        print(f"\n   开始模型融合")
        model_ensemble = ModelEnsemble(ensemble_config, trained_models)
        if model_ensemble.create_ensemble():
            # 训练融合模型
            model_ensemble.fit(X_train_processed, y_train)
            
            # 评估融合模型
            y_pred_proba = model_ensemble.predict_proba(X_val_processed)
            y_pred = (y_pred_proba >= 0.5).astype(int)
            
            auc = roc_auc_score(y_val, y_pred_proba)
            accuracy = accuracy_score(y_val, y_pred)
            f1 = f1_score(y_val, y_pred)
            precision = precision_score(y_val, y_pred)
            recall = recall_score(y_val, y_pred)
            
            print(f"   模型: Ensemble")
            print(f"   AUC: {auc:.4f}, Accuracy: {accuracy:.4f}, F1: {f1:.4f}")
            print(f"   Precision: {precision:.4f}, Recall: {recall:.4f}")
            
            # 保存融合模型结果
            fold_results["Ensemble"] = {
                "auc": auc,
                "accuracy": accuracy,
                "f1": f1,
                "precision": precision,
                "recall": recall,
                "best_params": ensemble_config.get("params", {})
            }
    
    return fold_results, feature_processor, trained_models, model_ensemble


def main():
    """主函数"""
    print("="*60)
    print("开始标准K折验证流程")
    print("="*60)
    
    # 1. 加载配置文件
    config_path = "config.yaml"
    print(f"1. 加载配置文件: {config_path}")
    config = load_config(config_path)
    print(f"   配置加载成功: {config}")
    
    # 2. 加载数据
    data_config = config.get("data", {})
    file_path = data_config.get("file_path")
    print(f"2. 加载数据文件: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"错误: 数据文件 {file_path} 不存在！")
        return
    
    data = pd.read_csv(file_path)
    print(f"   数据形状: {data.shape}")
    
    # 3. 设置K折验证参数
    evaluation_config = config.get("evaluation", {})
    cv_folds = evaluation_config.get("cv_folds", 5)
    random_state = config.get("data", {}).get("random_state", 42)
    
    print(f"3. 配置K折验证: {cv_folds} 折")
    
    # 4. 最外层K折验证
    print("4. 开始最外层K折验证...")
    skf = StratifiedKFold(
        n_splits=cv_folds,
        shuffle=True,
        random_state=random_state
    )
    
    # 根据配置分离特征和目标变量
    target_column = config.get("data", {}).get("target_column")
    
    if target_column is None or target_column == "null":
        # 假设最后一列是目标变量
        raise ValueError("未指定目标列，且数据中没有明确的目标列。请在配置文件中指定 'target_column'。")
    else:
        if target_column not in data.columns:
            raise ValueError(f"指定的目标列 '{target_column}' 不存在于数据中。请检查配置文件。")
        # 使用指定的目标列
        print(f"*****   目标列名: {target_column} ********")
        X = data.drop(columns=[target_column])
        y = data[target_column]
    
    # 初始化结果存储
    all_results = {}
    models_config = config.get("models", [])
    all_fold_models = {}
    
    # 执行K折验证
    for fold_index, (train_index, val_index) in enumerate(skf.split(X, y)):
        # 分割数据
        X_train, X_val = X.iloc[train_index], X.iloc[val_index]
        y_train, y_val = y.iloc[train_index], y.iloc[val_index]
        
        fold_results, feature_processor, trained_models, model_ensemble = run_full_pipeline(X_train, y_train, X_val, y_val, config, fold_index)
        
        # 保存所有折的模型
        all_fold_models[f"fold_{fold_index}"] = {
            "feature_processor": feature_processor,
            "trained_models": trained_models,
            "model_ensemble": model_ensemble
        }
        
        # 保存结果
        for model_name, result in fold_results.items():
            # 检查模型名称是否已经在all_results字典中，如果不在则创建
            if model_name not in all_results:
                all_results[model_name] = {
                    "metrics": {
                        "auc": [],
                        "accuracy": [],
                        "f1": [],
                        "precision": [],
                        "recall": []
                    },
                    "best_params_list": []
                }
            
            all_results[model_name]["metrics"]["auc"].append(result["auc"])
            all_results[model_name]["metrics"]["accuracy"].append(result["accuracy"])
            all_results[model_name]["metrics"]["f1"].append(result["f1"])
            all_results[model_name]["metrics"]["precision"].append(result["precision"])
            all_results[model_name]["metrics"]["recall"].append(result["recall"])
            all_results[model_name]["best_params_list"].append(result["best_params"])
    
    # 5. 计算平均指标
    print("\n" + "="*60)
    print("汇总结果")
    print("="*60)
    
    avg_results = {}
    for model_name, result in all_results.items():
        avg_metrics = {}
        for metric, scores in result["metrics"].items():
            avg_metrics[metric] = np.mean(scores)
            avg_metrics[f"{metric}_std"] = np.std(scores)
        
        avg_results[model_name] = {
            "average_metrics": avg_metrics,
            "all_fold_metrics": result["metrics"]
        }
        
        # 打印结果
        print(f"\n模型: {model_name}")
        for metric, avg_score in avg_metrics.items():
            if "std" in metric:
                print(f"   {metric}: {avg_score:.4f}")
            else:
                print(f"   {metric}: {avg_score:.4f} (±{avg_metrics[f'{metric}_std']:.4f})")
    
    # 6. 输出结果
    print("\n" + "="*60)
    print("标准K折验证流程完成")
    print("="*60)
    
    return avg_results, all_fold_models, config


def save_all_models(model_path, config, all_fold_models):
    """保存所有折的模型、特征处理器和相关配置到文件
    
    参数:
    model_path: 模型保存路径
    config: 配置文件
    all_fold_models: 所有折的模型字典
    """
    print(f"\n保存所有模型到文件: {model_path}")
    
    # 创建保存目录
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    
    # 保存模型
    model_data = {
        'config': config,
        'all_fold_models': all_fold_models,
        'version': '1.0'
    }
    
    with open(model_path, 'wb') as f:
        pickle.dump(model_data, f)
    
    print(f"模型保存成功: {model_path}")


def load_all_models(model_path):
    """从文件加载所有折的模型、特征处理器和相关配置
    
    参数:
    model_path: 模型加载路径
    
    返回:
    config: 配置文件
    all_fold_models: 所有折的模型字典
    """
    print(f"\n从文件加载模型: {model_path}")
    
    if not os.path.exists(model_path):
        print(f"错误: 模型文件 {model_path} 不存在！")
        return None, None
    
    with open(model_path, 'rb') as f:
        model_data = pickle.load(f)
    
    print(f"模型加载成功，版本: {model_data.get('version', 'unknown')}")
    
    return model_data['config'], model_data['all_fold_models']


def predict_with_all_models(X_new, all_fold_models, use_ensemble=False, model_name=None):
    """使用所有折的模型进行预测并取平均值
    
    参数:
    X_new: 新的特征数据
    all_fold_models: 所有折的模型字典
    use_ensemble: 是否使用融合模型
    model_name: 指定使用哪个模型进行预测（如果不使用融合模型）
    
    返回:
    predictions: 预测概率数组
    """
    print("\n执行多模型预测...")
    
    all_predictions = []
    
    for fold_name, fold_data in all_fold_models.items():
        print(f"   处理{fold_name}...")
        
        # 获取该折的组件
        feature_processor = fold_data['feature_processor']
        trained_models = fold_data['trained_models']
        model_ensemble = fold_data['model_ensemble']
        
        # 处理新数据
        X_processed = feature_processor.apply(X_new)
        
        # 进行预测
        if use_ensemble and model_ensemble is not None:
            # 使用融合模型
            fold_pred = model_ensemble.predict_proba(X_processed)
        else:
            # 使用指定模型或默认第一个模型
            if model_name and model_name in trained_models:
                fold_pred = trained_models[model_name].predict_proba(X_processed)[:, 1]
            else:
                # 使用第一个可用模型
                first_model_name = next(iter(trained_models.keys()))
                fold_pred = trained_models[first_model_name].predict_proba(X_processed)[:, 1]
        
        all_predictions.append(fold_pred)
    
    # 计算平均值
    avg_predictions = np.mean(all_predictions, axis=0)
    
    print(f"   多模型预测完成，使用了 {len(all_fold_models)} 个模型进行平均")
    
    return avg_predictions


def predict_pipeline(X_new, model_path, use_ensemble=False, model_name=None, threshold=0.5):
    """完整的预测流程，包括模型加载、特征处理和预测
    
    参数:
    X_new: 新的特征数据
    model_path: 模型加载路径
    use_ensemble: 是否使用融合模型
    model_name: 指定使用哪个模型进行预测（如果不使用融合模型）
    threshold: 预测类别的阈值
    
    返回:
    y_pred_proba: 预测概率数组
    y_pred: 预测类别数组
    """
    print("\n" + "="*60)
    print("执行预测流水线")
    print("="*60)
    
    # 1. 加载模型
    config, all_fold_models = load_all_models(model_path)
    if config is None or all_fold_models is None:
        return None, None
    
    # 2. 执行预测
    y_pred_proba = predict_with_all_models(X_new, all_fold_models, use_ensemble, model_name)
    
    # 3. 转换为类别
    y_pred = (y_pred_proba >= threshold).astype(int)
    
    print("\n" + "="*60)
    print("预测流水线完成")
    print("="*60)
    
    return y_pred_proba, y_pred


if __name__ == "__main__":
    avg_results, all_fold_models, config = main()
    
    # 保存模型
    model_save_path = "saved_models/model.pkl"
    save_all_models(model_save_path, config, all_fold_models)
