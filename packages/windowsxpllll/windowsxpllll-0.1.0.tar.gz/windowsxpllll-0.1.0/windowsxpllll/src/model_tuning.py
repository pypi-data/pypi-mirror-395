import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple, List, Optional
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, StratifiedKFold
from sklearn.metrics import roc_auc_score
from xgboost import XGBClassifier
from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier
from sklearn.base import ClassifierMixin

class ModelTuner:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.models = self._get_enabled_models()
        self.tuned_models = {}
    
    def _get_enabled_models(self) -> List[Dict[str, Any]]:
        """获取启用的模型配置"""
        return [model for model in self.config.get("models", []) if model.get("enable", True)]
    
    def _create_model(self, model_name: str, params: Dict[str, Any]) -> ClassifierMixin:
        """创建模型实例"""
        if model_name.lower() == "xgboost":
            return XGBClassifier(**params)
        elif model_name.lower() == "catboost":
            return CatBoostClassifier(**params)
        elif model_name.lower() == "lightgbm":
            return LGBMClassifier(**params)
        else:
            raise ValueError(f"不支持的模型类型: {model_name}")
    
    def tune_models(self, X: np.ndarray, y: np.ndarray) -> Dict[str, Dict[str, Any]]:
        """调优所有启用的模型"""
        results = {}
        for model_config in self.models:
            model_name = model_config["name"]
            print(f"\n开始处理模型: {model_name}")
            
            if model_config.get("tuning", {}).get("enable", False):
                # 执行参数调优
                best_params, best_model = self._tune_model(X, y, model_config)
                self.tuned_models[model_name] = best_model
                results[model_name] = {
                    "best_params": best_params,
                    "model": best_model
                }
            else:
                # 使用默认参数
                model = self._create_model(model_name, model_config["params"])
                self.tuned_models[model_name] = model
                results[model_name] = {
                    "best_params": model_config["params"],
                    "model": model
                }
        
        return results
    
    def _tune_model(self, X: np.ndarray, y: np.ndarray, model_config: Dict[str, Any]) -> Tuple[Dict[str, Any], ClassifierMixin]:
        """调优单个模型"""
        model_name = model_config["name"]
        tuning_config = model_config["tuning"]
        method = tuning_config.get("method", "grid")
        param_grid = tuning_config.get("param_grid", {})
        
        # 创建基础模型
        base_model = self._create_model(model_name, model_config["params"])
        
        # 创建交叉验证对象
        cv = StratifiedKFold(
            n_splits=self.config.get("evaluation", {}).get("cv_folds", 5),
            shuffle=True,
            random_state=self.config.get("data", {}).get("random_state", 42)
        )
        
        if method == "grid":
            # 网格搜索
            search = GridSearchCV(
                base_model,
                param_grid,
                cv=cv,
                scoring="roc_auc",
                n_jobs=-1,
                verbose=1
            )
        elif method == "random":
            # 随机搜索
            search = RandomizedSearchCV(
                base_model,
                param_grid,
                cv=cv,
                scoring="roc_auc",
                n_jobs=-1,
                verbose=1,
                n_iter=10,
                random_state=self.config.get("data", {}).get("random_state", 42)
            )
        else:
            raise ValueError(f"不支持的调优方法: {method}")
        
        # 执行搜索
        search.fit(X, y)
        
        print(f"模型 {model_name} 调优完成")
        print(f"最佳参数: {search.best_params_}")
        print(f"最佳AUC: {search.best_score_:.4f}")
        
        return search.best_params_, search.best_estimator_
    
    def train_models(self, X: np.ndarray, y: np.ndarray) -> None:
        """训练所有模型"""
        for model_name, model in self.tuned_models.items():
            print(f"\n训练模型: {model_name}")
            model.fit(X, y)
    
    def get_tuned_models(self) -> Dict[str, ClassifierMixin]:
        """获取调优后的模型"""
        return self.tuned_models
    
    def evaluate_models(self, X: np.ndarray, y: np.ndarray) -> Dict[str, Dict[str, float]]:
        """使用交叉验证评估所有模型"""
        results = {}
        cv_folds = self.config.get("evaluation", {}).get("cv_folds", 5)
        
        # 创建交叉验证对象
        skf = StratifiedKFold(
            n_splits=cv_folds,
            shuffle=True,
            random_state=self.config.get("data", {}).get("random_state", 42)
        )
        
        for model_name, model in self.tuned_models.items():
            print(f"\n评估模型: {model_name}")
            auc_scores = []
            
            for fold, (train_index, val_index) in enumerate(skf.split(X, y)):
                # 分割数据
                X_train, X_val = X[train_index], X[val_index]
                y_train, y_val = y[train_index], y[val_index]
                
                # 训练模型
                fold_model = self._create_model(
                    model_name,
                    self.models[[m["name"] for m in self.models].index(model_name)]["params"]
                )
                fold_model.fit(X_train, y_train)
                
                # 预测概率
                y_pred_proba = fold_model.predict_proba(X_val)[:, 1]
                
                # 计算AUC
                auc = roc_auc_score(y_val, y_pred_proba)
                auc_scores.append(auc)
                if self.config.get("evaluation", {}).get("verbose", True):
                    print(f"第 {fold+1} 折 AUC: {auc:.4f}")
            
            # 计算平均AUC和标准差
            avg_auc = np.mean(auc_scores)
            std_auc = np.std(auc_scores)
            results[model_name] = {
                "avg_auc": avg_auc,
                "std_auc": std_auc,
                "auc_scores": auc_scores
            }
            
            print(f"模型: {model_name}, 平均 AUC: {avg_auc:.4f}, 标准差: {std_auc:.4f}")
        
        return results