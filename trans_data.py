import pandas as pd
import os
import numpy as np

import gen_cololist
#转换总的用电数据
def trans_total_power(city_list,vendor_list_str,total_power_data_max):
    colo_name_list = []
    trans_total_power_data_max = pd.DataFrame([])
    vendor_list = gen_cololist.gen_cololist(vendor_list_str)
    for signle_city in city_list:
        for single_vendor in vendor_list:
            colo_name = signle_city + '.' + single_vendor
            # 遍历，然后选择有数据的站点
            if len(total_power_data_max[total_power_data_max['Series'].str.contains(colo_name)]) != 0:
                colo_name_list.append(colo_name)
                trans_total_power_data_max[colo_name] = \
                total_power_data_max[total_power_data_max['Series'].str.contains(colo_name)]['Value'].tolist()

    date_list = total_power_data_max[total_power_data_max['Series'].str.contains('BJS.03')]['key'].tolist()
    trans_total_power_data_max.insert(0, 'date', date_list)

    return trans_total_power_data_max,colo_name_list

def trans_per_cab_power(raw_data_dir,selected_colo_name,start_date,end_date):
    utility_rate_per_site = []
    file_list = os.listdir(raw_data_dir)
    power_limit_data = pd.read_csv(raw_data_dir + 'power_limit.csv')
    selected_colo_file = selected_colo_name + '_power_data_max.csv'
    for single_file in file_list:
        if single_file == selected_colo_file:
            per_colo_power_data = pd.read_csv(raw_data_dir + selected_colo_file)
            cab_list = list(set(per_colo_power_data['Series'].tolist()))
            cab_num = len(cab_list)
            cab_power_unit = \
                power_limit_data[power_limit_data['site'] == selected_colo_name]['power_limit'].tolist()[0]#单机柜额定功率
            for single_cab in cab_list:
                # print(single_cab)
                # print('-----------------------------------------------')
                selected_per_cab_data = per_colo_power_data[per_colo_power_data['Series'] == single_cab]
                # print(selected_per_cab_data)
                start_index = selected_per_cab_data[selected_per_cab_data['Key'] == start_date].index.tolist()[0]
                end_index = selected_per_cab_data[selected_per_cab_data['Key'] == end_date].index.tolist()[0]
                # print(selected_per_cab_data['Value'].tolist()[start_index:end_index+1])
                power_utility_per_cab = \
                    list(np.array(per_colo_power_data['Value'].tolist()[start_index:end_index+1]) / cab_power_unit)
                # 将这些每天的数据的list提取出来，单独存，方便过后处理
                for single_data in power_utility_per_cab:
                    utility_rate_per_site.append(single_data)
            break
    return utility_rate_per_site