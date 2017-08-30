#!/usr/bin/env python
# -*- coding:utf-8 -*- 
'''
Created on 2017-8-24

@author: yuql
'''
import numpy as np
import decimal

from datasrc import * 
#TODO jq not suport root path
#from dsadapter import *
from observer import DrawDownObserver

class Surmount(object):
    """break up model"""
    MODULE = 'Surmount'
    VERSION = '1.0.1'
    MDEBUG = True
    #pretime
    MIN_TIME_PRE = 15
    #avoid fake pre
    FAKE_LOCKSTAB = False
    MIN_TIME_PRE_FAKE = 150
    FAKE_LOCK = False
    #chipex rate
    MAX_CHIPEX_RATE = 500
    MIN_CHIPEX_RATE = 20
    #volmonth rate
    MAX_VOLM_RATE = 1000
    MIN_VOLM_RATE = 125
    MIN_VOLM5_RATE = 150
    MIN_VOLM10_RATE = 100
    #break wide
    CCI_RANGE = 15
    #routerate
    MID_ROUTE_RATE = 50
    MAX_ROUTE_RATE = 75
    MIN_ROUTE_RATE = 15
    
    #send every handle
    HANDLE_SEND = True
    #sending high level item count
    MAX_SEND_COUNT = 10
    
    #target flag
    RET_BUY = 1
    RET_SELL = -1
    RET_KEEP = 0
    def __init__(self, context, security):
        self.__security__ = security
        self._do_init(context)
    def __repr__(self):
        return '%s %s:{surmount:%s,locked:%s,chipex_rate:%s,chipex_stab:%s,chipex_amount:%s,aimed_time:%s,day_has_aimed:%s}\n' % (self.__class__.__name__, 
               self.__security__,self.aimed,self.locked(),str(self.strdec(self.chipex_rate)),str(self.strdec(self.chipex_stab)),str(self.strdec(self.chipex_amount)),
               str(self.aimed_time),self.day_has_aimed)

    def _do_init(self, context):
        self._reset_state()
        self.refresh(context)
        
    def __eq__(self, other):
        if not isinstance(other, Surmount):
            return False
        return self.__security__ == other.__security__
    
    def __cmp__(self, other):
        if not isinstance(other, Surmount):
            return 1
        #in portfolio first:
        if self.locked_sell and  (not other.locked_sell):
            return -1
        elif  (not self.locked_sell) and other.locked_sell:
            return 1
        if self.__fired__ and  (not other.__fired__):
            return -1
        elif  (not self.__fired__) and other.__fired__:
            return 1
        # return aimed 
        #if self.aimed and  (not other.aimed):
        #    return -1
        #elif  (not self.aimed) and other.aimed:
        #    return 1
        # return locked item first:
        if self.locked() and  (not other.locked()):
            return -1
        elif  (not self.locked()) and other.locked():
            return 1
        # return locked_prive item first:
        #if self.locked_price and  (not other.locked_price):
        #    return -1
        #elif  (not self.locked_price) and other.locked_price:
        #    return 1
        # return locked_vol item first:
        if self.locked_vol and  (not other.locked_vol):
            return -1
        elif  (not self.locked_vol) and other.locked_vol:
            return 1
        elif self.locked_vol and other.locked_vol:
            # return high volRateM5
            if self.volRateM5 > other.volRateM5:
                return -1
            else:
                return 1
        # return chipexmeet item first:
        if self.chipex_meet and  (not other.chipex_meet):
            return -1
        elif  (not self.chipex_meet) and other.chipex_meet:
            return 1
        if self.chipex_meet and  other.chipex_meet:
            # return high chipexrate item
            #if self.chipex_rate > other.chipex_rate:
            #    return -1
            #elif self.chipex_rate < other.chipex_rate:
            #    return 1
            # return high volRateM5
            if self.volRateM5 > other.volRateM5:
                return -1
            else:
                return 1
        elif  (not self.chipex_meet) and (not other.chipex_meet):
            # return high chipexstab item
            if self.chipex_stab > other.chipex_stab:
                return -1
            elif self.chipex_stab < other.chipex_stab:
                return 1
        if self.day_has_aimed > self.day_has_aimed:
            return -1
        else:
            return 1
        
    def _reset_state(self):
        self.aimed = False
        self.ref_cci = 0
        self.locked_sell = False
        self.locked_cci = 0
        self.locked_price = False
        self.locked_vol = False
        self.chipex_meet = False
        self.chipex_amount = 0
        self.volRateM5 = 0
        self.volRateM10 = 0
        self.volM5 = 0
        self.volM10 = 0
        self.volK5 = 0
        self.volK10 = 0
        self.volPre = 0
        self.chipex_rate = 0
        self.chipex_stab = 0
        self.aimed_time = None
        self.day_has_aimed = 0
        """
          aimed - flag to be aimed
          chipex_meet - flag to chiex_rate meet in range chip exchanging
          chipex_amount - MA vol keep amount PRE deadline amount
          chipex_rate - MA vol kepp CURRENT rate
          chipex_stab - MA vol stable keep PRE index
          aimed_time - lastest aimed timestamp
          day_has_aimed - aimed fly time, maybe we has ride it for many days :)
        """
        self.__fired__ = False
        self.__firepoint__ = 0
        #self.__wflag__ = 0
        self.observer = None
    
    def security(self):
        return self.__security__
    
    def fired(self):
        return self.__fired__
    
    def locked(self):
        return self.locked_price and self.locked_vol
    
    @classmethod
    def version(cls):
        return cls.VERSION
    
    @classmethod
    def setDebug(cls,setDebug):
        cls.MDEBUG = setDebug
        
    @classmethod
    def logd(cls, text):
        if(cls.MDEBUG):
            print(cls.MODULE +"<debug>:"+text)

    @staticmethod
    def strdec(n):
        return float(decimal.Decimal(n).quantize(decimal.Decimal('0.00')))
    
    @staticmethod
    def calRate(a, b):
        #avoid infinate
        if np.isnan(b) or b == 0:
            return 0
        return a/b * 100
    
    #量能转化均衡算法
    @staticmethod
    def chipExchange(varr5Rel,varr10Rel, volPre):
        varr5 = map(lambda x: Surmount.calRate(volPre-x, x), varr5Rel)
        varr10 = map(lambda x: Surmount.calRate(volPre-x, x), varr10Rel)
        #放量界点权值
        qtbegin = 100
        #界点权值步长
        qtrate = 10
        sumarr = 0
        lenarr = min(len(varr5),len(varr10))
        for i in range(0, lenarr):
            sumarr += varr5[i] * 100.0/qtbegin + varr10[i] * 100.0/qtbegin
            if qtbegin > qtrate:
                qtbegin -= qtrate
        return Surmount.calRate(sumarr, lenarr*200)
    
    #量能转化调和平均算法
    @staticmethod
    def chipHarmonic(varr5Rel,varr10Rel, volPreRate):
        #放量界点权值
        qtbegin = 100
        #界点权值步长
        qtrate = 10
        sumarr = 0
        lenarr = min(len(varr5Rel),len(varr10Rel))
        for i in range(0, lenarr):
            sumarr += 1.0/varr5Rel[i] * 100.0/qtbegin + 1.0/varr10Rel[i] * 100.0/qtbegin
            if qtbegin > qtrate:
                qtbegin -= qtrate
        return 2.0 * lenarr/sumarr * (volPreRate/100 + 1)
    
    @staticmethod
    def chipExchangeStab(varr5Rel,varr10Rel):
        #稳定转化缩量天数
        suffocate = 2
        stab5 = Surmount.calRate(varr5Rel[0] - np.array(varr5Rel[1:suffocate]).mean()*suffocate/2, varr5Rel[0])
        stab10 = Surmount.calRate(varr10Rel[0] - np.array(varr10Rel[1:suffocate]).mean()*suffocate/2, varr10Rel[0])
        return stab5 + stab10
    
    def sameDay(self, context):
        return (self.aimed_time != None and 
                    self.aimed_time.year==context.current_dt.year and 
                    self.aimed_time.month==context.current_dt.month and 
                    self.aimed_time.day==context.current_dt.day)

    def getProfit(self, context, data):
        if self.__fired__:
            close_last = GET_CLOSE_DAY(context, self.__security__, 0 , data)
            profit = (close_last -  self.__firepoint__)/self.__firepoint__ * 100
            self.logd(self.__security__ +" profit:" + str(profit))
        else:
            return 0
        
    def sellOut(self, context, data, limit=False):
        # fill limit ignore chipex
        if limit:
            try:
                zflimit = (data[self.__security__].close == data[self.__security__].high_limit)
            except Exception,e:
                zflimit = False
            if zflimit:
                return self.RET_KEEP
        try:
            dflimit = (data[self.__security__].close == data[self.__security__].low_limit)
        except Exception,e:
            dflimit = False
        self.getProfit(context, data) 
        if self.locked_sell:
            self.logd("security:%s failing to sellout now!!!pay for a fake breaking" % (str(self.__security__)))
            return self.RET_KEEP
        if dflimit:
            self.logd("security:%s failing to sellout now for low_limit!!!" % (str(self.__security__)))
            return self.RET_KEEP
        self.__fired__ = False
        self.observer = None
        return self.RET_SELL
    
    def buyIn(self, close_last, runTime):
        # avoid pre fake, fire only ONCE
        #if (Surmount.FAKE_LOCKSTAB or Surmount.FAKE_LOCK) and runTime < Surmount.MIN_TIME_PRE_FAKE:
        #    return self.RET_KEEP
        self.logd("%s:fire in the hold!:%s,chipex_rate:%s" %(str(self.__security__),str(close_last),str(Surmount.strdec(self.chipex_rate))))
        Surmount.FAKE_LOCK = True
        self.__fired__ = True
        self.__firepoint__ = close_last
        self.observer = DrawDownObserver(self.__security__, close_last)
        self.locked_sell = True
        return self.RET_BUY
    
    def handleTarget(self, context, data, runTime):
        try:
            close_last = data[self.__security__].close
        except Exception,e:
            close_last = GET_CLOSE_DAY(context, self.__security__)
        # decide to sell
        if self.__fired__ :
            # fail to meet chipex
            if runTime >= self.MIN_TIME_PRE:
                if not self.chipex_meet:
                    self.logd("security:%s chiex:%s not meet!" %(str(self.__security__), str(Surmount.strdec(self.chipex_rate))))
                    return self.sellOut(context, data, True)
                if self.volPre < self.volM10:
                    self.logd("security:%s volM10:%s not meet!" %(str(self.__security__), str(Surmount.strdec(self.volM10))))
                    return self.sellOut(context, data, True)
            # success for stoplimit 
            if not self.observer == None and self.observer.observe(close_last) < 0:
                #target dd stop
                #state stop
                maxvalue = self.observer.maxvalue()
                self.logd("%s:observe draw down, maxvalue:%s" %(str(self.__security__), str(maxvalue)))
                return self.sellOut(context, data)
            # fail to meet price
            if not self.aimed and not self.locked_sell:
                cci_last = CCI_DATA(context,self.__security__, 'D', data, 1)[-1]
                if cci_last > 0:
                    return self.RET_KEEP
                self.logd("security:%s day_has_aimed:%s not meet!" %(str(self.__security__), str(self.day_has_aimed)))
                return self.sellOut(context, data)
        # decide to buy
        if self.locked():
            if not self.aimed:
                cci_last = CCI_DATA(context,self.__security__, 'D', data, 1)[-1]
                if cci_last < 50:
                    self.logd("security:%s cci:%s for not aimed!" %(str(self.__security__), str(cci_last)))
                    return self.RET_KEEP
            if self.breakRoute(context, data, runTime):
                if self.__fired__:
                    if self.__firepoint__ == 0:
                        print "firepoint error"
                        return self.RET_BUY
                    return self.RET_KEEP
                if self.locked_sell:
                    return self.RET_KEEP
                return self.buyIn(close_last, runTime)
            else:
                #wait for route range
                return self.RET_KEEP
        return self.RET_KEEP
    
    def updateChipex(self, context, data):
        DATACAL = 4
        DATALEN = 8
        DATACOUNT = DATACAL + (DATALEN -1)
        volData = GET_VOL_DATA_DAY(context, self.__security__,True,data,DATACOUNT)
        varr5Rel = volData[-5:-5+DATACAL]
        varr10Rel = volData[-10:-10+DATACAL]
        self.chipex_stab = Surmount.chipExchangeStab(varr5Rel, varr10Rel)
        volHa = Surmount.chipHarmonic(varr5Rel, varr10Rel, Surmount.MIN_CHIPEX_RATE)
        volM = 1.0*self.MIN_VOLM_RATE/100 * MAVOL_N_DAY(context, self.__security__, 20, 0, data)
        self.volM5 = MAVOL_N_DAY(context, self.__security__, 5, 0, data)
        self.volM10 = MAVOL_N_DAY(context, self.__security__, 10, 0, data)
        self.volK5 = 1.0*varr5Rel[0]
        self.volK10 = 1.0*varr10Rel[0]
        self.chipex_amount = max(volHa, volM)
    
    def breakRoute(self, context, data, runTime):
        high_last = GET_HIGH_DAY(context, self.__security__)
        low_last = GET_LOW_DAY(context, self.__security__)
        close = GET_CLOSE_DAY(context, self.__security__,0)
        #close_ref = GET_CLOSE_DAY(context, self.__security__,1)
        mid =  (high_last + low_last)/2
        route = (high_last - low_last)/2
        routeRate = Surmount.calRate(close - mid, route)
        #self.logd("%s:routeRate:%s" % (str(self.__security__), str(Surmount.strdec(routeRate))))
        cci = CCI_DATA(context,self.__security__, 'D', data, 4)
        cci_last = cci[-1]
        if cci_last < 50:
            return False
        if cci_last > self.ref_cci:
            #if cci_last < cci.max():
            #    return False
            if runTime >= Surmount.MIN_TIME_PRE_FAKE:
                return routeRate < self.MID_ROUTE_RATE
            # strong break
            if self.locked_cci > 100 and cci_last > self.locked_cci:
                return routeRate < self.MAX_ROUTE_RATE
            return routeRate < self.MIN_ROUTE_RATE
        else:
            return routeRate < -self.MAX_ROUTE_RATE
        
    def breakPoint(self, context, data):
        cci = CCI_DATA(context,self.__security__, 'D', data, 4)
        #self.logd("%s: breakPoint :%s" % (str(self.__security__), str(cci)))
        # keep no impulsive 
        if cci.min() > 50:
            return False
        # preliminary stage
        if np.isnan(cci[-1]) or abs(cci[-1] - 100) > Surmount.CCI_RANGE:
            return False
        self.logd("%s: price breakPoint :%s" % (str(self.__security__), str(cci)))
        self.ref_cci = cci[-2]
        self.locked_cci = cci[-1]
        self.locked_price = True
        return True
    
    def chipexMeet(self, context, data): 
        volPre = VOL_PRE(context, self.__security__, data, True)
        self.volPre = volPre
        # meet deadline
        if volPre > self.chipex_amount:
            DATACAL = 4
            DATALEN = 8
            DATACOUNT = DATACAL + (DATALEN -1)
            volData = GET_VOL_DATA_DAY(context, self.__security__,True,data,DATACOUNT)
            varr5 = volData[-5-1:-5+DATACAL-1]
            varr10 = volData[-10-1:-10+DATACAL-1]
            self.chipex_rate = Surmount.chipExchange(varr5, varr10, volPre)
            self.volRateM5 = Surmount.calRate(volPre, self.volM5)
            self.volRateM10 = Surmount.calRate(volPre, self.volM10)
            if self.chipex_rate > self.MIN_CHIPEX_RATE and self.chipex_rate < self.MAX_CHIPEX_RATE:
                #self.logd("%s:chipexMeet for volPre:%s chipRate:%s" % (str(self.__security__), str(Surmount.strdec(volPre)),str(Surmount.strdec(self.chipex_rate))))
                self.chipex_meet =  True
        # useless other rate
        else:
            self.chipex_meet =  False
            self.chipex_rate = 0
            self.volRateM5 = 0
            self.volRateM10 = 0
        return self.chipex_meet
    
    def chipexStab(self):
        if self.chipex_stab > 0:
            return True
        # not stable enough
        if self.chipex_stab <= 0 and self.chipex_stab > -self.MAX_CHIPEX_RATE:
            bargin = self.chipex_rate + self.chipex_stab
            if bargin > 2*self.MIN_CHIPEX_RATE:
                #self.logd("%s:chipexStab bargin:%s for stab:%s" % (str(self.__security__), str(Surmount.strdec(bargin)),str(Surmount.strdec(self.chipex_stab))))
                return True
        return False
    
    def targetLock(self, context, data, runTime):
        if not self.locked_price:
            self.breakPoint(context, data)
        locked_vol_last = self.locked_vol
        # default lock state
        locked_vol_now = False
        locked_vol_change = False
        if self.chipexMeet(context, data) and self.chipexStab():
            if runTime >= self.MIN_TIME_PRE and self.volPre>self.volK5 and self.volPre>self.volK10:
                #self.logd("%s:chipexMeet for volRateM5:%s volRateM10:%s" % (str(self.__security__), str(Surmount.strdec(self.volRateM5)),str(Surmount.strdec(self.volRateM10))))
                if self.volRateM5 > self.MIN_VOLM5_RATE:
                    locked_vol_now =  True
        # update last lock state            
        self.locked_vol = locked_vol_now
        if not locked_vol_last and locked_vol_now:
            self.logd("%s:locked_vol revert True at runTime:%s" %(str(self.__security__), str(runTime)))
            locked_vol_change = True
        if locked_vol_last and (not locked_vol_now):
            self.logd("%s:locked_vol revert False at runTime:%s" %(str(self.__security__), str(runTime)))
            locked_vol_change = True
            self.locked_price = False
        if locked_vol_change:
            self.logd("%s:locked_vol change, volRateM5:%s, volRateM10:%s, chipRate:%s, chipStab:%s" % (str(self.__security__), str(Surmount.strdec(self.volRateM5)),str(Surmount.strdec(self.volRateM10)),str(Surmount.strdec(self.chipex_rate)),str(Surmount.strdec(self.chipex_stab))))
        return self.locked()
        
    def releaeLock(self):
        self.locked_sell = False
        self.locked_cci = 0
        self.locked_price = False
        self.locked_vol =  False
        self.chipex_rate = 0
        self.chipex_meet = False
        
    def refresh(self, context, data={}):
        #self.logd("refresh begin")
        self.releaeLock()
        reAimed = Surmount.aimed(context, data, self.__security__)
        #has aimed before
        if self.aimed:
            if reAimed:
                if not self.sameDay(context):
                    self.day_has_aimed += 1;
            else:
                self.logd("%s:failed aimed ,day_has_aimed:%s" % (str(self.__security__), str(self.day_has_aimed)))
                self.aimed = False
                #set day_has_aimed -1 to del flag
                self.day_has_aimed = -1
                self.aimed_time = None
        #has not aimed before
        else :
            #revive now! 
            if reAimed:
                self.day_has_aimed = 0
            else:
                # another day not aimed has to be del
                if not self.sameDay(context):
                    if self.fired():
                        return True
                    self._reset_state()
                    return False
        if reAimed:
            self.aimed =True;
            self.aimed_time =  context.current_dt if context != None else None
            self.updateChipex(context, data)
        #self.logd("refresh end:"+str(self.dragon_fly))
        return True
        
    @classmethod  
    def aimed(cls, context, data, security):
        ma240 = MA_N_DAY(context, security, 240)
        biasYear = Surmount.calRate(GET_CLOSE_DAY(context, security) - ma240, ma240)
        if biasYear > 100 or biasYear < 0:
            return False
        #print security
        DATA_COUNT = 1
        cci = CCI_DATA(context,security, 'M', data, DATA_COUNT)
        #月线不对
        if np.isnan(cci[-1]) or cci[-1] < 100:
            return False
        cci = CCI_DATA(context,security, 'W', data, DATA_COUNT)
        #周线不对
        if np.isnan(cci[-1]) or cci[-1] < 100:
            return False
        #cci = CCI_DATA(context,security, 'D', data, DATA_COUNT)
        #忽略次新股无日线数据
        #if np.isnan(cci[-1]):
            #log.info("MODE_CCI security:%s null data Day!", security)
            #return False
        return True;
        
    @classmethod
    def getSurmountPool(cls, context, stocklist):
        d_count = len(stocklist)
        cls.logd("begin count:%s" % (d_count))
        d_i = 0
        ret_list = []
        for security in stocklist:
            #g.debug =  security
            #d_i = d_i + 1;
            #if d_i % (d_count//100 + 1) == 0:
            #    cls.logd("doing:%s %%" % str(d_i/(d_count//100 + 1)))
            s = Surmount(context, security)
            if s.aimed:
                ret_list.append(s) 
        cls.logd("end count:%s" % len(ret_list))
        return ret_list
    
    @staticmethod
    def refreshSurmountPool(context, data, poollist, stocklist, pretrade=False):
        Surmount.FAKE_LOCK = False
        if pretrade:
            if len(stocklist) == 0:
                Surmount.logd("empty stocklist, stop pool")
                poollist = []
                return poollist
            if len(poollist) == 0:
                Surmount.logd("empty poollist!, begin to init pool")
            else:
                return poollist
        newlist = Surmount.getSurmountPool(context, stocklist)
        newadd = []
        todel= []
        for s in poollist:
            if s.refresh(context, data):
                #continue to aimed
                pass
            else:
                todel.append(s.security())
                poollist.remove(s)
        for s in newlist:
            if s not in poollist:
                newadd.append(s.security())
                poollist.append(s)
        Surmount.logd("len:%s,refresh to todel:\n%s" %(str(len(todel)), str(todel)))
        Surmount.logd("len:%s,refresh to newadd:\n%s" %(str(len(newadd)), str(newadd)))
        poollist.sort()
        #print poollist
        #send after trade data for next day
        Surmount.sendSurmountPool(context, data, poollist, True, True)
        return poollist
        
    @staticmethod
    def handleSurmountPool(context, data, poollist, sellcb, buycb):
        runTime = GET_RUN_MINUTES(context)
        if runTime % 5 != 0:
            return
        for s in poollist:
            s.targetLock(context, data, runTime)
        #resort list ready to handle high level item
        poollist.sort()
        for s in poollist:
            res = s.handleTarget(context, data, runTime)
            if res < 0:
                sellcb(context, s.security())
            if res > 0:
                buycb(context, s.security())
        #resort list ready to send high level item
        poollist.sort()
        #print poollist
        if Surmount.HANDLE_SEND:
            Surmount.sendSurmountPool(context, data, poollist[0:Surmount.MAX_SEND_COUNT], False, True)
    
    @staticmethod
    def sendSurmountPool(context, data, poollist, pretrading=False, sendMail=False):
        REDSTAR_NEW = '+'
        REDSTAR_DEL = '-'
        REDSTAR_FIRE = '$'
        REDSTAR_LOCK = '*'
        REDSTAR_LOCKPRICE = '!'
        REDSTAR_LOCKVOL = '@'
        def redStar(security, idx):
            s = poollist[idx]
            rs = ''
            if s.locked():
                rs += REDSTAR_LOCK
            elif s.locked_price:
                rs += REDSTAR_LOCKPRICE
            elif s.locked_vol:
                rs += REDSTAR_LOCKVOL
            else:
                #no other locked factor
                pass
            if s.fired(): 
                if s.locked_sell:
                    rs += ('('+REDSTAR_FIRE+')')
                else:
                    rs += REDSTAR_FIRE
            if s.day_has_aimed < 0:
                rs += REDSTAR_DEL
            if s.day_has_aimed == 0:
                rs += REDSTAR_NEW
            return rs
        DSUtil.sendSecurities(context, data, [s.security() for s in poollist], pretrading, sendMail, pretrading, redStar)
