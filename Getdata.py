import tushare as ts
import pandas as pd
import os


class getdata():
    def __init__(self, ds='', de='', tscode='', path='', asset='E', adj='qfq', freq='D', factor=''):
        self.ds = ds
        self.de = de
        self.tscode = tscode
        self.path = path
        self.asset = asset
        self.adj = adj
        self.freq = freq
        self.factor = factor
    def getmargindata(self):
        path = self.path
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
        csv_filepath1 = path + '\\' + 'Stock\\' + self.tscode
        isExists = os.path.exists(csv_filepath1)
        if not isExists:
            os.makedirs(csv_filepath1)
        csv_filepath1 = csv_filepath1 + '\\' + self.tscode + '_margin.csv'
        pro = ts.pro_api()
        df = pro.margin_detail(ts_code=self.tscode, start_date=self.ds, end_date=self.de)
        df.sort_values("trade_date", inplace=True)
        df.to_csv(csv_filepath1, index=False, encoding='gbk')
        df1 = pro.margin(start_date=self.ds, end_date=self.de, exchange_id='SSE')
        df1.sort_values("trade_date", inplace=True)
        isExists = os.path.exists(self.path + '\\' + 'Index\SSE')
        if not isExists:
            os.makedirs(self.path + '\\' + 'Index\SSE')
        df1.to_csv(self.path + '\\' + 'Index\SSE\SSE_margin.csv', index=False, encoding='gbk')
        df2 = pro.margin(start_date=self.ds, end_date=self.de, exchange_id='SZSE')
        df2.sort_values("trade_date", inplace=True)
        isExists = os.path.exists(self.path + '\\' + 'Index\SZSE')
        if not isExists:
            os.makedirs(self.path + '\\' + 'Index\SZSE')
        df2.to_csv(self.path + '\\' + 'Index\SZSE\SZSE_margin.csv', index=False, encoding='gbk')
        return 0

    def getkdata(self):
        path = self.path
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
        if self.asset == 'E':
            csv_filepath1 = path + '\\' + 'Stock\\' + self.tscode
        elif self.asset == 'I':
            csv_filepath1 = path + '\\' + 'Index\\' + self.tscode
        elif self.asset == 'C':
            csv_filepath1 = path + '\\' + 'DigitalCurrency\\' + self.tscode
        elif self.asset == 'FT':
            csv_filepath1 = path + '\\' + 'Future\\' + self.tscode
        elif self.asset == 'FD':
            csv_filepath1 = path + '\\' + 'Fund\\' + self.tscode
        elif self.asset == 'O':
            csv_filepath1 = path + '\\' + 'Options\\' + self.tscode
        elif self.asset == 'CB':
            csv_filepath1 = path + '\\' + 'ConvertibleBond\\' + self.tscode
        isExists = os.path.exists(csv_filepath1)
        if not isExists:
            os.makedirs(csv_filepath1)
        csv_filepath1 = csv_filepath1 + '\\' + self.tscode + '_k.csv'
        results = ts.pro_bar(ts_code=self.tscode, asset=self.asset, adj=self.adj, start_date=self.ds, end_date=self.de,
                             ma=[3, 5, 10, 30], freq=self.freq, factors=self.factor)
        results.sort_values("trade_date", inplace=True)
        results.to_csv(csv_filepath1, index=False, encoding='gbk')
        results1 = ts.pro_bar(ts_code='000001.SH', asset='I', start_date=self.ds, end_date=self.de, ma=[3, 5, 10, 30],
                              freq=self.freq, factors=self.factor)
        results1.sort_values("trade_date", inplace=True)
        isExists = os.path.exists(self.path + '\\' + 'Index\SSE')
        if not isExists:
            os.makedirs(self.path + '\\' + 'Index\SSE')
        results1.to_csv(self.path + '\\' + 'Index\SSE\SSE_k.csv', index=False, encoding='gbk')
        results2 = ts.pro_bar(ts_code='399001.SZ', asset='I', start_date=self.ds, end_date=self.de, ma=[3, 5, 10, 30],
                              freq=self.freq, factors=self.factor)
        results2.sort_values("trade_date", inplace=True)
        isExists = os.path.exists(self.path + '\\' + 'Index\SZSE')
        if not isExists:
            os.makedirs(self.path + '\\' + 'Index\SZSE')
        results2.to_csv(self.path + '\\' + 'Index\SZSE\SZSE_k.csv', index=False, encoding='gbk')
        return 0

    def readdata(self, format):
        path = self.path
        path = path.strip()
        path = path.rstrip("\\")
        isExists = os.path.exists(path)
        if not isExists:
            print('file does not exist')
        else:
            if self.asset == 'E':
                asset = 'Stock'
            elif self.asset == 'I':
                asset = 'Index'
            elif self.asset == 'C':
                asset = 'DigitalCurrency'
            elif self.asset == 'FT':
                asset = 'Future'
            elif self.asset == 'FD':
                asset  = 'Fund'
            elif self.asset == 'O':
                asset = 'Options'
            elif self.asset == 'CB':
                asset  = 'ConvertibleBond'
            csv_filepath = self.path + '\\' + asset  + '\\' + self.tscode + '\\' + self.tscode + '_' + format + '.csv'
            csv_data = pd.read_csv(csv_filepath)
            return csv_data
