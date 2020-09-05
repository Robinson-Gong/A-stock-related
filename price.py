import math
import cmath
import scipy.stats
import Getdata
from arch.univariate import ConstantMean, GARCH, Normal
import os
import pandas as pd

class Parameter:
    def __init__(self,strikeprice,spotprice,volatility,rate,time,period,initialprice):
        self.K = strikeprice
        self.S = initialprice
        self.sigma = volatility
        self.r = rate
        self.T = time
        self.pr = period
        self.t = self.T/slef.pr
        self.u = math.exp(sigma*cmath.sqrt(t))
        self.d = u**(-1)
        self.p = (math.exp(r*t)-d)/(u-d)
        self.C = spotprice
        self.list=[]

    def priceTreecall(self):
        for i in range(self.pr):
            temp = self.S*self.u**(self.pr - i)*self.d**(i)-self.K
            if temp < 0.0:
                temp = 0.0
            self.list.append(temp)
        for j in range(self.pr - 1):
            for k in range(0,len(self.list) - 1,-1):
                self.list[k] = (math.exp(-self.r*self.t/self.pr)*(self.p*self.list[k]+(1-self.p)*self.list[k+1]))
            if len(list) == 1:
                break
            self.list.pop()
        return self.list[0]

    def priceBSMcall(self):
        d1 = (math.log(self.S/self.K)+(self.r+self.sigma*self.sigma/2.0)*self.T/(self.sigma*cmath.sqrt(self.T)))
        d2 = d1 - self.sigma * cmath.sqrt(self.T)
        call = self.S*norm.ppf(d1,0,1)- self.K*exp(-1*self.r*self.T)*norm.ppf(d2,0,1)
        return call

    def priceTreeput(self):
        for i in range(self.pr):
            temp = self.K-self.S*self.u**(self.pr - i)*self.d**(i)
            if temp < 0:
                temp = 0
            self.list.append(temp)
        for j in range(self.pr - 1):
            for k in range(0,len(self.list) - 1,-1):
                self.list[k] = (math.exp(-self.r*self.t/self.pr)*(self.p*self.list[k]+(1-self.p)*self.list[k+1]))
            if len(list) == 1:
                break
            self.list.pop()
        return self.list[0]

    def priceBSMput(self):
        d1 = (math.log(self.S/self.K)+(self.r+self.sigma*self.sigma/2.0)*self.T/(self.sigma*cmath.sqrt(self.T)))
        d2 = d1 - self.sigma*cmath.sqrt(self.T)
        put = self.K*exp(-1*self.r*self.T)*norm.ppf(-d2,0,1)-self.S*norm.ppf(-d1,0,1)
        return put

    def BSMVega(self):
        d1 = (math.log(self.S / self.K) + (self.r + self.sigma * self.sigma / 2.0) * self.T / (
                    self.sigma * cmath.sqrt(self.T)))
        vega = self.S * stats.norm.cdf(d1, 0, 1) * np.sqrt(self.T)
        return Vega

    def BSMcallimpvol(self):
        for i in range(100):
            sigma_est -= ((priceBSMcall() - self.C)
                          / BSMVega())
        return sigma_est

    def BSMputimpvol(self):
        for i in range(100):
            sigma_est -= ((priceBSMput() - self.C)
                          / BSMVega())
        return sigma_est


class volatility():
    def __init__(self, path = '', tscode= '', format = 'k', asset = 'Index'):
        self.path = path
        self.tscode = tscode
        self.format = format
        self.asset = asset
    def readdata(self):
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
            csv_filepath = self.path + '\\' + asset  + '\\' + self.tscode + '\\' + self.tscode + '_' + self.format + '.csv'
            csv_data = pd.read_csv(csv_filepath)
            return csv_data
    def getyieldrate(self):
        dataframe = volatility.readdata(self)
        yieldrate = 100*dataframe['close'].pct_change().dropna()
        if self.asset == 'E':
            asset = 'Stock'
        elif self.asset == 'I':
            asset = 'Index'
        elif self.asset == 'C':
            asset = 'DigitalCurrency'
        elif self.asset == 'FT':
            asset = 'Future'
        elif self.asset == 'FD':
            asset = 'Fund'
        elif self.asset == 'O':
            asset = 'Options'
        elif self.asset == 'CB':
            asset = 'ConvertibleBond'
        csv_filepath = self.path + '\\' + asset + '\\' + self.tscode + '\\' + self.tscode + '_yieldrate.csv'
        yieldrate.to_csv(csv_filepath,index=False, encoding='gbk')
        return yieldrate
    def getvolatility(self):
        df = volatility.getyieldrate(self)
        vol = 0.0
        for i in range(1,len(df)):
            vol = vol + df[i]*df[i]/10000.0
        am = ConstantMean(df)
        am.volatility = GARCH(1, 0, 1)
        am.distribution = Normal()
        res = am.fit()
        print('vol =' + str(vol))
        print(res.summary)
        return 0

