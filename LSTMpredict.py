import math
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
import numpy as np
import pandas as pd
import Getdata
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf

plt.style.use('fivethirtyeight')

path = 'F:\stock data'
tscode = '002602.SZ'

GD = Getdata.getdata(path=path, ds='20120201', de='20200907', tscode=tscode)
GD.getkdata()
GD.getbasicdata()
df_k = GD.readdata('k')
df_basic = GD.readdata('basic')
df_merge = pd.merge(df_k, df_basic, on='trade_date')

data = df_merge.iloc[30:, [5, 8, 9, 10, 11, 13, 15, 17, 21, 22, 23, 24, 25, 26, 27, 28]]
data['hilochg'] = (df_k.iloc[30:, 3] - df_k.iloc[30:, 4]) / df_k.iloc[30:, 5]
data['ts_fls_ratio'] = df_merge.iloc[30:, 32] / df_merge.iloc[30:, 31]
data['ts_fs_ratio'] = df_merge.iloc[30:, 33] / df_merge.iloc[30:, 31]
data['fls_fs_ratio'] = df_merge.iloc[30:, 33] / df_merge.iloc[30:, 32]
data['cmv_tmv_ratio'] = df_merge.iloc[30:, 35]/df_merge.iloc[30:, 34]
dataset = data.values
training_data_len = math.ceil(len(dataset) * 0.8)

scaler = MinMaxScaler(feature_range=(0, 1))
scaler2 = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(dataset)
df = data['close_x'].values.reshape(-1, 1)
scale_data2 = scaler2.fit_transform(df)

train_data = scaled_data[0: training_data_len, :]
x_train = []
y_train = []

for i in range(60, len(train_data)):
    x_train.append(train_data[i - 60:i, :])
    y_train.append(train_data[i, 0])

x_train, y_train = np.array(x_train), np.array(y_train)

model = Sequential()

model.add(LSTM(100, return_sequences=True, input_shape=(x_train.shape[1], x_train.shape[2])))
model.add(LSTM(100, return_sequences=False))
model.add(Dense(50))
model.add(Dense(1))

model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(x_train, y_train, batch_size=1, epochs=25)

test_data = scaled_data[training_data_len - 60:, :]
x_test = []
y_test = dataset[training_data_len:, 0]
for i in range(60, len(test_data)):
    x_test.append(test_data[i - 60:i, :])

x_test = np.array(x_test)
print(x_test.shape)

prediction = model.predict(x_test)

prediction = scaler2.inverse_transform(prediction)
rmse = np.sqrt(np.mean(prediction - y_test) ** 2)

train = data[: training_data_len]
valid = data[training_data_len:]
valid['Prediction'] = prediction
plt.figure(figsize=(16, 8))
plt.title('Model')
plt.xlabel('date')
plt.ylabel('close price(RMB)')
plt.plot(train['close_x'])
plt.plot(valid[['close_x', 'Prediction']])
plt.legend(['Train', 'Val', 'Prediction'], loc='upper right')
plt.show()

if rmse < 0.28:
    model.save(tscode + '_' + 'LSTMmodel.h5')
    print(rmse)
valid.to_csv('F:\stock data\predict.csv')
