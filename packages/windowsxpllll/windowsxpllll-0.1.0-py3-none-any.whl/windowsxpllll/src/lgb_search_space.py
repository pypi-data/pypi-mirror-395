"""
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