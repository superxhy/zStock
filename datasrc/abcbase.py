#!/usr/bin/env python
# -*- coding:utf-8 -*- 
'''
Created on 2017-3-8

@author: yuql
'''
import datetime
import math
import decimal
import talib as tl
import numpy as np
from abc import ABCMeta, abstractmethod

class BRunparams(object):
    runtype = 'notebook'
    runfrequency = 'day'
    def __init__(self):
        self.start_date = None
        self.end_date = None
        self.type = self.runtype
        self.frequency = self.runfrequency
        
class BContext(object):
    timeformat = {
        'd': '%Y-%m-%d',
        'm': '%Y-%m-%d %h:%m:%s'
    }
    
    @classmethod
    def datetime2str(cls, dt, tf='d'):
        return dt.strftime(BContext.timeformat[tf])
    
    @classmethod
    def str2datetime(cls, dtstr, tf='d'):
        return datetime.datetime.strptime(dtstr, BContext.timeformat[tf])
    
    @classmethod
    def obj2datatime(cls, dtobj):
        if isinstance(dtobj, datetime.datetime):
            return dtobj
        elif isinstance(dtobj, str):
            return cls.str2datetime(dtobj)
        elif isinstance(dtobj,(int, long, float)):
            return datetime.datetime.fromtimestamp(dtobj)
        else:
            return dtobj.to_datetime()
        
    @classmethod
    def deltatimeday(cls, dt, offsetday):
        return dt + datetime.timedelta(days = offsetday)
    
    def __repr__(self):
        return "current_dt:%s,start_date:%s,end_date%s,type:%s" %(str(self.current_dt),str(self.run_params.start_date),
            str(self.run_params.end_date),str(self.run_params.type))
    
    #default return today date
    def __init__(self, date=None, count=0):
        self.universe = []
        self.current_dt = None
        self.run_params = BRunparams()
        self.__init_time_range__(date, count)
        #self.portfolio = None
        self.__timeformat__ = ''
        
    def __init_time_range__(self, date, count):
        self.setdaterange(date, count)
        self.run_params.start_date = self.__start_date__
        self.run_params.end_date = self.__end_date__
        self.current_dt = self.__end_date__
        
    def setcurrent_dt(self, date, tf='d'):
        if self.__timeformat__ == '':
            self.current_dt = self.obj2datatime(date)
            self.__timeformat__ = tf
            #print (self.current_dt, tf)
            return self.current_dt
        last_dt = self.obj2datatime(date)
        if self.current_dt < last_dt:
            self.current_dt = last_dt
            self.__timeformat__ = tf
        return self.current_dt
    
    def setdaterange(self, date, count, datastart=None):
        self.count = count
        if date == None:
            self.__end_date__ = datetime.datetime.now()
        else:
            self.__end_date__ = self.obj2datatime(date)
        if datastart==None:
            if count<=0:
                self.__start_date__ = self.__end_date__
            else:
                self.__start_date__ = self.deltatimeday(self.__end_date__, -count)
        else:
            self.__start_date__ = self.obj2datatime(datastart)
                
    def getstartdate(self, isStr=False):
        if isStr:
            return self.datetime2str(self.__start_date__)
        return self.__start_date__
    
    def getenddate(self, isStr=False):
        if isStr:
            return self.datetime2str(self.__end_date__)
        return self.__end_date__
    
    
