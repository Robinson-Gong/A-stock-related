# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 09:36:11 2020

@author: 
"""

from WindPy import *
import pandas as pd
import numpy as np

w.start()
import datetime as dt

'''
到期收益率违约
'''
# 这个是用来看行业利差的变动情况
import matplotlib.pyplot as plt

df = pd.read_excel(r'C:\Users\Administrator\Desktop\data\债券\20违约债券\20违约债券.xlsx')
fifteen_bp = []
twenty_bp = []
thirty_bp = []
fifteen_bp_breach = []
twenty_bp_breach = []
thirty_bp_breach = []
for i in range(df.shape[0]):
    bond_code = df.iloc[i, 0]
    bond_name = df.iloc[i, 1]
    # 给出剩余期限序列
    remain_maturity = w.wsd(bond_code, "ptmyear", "2017-10-12", "2020-11-10", usedf=True)[1]
    trade_date = remain_maturity.index.tolist()
    # 给出基准收益率
    benchmark_profit = []
    base_ytm_list = []
    for i in range(len(remain_maturity)):
        date = remain_maturity.index.tolist()[i]
        str_date = date.strftime('%Y%m%d')
        ptm_year = remain_maturity["PTMYEAR"].iloc[i]
        #
        base_ytm = \
            w.wss(bond_code, "calc_chinabond", "balanceDate=" + str_date + ";term=" + str(ptm_year), usedf=True)[
                1].iloc[0, 0]
        #
        base_ytm_list.append(base_ytm)
    # 给出债券的中债估值收益率
    bond_ytm = np.array(
        w.wsd(bond_code, "yield_cnbd", "2017-10-12", "2020-11-10", "credibility=1", usedf=True)[1]["YIELD_CNBD"])
    base_ytm_array = np.array(base_ytm_list)
    credit_spread_matrix = pd.DataFrame({"债券到期收益率": bond_ytm, "基准到期收益率": base_ytm_array}, index=trade_date)
    credit_spread_matrix = credit_spread_matrix.dropna()
    credit_spread = credit_spread_matrix.iloc[:, 0] - credit_spread_matrix.iloc[:, 1]
    # 给出债券在不同时间点上的对应曲线代码
    corr_code = w.wsd(bond_code, "YCCode", "2020-10-13", "2020-11-11", "agency=1")
    filepath = r'C:\Users\Administrator\Desktop\data\债券\30违约债券\\' + bond_name + '.xlsx'
    credit_spread_matrix.to_excel(filepath, index=False)
    for i in range(credit_spread_matrix.shape[0]-126,credit_spread_matrix.shape[0]):
        if credit_spread[i]-credit_spread[i-1] >= 0.3:
            fifteen_bp_breach.append(bond_name)
            twenty_bp_breach.append(bond_name)
            thirty_bp_breach.append(bond_name)
        elif 20<=credit_spread[i]-credit_spread[i-1] <0.3:
            fifteen_bp_breach.append(bond_name)
            twenty_bp_breach.append(bond_name)
        elif 15<=credit_spread[i]-credit_spread[i-1] <0.2:
            fifteen_bp_breach.append(bond_name)
    for i in range(0,credit_spread_matrix.shape[0]-126):
        if credit_spread[i+1]-credit_spread[i] >= 0.3:
            fifteen_bp.append(bond_name)
            twenty_bp.append(bond_name)
            thirty_bp.append(bond_name)
        elif 20<=credit_spread[i+1]-credit_spread[i] <0.3:
            fifteen_bp.append(bond_name)
            twenty_bp.append(bond_name)
        elif 15<=credit_spread[i+1]-credit_spread[i] <0.2:
            fifteen_bp.append(bond_name)
    #
    # 对信用利差进行可视化
    plt.plot(credit_spread_matrix.index.tolist()[:-1], credit_spread[:-1])
    plt.plot(credit_spread_matrix.index.tolist()[:-1], credit_spread_matrix["债券到期收益率"].tolist()[:-1])
    plt.plot(credit_spread_matrix.index.tolist()[:-1], credit_spread_matrix["基准到期收益率"].tolist()[:-1])
    plt.legend(["credit spread", "bond_ytm", "benchmark_ytm"])
    plt.xticks(rotation=90)
    plt.xlabel("date")
    plt.ylabel("credit spread")
    plt.title(bond_code)
    plt.savefig(r'C:\Users\Administrator\Desktop\data\债券\30违约债券\\' + bond_name + '.jpeg')
