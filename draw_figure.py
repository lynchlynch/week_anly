#画整个站点总耗电量的errorbar，15天平均，std为15天内的std，值为当天的数值
#该图可以看具体哪天的波动情况，从而找出有可能的问题值
import numpy as np
import math
import matplotlib.pyplot as plt
import pandas as pd
import os

import gen_cololist
import trans_data as td

def draw_errorbar(trans_total_power_data_max,start_date,end_date,colo_name_list,vendor_list_str,result_dir):
    #首先生成colo_name_list
    vendor_list = gen_cololist.gen_cololist(vendor_list_str)
    start_index = trans_total_power_data_max[trans_total_power_data_max['date'] == start_date].index.tolist()[0]
    end_index = trans_total_power_data_max[trans_total_power_data_max['date'] == end_date].index.tolist()[0]

    for single_vendor in vendor_list:
        plt.figure()
        plt.style.use('dark_background')
        for single_colo in colo_name_list:
            # print(single_colo)
            std_list = []
            if single_vendor in single_colo:
                single_total_power_max = trans_total_power_data_max[single_colo].tolist()
                for processing_index in range(start_index,end_index+1):
                    single_std = np.std(single_total_power_max[processing_index-14:processing_index+1])
                    std_list.append(single_std)
            else:
                continue

            errorbar_x = range(end_index-start_index+1)
            errorbar_y = list(np.array(single_total_power_max[start_index:end_index+1])/1000)
            errorbar_yerr = list(np.array(std_list)/math.sqrt(1000))
            # print(errorbar_y)
            # print(errorbar_yerr)
            # print('***********************************************')
            plt.errorbar(errorbar_x,errorbar_y,yerr=errorbar_yerr,label = single_colo,fmt='o:')
            plt.ylim(6,20)
        plt.legend(bbox_to_anchor=(1.25, 1))
        plt.xticks(errorbar_x,trans_total_power_data_max['date'].tolist()[start_index:end_index+1],rotation=45)
        plt.title(vendor_list_str[vendor_list.index(single_vendor)] + ' Power Consumption',style='italic')
        plt.savefig(result_dir + vendor_list_str[vendor_list.index(single_vendor)] +
                    '_power_consumption.png',bbox_inches='tight')

def draw_box(trans_total_power_data_max,start_date,end_date,colo_name_list,vendor_list_str,result_dir):
    start_index = trans_total_power_data_max[trans_total_power_data_max['date'] == start_date].index.tolist()[0]
    end_index = trans_total_power_data_max[trans_total_power_data_max['date'] == end_date].index.tolist()[0]

    outlier_num = 3#显示前3大的异常值
    #生成新的站点名称，方便阅读
    orgin_columns = trans_total_power_data_max.columns.tolist()[1:]
    new_columns = []
    for single_columns in orgin_columns:
        vendor = single_columns.split('.')[1]
        if vendor == '01':
            new_columns.append(single_columns.split('.')[0] + '_CT')
        elif vendor == '02':
            new_columns.append(single_columns.split('.')[0] + '_CM')
        elif vendor == '03':
            new_columns.append(single_columns.split('.')[0] + '_CU')
        else:
            if single_columns.split('.')[0] == 'CTU':
                new_columns.append('GDS')
            elif single_columns.split('.')[0] == 'TNJ':
                new_columns.append('Telstra')
            else:
                new_columns.append(single_columns.split('.')[0] + '_DP')

    pure_total_power_slice = trans_total_power_data_max.iloc[start_index:end_index + 1, :]
    pure_total_power = pure_total_power_slice.drop('date',axis=1,inplace=False)
    pure_total_power = pd.DataFrame(np.array(pure_total_power)/1000,columns=new_columns)
    plt.style.use('dark_background')
    box_figure = pure_total_power.plot.box(title='Total Power Data',return_type='dict')
    #检测异常值
    x_outlier_list = []
    y_outlier_list = []
    for index in range(len(new_columns)):
        if len(box_figure['fliers'][index].get_ydata()) > 0 :
            for single_filier_index in range(len(box_figure['fliers'][index].get_ydata())):
                x_outlier_list.append(box_figure['fliers'][index].get_xdata()[single_filier_index])
                y_outlier_list.append(box_figure['fliers'][index].get_ydata()[single_filier_index])

    outlier_df = pd.DataFrame(x_outlier_list, columns=['x_outlier'])
    outlier_df['y_outlier'] = y_outlier_list
    outlier_df_sort = outlier_df.sort_values(by='y_outlier',ascending=False)
    outlier_df_sort = outlier_df_sort.reset_index()
    if len(outlier_df_sort) == 0:
        plt.savefig(result_dir + 'Total_Power_Data_Box.png')
    elif len(outlier_df_sort) >0 and len(outlier_df_sort) < 3:
        draw_box_annote(len(outlier_df_sort),outlier_df_sort,new_columns,pure_total_power,pure_total_power_slice)
        plt.savefig(result_dir + 'Total_Power_Data_Box.png')
    else:
        draw_box_annote(outlier_num, outlier_df_sort, new_columns, pure_total_power, pure_total_power_slice)
        plt.savefig(result_dir + 'Total_Power_Data_Box.png')

