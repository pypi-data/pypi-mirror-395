"""
# 1. 数据准备

## 1.1 特征工程

关注 TimeSeriesFactor.py 文件，该文件包含了时间序列因子的生成代码。详细用法说明如下：
参数：
input_path: 银行流水数据文件路径
output_path: 时序流水因子输出文件路径
id_col = 'id': ID列列名，默认为'id'
time_col = 'time': 时间列列名，默认为'time'
direction_col = 'direction': 方向列列名，默认为'direction'
amount_col = 'amount': 金额列列名，默认为'amount'



## 2. 模型训练

默认配置文件在 projects/config.yaml 中, 需要关注数据集的路径，以及相关功能开关。

执行代码如下：

```
cd projects
python main_stand.py
```

## 3. 模型预测

test_feature.csv 是预测数据，需要放在 projects 目录下。 需要和训练数据的特征列名保持一致。
```
python3 predict.py
```

"""