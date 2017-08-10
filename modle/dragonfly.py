#!/usr/bin/env python
# -*- coding:utf-8 -*- 
'''
Created on 2017-3-9

@author: yuql
'''
import numpy as np

#from datasrc import * 
#TODO jq not suport root path
from dsadapter import *
from observer import DrawDownObserver

class FlyDragon(object):
    """fly dragon model"""
    MODULE = 'FlyDragon'
    VERSION = '1.0.1'
    MDEBUG = True
    #max watch time 
    FLYDAY_MAX = 4
    HORVER_MARGIN = 0
    #TODO HORVER_MAGIN
    HORVER_MARGIN_STOP = HORVER_MARGIN-3
    HORVER_MARGIN_FIRE = HORVER_MARGIN-6
    #fly height range
    WBBMIN = 20
    WBBMAX = 40
    #target flag
    RET_BUY = 1
    RET_SELL = -1
    RET_KEEP = 0
    def __init__(self, context, security):
        self.__security__ = security
        self._do_init(context)
    def __repr__(self):
        return '%s %s:{dragon_fly:%s,day_to_hover:%s,height_to_hover:%s,aimed_time:%s,day_has_fly:%s}\t' % (self.__class__.__name__, 
               self.__security__,self.dragon_fly,self.day_to_hover,self.height_to_hover,str(self.aimed_time),self.day_has_fly)

    def _do_init(self, context):
        self._reset_state()
        self.refresh(context)
        
    def __eq__(self, other):
        if not isinstance(other, FlyDragon):
            return False
        return self.__security__ == other.__security__
    
    def __cmp__(self, other):
        if not isinstance(other, FlyDragon):
            return 1
        #in portfolio first:
        if self.__fired__ and  (not other.__fired__):
            return -1
        elif  (not self.__fired__) and other.__fired__:
            return 1
        # return aimed 
        #if not self.dragon_fly:
        #    return 1
        # return high wflag item
        if self.__wflag__ > other.__wflag__:
            return -1
        elif self.__wflag__ < other.__wflag__:
            return 1
        else:
            # return fly longer
            if self.day_has_fly > other.day_has_fly:
                return -1
            elif self.day_has_fly < other.day_has_fly:
                return 1
            else:
                # return hover longer
                if self.day_to_hover > other.day_to_hover:
                    return -1
                elif self.day_to_hover < other.day_to_hover:
                    return 1
                else:
                    # return hover highter
                    if self.height_to_hover > other.height_to_hover:
                        return -1
                    elif self.height_to_hover > other.height_to_hover:
                        return 1
                    else:
                        return 0
    
    def _reset_state(self):
        self.dragon_fly = False
        self.day_to_hover = 0
        self.height_to_hover = 0
        self.aimed_time = None
        self.day_has_fly = 0
        """
          dragon_fly - flag for fly to be aimed
          day_to_hover - lastest hover ma10 time by withhold
          height_to_hover - lastest hover ma10 percent by withhold
          aimed_time - lastest aimed timestamp
          day_has_fly - aimed fly time, maybe we has ride it for many days :)
        """
        self.__fired__ = False
        self.__firepoint__ = 0
        self.__wflag__ = 0
        self.observer = None
    
    def security(self):
        return self.__security__
    
    def setFlag(self, flag):
        self.__wflag__ = flag
        
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

    def sameDay(self, context):
        return (self.aimed_time != None and 
                    self.aimed_time.year==context.current_dt.year and 
                    self.aimed_time.month==context.current_dt.month and 
                    self.aimed_time.day==context.current_dt.day)

    def getProfit(self,context):
        if self.__fired__:
            close_last = GET_CLOSE_DAY(context, self.__security__)
            profit = (close_last -  self.__firepoint__)/self.__firepoint__ * 100
            self.logd(self.__security__ +" profit:" + str(profit))
        else:
            return 0
        
    def handleTarget(self, context, data):
        if not self.dragon_fly:
            self.__fired__ = False
            self.observer = None
            return self.RET_SELL
        close_last = GET_CLOSE_DAY(context, self.__security__, 0, data)
        ma20 = MA_N_DAY(context, self.__security__, 20, 0, data)
        if close_last < ma20:
            #self.logd(self.__security__ +" stopLoss!")
            self.__fired__ = False
            self.observer = None
            return self.RET_SELL
        #refresh koudi
        dropDown = self.horver(context, True)
        #decide to sell
        if self.__fired__ :
            if dropDown:
                self.__fired__ = False
                self.observer = None
                #reset flystate
                self.dragon_fly = False
                #reset firepoint to void refire
                self.__firepoint__ = 0
                return self.RET_SELL
            else:
                #profit = (close_last -  self.__firepoint__)/self.__firepoint__ * 100
                #self.logd(self.__security__ +" profit:" + str(profit))
                return self.RET_KEEP
        
        #decide to buy
        runTime = GET_RUN_MINUTES(context)
        #after 9:45 to sample
        if runTime < 15 or runTime % 5 !=0:
            #wait to stable
            return self.RET_KEEP
        if self.dragon_fly and self.__firepoint__ !=0 and close_last >= self.__firepoint__:
            lagprofit = (close_last -  self.__firepoint__)/self.__firepoint__ * 100
            if lagprofit > 3.5:
                #self.logd("%s:no fire for lagprofit %s!" % (str(self.__security__), str(lagprofit)))
                return self.RET_KEEP
            if self.height_to_hover < self.HORVER_MARGIN_FIRE:
                #self.logd("%s:no fire for hover %s !!!" % (str(self.__security__), str(self.height_to_hover)))
                return self.RET_KEEP
            lockw = self.targetLock(context, data, close_last, ma20, runTime)
            if lockw > 0:
                self.logd("%s %s:fire in the hold!:%s,weight:X%s" %(str(self.__firepoint__),str(self.__security__),str(close_last),str(lockw)))
                self.__fired__ = True
                self.observer = DrawDownObserver(self.__security__, close_last)
            return lockw
        return self.RET_KEEP
    
    def horver(self, context, dropDownCheck=False):
        dropDown = False;
        runTime = GET_RUN_MINUTES(context)
        kma10 = GET_CLOSE_DAY(context, self.__security__, 10)
        close_last = GET_CLOSE_DAY(context, self.__security__)
        #fail for ma10 revert after 2:45
        if runTime >= 225 and close_last < kma10:
            #self.logd("%s:ma10 revert dropDown %s" % (str(self.__security__), str(kma10)))
            dropDown = True
        day_to_hover = 0
        height_to_hover = 0
        for i in range(1, 10):
            kMa10_close = GET_CLOSE_DAY(context, self.__security__, 10-i)
            day_to_hover = i
            hei_to_hover = (close_last - kMa10_close)/close_last * 100
            if i==1:
                height_to_hover = hei_to_hover
            if hei_to_hover < self.HORVER_MARGIN:
                #self.logd("close_last:"+str(close_last)+",kMa10_close:"+str(kMa10_close))
                #self.logd("day_to_hover:"+str(day_to_hover)+",height_to_hover:"+str(height_to_hover))
                break
        self.day_to_hover = day_to_hover
        self.height_to_hover = height_to_hover
        #fail for check dropDown margin
        if self.height_to_hover < self.HORVER_MARGIN_FIRE:
            #self.logd("%s:probaly dropDown %s" % (str(self.__security__), str(self.height_to_hover)))
            dropDown = True
        if runTime >= 225 and self.height_to_hover < self.HORVER_MARGIN_STOP:
            #self.logd("%s:probaly dropDown before trade %s" % (str(self.__security__), str(self.height_to_hover)))
            dropDown = True
            
        #success for stoplimit 
        if not self.observer == None and self.day_has_fly > 0:
            #target dd stop
            if self.observer.observe(close_last) < 0 :
                self.logd("%s:observe draw down" % (str(self.__security__)))  
                dropDown = True
            #state stop
            maxvalue = self.observer.maxvalue()
            state, keyvalue = BOLL_DAY_STATE(context, self.__security__)
            #print state
            #print keyvalue
            #print close_last
            if state == 1 and maxvalue >= keyvalue and close_last < keyvalue:
                self.logd("%s:state stop UP_END:%s" % (str(self.__security__),str(keyvalue)))  
                dropDown = True
            if state == 2 and close_last >= keyvalue:
                self.logd("%s:state stop UP_KEEP:%s" % (str(self.__security__),str(keyvalue)))  
                dropDown = True
        if dropDownCheck:
            return dropDown
        return False
    
    def target(self, context):
        high_last = GET_HIGH_DAY(context, self.__security__)
        low_last = GET_LOW_DAY(context, self.__security__)
        close = GET_CLOSE_DAY(context, self.__security__,0)
        close_ref = GET_CLOSE_DAY(context, self.__security__,1)
        co_2 =  (high_last + low_last)/2
        vibrate = (high_last - low_last)/close_ref *100
        if vibrate < 3 or close >co_2:
            self.__firepoint__ = high_last
        else:
            self.__firepoint__ = co_2
        self.logd("%s:target:%s" % (str(self.__security__), str(self.__firepoint__))) 
    
    def targetLock(self, context, data, closeLast ,ma20, runtime): 
        ret = self.RET_KEEP
        volPv = VOL_PV(context, self.__security__, 20, data)
        #TODO, avoid vop implse 
        if (volPv > 55 and runtime < 180) or (volPv > 52 and runtime >= 180):
            self.logd("%s:targetLock for volPv:%s !!!" % (str(self.__security__), str(volPv)))
            ret += 1
            ma60 = MA_N_DAY(self.__security__, 60, 0, data)
            kMa60_close = GET_CLOSE_DAY(context, self.__security__, 54)
            if ma20 > ma60 and closeLast > kMa60_close:
                self.logd("%s:targetLock for ma60:%s !!!" % (str(self.__security__), str(volPv)))
                ret += 1
            #add wfalg
            ret += self.__wflag__
        else :
            #self.logd("%s:target volPv:%s" % (str(self.__security__), str(volPv)))
            pass
        return ret
    
    def refresh(self, context):
        #self.logd("refresh begin")
        reAimed = FlyDragon.aimed(context,self.__security__)
        dropDownCheck = False
        if self.dragon_fly:
            #has aimed before
            if not reAimed:
                #reAimed NOT checkDropDown
                dropDownCheck = True;
                #update day fly at LEAST refresh DAILY
                if not self.sameDay(context):
                    self.day_has_fly += 1;
                    self.logd("refresh time:"+str(self.aimed_time)+",day_has_fly:"+str(self.day_has_fly))
        else :
            #has not fly yet! need reAimed 
            if not reAimed:
                #self.logd("not fly:"+self.__security__)
                self._reset_state()
                return False
        if reAimed:
            self.dragon_fly =True;
            self.aimed_time = context.current_dt
            self.day_has_fly = 0
            self.target(context)
        dropDown = self.horver(context, dropDownCheck)
        #well done for fly success
        if (self.day_has_fly >= self.FLYDAY_MAX):
            if self.observer and self.observer.overthrethold():
                self.logd("hold on fly:"+self.__security__+",maxprofit:"+str(self.observer.maxprofit()))
                return self.dragon_fly
            self.logd("dropDown fly:"+self.__security__)
            self.getProfit(context)
            self._reset_state()
            return False
        if dropDown :
            self.logd("dropDown hover:"+self.__security__)
            self.getProfit(context)
            self._reset_state()
            return False
        #self.logd("refresh end:"+str(self.dragon_fly))
        return self.dragon_fly
        
    @classmethod  
    def aimed(cls, context, security):
        #print security
        #MA20
        MA20 = MA_N_DATA_DAY(context, security,20)
        #忽略次新股无日线数据
        if np.isnan(MA20[-1]) or np.isnan(MA20[-2]):
            #cls.logd("MODE_FLY_DRAGON null data Day!"+security)
            return False
        SPKEEP = (MA20[-1] - MA20[-2])/MA20[-2]*20*100
        if SPKEEP<=0:
            #cls.logd("SPKEEP:"+str(SPKEEP))
            return False
        #MA10
        MA10 = MA_N_DATA_DAY(context, security,10)
        if MA10[-1]<MA10[-2]:
            #cls.logd("MA10:"+str(MA10))
            return False
        #BOLL
        stdDev = STD_DATA_DAY(context, security)
        std = stdDev[-1]
        std1 = stdDev[-2]
        WBB = std*4/MA20[-1] * 100
        WBB1 = std1*4/MA20[-2] * 100
        if WBB <= cls.WBBMIN or WBB >cls.WBBMAX:
            #cls.logd("WBB:"+str(WBB))
            return False
        close = GET_CLOSE_DAY(context, security)
        BB = (close -  (MA20[-1]-std*2))/(std*4)*100
        if BB<50 or BB>70:
            #cls.logd("BB:"+str(BB))
            return False
        SHRINK = (WBB-WBB1)/2*20
        if SPKEEP+SHRINK <= 0:
            #cls.logd("SPKEEP:"+SPKEEP+",SHRINK:"+SHRINK)
            return False
        #WR
        wrr9 = 100-WR_DAY(context, security, 9)
        #rsi10 = RSI_DAY(security, 10)
        #cls.logd("wrr9:"+str(wrr9))
        #cls.logd("rsi10:"+str(rsi10))
        if wrr9 >=20 and RSI_DAY(context, security, 10) >=55:
            return False
        return True;
        
    @classmethod
    def getDragonPool(cls, context, stocklist):
        d_count = len(stocklist)
        cls.logd("begin count:%s" % (d_count))
        d_i = 0
        dragon_list = []
        for security in stocklist:
            #g.debug =  security
            #d_i = d_i + 1;
            #if d_i % (d_count//100 + 1) == 0:
            #    cls.logd("doing:%s %%" % str(d_i/(d_count//100 + 1)))
            flydragon = FlyDragon(context, security)
            if flydragon.dragon_fly:
                dragon_list.append(flydragon) 
        cls.logd("end count:%s" % len(dragon_list))
        return dragon_list
