#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 22:37:01 2018

@author: jessiechu
"""

import pandas as pd
import itertools
import draw_pic
import clean_statistic as cs
from multiprocessing import Process

# 读取csv文件
def load_file(file):
    csv_file = pd.read_csv(file, low_memory=False)
    return csv_file


if __name__ == "__main__":
     homework_file2 = r"/Users/jessiechu/Documents/文档/DMPro/hw1/Data/NFL Play by Play 2009-2017 (v4).csv/NFL Play by Play 2009-2017 (v4).csv"

     csv_file2 = load_file(homework_file2)

#     人工选取若干数值属性
     numeric_attr2 =['Drive','qtr	down','TimeUnder','TimeSecs	','PlayTimeDiff','yrdln','yrdline100','ydstogo','ydsnet','Yards.Gained','	AirYards','YardsAfterCatch','FieldGoalDistance','Penalty.Yards','PosTeamScore','DefTeamScore','ScoreDiff','AbsScoreDiff','posteam_timeouts_pre','HomeTimeouts_Remaining_Pre','AwayTimeouts_Remaining_Pre','HomeTimeouts_Remaining_Post','AwayTimeouts_Remaining_Post','No_Score_Prob','Opp_Field_Goal_Prob','Opp_Safety_Prob','Opp_Touchdown_Prob','Field_Goal_Prob','Safety_Prob','Touchdown_Prob','ExPoint_Prob','TwoPoint_Prob','ExpPts','EPA','airEPA','yacEPA','Home_WP_pre','Away_WP_pre','Home_WP_post','Away_WP_post','Win_Prob',	'WPA	airWPA','yacWPA']
#     numeric_attr2 = ['Away_WP_pre', 'FieldGoalDistance', 'Field_Goal_Prob', 'Home_WP_pre', 'Opp_Field_Goal_Prob', 'Touchdown_Prob', 'yrdline100', 'yrdln']
     cs.nominal_statistic(csv_file2, numeric_attr2, "NFL Play by Play 2009-2017 (v4)")
     cs.numeric_statistic(csv_file2, numeric_attr2, "NFL Play by Play 2009-2017 (v4)")
     draw_pic.draw_numeric(csv_file2, numeric_attr2)

#     多线程
     def child(csv_file, column):
         draw_pic.draw_numeric(csv_file, [column])
    
    
     childs = []
     for column in numeric_attr2:
         p = Process(target=child, args=(csv_file2, column))
         p.start()
         childs.append(p)
    
     for child_p in childs:
         child_p.join()

     for double_column in itertools.combinations(numeric_attr2, 2):
         draw_pic.draw_qq_double(csv_file2, double_column)

#     只展示Home_WP_pre属性填补后的效果
     draw_pic.complete_dropna(csv_file2, 'Home_WP_pre')
     draw_pic.complete_fre_attr(csv_file2, 'Home_WP_pre')
     draw_pic.complete_rel_attr(csv_file2, ['Home_WP_pre', 'Away_WP_pre'])
     draw_pic.complete_smi_attr(csv_file2, 'Away_WP_pre', numeric_attr2)
