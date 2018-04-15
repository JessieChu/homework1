#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: jessiechu
"""

import json
import copy
import numpy as np

# 标称属性统计
def nominal_statistic(csv_file, numeric_attr, name):
    res_dict = {}
    for column in csv_file.columns:
        if column not in numeric_attr:
            res_dict[column] = csv_file[column].value_counts().to_dict()
    json.dump(str(res_dict), open(r'results/'+name+'_nominal.json', 'w', encoding='utf-8'))

# 数值属性统计
def numeric_statistic(csv_file, numeric_attr, name):
    res_dict = {}
    for column in numeric_attr:
        column_series = copy.copy(csv_file[column])
        clean_series = column_series.dropna()

        num_of_NaN = column_series.__len__() - clean_series.__len__()

        clean_list = clean_series.values.tolist()

        clean_list.sort()
        len = clean_list.__len__()
        max_value = clean_list[-1]
        min_value = clean_list[0]
        sum_value = sum(clean_list)
        mean_value = sum_value / clean_list.__len__()

        Q1 = clean_list[int((len + 1) * 0.25)]
        Q2 = clean_list[int((len + 1) * 0.5)]
        Q3 = clean_list[int((len + 1) * 0.75)]

        result = [max_value, min_value, mean_value, Q2, [Q1, Q2, Q3], num_of_NaN]
        res_dict[column] = result
    json.dump(res_dict, open('results/'+name+'_numeric.json', 'w', encoding='utf-8'))
    
# 查找两个对象间相异度最小的 指定的 column值
def find_dis_value(csv_file, pos, column, numeric_attr):

    def dis_objs(tar_obj, sou_obj):
        dis_value = 0
        count = 0
        for column in tar_obj.index:
            if tar_obj[column] != np.NaN and sou_obj[column] != np.NaN:
                if column in numeric_attr:
                        values_sort = csv_file[column].dropna().values.sort()
                        denominator = values_sort[-1] - values_sort[0]
                        dis_value += abs(tar_obj[column] - sou_obj[column])/denominator
                        count += 1

                elif tar_obj[column] == sou_obj[column]:
                    dis_value += 1
                count += 1
            else:
                continue
        return dis_value/count

    mindis = 9999
    result_pos = -1
    target_obj = csv_file.ix[pos]
    for index in csv_file.index:
        if index == pos:
            continue
        source_obj = csv_file.ix(index)
        tmp = dis_objs(target_obj, source_obj)
        if tmp < mindis:
            result_pos = index
    return result_pos
# 数据清洗
def clean_data(csv_file, column, percent):
    # 去除缺失值
    values_dropna = csv_file[column].dropna().values
    values_count = csv_file[column].dropna().value_counts()
    values_clean = list(values_dropna)

    # 去除频率为1的值,对所有取值种类的频数-1
    for item in values_count.index:
        values_clean.remove(item)

    values_clean.sort()
    len = values_clean.__len__()

    # 按percent比例截尾
    vc = values_clean[int(len * percent):int(len * (1 - percent))]

    return values_dropna, values_clean, vc

