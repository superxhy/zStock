#!/usr/bin/env python
# -*- coding:utf-8 -*- 
'''
Created on 2017-3-10

@author: yuql
'''

from datasrc import * 
#TODO jq not suport root path
#from dsadapter import *

'''
    hhv = (1 + mf)base
    hhv * (1 - drawDown) - base = (hhv-base) * (1 - bargin)
    drawDown = 1 - (1+ (1-bm)mf)/1+mf
    margin * 100 = -k*(mfp-MP) + MPMR
    k = (margin7 - MPMR )/(MP - 7)
'''

'''
0.5
i:7, val:0.0327102803738
0.482608695652
i:8, val:0.0357487922705
0.465217391304
i:9, val:0.0384124451536
0.447826086957
i:10, val:0.0407114624506
0.430434782609
i:11, val:0.0426556991774
0.413043478261
i:12, val:0.0442546583851
0.395652173913
i:13, val:0.0455175067334
0.378260869565
i:14, val:0.0464530892449
0.360869565217
i:15, val:0.0470699432892
0.34347826087
i:16, val:0.0473763118441
0.326086956522
i:17, val:0.0473801560758
0.308695652174
i:18, val:0.0470891672808
0.291304347826
i:19, val:0.0465107782243
0.273913043478
i:20, val:0.045652173913
0.25652173913
i:21, val:0.0445203018326
0.239130434783
i:22, val:0.0431218816821
0.221739130435
i:23, val:0.0414634146341
0.204347826087
i:24, val:0.0395511921459
0.186956521739
i:25, val:0.0373913043478
0.169565217391
i:26, val:0.0349896480331
0.152173913043
i:27, val:0.0323519342691
0.134782608696
i:28, val:0.0294836956522
0.117391304348
i:29, val:0.0263902932255
0.1
i:30, val:0.0230769230769
'''
def GET_DRAW_DOWN(mfp, MP = 30, MPMR = 10, TH=7, THMR=50):
    if mfp < TH:
        #0.04326
        return TH * 0.618 /100
    if mfp > MP:
        return MPMR *1.0/3/100
    margin = (-1.0*(THMR - MPMR )/(MP -TH)*(mfp-MP) + MPMR)*1.0/100
    #print margin
    return 1 - (1+(1-margin)*mfp*1.0/100)/(1 + mfp*1.0/100)

class DrawDownObserver(object):
    MAXFP_TH = 7
    
    def __init__(self, security, cost):
        self.__security__ = security
        self.__basecost__ = cost
        self.reset()
        
    def reset(self):
        self.__maxvalue__ = 0
        self.__maxprofit__ = 0
        self.__drawdown__= 0
        self.__stoplimit__ = 0
        self.__overth__ = False
        
    def started(self):
        if self.__maxvalue__ == 0:
            return True
        return False
    
    def maxvalue(self):
        return self.__maxvalue__
    
    def maxprofit(self):
        return self.__maxprofit__
    
    def overthrethold(self):
        return self.__overth__
    
    def observe(self, lastclose):
        #begin to start
        currentfp = (lastclose - self.__basecost__)*1.0/self.__basecost__ * 100
        if currentfp < -self.MAXFP_TH:
            #stop loss
            return -1
        elif currentfp < 0:
            #print "%s: - profit:%s" %(str(self.__security__), str(currentfp))
            pass
        else :
            #print "%s: + profit:%s" %(str(self.__security__), str(currentfp))
            pass
        
        #refresh threthold
        overth = currentfp > self.MAXFP_TH
        if not (self.__overth__ == overth):
            self.__overth__ = overth
            print "%s:set overth :%s,currentfp:%s" %(str(self.__security__), str(overth), str(currentfp))
        #refresh maxfp maxdd
        if lastclose > self.__maxvalue__:
            #print "%s: refresh maxvalue:%s,mfp:%s" %(str(self.__security__), str(lastclose), str(currentfp))
            self.__maxvalue__ = lastclose
            self.__maxprofit__ = currentfp
            self.__drawdown__ = GET_DRAW_DOWN(currentfp,30)
            self.__stoplimit__ = self.__maxvalue__ * (1 - self.__drawdown__)
            #print "%s: refresh stoplimit:%s, dd:%s" %(str(self.__security__), str(self.__stoplimit__),str(self.__drawdown__))
        if lastclose < self.__stoplimit__:
            print "%s: observer stoplimit:%s, dd:%s, currentfp:%s" %(str(self.__security__), str(self.__stoplimit__),str(self.__drawdown__),str(currentfp))
            return -1
        #print "%s: observer keep profit:%s" %(str(self.__security__), str(currentfp))
        return 0

