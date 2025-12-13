"""
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