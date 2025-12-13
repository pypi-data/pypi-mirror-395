import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from tqdm import tqdm


def main(input_path,output_path,id_col = 'id',time_col = 'time',direction_col = 'direction',amount_col = 'amount'):
    # 设置文件路径
    bank_stmt_path = input_path
    factors_output_path = output_path

    # 读取数据
    print("正在读取数据...")
    bank_stmt = pd.read_csv(bank_stmt_path)
    bank_stmt = bank_stmt.rename(columns={id_col:'id',time_col:'time',direction_col:'direction',amount_col:'amount'})
    # 数据预处理
    print("\n正在预处理数据...")
    # 将时间戳转换为日期格式
    bank_stmt['time'] = pd.to_datetime(bank_stmt['time'], unit='s')

    # 计算每个ID的最近交易日期
    def get_latest_transaction_date(df):
        return df.groupby('id')['time'].max().reset_index(name='latest_date')

    latest_dates = get_latest_transaction_date(bank_stmt)
    bank_stmt = bank_stmt.merge(latest_dates, on='id', how='left')

    # 计算每个交易距离最近交易日期的天数
    bank_stmt['days_from_latest'] = (bank_stmt['latest_date'] - bank_stmt['time']).dt.days

    # 生成所有因子的主函数
    def generate_all_factors(df):
        factors = pd.DataFrame()
        factors['id'] = df['id'].unique()
        
        # 遍历每个ID，计算各个因子
        for index, row in tqdm(factors.iterrows(),total = len(factors)):
            id_ = row['id']
            id_data = df[df['id'] == id_].copy()
            
            # ========== 原始11因子 ==========
            # 因子1：近3个月流水波动率（标准差/均值）
            recent_3m = id_data[id_data['days_from_latest'] <= 90]
            if len(recent_3m) > 0:
                factor1 = recent_3m['amount'].std() / recent_3m['amount'].mean() if recent_3m['amount'].mean() != 0 else 0
            else:
                factor1 = 0
            factors.loc[index, 'factor1_3m_volatility'] = factor1
            
            # 因子2：近6个月流水波动率（标准差/均值）
            recent_6m = id_data[id_data['days_from_latest'] <= 180]
            if len(recent_6m) > 0:
                factor2 = recent_6m['amount'].std() / recent_6m['amount'].mean() if recent_6m['amount'].mean() != 0 else 0
            else:
                factor2 = 0
            factors.loc[index, 'factor2_6m_volatility'] = factor2
            
            # 因子3：3个月波动率比（因子1/因子2）
            factor3 = factor1 / factor2 if factor2 != 0 else 0
            factors.loc[index, 'factor3_volatility_ratio'] = factor3
            
            # 因子4：近1个月净流入（direction=0为流入，direction=1为流出）
            recent_1m = id_data[id_data['days_from_latest'] <= 30]
            inflow_1m = recent_1m[recent_1m['direction'] == 0]['amount'].sum()
            outflow_1m = recent_1m[recent_1m['direction'] == 1]['amount'].sum()
            factor4 = inflow_1m - outflow_1m
            factors.loc[index, 'factor4_1m_net_inflow'] = factor4
            
            # 因子5：近1个月净流出
            factor5 = outflow_1m - inflow_1m if outflow_1m > inflow_1m else 0
            factors.loc[index, 'factor5_1m_net_outflow'] = factor5
            
            # 因子6：近3个月净流入
            recent_3m = id_data[id_data['days_from_latest'] <= 90]
            inflow_3m = recent_3m[recent_3m['direction'] == 0]['amount'].sum()
            outflow_3m = recent_3m[recent_3m['direction'] == 1]['amount'].sum()
            factor6 = inflow_3m - outflow_3m
            factors.loc[index, 'factor6_3m_net_inflow'] = factor6
            
            # 因子7：近3个月净流出
            factor7 = outflow_3m - inflow_3m if outflow_3m > inflow_3m else 0
            factors.loc[index, 'factor7_3m_net_outflow'] = factor7
            
            # 因子8：近1个月净流入/近3个月净流入
            factor8 = factor4 / factor6 if factor6 != 0 else 0
            factors.loc[index, 'factor8_inflow_ratio'] = factor8
            
            # 因子9：近1个月净流出/近3个月净流出    
            factor9 = factor5 / factor7 if factor7 != 0 else 0
            factors.loc[index, 'factor9_outflow_ratio'] = factor9
            
            # 因子10：剔除10元以下交易后，（近6个月第三高流水金额 - 近6个月第三低流水金额）/近6个月平均流水金额
            recent_6m = id_data[id_data['days_from_latest'] <= 180]
            recent_6m_above_10 = recent_6m[recent_6m['amount'] >= 10]
            if len(recent_6m_above_10) >= 3:
                sorted_amounts = recent_6m_above_10['amount'].sort_values()
                third_low = sorted_amounts.iloc[2] if len(sorted_amounts) >= 3 else 0
                third_high = sorted_amounts.iloc[-3] if len(sorted_amounts) >= 3 else 0
                mean_amount = recent_6m_above_10['amount'].mean()
                factor10 = (third_high - third_low) / mean_amount if mean_amount != 0 else 0
            else:
                factor10 = 0
            factors.loc[index, 'factor10_range_ratio'] = factor10
            
            # 因子11：近1个月平均流水数额/近1年平均流水数额
            recent_1m = id_data[id_data['days_from_latest'] <= 30]
            recent_12m = id_data[id_data['days_from_latest'] <= 365]
            mean_1m = recent_1m['amount'].mean() if len(recent_1m) > 0 else 0
            mean_12m = recent_12m['amount'].mean() if len(recent_12m) > 0 else 0
            factor11 = mean_1m / mean_12m if mean_12m != 0 else 0
            factors.loc[index, 'factor11_recent_avg_ratio'] = factor11
            
            # 因子12：近7天交易次数
            recent_7d = id_data[id_data['days_from_latest'] <= 7]
            factors.loc[index, 'factor12_7d_txn_count'] = len(recent_7d)
            
            # 因子13：近30天交易次数
            recent_30d = id_data[id_data['days_from_latest'] <= 30]
            factors.loc[index, 'factor13_30d_txn_count'] = len(recent_30d)
            
            # 因子14：近90天交易次数
            recent_90d = id_data[id_data['days_from_latest'] <= 90]
            factors.loc[index, 'factor14_90d_txn_count'] = len(recent_90d)
            
            # 因子15：近7天交易频率（次数/天数）
            days_in_7d = len(recent_7d['time'].dt.date.unique()) if len(recent_7d) > 0 else 1
            factors.loc[index, 'factor15_7d_txn_freq'] = len(recent_7d) / days_in_7d
            
            # 因子16：近30天交易频率（次数/天数）
            days_in_30d = len(recent_30d['time'].dt.date.unique()) if len(recent_30d) > 0 else 1
            factors.loc[index, 'factor16_30d_txn_freq'] = len(recent_30d) / days_in_30d
            
            # 因子17：近90天交易频率（次数/天数）
            days_in_90d = len(recent_90d['time'].dt.date.unique()) if len(recent_90d) > 0 else 1
            factors.loc[index, 'factor17_90d_txn_freq'] = len(recent_90d) / days_in_90d
            
            # 因子18：（近30天交易次数 - 近90天交易次数）/近90天交易次数
            total_90d = len(recent_90d)
            if total_90d > 0:
                factors.loc[index, 'factor18_txn_count_ratio'] = (len(recent_30d) - total_90d) / total_90d
            else:
                factors.loc[index, 'factor18_txn_count_ratio'] = 0

            # 因子19：近3个月流水中位数
            recent_3m = id_data[id_data['days_from_latest'] <= 90]
            if len(recent_3m) > 0:
                factors.loc[index, 'factor19_3m_median'] = recent_3m['amount'].median()
            else:
                factors.loc[index, 'factor19_3m_median'] = 0
            
            # 因子20：近6个月流水中位数
            recent_6m = id_data[id_data['days_from_latest'] <= 180]
            if len(recent_6m) > 0:
                factors.loc[index, 'factor20_6m_median'] = recent_6m['amount'].median()
            else:
                factors.loc[index, 'factor20_6m_median'] = 0
            
            # 因子21：近3个月流水四分位距（Q3-Q1）
            if len(recent_3m) > 0:
                q1 = recent_3m['amount'].quantile(0.25)
                q3 = recent_3m['amount'].quantile(0.75)
                factors.loc[index, 'factor21_3m_iqr'] = q3 - q1
            else:
                factors.loc[index, 'factor21_3m_iqr'] = 0
            
            # 因子22：近6个月流水四分位距（Q3-Q1）
            if len(recent_6m) > 0:
                q1 = recent_6m['amount'].quantile(0.25)
                q3 = recent_6m['amount'].quantile(0.75)
                factors.loc[index, 'factor22_6m_iqr'] = q3 - q1
            else:
                factors.loc[index, 'factor22_6m_iqr'] = 0
            
            # 因子23：近3个月大额交易（>1000元）占比
            if len(recent_3m) > 0:
                large_txns = recent_3m[recent_3m['amount'] > 1000]
                factors.loc[index, 'factor23_3m_large_txn_ratio'] = len(large_txns) / len(recent_3m)
            else:
                factors.loc[index, 'factor23_3m_large_txn_ratio'] = 0
            
            # 因子24：近6个月小额交易（<100元）占比
            if len(recent_6m) > 0:
                small_txns = recent_6m[recent_6m['amount'] < 100]
                factors.loc[index, 'factor24_6m_small_txn_ratio'] = len(small_txns) / len(recent_6m)
            else:
                factors.loc[index, 'factor24_6m_small_txn_ratio'] = 0
            
            # 因子25：近3个月流水偏度
            if len(recent_3m) > 0:
                factors.loc[index, 'factor25_3m_skewness'] = recent_3m['amount'].skew()
            else:
                factors.loc[index, 'factor25_3m_skewness'] = 0
            
            # 因子26：近6个月流水峰度
            if len(recent_6m) > 0:
                factors.loc[index, 'factor26_6m_kurtosis'] = recent_6m['amount'].kurtosis()
            else:
                factors.loc[index, 'factor26_6m_kurtosis'] = 0
            
            # 因子27：近3个月收入交易占比（流入交易次数/总交易次数）
            if len(recent_3m) > 0:
                income_txns = recent_3m[recent_3m['direction'] == 0]
                factors.loc[index, 'factor27_3m_income_ratio'] = len(income_txns) / len(recent_3m)
            else:
                factors.loc[index, 'factor27_3m_income_ratio'] = 0
            
            # 因子28：近6个月收入交易占比
            if len(recent_6m) > 0:
                income_txns = recent_6m[recent_6m['direction'] == 0]
                factors.loc[index, 'factor28_6m_income_ratio'] = len(income_txns) / len(recent_6m)
            else:
                factors.loc[index, 'factor28_6m_income_ratio'] = 0
            
            # 因子29：近3个月平均收入金额
            if len(recent_3m) > 0:
                income_txns = recent_3m[recent_3m['direction'] == 0]
                if len(income_txns) > 0:
                    factors.loc[index, 'factor29_3m_avg_income'] = income_txns['amount'].mean()
                else:
                    factors.loc[index, 'factor29_3m_avg_income'] = 0
            else:
                factors.loc[index, 'factor29_3m_avg_income'] = 0
            
            # 因子30：近3个月平均支出金额
            if len(recent_3m) > 0:
                expense_txns = recent_3m[recent_3m['direction'] == 1]
                if len(expense_txns) > 0:
                    factors.loc[index, 'factor30_3m_avg_expense'] = expense_txns['amount'].mean()
                else:
                    factors.loc[index, 'factor30_3m_avg_expense'] = 0
            else:
                factors.loc[index, 'factor30_3m_avg_expense'] = 0
            
            # 因子33：近3个月收入/支出金额比
            if len(recent_3m) > 0:
                income = recent_3m[recent_3m['direction'] == 0]['amount'].sum()
                expense = recent_3m[recent_3m['direction'] == 1]['amount'].sum()
                if expense > 0:
                    factors.loc[index, 'factor33_3m_income_expense_ratio'] = income / expense
                else:
                    factors.loc[index, 'factor33_3m_income_expense_ratio'] = 0
            else:
                factors.loc[index, 'factor33_3m_income_expense_ratio'] = 0
            
            # 因子34：近6个月收入/支出金额比
            if len(recent_6m) > 0:
                income = recent_6m[recent_6m['direction'] == 0]['amount'].sum()
                expense = recent_6m[recent_6m['direction'] == 1]['amount'].sum()
                if expense > 0:
                    factors.loc[index, 'factor34_6m_income_expense_ratio'] = income / expense
                else:
                    factors.loc[index, 'factor34_6m_income_expense_ratio'] = 0
            else:
                factors.loc[index, 'factor34_6m_income_expense_ratio'] = 0
            
            # 趋势与稳定性相关因子
            # 因子35：近3个月流水环比增长率（与前3个月相比）
            recent_3m = id_data[(id_data['days_from_latest'] > 90) & (id_data['days_from_latest'] <= 180)]
            prev_3m = id_data[(id_data['days_from_latest'] > 180) & (id_data['days_from_latest'] <= 270)]
            recent_3m_sum = recent_3m['amount'].sum()
            prev_3m_sum = prev_3m['amount'].sum()
            if prev_3m_sum > 0:
                factors.loc[index, 'factor35_3m_mom'] = (recent_3m_sum - prev_3m_sum) / prev_3m_sum
            else:
                factors.loc[index, 'factor35_3m_mom'] = 0
            
            # 因子36：近6个月流水环比增长率（与前6个月相比）
            recent_6m = id_data[(id_data['days_from_latest'] > 180) & (id_data['days_from_latest'] <= 360)]
            prev_6m = id_data[(id_data['days_from_latest'] > 360) & (id_data['days_from_latest'] <= 540)]
            recent_6m_sum = recent_6m['amount'].sum()
            prev_6m_sum = prev_6m['amount'].sum()
            if prev_6m_sum > 0:
                factors.loc[index, 'factor36_6m_mom'] = (recent_6m_sum - prev_6m_sum) / prev_6m_sum
            else:
                factors.loc[index, 'factor36_6m_mom'] = 0
            
            # 因子39：近12个月流水的线性增长斜率
            recent_12m = id_data[id_data['days_from_latest'] <= 365]
            if len(recent_12m) > 0:
                # 按月份分组，计算每月流水
                recent_12m['month'] = recent_12m['time'].dt.to_period('M')
                monthly_sum = recent_12m.groupby('month')['amount'].sum().reset_index()
                if len(monthly_sum) >= 2:
                    # 计算线性回归斜率
                    X = np.arange(len(monthly_sum)).reshape(-1, 1)
                    y = monthly_sum['amount'].values
                    slope = np.polyfit(X.flatten(), y, 1)[0]
                    factors.loc[index, 'factor39_12m_trend_slope'] = slope
                else:
                    factors.loc[index, 'factor39_12m_trend_slope'] = 0
            else:
                factors.loc[index, 'factor39_12m_trend_slope'] = 0
            
            # 因子40：近12个月流水的R²（拟合优度）
            recent_12m = id_data[id_data['days_from_latest'] <= 365]
            if len(recent_12m) > 0:
                recent_12m['month'] = recent_12m['time'].dt.to_period('M')
                monthly_sum = recent_12m.groupby('month')['amount'].sum().reset_index()
                if len(monthly_sum) >= 2:
                    X = np.arange(len(monthly_sum)).reshape(-1, 1)
                    y = monthly_sum['amount'].values
                    # 计算R²
                    slope, intercept = np.polyfit(X.flatten(), y, 1)
                    y_pred = slope * X.flatten() + intercept
                    ss_res = np.sum((y - y_pred) ** 2)
                    ss_tot = np.sum((y - np.mean(y)) ** 2)
                    r2 = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
                    factors.loc[index, 'factor40_12m_trend_r2'] = r2
                else:
                    factors.loc[index, 'factor40_12m_trend_r2'] = 0
            else:
                factors.loc[index, 'factor40_12m_trend_r2'] = 0
            
            # 异常交易相关因子
            # 因子43：近3个月最大单笔交易金额
            recent_3m = id_data[id_data['days_from_latest'] <= 90]
            if len(recent_3m) > 0:
                factors.loc[index, 'factor43_3m_max_txn_amount'] = recent_3m['amount'].max()
            else:
                factors.loc[index, 'factor43_3m_max_txn_amount'] = 0
            
            # 因子44：近6个月最大单笔交易金额
            recent_6m = id_data[id_data['days_from_latest'] <= 180]
            if len(recent_6m) > 0:
                factors.loc[index, 'factor44_6m_max_txn_amount'] = recent_6m['amount'].max()
            else:
                factors.loc[index, 'factor44_6m_max_txn_amount'] = 0
            
            # 因子47：近3个月连续交易天数
            recent_3m = id_data[id_data['days_from_latest'] <= 90]
            if len(recent_3m) > 0:
                # 获取所有交易日期
                txn_dates = sorted(recent_3m['time'].dt.date.unique())
                max_consecutive = 1
                current_consecutive = 1
                for i in range(1, len(txn_dates)):
                    if (txn_dates[i] - txn_dates[i-1]).days == 1:
                        current_consecutive += 1
                        max_consecutive = max(max_consecutive, current_consecutive)
                    else:
                        current_consecutive = 1
                factors.loc[index, 'factor47_3m_consecutive_days'] = max_consecutive
            else:
                factors.loc[index, 'factor47_3m_consecutive_days'] = 0
            
            # 因子48：近6个月连续交易天数
            recent_6m = id_data[id_data['days_from_latest'] <= 180]
            if len(recent_6m) > 0:
                txn_dates = sorted(recent_6m['time'].dt.date.unique())
                max_consecutive = 1
                current_consecutive = 1
                for i in range(1, len(txn_dates)):
                    if (txn_dates[i] - txn_dates[i-1]).days == 1:
                        current_consecutive += 1
                        max_consecutive = max(max_consecutive, current_consecutive)
                    else:
                        current_consecutive = 1
                factors.loc[index, 'factor48_6m_consecutive_days'] = max_consecutive
            else:
                factors.loc[index, 'factor48_6m_consecutive_days'] = 0
            
            # 时间模式相关因子
            # 因子51：近3个月工作日交易占比
            recent_3m = id_data[id_data['days_from_latest'] <= 90]
            if len(recent_3m) > 0:
                weekday_txns = recent_3m[recent_3m['time'].dt.weekday < 5]
                factors.loc[index, 'factor51_3m_weekday_ratio'] = len(weekday_txns) / len(recent_3m)
            else:
                factors.loc[index, 'factor51_3m_weekday_ratio'] = 0
            
            # 因子52：近6个月工作日交易占比
            recent_6m = id_data[id_data['days_from_latest'] <= 180]
            if len(recent_6m) > 0:
                weekday_txns = recent_6m[recent_6m['time'].dt.weekday < 5]
                factors.loc[index, 'factor52_6m_weekday_ratio'] = len(weekday_txns) / len(recent_6m)
            else:
                factors.loc[index, 'factor52_6m_weekday_ratio'] = 0
            
            # 因子53：近3个月周末交易占比
            recent_3m = id_data[id_data['days_from_latest'] <= 90]
            if len(recent_3m) > 0:
                weekend_txns = recent_3m[recent_3m['time'].dt.weekday >= 5]
                factors.loc[index, 'factor53_3m_weekend_ratio'] = len(weekend_txns) / len(recent_3m)
            else:
                factors.loc[index, 'factor53_3m_weekend_ratio'] = 0
            
            # 因子54：近6个月周末交易占比
            recent_6m = id_data[id_data['days_from_latest'] <= 180]
            if len(recent_6m) > 0:
                weekend_txns = recent_6m[recent_6m['time'].dt.weekday >= 5]
                factors.loc[index, 'factor54_6m_weekend_ratio'] = len(weekend_txns) / len(recent_6m)
            else:
                factors.loc[index, 'factor54_6m_weekend_ratio'] = 0
            
            # 因子55：近3个月白天（9:00-18:00）交易占比
            recent_3m = id_data[id_data['days_from_latest'] <= 90]
            if len(recent_3m) > 0:
                daytime_txns = recent_3m[(recent_3m['time'].dt.hour >= 9) & (recent_3m['time'].dt.hour < 18)]
                factors.loc[index, 'factor55_3m_daytime_ratio'] = len(daytime_txns) / len(recent_3m)
            else:
                factors.loc[index, 'factor55_3m_daytime_ratio'] = 0
            
            # 因子56：近6个月白天（9:00-18:00）交易占比
            recent_6m = id_data[id_data['days_from_latest'] <= 180]
            if len(recent_6m) > 0:
                daytime_txns = recent_6m[(recent_6m['time'].dt.hour >= 9) & (recent_6m['time'].dt.hour < 18)]
                factors.loc[index, 'factor56_6m_daytime_ratio'] = len(daytime_txns) / len(recent_6m)
            else:
                factors.loc[index, 'factor56_6m_daytime_ratio'] = 0
            
            # 因子57：近3个月夜间（18:00-次日9:00）交易占比
            recent_3m = id_data[id_data['days_from_latest'] <= 90]
            if len(recent_3m) > 0:
                night_txns = recent_3m[(recent_3m['time'].dt.hour < 9) | (recent_3m['time'].dt.hour >= 18)]
                factors.loc[index, 'factor57_3m_night_ratio'] = len(night_txns) / len(recent_3m)
            else:
                factors.loc[index, 'factor57_3m_night_ratio'] = 0
            
            # 因子58：近6个月夜间（18:00-次日9:00）交易占比
            recent_6m = id_data[id_data['days_from_latest'] <= 180]
            if len(recent_6m) > 0:
                night_txns = recent_6m[(recent_6m['time'].dt.hour < 9) | (recent_6m['time'].dt.hour >= 18)]
                factors.loc[index, 'factor58_6m_night_ratio'] = len(night_txns) / len(recent_6m)
            else:
                factors.loc[index, 'factor58_6m_night_ratio'] = 0
            
            # ========== 20个新颖流水因子 ==========
            # 因子59：交易周期稳定性：近3个月交易周期稳定性（连续交易间隔的变异系数）
            recent_3m = id_data[id_data['days_from_latest'] <= 90]
            if len(recent_3m) >= 2:
                txn_dates = sorted(recent_3m['time'].dt.date.unique())
                intervals = [(txn_dates[i] - txn_dates[i-1]).days for i in range(1, len(txn_dates))]
                if len(intervals) >= 2:
                    mean_interval = np.mean(intervals)
                    std_interval = np.std(intervals)
                    factors.loc[index, 'factor59_transaction_cycle_stability'] = std_interval / mean_interval if mean_interval > 0 else 0
                else:
                    factors.loc[index, 'factor59_transaction_cycle_stability'] = 0
            else:
                factors.loc[index, 'factor59_transaction_cycle_stability'] = 0
            
            # 因子60：收入金额集中度：近3个月收入金额集中度（基尼系数）
            recent_3m = id_data[id_data['days_from_latest'] <= 90]
            income_txns = recent_3m[recent_3m['direction'] == 0]
            if len(income_txns) >= 2:
                amounts = income_txns['amount'].values
                amounts_sorted = np.sort(amounts)
                n = len(amounts_sorted)
                index = np.arange(1, n + 1)
                gini = (2 * np.sum(index * amounts_sorted) / (n * np.sum(amounts_sorted))) - (n + 1) / n
                factors.loc[index, 'factor60_income_amount_concentration'] = gini
            else:
                factors.loc[index, 'factor60_income_amount_concentration'] = 0
            
            # 因子61：支出金额集中度：近3个月支出金额集中度（基尼系数）
            expense_txns = recent_3m[recent_3m['direction'] == 1]
            if len(expense_txns) >= 2:
                amounts = expense_txns['amount'].values
                amounts_sorted = np.sort(amounts)
                n = len(amounts_sorted)
                index = np.arange(1, n + 1)
                gini = (2 * np.sum(index * amounts_sorted) / (n * np.sum(amounts_sorted))) - (n + 1) / n
                factors.loc[index, 'factor61_expense_amount_concentration'] = gini
            else:
                factors.loc[index, 'factor61_expense_amount_concentration'] = 0
            
            # 因子62：收入频率一致性：近3个月收入频率一致性（周收入次数的变异系数）
            recent_3m = id_data[id_data['days_from_latest'] <= 90]
            income_txns = recent_3m[recent_3m['direction'] == 0].copy()  # 添加.copy()避免SettingWithCopyWarning
            if len(income_txns) >= 2:
                income_txns['week'] = income_txns['time'].dt.isocalendar().week
                weekly_counts = income_txns.groupby('week')['amount'].count().values
                if len(weekly_counts) >= 2:
                    mean_count = np.mean(weekly_counts)
                    std_count = np.std(weekly_counts)
                    factors.loc[index, 'factor62_income_freq_consistency'] = std_count / mean_count if mean_count > 0 else 0
                else:
                    factors.loc[index, 'factor62_income_freq_consistency'] = 0
            else:
                factors.loc[index, 'factor62_income_freq_consistency'] = 0
            
            # 因子63：支出频率一致性：近3个月支出频率一致性（周支出次数的变异系数）
            expense_txns = recent_3m[recent_3m['direction'] == 1].copy()  # 添加.copy()避免SettingWithCopyWarning
            if len(expense_txns) >= 2:
                expense_txns['week'] = expense_txns['time'].dt.isocalendar().week
                weekly_counts = expense_txns.groupby('week')['amount'].count().values
                if len(weekly_counts) >= 2:
                    mean_count = np.mean(weekly_counts)
                    std_count = np.std(weekly_counts)
                    factors.loc[index, 'factor63_expense_freq_consistency'] = std_count / mean_count if mean_count > 0 else 0
                else:
                    factors.loc[index, 'factor63_expense_freq_consistency'] = 0
            else:
                factors.loc[index, 'factor63_expense_freq_consistency'] = 0
            
            # 因子64：周末收入/支出金额比：近3个月周末收入/支出金额比
            recent_3m = id_data[id_data['days_from_latest'] <= 90]
            weekend_txns = recent_3m[recent_3m['time'].dt.weekday >= 5]
            weekend_income = weekend_txns[weekend_txns['direction'] == 0]['amount'].sum()
            weekend_expense = weekend_txns[weekend_txns['direction'] == 1]['amount'].sum()
            factors.loc[index, 'factor64_weekend_income_expense_ratio'] = weekend_income / weekend_expense if weekend_expense > 0 else 0
            
            # 因子65：工作日收入/支出金额比：近3个月工作日收入/支出金额比
            workday_txns = recent_3m[recent_3m['time'].dt.weekday < 5]
            workday_income = workday_txns[workday_txns['direction'] == 0]['amount'].sum()
            workday_expense = workday_txns[workday_txns['direction'] == 1]['amount'].sum()
            factors.loc[index, 'factor65_workday_income_expense_ratio'] = workday_income / workday_expense if workday_expense > 0 else 0
            
            # 因子66：夜间大额交易占比：近3个月夜间（18:00-次日9:00）大额交易占比
            recent_3m = id_data[id_data['days_from_latest'] <= 90]
            night_txns = recent_3m[(recent_3m['time'].dt.hour < 9) | (recent_3m['time'].dt.hour >= 18)]
            if len(night_txns) > 0:
                night_large_txns = night_txns[night_txns['amount'] > 1000]
                factors.loc[index, 'factor66_night_large_txn_ratio'] = len(night_large_txns) / len(night_txns)
            else:
                factors.loc[index, 'factor66_night_large_txn_ratio'] = 0
            
            # 因子67：白天小额交易占比：近3个月白天（9:00-18:00）小额交易占比
            daytime_txns = recent_3m[(recent_3m['time'].dt.hour >= 9) & (recent_3m['time'].dt.hour < 18)]
            if len(daytime_txns) > 0:
                daytime_small_txns = daytime_txns[daytime_txns['amount'] < 100]
                factors.loc[index, 'factor67_daytime_small_txn_ratio'] = len(daytime_small_txns) / len(daytime_txns)
            else:
                factors.loc[index, 'factor67_daytime_small_txn_ratio'] = 0
            
            # 因子68：连续收入增长天数：近3个月连续收入增长天数
            recent_3m = id_data[id_data['days_from_latest'] <= 90]
            income_txns = recent_3m[recent_3m['direction'] == 0]
            if len(income_txns) >= 2:
                # 按天汇总收入
                daily_income = income_txns.groupby(income_txns['time'].dt.date)['amount'].sum().reset_index(name='daily_sum')
                daily_income = daily_income.sort_values(by='time')
                # 计算连续增长天数
                max_consecutive = 1
                current_consecutive = 1
                for i in range(1, len(daily_income)):
                    if daily_income['daily_sum'].iloc[i] > daily_income['daily_sum'].iloc[i-1]:
                        current_consecutive += 1
                        max_consecutive = max(max_consecutive, current_consecutive)
                    else:
                        current_consecutive = 1
                factors.loc[index, 'factor68_consecutive_increase_days'] = max_consecutive
            else:
                factors.loc[index, 'factor68_consecutive_increase_days'] = 0
            
            # 因子69：连续收入下降天数：近3个月连续收入下降天数
            if len(income_txns) >= 2:
                # 按天汇总收入
                daily_income = income_txns.groupby(income_txns['time'].dt.date)['amount'].sum().reset_index(name='daily_sum')
                daily_income = daily_income.sort_values(by='time')
                # 计算连续下降天数
                max_consecutive = 1
                current_consecutive = 1
                for i in range(1, len(daily_income)):
                    if daily_income['daily_sum'].iloc[i] < daily_income['daily_sum'].iloc[i-1]:
                        current_consecutive += 1
                        max_consecutive = max(max_consecutive, current_consecutive)
                    else:
                        current_consecutive = 1
                factors.loc[index, 'factor69_consecutive_decrease_days'] = max_consecutive
            else:
                factors.loc[index, 'factor69_consecutive_decrease_days'] = 0
            
            # 因子70：平均交易间隔：近6个月平均交易间隔天数
            recent_6m = id_data[id_data['days_from_latest'] <= 180]
            if len(recent_6m) >= 2:
                txn_dates = sorted(recent_6m['time'].dt.date.unique())
                intervals = [(txn_dates[i] - txn_dates[i-1]).days for i in range(1, len(txn_dates))]
                factors.loc[index, 'factor70_avg_transaction_gap'] = np.mean(intervals) if intervals else 0
            else:
                factors.loc[index, 'factor70_avg_transaction_gap'] = 0
            
            # 因子71：交易间隔变化趋势：近6个月交易间隔变化趋势（斜率）
            if len(recent_6m) >= 2:
                txn_dates = sorted(recent_6m['time'].dt.date.unique())
                intervals = [(txn_dates[i] - txn_dates[i-1]).days for i in range(1, len(txn_dates))]
                if len(intervals) >= 2:
                    X = np.arange(len(intervals)).reshape(-1, 1)
                    y = np.array(intervals)
                    slope = np.polyfit(X.flatten(), y, 1)[0]
                    factors.loc[index, 'factor71_transaction_gap_trend'] = slope
                else:
                    factors.loc[index, 'factor71_transaction_gap_trend'] = 0
            else:
                factors.loc[index, 'factor71_transaction_gap_trend'] = 0
            
            # 因子72：节假日交易占比：近3个月节假日交易占比（简化实现，使用周末替代节假日）
            recent_3m = id_data[id_data['days_from_latest'] <= 90]
            if len(recent_3m) > 0:
                # 简化实现：将周末视为节假日
                holiday_txns = recent_3m[recent_3m['time'].dt.weekday >= 5]
                factors.loc[index, 'factor72_holiday_transaction_ratio'] = len(holiday_txns) / len(recent_3m)
            else:
                factors.loc[index, 'factor72_holiday_transaction_ratio'] = 0
            
            # 因子73：高峰期交易占比：近3个月高峰期（10:00-11:00, 15:00-16:00）交易占比
            recent_3m = id_data[id_data['days_from_latest'] <= 90]
            if len(recent_3m) > 0:
                peak_txns = recent_3m[((recent_3m['time'].dt.hour == 10) & (recent_3m['time'].dt.minute >= 0)) | \
                                    ((recent_3m['time'].dt.hour == 15) & (recent_3m['time'].dt.minute >= 0))]
                factors.loc[index, 'factor73_peak_hour_transaction_ratio'] = len(peak_txns) / len(recent_3m)
            else:
                factors.loc[index, 'factor73_peak_hour_transaction_ratio'] = 0
            
            # 因子74：连续大额交易天数：近3个月连续有大额交易的天数
            recent_3m = id_data[id_data['days_from_latest'] <= 90]
            if len(recent_3m) > 0:
                # 按天检查是否有大额交易
                daily_has_large_txn = recent_3m[recent_3m['amount'] > 1000].groupby(recent_3m['time'].dt.date).size().reset_index(name='count')
                large_txn_dates = sorted(daily_has_large_txn['time'].unique())
                # 计算连续天数
                max_consecutive = 1
                current_consecutive = 1
                for i in range(1, len(large_txn_dates)):
                    if (large_txn_dates[i] - large_txn_dates[i-1]).days == 1:
                        current_consecutive += 1
                        max_consecutive = max(max_consecutive, current_consecutive)
                    else:
                        current_consecutive = 1
                factors.loc[index, 'factor74_large_txn_consecutive_days'] = max_consecutive
            else:
                factors.loc[index, 'factor74_large_txn_consecutive_days'] = 0
            
            # 因子75：连续小额交易天数：近3个月连续有小额交易的天数
            recent_3m = id_data[id_data['days_from_latest'] <= 90]
            if len(recent_3m) > 0:
                # 按天检查是否有小额交易
                daily_has_small_txn = recent_3m[recent_3m['amount'] < 100].groupby(recent_3m['time'].dt.date).size().reset_index(name='count')
                small_txn_dates = sorted(daily_has_small_txn['time'].unique())
                # 计算连续天数
                max_consecutive = 1
                current_consecutive = 1
                for i in range(1, len(small_txn_dates)):
                    if (small_txn_dates[i] - small_txn_dates[i-1]).days == 1:
                        current_consecutive += 1
                        max_consecutive = max(max_consecutive, current_consecutive)
                    else:
                        current_consecutive = 1
                factors.loc[index, 'factor75_small_txn_consecutive_days'] = max_consecutive
            else:
                factors.loc[index, 'factor75_small_txn_consecutive_days'] = 0
            
            # 因子76：收入波动率比：近3个月收入波动率/近6个月收入波动率
            recent_3m_income = id_data[(id_data['days_from_latest'] <= 90) & (id_data['direction'] == 0)]
            recent_6m_income = id_data[(id_data['days_from_latest'] <= 180) & (id_data['direction'] == 0)]
            if len(recent_3m_income) >= 2 and len(recent_6m_income) >= 2:
                vol_3m = recent_3m_income['amount'].std() / recent_3m_income['amount'].mean() if recent_3m_income['amount'].mean() > 0 else 0
                vol_6m = recent_6m_income['amount'].std() / recent_6m_income['amount'].mean() if recent_6m_income['amount'].mean() > 0 else 0
                factors.loc[index, 'factor76_income_volatility_ratio'] = vol_3m / vol_6m if vol_6m > 0 else 0
            else:
                factors.loc[index, 'factor76_income_volatility_ratio'] = 0
            
            # 因子77：支出波动率比：近3个月支出波动率/近6个月支出波动率
            recent_3m_expense = id_data[(id_data['days_from_latest'] <= 90) & (id_data['direction'] == 1)]
            recent_6m_expense = id_data[(id_data['days_from_latest'] <= 180) & (id_data['direction'] == 1)]
            if len(recent_3m_expense) >= 2 and len(recent_6m_expense) >= 2:
                vol_3m = recent_3m_expense['amount'].std() / recent_3m_expense['amount'].mean() if recent_3m_expense['amount'].mean() > 0 else 0
                vol_6m = recent_6m_expense['amount'].std() / recent_6m_expense['amount'].mean() if recent_6m_expense['amount'].mean() > 0 else 0
                factors.loc[index, 'factor77_expense_volatility_ratio'] = vol_3m / vol_6m if vol_6m > 0 else 0
            else:
                factors.loc[index, 'factor77_expense_volatility_ratio'] = 0
            
            # 因子78：交易金额信息熵：近3个月交易金额的信息熵
            recent_3m = id_data[id_data['days_from_latest'] <= 90]
            if len(recent_3m) >= 2:
                # 将交易金额分为10个区间
                amounts = recent_3m['amount'].values
                bins = np.histogram_bin_edges(amounts, bins=10)
                counts, _ = np.histogram(amounts, bins=bins)
                # 计算概率分布
                probs = counts / counts.sum()
                # 计算信息熵
                probs = probs[probs > 0]  # 过滤掉概率为0的区间
                entropy = -np.sum(probs * np.log2(probs))
                factors.loc[index, 'factor78_transaction_amount_entropy'] = entropy
            else:
                factors.loc[index, 'factor78_transaction_amount_entropy'] = 0
        return factors

    # 生成所有因子
    print("\n正在生成所有因子...")
    all_combined_factors = generate_all_factors(bank_stmt)

    print(f"\n生成的所有因子数据形状: {all_combined_factors.shape}")
    print(f"生成的因子数量: {len(all_combined_factors.columns) - 1}")
    print(f"生成的因子列表: {all_combined_factors.columns.tolist()[1:]}")

    # 保存所有因子数据
    print("\n正在保存所有因子数据...")
    all_combined_factors.to_csv(factors_output_path, index=False)
    print(f"所有因子数据已保存到: {factors_output_path}")


    # 输出因子的基本统计信息
    print("\n因子的基本统计信息:")
    for col in all_combined_factors.columns[1:]:  # 跳过id列
        print(f"\n{col}:")
        print(all_combined_factors[col].describe())

    print("\n所有因子生成和整合完成！")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Generate time series factors')
    parser.add_argument('--input_path', type=str, required=True, help='Path to input bank statement CSV file')
    parser.add_argument('--output_path', type=str, required=True, help='Path to output factors CSV file')
    parser.add_argument('--id_col', type=str, required=False, help='ID列列名')
    parser.add_argument('--time_col', type=str, required=False, help='时间列(time)列名')
    parser.add_argument('--direction_col', type=str, required=False, help='交易方向列(direction)列名')
    parser.add_argument('--amount_col', type=str, required=False, help='交易金额列(amount)列名')
    args = parser.parse_args()
    main(args.input_path, args.output_path, args.id_col, args.time_col, args.direction_col, args.amount_col)