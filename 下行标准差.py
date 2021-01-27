# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 14:04:14 2020

@author: Administrator
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
#%%
def get_downside_div(data,period,fixed_return):
    downside = []
    for i in range(period,data.shape[0]):
        df = data['return'].tolist()[i-period:i:]
        diff_sum = 0
        for j in range(len(df)):
            if df[j] < fixed_return:
                diff_sum = diff_sum + (df[j]-fixed_return)**2
        div = math.sqrt(diff_sum/(period-1))
        downside.append(div)
    return downside
#%%
data = pd.read_excel(r'D:\国债期货2.xltm',sheet_name= 1)
#%%
data = data.iloc[1:-2,:]
#%%
data = data.dropna(axis = 1)
data = data.reset_index(drop = True)
#%%
data = data.rename(columns={'收益率':'return'})
#%%
downside = get_downside_div(data,252,0)
#%%
