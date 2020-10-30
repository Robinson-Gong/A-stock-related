from selenium import webdriver
import datetime
import pandas as pd
import time
import pymssql
import os


def get_official_data():
    chrome_driver = r"C:\Program Files\Google\Chrome\chromedriver.exe"  # chromedriver安装位置
    driver = webdriver.Chrome(executable_path=chrome_driver)
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
    connection = pymssql.connect(host='192.168.1.126', user='Wind', password='111111', database='WindDB')
    return connection


def get_time_series(df):
    time_series = []
    for i in range(df.shape[0] // 100):
        time_series.append(df.iloc[100 * i, 0])
    time_series.sort()
    return time_series


def deal_data(path=r'C:\Users\Administrator\Desktop\data', start_date='20200101', end_date=None):
    df = read_data(r'C:\Users\Administrator\Downloads\399006_cons.xlsx')
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
    save_data(df, path + '\\' + '399006_cons.xlsx')
    return df


def get_trade_date(start_date='20200101', end_date=None):
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


def make_data(path=r'C:\Users\Administrator\Desktop\data', start_date='20200101'):
    dataframe = pd.DataFrame()
    print(r'处理官方数据')
    df = deal_data(path=path, start_date=start_date)
    print(r'生成基础表格')
    trade_date = get_trade_date(start_date=start_date)
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
    save_data(dataframe, path + '\\' + 'detail.xlsx')
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
    save_data(dataframe, path + '\\' + 'detail.xlsx')


def getresult(path=r'C:\Users\Administrator\Desktop\data'):
    make_data(path=path)
    print(r'处理数据获得权重')
    df = read_data(path + '\\' + 'detail.xlsx')
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
            result.loc[100 * i + j, '权重'] = 100 * df.iloc[100 * i + j, -1] / df.iloc[100 * i:100 * i + 100, -1].sum()
    save_data(result, path + '\\' + '权重.xlsx')
    return 0


def update(path=r'C:\Users\Administrator\Desktop\data'):
    filepath = path + '\\' + '权重.xlsx'
    result = read_data(filepath)
    length = result.shape[0]
    last_date = str(result.iloc[-1, 2])
    print(last_date)
    trade_date = get_trade_date()
    print(trade_date)
    place = [i for i, x in enumerate(trade_date['Trade_days']) if x == last_date][0]
    if place + 1 == trade_date.shape[0]:
        print(r'已是最新数据')
        return 0
    else:
        start_date = trade_date.iloc[place + 1, 0]
        make_data(path=path, start_date=start_date)
        print(r'处理数据获得权重')
        df = read_data(path + '\\' + 'detail.xlsx')
        for i in range(df.shape[0] // 100):
            print(str(i + 1) + '/' + str(df.shape[0] / 100))
            for j in range(100):
                result.loc[length + 100 * i + j, '指数代码'] = '399006'
                result.loc[length + 100 * i + j, '指数名称'] = '创业板指'
                result.loc[length + 100 * i + j, '日期'] = str(df.loc[100 * i + j, 'trade_date'])
                result.loc[length + 100 * i + j, '权重股代码'] = str(df.loc[100 * i + j, 'code'])
                result.loc[length + 100 * i + j, '权重股市场'] = '深圳'
                result.loc[length + 100 * i + j, '权重股名称'] = df.loc[100 * i + j, 'name']
                result.loc[length + 100 * i + j, '权重'] = 100 * df.iloc[100 * i + j, -1] / df.iloc[100 * i:100 * i + 100,
                                                                                          -1].sum()
        save_data(result, path + '\\' + '权重.xlsx')
        return 0


def main():
    exists = os.path.isfile(save_file_path + '\\' + '权重.xlsx')
    if not exists:
        print(r'获取官网数据')
        if os.path.isfile(r'C:\Users\Administrator\Downloads\399006_cons.xlsx'):
            os.remove(r'C:\Users\Administrator\Downloads\399006_cons.xlsx')
        get_official_data()
        getresult(path=save_file_path)
    else:
        print(r'获取官网数据')
        if os.path.isfile(r'C:\Users\Administrator\Downloads\399006_cons.xlsx'):
            os.remove(r'C:\Users\Administrator\Downloads\399006_cons.xlsx')
        get_official_data()
        update(path=save_file_path)


if __name__ == '__main__':
    save_file_path = input(r'请输入保存地址(不输入默认C:\Users\Administrator\Desktop\data)：')
    isExists = os.path.exists(save_file_path)
    if not isExists:
        save_file_path = r'C:\Users\Administrator\Desktop\data'
    isExists = os.path.exists(save_file_path)
    if not isExists:
        os.makedirs(save_file_path)
    main()
