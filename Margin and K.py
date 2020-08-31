import tushare as ts
import pandas as pd
import time
import os
import numpy as np
import matplotlib.pyplot as plt
import Getdata

def readdata(path, tscode, format):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        print('file does not exist')
    else:
        csv_filepath = path + '\\' + tscode + '\\'+ tscode + '_' + format +'.csv'
        csv_data = pd.read_csv(csv_filepath)
        return csv_data





path = 'F:\stock data\\'
tscode = '002602.SZ'
ds = '20200201'
de = '20200828'
GD = Getdata.getdata(ds = ds,de = de,tscode = tscode,path = path)
GD.getmargindata()
GD.getkdata()

format = 'margin'
dataframe = readdata(path, tscode, format)
temp = dataframe.columns

plt.subplot(3,2,1)
dataframe['rzye'] = dataframe['rzye'].astype(float)
plt.plot(dataframe['trade_date'], dataframe['rzye'] , 'r', dataframe['trade_date'], dataframe['rzrqye'], 'k')


plt.subplot(3,2,3)
plt. plot(dataframe['trade_date'], dataframe['rqye'], 'b')

format = 'k'
dataframe = readdata(path, tscode, format)
plt.subplot(3,2,5)
plt.plot(dataframe['trade_date'], dataframe['close'], 'k', dataframe['trade_date'], dataframe['open'], 'r', dataframe['trade_date'], dataframe['high'], 'b')

tscode = 'SZSE'
format = 'margin'
dataframe = readdata(path, tscode, format)

plt.subplot(3,2,2)
dataframe['rzye'] = dataframe['rzye'].astype(float)
plt.plot(dataframe['trade_date'], dataframe['rzye'] , 'r', dataframe['trade_date'], dataframe['rzrqye'], 'k')


plt.subplot(3,2,4)
plt. plot(dataframe['trade_date'], dataframe['rqye'], 'b')

format = 'k'
dataframe = readdata(path, tscode, format)
plt.subplot(3,2,6)
plt.plot(dataframe['trade_date'], dataframe['close'], 'k', dataframe['trade_date'], dataframe['open'], 'r', dataframe['trade_date'], dataframe['high'], 'b')
plt.show()

