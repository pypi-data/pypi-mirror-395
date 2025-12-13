"""
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