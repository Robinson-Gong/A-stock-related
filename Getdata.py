import tushare as ts
import pandas as pd
import os

class getdata():
    def __init__(self, ds='', de = '', tscode = '', path = '', asset = 'E', adj = 'qfq'):
        self.ds = ds
        self.de = de
        self.tscode = tscode
        self.path = path
        self.asset = asset
        self.adj = adj
    def getmargindata(self):
        path = self.path + '\\' + self.tscode
        path = path.strip()
        path = path.rstrip("\\")
        isExists = os.path.exists(path)
        if not isExists:
            os.mkdir(path)
        csv_filepath1 = path + '\\' + self.tscode + '_margin.csv'
        ts.set_token('f080e8e80b7d59a508fd93f99e230ab69fabb4727541331ed86ac9e3')
        pro = ts.pro_api()
        df = pro.margin_detail(ts_code=self.tscode, start_date=self.ds, end_date=self.de)
        df.sort_values("trade_date", inplace=True)
        df.to_csv(csv_filepath1, index=False, encoding='gbk')
        df1 = pro.margin(start_date=self.ds, end_date=self.de, exchange_id='SSE')
        df1.sort_values("trade_date", inplace=True)
        isExists = os.path.exists(self.path + '\\' + 'SSE')
        if not isExists:
            os.mkdir(self.path + '\\' + 'SSE')
        df1.to_csv(self.path + '\\' + 'SSE\SSE_margin.csv', index=False, encoding='gbk')
        df2 = pro.margin(start_date=self.ds, end_date=self.de, exchange_id='SZSE')
        df2.sort_values("trade_date", inplace=True)
        isExists = os.path.exists(self.path + '\\' + 'SZSE')
        if not isExists:
            os.mkdir(self.path + '\\' + 'SZSE')
        df2.to_csv(self.path + '\\' + 'SZSE\SZSE_margin.csv', index=False, encoding='gbk')
        return 0

    def getkdata(self):
        path = 'F:\stock data\\' + self.tscode
        path = path.strip()
        path = path.rstrip("\\")
        isExists = os.path.exists(path)
        if not isExists:
            os.mkdir(path)
        csv_filepath1 = path + '\\' + self.tscode + '_k.csv'
        ts.set_token('f080e8e80b7d59a508fd93f99e230ab69fabb4727541331ed86ac9e3')
        results = ts.pro_bar(ts_code=self.tscode, asset =self.asset, adj= self.adj, start_date=self.ds, end_date=self.de, ma=[3, 5, 10, 30])
        results.sort_values("trade_date", inplace=True)
        results.to_csv(csv_filepath1, index=False, encoding='gbk')
        results1 = ts.pro_bar(ts_code='000001.SH', asset='I', start_date=self.ds, end_date=self.de, ma=[3, 5, 10, 30])
        results1.sort_values("trade_date", inplace=True)
        isExists = os.path.exists(self.path + '\\' + 'SSE')
        if not isExists:
            os.mkdir(self.path + '\\' + 'SSE')
        results1.to_csv(self.path + '\\' + 'SSE\SSE_k.csv', index=False, encoding='gbk')
        results2 = ts.pro_bar(ts_code='399001.SZ', asset='I', start_date=self.ds, end_date=self.de, ma=[3, 5, 10, 30])
        results2.sort_values("trade_date", inplace=True)
        isExists = os.path.exists(self.path + '\\' + 'SZSE')
        if not isExists:
            os.mkdir(self.path + '\\' + 'SZSE')
        results2.to_csv(self.path + '\\' + 'SZSE\SZSE_k.csv', index=False, encoding='gbk')
        return 0

