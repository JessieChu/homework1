#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 19:02:33 2018

@author: jessiechu
"""

import json
import copy

# 标称属性统计
def nominal_statistic(csv_file, numeric_attr, name):
    res_dict = {}
    for column in csv_file.columns:
        if column not in numeric_attr:
            res_dict[column] = csv_file[column].value_counts().to_dict()
    json.dump(str(res_dict), open(r'result/'+name+'_nominal_attr.json', 'w', encoding='utf-8'))

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
    json.dump(res_dict, open('result/'+name+'_numeric_attr.json', 'w', encoding='utf-8'))

# 数据清洗
def clean_data(csv_file, column, percent):
    # 去除缺失值
    values_dropna = csv_file[column].dropna().values
    values_count = csv_file[column].dropna().value_counts()
    values_clean = list(values_dropna)

    # 去除频率为1的值
    # for value, count in values_count.iteritems():
    #     if count == 1:
    #         values_clean.remove(value)

    # 为加快速度，对所有取值种类的频数-1，近似等效于去除频率为1的值
    for item in values_count.index:
        values_clean.remove(item)

    values_clean.sort()
    len = values_clean.__len__()

    # 按percent比例截尾
    vc = values_clean[int(len * percent):int(len * (1 - percent))]

    return values_dropna, values_clean, vc