class SecurityDataSrcBase(object):
    '''
    classdocs
    '''
    __metaclass__ = ABCMeta

    def __init__(self, name):
        self.name = name
        self.data = {}
           
    SINVOKEMETHODS = None
    #lazy mode to save methodsname
    @classmethod
    def getMethodNames(cls):
        if not cls.SINVOKEMETHODS:
            allatr = dir(SecurityDataSrcBase)
            methods = []
            for atr in allatr:
                if atr.find('__')>=0 and atr.rfind('__')>=2:
                    continue
                #<unbound method SecurityDataSrcBase.getVersionName>
                #python3 has all methods in base class...
                #if str(type(getattr(SecurityDataSrcBase, atr))).find('method') == -1:
                #    continue
                if str(atr) == 'getMethodNames':
                    #ignore self
                    continue
                if str(atr) == 'invokeMethod':
                    #ignore invoke
                    continue
                methods.append(str(atr))
                cls.SINVOKEMETHODS = methods
                #print cls.SINVOKEMETHODS
        return cls.SINVOKEMETHODS
    
    def invokeMethod(self, name, *args):
        '''
        getcurrent funname :sys._getframe().f_code.co_name
        '''
        if name not in self.getMethodNames():
            print ("%s not in methods:%s" % (str(name),str(SecurityDataSrcBase.SINVOKEMETHODS)))
            return None
        return getattr(self, name)(*args)
    
    '''
    index function begin ------------------------------------
    '''
    def GET_CONTEXT(self, date=None, count=0):
        return BContext(date, count)
        
    def IS_INNER_CONTEXT(self, context):
        if context == None:
            return self.GET_CONTEXT()
        if context.run_params.type == BRunparams.runtype:
            return context
        return False
    
    @staticmethod
    def GET_RUN_MINUTES(context):
        if context == None:
            return 240
        #9:30-11:30 13:00-15:00
        hour = context.current_dt.hour
        minute = context.current_dt.minute
        #run_hours = 0
        run_minutes = 0
        #before trade return lastest data
        if hour < 9:
            return 240
        if hour == 9 and minute < 25:
            return 0
        if hour < 13:
            run_minutes = (hour-9)*60 + minute - 30
        else:
            run_minutes = (hour-13+2)*60 + minute
        if run_minutes < 0:
            run_minutes = 0
        if run_minutes > 240:
            run_minutes = 240
        #run_hours = run_minutes//60
        #run_half_hours = run_minutes//30
        #run_5_minutes = run_5_minutes//5
        return run_minutes

    #[-1] pretrade
    #[0,10) on call auction
    #[10,15) stable openprice
    #[15,15+240] on trade
    @staticmethod
    def GET_CALLAUCTION_MINUTES(context):
        if context == None:
            return 15+240
        #9:15-9:25
        hour = context.current_dt.hour
        minute = context.current_dt.minute
        #run_hours = 0
        run_minutes = 0
        #before trade return lastest data
        if hour < 9:
            return 15+240
        #reset call auction for pretrade
        if hour == 9 and minute < 15:
            return -1
        if hour < 13:
            run_minutes = (hour-9)*60 + minute - 15
        else:
            run_minutes = (hour-13+2)*60 + minute + 15
        if run_minutes < 0:
            run_minutes = -1
        if run_minutes > 15+240:
            run_minutes = 15+240
        return run_minutes
    
    @staticmethod
    def SIMPLE_DATA(src, count, freq, offset=0):
        des = np.array([])
        for i in range (0,count):
            lenth = len(src)
            index = lenth-1-i*freq-offset
            if index >= 0 and index < lenth: 
                des= np.append(src[index],des)
        return des

    @staticmethod
    def SIMPLE_DATA_HIGH(src, count, freq, offset=0):
        des = np.array([])
        for i in range (0,count):
            lenth = len(src)
            index = lenth-1-i*freq-offset
            if index >= 0 and index < lenth: 
                data_h = src[index]
                for j in range (1,freq):
                    index_j = index - j
                    if index_j >= 0 and index_j < lenth:
                        data = src[index_j] 
                        if data > data_h:
                            data_h = data
                des= np.append(data_h,des)
        return des
    
    @staticmethod
    def SIMPLE_DATA_LOW(src, count, freq, offset=0):
        des = np.array([])
        for i in range (0,count):
            lenth = len(src)
            index = lenth-1-i*freq-offset
            if index >= 0 and index < lenth: 
                data_l = src[index]
                for j in range (1,freq):
                    index_j = index - j
                    if index_j >= 0 and index_j < lenth:
                        data = src[index_j] 
                        if data < data_l:
                            data_l = data
                des= np.append(data_l,des)
        return des
    
    @staticmethod
    def SIMPLE_DATA_SUM(src, count, freq, offset=0):
        des = np.array([])
        for i in range (0,count):
            lenth = len(src)
            index = lenth-1-i*freq-offset
            if index >= 0 and index < lenth:
                data_v = src[index]
                data_s = np.array([data_v])
                for j in range (1,freq):
                    index_j = index - j
                    if index_j >= 0 and index_j < lenth:
                        data = src[index_j] 
                        data_s = np.append(data,data_s)
                des= np.append(np.sum(data_s),des)
        return des
    
    @staticmethod
    def CROSS_LAST_COUNT(src, crossval, crossup=True):
        lenth = len(src)
        if lenth == 0 or np.isnan(src[-1]):
            return 0
        cross = -lenth
        #find cross position
        for i in range(0, lenth):
            index = lenth - 1 - i
            index_ref = index - 1
            if index_ref >= 0 :
                if crossup and src[index_ref] <= crossval and src[index]>crossval:
                    cross = -1 - i
                    break
                if (not crossup) and src[index_ref] >= crossval and src[index]<crossval:
                    cross = -1 - i
                    break
        if cross == -lenth:
            return 0
        return -cross
    
    # SMA
    @staticmethod
    def SMA_CN(close, timeperiod) :
        close = np.nan_to_num(close)
        return reduce(lambda x, y: ((timeperiod - 1) * x + y) / timeperiod, close)
        
    # KDJ
    @staticmethod
    def KDJ_CN(high, low, close, fastk_period=9, slowk_period=3, fastd_period=3) :
        len1 = len(high)
        len2 = len(low)
        len3 = len(close)
        if len1 != len2 or len1 != len3:
            print ("KDJ_CN input invalid for len:%s %s %s " %(str(len1),str(len2),str(len3)))
            return np.array(np.nan),np.array(np.nan),np.array(np.nan)
        kValue, dValue = tl.STOCHF(high, low, close, fastk_period, fastd_period=fastd_period, fastd_matype=0)
        
        kValue = np.array(map(lambda x : SecurityDataSrcBase.SMA_CN(kValue[:x], slowk_period), range(1, len(kValue) + 1)))
        dValue = np.array(map(lambda x : SecurityDataSrcBase.SMA_CN(kValue[:x], fastd_period), range(1, len(kValue) + 1)))
        
        jValue = 3 * kValue - 2 * dValue
        
        func = lambda arr : np.array([0 if x < 0 else (100 if x > 100 else x) for x in arr])
        
        kValue = func(kValue)
        dValue = func(dValue)
        jValue = func(jValue)
        return kValue, dValue, jValue

    @staticmethod
    def HHV_COM(val, period=1, fixpre=False):
        lenval = len(val)
        lenrolling = lenval - period
        if lenrolling < 0:
            return np.array([np.nan])
        resh = np.array([])
        fdropnan = lambda arr: np.array([s for s in arr if not np.isnan(s)])
        fmax = lambda arr: np.nan if len(arr) == 0 else arr.max()
        precount = False
        for i in range(0, period):
            if not fixpre:
                resh = np.append(resh, np.nan)
                continue
            if i < 1:
                resh = np.append(resh, val[i])
                if np.isnan(val[i]):
                    precount = True
                continue
            resh = np.append(resh, fmax(fdropnan(val[:i+1])))
        for i in range(0, lenrolling):
            if precount:
                hhv = val[i+1:period+i+1].max()
                if np.isnan(hhv):
                    hhv = fmax(fdropnan(val[i+1:period+i+1]))
                else:
                    precount = False
            else:
                hhv = val[i+1:period+i+1].max()
            resh = np.append(resh, hhv)
            #resh = np.append(resh, fmax(fdropnan(val[i+1:period+i+1])))
        return resh

    @staticmethod
    def LLV_COM(val, period=1, fixpre=False):
        lenval = len(val)
        lenrolling = lenval - period
        if lenrolling < 0:
            return np.array([np.nan])
        resl = np.array([])
        fdropnan = lambda arr: np.array([s for s in arr if not np.isnan(s)])
        fmin = lambda arr: np.nan if len(arr) == 0 else arr.min()
        precount = False
        for i in range(0, period):
            if not fixpre:
                resl = np.append(resl, np.nan)
                continue
            if i < 1:
                resl = np.append(resl, val[i])
                if np.isnan(val[i]):
                    precount = True
                continue
            resl = np.append(resl, fmin(fdropnan(val[:i+1])))
        for i in range(0, lenrolling):
            if precount:
                llv = val[i+1:period+i+1].min()
                if np.isnan(llv):
                    llv = fmin(fdropnan(val[i+1:period+i+1]))
                else:
                    precount = False
            else:
                llv = val[i+1:period+i+1].min()
            resl = np.append(resl, llv)
            #resl = np.append(resl, fmin(fdropnan(val[i+1:period+i+1])))
        return resl
    
    @staticmethod
    def EMA_COM(val, period=20):
        a = 1.0/(period+1)
        res = np.array([])
        last = np.nan
        for i in range(0, len(val)):
            x = val[i]
            ema = x if np.isnan(last) else (a*x + (1 - a) * last)
            last = x if np.isnan(ema) else ema
            res = np.append(res, ema)
        return res
    
    @staticmethod
    def SMA_COM(val, period=3, weight=1):
        res = np.array([])
        last = np.nan
        for i in range(0, len(val)):
            x = val[i]
            sma = x if np.isnan(last) else (x + (period - weight) * last *1.0) / period
            last = x if np.isnan(sma) else sma
            res = np.append(res, sma)
        return res

    @staticmethod
    def KDJ_COM(high, low, close, fastk_period=9, slowk_period=3, slowd_period=3, fixpre=True) :
        len1 = len(high)
        len2 = len(low)
        len3 = len(close)
        if len1 != len2 or len1 != len3:
            print (("KDJ_COM input invalid for len:%s %s %s " %(str(len1),str(len2),str(len3))))
            return np.array([np.nan]),np.array([np.nan]),np.array([np.nan])
        hValue = SecurityDataSrcBase.HHV_COM(high, fastk_period, fixpre)
        lValue = SecurityDataSrcBase.LLV_COM(low, fastk_period, fixpre)
        a = close - lValue
        b = hValue - lValue
        rsValue = 100* np.divide(a, b, out=np.zeros_like(a), where=b!=0)
        kValue = SecurityDataSrcBase.SMA_COM(rsValue, slowk_period)
        dValue = SecurityDataSrcBase.SMA_COM(kValue,  slowd_period)
        jValue = 3 * kValue - 2 * dValue
        return kValue, dValue, jValue
    
    # RSI COMMON
    @staticmethod
    def RSI_CN_COM(close, timeperiod) :
        diff = map(lambda x, y : x - y, close[1:], close[:-1])
        diffGt0 = map(lambda x : 0 if x < 0 else x, diff)
        diffABS = map(lambda x : abs(x), diff)
        diff = np.array(diff)
        diffGt0 = np.array(diffGt0)
        diffABS = np.array(diffABS)
        diff = np.append(diff[0], diff)
        diffGt0 = np.append(diffGt0[0], diffGt0)
        diffABS = np.append(diffABS[0], diffABS)
        rsi = map(lambda x : SecurityDataSrcBase.SMA_CN(diffGt0[:x], timeperiod) / SecurityDataSrcBase.SMA_CN(diffABS[:x], timeperiod) * 100
                , range(1, len(diffGt0) + 1) )
        
        return np.array(rsi)
    
    # CCI
    @staticmethod
    def CCI_CN(high, low, close, timeperiod=14) :
        len1 = len(high)
        len2 = len(low)
        len3 = len(close)
        if len1 != len2 or len1 != len3:
            print ("CCI_CN input invalid for len:%s %s %s " %(str(len1),str(len2),str(len3)))
            return np.array(np.nan)
        cci = tl.CCI(high, low, close, timeperiod=timeperiod)
        return cci
    
    #MACD
    @staticmethod
    def MACD_CN(close, fastperiod=12, slowperiod=26, signalperiod=9) :
        macdDIFF, macdDEA, macd = tl.MACDEXT(close, fastperiod=fastperiod, fastmatype=1, slowperiod=slowperiod, slowmatype=1, signalperiod=signalperiod, signalmatype=1)
        macd = macd * 2
        return macdDIFF, macdDEA, macd 
    
    @staticmethod
    def STD_CN(close, timeperiod=20, nbdev=1, isDEV=False):
        STDDEV = tl.STDDEV(close, timeperiod=timeperiod, nbdev=nbdev)
        if isDEV :
            return STDDEV
        devfix =  np.sqrt(1.0*timeperiod/(timeperiod-1))
        return devfix * tl.STDDEV(close, timeperiod=timeperiod, nbdev=nbdev)

    @staticmethod
    def BOLL_CN(close,timeperiod=20, nbdev=2, isDEV=False):
        stddev = nbdev
        if not isDEV:
            devfix =  np.sqrt(1.0*timeperiod/(timeperiod-1))
            stddev = nbdev * devfix
        bollUPPER, bollMIDDLE, bollLOWER = tl.BBANDS(
                    #close narray 
                    close, 
                    #time default 20
                    timeperiod=timeperiod,
                    # number of non-biased standard deviations from the mean
                    nbdevup=stddev,
                    nbdevdn=stddev,
                    # Moving average type: simple moving average here
                    matype=0)
        return bollUPPER, bollMIDDLE, bollLOWER
    
    #WR%
    @staticmethod
    def WR_CN(high, low, close, timeperiod=9):
        return -tl.WILLR(high, low, close, timeperiod)
    
    #MAX 
    @staticmethod
    def MAX_CN(close, timeperiod=5):
        return tl.MAX(close, timeperiod)
        
    #MIN
    @staticmethod
    def MIN_CN(close, timeperiod=5):
        return tl.MIN(close, timeperiod)
        
    #RSI
    @staticmethod
    def RSI_CN(close, timeperiod=6):
        return tl.RSI(close, timeperiod)
    
    # MA
    @staticmethod
    def MA_CN(close,timeperiod=5):
        return tl.MA(close, timeperiod, 0)

    @staticmethod
    def calRate(a, b):
        #avoid infinate
        if np.isnan(b) or b == 0:
            return 0
        return float(decimal.Decimal(a/b * 100).quantize(decimal.Decimal('0.00')))
    
    def PERCENT_DAY(self, context, security, data={}, ref=1):
        close = self.GET_CLOSE_DAY(context, security, 0, data)
        if ref==0:
            closeRef = self.GET_OPEN_DAY(context, security, 0)
        else:
            closeRef = self.GET_CLOSE_DAY(context, security,ref)
        if ref==1 and np.isnan(closeRef):
            #issue price higher 120% than openday
            closeRef = self.GET_OPEN_DAY(context, security, 0)*1.0/1.2
            #print ("security:%s no refclose, use issueprice:%s" %(str(security),str(closeRef)))
        return self.calRate(close-closeRef, closeRef), close
    
    def STD_DATA_DAY(self, context, security, data={}, dataCount=1):
        closeDay = self.GET_CLOSE_DATA_DAY(context, security, True, data, dataCount-1+20)
        if np.isnan(closeDay[-1]):
            return np.nan
        return self.STD_CN(closeDay)
    
    def STD_DAY(self, context, security, ref=0, data={}):
        stdDev = self.STD_DATA_DAY(context, security, data, ref+1)
        if np.isnan(stdDev[-1-ref]):
            return np.nan
        return stdDev[-1-ref]
        #dataCount = ref + 20
        #closeDay = GET_CLOSE_DATA_DAY(context, security, True, data, dataCount)
        #if ref==0:
        #    closeDayOffset = closeDay[1:]
        #else:
        #    closeDayOffset = closeDay[1:-ref]
        #print closeDayOffset
        #if isnan(closeDayOffset[-1]):
        #    return np.nan   
        #return np.std(closeDayOffset,ddof = 1)
    
    '''
    UEX:IF(PERIOD>=3 AND MA20>=REF(MA20,1) AND UB>REF(UB,1) AND LB<=REF(LB,1),UB,DRAWNULL),DOTLINE,LINETHICK1,COLORRED;
    USH:IF(PERIOD>=3 AND MA20>=REF(MA20,1) AND UB<=REF(UB,1) AND LB>REF(LB,1),UB,DRAWNULL),DOTLINE,LINETHICK1,COLORGREEN;
    DEX:IF(PERIOD>=3 AND MA20<=REF(MA20,1) AND UB>=REF(UB,1) AND LB<REF(LB,1),LB,DRAWNULL),DOTLINE,LINETHICK1,COLORGREEN;
    DSH:IF(PERIOD>=3 AND MA20<=REF(MA20,1) AND UB<REF(UB,1) AND LB>=REF(LB,1),LB,DRAWNULL),DOTLINE,LINETHICK1,COLORRED;
    '''
    def BOLL_DAY_STATE(self, context, security, data={}):
        RET_UP_START = 3
        RET_UP_KEEP = 2
        RET_UP_END = 1
        RET_DN_START = -3
        RET_DN_KEEP = -2
        RET_DN_END = -1
        ret = 0
        keyprice = 0
        bollUPPER, bollMIDDLE, bollLOWER = self.BOLL_DATA_DAY(context, security, data, 2)
        if len(bollMIDDLE) < 2 or np.isnan(bollMIDDLE[-1]) or np.isnan(bollMIDDLE[-2]):
            return ret, keyprice
        upper = bollUPPER[-1]
        middle = bollMIDDLE[-1]
        lower = bollLOWER[-1]
        upper1 = bollUPPER[-2]
        middle1 = bollMIDDLE[-2]
        lower1 = bollLOWER[-2]
        if middle > middle1:
            if upper > upper1 and lower <= lower1:
                ret = RET_UP_START
            if upper > upper1 and lower >= lower1:
                ret = RET_UP_KEEP
            if upper <= upper1 and lower> lower1:
                ret = RET_UP_END
            keyprice = upper
        else: 
            if lower < lower1 and upper >= upper1:
                ret  = RET_DN_START
            if lower < lower1 and upper <= upper1:
                ret = RET_DN_KEEP
            if lower >= lower1 and upper< upper1:
                ret = RET_DN_END
            keyprice = lower
        return ret, keyprice
    
    def BOLL_DATA_DAY(self, context, security, data={}, dataCount=1):
        closeDay = self.GET_CLOSE_DATA_DAY(context, security, True, data, dataCount-1+20)
        if np.isnan(closeDay[-1]):
            return np.array(closeDay[-1]),np.array(closeDay[-1]),np.array(closeDay[-1])
        return self.BOLL_CN(closeDay)
        
    def BOLL_DAY(self, context, security, ref=0, data={}):
        bollUPPER, bollMIDDLE, bollLOWER = self.BOLL_DATA_DAY(context, security, data, ref+1)
        upper = middle = lower = np.nan
        if not np.isnan(bollMIDDLE[-1]):
            upper = bollUPPER[-1-ref]
            middle = bollMIDDLE[-1-ref]
            lower = bollLOWER[-1-ref]
        return upper,middle,lower
    
    def BOLL_STATE(self, context, security, freq = 30, data={}):
        RET_UP_START = 3
        RET_UP_KEEP = 2
        RET_UP_END = 1
        RET_DN_START = -3
        RET_DN_KEEP = -2
        RET_DN_END = -1
        ret = 0
        wbb = 0
        bb = 0
        bbH = 0
        bbL = 0
        iex = 0
        sex = 0
        kex = 0
        dataCount = 21
        bollUPPER, bollMIDDLE, bollLOWER = np.array([np.nan]),np.array([np.nan]),np.array([np.nan])
        high, low, close = self.GET_PERIOD_DATA(context, security, freq, data, dataCount)
        if not np.isnan(close[-1]):
            bollUPPER, bollMIDDLE, bollLOWER = self.BOLL_CN(close)
        if len(bollMIDDLE) < 2 or np.isnan(bollMIDDLE[-1]) or np.isnan(bollMIDDLE[-2]):
            return ret, wbb, bb, bbH, bbL, sex, kex, iex
        upper = bollUPPER[-1]
        middle = bollMIDDLE[-1]
        lower = bollLOWER[-1]
        upper1 = bollUPPER[-2]
        middle1 = bollMIDDLE[-2]
        lower1 = bollLOWER[-2]
        wbb = (upper - lower)*1.0/middle * 100
        wbb1 = (upper1 -lower1)*1.0/middle1 * 100
        sex = (wbb - wbb1)*1.0/2 * 20
        kex = (middle - middle1)*1.0/middle1*20*100
        bb = (close[-1] - lower)*1.0/(upper - lower)*100
        bbH = (high[-1] - lower)*1.0/(upper - lower)*100
        bbL = (low[-1] - lower)*1.0/(upper - lower)*100
        if middle > middle1:
            iex = kex + sex
            if upper > upper1 and lower <= lower1:
                ret = RET_UP_START
            if upper > upper1 and lower >= lower1:
                ret = RET_UP_KEEP
            if upper <= upper1 and lower> lower1:
                ret = RET_UP_END
        else:
            iex = kex - sex
            if lower < lower1 and upper >= upper1:
                ret  = RET_DN_START
            if lower < lower1 and upper <= upper1:
                ret = RET_DN_KEEP
            if lower >= lower1 and upper< upper1:
                ret = RET_DN_END
        return ret, wbb, bb, bbH, bbL, sex, kex, iex
    
    def WR_DAY(self, context, security, timeperiod=9, ref=0):
        WR = self.WR_DATA_DAY(context,security, timeperiod, ref+1)
        return WR[-1-ref]
    
    def WR_DATA_DAY(self, context, security, timeperiod=9, dataCount=1):
        closeDay = self.GET_CLOSE_DATA_DAY(context, security, True, {}, timeperiod + dataCount - 1)
        highDay = self.GET_HIGH_DATA_DAY(context, security, True, {}, timeperiod + dataCount - 1)
        lowDay = self.GET_LOW_DATA_DAY(context, security, True, {}, timeperiod + dataCount -1)
        if np.isnan(closeDay[-timeperiod]):
            return np.array([np.nan])
        return self.WR_CN(highDay, lowDay, closeDay, timeperiod)
    
    def RSI_DAY(self, context, security, timeperiod=6, data={}, ref=0):
        real = self.RSI_DATA_DAY(context, security, timeperiod, data, ref+1)
        rsi = np.nan
        if not np.isnan(real[-1]):
            rsi = real[-1-ref]
        return rsi
    
    def RSI_DATA_DAY(self, context, security, timeperiod=6, data={}, dataCount=1):
        closeDay = self.GET_CLOSE_DATA_DAY(context, security, True, data, dataCount-1+timeperiod*10)
        if np.isnan(closeDay[-1]):
            return np.array([np.nan])
        return self.RSI_CN(closeDay, timeperiod)
    
    def KDJ_DAY(self, context, security, data={}, ref=0):
        k,d,j = self.KDJ_DATA_DAY(context, security, data, ref+1)
        if np.isnan(k[-1]):
            return np.nan,np.nan,np.nan,
        return k[-1-ref],d[-1-ref],j[-1-ref]

    def KDJ_DATA_DAY(self, context, security, data={}, dataCount=1):
        return self.KDJ_DATA(context, security, 'D',data, dataCount)
    
    #should override to has in row
    def GET_PERIOD_DATA_MIN(self,context, security, data={}, dataCount=1):
        close = self.GET_CLOSE_DATA_MIN(context,security, data, dataCount)
        high = self.GET_HIGH_DATA_MIN(context, security, data, dataCount)
        low = self.GET_LOW_DATA_MIN(context, security, data, dataCount)
        if len(close) == 0 or np.isnan(close[-1]):
            return np.array([np.nan]),np.array([np.nan]),np.array([np.nan])
        len1 = len(close)
        len2 = len(high)
        len3 = len(low)
        if len1 != len2 or len1 != len3:
            print ("%s, GET_PERIOD_DATA_MIN len neq!!!:%s,%s,%s" %(str(security),str(len1),str(len2),str(len3)))
            #print close
            #print high
            #print low
            lenmin = np.array([len1,len2,len3]).min()
            close = close[len1-lenmin:]
            high  =  high[len2-lenmin:]
            low   =   low[len3-lenmin:]
        return high, low ,close
    
    #should override to has in row
    def GET_PERIOD_DATA_DAY(self,context, security, data={}, dataCount=1):
        close = self.GET_CLOSE_DATA_DAY(context, security, True, data, dataCount)
        high = self.GET_HIGH_DATA_DAY(context, security, True, {}, dataCount)
        low = self.GET_LOW_DATA_DAY(context, security, True, {}, dataCount)
        len1 = len(close)
        len2 = len(high)
        len3 = len(low)
        if len1 != len2 or len1 != len3:
            print ("%s, GET_PERIOD_DATA_DAY len neq!!!:%s,%s,%s" %(str(security),str(len1),str(len2),str(len3)))
            #print close
            #print high
            #print low
            lenmin = np.array([len1,len2,len3]).min()
            close = close[len1-lenmin:]
            high  =  high[len2-lenmin:]
            low   =   low[len3-lenmin:]
        return high, low ,close
    
    def GET_CLOSE_DATA_INTRADAY_DA(self, context, security, data, freq, m_close):
        run_minutes = self.GET_RUN_MINUTES(context)
        offset = run_minutes % freq
        intra = (freq-1 if offset == 0 else offset-1)
        closeMin = m_close
        dataCount = len(closeMin)//freq
        closeLast = closeMin[-1]
        if np.isnan(closeLast):
            return np.array([np.nan])
        if run_minutes==240:
            closeLast = self.GET_CLOSE_DAY(context, security, 0, data)
        if run_minutes==0:
            close_intraday = self.SIMPLE_DATA(closeMin, dataCount-1, freq, 0)
            closeLast = self.GET_CLOSE_DAY(context, security, 0, data)
        else:
            close_intraday = self.SIMPLE_DATA(closeMin, dataCount-1, freq, intra+1)
        close_intraday = np.append(close_intraday, closeLast)
        return close_intraday
    
    def GET_HIGH_DATA_INTRADAY_DA(self, context, security, data, freq, m_high):
        run_minutes = self.GET_RUN_MINUTES(context)
        offset = run_minutes % freq
        intra = (freq-1 if offset == 0 else offset-1)
        highMin = m_high
        dataCount = len(highMin)//freq
        highLast = highMin[-1]
        if np.isnan(highLast):
            return np.array([np.nan])
        if run_minutes==240:
            curLast = self.GET_CLOSE_DAY(context, security, 0, data)
            if not np.isnan(curLast) and curLast > highLast:
                highLast = curLast
        if run_minutes==0:
            high_intraday = self.SIMPLE_DATA_HIGH(highMin, dataCount-1, freq, 0)
            highLast = self.GET_CLOSE_DAY(context, security, 0, data)
        else:
            high_intraday = self.SIMPLE_DATA_HIGH(highMin, dataCount-1, freq, intra+1)
            highLastPre = highMin[-intra-1:].max()
            if not np.isnan(highLastPre):
                if highLastPre > highLast:
                    highLast = highLastPre
        high_intraday = np.append(high_intraday, highLast)
        return high_intraday
    
    def GET_LOW_DATA_INTRADAY_DA(self, context, security, data, freq, m_low):
        run_minutes = self.GET_RUN_MINUTES(context)
        offset = run_minutes % freq
        intra = (freq-1 if offset == 0 else offset-1)
        lowMin = m_low
        dataCount = len(lowMin)//freq
        lowLast = lowMin[-1]
        if np.isnan(lowLast):
            return np.array([np.nan])
            lowLast = lowMin[-1]
        if run_minutes==240:
            curLast = self.GET_CLOSE_DAY(context, security, 0, data)
            if not np.isnan(curLast) and curLast < lowLast:
                lowLast = curLast
        if run_minutes==0:
            low_intraday = self.SIMPLE_DATA_LOW(lowMin, dataCount-1, freq, 0)
            lowLast = self.GET_CLOSE_DAY(context, security, 0, data)
        else:
            low_intraday = self.SIMPLE_DATA_LOW(lowMin, dataCount-1, freq, intra+1)
            lowLastPre = lowMin[-intra-1:].min()
            if not np.isnan(lowLastPre):
                if lowLastPre < lowLast:
                    lowLast = lowLastPre
        low_intraday = np.append(low_intraday, lowLast)
        return low_intraday
    
    def GET_VOL_DATA_INTRADAY_DA(self, context, security, data, freq, m_vol):
        run_minutes = self.GET_RUN_MINUTES(context)
        offset = run_minutes % freq
        intra = (freq-1 if offset == 0 else offset-1)
        volMin = m_vol
        dataCount = len(volMin)//freq
        volLast = volMin[-1]
        if np.isnan(volLast):
            return np.array([np.nan])
        if run_minutes==240:
            return self.GET_VOL_DAY(context, security, 0, data)
        if run_minutes==0:
            vol_intraday = self.SIMPLE_DATA_SUM(volMin, dataCount, freq, offset)
        else:
            vol_intraday = self.SIMPLE_DATA_SUM(volMin, dataCount, freq, intra)
            volLast += np.sum(volMin[-intra:])
        vol_intraday = np.append(vol_intraday, volLast)
        return vol_intraday
    
    def GET_CLOSE_DATA_WEEK_DA(self, context,security,isLastest,data,d_close):
        freq = 5
        closeData = d_close
        dataCount = len(closeData)//freq
        closeWeek = np.array([np.nan])
        closeLast = closeData[-1]
        if np.isnan(closeLast):
            return closeWeek
        if len(closeData) <= freq:
            return np.array([closeLast])
        close = closeData[:-1]
        weekday = context.current_dt.isoweekday()
        closeWeek = self.SIMPLE_DATA(close,dataCount-1,freq,weekday-1)
        if not isLastest:
            return closeWeek
        if not np.isnan(closeLast) and closeLast != 0:
            closeWeek= np.append(closeWeek,closeLast)
        return closeWeek
    
    def GET_HIGH_DATA_WEEK_DA(self, context,security,isLastest,data,d_high):
        freq = 5
        highData = d_high
        dataCount = len(highData)//freq
        highWeek = np.array([np.nan])
        highLast = highData[-1]
        if np.isnan(highLast):
            return highWeek
        if len(highData) <= freq:
            highLast = self.SIMPLE_DATA_HIGH(highData,1,freq,0)[-1]
            return np.array([highLast])
        high = highData[:-1]
        weekday = context.current_dt.isoweekday()
        highWeek = self.SIMPLE_DATA_HIGH(high,dataCount-1,freq,weekday-1)
        highLast = highData[-weekday:].max()
        if np.isnan(highLast):
            highLast = self.SIMPLE_DATA_HIGH(highData,1,weekday,0)[-1]
        highWeek= np.append(highWeek,highLast)
        return highWeek
    
    def GET_LOW_DATA_WEEK_DA(self, context,security,isLastest,data,d_low):
        freq = 5
        lowData = d_low
        dataCount = len(lowData)//freq
        lowWeek = np.array([np.nan])
        lowLast = lowData[-1]
        if np.isnan(lowLast):
            return lowWeek
        if len(lowData) <= freq:
            lowLast = self.SIMPLE_DATA_LOW(lowData,1,freq,0)[-1]
            return np.array([lowLast])
        low = lowData[:-1]
        weekday = context.current_dt.isoweekday()
        lowWeek = self.SIMPLE_DATA_LOW(low,dataCount-1,freq,weekday-1)
        lowLast = lowData[-weekday:].min()
        if np.isnan(lowLast):
            lowLast = self.SIMPLE_DATA_LOW(lowData,1,weekday,0)[-1]
        lowWeek= np.append(lowWeek,lowLast)
        return lowWeek
    
    def GET_CLOSE_DATA_MONTH_DA(self, context,security,isLastest,data,d_close):
        freq = 20
        closeData = d_close
        dataCount = len(closeData)//freq
        closeMonth = np.array([np.nan])
        closeLast = closeData[-1]
        if np.isnan(closeLast):
            return closeMonth
        if len(closeData) <= freq:
            return np.array([closeLast])
        close = closeData[:-1]
        day = context.current_dt.day
        closeMonth = self.SIMPLE_DATA(close,dataCount-1,freq,day-1)
        if not isLastest:
            return closeMonth
        if not np.isnan(closeLast) and closeLast != 0:
            closeMonth = np.append(closeMonth,closeLast)
        return closeMonth
    
    def GET_HIGH_DATA_MONTH_DA(self, context,security,isLastest,data,d_high):
        freq = 20
        highData = d_high
        dataCount = len(highData)//freq
        highLast = highData[-1]
        highMonth = np.array([np.nan])
        if np.isnan(highLast):
            return highMonth
        if len(highData) <= freq:
            highLast = self.SIMPLE_DATA_HIGH(highData,1,freq,0)[-1]
            return np.array([highLast])
        high = highData[:-1]
        day = context.current_dt.day
        highMonth = self.SIMPLE_DATA_HIGH(high,dataCount-1,freq,day-1)
        highLast = highData[-day:].max()
        if np.isnan(highLast):
            highLast = self.SIMPLE_DATA_HIGH(highData,1,day,0)[-1]
        highMonth= np.append(highMonth,highLast)
        return highMonth
    
    def GET_LOW_DATA_MONTH_DA(self, context,security,isLastest,data,d_low):
        freq = 20
        lowData = d_low
        dataCount = len(lowData)//freq
        lowLast = lowData[-1]
        lowMonth = np.array([np.nan])
        if np.isnan(lowLast):
            return lowMonth
        if len(lowData) <= freq:
            lowLast = self.SIMPLE_DATA_LOW(lowData,1,freq,0)[-1]
            return np.array([lowLast])
        low = lowData[:-1]
        day = context.current_dt.day
        lowMonth = self.SIMPLE_DATA_LOW(low,dataCount-1,freq,day-1)
        lowLast = lowData[-day:].min()
        if np.isnan(lowLast):
            lowLast = self.SIMPLE_DATA_LOW(lowData,1,day,0)[-1]
        lowMonth= np.append(lowMonth,lowLast)
        return lowMonth
    
    def GET_CLOSE_DATA_SEASON_DA(self,context,security,isLastest,data,d_close):
        freq = 3
        closeData = self.GET_CLOSE_DATA_MONTH_DA(context, security, isLastest, data, d_close)
        dataCount = len(closeData)//freq
        close = closeData[:-1]
        closeLast = np.nan
        if len(closeData) <= freq:
            return np.array([closeData[-1]])
        else: 
            closeLast = closeData[-1]
        month = context.current_dt.month
        season = (freq if month % freq == 0 else month % freq)
        closeSeason = self.SIMPLE_DATA(close,dataCount-1,freq,season-1)
        if not np.isnan(closeLast) and closeLast != 0:
            closeSeason = np.append(closeSeason,closeLast)
        return  closeSeason
    
    def GET_HIGH_DATA_SEASON_DA(self,context,security,isLastest,data,d_high):
        freq = 3
        highData = self.GET_HIGH_DATA_MONTH_DA(context, security, isLastest, data, d_high)
        dataCount = len(highData)//freq
        high = highData[:-1]
        highLast = np.nan
        if len(highData) <= freq:
            highLast = self.SIMPLE_DATA_HIGH(highData,1,freq,0)[-1]
            return np.array([highLast])
        month = context.current_dt.month
        season = (freq if month % freq == 0 else month % freq)
        highSeason = self.SIMPLE_DATA_HIGH(high,dataCount-1,freq,season-1)
        highLast = highData[-season:].max()
        if np.isnan(highLast):
            highLast = self.SIMPLE_DATA_HIGH(highData,1,season,0)[-1]
        highSeason= np.append(highSeason,highLast)
        return highSeason
    
    def GET_LOW_DATA_SEASON_DA(self,context,security,isLastest,data,d_low):
        freq = 3
        lowData = self.GET_LOW_DATA_MONTH_DA(context, security, isLastest, data, d_low)
        dataCount = len(lowData)//freq
        low = lowData[:-1]
        lowLast = np.nan
        if len(lowData) <= freq:
            lowLast = self.SIMPLE_DATA_LOW(lowData,1,freq,0)[-1]
            return np.array([lowLast])
        month = context.current_dt.month
        season = (freq if month % freq == 0 else month % freq)
        lowSeason = self.SIMPLE_DATA_LOW(low,dataCount-1,freq,season-1)
        lowLast = lowData[-season:].min()
        if np.isnan(lowLast):
            lowLast = self.SIMPLE_DATA_LOW(lowData,1,season,0)[-1]
        lowSeason= np.append(lowSeason,lowLast)
        return lowSeason
    
    def GET_CLOSE_DATA_YEAR_DA(self,context,security,isLastest,data,d_close):
        freq = 12
        closeData = self.GET_CLOSE_DATA_MONTH_DA(context, security, isLastest, data, d_close)
        dataCount = len(closeData)//freq
        close = closeData[:-1]
        closeLast = np.nan
        if len(closeData) <= freq:
            return np.array([closeData[-1]])
        else: 
            closeLast = closeData[-1]
        month = context.current_dt.month
        closeYear = self.SIMPLE_DATA(close,dataCount-1,freq,month-1)
        if not np.isnan(closeLast) and closeLast != 0:
            closeYear = np.append(closeYear,closeLast)
        return  closeYear
    
    def GET_HIGH_DATA_YEAR_DA(self,context,security,isLastest,data,d_high):
        freq = 12
        highData = self.GET_HIGH_DATA_MONTH_DA(context, security, isLastest, data, d_high)
        dataCount = len(highData)//freq
        high = highData[:-1]
        highLast = np.nan
        if len(highData) <= freq:
            highLast = self.SIMPLE_DATA_HIGH(highData,1,freq,0)[-1]
            return np.array([highLast])
        month = context.current_dt.month
        highYear = self.SIMPLE_DATA_HIGH(high,dataCount-1,freq,month-1)
        highLast = highData[-month:].max()
        if np.isnan(highLast):
            highLast = self.SIMPLE_DATA_HIGH(highData,1,month,0)[-1]
        highYear= np.append(highYear,highLast)
        return highYear
    
    def GET_LOW_DATA_YEAR_DA(self,context,security,isLastest,data, d_low):
        freq = 12
        lowData = self.GET_LOW_DATA_MONTH_DA(context, security, isLastest, data, d_low)
        dataCount = len(lowData)//freq
        low = lowData[:-1]
        lowLast = np.nan
        if len(lowData) <= freq:
            lowLast = self.SIMPLE_DATA_LOW(lowData,1,freq,0)[-1]
            return np.array([lowLast])
        month = context.current_dt.month
        lowYear = self.SIMPLE_DATA_LOW(low,dataCount-1,freq,month-1)
        lowLast = lowData[-month:].min()
        if np.isnan(lowLast):
            lowLast = self.SIMPLE_DATA_LOW(lowData,1,month,0)[-1]
        lowYear= np.append(lowYear,lowLast)
        return lowYear
    
    def GET_PERIOD_DATA_OLD(self,context, security, freq = 'D', data={}, dataCount=1):
        if freq == 'D':
            close = self.GET_CLOSE_DATA_DAY(context, security, True, data, dataCount)
            high = self.GET_HIGH_DATA_DAY(context, security, True, {}, dataCount)
            low = self.GET_LOW_DATA_DAY(context, security, True, {}, dataCount)
        elif freq == 'W':
            close = self.GET_CLOSE_DATA_WEEK(context,security, True, data, dataCount)
            high = self.GET_HIGH_DATA_WEEK(context,security, True, {}, dataCount)
            low = self.GET_LOW_DATA_WEEK(context,security, True, {}, dataCount)
        elif freq == 'M':
            close = self.GET_CLOSE_DATA_MONTH(context,security, True, data, dataCount)
            high = self.GET_HIGH_DATA_MONTH(context,security, True, {}, dataCount)
            low = self.GET_LOW_DATA_MONTH(context,security, True, {}, dataCount)
        elif freq == 'S':
            close = self.GET_CLOSE_DATA_SEASON(context,security, True, data, dataCount)
            high = self.GET_HIGH_DATA_SEASON(context,security, True, {}, dataCount)
            low = self.GET_LOW_DATA_SEASON(context,security, True, {}, dataCount)
        elif freq == 'Y':
            close = self.GET_CLOSE_DATA_YEAR(context,security, True, data, dataCount)
            high = self.GET_HIGH_DATA_YEAR(context,security, True, {}, dataCount)
            low = self.GET_LOW_DATA_YEAR(context,security, True, {}, dataCount)
        else :
            close = self.GET_CLOSE_DATA_INTRADAY(context,security, data, freq,dataCount)
            high = self.GET_HIGH_DATA_INTRADAY(context, security, data, freq,dataCount)
            low = self.GET_LOW_DATA_INTRADAY(context, security, data, freq,dataCount)
        if len(close) == 0 or np.isnan(close[-1]):
            return np.array([np.nan]),np.array([np.nan]),np.array([np.nan])
        len1 = len(close)
        len2 = len(high)
        len3 = len(low)
        if len1 != len2 or len1 != len3:
            print ("%s,freq:%s GET_PERIOD_DATA len neq!!!:%s,%s,%s" %(str(security),str(freq),str(len1),str(len2),str(len3)))
            #print close
            #print high
            #print low
            lenmin = np.array([len1,len2,len3]).min()
            close = close[len1-lenmin:]
            high  =  high[len2-lenmin:]
            low   =   low[len3-lenmin:]
        return high, low ,close
    
    def GET_PERIOD_DATA(self,context, security, freq = 'D', data={}, dataCount=1):
        close = np.array([np.nan])
        high = np.array([np.nan])
        low = np.array([np.nan])
        if context == None:
            context = self.GET_CONTEXT()
        if freq == 'D':
            high, low, close = self.GET_PERIOD_DATA_DAY(context, security, data, dataCount)
            if len(close) == 0 or np.isnan(close[-1]):
                print ("security:%s in freq:%s NO GET_PERIOD_DATA_DA!" %(str(security),str(freq)))
                return np.array([np.nan]),np.array([np.nan]),np.array([np.nan])
        elif freq == 'W':
            d_high, d_low, d_close = self.GET_PERIOD_DATA_DAY(context, security, data, dataCount*5)
            if len(d_close) == 0 or np.isnan(d_close[-1]):
                print ("security:%s in freq:%s NO GET_PERIOD_DATA_DA!" %(str(security),str(freq)))
                return np.array([np.nan]),np.array([np.nan]),np.array([np.nan])
            close = self.GET_CLOSE_DATA_WEEK_DA(context, security, True, data, d_close)
            high = self.GET_HIGH_DATA_WEEK_DA(context, security, True, data, d_high)
            low = self.GET_LOW_DATA_WEEK_DA(context, security, True, data, d_low)
        elif freq == 'M':
            d_high, d_low, d_close = self.GET_PERIOD_DATA_DAY(context, security, data, dataCount*20)
            if len(d_close) == 0 or np.isnan(d_close[-1]):
                print ("security:%s in freq:%s NO GET_PERIOD_DATA_DA!" %(str(security),str(freq)))
                return np.array([np.nan]),np.array([np.nan]),np.array([np.nan])
            close = self.GET_CLOSE_DATA_MONTH_DA(context, security, True, data, d_close)
            high = self.GET_HIGH_DATA_MONTH_DA(context, security, True, data, d_high)
            low = self.GET_LOW_DATA_MONTH_DA(context, security, True, data, d_low)
        elif freq == 'S':
            d_high, d_low, d_close = self.GET_PERIOD_DATA_DAY(context, security, data, dataCount*3*20)
            if len(d_close) == 0 or np.isnan(d_close[-1]):
                print ("security:%s in freq:%s NO GET_PERIOD_DATA_DA!" %(str(security),str(freq)))
                return np.array([np.nan]),np.array([np.nan]),np.array([np.nan])
            close = self.GET_CLOSE_DATA_SEASON_DA(context, security, True, data, d_close)
            high = self.GET_HIGH_DATA_SEASON_DA(context, security, True, data, d_high)
            low = self.GET_LOW_DATA_SEASON_DA(context, security, True, data, d_low)
        elif freq == 'Y':
            d_high, d_low, d_close = self.GET_PERIOD_DATA_DAY(context, security, data, dataCount*12*20)
            if len(d_close) == 0 or np.isnan(d_close[-1]):
                print ("security:%s in freq:%s NO GET_PERIOD_DATA_DA!" %(str(security),str(freq)))
                return np.array([np.nan]),np.array([np.nan]),np.array([np.nan])
            close = self.GET_CLOSE_DATA_YEAR_DA(context, security, True, data, d_close)
            high = self.GET_HIGH_DATA_YEAR_DA(context, security, True, data, d_high)
            low = self.GET_LOW_DATA_YEAR_DA(context, security, True, data, d_low)
        else :
            get_count = dataCount * freq
            m_high, m_low, m_close = self.GET_PERIOD_DATA_MIN(context, security, data, get_count)
            #print (context)
            if len(m_close) == 0 or np.isnan(m_close[-1]):
                print ("security:%s in freq:%s NO GET_PERIOD_DATA_DA!" %(str(security),str(freq)))
                return np.array([np.nan]),np.array([np.nan]),np.array([np.nan])
            close = self.GET_CLOSE_DATA_INTRADAY_DA(context, security, data, freq, m_close)
            high = self.GET_HIGH_DATA_INTRADAY_DA(context, security, data, freq, m_high)
            low = self.GET_LOW_DATA_INTRADAY_DA(context, security, data, freq, m_low)
        if len(close) == 0 or np.isnan(close[-1]):
            return np.array([np.nan]),np.array([np.nan]),np.array([np.nan])
        len1 = len(close)
        len2 = len(high)
        len3 = len(low)
        #print "%s,freq:%s GET_PERIOD_DATA !!!:%s,%s,%s" %(str(security),str(freq),str(len1),str(len2),str(len3))
        #print close
        #print high
        #print low
        if len1 != len2 or len1 != len3:
            print ("%s,freq:%s GET_PERIOD_DATA len neq!!!:%s,%s,%s" %(str(security),str(freq),str(len1),str(len2),str(len3)))
            #print close
            #print high
            #print low
            lenmin = np.array([len1,len2,len3]).min()
            close = close[len1-lenmin:]
            high  =  high[len2-lenmin:]
            low   =   low[len3-lenmin:]
        if len1 > dataCount:
            print (len1)
            close = close[len1-dataCount:]
            high  =  high[len2-dataCount:]
            low   =   low[len3-dataCount:]
        return high, low ,close
    
    # 获取当前分时收盘价
    def GET_CLOSE_DATA_INTRADAY(self, context, security, data={}, freq=5, dataCount=1):
        run_minutes = self.GET_RUN_MINUTES(context)
        offset = run_minutes % freq
        get_count = dataCount * freq + offset
        m_high, m_low, m_close = self.GET_PERIOD_DATA_MIN(context, security, data, get_count)
        if len(m_close) == 0 or np.isnan(m_close[-1]):
            return np.array([np.nan])
        return self.GET_CLOSE_DATA_INTRADAY_DA(context, security, data, freq, m_close)
    
    # 获取当前分时最高价
    def GET_HIGH_DATA_INTRADAY(self, context, security, data={}, freq=5, dataCount=1):
        run_minutes = self.GET_RUN_MINUTES(context)
        offset = run_minutes % freq
        get_count = dataCount * freq + offset
        m_high, m_low, m_close = self.GET_PERIOD_DATA_MIN(context, security, data, get_count)
        if len(m_high) == 0 or np.isnan(m_high[-1]):
            return np.array([np.nan])
        return self.GET_HIGH_DATA_INTRADAY_DA(context, security, data, freq, m_close)
    
    # 获取当前分时最低价
    def GET_LOW_DATA_INTRADAY(self, context, security, data={}, freq=5, dataCount=1):
        run_minutes = self.GET_RUN_MINUTES(context)
        offset = run_minutes % freq
        get_count = dataCount * freq + offset
        m_high, m_low, m_close = self.GET_PERIOD_DATA_MIN(context, security, data, get_count)
        if len(m_low) == 0 or np.isnan(m_low[-1]):
            return np.array([np.nan])
        return self.GET_LOW_DATA_INTRADAY_DA(context, security, data, freq, m_close)
    
    # 获取当前分时成交量
    def GET_VOL_DATA_INTRADAY(self, context, security, data={}, freq=5, dataCount=1):
        run_minutes = self.GET_RUN_MINUTES(context)
        offset = run_minutes % freq
        get_count = dataCount * freq + offset
        m_high, m_low, m_close, m_vol = self.GET_PERIOD_DATA_MIN(context, security, data, get_count, True)
        if len(m_vol) == 0 or np.isnan(m_vol[-1]):
            return np.array([np.nan])
        return self.GET_VOL_DATA_INTRADAY_DA(context, security, data, freq, m_close)
    
    # 获取周线历史数据
    def GET_CLOSE_DATA_WEEK(self, context,security,isLastest=True,data={},dataCount=20):
        d_close = self.GET_CLOSE_DATA_DAY(context, security, True, data, dataCount*5)
        if len(d_close) == 0 or np.isnan(d_close[-1]):
            return np.array([np.nan])
        return self.GET_CLOSE_DATA_WEEK_DA(context, security, isLastest, data, d_close)
    
    # 获取周线历史数据最大值
    def GET_HIGH_DATA_WEEK(self, context,security,isLastest=True,data={},dataCount=1):
        d_high = self.GET_HIGH_DATA_DAY(context, security, True, data, dataCount*5)
        if len(d_high) == 0 or np.isnan(d_high[-1]):
            return np.array([np.nan])
        return self.GET_HIGH_DATA_WEEK_DA(context, security, isLastest, data, d_high)
    
    # 获取周线历史数据最小值
    def GET_LOW_DATA_WEEK(self, context,security,isLastest=True,data={},dataCount=1):
        d_low = self.GET_LOW_DATA_DAY(context, security, True, data, dataCount*5)
        if len(d_low) == 0 or np.isnan(d_low[-1]):
            return np.array([np.nan])
        return self.GET_LOW_DATA_WEEK_DA(context, security, isLastest, data, d_low)
    
    # 获取月线历史数据
    def GET_CLOSE_DATA_MONTH(self, context,security,isLastest=True,data={},dataCount=1):
        d_close = self.GET_CLOSE_DATA_DAY(context, security, True, data, dataCount*20)
        if len(d_close) == 0 or np.isnan(d_close[-1]):
            return np.array([np.nan])
        return self.GET_CLOSE_DATA_MONTH_DA(context, security, isLastest, data, d_close)
    
    # 获取月线历史数据最大值
    def GET_HIGH_DATA_MONTH(self, context,security,isLastest=True,data={},dataCount=1):
        d_high = self.GET_HIGH_DATA_DAY(context, security, True, data, dataCount*20)
        if len(d_high) == 0 or np.isnan(d_high[-1]):
            return np.array([np.nan])
        return self.GET_HIGH_DATA_MONTH_DA(context, security, isLastest, data, d_high)
    
    # 获取月线历史数据最小值
    def GET_LOW_DATA_MONTH(self, context,security,isLastest=True,data={},dataCount=1):
        d_low = self.GET_LOW_DATA_DAY(context, security, True, data, dataCount*20)
        if len(d_low) == 0 or np.isnan(d_low[-1]):
            return np.array([np.nan])
        return self.GET_LOW_DATA_MONTH_DA(context, security, isLastest, data, d_low)
    
    # 获取季线历史数据
    def GET_CLOSE_DATA_SEASON(self,context,security,isLastest=True,data={},dataCount=1):
        d_close = self.GET_CLOSE_DATA_DAY(context, security, True, data, dataCount*3*20)
        if len(d_close) == 0 or np.isnan(d_close[-1]):
            return np.array([np.nan])
        return self.GET_CLOSE_DATA_SEASON_DA(context, security, isLastest, data, d_close)
    
    # 获取季线历史数据最大值
    def GET_HIGH_DATA_SEASON(self, context,security,isLastest=True,data={},dataCount=1):
        d_high = self.GET_HIGH_DATA_DAY(context, security, True, data, dataCount*3*20)
        if len(d_high) == 0 or np.isnan(d_high[-1]):
            return np.array([np.nan])
        return self.GET_HIGH_DATA_SEASON_DA(context, security, isLastest, data, d_high)
    
    # 获取季线历史数据最小值
    def GET_LOW_DATA_SEASON(self, context,security,isLastest=True,data={},dataCount=1):
        d_low = self.GET_LOW_DATA_DAY(context, security, True, data, dataCount*3*20)
        if len(d_low) == 0 or np.isnan(d_low[-1]):
            return np.array([np.nan])
        return self.GET_LOW_DATA_SEASON_DA(context, security, isLastest, data, d_low)
    
    # 获取年线历史数据
    def GET_CLOSE_DATA_YEAR(self,context,security,isLastest=True,data={},dataCount=20):
        d_close = self.GET_CLOSE_DATA_DAY(context, security, True, data, dataCount*12*20)
        if len(d_close) == 0 or np.isnan(d_close[-1]):
            return np.array([np.nan])
        return self.GET_CLOSE_DATA_YEAR_DA(context, security, isLastest, data, d_close)
    
    # 获取季线历史数据最大值
    def GET_HIGH_DATA_YEAR(self, context,security,isLastest=True,data={},dataCount=1):
        d_high = self.GET_HIGH_DATA_DAY(context, security, True, data, dataCount*12*20)
        if len(d_high) == 0 or np.isnan(d_high[-1]):
            return np.array([np.nan])
        return self.GET_HIGH_DATA_YEAR_DA(context, security, isLastest, data, d_high)
    
    # 获取季线历史数据最小值
    def GET_LOW_DATA_YEAR(self, context,security,isLastest=True,data={},dataCount=1):
        d_low = self.GET_LOW_DATA_DAY(context, security, True, data, dataCount*12*20)
        if len(d_low) == 0 or np.isnan(d_low[-1]):
            return np.array([np.nan])
        return self.GET_LOW_DATA_YEAR_DA(context, security, isLastest, data, d_low)
    
    # 获取当前日线或ref天前收盘价
    def GET_CLOSE_DAY(self, context, security, ref=0 ,data={}):
        dataCount =  ref + 1
        d_close = self.GET_CLOSE_DATA_DAY(context, security, True, data, dataCount)
        if len(d_close) == 0 or np.isnan(d_close[-1]):
            return np.nan
        if len(d_close) < dataCount:
            return np.nan
        return d_close[-1-ref]
    
    def GET_HIGH_DAY(self, context, security, ref=0, data={}):
        dataCount =  ref + 1
        d_high = self.GET_HIGH_DATA_DAY(context, security, True, data, dataCount)
        if len(d_high) == 0 or np.isnan(d_high[-1]):
            return np.nan
        if len(d_high) < dataCount:
            return np.nan
        return d_high[-1-ref]
    
    def GET_LOW_DAY(self, context, security, ref=0, data={}):
        dataCount =  ref + 1
        d_low = self.GET_LOW_DATA_DAY(context, security, True, data, dataCount)
        if len(d_low) == 0 or np.isnan(d_low[-1]):
            return np.nan
        if len(d_low) < dataCount:
            return np.nan
        return d_low[-1-ref]
    
    def GET_VOL_DAY(self, context, security, ref=0, data={}):
        dataCount =  ref + 1
        d_vol = self.GET_VOL_DATA_DAY(context, security, True, data, dataCount)
        if len(d_vol) == 0 or np.isnan(d_vol[-1]):
            return np.nan
        if len(d_vol) < dataCount:
            return np.nan
        return d_vol[-1-ref]
    
    def KDJ_DATA(self, context, security, freq = 'D', data={}, dataCount=1):
        #sma target round2
        precision = 40
        high, low, close = self.GET_PERIOD_DATA(context, security, freq, data, dataCount+precision)
        if np.isnan(close[-1]):
            return np.array([np.nan]),np.array([np.nan]),np.array([np.nan])
        #K_V, D_V, J_V = self.KDJ_CN(high, low, close)
        K_V, D_V, J_V = self.KDJ_COM(high, low, close)
        if len(K_V) > precision:
            K_V = K_V[precision:]
            D_V = D_V[precision:]
            J_V = J_V[precision:]
        else:
            #print "security:%s no len data precison %s" %(str(security), len(K_V))
            pass
        decimal.getcontext().rounding=decimal.ROUND_HALF_UP
        K_V = np.array([float(decimal.Decimal(s).quantize(decimal.Decimal('0.00'))) for s in K_V])
        D_V = np.array([float(decimal.Decimal(s).quantize(decimal.Decimal('0.00'))) for s in D_V])
        J_V = np.array([float(decimal.Decimal(s).quantize(decimal.Decimal('0.00'))) for s in J_V])
        return K_V, D_V, J_V
    
    '''
      @     B     D     F     
      ^  |  ^  |  ^  |  ^  |  
      |  v  |  v  |  v  |  v  
         A     C     E     A  
    period#waveindex:wavechr kd%k/kmaxindex:kmaxchr kmaxkd%kmax|waveseqstr
    exp:
    D#19:C0.46%77.15/17:B7.18%81.96|@ABCD4E3F2A2B2C2
    '''
    def GET_WAVE_CRYPTO(self, context, security, period = 'D', data={}):
        count = 40
        K,D,J= self.KDJ_DATA(context,security, period, data, count)
        KD = K- D
        #print np.array([str(s) for s in KD])
        lenth = len(KD)
        cross = -lenth
        #find cross position
        for i in range(0, lenth):
            index = lenth - 1 - i
            index_ref = index - 1
            if index_ref >= 0 :
                if KD[index_ref] <= 0 and KD[index]>0:
                    cross = -1 - i
                    break
        #calculate waveseq
        waveordStart = ord('A')
        waveord = waveordStart - 1
        waveflag = 1
        waveindex = 1
        kd = KD[cross]
        k = K[cross]
        kmaxindex = waveindex
        kmax = k
        kmaxkd = kd
        kmaxord = waveord
        waveseq = np.array([chr(int(waveord))])
        if cross > -lenth:
            for i in range(cross+1, 0):
                if waveflag > 0 and KD[i] < KD[i-1]:
                    waveflag = -1
                    waveord += 1
                if waveflag < 0 and KD[i] >= KD[i-1]:
                    waveflag = 1
                    waveord += 1
                if waveord > ord('F'):
                    waveord = waveordStart - 1 + waveord - ord('F')
                waveseq = np.append(waveseq, chr(int(waveord)))
                waveindex += 1
                k = K[i]
                kd = KD[i]
                if K[i] > kmax:
                    kmaxindex = waveindex
                    kmax = K[i]
                    kmaxkd = KD[i]
                    kmaxord = waveord
        wavechr = chr(int(waveord))
        kmaxchr = chr(int(kmaxord))
        #format waveseq to str
        waveseqstr = ''
        indexseq = 0
        while (indexseq < len(waveseq)):
            seqdata = waveseq[indexseq]
            waveseqstr = waveseqstr + seqdata
            waveseqnum = 1
            while (indexseq + waveseqnum < len(waveseq) and seqdata == waveseq[indexseq + waveseqnum]):
                waveseqnum += 1
            if waveseqnum > 1:
                waveseqstr = waveseqstr + str(waveseqnum)
            indexseq += waveseqnum
        #period#waveindex:wavechr kd%k/kmaxindex:kmaxchr kmaxkd%kmax|waveseqstr
        waveformat = "%s#%s:%s%s%%%s/%s:%s%s%%%s|%s" %(str(period),str(waveindex),str(wavechr),str(kd),str(k),str(kmaxindex),str(kmaxchr),str(kmaxkd),str(kmax),str(waveseqstr))
        return waveformat
    
    '''
    period#state:inerchr/sex:iex%kex|bb/bbL~bbH%wbb
    '''
    def GET_INERT_CRYPTO(self, context, security, freq = 'D', data={}):
        state, wbb, bb, bbH, bbL, sex, kex, iex = self.BOLL_STATE(context, security, freq, data)
        inerchr = '=='
        if state == 3:
            inerchr = '</'
        if state == 1:
            inerchr = '/>'
        if state == -3:
            inerchr = '<\\'
        if state == -1:
            inerchr = '\>'
        if state == 2:
            if sex >= 0:
                inerchr = '<=/'
            else:
                inerchr = '/=>'
        if state == -2:
            if sex >= 0:
                inerchr = '<=\\'
            else:
                inerchr = '\=>'
        cci = self.CCI_DATA(context, security, freq)[0]
        if cci > 100:
            inerchr += '^'
        if cci < -100:
            inerchr += 'v'
        sex = float(decimal.Decimal(sex).quantize(decimal.Decimal('0.00')))
        iex = float(decimal.Decimal(iex).quantize(decimal.Decimal('0.00')))
        kex = float(decimal.Decimal(kex).quantize(decimal.Decimal('0.00')))
        bb = float(decimal.Decimal(bb).quantize(decimal.Decimal('0.00')))
        bbL = float(decimal.Decimal(bbL).quantize(decimal.Decimal('0.00')))
        bbH = float(decimal.Decimal(bbH).quantize(decimal.Decimal('0.00')))
        wbb = float(decimal.Decimal(wbb).quantize(decimal.Decimal('0.00')))
        inerformat = "%s#%s:%s%s/%s%%%s|%s/%s~%s%%%s" %(str(freq),str(state),str(inerchr),str(sex),str(iex),str(kex),str(bb),str(bbL),str(bbH),str(wbb))
        return inerformat
    
    '''
                ( 天 )              
      ( 泽 )      ≡       ( 风 )    
            ⌋     |      ⌈          
            |     |     |           
  ( 火 ) ψ ———————|———————— § ( 水 ) 
            |     |     |           
            ⌊     |     ⌉            
      ( 雷 )      ±      ( 山 )      
                ( 地 )               
                
    ≡     ±     ⌈     ⌊     §    ψ    ⌉     ⌋
    天    地    风    雷    水    火   山    泽
    乾    坤    巽    震    坎    離   艮    兌
   +++   ---   ++-   __+   -+-  +-+  +--   _++  
    左放转上，右缩转下
    右放转左，左缩转右
    木性(雷风)转位为两格，变盘关键转折如:
    雷阴 或者 雷+水阳 可转泽位 火阳位 易长红
    风阳 或者 风+火阴 可转山位 水阴位 易长黑
    
    period#volyinyang/volbody|avgRate%volPreStr:volmk volRate~volBB%volBand
    cryptomk 
    cryptoel
    exp:
    P#-94.05/0.79|3.5%2.75E+8:(ψ’^) 118.27~100.0%51.41
    ψ‘.§‘v.ψ’^.§’.(ψ’^) 
    火陽.水陽v.火陰^.水陰.(火陰^)
    卦象:
    当天#近光脚/0.79百分点幅程|3.5百分点偏离均价2.75亿空方:火阴量(5天内最大) 比昨天1.18倍放量~8天内量能宽度顶部%8天内量能宽度为51个点
    5天内乾坤量为
    火阳.水阳'背离低吸'.火阴'背离高抛'.水阴.火阴'背离高抛'
    '''
    def GET_VOL_CRYPTO(self, context, security, period = 'D', data={}):
        trigrams421 = [
            {'mark':'±','element':'地','name':'坤'},#000
            {'mark':'⌊','element':'雷','name':'震'},#001
            {'mark':'§','element':'水','name':'坎'},#010
            {'mark':'⌋','element':'澤','name':'兌'},#011
            {'mark':'⌉','element':'山','name':'艮'},#100
            {'mark':'ψ','element':'火','name':'離'},#101
            {'mark':'⌈','element':'風','name':'巽'},#110
            {'mark':'≡','element':'天','name':'乾'},#111
                       ]
        yinmark = '’'
        yinelement = '陰'
        yangmark = '‘'
        yangelement = '陽'
        yindepart = 'v'
        yangdepart = '^'
        #量能缩放组合编码
        def comp(volarr):
            bcd = []
            lenth = len(volarr)
            if lenth < 2:
                return bcd
            for i in range(1, lenth):
                if volarr[i] > volarr[i-1]:
                    bcd.append('1')
                else:
                    bcd.append('0')
            bcdstr = ''.join(bcd)
            return int(bcdstr, 2)
        #量能行程多空编码
        def yinyang(karr):
            if len(karr) < 3:
                return -1
            high = karr[0]
            low = karr[1]
            close = karr[2]
            mid = (high + low)*1.0/2
            route = (high - low)*1.0/2
            res = 0
            if (route > 0):
                res = (close-mid)/route
            return float(decimal.Decimal(res * 100).quantize(decimal.Decimal('0.00')))
        
        #量能转化均衡算法
        def chipExchange(varr5,varr10):
            #放量界点权值
            qtbegin = 100
            #界点权值步长
            qtrate = 10
            sumarr = 0
            lenarr = min(np.array([len(varr5),len(varr10)]))
            for i in range(0, lenarr):
                sumarr += varr5[i] * 100.0/qtbegin + varr10[i] * 100.0/qtbegin
                if qtbegin > qtrate:
                    qtbegin -= qtrate
            return calRate(sumarr, lenarr*200)
        
        def chipExchangeStab(varr5Rel,varr10Rel):
            #稳定转化缩量天数
            suffocate = 2
            stab5 = calRate(varr5Rel[0] - np.array(varr5Rel[1:suffocate]).mean()*suffocate/2, varr5Rel[0])
            stab10 = calRate(varr10Rel[0] - np.array(varr10Rel[1:suffocate]).mean()*suffocate/2, varr10Rel[0])
            return float(decimal.Decimal(stab5 + stab10).quantize(decimal.Decimal('0.00')))
        
        def calRate(a, b):
            #avoid infinate
            if np.isnan(b) or b == 0:
                return 0
            return float(decimal.Decimal(a/b * 100).quantize(decimal.Decimal('0.00')))
        
        DATACAL = 4
        DATALEN = 8
        DATACOUNT = DATACAL + (DATALEN -1)
        volData = self.GET_VOL_DATA_DAY(context, security,True,data,DATACOUNT)
        #volLast = volData[-1]
        volRef = 0
        #volRate = 0
        volmk =''
        volyinyang = 0
        volbody = 0
        volPre = self.VOL_PRE(context, security, data, True)
        if len(volData) > 1 :
            volRef = volData[-2]
        volRate = calRate(volPre, volRef)
        volPreStr = decimal.Context(prec=3, rounding=decimal.ROUND_DOWN).create_decimal(volPre)
        #print volPreStr
        volDataPre = np.append(volData[:-1],volPre)
        volPre5 = volDataPre[-5-1:-5+DATACAL-1]
        volPre10 = volDataPre[-10-1:-10+DATACAL-1]
        volPre5Rate = [calRate(volPre-s, s) for s in volPre5]
        volPre10Rate =[calRate(volPre-s, s) for s in volPre10]
        volPreEx = chipExchange(volPre5Rate, volPre10Rate)
        volPreStable = chipExchangeStab(volPre5, volPre10)
        #max point
        volMax = volDataPre.max()
        volMaxIndex = np.where(volDataPre==volMax)[0][0]
        volMaxOffset = len(volDataPre) -1 - volMaxIndex
        #min point 
        volMin = volDataPre.min()
        volMinIndex = np.where(volDataPre==volMin)[0][0]
        volMinOffset = len(volDataPre) -1 - volMinIndex
        #band
        volBand = calRate(volMax - volMin, volMin)
        volBB = calRate(volPre -volMin, volMax - volMin)
        volArray = []
        for i in range(0, DATALEN):
            lenth = len(volDataPre)
            index = lenth-1-(DATACAL-1) - i
            des = np.array([])
            if index >= 0 and index < lenth:
                if np.isnan(volDataPre[index]):
                    break
                des= volDataPre[index:index+DATACAL]
            if len(des) < DATACAL:
                break
            volArray.insert(0, des)
            
        cryptoindex = [comp(s) for s in volArray]
        cryptomk = [trigrams421[x]['mark'] for x in cryptoindex]
        cryptoel = [trigrams421[x]['element'] for x in cryptoindex]
        #cryptomkMax = cryptomk[0] if volMaxOffset > len(cryptomk) else cryptomk[-1-volMaxOffset]
        #cryptoelMax = cryptoel[0] if volMaxOffset > len(cryptoel) else cryptoel[-1-volMaxOffset]
        #yin yang
        high, low, close = self.GET_PERIOD_DATA(context, security, 'D', data, DATALEN)
        avgData = self.GET_AVG_DATA_DAY(context, security, 1, data)
        avg = avgData[-1] if len(avgData) >0 else 0
        closeLast = close[-1] if len(close) >0 else 0
        avgRate = calRate(closeLast-avg, avg)
        #print avgRate
        kArray = []
        for i in range(0, len(close)):
            kdata = [high[i],low[i],close[i]]
            kArray.append(kdata)
        yy = [yinyang(s) for s in kArray]
        yymk = [yinmark if(x < 0) else yangmark for x in yy]
        yyel = [yinelement if(x < 0) else yangelement for x in yy]
        for i in range(0,len(cryptomk)):
            if len(yymk)-1-i >= 0:
                cryptomk[-1-i] +=  yymk[-1-i]
                cryptoel[-1-i] +=  yyel[-1-i]
            if cryptoindex[-1-i] % 2 == 0 and yy[-1-i] >= 0:
                cryptomk[-1-i]+= yindepart
                cryptoel[-1-i]+= yindepart
            if cryptoindex[-1-i] % 2 == 1 and yy[-1-i] < 0:
                cryptomk[-1-i]+= yangdepart
                cryptoel[-1-i]+= yangdepart
        if len(cryptomk) - volMaxOffset >0 :
            cryptomk[-1-volMaxOffset] = '('+ cryptomk[-1-volMaxOffset]+')'
            cryptoel[-1-volMaxOffset] = '('+ cryptoel[-1-volMaxOffset]+')'
        if len(cryptomk) - volMinOffset >0 :
            cryptomk[-1-volMinOffset] = '['+ cryptomk[-1-volMinOffset]+']'
            cryptoel[-1-volMinOffset] = '['+ cryptoel[-1-volMinOffset]+']'
        if len(cryptomk) > 0:
            volmk = cryptomk[-1]
        if len(yy) > 0:
            volyinyang = yy[-1]
        if len(kArray) >0:
            volbody = calRate(kArray[-1][0] - kArray[-1][1],kArray[-1][1])
        volformat = "P#%s/%s|%s%%%s:%s %s~%s%%%s" %(str(volyinyang),str(volbody),str(avgRate),str(volPreStr),str(volmk),str(volRate),str(volBB),str(volBand))
        #print volformat
        return [volformat,'. '.join(cryptomk),'. '.join(cryptoel),[volPre10Rate, volPre5Rate],[volPreEx, volPreStable]]
    
    '''
    ≡     ±     ⌈     ⌊     §    ψ    ⌉     ⌋
    天    地    风    雷    水    火   山    泽
    乾    坤    巽    震    坎    離   艮    兌
   三红  三黑  红红黑 黑黑红 黑红黑 红黑红 红黑黑 黑红红
   三高  三低  震荡高 震荡低 反覆低 反覆高 瞬间高 瞬间低
   
    三高:多方气势强盛，伴随量增一般收中长红，标准低点高点逐高，一盘低点破掉会转弱
    三低:空方气势强盛，伴随量增一般收中长黑，标准低点高点逐低，一盘高点破掉会转强
    震荡高:多方稳步推升，一般收小红，盘中有两波以上的波动（两个高点，两个低点），标准两波半， 上下上下上，一盘低点破掉会转弱
    震荡低:空方稳步压制，一般收小黑，盘中有两波以上的波动（两个低点，两个高点），标准两波半， 下上下上下，一盘高点破掉会转强
    反覆低:多空反复，空方略占，一般收小黑小红，一盘低点破掉会转弱
    反覆高:多空反复，多方略占，一般收小黑小红，一盘高点破掉会转强
    瞬间高:多方最后一击后被空方反击，反而会中长黑，一盘高点破掉会转强
    瞬间低:空方最后一击后被多方反击，反而会中长红，一盘低点破掉会转弱
    O#idxRate%idxBand/idx1volStr:idxmk idxel
    idxK
    idxbody
    idxMax,idxMin
    '''
    def GET_INDEXO_CRYPTO(self, context, security, period = 'D', data={}):
        trigrams421 = [
            {'mark':'±','element':'三低','name':'坤'},#000
            {'mark':'⌊','element':'震荡低','name':'震'},#001
            {'mark':'§','element':'反覆低','name':'坎'},#010
            {'mark':'⌋','element':'瞬间低','name':'兌'},#011
            {'mark':'⌉','element':'瞬间高','name':'艮'},#100
            {'mark':'ψ','element':'反覆高','name':'離'},#101
            {'mark':'⌈','element':'震荡高','name':'巽'},#110
            {'mark':'≡','element':'三高','name':'乾'},#111
                       ]
        yinmark = '’'
        yangmark = '‘'
        #三盘组合编码
        def compk(karr):
            bcd = []
            lenth = len(karr)
            if lenth < 3:
                return -1
            for i in range(0, lenth):
                high = karr[i][0]
                low = karr[i][1]
                close = karr[i][2]
                open = karr[i][3]
                if close > open:
                    bcd.append('1')
                else:
                    bcd.append('0')
            bcdstr = ''.join(bcd)
            return int(bcdstr, 2)
        
        freq = 5 
        panCount = 0
        runTime = self.GET_RUN_MINUTES(context)
        if runTime == 0 :
            panCount = 1
            #计算集合竞价开盘数值
            openday = self.GET_CLOSE_DAY(context,security, 1)
        else:
            if  not security in self.GET_ALL_INDEXES():
                #开盘八法只适用于指数
                return None
            panCount = runTime//freq 
            if runTime % freq != 0:
                panCount +=1
            openday = self.GET_OPEN_DAY(context, security)
        DATACAL = 3
        DATALEN = panCount
        #yin yang
        high, low, close = self.GET_PERIOD_DATA(context, security, freq, data, DATALEN)
        vol = self.GET_VOL_DATA_INTRADAY(context, security, data, freq, DATALEN)
        idxV = vol[-panCount:-(panCount-DATACAL)] if panCount > DATACAL else vol[-panCount:]
        idxC = close[-panCount:-(panCount-DATACAL)] if panCount > DATACAL else close[-panCount:]
        idxH = high[-panCount:-(panCount-DATACAL)] if panCount > DATACAL else high[-panCount:]
        idxL = low[-panCount:-(panCount-DATACAL)] if panCount > DATACAL else low[-panCount:]
        idxO = np.array([openday])
        idxlen = len(idxC)
        for i in range(0,idxlen-1):
            idxO = np.append(idxO, idxC[i])
        idxMax = idxH.max()
        idxMaxIndex = np.where(idxH==idxMax)[0][0]
        idxMin = idxL.min()
        idxMinIndex = np.where(idxL==idxMin)[0][0]
        idxBand = idxMax - idxMin
        if idxBand > 0:
            idxRate = (close[-1]-idxMin)/idxBand * 100
        else:
            #开盘无波动范围，使用相对昨天值
            idxRate = (close[-1]-openday)/openday * 100
        idxRateStr = decimal.Context(prec=3, rounding=decimal.ROUND_DOWN).create_decimal(idxRate)
        dataJj = self.data.get(security,None)
        if dataJj:
            print ("get idx dataJj:" %(str(dataJj['volume'])))
            idxV[0] += dataJj['volume']
        idx1volStr = decimal.Context(prec=3, rounding=decimal.ROUND_DOWN).create_decimal(idxV[0])
        kArray = []
        for i in range(0, idxlen):
            kdata = [idxH[i],idxL[i],idxC[i],idxO[i]]
            kArray.append(kdata)
        funKinc = lambda x:float(decimal.Decimal(x[2]-x[3]).quantize(decimal.Decimal('0.00')))
        funKvib = lambda x:float(decimal.Decimal(np.array(x).max()-np.array(x).min()).quantize(decimal.Decimal('0.00')))
        idxK = [funKinc(s) for s in kArray]
        idxBody = [funKvib(s) for s in kArray]
        yymk = [yinmark if(x < 0) else yangmark for x in idxK]
        idxid = compk(kArray)
        if idxid < 0:
            idxmk = '-'
            idxel = '-'
        else:
            idxmk = trigrams421[compk(kArray)]['mark']
            idxel = trigrams421[compk(kArray)]['element']
        for i in range(0,idxlen):
            idxBody[i] = str(idxBody[i]) + yymk[i]
            if i in [idxMaxIndex,idxMinIndex]:
                if i == idxMaxIndex:
                    idxK[idxMaxIndex] = '('+str(idxK[idxMaxIndex])+')'
                if i == idxMinIndex:
                    idxK[idxMinIndex] = '['+str(idxK[idxMinIndex])+']'
            else:
                idxK[i] = str(idxK[i])
        idxformat = "O#%s%%%s/%s:%s %s" %(str(idxRateStr),str(idxBand),str(idx1volStr),str(idxmk),str(idxel))
        #print idxformat
        return [idxformat,str(','.join(idxK)), str(','.join(idxBody)),[str(idxMax), str(idxMin)]]
    
    '''
    ['code','name','industry','close','per','wave','inert','vol']
    '''
    def GET_BUNDLE(self, context, security, pulldata=False, data={}):
        per, close = self.PERCENT_DAY(context, security, data)
        code = security.split('.')[0]
        info = self.GET_SECURITY_INFO(security, context)
        name = info['name']
        if per >= 20:
            name = 'N'+ str(name)
        industry = info['industry']
        bundle = {
        'code':code,
        'name':name,
        'industry':industry,
        'close':close,
        'per':per}
        #TODO pulldata
        #if not pulldata:
        #    return bundle
        auction_minutes = self.GET_CALLAUCTION_MINUTES(context)
        #ignore crypto for pretrade
        if auction_minutes < 15 or (not security in self.GET_ALL_INDEXES()):
            return bundle
        wave = [
        self.GET_WAVE_CRYPTO(context, security, 30),
        self.GET_WAVE_CRYPTO(context, security, 'D'), 
        self.GET_WAVE_CRYPTO(context, security, 'W')]
        #add wave more for aftertrade
        if auction_minutes == 15+240:
            wavemore = [
            self.GET_WAVE_CRYPTO(context, security, 'M'),
            self.GET_WAVE_CRYPTO(context, security, 'S'),
            self.GET_WAVE_CRYPTO(context, security, 'Y')]
            wave = wave + wavemore
        inert = [
        self.GET_INERT_CRYPTO(context, security, 30),
        self.GET_INERT_CRYPTO(context, security, 'D'),
        self.GET_INERT_CRYPTO(context, security, 'W')]
        bundle['wave'] = wave
        bundle['inert'] = inert
        bundle['vol'] = self.GET_VOL_CRYPTO(context, security,'D',data)
        #add idxopen first 3bar
        #if auction_minutes <= 15+15:
        idx = self.GET_INDEXO_CRYPTO(context, security,'D',data)
        if idx :
            bundle['bidx'] =  idx
            print (str(bundle))
        return bundle
    
    def CCI_DAY(self, context, security, data={}, ref=0):
        CCI = self.CCI_DATA_DAY(context, security, data, ref+1)
        if np.isnan(CCI[-1]):
            return 0
        return CCI[-1-ref]

    def CCI_DATA_DAY(self, context, security, data={}, dataCount=1):
        return self.CCI_DATA(context, security, 'D',data, dataCount)
    
    def CCI_DATA(self, context, security, freq = 'D', data={}, dataCount=1):
        #sma target round2
        precision = 14
        high, low, close = self.GET_PERIOD_DATA(context, security, freq, data, dataCount+precision)
        if np.isnan(close[-1]):
            return np.array([np.nan])
        CCI = self.CCI_CN(high, low, close)
        if len(CCI) > precision:
            CCI = CCI[-dataCount:]
        else:
            #print "security:%s no len data precison %s" %(str(security), len(CCI))
            pass
        decimal.getcontext().rounding=decimal.ROUND_HALF_UP
        CCI = np.array([float(decimal.Decimal(s).quantize(decimal.Decimal('0.00'))) for s in CCI])
        return CCI
    
    def MA_N_DAY(self, context, security, n=5, ref=0, data={}):
        MA_N = self.MA_N_DATA_DAY(context, security, n, data, ref+1)
        if not np.isnan(MA_N[-1]):
            return MA_N[-1-ref]
        return 0
    
    def MA_N_DATA_DAY(self, context, security, n=5, data={}, dataCount=1):
        closeDay = self.GET_CLOSE_DATA_DAY(context, security, True, data, n + dataCount - 1)
        if np.isnan(closeDay[-1]) or len(closeDay) == 0:
            return np.array([np.nan])
        return self.MA_CN(closeDay,n)
   
    def MAVOL_N_DAY(self, context, security, n=5, ref=0, data={}):
        MAVOL_N = self.MAVOL_N_DATA_DAY(context, security, n, data, ref+1)
        if not np.isnan(MAVOL_N[-1]):
            return MAVOL_N[-1-ref]
        return 0
    
    def MAVOL_N_DATA_DAY(self, context, security, n=5, data={}, dataCount=1):        
        volumeDay = self.GET_VOL_DATA_DAY(context, security, True, data, n + dataCount - 1)
        if np.isnan(volumeDay[-1]):
            return np.array(np.nan)
        return self.MA_CN(volumeDay,n)
    
    '''
    TOTAL:=IF(PERIOD=1,5,IF(PERIOD=2,15,IF(PERIOD=3,30,IF(PERIOD=4,60,IF(PERIOD=5,TOTALFZNUM,1)))));
    MTIME:=MOD(FROMOPEN,TOTAL);
    CTIME:=IF(MTIME<0.5,TOTAL,MTIME);
    TIME60VALUE := 1.5;
    TIME210VALUE := 1.001;
    A:=POW(TIME60VALUE - 1.0, 1.4) * POW(TIME210VALUE - 1.0, -0.4);
    B:=LOG((TIME60VALUE - 1.0) / (TIME210VALUE - 1.0)) / 150;
    DIV:=A * POW(10, -B*FROMOPEN) + 1;
    VVOL:IF(1,VOL*TOTAL/CTIME,DRAWNULL),NODRAW;
    STICKLINE((CURRBARSCOUNT=1 AND DYNAINFO(8)>1),VVOL/DIV,0,-1,-1),COLOR00C0C0;
    VOLUME:VOL,VOLSTICK;
    MAVOL1:MA(VOLUME,M1);
    MAVOL2:MA(VOLUME,M2);
    MAVOL3:MA(VOLUME,M3);
    PREDICT: VVOL/DIV;
    SC:(LOG(VVOL/DIV/MA(VOL,20))+1) * 50;
    '''
    
    def VOL_PRE(self, context, security, data={}, isFix=True):
        volumLast = self.GET_VOL_DAY(context, security, 0 , data)
        if volumLast==0:
            return 0
        run_minutes = self.GET_RUN_MINUTES(context)
        alltime = 240
        jjtimes = 1
        if run_minutes==alltime:
            return volumLast
        if run_minutes==0:
            volumPre = volumLast * 1.0 * alltime / jjtimes
        else:
            volumPre = volumLast * 1.0 * alltime / run_minutes
        '''
        9:30 4.15 ,9:45 2.99 , 10:00 2.25 ,10:30 (1.5) , 2:00 (1.01) , 2:30 (1.005)  
        '''
        def fix_times(time, t60=1.5, t210=1.005):
            if time == 0:
                return math.exp(1.0)
            fparam1 = lambda t60, t210: math.log((t60 - 1.0) / (t210 - 1.0)) / math.log(10) / 150
            fparam2 = lambda t60, t210: math.pow(t60 - 1.0, 1.4) * math.pow(t210 - 1.0, -0.4)
            return fparam2(t60, t210) * math.pow(10, -fparam1(t60, t210)*time) + 1
        if isFix:
            volumPre = volumPre/fix_times(run_minutes)
        return volumPre

    '''
    {VOL 100X=150 10X=100 2X=65 0.1X=0 0.5X=35}
    '''
    def VOL_PV(self, context, security, n=20, data={}, isFix=True):
        volumePre = self.VOL_PRE(context, security, data, isFix)
        volumeMa = self.MAVOL_N_DAY(context, security, n, 1, data)
        if volumePre==0 or volumeMa==0:
            return 0
        return  (1 + math.log(volumePre / volumeMa)/math.log(10))*50
    
    # 获取日线成交均价
    def GET_AVG_DATA_DAY(self, context, security, n=20, data={}):
        #TODO calcate index avg
        if security in self.GET_ALL_INDEXES():
            return np.array([np.nan])
        volData = self.GET_VOL_DATA_DAY(context, security, True, data, n)
        amountData = self.GET_AMOUNT_DATA_DAY(context, security, True, data, n)
        avgData = np.array([])
        for i in range(0, len(volData)):
            vol = volData[-1-i]
            amount = amountData[-1-i]
            if np.isnan(amount) or amount==0:
                avgData = np.append(np.nan, avgData)
            else:
                avgData = np.append(0.01*amount/vol, avgData)
        return avgData
    
    '''
    index function end   ------------------------------------
    '''
    @abstractmethod
    def getVersionName(self):
        pass
    
    @abstractmethod
    def getDataSrcName(self):
        pass
    '''
    data function begin ------------------------------------
    '''
    # 获取所有指数代码
    @abstractmethod
    #return list
    def GET_ALL_INDEXES(self):
        pass
    
    # 获取所有股票代码
    @abstractmethod
    #return list
    #filtPaused=True, filtSt=True, filtMarketcap=0
    def GET_ALL_SECURITIES(self):
        pass
    
    # 获取股票信息
    @abstractmethod
    #security, context=None
    def GET_SECURITY_INFO(self):
        pass
    
    # 获取当前分时收盘价
    #@abstractmethod
    #context, security, data={}, freq=5, dataCount=1
    #def GET_CLOSE_DATA_INTRADAY(self):
    #    pass
    
    # 获取当前分时最高价
    #@abstractmethod
    #context, security, data={}, freq=5, dataCount=1
    #def GET_HIGH_DATA_INTRADAY(self):
    #    pass
    
    # 获取当前分时最低价
    #@abstractmethod
    #context, security, data={}, freq=5, dataCount=1
    #def GET_LOW_DATA_INTRADAY(self):
    #    pass
    
    # 获取当前分时成交量
    #@abstractmethod
    #context, security, data={}, freq=5, dataCount=1
    #def GET_VOL_DATA_INTRADAY(self):
    #    pass
    
    #@abstractmethod
    #context, security, ref=0
    #def GET_HIGH_DAY(self):
    #    pass
            
    #@abstractmethod
    #context, security, ref=0
    #def GET_LOW_DAY(self):
    #    pass
            
    @abstractmethod
    #context, security, ref=0
    def GET_OPEN_DAY(self):
        pass
    
    # 获取日线历史数据最大值
    @abstractmethod
    #context,security,isLastest=True,data={},dataCount=1
    def GET_HIGH_DATA_DAY(self):
        pass
    
    # 获取日线历史数据最小值
    @abstractmethod
    #context,security,isLastest=True,data={},dataCount=1
    def GET_LOW_DATA_DAY(self):
        pass

    # 获取周线历史数据最大值
    #@abstractmethod
    #context,security,isLastest=True,data={},dataCount=1
    #def GET_HIGH_DATA_WEEK(self):
    #    pass
    
    # 获取周线历史数据最小值
    #@abstractmethod
    #context,security,isLastest=True,data={},dataCount=1
    #def GET_LOW_DATA_WEEK(self):
    #    pass
    
    # 获取月线历史数据最大值
    #@abstractmethod
    #context,security,isLastest=True,data={},dataCount=1
    #def GET_HIGH_DATA_MONTH(self):
    #    pass
    
    # 获取月线历史数据最小值
    #@abstractmethod
    #context,security,isLastest=True,data={},dataCount=1
    #def GET_LOW_DATA_MONTH(self):
    #    pass
    
    # 获取当前日线或ref天前收盘价
    #@abstractmethod
    #context,security, ref=0 ,data={}
    #def GET_CLOSE_DAY(self):
    #    pass
    
    @abstractmethod
    #context,security,isLastest=True,data={},dataCount=20
    # 获取日线历史数据
    def GET_CLOSE_DATA_DAY(self):
        pass
       
    #@abstractmethod
    #security,isLastest=True,data={},dataCount=20
    # 获取周线历史数据
    #def GET_CLOSE_DATA_WEEK(self):
    #    pass
    
    #@abstractmethod
    #security,isLastest=True,data={},dataCount=20
    # 获取月线历史数据
    #def GET_CLOSE_DATA_MONTH(self):
    #    pass
    
    #@abstractmethod
    #context,security,isLastest=True,data={},dataCount=20
    # 获取季线历史数据
    #def GET_CLOSE_DATA_SEASON(self):
    #    pass
    
    #@abstractmethod
    #context,security,isLastest=True,data={},dataCount=20
    # 获取年线历史数据
    #def GET_CLOSE_DATA_YEAR(self):
    #    pass
    
    #@abstractmethod
    # 获取季线历史数据最大值
    #context,security,isLastest=True,data={},dataCount=20
    #def GET_HIGH_DATA_SEASON(self):
    #    pass
    
    #@abstractmethod
    # 获取季线历史数据最小值
    #context,security,isLastest=True,data={},dataCount=20
    #def GET_LOW_DATA_SEASON(self):
    #    pass
    
    #@abstractmethod
    # 获取年线历史数据最大值
    #context,security,isLastest=True,data={},dataCount=20
    #def GET_HIGH_DATA_YEAR(self):
    #    pass
    
    #@abstractmethod
    # 获取年线历史数据最小值
    #context,security,isLastest=True,data={},dataCount=20
    #def GET_LOW_DATA_YEAR(self):
    #    pass
    
    # 获取日线周线月线收盘价历史数据
    @abstractmethod
    #context,security,isLastest=True,data={},dataCount=180*20
    #return closeDay, closeMonth, closeWeek
    def GET_CLOSE_DATA(self):
        pass
    
    #@abstractmethod
    # 获取当前日线或ref天前成交量
    #context, security, ref=0 ,data={}
    #def GET_VOL_DAY(self):
    #    pass
    
    @abstractmethod
    # 获取日线历史成交量
    #context, security,isLastest=True,data={},dataCount=20
    def GET_VOL_DATA_DAY(self):
        pass
    
    @abstractmethod
    # 获取日线历史成交额
    #context, security,isLastest=True,data={},dataCount=20
    def GET_AMOUNT_DATA_DAY(self):
        pass
    
    '''
    data function end   ------------------------------------
    '''
    
