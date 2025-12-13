from typing import Dict, Any, List, Tuple, Union
import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.linear_model import LassoCV

# 导入现有的特征工程功能
from .feature_engineering import EnhancedFeatureEngineer, decision_tree_binning, _apply_precomputed_binning
from .feature_engineering import PrintUtils
from scorecardbundle.feature_encoding import WOE as woe


class FeatureProcessorInterface(ABC):
    """特征处理器接口，定义了所有特征处理器必须实现的方法"""
    
    @abstractmethod
    def process(self, X: pd.DataFrame, y: pd.Series = None) -> Tuple[pd.DataFrame, Any]:
        """
        处理特征数据
        
        Args:
            X: 特征数据
            y: 目标变量（可选）
            
        Returns:
            处理后的特征数据和额外的信息（如规则、元数据等）
        """
        pass
    
    @abstractmethod
    def apply(self, X: pd.DataFrame, metadata: Any) -> pd.DataFrame:
        """
        将学习到的处理规则应用到新数据
        
        Args:
            X: 特征数据
            metadata: 处理过程中学习到的规则或元数据
            
        Returns:
            处理后的特征数据
        """
        pass


class CategoryEncodingProcessor(FeatureProcessorInterface):
    """分类特征编码处理器 - 将字符串型特征转换为数值型"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = config.get("enable", True)
        self.encoding_method = config.get("method", "label")  # label, onehot
        self.encoding_maps = {}  # 保存编码映射关系
    
    def process(self, X: pd.DataFrame, y: pd.Series = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """对训练数据进行分类特征编码"""
        if not self.enabled:
            return X, {}
            
        print(f"   执行分类特征编码，方法: {self.encoding_method}")
        X_encoded = X.copy()
        
        # 识别分类特征（object类型或category类型）
        categorical_cols = X_encoded.select_dtypes(include=['object', 'category']).columns.tolist()
        if not categorical_cols:
            print("   未检测到分类特征")
            return X_encoded, {}
        
        print(f"   检测到分类特征: {categorical_cols}")
        
        # 对每个分类特征进行编码
        for col in categorical_cols:
            if self.encoding_method == "label":
                # 使用标签编码
                le = LabelEncoder()
                # 处理缺失值，将缺失值视为一个特殊类别
                X_encoded[col] = X_encoded[col].fillna("Missing")
                # 获取所有唯一值，确保包含'Missing'
                unique_values = X_encoded[col].unique()
                if "Missing" not in unique_values:
                    # 如果训练数据中没有缺失值，手动添加'Missing'到唯一值列表
                    temp_series = pd.Series(list(unique_values) + ["Missing"])
                    le.fit(temp_series)
                    # 然后对原始数据进行转换
                    X_encoded[col] = le.transform(X_encoded[col])
                else:
                    # 正常训练和转换
                    X_encoded[col] = le.fit_transform(X_encoded[col])
                self.encoding_maps[col] = le
            elif self.encoding_method == "onehot":
                # 使用独热编码
                # 先处理缺失值
                X_encoded[col] = X_encoded[col].fillna("Missing")
                # 创建独热编码矩阵
                onehot = OneHotEncoder(sparse_output=False, drop='first')
                onehot_encoded = onehot.fit_transform(X_encoded[[col]])
                # 创建新的列名
                new_cols = [f"{col}_{cat}" for cat in onehot.categories_[0][1:]]
                # 将独热编码结果添加到DataFrame
                onehot_df = pd.DataFrame(onehot_encoded, columns=new_cols, index=X_encoded.index)
                X_encoded = pd.concat([X_encoded, onehot_df], axis=1)
                # 删除原始列
                X_encoded = X_encoded.drop(columns=[col])
                self.encoding_maps[col] = {
                    "type": "onehot",
                    "encoder": onehot,
                    "new_cols": new_cols
                }
        
        print(f"   分类特征编码完成，编码特征数量: {len(self.encoding_maps)}")
        return X_encoded, self.encoding_maps
    
    def apply(self, X: pd.DataFrame, metadata: Dict[str, Any]) -> pd.DataFrame:
        """将分类特征编码规则应用到新数据"""
        if not metadata:
            return X

        X_encoded = X.copy()
        
        for col, encoder_info in metadata.items():
            if col not in X_encoded.columns:
                continue
                
            if isinstance(encoder_info, LabelEncoder):
                # 应用标签编码
                le = encoder_info
                # 处理缺失值，将缺失值视为一个特殊类别
                X_encoded[col] = X_encoded[col].fillna("Missing")
                # 获取所有可能的类别
                classes = list(le.classes_)
                # 处理训练集中未出现的类别和缺失值
                X_encoded[col] = X_encoded[col].apply(lambda x: x if x in classes else "Missing")
                # 确保'Missing'在classes中，如果不在则添加
                if "Missing" not in classes:
                    # 将'Missing'添加到classes中，并重新训练编码器
                    new_classes = classes + ["Missing"]
                    le.classes_ = np.array(new_classes)
                # 进行转换
                X_encoded[col] = le.transform(X_encoded[col])
            elif isinstance(encoder_info, dict) and encoder_info["type"] == "onehot":
                # 应用独热编码
                onehot = encoder_info["encoder"]
                new_cols = encoder_info["new_cols"]
                # 处理缺失值
                X_encoded[col] = X_encoded[col].fillna("Missing")
                # 处理训练集中未出现的类别
                X_encoded[col] = X_encoded[col].apply(lambda x: x if x in onehot.categories_[0] else "Missing")
                # 创建独热编码矩阵
                onehot_encoded = onehot.transform(X_encoded[[col]])
                # 将独热编码结果添加到DataFrame
                onehot_df = pd.DataFrame(onehot_encoded, columns=new_cols, index=X_encoded.index)
                X_encoded = pd.concat([X_encoded, onehot_df], axis=1)
                # 删除原始列
                X_encoded = X_encoded.drop(columns=[col])
        
        return X_encoded


class DecisionTreeBinningProcessor(FeatureProcessorInterface):
    """决策树分箱处理器"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.method = config.get("method", "decision_tree")
        self.tune_params = config.get("tune_params", False)
        self.n_trials = config.get("n_trials", 50)
        self.params = config.get("params", {})
    
    def process(self, X: pd.DataFrame, y: pd.Series = None) -> Tuple[pd.DataFrame, Dict[str, List[float]]]:
        """对训练数据进行分箱"""
        if self.method != "decision_tree":
            return X, {}
            
        print(f"   使用决策树分箱，参数调优: {self.tune_params}")
        X_binned, binning_rules = decision_tree_binning(
            X, y,
            tune_params=self.tune_params,
            n_trials=self.n_trials,
            **self.params
        )
        # 返回空的分箱规则，因为当前decision_tree_binning函数不返回规则
        woe_encode = self.config.get("woe_encode", False)
        print(f"   woe编码: {woe_encode}")
        if woe_encode:
            print("=" * 50)
            print("执行woe编码")
            print("=" * 50)
            bins_dict = binning_rules
            cols_to_encode = [f"{col}_binned" for col, bins in bins_dict.items() if len(bins) > 0]

            trans_woe = woe.WOE_Encoder(output_dataframe=True)
            X_woe = trans_woe.fit_transform(X_binned[cols_to_encode], y)
            X_binned.loc[:, cols_to_encode] = X_woe
            self.trans_woe = trans_woe
        return X_binned, binning_rules
    
    def apply(self, X: pd.DataFrame, metadata: Dict[str, List[float]]) -> pd.DataFrame:
        """将分箱规则应用到新数据"""
        if not metadata:
            return X

        x_binned = _apply_precomputed_binning(X, metadata)
        
        print("   应用决策树分箱规则到新数据...")
        woe_encode = self.config.get("woe_encode", False)
        if woe_encode:
            print("=" * 50)
            print("执行woe编码")
            print("=" * 50)
            bins_dict = metadata
            cols_to_encode = [f"{col}_binned" for col, bins in bins_dict.items() if len(bins) > 0]
            x_woe = self.trans_woe.transform(x_binned[cols_to_encode])
            x_binned.loc[:, cols_to_encode] = x_woe
        return x_binned

