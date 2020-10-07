import tushare as ts
import pandas as pd
import time
import os
import numpy as np
import matplotlib.pyplot as plt
import Getdata
import datetime


path = 'F:\stock data'
tscode = '000100.SZ'
ds = '20200201'
de = '20200930'


asset = 'E'
format = 'margin'
GD = Getdata.getdata(ds = ds,de = de,tscode = tscode,path = path, asset = asset)
GD.getmargindata()
GD.getkdata()
dataframe = GD.readdata(format)

plt.subplot(3,2,1)
dataframe['rzye'] = dataframe['rzye'].astype(float)
plt.plot( dataframe['rzye'] , 'r',  dataframe['rzrqye'], 'k')


plt.subplot(3,2,3)
plt. plot(dataframe['rqye'], 'b')

format = 'k'
dataframe = GD.readdata(format)
plt.subplot(3,2,5)
plt.plot(dataframe['close'], 'k', dataframe['open'], 'r', dataframe['high'], 'b')



tscode = 'SZSE'
format = 'margin'
asset = 'I'
GD = Getdata.getdata(ds = ds,de = de,tscode = tscode,path = path, asset = asset)
dataframe = GD.readdata(format)

plt.subplot(3,2,2)
dataframe['rzye'] = dataframe['rzye'].astype(float)
plt.plot(dataframe['rzye'] , 'r',  dataframe['rzrqye'], 'k')


plt.subplot(3,2,4)
plt. plot( dataframe['rqye'], 'b')

format = 'k'
dataframe = GD.readdata(format)
plt.subplot(3,2,6)
plt.plot( dataframe['close'], 'k', dataframe['open'], 'r', dataframe['high'], 'b')
plt.show()
