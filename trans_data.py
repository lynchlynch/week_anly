import pandas as pd

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