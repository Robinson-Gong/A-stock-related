import tushare as ts
import pandas as pd
import time
import os
import numpy as np
import matplotlib.pyplot as plt
import Getdata
import datetime


path = 'F:\stock data'
tscode = '002602.SZ'
ds = '20200801'
de = '20200902'


asset = 'E'
format = 'margin'
GD = Getdata.getdata(ds = ds,de = de,tscode = tscode,path = path, asset = asset)
GD.getmargindata()
GD.getkdata()
dataframe = GD.readdata(format)

plt.subplot(3,2,1)
dataframe['rzye'] = dataframe['rzye'].astype(float)
plt.plot(dataframe['trade_date'], dataframe['rzye'] , 'r', dataframe['trade_date'], dataframe['rzrqye'], 'k')


plt.subplot(3,2,3)
plt. plot(dataframe['trade_date'], dataframe['rqye'], 'b')

format = 'k'
dataframe = GD.readdata(format)
plt.subplot(3,2,5)
plt.plot(dataframe['trade_date'], dataframe['close'], 'k', dataframe['trade_date'], dataframe['open'], 'r', dataframe['trade_date'], dataframe['high'], 'b')



tscode = 'SZSE'
format = 'margin'
asset = 'I'
dataframe = GD.readdata(format)

plt.subplot(3,2,2)
dataframe['rzye'] = dataframe['rzye'].astype(float)
plt.plot(dataframe['trade_date'], dataframe['rzye'] , 'r', dataframe['trade_date'], dataframe['rzrqye'], 'k')


plt.subplot(3,2,4)
plt. plot(dataframe['trade_date'], dataframe['rqye'], 'b')

format = 'k'
dataframe = GD.readdata(format)
plt.subplot(3,2,6)
plt.plot(dataframe['trade_date'], dataframe['close'], 'k', dataframe['trade_date'], dataframe['open'], 'r', dataframe['trade_date'], dataframe['high'], 'b')
plt.show()
