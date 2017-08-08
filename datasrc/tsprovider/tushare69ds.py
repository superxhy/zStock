#!/usr/bin/env python
# -*- coding:utf-8 -*- 
'''
Created on 2017-3-8

@author: yuql
'''

from datasrc import *
import tushare as ts
import numpy as np
import datetime

class TsDatasrc(SecurityDataSrcBase):

    INDEX_LABELS = ['sh', 'sz', 'hs300', 'sz50', 'cyb', 'zxb', 'zx300', 'zh500']
    INDEX_NAMES = {'sh':'上证指数', 'sz':'深圳成指', 'hs300':'沪深300', 'sz50':'上证50', 'cyb':'创业板', 'zxb':'中小板', 'zx300':'中小300', 'zh500':'中证500'}
    
    def __init__(self, name):
        super(TsDatasrc, self).__init__(name)
        print 'security init begin ...'
        self.__initFlag__()
        self.__df_allsecurities__ = ts.get_stock_basics().sort_index()
        print 'security init end ...'
    
    def __initFlag__(self):
        #use sh for index flag
        flagindex = self.INDEX_LABELS[0]
        df_data = ts.get_k_data(flagindex, index=False, ktype='D').tail(1)
        if df_data.empty == True:
            print "security:%s NO __initFlag__!" %(str(flagindex))
            return
        if len(df_data['close'].values) < 1:
            print "security:%s noclose data __initFlag__!" %(str(flagindex))
        dateStr = df_data['date'].values[0]
        close = df_data['close'].values[0]
        print "init flagindex last time:%s,close:%s" %(str(dateStr),str(close)) 
        current_dt =  self.__getdatetime__(dateStr)
        self.__indexc__= close
        self.__context__= TsContext(current_dt)
        
    def __getdatetime__(self,timestr):
        #'2017-03-31 15:00'.split()[0].split('-')
        timetemp = timestr.split()
        dates = timetemp[0].split('-')
        time = ['15', '00']
        if len(timetemp) > 1:
            time =  timestr.split()[1].split(':')
        current_dt = datetime.datetime(int(dates[0]),int(dates[1]),int(dates[2]),int(time[0]),int(time[1]))
        return current_dt
    
    def getVersionName(self):
        return "0.8.2"
    
    def getDataSrcName(self):
        return "tushare"
    
    # 获取所有指数代码
    #return list
    def GET_ALL_INDEXES(self):
        return self.INDEX_LABELS
    
    # 获取所有股票代码
    #return list
    def GET_ALL_SECURITIES(self,filtPaused=True, filtSt=True):
        l_stocks = self.__df_allsecurities__.index.get_values().tolist()
        print "l_stocks %s in all", len(l_stocks)
        if filtPaused or filtSt:
            filtresult = []
            for s in l_stocks:
                isfilted = False
                try:
                    dfreal = ts.get_realtime_quotes(s)
                except Exception,e:
                    print Exception,":",e
                    dfreal = None
                if not dfreal is None and filtPaused:
                    if float(str(dfreal['volume'][0])) == 0 and float(str(dfreal['bid'][0])) == 0 and float(str(dfreal['ask'][0])) == 0:
                        isfilted = True
                if not dfreal is None and filtSt:
                    if str(dfreal['name'][0]).find('ST') > -1:
                        isfilted = True
                if isfilted:
                    print "security %s isfilted" % str(s)
                    pass
                else:
                    filtresult.append(s)
            l_stocks = filtresult
            print "l_stocks %s after filtSt", len(l_stocks)
        return l_stocks
    
    # 获取股票信息
    #security
    '''
    code,代码
    name,名称
    industry,所属行业
    area,地区
    pe,市盈率
    outstanding,流通股本(亿)
    totals,总股本(亿)
    totalAssets,总资产(万)
    liquidAssets,流动资产
    fixedAssets,固定资产
    reserved,公积金
    reservedPerShare,每股公积金
    esp,每股收益
    bvps,每股净资
    pb,市净率
    timeToMarket,上市日期
    undp,未分利润
    perundp, 每股未分配
    rev,收入同比(%)
    profit,利润同比(%)
    gpr,毛利率(%)
    npr,净利润率(%)
    holders,股东人数
    '''
    def GET_SECURITY_INFO(self, security):
        if security in self.INDEX_LABELS:
            return {'name':self.INDEX_NAMES[security],'industry':'指数'}
        
        df_security = self.__df_allsecurities__[security : security]
        securityInfo = {
        'name': df_security['name'].get_values()[0].decode("utf-8"),
        'industry':df_security['industry'].get_values()[0].decode("utf-8"),
        'area':df_security['area'].get_values()[0].decode("utf-8"),
        'pe':df_security['pe'].get_values()[0],
        'outstanding':df_security['outstanding'].get_values()[0],
        'totals':df_security['totals'].get_values()[0],
        'totalAssets':df_security['totalAssets'].get_values()[0],
        'liquidAssets':df_security['liquidAssets'].get_values()[0],
        'fixedAssets':df_security['fixedAssets'].get_values()[0],
        'reserved':df_security['reserved'].get_values()[0],
        'esp':df_security['esp'].get_values()[0],
        'bvps':df_security['bvps'].get_values()[0],
        'pb':df_security['pb'].get_values()[0],
        'timeToMarket':df_security['timeToMarket'].get_values()[0],
        'undp':df_security['undp'].get_values()[0],
        'perundp':df_security['perundp'].get_values()[0],
        'rev':df_security['rev'].get_values()[0],
        'profit':df_security['profit'].get_values()[0],
        'gpr':df_security['gpr'].get_values()[0],
        'npr':df_security['npr'].get_values()[0],
        'holders':df_security['holders'].get_values()[0]}
        return securityInfo
    
    # 获取当前分时收盘价
    def GET_CLOSE_DATA_INTRADAY(self, context, security, data={}, freq=5, dataCount=1):
        periodtype = str(freq)
        df_data = ts.get_k_data(security, index=False, ktype=periodtype).tail(dataCount)
        if df_data.empty == True:
            print "security:%s in context:%s NO GET_CLOSE_DATA_INTRADAY!" %(str(security),str(context))
            return np.array([np.nan])
        return df_data['close'].values
    
    def GET_HIGH_DATA_INTRADAY(self, context, security, data={}, freq=5, dataCount=1):
        periodtype = str(freq)
        df_data = ts.get_k_data(security, index=False, ktype=periodtype).tail(dataCount)
        if df_data.empty == True:
            print "security:%s in context:%s NO GET_HIGH_DATA_INTRADAY!" %(str(security),str(context))
            return np.array([np.nan])
        return df_data['high'].values

    def GET_LOW_DATA_INTRADAY(self, context, security, data={}, freq=5, dataCount=1):
        periodtype = str(freq)
        df_data = ts.get_k_data(security, index=False, ktype=periodtype).tail(dataCount)
        if df_data.empty == True:
            print "security:%s in context:%s NO GET_LOW_DATA_INTRADAY!" %(str(security),str(context))
            return np.array([np.nan])
        return df_data['low'].values
    
    def GET_VOL_DATA_INTRADAY(self, context, security, data={}, freq=5, dataCount=1):
        periodtype = str(freq)
        df_data = ts.get_k_data(security, index=False, ktype=periodtype).tail(dataCount)
        if df_data.empty == True:
            print "security:%s in context:%s NO GET_VOL_DATA_INTRADAY!" %(str(security),str(context))
            return np.array([np.nan])
        return df_data['volume'].values
    
    def GET_HIGH_DAY(self, context, security, ref=0):
        dataCount =  ref + 1
        df_data = ts.get_k_data(security, index=False, ktype='D').tail(dataCount)
        if df_data.empty == True:
            print "security:%s in context:%s NO GET_HIGH_DAY!" %(str(security),str(context))
            return np.nan
        if len(df_data['high']) < ref:
            return np.nan
        return df_data['high'].values[-ref]
            
    def GET_LOW_DAY(self, context, security, ref=0):
        dataCount =  ref + 1
        df_data = ts.get_k_data(security, index=False, ktype='D').tail(dataCount)
        if df_data.empty == True:
            print "security:%s in context:%s NO GET_LOW_DAY!" %(str(security),str(context))
            return np.nan
        if len(df_data['low']) < ref:
            return np.nan
        return df_data['low'].values[-ref]
            
    def GET_OPEN_DAY(self, context, security, ref=0):
        if ref==0:
            dfreal = ts.get_realtime_quotes(security)
            if dfreal.empty == True:
                return np.nan
            return float(dfreal['open'][0])
        else:
            dataCount =  ref + 1
            df_data = ts.get_k_data(security, index=False, ktype='D').tail(dataCount)
            if df_data.empty == True:
                print "security:%s in context:%s NO GET_OPEN_DAY!" %(str(security),str(context))
                return np.nan
            if len(df_data['open']) < ref:
                return np.nan
            return df_data['open'].values[-ref]
        
    # 获取日线历史数据最大值
    def GET_HIGH_DATA_DAY(self, context,security,isLastest=True,data={},dataCount=1):
        df_data = ts.get_k_data(security, index=False, ktype='D').tail(dataCount)
        if df_data.empty == True:
            print "security:%s in context:%s NO GET_HIGH_DATA_DAY!" %(str(security),str(context))
            return np.array([np.nan])
        return df_data['high'].values
    
    # 获取日线历史数据最小值
    def GET_LOW_DATA_DAY(self, context,security,isLastest=True,data={},dataCount=1):
        df_data = ts.get_k_data(security, index=False, ktype='D').tail(dataCount)
        if df_data.empty == True:
            print "security:%s in context:%s NO GET_LOW_DATA_DAY!" %(str(security),str(context))
            return np.array([np.nan])
        return df_data['low'].values
  
    # 获取周线历史数据最大值
    def GET_HIGH_DATA_WEEK(self,context,security,isLastest=True,data={},dataCount=1,isSample=False):
        if isSample:
            df_data = ts.get_k_data(security, index=False, ktype='W').tail(dataCount)
            if df_data.empty == True:
                print "security:%s in context:%s NO GET_HIGH_DATA_WEEK!" %(str(security),str(context))
                return np.array([np.nan])
            if len(df_data['high'].values) < 1:
                return np.array([np.nan])
            return df_data['high'].values
        else:
            freq = 5
            df_data = ts.get_k_data(security, index=False, ktype='D').tail(dataCount*freq)
            if df_data.empty == True:
                print "security:%s in context:%s NO GET_HIGH_DATA_WEEK!" %(str(security),str(context))
                return np.array([np.nan])
            highData = df_data['high'].values
            high = highData[:-1]
            highLast = np.nan
            highWeek = np.array([np.nan])
            if len(highData) >= freq:
                pass
            else: 
                return highWeek
            weekday = 1
            if context and any(context):
                weekday = context.current_dt.isoweekday()
            else:
                dateStr = df_data.tail(1)['date'].values[0]
                current_dt =  self.__getdatetime__(dateStr)
                weekday = current_dt.isoweekday()
            highWeek = self.SIMPLE_DATA_HIGH(high,dataCount,freq,weekday-1)
            highLast = highData[-weekday:].max()
            if not np.isnan(highLast) and highLast != 0:
                highWeek= np.append(highWeek,highLast)
            return highWeek
    
    # 获取周线历史数据最小值
    def GET_LOW_DATA_WEEK(self, context,security,isLastest=True,data={},dataCount=1,isSample=False):
        if isSample:
            df_data = ts.get_k_data(security, index=False, ktype='W').tail(dataCount)
            if df_data.empty == True:
                print "security:%s in context:%s NO GET_LOW_DATA_WEEK!" %(str(security),str(context))
                return np.array([np.nan])
            if len(df_data['low'].values) < 1:
                return np.array([np.nan])
            return df_data['low'].values
        else:
            freq = 5
            df_data = ts.get_k_data(security, index=False, ktype='D').tail(dataCount*freq)
            if df_data.empty == True:
                print "security:%s in context:%s NO GET_LOW_DATA_WEEK!" %(str(security),str(context))
                return np.array([np.nan])
            lowData = df_data['low'].values
            low = lowData[:-1]
            lowLast = np.nan
            lowWeek = np.array([np.nan])
            if len(lowData) >= freq:
                pass
            else: 
                return lowWeek
            weekday = 1
            if context and any(context):
                weekday = context.current_dt.isoweekday()
            else:
                dateStr = df_data.tail(1)['date'].values[0]
                current_dt =  self.__getdatetime__(dateStr)
                weekday = current_dt.isoweekday()
            lowWeek = self.SIMPLE_DATA_LOW(low,dataCount,freq,weekday-1)
            lowLast = lowData[-weekday:].min()
            if not np.isnan(lowLast) and lowLast != 0:
                lowWeek= np.append(lowWeek,lowLast)
            return lowWeek
    
    # 获取月线历史数据最大值
    def GET_HIGH_DATA_MONTH(self, context,security,isLastest=True,data={},dataCount=1,isSample=True):
        if isSample:
            df_data = ts.get_k_data(security, index=False, ktype='M').tail(dataCount)
            if df_data.empty == True:
                print "security:%s in context:%s NO GET_HIGH_DATA_MONTH!" %(str(security),str(context))
                return np.array([np.nan])
            if len(df_data['high'].values) < 1:
                return np.array([np.nan])
            return df_data['high'].values
        else:
            freq = 20
            df_data = ts.get_k_data(security, index=False, ktype='D').tail(dataCount*freq)
            if df_data.empty == True:
                print "security:%s in context:%s NO GET_HIGH_DATA_MONTH!" %(str(security),str(context))
                return np.array([np.nan])
            highData = df_data['high'].values
            high = highData[:-1]
            highLast = np.nan
            highMonth = np.array([np.nan])
            if len(highData) >= freq:
                pass
            else: 
                return highMonth
            day = 1
            if context and any(context):
                day = context.current_dt.day
            else:
                dateStr = df_data.tail(1)['date'].values[0]
                current_dt =  self.__getdatetime__(dateStr)
                day = current_dt.day
            highMonth = self.SIMPLE_DATA_HIGH(high,dataCount,freq,day-1)
            highLast = highData[-day:].max()
            if not np.isnan(highLast) and highLast != 0:
                highMonth= np.append(highMonth,highLast)
            return highMonth
    
    # 获取月线历史数据最小值
    def GET_LOW_DATA_MONTH(self, context,security,isLastest=True,data={},dataCount=1,isSample=True):
        if isSample:
            df_data = ts.get_k_data(security, index=False, ktype='M').tail(dataCount)
            if df_data.empty == True:
                print "security:%s in context:%s NO GET_LOW_DATA_MONTH!" %(str(security),str(context))
                return np.array([np.nan])
            if len(df_data['low'].values) < 1:
                return np.array([np.nan])
            return df_data['low'].values
        else:
            freq = 20
            df_data = ts.get_k_data(security, index=False, ktype='D').tail(dataCount*freq)
            if df_data.empty == True:
                print "security:%s in context:%s NO GET_LOW_DATA_MONTH!" %(str(security),str(context))
                return np.array([np.nan])
            lowData = df_data['low'].values
            low = lowData[:-1]
            lowLast = np.nan
            lowMonth = np.array([np.nan])
            if len(lowData) >= freq:
                pass
            else: 
                return lowMonth
            day = 1
            if context and any(context):
                day = context.current_dt.day
            else:
                dateStr = df_data.tail(1)['date'].values[0]
                current_dt =  self.__getdatetime__(dateStr)
                day = current_dt.day
            lowMonth = self.SIMPLE_DATA_LOW(low,dataCount,freq,day-1)
            lowLast = lowData[-day:].min()
            if not np.isnan(lowLast) and lowLast != 0:
                lowMonth= np.append(lowMonth,lowLast)
            return lowMonth
        
    # 获取当前日线或ref天前收盘价
    def GET_CLOSE_DAY(self, security, ref=0 ,data={}):
        dataCount =  ref + 1
        df_data = ts.get_k_data(security, index=False, ktype='D').tail(dataCount)
        if df_data.empty == True:
            print "security:%s NO GET_CLOSE_DAY!" %(str(security))
            return np.nan
        if len(df_data['close']) < ref + 1:
            return np.nan
        return df_data['close'].values[-ref]
    
    # 获取日线历史数据
    def GET_CLOSE_DATA_DAY(self, security,isLastest=True,data={},dataCount=20):
        df_data = ts.get_k_data(security, index=False, ktype='D').tail(dataCount)
        if df_data.empty == True:
            print "security:%s NO GET_CLOSE_DATA_DAY!" %(str(security))
            return np.array([np.nan])
        closeData = df_data['close'].values
        if len(closeData) < 1:
            return np.array([np.nan])
        return closeData
    
    # 获取周线历史数据
    def GET_CLOSE_DATA_WEEK(self, context, security,isLastest=True,data={},dataCount=20,isSample=False):
        if isSample:
            df_data = ts.get_k_data(security, index=False, ktype='W').tail(dataCount)
            if df_data.empty == True:
                print "security:%s in context:%s NO GET_CLOSE_DATA_WEEK!" %(str(security),str(context))
                return np.array([np.nan])
            if len(df_data['close'].values) < 1:
                return np.array([np.nan])
            return df_data['close'].values
        else:
            freq = 5
            df_data = ts.get_k_data(security, index=False, ktype='D').tail(dataCount*freq)
            if df_data.empty == True:
                print "security:%s in context:%s NO GET_CLOSE_DATA_WEEK!" %(str(security),str(context))
                return np.array([np.nan])
            closeData = df_data['close'].values
            close = closeData[:-1]
            closeLast = np.nan
            closeWeek = np.array([np.nan])
            if len(closeData) >= freq:
                closeLast = df_data['close'].values[-1]
            else: 
                return closeWeek
            weekday = 1
            if context and any(context):
                weekday = context.current_dt.isoweekday()
            else:
                dateStr = df_data.tail(1)['date'].values[0]
                current_dt =  self.__getdatetime__(dateStr)
                weekday = current_dt.isoweekday()
            closeWeek = self.SIMPLE_DATA(close,dataCount,freq,weekday-1)
            if not np.isnan(closeLast) and closeLast != 0:
                closeWeek= np.append(closeWeek,closeLast)
            return closeWeek
    
    # 获取月线历史数据
    def GET_CLOSE_DATA_MONTH(self, context,security,isLastest=True,data={},dataCount=20,isSample=True):
        if isSample:
            df_data = ts.get_k_data(security, index=False, ktype='M').tail(dataCount)
            if df_data.empty == True:
                print "security:%s in context:%s NO GET_CLOSE_DATA_MONTH!" %(str(security),str(context))
                return np.array([np.nan])
            if len(df_data['close'].values) < 1:
                return np.array([np.nan])
            return df_data['close'].values
        else:
            freq = 20
            df_data = ts.get_k_data(security, index=False, ktype='D').tail(dataCount*freq)
            if df_data.empty == True:
                print "security:%s in context:%s NO GET_CLOSE_DATA_MONTH!" %(str(security),str(context))
                return np.array([np.nan])
            closeData = df_data['close'].values
            close = closeData[:-1]
            closeLast = np.nan
            closeMonth = np.array([np.nan])
            if len(closeData) >= freq:
                closeLast = df_data['close'].values[-1]
            else: 
                return closeMonth
            day = 1
            if context and any(context):
                day = context.current_dt.day
            else:
                dateStr = df_data.tail(1)['date'].values[0]
                current_dt =  self.__getdatetime__(dateStr)
                day = current_dt.day
            closeMonth = self.SIMPLE_DATA(close,dataCount,freq,day-1)
            if not np.isnan(closeLast) and closeLast != 0:
                closeMonth = np.append(closeMonth,closeLast)
            return  closeMonth
        
    # 获取季线历史数据
    def GET_CLOSE_DATA_SEASON(self,context,security,isLastest=True,data={},dataCount=20):
        freq = 3
        df_data = ts.get_k_data(security, index=False, ktype='M').tail(dataCount*freq)
        if df_data.empty == True:
            print "security:%s in context:%s NO GET_CLOSE_DATA_SEASON!" %(str(security),str(context))
            return np.array([np.nan])
        closeData = df_data['close'].values
        close = closeData[:-1]
        closeLast = np.nan
        closeSeason = np.array([np.nan])
        if len(closeData) >= freq:
            closeLast = df_data['close'].values[-1]
        else: 
            return closeSeason
        month = 1
        if context and any(context):
            month = context.current_dt.month
        else:
            dateStr = df_data.tail(1)['date'].values[0]
            current_dt =  self.__getdatetime__(dateStr)
            month = current_dt.month
        season = (freq if month % freq == 0 else month % freq)
        closeSeason = self.SIMPLE_DATA(close,dataCount,freq,season-1)
        if not np.isnan(closeLast) and closeLast != 0:
            closeSeason = np.append(closeSeason,closeLast)
        return  closeSeason
    
    #context,security,isLastest=True,data={},dataCount=20
    # 获取年线历史数据
    def GET_CLOSE_DATA_YEAR(self,context,security,isLastest=True,data={},dataCount=20):
        freq = 12
        df_data = ts.get_k_data(security, index=False, ktype='M').tail(dataCount*freq)
        if df_data.empty == True:
            print "security:%s in context:%s NO GET_CLOSE_DATA_YEAR!" %(str(security),str(context))
            return np.array([np.nan])
        closeData = df_data['close'].values
        close = closeData[:-1]
        closeLast = np.nan
        closeYear = np.array([np.nan])
        if len(closeData) >= freq:
            closeLast = df_data['close'].values[-1]
        else: 
            return closeYear
        month = 1
        if context and any(context):
            month = context.current_dt.month
        else:
            dateStr = df_data.tail(1)['date'].values[0]
            current_dt =  self.__getdatetime__(dateStr)
            month = current_dt.month
        closeYear = self.SIMPLE_DATA(close,dataCount,freq,month-1)
        if not np.isnan(closeLast) and closeLast != 0:
            closeYear = np.append(closeYear,closeLast)
        return  closeYear
    
    # 获取季线历史数据最大值
    #context,security,isLastest=True,data={},dataCount=1
    def GET_HIGH_DATA_SEASON(self,context,security,isLastest=True,data={},dataCount=20):
        freq = 3
        df_data = ts.get_k_data(security, index=False, ktype='M').tail(dataCount*freq)
        if df_data.empty == True:
            print "security:%s in context:%s NO GET_HIGH_DATA_SEASON!" %(str(security),str(context))
            return np.array([np.nan])
        highData = df_data['high'].values
        high = highData[:-1]
        highLast = np.nan
        highSeason = np.array([np.nan])
        if len(highData) >= freq:
            pass
        else: 
            return highSeason
        month = 1
        if context and any(context):
            month = context.current_dt.month
        else:
            dateStr = df_data.tail(1)['date'].values[0]
            current_dt =  self.__getdatetime__(dateStr)
            month = current_dt.month
        season = (freq if month % freq == 0 else month % freq)
        highSeason = self.SIMPLE_DATA_HIGH(high,dataCount,freq,season-1)
        highLast = highData[-season:].max()
        if not np.isnan(highLast) and highLast != 0:
            highSeason= np.append(highSeason,highLast)
        return highSeason
    
    # 获取季线历史数据最小值
    #context,security,isLastest=True,data={},dataCount=20
    def GET_LOW_DATA_SEASON(self,context,security,isLastest=True,data={},dataCount=20):
        freq = 3
        df_data = ts.get_k_data(security, index=False, ktype='M').tail(dataCount*freq)
        if df_data.empty == True:
            print "security:%s in context:%s NO GET_LOW_DATA_SEASON!" %(str(security),str(context))
            return np.array([np.nan])
        lowData = df_data['low'].values
        low = lowData[:-1]
        lowLast = np.nan
        lowSeason = np.array([np.nan])
        if len(lowData) >= freq:
            pass
        else: 
            return lowSeason
        month = 1
        if context and any(context):
            month = context.current_dt.month
        else:
            dateStr = df_data.tail(1)['date'].values[0]
            current_dt =  self.__getdatetime__(dateStr)
            month = current_dt.month
        season = (freq if month % freq == 0 else month % freq)
        lowSeason = self.SIMPLE_DATA_LOW(low,dataCount,freq,season-1)
        lowLast = lowData[-season:].min()
        if not np.isnan(lowLast) and lowLast != 0:
            lowSeason= np.append(lowSeason,lowLast)
        return lowSeason
    
    # 获取年线历史数据最大值
    #context,security,isLastest=True,data={},dataCount=20
    def GET_HIGH_DATA_YEAR(self,context,security,isLastest=True,data={},dataCount=20):
        freq = 12
        df_data = ts.get_k_data(security, index=False, ktype='M').tail(dataCount*freq)
        if df_data.empty == True:
            print "security:%s in context:%s NO GET_HIGH_DATA_YEAR!" %(str(security),str(context))
            return np.array([np.nan])
        highData = df_data['high'].values
        high = highData[:-1]
        highLast = np.nan
        highYear = np.array([np.nan])
        if len(highData) >= freq:
            pass
        else: 
            return highYear
        month = 1
        if context and any(context):
            month = context.current_dt.month
        else:
            dateStr = df_data.tail(1)['date'].values[0]
            current_dt =  self.__getdatetime__(dateStr)
            month = current_dt.month
        highYear = self.SIMPLE_DATA_HIGH(high,dataCount,freq,month-1)
        highLast = highData[-month:].max()
        if not np.isnan(highLast) and highLast != 0:
            highYear= np.append(highYear,highLast)
        return highYear
    
    # 获取年线历史数据最小值
    #context,security,isLastest=True,data={},dataCount=20
    def GET_LOW_DATA_YEAR(self,context,security,isLastest=True,data={},dataCount=20):
        freq = 12
        df_data = ts.get_k_data(security, index=False, ktype='M').tail(dataCount*freq)
        if df_data.empty == True:
            print "security:%s in context:%s NO GET_LOW_DATA_YEAR!" %(str(security),str(context))
            return np.array([np.nan])
        lowData = df_data['low'].values
        low = lowData[:-1]
        lowLast = np.nan
        lowYear = np.array([np.nan])
        if len(lowData) >= freq:
            pass
        else: 
            return lowYear
        month = 1
        if context and any(context):
            month = context.current_dt.month
        else:
            dateStr = df_data.tail(1)['date'].values[0]
            current_dt =  self.__getdatetime__(dateStr)
            month = current_dt.month
        lowYear = self.SIMPLE_DATA_LOW(low,dataCount,freq,month-1)
        lowLast = lowData[-month:].min()
        if not np.isnan(lowLast) and lowLast != 0:
            lowYear= np.append(lowYear,lowLast)
        return lowYear
    
    # 获取日线周线月线收盘价历史数据
    def GET_CLOSE_DATA(self, context,security,isLastest=True,data={},dataCount=180*20):
        df_data = ts.get_k_data(security, index=False, ktype='D').tail(dataCount)
        if df_data.empty == True:
            print "security:%s in context:%s NO GET_CLOSE_DATA!" %(str(security),str(context))
            return np.array([np.nan]), np.array([np.nan]),np.array([np.nan])
        closeData = df_data['close'].values
        close = closeData[:-1]
        closeLast = np.nan
        closeMonth = np.nan
        closeWeek = np.nan
        if len(closeData) >= 1:
            closeLast = df_data['close'].values[-1]
        else: 
            return np.array([closeLast]), np.array([closeMonth]), np.array([closeWeek])
        weekday = 1
        day = 1
        if context and any(context):
            weekday = context.current_dt.isoweekday()
            day = context.current_dt.day
        else:
            dateStr = df_data.tail(1)['date'].values[0]
            current_dt =  self.__getdatetime__(dateStr)
            weekday = current_dt.isoweekday()
            day = current_dt.day
        count = dataCount/20
        closeDay = close
        #if len(close) > 180:
        #    closeDay = close[len(close)-180:]
        closeMonth = self.SIMPLE_DATA(close,count,20,day-1)
        closeWeek = self.SIMPLE_DATA(close,count,5,weekday-1)
        if not np.isnan(closeLast) and closeLast != 0:
            closeDay = np.append(closeDay,closeLast)
            closeMonth = np.append(closeMonth,closeLast)
            closeWeek= np.append(closeWeek,closeLast)
        return closeDay, closeMonth, closeWeek

    # 获取当前日线或ref天前成交量
    def GET_VOL_DAY(self, context, security, ref=0 ,data={}):
        dataCount =  ref + 1
        df_data = ts.get_k_data(security, index=False, ktype='D').tail(dataCount)
        if df_data.empty == True:
            print "security:%s in context:%s NO GET_VOL_DAY!" %(str(security),str(context))
            return np.nan
        return df_data['volume'].values[-ref]

    # 获取日线历史成交量
    def GET_VOL_DATA_DAY(self, context, security,isLastest=True,data={},dataCount=20):
        df_data = ts.get_k_data(security, index=False, ktype='D').tail(dataCount)
        if df_data.empty == True:
            print "security:%s in context:%s NO GET_VOL_DATA_DAY!" %(str(security),str(context))
            return np.nan
        return df_data['volume'].values
    
    # overide
    def GET_INDEXO_CRYPTO(self, context, security, period = 'D', data={}):
        df_data = ts.get_k_data(security, index=False, ktype='5')
        if df_data.empty == True:
            print "security:%s in context:%s NO GET_INDEXO_CRYPTO!" %(str(security),str(context))
            return np.nan
        if len(df_data) < 1:
            return np.nan
        dateStr = df_data.tail(1)['date'].values[0]
        current_dt =  self.__getdatetime__(dateStr)
        return super(TsDatasrc, self).GET_INDEXO_CRYPTO(TsContext(current_dt),security)
    
    # overide
    def VOL_PRE(self, context, security, data={}, isFix=True):
        df_data = ts.get_k_data(security, index=False, ktype='5')
        if df_data.empty == True:
            print "security:%s in context:%s NO VOL_PRE!" %(str(security),str(context))
            return np.nan
        if len(df_data) < 1:
            return np.nan
        dateStr = df_data.tail(1)['date'].values[0]
        current_dt =  self.__getdatetime__(dateStr)
        return super(TsDatasrc, self).VOL_PRE(TsContext(current_dt),security)
    
class TsContext(object):
    
    def __init__(self, time):
        self.current_dt = time
        #TODO
        self.run_params = {'start':time,
        'end':None}
        #self.portfolio = None
        
    def updatetime(self, time):
        self.current_dt = time
