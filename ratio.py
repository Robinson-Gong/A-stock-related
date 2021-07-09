from selenium import webdriver
import datetime
import pandas as pd
import time
import pymssql
import os


def get_official_data():
    chrome_driver = r"C:\Program Files\Google\Chrome\chromedriver.exe"  # chromedriver安装位置
    driver = webdriver.Chrome(executable_path=chrome_driver)
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"download.default_directory":os.getcwd()}
    chromeOptions.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(chrome_options=chromeOptions)
    time.sleep(10)
    driver.get("http://www.cnindex.com.cn/sample-detail/download-history?indexcode=399006")
    time.sleep(3)
    driver.close()


def read_data(filepath):
    data = pd.read_excel(filepath)
    return data


def save_data(dataframe, filepath):
    dataframe.to_excel(filepath, index=False, encoding='utf_8_sig')


def change_time_format(dataframe):
    for i in range(dataframe.shape[0]):
        dataframe.iloc[i, 0] = datetime.datetime.strptime(dataframe.iloc[i, 0], '%Y-%m-%d').strftime('%Y%m%d')
    return dataframe


def sql_connect():
    connection = pymssql.connect(host='', user='', password='', database='')
    return connection


def get_time_series(df):
    time_series = []
    for i in range(df.shape[0] // 100):
        time_series.append(df.iloc[100 * i, 0])
    time_series.sort()
    return time_series

class ratio():
    def __inti__(self, start_date = '20200101',end_date = None):
        self.start_date = start_date
        self.end_date = end_date
    def deal_data(self):
        start_date = self.start_date
        end_date = self.end_date
        df = read_data(r'399006_cons.xlsx')
        df = change_time_format(df)
        time_series = get_time_series(df)
        con = sql_connect()
        for i in range(len(time_series)):
            if time_series[i] <= start_date:
                std = len(time_series) - i
            if end_date is not None:
                if time_series[i] <= end_date:
                    edate = len(time_series) - i
        if end_date is None:
            edate = len(time_series) - len(time_series)
        for i in range(edate, std):
            date = str(df.iloc[100 * i, 0])
            sql = 'select S_INFO_WINDCODE,trade_dt,s_dq_close from AShareEODPrices'
            for j in range(100):
                code = str(df.iloc[100 * i + j, 1]) + '.SZ'
                if j == 0:
                    sql = sql + ' where S_INFO_WINDCODE = ' + "'" + code + "'"
                    sql = sql + ' and trade_dt = ' + "'" + date + "'"
                else:
                    sql = sql + ' or S_INFO_WINDCODE = ' + "'" + code + "'"
                    sql = sql + ' and trade_dt = ' + "'" + date + "'"
            sql = sql + ' order by 1'
            print(str(i - edate + 1) + '/' + str(std - edate))
            temp = pd.read_sql(sql, con)
            for k in range(100):
                df.loc[100 * i + k, 'close'] = temp.iloc[k, 2]
        for i in range(df.shape[0]):
            df.loc[i, 'volume'] = df.iloc[i, 4] / df.loc[i, 'close']
        df = df.dropna()
        save_data(df, r'399006_cons.xlsx')
        return df
    
    
    def get_trade_date(self):
        start_date = self.start_date
        end_date = self.end_date
        if end_date is not None:
            ed = end_date
        if end_date is None:
            ed = datetime.date.today().strftime('%Y%m%d')
        if int(datetime.datetime.now().strftime('%H')) < 16:
            ed = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y%m%d')
        con = sql_connect()
        sql = 'select Trade_days from AShareCalendar where TRADE_DAYS between ' + \
              "'" + start_date + "'" + ' and ' + "'" + ed + "'" + \
              " and S_INFO_EXCHMARKET = 'sse' order by TRADE_DAYS "
        trade_date = pd.read_sql(sql, con)
        return trade_date
    
    
    def make_data(self):
        dataframe = pd.DataFrame()
        print(r'处理官方数据')
        df = self.deal_data()
        print(r'生成基础表格')
        trade_date = self.get_trade_date()
        time_series = get_time_series(df)
        print(trade_date)
        print(time_series)
        for j in range(len(trade_date)):
            if len(time_series) - 1 != 0:
                for i in range(len(time_series) - 1):
                    print(str(j * len(time_series) + i + 1) + '/' + str(len(trade_date) * len(time_series)))
                    if time_series[i] <= trade_date.iloc[j, 0] < time_series[i + 1]:
                        for k in range(100):
                            dataframe.loc[j * 100 + k, 'trade_date'] = trade_date.iloc[j, 0]
                            dataframe.loc[j * 100 + k, 'code'] = str(df.iloc[(len(time_series) - i - 1) * 100 + k, 1])
                            dataframe.loc[j * 100 + k, 'name'] = df.iloc[(len(time_series) - i - 1) * 100 + k, 2]
                            dataframe.loc[j * 100 + k, 'vol'] = df.loc[(len(time_series) - i - 1) * 100 + k, 'volume']
                    elif time_series[-1] <= trade_date.iloc[j, 0]:
                        for k in range(100):
                            dataframe.loc[j * 100 + k, 'trade_date'] = trade_date.iloc[j, 0]
                            dataframe.loc[j * 100 + k, 'code'] = str(df.iloc[k, 1])
                            dataframe.loc[j * 100 + k, 'name'] = df.iloc[k, 2]
                            dataframe.loc[j * 100 + k, 'vol'] = df.loc[k, 'volume']
            else:
                for k in range(100):
                    dataframe.loc[j * 100 + k, 'trade_date'] = trade_date.iloc[j, 0]
                    dataframe.loc[j * 100 + k, 'code'] = str(df.iloc[k, 1])
                    dataframe.loc[j * 100 + k, 'name'] = df.iloc[k, 2]
                    dataframe.loc[j * 100 + k, 'vol'] = df.loc[k, 'volume']
        save_data(dataframe,r'399006_detail.xlsx')
        con = sql_connect()
        print(r'获取日数据')
        for i in range(dataframe.shape[0] // 100):
            date = str(dataframe.iloc[100 * i, 0])
            sql = 'select S_INFO_WINDCODE,trade_dt,s_dq_close from AShareEODPrices'
            for j in range(100):
                code = str(dataframe.loc[100 * i + j, 'code']) + '.SZ'
                if j == 0:
                    sql = sql + ' where S_INFO_WINDCODE = ' + "'" + code + "'"
                    sql = sql + ' and trade_dt = ' + "'" + date + "'"
                else:
                    sql = sql + ' or S_INFO_WINDCODE = ' + "'" + code + "'"
                    sql = sql + ' and trade_dt = ' + "'" + date + "'"
            sql = sql + ' order by 1'
            temp = pd.read_sql(sql, con)
            for k in range(100):
                dataframe.loc[100 * i + k, 'close'] = temp.iloc[k, 2]
            print(str(i + 1) + '/' + str(dataframe.shape[0] // 100))
        for i in range(dataframe.shape[0]):
            dataframe.loc[i, 'mv'] = dataframe.loc[i, 'vol'] * dataframe.loc[i, 'close']
        save_data(dataframe,r'399006_detail.xlsx')
    
    
    def getresult(self):
        self.make_data()
        print(r'处理数据获得权重')
        df = read_data(r'399006_detail.xlsx')
        result = pd.DataFrame(columns=['指数代码', '指数名称', '日期', '权重股代码', '权重股市场', '权重', '权重股名称'])
        for i in range(df.shape[0] // 100):
            print(str(i + 1) + '/' + str(df.shape[0] / 100))
            for j in range(100):
                result.loc[100 * i + j, '指数代码'] = '399006'
                result.loc[100 * i + j, '指数名称'] = '创业板指'
                result.loc[100 * i + j, '日期'] = str(df.loc[100 * i + j, 'trade_date'])
                result.loc[100 * i + j, '权重股代码'] = str(df.loc[100 * i + j, 'code'])
                result.loc[100 * i + j, '权重股市场'] = '深圳'
                result.loc[100 * i + j, '权重股名称'] = df.loc[100 * i + j, 'name']
                result.loc[100 * i + j, '权重'] = df.iloc[100 * i + j, -1] / df.iloc[100 * i:100 * i + 100, -1].sum()
        save_data(result,r'399006_权重.xlsx')
        CYBZ = pd.read_excel('399006_权重.xlsx')
        date = list(set(CYBZ['日期']))
        for i in date:
            f = open('CYBZ.'+str(i),'w')
            f.write('!DATE:'+str(i)+'\n!WEIGHT:ASIS\n')
            for k in range(len(CYBZ['日期'])):
                if CYBZ.iloc[k,2] == i:
                    f.write(str(CYBZ.iloc[k,3])+'   A   '+str(CYBZ.iloc[k,5])+'\n')
            f.close()
        return 0



start_date = '20210101'
end_date = None
ratio(start_date = start_date,end_date = end_date)
print(r'获取官网数据')
if os.path.isfile(r'399006_cons.xlsx'):
    os.remove(r'399006_cons.xlsx')
get_official_data()
ratio.getresult()


