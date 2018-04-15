#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: jessiechu
"""

import pandas as pd
import itertools
import draw_pic
import clean_statistic as cs

# 读取csv文件
def load_file(file):
    csv_file = pd.read_csv(file, low_memory=False)
    return csv_file


if __name__ == "__main__":
    homework_file1 = r"/Users/jessiechu/Documents/文档/DMPro/hw1/Data/Building_Permits.csv"

    # 人工选择所有数值属性
    numeric_attr1 = ['Number of Existing Stories', 'Number of Proposed Stories', 'Estimated Cost', 'Revised Cost',
                    'Existing Units', 'Proposed Units']
    csv_file1 = load_file(homework_file1)
    
    cs.nominal_statistic(csv_file1, numeric_attr1, "Building_Permits")
    cs.numeric_statistic(csv_file1, numeric_attr1, "Building_Permits")
    draw_pic.draw_numeric(csv_file1, numeric_attr1)

    # 绘制两个属性的qq图，并进行对比
    for double_column in itertools.combinations(numeric_attr1, 2):
        draw_pic.draw_qq_comparion(csv_file1, double_column)

    # 以Estimated Cost属性填补为例
    draw_pic.final_dropna(csv_file1, 'Estimated Cost')
    draw_pic.final_fre_attr(csv_file1, 'Estimated Cost')
    draw_pic.final_rel_attr(csv_file1, ['Estimated Cost', 'Revised Cost'])
    draw_pic.final_smi_attr(csv_file1, 'Estimated Cost', numeric_attr1)
