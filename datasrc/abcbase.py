#!/usr/bin/env python
# -*- coding:utf-8 -*- 
'''
Created on 2017-3-8

@author: yuql
'''

import math
import decimal
import talib as tl
import numpy as np
from abc import ABCMeta, abstractmethod

class SecurityDataSrcBase(object):
    '''
    classdocs
    '''
    __metaclass__ = ABCMeta

    def __init__(self, name):
        self.name = name

           
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
                if str(type(getattr(SecurityDataSrcBase, atr))).find('method') == -1:
                    continue
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
            print "%s not in methods:%s" % (str(name),str(SecurityDataSrcBase.SINVOKEMETHODS))
            return None
        return getattr(self, name)(*args)
    
    '''
    index function begin ------------------------------------
    '''
    @staticmethod
    def GET_RUN_MINUTES(context):
        #9:30-11:30 13:00-15:00
        hour = context.current_dt.hour
        minute = context.current_dt.minute
        run_hours = 0
        run_minutes = 0
        if hour < 13:
            run_minutes = (hour-9)*60 + minute - 30
        else:
            run_minutes = (hour-13+2)*60 + minute
        if run_minutes > 240:
            run_minutes = 240
        #run_hours = run_minutes//60
        #run_half_hours = run_minutes//30
        #run_5_minutes = run_5_minutes//5
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
            print "KDJ_CN input invalid for len:%s %s %s " %(str(len1),str(len2),str(len3))
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
            print "CCI_CN input invalid for len:%s %s %s " %(str(len1),str(len2),str(len3))
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
    
    def STD_DATA_DAY(self, security, data={}, dataCount=1):
        closeDay = self.GET_CLOSE_DATA_DAY(security, True, data, dataCount-1+20)
        if np.isnan(closeDay[-1]):
            return np.nan
        return self.STD_CN(closeDay)
    
    def STD_DAY(self, security, ref=0, data={}):
        stdDev = self.STD_DATA_DAY(security, data, ref+1)
        if np.isnan(stdDev[-1-ref]):
            return np.nan
        return stdDev[-1-ref]
        #dataCount = ref + 20
        #closeDay = GET_CLOSE_DATA_DAY(security, True, data, dataCount)
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
    def BOLL_DAY_STATE(self, security, data={}):
        RET_UP_START = 3
        RET_UP_KEEP = 2
        RET_UP_END = 1
        RET_DN_START = -3
        RET_DN_KEEP = -2
        RET_DN_END = -1
        ret = 0
        keyprice = 0
        bollUPPER, bollMIDDLE, bollLOWER = self.BOLL_DATA_DAY(security, data, 2)
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
    
    def BOLL_DATA_DAY(self, security, data={}, dataCount=1):
        closeDay = self.GET_CLOSE_DATA_DAY(security, True, data, dataCount-1+20)
        if np.isnan(closeDay[-1]):
            return np.array(closeDay[-1]),np.array(closeDay[-1]),np.array(closeDay[-1])
        return self.BOLL_CN(closeDay)
        
    def BOLL_DAY(self, security, ref=0, data={}):
        bollUPPER, bollMIDDLE, bollLOWER = self.BOLL_DATA_DAY(security, data, ref+1)
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
        closeDay = self.GET_CLOSE_DATA_DAY(security, True, {}, timeperiod + dataCount - 1)
        highDay = self.GET_HIGH_DATA_DAY(context, security, True, {}, timeperiod + dataCount - 1)
        lowDay = self.GET_LOW_DATA_DAY(context, security, True, {}, timeperiod + dataCount -1)
        if np.isnan(closeDay[-timeperiod]):
            return np.array([np.nan])
        return self.WR_CN(highDay, lowDay, closeDay, timeperiod)
    
    def RSI_DAY(self, security, timeperiod=6, data={}, ref=0):
        real = self.RSI_DATA_DAY(security, timeperiod, data, ref+1)
        rsi = np.nan
        if not np.isnan(real[-1]):
            rsi = real[-1-ref]
        return rsi
    
    def RSI_DATA_DAY(self, security, timeperiod=6, data={}, dataCount=1):
        closeDay = self.GET_CLOSE_DATA_DAY(security, True, data, dataCount-1+timeperiod*10)
        if np.isnan(closeDay[-1]):
            return np.array([np.nan])
        return self.RSI_CN(closeDay, timeperiod)
    
    def KDJ_DAY(self, security, data={}, ref=0):
        k,d,j = self.KDJ_DATA_DAY(security, data, ref+1)
        if np.isnan(k[-1]):
            return 0,0,0,
        return k[-1-ref],d[-1-ref],j[-1-ref]

    def KDJ_DATA_DAY(self, security, data={}, dataCount=1):
        return self.KDJ_DATA(None, security, 'D',data, dataCount)
    
    def GET_PERIOD_DATA(self,context, security, freq = 'D', data={}, dataCount=1):
        if freq == 'D':
            close = self.GET_CLOSE_DATA_DAY(security, True, data, dataCount)
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
        return high, low ,close
    
    def KDJ_DATA(self, context, security, freq = 'D', data={}, dataCount=1):
        #sma target round2
        precision = 40
        high, low, close = self.GET_PERIOD_DATA(context, security, freq, data, dataCount+precision)
        if np.isnan(close[-1]):
            return np.array([0]),np.array([0]),np.array([0])
        K_V, D_V, J_V = self.KDJ_CN(high, low, close)
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
    period#waveindex:wavechr kd%k/kmaxindex:kmaxchr kmaxkd%kmax|waveseqstr
    exp:
    D#19:C0.46%77.15/17:B7.18%81.96|@ABCD4E3F2A2B2C2
    '''
    def GET_VOL_CRYPTO(self, context, security, period = 'D', data={}):
        trigrams421 = [
            {'mark':'±','element':'地','name':'坤'},#000
            {'mark':'⌊','element':'雷','name':'震'},#001
            {'mark':'§','element':'水','name':'坎'},#010
            {'mark':'⌋','element':'泽','name':'兌'},#011
            {'mark':'⌉','element':'山','name':'艮'},#100
            {'mark':'ψ','element':'火','name':'離'},#101
            {'mark':'⌈','element':'风','name':'巽'},#110
            {'mark':'≡','element':'天','name':'乾'},#111
                       ]
        DATACAL = 4
        DATALEN = 5
        DATACOUNT = DATACAL + (DATALEN -1)
        volData = self.GET_VOL_DATA_DAY(context, security,True,{},DATACOUNT)
        volArray = []
        for i in range(0, DATALEN):
            lenth = len(volData)
            index = lenth-1-(DATACAL-1) - i
            des = np.array([])
            if index >= 0 and index < lenth: 
                des= volData[index:index+DATACAL]
            if len(des) < DATACAL:
                break
            volArray.insert(0, des)
            
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
        cryptoindex = map(comp,volArray)
        cryptomk = [trigrams421[x]['mark'] for x in cryptoindex]
        cryptoel = [trigrams421[x]['element'] for x in cryptoindex]
        #print '.'.join(cryptomk)
        #print '.'.join(cryptoel)
        return '.'.join(cryptomk) + '.'.join(cryptoel)
    
    '''
    ['code','name','industry','close','wave','inert','vol']
    '''
    def GET_BUNDLE(self, context, security, crypto=False):
        code = security.split('.')[0]
        info = self.GET_SECURITY_INFO(security)
        name = info['name']
        industry = info['industry']
        close = self.GET_CLOSE_DAY(security)
        bundle = {
        'code':code,
        'name':name,
        'industry':industry,
        'close':close}
        if not crypto:
            return bundle
        wave = [
        self.GET_WAVE_CRYPTO(context, security, 30),
        self.GET_WAVE_CRYPTO(context, security, 'D'), 
        self.GET_WAVE_CRYPTO(context, security, 'W'), 
        self.GET_WAVE_CRYPTO(context, security, 'M'),
        self.GET_WAVE_CRYPTO(context, security, 'S'),
        self.GET_WAVE_CRYPTO(context, security, 'Y')]
        inert = [
        self.GET_INERT_CRYPTO(context, security, 30),
        self.GET_INERT_CRYPTO(context, security, 'D'),
        self.GET_INERT_CRYPTO(context, security, 'W')]
        vol = [self.GET_VOL_CRYPTO(context, security)]
        bundle['wave'] = wave
        bundle['inert'] = inert
        bundle['vol'] = vol
        return bundle
    
    def CCI_DAY(self, security, data={}, ref=0):
        CCI = self.KDJ_DATA_DAY(security, data, ref+1)
        if np.isnan(CCI[-1]):
            return 0
        return CCI[-1-ref]

    def CCI_DATA_DAY(self, security, data={}, dataCount=1):
        return self.CCI_DATA(None, security, 'D',data, dataCount)
    
    def CCI_DATA(self, context, security, freq = 'D', data={}, dataCount=1):
        #sma target round2
        precision = 14
        high, low, close = self.GET_PERIOD_DATA(context, security, freq, data, dataCount+precision)
        if np.isnan(close[-1]):
            return np.array([0])
        CCI = self.CCI_CN(high, low, close)
        if len(CCI) > precision:
            CCI = CCI[-dataCount:]
        else:
            #print "security:%s no len data precison %s" %(str(security), len(CCI))
            pass
        decimal.getcontext().rounding=decimal.ROUND_HALF_UP
        CCI = np.array([float(decimal.Decimal(s).quantize(decimal.Decimal('0.00'))) for s in CCI])
        return CCI
    
    def MA_N_DAY(self, security, n=5, ref=0, data={}):
        MA_N = self.MA_N_DATA_DAY(security, n, data, ref+1)
        if not np.isnan(MA_N[-1]):
            return MA_N[-1-ref]
        return 0
    
    def MA_N_DATA_DAY(self, security, n=5, data={}, dataCount=1):
        closeDay = self.GET_CLOSE_DATA_DAY(security, True, data, n + dataCount - 1)
        if np.isnan(closeDay[-1]):
            return np.array(closeDay[-1])
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
        if run_minutes==0:
            return 0
        alltime = 240
        if run_minutes==alltime:
            return volumLast
        volumPre = volumLast * 1.0 * alltime / run_minutes
        '''
        9:30 4.15 ,9:45 2.99 , 10:00 2.25 ,10:30 (1.5) , 2:00 (1.01) , 2:30 (1.005)  
        '''
        def fix_times(time, t60=1.5, t210=1.005):
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
    #filtPaused=True, filtSt=True
    def GET_ALL_SECURITIES(self):
        pass
    
    # 获取股票信息
    @abstractmethod
    #security
    def GET_SECURITY_INFO(self):
        pass
    
    # 获取当前分时收盘价
    @abstractmethod
    #context, security, data={}, freq=5, dataCount=1
    def GET_CLOSE_DATA_INTRADAY(self):
        pass
    #context, security, data={}, freq=5, dataCount=1
    def GET_HIGH_DATA_INTRADAY(self):
        pass
    
    #context, security, data={}, freq=5, dataCount=1
    def GET_LOW_DATA_INTRADAY(self):
        pass
    
    @abstractmethod
    #context, security, ref=0
    def GET_HIGH_DAY(self):
        pass
            
    @abstractmethod
    #context, security, ref=0
    def GET_LOW_DAY(self):
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
    @abstractmethod
    #context,security,isLastest=True,data={},dataCount=1
    def GET_HIGH_DATA_WEEK(self):
        pass
    
    # 获取周线历史数据最小值
    @abstractmethod
    #context,security,isLastest=True,data={},dataCount=1
    def GET_LOW_DATA_WEEK(self):
        pass
    
    # 获取月线历史数据最大值
    @abstractmethod
    #context,security,isLastest=True,data={},dataCount=1
    def GET_HIGH_DATA_MONTH(self):
        pass
    
    # 获取月线历史数据最小值
    @abstractmethod
    #context,security,isLastest=True,data={},dataCount=1
    def GET_LOW_DATA_MONTH(self):
        pass
    
    # 获取当前日线或ref天前收盘价
    @abstractmethod
    #security, ref=0 ,data={}
    def GET_CLOSE_DAY(self):
        pass
    
    @abstractmethod
    #security,isLastest=True,data={},dataCount=20
    # 获取日线历史数据
    def GET_CLOSE_DATA_DAY(self):
        pass
       
    @abstractmethod
    #security,isLastest=True,data={},dataCount=20
    # 获取周线历史数据
    def GET_CLOSE_DATA_WEEK(self):
        pass
    
    @abstractmethod
    #security,isLastest=True,data={},dataCount=20
    # 获取月线历史数据
    def GET_CLOSE_DATA_MONTH(self):
        pass
    
    @abstractmethod
    #context,security,isLastest=True,data={},dataCount=20
    # 获取季线历史数据
    def GET_CLOSE_DATA_SEASON(self):
        pass
    
    @abstractmethod
    #context,security,isLastest=True,data={},dataCount=20
    # 获取年线历史数据
    def GET_CLOSE_DATA_YEAR(self):
        pass
    
    @abstractmethod
    # 获取季线历史数据最大值
    #context,security,isLastest=True,data={},dataCount=20
    def GET_HIGH_DATA_SEASON(self):
        pass
    
    @abstractmethod
    # 获取季线历史数据最小值
    #context,security,isLastest=True,data={},dataCount=20
    def GET_LOW_DATA_SEASON(self):
        pass
    
    @abstractmethod
    # 获取年线历史数据最大值
    #context,security,isLastest=True,data={},dataCount=20
    def GET_HIGH_DATA_YEAR(self):
        pass
    
    @abstractmethod
    # 获取年线历史数据最小值
    #context,security,isLastest=True,data={},dataCount=20
    def GET_LOW_DATA_YEAR(self):
        pass
    
    # 获取日线周线月线收盘价历史数据
    @abstractmethod
    #context,security,isLastest=True,data={},dataCount=180*20
    #return closeDay, closeMonth, closeWeek
    def GET_CLOSE_DATA(self):
        pass
    
    @abstractmethod
    # 获取当前日线或ref天前成交量
    #context, security, ref=0 ,data={}
    def GET_VOL_DAY(self):
        pass
    
    @abstractmethod
    # 获取日线历史成交量
    #context, security,isLastest=True,data={},dataCount=20
    def GET_VOL_DATA_DAY(self):
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
        except Exception,e:
            print Exception,":",e
            return None
        if str(type(clazz)).find('class') == -1:
            raise Exception("cannot get class type by clazzname:%s ,from module:%s" % (str(clazzname), str(modulename)))
        baseclazz = cls.inheritcheck(clazz)
        if baseclazz == None:
            raise Exception("class:%s not inherit baseclazz:%s" %(str(clazz), str(SecurityDataSrcBase)))
        print "class:%s find inherit baseclazz:%s" %(str(clazz), str(SecurityDataSrcBase))
        return clazz(*args)
    
    @classmethod
    def inheritcheck(cls, clazz):
        "Look up name in cls and its base classes."
        if clazz.__name__.find(cls.__ABCCLASSNAME__) != -1 :
            print "%s inherit find" %(clazz.__name__)
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
            print "reload for new clazzpath:" + clazzpath
            DataSrcFactory.__FINSTANCE_ = DataSrcFactory(clazzpath, *args)
        return DataSrcFactory.__FINSTANCE_
