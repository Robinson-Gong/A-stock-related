import tushare as ts
import pandas as pd
import time
import os
import numpy as np
import matplotlib.pyplot as plt
import pywt


def getkdatas(datestart, dateend):
    ts.set_token('your token here')
    results1 = ts.pro_bar(ts_code= stockno, adj='qfq', start_date= datestart, end_date= dateend, ma = [3])
    results1.sort_values("trade_date", inplace=True)
    results1[results1['ma3'] == 'nan']
    results1.to_csv(csv_filepath1, index=False, encoding='gbk')
    return 0

def fft_combine(bins, n, loops=1):
    length = int(len(bins) * loops)
    data = np.zeros(length)
    index = loops * np.arange(0, length, 1.0) / length * (2 * np.pi)
    for k, p in enumerate(bins[:n]):
        if k != 0 : p *= 2
        data += np.real(p) * np.cos(k*index)
        data -= np.imag(p) * np.sin(k*index)
    return index, data

def analyze_wavelet(dataform1):
    w = pywt.Wavelet('sym5')

    ts_log = np.log(dataform1["ma3"])
    ts_diff = ts_log.dropna()
    a = ts_diff
    ca = []
    cd = []
    mode = pywt.Modes.smooth
    for i in range(3 ):
        (a, d) = pywt.dwt(a, w, mode)
        ca.append(a)
        cd.append(d)
    rec_a = []
    rec_d = []
    for i, coeff in enumerate(ca):
        coeff_list = [coeff, None] + [None] * i
        rec_a.append(pywt.waverec(coeff_list, w))
    for i, coeff in enumerate(cd):
        coeff_list = [None, coeff] + [None] * i
        rec_d.append(pywt.waverec(coeff_list, w))
    rowstotal = len(rec_a) + 1
    fig = plt.figure()
    ax_main = fig.add_subplot(rowstotal, 1, 1)
    ax_main.plot(dataform1["ma3"])
    ax_main.set_xlim(0, len(ts_diff)  )

    for i, y in enumerate(rec_a):
        ax = fig.add_subplot(rowstotal, 2, 3 + i * 2)
        ax.plot(y, 'r')
        ax.set_xlim(0, len(y)  )
        ax.set_ylabel("A%d" % (i + 1))
    for i, y in enumerate(rec_d):
        ax = fig.add_subplot(rowstotal, 2, 4 + i * 2)
        ax.plot(y, 'g')
        ax.set_xlim(0, len(y)  )
        ax.set_ylabel("D%d" % (i + 1))

    plt.show()
    return 0
def analyze_fft(dataform1):
    print('\n ma3: %s ' % (dataform1.columns.values[7]))

    lines = dataform1.shape[0]
    x = np.random.random(100)
    y = np.fft.fft(x)
    plt.subplot(2, 1, 1)
    # plt.plot(x)
    plt.plot(dataform1["ma3"])
    plt.xlabel('Time'), plt.ylabel('ma3')

    #dft_a = np.fft.fft(dataform1["ma5"])

    plt.subplot(2, 1, 2)
    """
    plt.plot(dft_a)
    #plt.plot(y)
    plt.xlabel('Freq (Hz)'), plt.ylabel(' ')
    plt.show()"""
    ts_log = np.log(dataform1["ma3"])
    #ts_log = dataform1["ma5"]
    #ts_diff = ts_log.diff(1)
    ts_diff = ts_log
    ts_diff = ts_diff.dropna()
    fy = np.fft.fft(ts_diff)
    conv1 = np.real(np.fft.ifft(fy))
    index, conv2 = fft_combine(fy / len(ts_diff), int(len(fy) / 2 - 1), 1.3)
    ntotal = (len(ts_diff)/10 +2)*10

    plt.plot(ts_diff)
    plt.plot(conv1 - 0.5)
    plt.plot(conv2 - 1)
    plt.xticks(np.arange(1, ntotal, 5))
    plt.grid( )
    plt.show()
    return 0

stockno = 'stock code'
csv_filepath1 = 'saving file dic'+ stockno + '_k.csv'
date0 = 'startdate'
date1 = 'enddate'

getkdatas(date0, date1)

df = pd.read_csv(csv_filepath1, encoding='gbk')


df['ma3'] = df['ma3'].astype(float)

analyze_fft(df)
analyze_wavelet(df)
realtimeinfo = ts.get_realtime_quotes(stockno)
print(realtimeinfo)
