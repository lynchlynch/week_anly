import os
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

import trans_data as td
import draw_figure as drf

# raw_data_dir = '/Users/pei/pydir/week_anly/weekly_data/'
raw_data_dir = 'D:/pydir/week_anly/weekly_data/'

# result_dir = '/Users/pei/pydir/week_anly/result/'
result_dir = 'D:/pydir/week_anly/result/'

start_date = '2021-02-06'
end_date = '2021-02-19'

#delete non-csv file
for single_file in os.listdir(raw_data_dir):
    if single_file.split('.')[1] != 'csv':
        os.remove(raw_data_dir + single_file)

# city_list = ['SHA','BJS','CTU','CAN','WUH']
city_list = ['SHA','BJS','CTU','CAN']
vendor_list = ['03','04']
vendor_list_str = ['CU','DP']

total_power_data_max = pd.read_csv(raw_data_dir + 'total_power_data_max.csv')
total_power_data_avg = pd.read_csv(raw_data_dir + 'total_power_data_avg.csv')
print(total_power_data_max)

#转换源文件格式，以便处理
trans_total_power_data_max,colo_name_list = td.trans_total_power(city_list,vendor_list_str,total_power_data_max)
trans_total_power_data_max.to_csv(result_dir + 'trans_total_max' + '.csv',index=False)

# print(trans_total_power_data_max)

#画errorbar
print('Drawing Errorbar......')
drf.draw_errorbar(trans_total_power_data_max,start_date,end_date,colo_name_list,vendor_list_str,result_dir)

#画箱形图
print('Draw Boxplot......')
drf.draw_box(trans_total_power_data_max,start_date,end_date,colo_name_list,vendor_list_str,result_dir)

#单机柜功率密度图
# print('Draw Boxplot......')
# drf.draw_kde(raw_data_dir,city_list,vendor_list_str)