class DataSrcFactory(object):
    #singleton
    __FINSTANCE_ = None
    #subclass inherit check
    __ABCCLASSNAME__ = SecurityDataSrcBase.__name__
    
    def __init__(self, clazzpath, *args):
        self.__fclazzpath__ = clazzpath
        self.__parseparam__(clazzpath)
        self.__fdatasrcobj__ = None
        self.__fdatasrcobj__ = DataSrcFactory.reflectmethod(self.__fmodulename__, self.__fclazzname__, *args)
        
    def __parseparam__(self, clazzpath):
        self.__fmodulename__ = clazzpath[0:clazzpath.rindex('.')]
        self.__fclazzname__ = clazzpath[clazzpath.rindex('.')+1:]

    def getDataSrc(self):
        return self.__fdatasrcobj__
    
    @classmethod
    def reflectmethod(cls, modulename, clazzname, *args):
        clazz = None
        try:
            m = __import__(modulename,fromlist=True)
            clazz = getattr(m, clazzname)
        except Exception as e:
            print ("%s:%s" %(str(Exception),str(e)))
            return None
        if str(type(clazz)).find('class') == -1:
            raise Exception("cannot get class type by clazzname:%s ,from module:%s" % (str(clazzname), str(modulename)))
        baseclazz = cls.inheritcheck(clazz)
        if baseclazz == None:
            raise Exception("class:%s not inherit baseclazz:%s" %(str(clazz), str(SecurityDataSrcBase)))
        print ("class:%s find inherit baseclazz:%s" %(str(clazz), str(SecurityDataSrcBase)))
        return clazz(*args)
    
    @classmethod
    def inheritcheck(cls, clazz):
        "Look up name in cls and its base classes."
        if clazz.__name__.find(cls.__ABCCLASSNAME__) != -1 :
            print ("%s inherit find" %(clazz.__name__))
            return clazz
        for base in clazz.__bases__:
            return cls.inheritcheck(base)
        return None
    
    @staticmethod
    def getFrom(clazzpath, *args):
        if not DataSrcFactory.__FINSTANCE_:
            #new instance 
            DataSrcFactory.__FINSTANCE_ = DataSrcFactory(clazzpath, *args)
        if not DataSrcFactory.__FINSTANCE_.__fclazzpath__ == clazzpath:
            print ("reload for new clazzpath:" + clazzpath)
            DataSrcFactory.__FINSTANCE_ = DataSrcFactory(clazzpath, *args)
        return DataSrcFactory.__FINSTANCE_
