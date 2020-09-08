import math
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
import numpy as np
import pandas as pd
import Getdata
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from keras.models import load_model



path = 'F:\stock data'
tscode = '002602.SZ'

GD = Getdata.getdata(path=path, ds='20120201', de='20200908', tscode=tscode)
GD.getkdata()
df_k = GD.readdata('k')
df_basic = GD.readdata('basic')
df_merge = pd.merge(df_k, df_basic, on='trade_date')

data = df_merge.iloc[30:, [5, 8, 9, 10, 11, 13, 15, 17, 21, 22, 23, 24, 25, 26, 27, 28]]
data['hilochg'] = (df_k.iloc[30:, 3] - df_k.iloc[30:, 4]) / df_k.iloc[30:, 5]
data['ts_fls_ratio'] = df_merge.iloc[30:, 32] / df_merge.iloc[30:, 31]
data['ts_fs_ratio'] = df_merge.iloc[30:, 33] / df_merge.iloc[30:, 31]
data['fls_fs_ratio'] = df_merge.iloc[30:, 33] / df_merge.iloc[30:, 32]
data['cmv_tmv_ratio'] = df_merge.iloc[30:, 35]/df_merge.iloc[30:, 34]

model = load_model(tscode + '_'+'LSTMmodel.h5')
last_60_days = data[-60:].values
scaler = MinMaxScaler(feature_range=(0, 1))
last_60_days_scaled = scaler.fit_transform(last_60_days)
x_test = [last_60_days_scaled]
x_test = np.array(x_test)
scaler2 = MinMaxScaler(feature_range=(0, 1))
df = data.iloc[-60:, 0].values.reshape(-1, 1)
scale_data2 = scaler2.fit_transform(df)
pred_price = model.predict(x_test)
pred_price = scaler2.inverse_transform(pred_price)
print(pred_price)