#标记箱形图的异常点
def draw_box_annote(outlier_num,outlier_df_sort,new_columns,pure_total_power,pure_total_power_slice):
    for index in range(outlier_num):
        single_x_outlier = outlier_df_sort['x_outlier'].tolist()[index]
        single_y_outlier = outlier_df_sort['y_outlier'].tolist()[index]
        single_column_in_pure = new_columns[int(single_x_outlier) - 1]
        index_in_slice = \
        pure_total_power[pure_total_power[new_columns[int(single_x_outlier) - 1]] == single_y_outlier].index.tolist()[0]
        annocate_date = pure_total_power_slice['date'].tolist()[index_in_slice]
        annotate_note = str(annocate_date) + ',' + str(single_y_outlier)
        # print(max(pure_total_power))
        if single_y_outlier == np.array(pure_total_power).min() or single_y_outlier == np.array(pure_total_power).max():
            plt.annotate(annotate_note, xy=(single_x_outlier, single_y_outlier),
                         xytext=(single_x_outlier + 0.3, single_y_outlier), xycoords='data',
                         arrowprops=dict(facecolor='red', shrink=0.05))
        else:
            plt.annotate(annotate_note, xy=(single_x_outlier, single_y_outlier),
                         xytext=(single_x_outlier + 0.3, single_y_outlier + 0.5 * (-1) ** index), xycoords='data',
                         arrowprops=dict(facecolor='red', shrink=0.05))

def draw_kde(raw_data_dir,result_dir,city_list,vendor_list_str,start_date,end_date):
    #按不同的运营商画图
    for single_vendor in vendor_list_str:
        # print('---------------'+single_vendor+'--------------------')
        plt.figure()
        plt.style.use('dark_background')
        utility_rate_per_vendor = []
        weigh_list = [10,20,30,40,50,60,70,80,90,100]
        weigh_rate = [0 for index in range(len(weigh_list))]
        for single_city in city_list:
            selected_colo_name = single_city + '_' + single_vendor
            if os.path.exists(raw_data_dir + selected_colo_name + '_power_data_max.csv'):
                utility_rate_per_site = td.trans_per_cab_power(raw_data_dir,selected_colo_name,start_date,end_date)
                #将utility_rate_per_vendor转为一维，方便处理
                for single_data in utility_rate_per_site:
                    utility_rate_per_vendor.append(single_data)
            else:
                continue

        #计算每个利用率下的比例
        for index in range(len(weigh_list)):
            single_weigh = weigh_list[index]
            # print('-----------------')
            # print(single_weigh)
            # print(list(np.array(utility_rate_per_vendor)*100))
            cpr_list = list(np.array(utility_rate_per_vendor)*100 - single_weigh)
            selected_cpr_list = [i for i in cpr_list if i > 0 and i < 10]
            weigh_rate[index] = len(selected_cpr_list)/len(utility_rate_per_vendor) * 100
        # print(weigh_list)
        # print(weigh_rate)
        # print(utility_rate_per_vendor)
        # print(list(np.array(utility_rate_per_vendor)*100))
        plt.bar(weigh_list,weigh_rate,width=5)
        plt.xlabel('Power Utility Rate(%)')
        plt.ylabel('proportion(%)')
        plt.xticks(weigh_list,weigh_list)
        plt.savefig(result_dir + single_vendor + '_Power_Rate.png')