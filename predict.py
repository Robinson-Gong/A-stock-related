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
tscode = '002739.SZ'

GD = Getdata.getdata(path=path, ds='20120201', de='20200904', tscode=tscode)
df = GD.readdata('k')
data = df.filter(['close'])

model = load_model(tscode + '_'+'LSTMmodel.h5')
last_60_days = data[-60:].values
scaler = MinMaxScaler(feature_range=(0, 1))
last_60_days_scaled = scaler.fit_transform(last_60_days)
x_test = [last_60_days_scaled]
x_test = np.array(x_test)
x_test = np.reshape(x_test,(x_test.shape[0], x_test.shape[1], 1))
pred_price = model.predict(x_test)
pred_price = scaler.inverse_transform(pred_price)
print(pred_price)