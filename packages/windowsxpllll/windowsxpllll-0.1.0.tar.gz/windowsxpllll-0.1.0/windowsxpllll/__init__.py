"""
windowsxpllll - 机器学习管道工具包
"""

__version__ = "0.1.0"
__author__ = "Your Name"

# 导入主要模块，方便用户使用
from .src.config import Config
from .src.feature_engineering import FeatureEngineer
from .src.feature_processor import FeatureProcessor
from .src.model_automl import AutoMLPipeline
from .src.model_tuning import ModelTuner
from .src.model_ensemble import EnsembleModel
from .src.model_stacking import Stackingfrom 

# 导入projects和root中的模块（如果需要）
from .projects import main_stand
from .root import model_automl_with_auto_dt

__all__ = [
    'Config', 'FeatureEngineer', 'FeatureProcessor', 
    'AutoMLPipeline', 'ModelTuner', 'EnsembleModel', 
    'StackingModel', 'ModelEvaluator',
    'main_stand', 'model_automl_with_auto_dt'
]

def main():
    """命令行入口点"""
    print(f"windowsxpllllversion__")
    # 这里可以添加命令行逻辑
"""

1、以下四个文件置于root目录下
model_automl_with_auto_dt.py
README.md -> readme.py
requirements.txt -> requirements.py
TimeSeriesFactor.py
2、projects目录下的config.yaml内容置于__init__.py中，同时重命名为同名py文件
3、src目录下cat_search_space.yaml、lgb_search_space.yaml、xgb_search_space.yaml内容置于__init__.py中，同时分别重命名为同名py文件
4、原目录结构如下，根目录-projects-src，目前为打包方便，将root、projects、src并列了

D:.
│  model_automl_with_auto_dt.py
│  pyproject.toml
│  README.md
│  requirements.txt
│  TimeSeriesFactor.py
│  uv.lock
│
├─projects
│  │  .DS_Store
│  │  config.yaml
│  │  config_new.yaml
│  │  dimension_reduction.py
│  │  evaluation_report.csv
│  │  main_stand.py
│  │  predict.py
│  │  test_feature.csv
│  │
│  ├─catboost_info
│  │  │  .DS_Store
│  │  │  catboost_training.json
│  │  │  learn_error.tsv
│  │  │  time_left.tsv
│  │  │
│  │  ├─learn
│  │  │      events.out.tfevents
│  │  │
│  │  ├─test
│  │  └─tmp
│  ├─models
│  │      ensemble_model.joblib
│  │      feature_engineering.joblib
│  │      lightgbm_model.joblib
│  │      xgboost_model.joblib
│  │
│  ├─saved_models
│  ├─src
│  │  │  .DS_Store
│  │  │  cat_search_space.yaml
│  │  │  config.py
│  │  │  evaluation.py
│  │  │  feature_engineering.py
│  │  │  feature_processor.py
│  │  │  lgb_search_space.yaml
│  │  │  model_automl.py
│  │  │  model_ensemble.py
│  │  │  model_stacking.py
│  │  │  model_tuning.py
│  │  │  xgb_search_space.yaml
│  │  │
│  │  └─__pycache__
│  │          config.cpython-312.pyc
│  │          evaluation.cpython-312.pyc
│  │          feature_engineering.cpython-312.pyc
│  │          feature_processor.cpython-312.pyc
│  │          model.cpython-312.pyc
│  │          model_automl.cpython-312.pyc
│  │          model_ensemble.cpython-312.pyc
│  │          model_tuning.cpython-312.pyc
│  │
│  └─__pycache__
│          main.cpython-312.pyc
│          main_stand.cpython-312.pyc
│
└─__MACOSX
    │  ._model_automl_with_auto_dt.py
    │  ._pyproject.toml
    │  ._README.md
    │  ._requirements.txt
    │  ._TimeSeriesFactor.py
    │  ._uv.lock
    │
    └─projects
        │  ._.DS_Store
        │  ._catboost_info
        │  ._config.yaml
        │  ._dimension_reduction.py
        │  ._evaluation_report.csv
        │  ._main_stand.py
        │  ._models
        │  ._predict.py
        │  ._saved_models
        │  ._src
        │  ._test_feature.csv
        │  .___pycache__
        │
        ├─catboost_info
        │  │  ._.DS_Store
        │  │  ._catboost_training.json
        │  │  ._learn
        │  │  ._learn_error.tsv
        │  │  ._test
        │  │  ._time_left.tsv
        │  │  ._tmp
        │  │
        │  └─learn
        │          ._events.out.tfevents
        │
        ├─models
        │      ._ensemble_model.joblib
        │      ._feature_engineering.joblib
        │      ._lightgbm_model.joblib
        │      ._xgboost_model.joblib
        │
        ├─src
        │  │  ._.DS_Store
        │  │  ._cat_search_space.yaml
        │  │  ._config.py
        │  │  ._evaluation.py
        │  │  ._feature_engineering.py
        │  │  ._feature_processor.py
        │  │  ._lgb_search_space.yaml
        │  │  ._model_automl.py
        │  │  ._model_ensemble.py
        │  │  ._model_stacking.py
        │  │  ._model_tuning.py
        │  │  ._xgb_search_space.yaml
        │  │  .___pycache__
        │  │
        │  └─__pycache__
        │          ._config.cpython-312.pyc
        │          ._evaluation.cpython-312.pyc
        │          ._feature_engineering.cpython-312.pyc
        │          ._feature_processor.cpython-312.pyc
        │          ._model.cpython-312.pyc
        │          ._model_automl.cpython-312.pyc
        │          ._model_ensemble.cpython-312.pyc
        │          ._model_tuning.cpython-312.pyc
        │
        └─__pycache__
                ._main.cpython-312.pyc
                ._main_stand.cpython-312.pyc

"""