class FeatureSelectionProcessor(FeatureProcessorInterface):
    """特征选择处理器"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = config.get("enable", False)
        self.method = config.get("method", "lasso")
        self.params = config.get("params", {})
        self.threshold = self.params.get("threshold", 0.01)
    
    def _lasso_feature_selection(self, X: pd.DataFrame, X_scaled: pd.DataFrame, y: pd.Series) -> List[str]:
        """使用LASSO进行特征选择"""
        print(f"   执行LASSO特征选择，alpha={self.threshold}")
        
        # LASSO特征选择
        lasso = LassoCV(cv=5, random_state=42, max_iter=10000)
        lasso.fit(X_scaled.values, y)
        
        # 选择非零系数的特征
        selected_features = np.abs(lasso.coef_) > 0
        selected_feature_names = X.columns[selected_features].tolist()
        
        print(f"   选择的特征数量: {len(selected_feature_names)}")
        return selected_feature_names
    
    def process(self, X: pd.DataFrame, y: pd.Series = None) -> Tuple[pd.DataFrame, List[str]]:
        """执行特征选择"""
        if not self.enabled or y is None:
            return X, X.columns.tolist()
            
        print(f"   执行特征选择，方法: {self.method}")
        
        # 处理非数值数据
        X_processed = X.copy()
        for col in X_processed.columns:
            # 尝试将列转换为数值类型
            X_processed[col] = pd.to_numeric(X_processed[col], errors='coerce')
        
        # 填充缺失值
        X_processed = X_processed.fillna(X_processed.median())
        X_processed = X_processed.fillna(0)
        
        # 标准化数据
        scaler = StandardScaler()
        X_scaled = pd.DataFrame(scaler.fit_transform(X_processed), columns=X_processed.columns)
        
        selected_features = X_processed.columns.tolist()
        
        # 根据方法选择特征
        if self.method == "lasso":
            selected_features = self._lasso_feature_selection(X_processed, X_scaled, y)
        # 可以在这里添加其他特征选择方法的支持
        
        # 选择特征
        X_selected = X_processed[selected_features]
        
        return X_selected, selected_features
    
    def apply(self, X: pd.DataFrame, metadata: List[str]) -> pd.DataFrame:
        """将特征选择规则应用到新数据"""
        if not metadata:
            return X
        
        # 只保留处理过程中选择的特征
        features_to_keep = [f for f in metadata if f in X.columns]
        if not features_to_keep:
            return X
        
        return X[features_to_keep]


class EnhancedFeatureProcessor(FeatureProcessorInterface):
    """增强特征处理器 - 整合多重共线性处理和特征重要性筛选"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = config.get("enable", False)
        self.corr_threshold = config.get("corr_threshold", 0.95)
        self.selection_threshold = config.get("selection_threshold", 25)
        self.remove_collinearity = config.get("remove_collinearity", True)
        self.use_feature_selection = config.get("use_feature_selection", True)
    
    def process(self, X: pd.DataFrame, y: pd.Series = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """执行增强特征处理：多重共线性处理 + 特征重要性筛选"""
        if not self.enabled:
            return X, {"selected_features": X.columns.tolist()}
            
        print(f"   执行增强特征处理")
        
        # 保存原始特征列表
        original_features = X.columns.tolist()
        
        # 1. 处理多重共线性
        removed_collinear_features = []
        if self.remove_collinearity:
            X, removed_collinear_features = EnhancedFeatureEngineer.remove_multicollinearity(
                X, threshold=self.corr_threshold
            )
        
        # 2. 特征重要性筛选
        selected_features = X.columns.tolist()
        feature_importance_df = None
        
        if self.use_feature_selection and y is not None:
            X, selected_features, feature_importance_df = EnhancedFeatureEngineer.select_by_importance(
                X, y, threshold_percentile=self.selection_threshold, method="xgboost"
            )
        
        # 保存元数据
        metadata = {
            "selected_features": selected_features,
            "removed_collinear_features": removed_collinear_features,
            "original_features": original_features
        }
        
        return X, metadata
    
    def apply(self, X: pd.DataFrame, metadata: Dict[str, Any]) -> pd.DataFrame:
        """应用增强特征处理规则到新数据"""
        if not metadata or "selected_features" not in metadata:
            return X
        
        selected_features = metadata["selected_features"]
        # 只保留处理过程中选择的特征
        features_to_keep = [f for f in selected_features if f in X.columns]
        
        return X[features_to_keep]


class FeatureProcessor:
    """特征处理器，统一管理和应用各种特征加工策略"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化特征处理器
        
        Args:
            config: 配置文件，包含各种特征处理器的配置
        """
        self.config = config
        self.processors: Dict[str, FeatureProcessorInterface] = {}
        self.processor_metadata: Dict[str, Any] = {}
        
        # 初始化默认处理器
        self._initialize_processors()
    
    def _initialize_processors(self):
        """初始化特征处理器"""
        # 获取特征工程配置
        feature_engineering_config = self.config.get("feature_engineering", {})
        
        # 初始化分类特征编码处理器（必须在分箱前执行）
        # 创建默认的分类编码配置
        category_encoding_config = {
            "enable": True,
            "method": "label"
        }
        # 从配置文件中获取分类编码配置
        category_encoding_config.update(feature_engineering_config.get("category_encoding", {}))
        if category_encoding_config.get("enable", True):
            self.add_processor("category_encoding", CategoryEncodingProcessor(category_encoding_config))
        
        # 初始化分箱处理器
        binning_config = feature_engineering_config.get("binning", {})
        if binning_config.get("enable", False):
            self.add_processor("binning", DecisionTreeBinningProcessor(binning_config))
        
        # 初始化特征选择处理器
        feature_selection_config = feature_engineering_config.get("feature_selection", {})
        if feature_selection_config.get("enable", False):
            self.add_processor("feature_selection", FeatureSelectionProcessor(feature_selection_config))
        
        # 初始化增强特征处理器（替换原有的特征删除处理器）
        enhanced_fe_config = feature_engineering_config.get("enhanced_feature_engineering", {})
        if enhanced_fe_config.get("enable", False):
            self.add_processor("enhanced_feature", EnhancedFeatureProcessor(enhanced_fe_config))
    
    def add_processor(self, name: str, processor: FeatureProcessorInterface):
        """
        添加新的特征处理器（扩展点）
        
        Args:
            name: 处理器名称
            processor: 特征处理器实例
        """
        self.processors[name] = processor
    
    def process(self, X: pd.DataFrame, y: pd.Series = None) -> pd.DataFrame:
        """
        处理训练数据，应用所有启用的特征处理器
        
        Args:
            X: 特征数据
            y: 目标变量（可选）
            
        Returns:
            处理后的特征数据
        """
        X_processed = X.copy()
        
        if not self.processors:
            print("没有启用任何特征处理器")
            return X_processed
        
        PrintUtils.print_section("执行特征处理")
        
        for name, processor in self.processors.items():
            print(f"\n处理步骤: {name}")
            X_processed, metadata = processor.process(X_processed, y)
            self.processor_metadata[name] = metadata
            print(f"   处理后特征数量: {X_processed.shape[1]}")
        
        PrintUtils.print_section("特征处理完成")
        print(f"最终特征数量: {X_processed.shape[1]}")
        
        return X_processed
    
    def apply(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        将训练好的特征处理规则应用到新数据
        
        Args:
            X: 特征数据
            
        Returns:
            处理后的特征数据
        """
        X_processed = X.copy()
        
        for name, processor in self.processors.items():
            metadata = self.processor_metadata.get(name)
            if metadata is not None:
                X_processed = processor.apply(X_processed, metadata)
        
        return X_processed
    
    def get_processor_metadata(self, processor_name: str) -> Any:
        """
        获取特定处理器的元数据
        
        Args:
            processor_name: 处理器名称
            
        Returns:
            处理器的元数据
        """
        return self.processor_metadata.get(processor_name)
    
    def list_processors(self) -> List[str]:
        """
        列出所有启用的处理器
        
        Returns:
            启用的处理器名称列表
        """
        return list(self.processors.keys())