'''
simple method to buy in the low and sell in the high
usually use observer the LONG position security and get in 
the SUB period relative low position
1. use bollstate to judge relative position and state
2. use cci to observe the transition for state from abnormal state to normal
'''
class InTradayObserver(object):
    #observer cost under threshold
    MAXDE_TH = 3
    #boll day state to distinguish to buy aggressive
    STATE_INIT    = 0
    STATE_HIGH_30 = 1
    STATE_HIGH_15 = 2
    STATE_HIGH_5  = 3
    STATE_LOW_30  = -1
    STATE_LOW_15  = -2
    STATE_LOW_5   = -3
    
    def __init__(self, security):
        self.__security__ = security
        self.reset()
        
    def __observe_stateday__(self, context):
        state, wbb, bb, bbH, bbL = BOLL_STATE(context, self.__security__,'D')
        print "security:%s boll State:%s,wbb:%s,bb:%s,bbH:%s,bbL%s" %(str(self.__security__), str(state),str(wbb),str(bb),str(bbH),str(bbL))
        if state == 3 :
            self.__upstart__ = True
        else:
            self.__upstart__ = False
        return self.__upstart__
    
    def __observe_state30__(self, context, lastclose):
        state, wbb, bb, bbH, bbL = BOLL_STATE(context, self.__security__,30)
        if state > 1 and bbH > 90:
                CCI30= CCI_DATA(context,self.__security__, 30, {}, 1)
                if CCI30[-1] > 100 :
                    self.__state__ = self.STATE_HIGH_30
                    self.__observecost__ = lastclose
                    print "security:%s state:%s observecost:%s" %(str(self.__security__), str(self.__state__),str(self.__observecost__))
        if self.__upstart__:
            if state > 0 and state < 3 and bb > 50 and bb < 70:
                CCI30= CCI_DATA(context,self.__security__, 30, {}, 1)
                if CCI30[-1] < 0 :
                    self.__state__ = self.STATE_LOW_30
                    self.__observecost__ = lastclose
                    print "security:%s state:%s observecost:%s forupstart" %(str(self.__security__), str(self.__state__),str(self.__observecost__))
        else:
            if state < 0 and state > -3 and bbL < 10:
                CCI30= CCI_DATA(context,self.__security__, 30, {}, 1)
                if CCI30[-1] < -100 :
                    self.__state__ = self.STATE_LOW_30
                    self.__observecost__ = lastclose
                    print "security:%s state:%s observecost:%s forpullback" %(str(self.__security__), str(self.__state__),str(self.__observecost__))
        return 0

    def __observe_state15__(self, context, lastclose):
        currentTh = (lastclose - self.__observecost__)*1.0/self.__observecost__ * 100
        if self.__state__ > 0 :
            print "security:%s state:%s currentTh:%s reset" %(str(self.__security__), str(self.__state__),str(self.currentTh))
            if currentTh < -self.MAXDE_TH:
                self.__state__ = self.STATE_INIT
                self.__observecost__ = 0
                return -1
            CCI15= CCI_DATA(context,self.__security__, 15, {}, 2)
            #if len(CCI15) >= 2 and CCI15[-2] > 100 and CCI15[-1] < CCI15[-2]:
            if len(CCI15) >= 2 and CCI15[-1] < CCI15[-2]:
                self.__state__ = self.STATE_HIGH_15
                self.__observecost__ = lastclose
                print "security:%s state:%s currentTh:%s" %(str(self.__security__), str(self.__state__),str(self.currentTh))
                return 0
        else :
            if currentTh > self.MAXDE_TH:
                print "security:%s state:%s currentTh:%s reset" %(str(self.__security__), str(self.__state__),str(self.currentTh))
                self.__state__ = self.STATE_INIT
                self.__observecost__ = 0
                return 0
            CCI15= CCI_DATA(context,self.__security__, 15, {}, 2)
            if len(CCI15) >= 2 and CCI15[-2] < -100 and CCI15[-1] > CCI15[-2]:
                self.__state__ = self.STATE_LOW_15
                self.__observecost__ = lastclose
                print "security:%s state:%s currentTh:%s" %(str(self.__security__), str(self.__state__),str(self.currentTh))
                return 0
        return 0
    
    def __observe_state5__(self, context, lastclose):
        currentTh = (lastclose - self.__observecost__)*1.0/self.__observecost__ * 100
        if self.__state__ > 0 :
            if currentTh < -self.MAXDE_TH:
                print "security:%s state:%s currentTh:%s reset" %(str(self.__security__), str(self.__state__),str(self.currentTh))
                self.__state__ = self.STATE_INIT
                self.__observecost__ = 0
                return -1
            CCI5= CCI_DATA(context,self.__security__, 5, {}, 1)
            if CCI5[-1] < 100:
                self.__state__ = self.STATE_HIGH_5
                print "security:%s state:%s currentTh:%s" %(str(self.__security__), str(self.__state__),str(self.currentTh))
                return -1
        else :
            if currentTh > self.MAXDE_TH:
                print "security:%s state:%s currentTh:%s reset" %(str(self.__security__), str(self.__state__),str(self.currentTh))
                self.__state__ = self.STATE_INIT
                self.__observecost__ = 0
                return 0
            CCI5= CCI_DATA(context,self.__security__, 5, {}, 1)
            if CCI5[-1] > -100:
                self.__state__ = self.STATE_LOW_5
                print "security:%s state:%s currentTh:%s" %(str(self.__security__), str(self.__state__),str(self.currentTh))
                return 1
        return 0
    
    def reset(self):
        self.__state__ = self.STATE_INIT
        self.__upstart__ = False
        self.__basecost__ = 0
        self.__observecost__ = 0
        
    def started(self):
        if self.__basecost__ == 0:
            return True
        return False
        
    def observe(self, context, lastclose):
        runTime = GET_RUN_MINUTES(context)
        #begin to start
        if self.__state__ == self.STATE_INIT:
            if runTime % 30 != 0 :
                return 0
            self.__observe_stateday__(context)
            return self.__observe_state30__(context, lastclose)
        #use 5 minutes freq to observe
        if runTime % 5 != 0 :
            return 0
        if self.__state__ == self.STATE_LOW_30 or self.__state__ == self.STATE_HIGH_30:
            return self.__observe_state15__(context, lastclose)
        if self.__state__ == self.STATE_LOW_15 or self.__state__ == self.STATE_HIGH_15:
            return self.__observe_state5__(context, lastclose)
        if self.__state__ == self.STATE_LOW_5 or self.__state__ == self.STATE_HIGH_5:
            return self.__observe_state5__(context, lastclose)
        return 0
