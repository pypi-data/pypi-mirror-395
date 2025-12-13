import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier

def load_data(file_path):
    """加载数据"""
    data = pd.read_csv(file_path)
    return data

def preprocess_data(data):
    """特征处理"""
    # 分离特征和目标变量
    X = data.iloc[:, :-1]
    y = data.iloc[:, -1]
    
    # 特征标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled, y

def get_base_models():
    """定义基学习器"""
    models = {
        'lightgbm': LGBMClassifier(
            n_estimators=200,
            learning_rate=0.05,
            random_state=42,
            verbose=-1
        ),
        'xgboost': XGBClassifier(
            n_estimators=200,
            learning_rate=0.05,
            random_state=42,
            eval_metric='auc',
            verbosity=0
        ),
        'catboost': CatBoostClassifier(
            iterations=200,
            learning_rate=0.05,
            random_state=42,
            verbose=False
        )
    }
    return models

def get_stacking_predictions(X, y, models, n_splits=5):
    """
    使用交叉验证生成基学习器的预测结果
    """
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    
    # 存储每个模型的预测结果
    train_meta_features = np.zeros((X.shape[0], len(models)))
    
    # 存储每个模型在每折的AUC分数
    model_scores = {name: [] for name in models.keys()}
    
    for fold, (train_index, val_index) in enumerate(skf.split(X, y)):
        print(f"\n第 {fold+1} 折交叉验证")
        
        X_train, X_val = X[train_index], X[val_index]
        y_train, y_val = y.iloc[train_index], y.iloc[val_index]
        
        for idx, (name, model) in enumerate(models.items()):
            print(f"  训练 {name}...")
            
            # 训练模型
            model.fit(X_train, y_train)
            
            # 预测验证集
            y_pred_proba = model.predict_proba(X_val)[:, 1]
            
            # 保存预测结果用于meta模型训练
            train_meta_features[val_index, idx] = y_pred_proba
            
            # 计算AUC
            auc = roc_auc_score(y_val, y_pred_proba)
            model_scores[name].append(auc)
            print(f"    {name} AUC: {auc:.4f}")
    
    return train_meta_features, model_scores

def train_stacking_model(X, y, n_splits=5):
    """
    使用Stacking方法训练模型（DNN元学习器）
    """
    print("="*60)
    print("开始Stacking模型训练（DNN元学习器）")
    print("="*60)
    
    # 获取基学习器
    base_models = get_base_models()
    
    # 第一层：获取基学习器的预测结果
    print("\n【第一层】训练基学习器...")
    train_meta_features, model_scores = get_stacking_predictions(
        X, y, base_models, n_splits
    )
    
    # 打印每个基学习器的平均AUC
    print("\n" + "="*60)
    print("基学习器性能:")
    for name, scores in model_scores.items():
        avg_score = np.mean(scores)
        std_score = np.std(scores)
        print(f"{name:15s}: {avg_score:.4f} (+/- {std_score:.4f})")
    print("="*60)
    
    # 第二层：训练DNN元学习器
    print("\n【第二层】训练DNN元学习器...")
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    
    stacking_scores = []
    
    for fold, (train_index, val_index) in enumerate(skf.split(train_meta_features, y)):
        X_meta_train = train_meta_features[train_index]
        X_meta_val = train_meta_features[val_index]
        y_meta_train = y.iloc[train_index]
        y_meta_val = y.iloc[val_index]
        
        # 训练DNN元学习器
        meta_model = MLPClassifier(
            hidden_layer_sizes=(64, 32, 16),  # 三层隐藏层
            activation='relu',                 # 激活函数
            solver='adam',                     # 优化器
            alpha=0.0001,                      # L2正则化参数
            batch_size=32,                     # 批次大小
            learning_rate='adaptive',          # 自适应学习率
            learning_rate_init=0.001,          # 初始学习率
            max_iter=200,                      # 最大迭代次数
            early_stopping=True,               # 早停
            validation_fraction=0.1,           # 验证集比例
            n_iter_no_change=10,               # 早停patience
            random_state=42,
            verbose=False                      # 不打印训练过程
        )
        meta_model.fit(X_meta_train, y_meta_train)
        
        # 预测
        y_pred_proba = meta_model.predict_proba(X_meta_val)[:, 1]
        
        # 计算AUC
        auc = roc_auc_score(y_meta_val, y_pred_proba)
        stacking_scores.append(auc)
        print(f"第 {fold+1} 折 Stacking AUC: {auc:.4f}")
    
    # 计算平均AUC
    avg_stacking_auc = np.mean(stacking_scores)
    std_stacking_auc = np.std(stacking_scores)
    
    print("\n" + "="*60)
    print(f"DNN Stacking模型平均 AUC: {avg_stacking_auc:.4f} (+/- {std_stacking_auc:.4f})")
    print("="*60)
    
    return avg_stacking_auc, stacking_scores, model_scores

def train_final_stacking_model(X, y):
    """
    在全量数据上训练最终的Stacking模型（用于生产环境）
    """
    print("\n训练最终DNN Stacking模型...")
    
    # 获取基学习器
    base_models = get_base_models()
    
    # 训练所有基学习器
    trained_base_models = {}
    for name, model in base_models.items():
        print(f"训练 {name}...")
        model.fit(X, y)
        trained_base_models[name] = model
    
    # 生成元特征
    meta_features = np.zeros((X.shape[0], len(base_models)))
    for idx, (name, model) in enumerate(trained_base_models.items()):
        meta_features[:, idx] = model.predict_proba(X)[:, 1]
    
    # 训练DNN元学习器
    meta_model = MLPClassifier(
        hidden_layer_sizes=(64, 32, 16),
        activation='relu',
        solver='adam',
        alpha=0.0001,
        batch_size=32,
        learning_rate='adaptive',
        learning_rate_init=0.001,
        max_iter=200,
        early_stopping=True,
        validation_fraction=0.1,
        n_iter_no_change=10,
        random_state=42,
        verbose=False
    )
    meta_model.fit(meta_features, y)
    
    print("最终DNN模型训练完成！")
    
    return trained_base_models, meta_model

def main():
    """主函数"""
    # 数据文件路径
    file_path = "dataset/lasso_reduce.csv"
    
    # 加载数据
    print("加载数据...")
    data = load_data(file_path)
    
    # 特征处理
    print("特征处理...")
    X, y = preprocess_data(data)
    
    # 使用DNN Stacking进行交叉验证
    avg_auc, stacking_scores, model_scores = train_stacking_model(X, y, n_splits=5)
    
    # 训练最终模型
    final_base_models, final_meta_model = train_final_stacking_model(X, y)
    
    return avg_auc, stacking_scores, model_scores, final_base_models, final_meta_model

if __name__ == "__main__":
    results = main()
