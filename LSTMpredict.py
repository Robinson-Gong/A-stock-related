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
tscode = '002739.SZ'

GD = Getdata.getdata(path=path, ds='20120201', de='20200904', tscode=tscode)
df = GD.readdata('k')
data = df.filter(['close'])
dataset = data.values
training_data_len = math.ceil(len(dataset) * 0.8)

scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(dataset)

train_data = scaled_data[0: training_data_len, :]
x_train = []
y_train = []

for i in range(60, len(train_data)):
    x_train.append(train_data[i - 60:i, 0])
    y_train.append(train_data[i, 0])

x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

model = Sequential()

model.add(LSTM(100, return_sequences=True, input_shape=(x_train.shape[1], 1)))
model.add(LSTM(100, return_sequences=False))
model.add(Dense(50))
model.add(Dense(1))

model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(x_train, y_train, batch_size=1, epochs=5)

test_data = scaled_data[training_data_len - 60:, :]
x_test = []
y_test = dataset[training_data_len:, :]
for i in range(60, len(test_data)):
    x_test.append(test_data[i - 60:i, 0])

x_test = np.array(x_test)
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

prediction = model.predict(x_test)
prediction = scaler.inverse_transform(prediction)
rmse = np.sqrt(np.mean(prediction - y_test) ** 2)

train = data[: training_data_len]
valid = data[training_data_len:]
valid['Prediction'] = prediction
plt.figure(figsize=(16, 8))
plt.title('Model')
plt.xlabel('date')
plt.ylabel('close price(RMB)')
plt.plot(train['close'])
plt.plot(valid[['close', 'Prediction']])
plt.legend(['Train', 'Val', 'Prediction'], loc='upper right')
plt.show()

if rmse < 0.008 * np.mean(dataset):
    model.save(tscode + '_' + 'LSTMmodel.h5')
    print(rmse)
    valid.to_csv('F:\stock data\predict.csv')
