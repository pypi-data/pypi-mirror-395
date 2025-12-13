
# 导入主要模块，方便用户直接使用
from .config import Config
from .feature_engineering import FeatureEngineer
from .feature_processor import FeatureProcessor
from .model_automl import AutoMLPipeline
from .model_tuning import ModelTuner
from .model_ensemble import EnsembleModel
from .model_stacking import StackingModel
from .evaluation import ModelEvaluator

# 定义公开的API
__all__ = [
    'Config',
    'FeatureEngineer', 
    'FeatureProcessor',
    'AutoMLPipeline',
    'ModelTuner',
    'EnsembleModel',
    'StackingModel',
    'ModelEvaluator'
]

# 包初始化信息
print(f"AutoML Pipeline {__version__} 加载成功")

"""
cat_search_space.yaml

learning_rate:
  distribution: loguniform
  low: 0.01
  high: 0.02
iterations:
  distribution: int
  low: 50
  high: 500
depth:
  distribution: int
  low: 3
  high: 8
l2_leaf_reg:
  distribution: loguniform
  low: 0.001
  high: 8.0
bagging_temperature:
  distribution: float
  low: 0.0
  high: 10.0
random_strength:
  distribution: float
  low: 0.0
  high: 10.0
border_count:
  distribution: int
  low: 32
  high: 255
"""

"""
lgb_search_space.yaml

learning_rate:
  distribution: loguniform
  low: 0.01
  high: 0.02
n_estimators:
  distribution: int
  low: 50
  high: 500
max_depth:
  distribution: int
  low: 3
  high: 9
num_leaves:
  distribution: int
  low: 10
  high: 100
min_child_samples:
  distribution: int
  low: 10
  high: 200
subsample:
  distribution: uniform
  low: 0.6
  high: 1.0
colsample_bytree:
  distribution: uniform
  low: 0.6
  high: 1.0
min_split_gain:
  distribution: loguniform
  low: 0.001
  high: 5.0
reg_alpha:
  distribution: loguniform
  low: 0.001
  high: 1.0
reg_lambda:
  distribution: loguniform
  low: 0.001
  high: 1.0
"""

"""
xgb_search_space.yaml

learning_rate:
  distribution: loguniform
  low: 0.01
  high: 0.3
n_estimators:
  distribution: int
  low: 50
  high: 500
max_depth:
  distribution: int
  low: 3
  high: 10
min_child_weight:
  distribution: float
  low: 0.1
  high: 10.0
subsample:
  distribution: uniform
  low: 0.6
  high: 1.0
colsample_bytree:
  distribution: uniform
  low: 0.6
  high: 1.0
gamma:
  distribution: loguniform
  low: 0.001
  high: 5.0
reg_alpha:
  distribution: loguniform
  low: 0.001
  high: 1.0
reg_lambda:
  distribution: loguniform
  low: 0.001
  high: 1.0



"""