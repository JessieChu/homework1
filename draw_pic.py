#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 22:15:00 2018

@author: jessiechu
"""

import matplotlib.pyplot as plt
import scipy.stats as stats
import clean_statistic as cs
import numpy as np

# 画图
def draw_numeric(csv_file, numeric_attr):
    for column in numeric_attr:
        print("clean start...")
        values_dropna, values_clean, vc = cs.clean_data(csv_file, column, 0.05)
        print("clean is over")
        loc = 'result_pic/'
        draw_hist(column, vc, loc)
        print("hist is over")
        draw_qq_norm(column, vc, loc)
        print("qq is over")
        draw_box(column, values_clean, loc)

# 绘制盒图
def draw_box(column, values_clean, loc):
    plt.figure(figsize=(5,3))
    fp = {'marker': "x", 'markerfacecolor': 'red', 'markersize': 5, 'linestyle': 'none'}
    plt.title("Box:" + str(column))
    plt.boxplot(values_clean, flierprops=fp)
    plt.savefig(loc+'Box '+column+'.png')
    # plt.show()
    plt.close()
    pass

# 绘制直方图
def draw_hist(column, vc, loc):
    plt.figure(figsize=(5, 3))
    plt.title("Hist:" + str(column))
    plt.hist(vc,color='g',bins=10)
    plt.savefig(loc+'Hist '+column+'.png')
    plt.close()
    pass

# qq图识别是否为正态分布
def draw_qq_norm(column, vc, loc):
    plt.figure(figsize=(5, 3))
    stats.probplot(vc, dist="norm", plot=plt)
    plt.title("Q-Q:" + str(column))
    plt.savefig(loc+'Q-Q '+column+'.png')
    # plt.show()
    plt.close()
    pass

# qq图识别属性间的相关度
def draw_qq_double(csv_file, double_column):
    data = csv_file[list(double_column)].dropna()
    x = data[double_column[0]].values
    y = data[double_column[1]].values

    plt.figure(figsize=(5,3))
    plt.title(double_column[0] + "_" + double_column[1])
    plt.plot(x, y, 'bx')
    plt.savefig('result_pic/duibi/'+double_column[0]+"_"+double_column[1]+'.png')
#    plt.show()
    plt.close()


# 去除缺失值 绘图函数
def complete_dropna(csv_file, column):
    loc = "result_pic/final/1_"
    values_dropna = csv_file[column].dropna().values
    draw_hist(column, values_dropna, loc)
    draw_qq_norm(column, values_dropna, loc)
    draw_box(column, values_dropna, loc)
    pass

# 用最高频率值来填补缺失值 绘图函数
def complete_fre_attr(csv_file, column):
    value_count = csv_file[column].dropna().value_counts()
    max_fre_value = value_count.index[0]
    data = csv_file[column]
    miss_index = data[data.isnull()].index
    complete_data = data.copy()
    for i in miss_index:
        complete_data[i] = max_fre_value

    loc = "result_pic/final/2_"
    draw_hist(column, complete_data, loc)
    draw_qq_norm(column, complete_data, loc)
    draw_box(column, complete_data, loc)

# 通过属性的相关关系来填补缺失值 绘图函数
def complete_rel_attr(csv_file, double_column):
    target_data = csv_file[double_column[0]]
    source_data = csv_file[double_column[1]]
    flag1 = target_data.isnull().values
    flag2 = source_data.isnull().values
    complete_data = target_data.copy()
    for index, value in target_data.iteritems():
        if flag1[index] == True and flag2[index] == False:
            complete_data[index] = 1 - source_data[index]

    values_clean = list(complete_data.dropna().values)

    # 去除频率为1的值
    for value, count in complete_data.value_counts().iteritems():
        if count == 1:
            values_clean.remove(value)

    loc = "result_pic/final/3_"
    draw_hist(double_column[0], values_clean, loc)
    draw_qq_norm(double_column[0], values_clean, loc)
    draw_box(double_column[0], values_clean, loc)

# 通过数据对象之间的相似性来填补缺失值 绘图函数
def complete_smi_attr(csv_file, column, numeric_attr):
    data = csv_file[column].copy()
    for index, value in data.iteritems():
        if value == np.NaN:
            data[index] = data[cs.find_dis_value(csv_file, index, column, numeric_attr)]
    loc = "result_pic/final/4_"
    draw_hist(column, data.dropna().values, loc)
    draw_qq_norm(column, data.dropna().values, loc)
    draw_box(column, data.dropna().values, loc)