"""
# 数据配置
data:
  # file_path: "/Users/yuguangdeng/code/competition/projects/dataset/lasso_reduce.csv"
  # file_path: "/Users/yuguangdeng/code/competition/projects/dataset/optimal_model_data.csv"
  file_path: "/Users/andrewsu/Desktop/loan/1207/data/train.csv"
  target_column: 'isDefault'  # null表示最后一列是目标变量
  # target_column: null  # null表示最后一列是目标变量
  random_state: 42

# 特征工程配置
feature_engineering:
  enable: true
  # 分类特征编码配置
  category_encoding:
    enable: true
    method: "label"  # label或onehot
  enhanced_feature_engineering:
    enable: true
    corr_threshold: 0.95
    selection_threshold: 25
    remove_collinearity: true
    use_feature_selection: true

  feature_selection:
    enable: true
    method: "lasso"  # lasso, tree_importance, rfe
    params:
      threshold: 0.01

  # 自动分箱
  binning:
    enable: true
    method: "decision_tree"
    tune_params: true
    n_trials: 1
    woe_encode: true
    params:
      max_depth: 3
      min_samples_leaf: 0.05

# 模型配置
models:
  - name: "xgboost"
    enable: true
    feature_set: "selected"  # 使用经过特征筛选的特征集
    automl:
      enable: false
      n_trials: 1
      search_space_path: "src/xgb_search_space.yaml"
    params:
      learning_rate: 0.02
      n_estimators: 300
      max_depth: 6
      subsample: 0.8
      colsample_bytree: 0.8

  - name: "catboost"
    enable: true
    feature_set: "selected"  # 使用经过特征筛选的特征集
    automl:
      enable: false
      n_trials: 1
      search_space_path: "src/cat_search_space.yaml"
    params:
      learning_rate: 0.02
      n_estimators: 300
      max_depth: 6
      subsample: 0.8
      verbose: false

  - name: "lightgbm"
    enable: true
    feature_set: "original"  # 使用只经过多重共线性处理的特征集
    automl:
      enable: false
      n_trials: 1
      search_space_path: "src/lgb_search_space.yaml"
    params:
      learning_rate: 0.02
      n_estimators: 300
      max_depth: 6
      subsample: 0.8
      colsample_bytree: 0.8
      verbose: -1

# 模型融合配置
ensemble:
  enable: true
  method: "weighted_average"
  params:
    weights: [0.33, 0.33, 0.33]  # 对应models列表中启用的模型权重

# 评估配置
evaluation:
  cv_folds: 2
  metrics: ["auc"]
  random_state: 42
  verbose: true

"""