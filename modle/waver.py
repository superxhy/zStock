#!/usr/bin/env python
# -*- coding:utf-8 -*- 
'''
Created on 2017-10-31

@author: yuql
'''
import numpy as np
import decimal

from datasrc import * 
#TODO jq not suport root path
#from dsadapter import *
import datetime

class Waver(object):
    """wave model"""
    MODULE = 'Waver'
    VERSION = '1.5.6'
    MDEBUG = True
    #max calculate wave item count
    MAX_WAVE_COUNT = 20
    #wave begin char
    WAVE_CHAR_GOLD = '@'
    #wave up char
    WAVE_CHAR_UP = ['B','D','F']
    #wave down char
    WAVE_CHAR_DN = ['A','C','E']
    #fib reverter array
    FIB_ARRAY = [3, 5, 8]
    #421encode
    TRIGRAMS421R = [
        {'mark':'±','element':'地','name':'坤'},#000黑黑黑
        {'mark':'⌉','element':'山','name':'艮'},#001红黑黑
        {'mark':'§','element':'水','name':'坎'},#010黑红黑
        {'mark':'⌈','element':'風','name':'巽'},#011红红黑
        {'mark':'⌊','element':'雷','name':'震'},#100黑黑红
        {'mark':'ψ','element':'火','name':'離'},#101红黑红
        {'mark':'⌋','element':'澤','name':'兌'},#110黑红红
        {'mark':'≡','element':'天','name':'乾'},#111红红红
                   ]
    #flag for strong range
    #no enough data
    FLAG_WAVE_NOENOUGH = 0
    #range k80 upper cci 100upper
    FLAG_WAVE_STRONG = 2
    #range k50~80 cci 0~100
    FLAG_WAVE_MIDSTR = 1
    #range 20~50 cci -100~0
    FLAG_WAVE_MIDWEAK = -1
    #range 20 lower cci -100lower
    FLAG_WAVE_WEAK = -2
    #max scorerange deque length
    MAX_SCORERANGE_DEQUE = 10
    #send every handle
    HANDLE_SEND = True
    #sending high level item count
    MAX_SEND_COUNT = 100
    
    #target flag
    RET_BUY = 1
    RET_SELL = -1
    RET_KEEP = 0
    
    #static index instance for average compare
    index = None
    #threthhold position compare index to poollist
    indexPos = 0
    
    def __init__(self, context, security, data={}):
        self.__security__ = security
        self._do_init(context, data)
    def __repr__(self):
        return "%s %s%s#%s:%s%s%%%s/%s:%s%s%%%s|%s?%s\n" %(str(self.__security__),str(self.getScoreMark()),str(self.period),str(self.waveindex),str(self.wavechr),
            str(self.kd),str(self.k),str(self.kmaxindex),str(self.kmaxchr),str(self.kmaxkd),str(self.kmax),str(self.waveseqstr),self.getScoreStr())

    def _do_init(self, context, data):
        self._reset_state()
        self.refresh(context, data)
        
    def __eq__(self, other):
        if not isinstance(other, Waver):
            return False
        return self.__security__ == other.__security__
    
    def __cmp__(self, other):
        return Waver.cmpitem(self, other)
    
    def __lt__(self, other):
        return Waver.cmpitem(self, other) < 0
    
    def __gt__(self, other):
        return Waver.cmpitem(self, other) > 0
    
    def __le__(self, other):
        return Waver.cmpitem(self, other) <= 0
    
    def __ge__(self, other):
        return Waver.cmpitem(self, other) >= 0
    
    def __ne__(self, other):
        return Waver.cmpitem(self, other) != 0
    
    @classmethod
    def cmpitem(cls, my, other, aftertrade=False):
        if not isinstance(other, Waver):
            return 1
        #ignore no same period item 
        if not my.period == other.period:
            return 0
        #data not enough calc last
        if my.waveboundflag == cls.FLAG_WAVE_NOENOUGH and other.waveboundflag != cls.FLAG_WAVE_NOENOUGH:
            return 1
        elif my.waveboundflag != cls.FLAG_WAVE_NOENOUGH and other.waveboundflag == cls.FLAG_WAVE_NOENOUGH:
            return -1
        else:
            #waveboundflag strong first
            if my.waveboundflag > other.waveboundflag:
                return -1
            if my.waveboundflag < other.waveboundflag:
                return 1
        #data not enough calc last
        if my.waverangeflag == cls.FLAG_WAVE_NOENOUGH and other.waverangeflag == cls.FLAG_WAVE_NOENOUGH:
            #percentref first
            if my.percentref > other.percentref:
                return -1
            if my.percentref < other.percentref:
                return 1
            if my.percentref == other.percentref:
                return 0
        elif my.waverangeflag == cls.FLAG_WAVE_NOENOUGH and other.waverangeflag != cls.FLAG_WAVE_NOENOUGH:
            return 1
        elif my.waverangeflag != cls.FLAG_WAVE_NOENOUGH and other.waverangeflag == cls.FLAG_WAVE_NOENOUGH:
            return -1
        else:
            #waverangeflag strong first
            if my.waverangeflag > other.waverangeflag:
                return -1
            if my.waverangeflag < other.waverangeflag:
                return 1
        #gold cross first
        if my.kd >= 0 and other.kd < 0:
            return -1
        if my.kd < 0 and other.kd >= 0:
            return 1
        #gold cross no deviation first
        if my.kd > 0 and other.kd > 0:
            if my.waveindex == my.kmaxindex and other.waveindex != other.kmaxindex:
                return -1
            if my.waveindex != my.kmaxindex and other.waveindex == other.kmaxindex:
                return 1
        #wave direction strong first:
        if my.wavedirectflag > other.wavedirectflag:
            return -1
        elif my.wavedirectflag < other.wavedirectflag:
            return 1
        #speedup quick first:
        if my.kd > other.kd:
            return -1
        else:
            return 1
        
    @classmethod
    def cmpScoreRaise(cls, my, other, cmpindex=False, pretrade=False):
        #data not enough calc last
        if my.waveboundflag == cls.FLAG_WAVE_NOENOUGH and other.waveboundflag != cls.FLAG_WAVE_NOENOUGH:
            return 1
        if my.waveboundflag != cls.FLAG_WAVE_NOENOUGH and other.waveboundflag == cls.FLAG_WAVE_NOENOUGH:
            return -1
        if my.waverangeflag == cls.FLAG_WAVE_NOENOUGH and other.waverangeflag != cls.FLAG_WAVE_NOENOUGH:
            return 1
        if my.waverangeflag != cls.FLAG_WAVE_NOENOUGH and other.waverangeflag == cls.FLAG_WAVE_NOENOUGH:
            return -1
        #percent raise first
        pk = 1 if pretrade else 2
        if my.percentref > pk and other.percentref <= pk:
            return -1
        if my.percentref <= pk and other.percentref > pk:
            return 1
        #over index first
        if cmpindex:
            if my.getExcessIndex()==True and other.getExcessIndex()==False:
                return -1
            if my.getExcessIndex()==False and other.getExcessIndex()==True:
                return 1
        #gold cross first
        if my.kd >= 0 and other.kd < 0:
            return -1
        if my.kd < 0 and other.kd >= 0:
            return 1
        #waveboundflag strong first
        if my.waveboundflag > other.waveboundflag:
            return -1
        if my.waveboundflag < other.waveboundflag:
            return 1
        #wave range strong inactive first 
        if my.waverangeflag == cls.FLAG_WAVE_STRONG and other.waverangeflag != cls.FLAG_WAVE_STRONG:
            return -1
        if my.waverangeflag != cls.FLAG_WAVE_STRONG and other.waverangeflag == cls.FLAG_WAVE_STRONG:
            return 1
        if not pretrade:
            scorersmy = my.getScoreRaise()
            scorersother = other.getScoreRaise()
            #only order sk more
            sk = 10
            if scorersmy > sk and scorersother < sk:
                return -1
            if scorersmy < sk and scorersother > sk:
                return 1
        #percentref first
        if my.percentref > other.percentref:
            return -1
        if my.percentref < other.percentref:
            return 1
        if my.percentref == other.percentref:
            return 0
        
    @classmethod
    def cmpScoreMaRaise(cls, my, other, cmpindex=False):
        if cmpindex:
            if my.getExcessIndex()==True and other.getExcessIndex()==False:
                return -1
            if my.getExcessIndex()==False and other.getExcessIndex()==True:
                return 1
        scoremarsmy = my.getScoreMaRaise()
        scoremarsother = other.getScoreMaRaise()
        if scoremarsmy > scoremarsother:
            return -1
        if scoremarsmy < scoremarsother:
            return 1
        return 0
    
    @classmethod
    def cmpBbi(cls, my, other, cmpindex=False):
        #over index first
        if cmpindex:
            if my.getExcessIndex()==True and other.getExcessIndex()==False:
                return -1
            if my.getExcessIndex()==False and other.getExcessIndex()==True:
                return 1
        bbimy = my.getScoreBBI()
        bbiother = other.getScoreBBI()
        if bbimy > bbiother:
            return -1
        if bbimy < bbiother:
            return 1
        if bbimy == bbiother:
            return 0
        
    '''
      @     B     D     F     
      ^  |  ^  |  ^  |  ^  |  
      |  v  |  v  |  v  |  v  
         A     C     E     A  
    period#waveindex:wavechr kd%k/kmaxindex:kmaxchr kmaxkd%kmax|waveseqstr
    exp:
    D#19:C0.46%77.15/17:B7.18%81.96|@ABCD4E3F2A2B2C2
    '''
    def _reset_state(self):
        '''
        wave index cryptal
        '''
        #percent raise compare yestody
        self.percentref = 0
        #cci for period weekly
        self.cciw = 0
        #current wave period level, common in 'D' for daily , 'W' for weakly
        self.period = ''
        #current wave index from gold cross wave index begin with 1 
        self.waveindex = 0
        #curerent wave direct char range from 'A'~'F' begin with '@',common in 3upwave and 3 downwave
        self.wavechr = ''
        #average k index in one month
        self.kma = 0
        #current k index for strong/weak range from 0~100
        self.k = 0
        #current k-d index for strong/weak speed range from -20~20 in common
        self.kd = 0
        #max strong wave index from gold cross wave index begin with 1 
        self.kmaxindex = 0
        #max strong wave direct char
        self.kmaxchr = ''
        #max k index for strong/weak range from 0~100
        self.kmax = 0
        #max k index point strong/weak speed
        self.kmaxkd = 0
        #from gold cross to current all the wavechr squence 
        self.waveseq = np.array([])
        self.waveseqstr = ''
        
        '''
        strong range flag to compare with myself
        '''
        #flag to wave data not enough for new security
        self.waveenough = False
        self.waveboundflag = 0
        self.waverangeflag = 0
        self.wavedirectflag = 0
        '''
        order score flag to compare with others in waver sequences
        '''
        #current score range in waverpool list range from 0~100, ordered by strongtrade
        #last score range in waverpool list range from 0~100, init for -1 and use the current data to overwrite it after trade
        self.scorerangedeque = []
        #overwrite time stamp 
        self.aimed_time = None
        
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
    
    def sameDay(self, current_dt):
        return (self.aimed_time != None and 
                    self.aimed_time.year==current_dt.year and 
                    self.aimed_time.month==current_dt.month and 
                    self.aimed_time.day==current_dt.day)

    def refresh(self, context, data={}, period='D', callauction=False):
        #calculate percentref
        percentref, lastprice = PERCENT_DAY(context, self.__security__, data)
        self.percentref = percentref
        #skip to refresh for callauction
        if callauction:
            return
        K,D,J= KDJ_DATA(context,self.__security__, period, data, self.MAX_WAVE_COUNT)
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
        else:
            k = K[-1]
            kd = KD[-1]
            kmax = k
            kmaxkd = kd
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
        #waveformat = "%s#%s:%s%s%%%s/%s:%s%s%%%s|%s" %(str(period),str(waveindex),str(wavechr),str(kd),str(k),str(kmaxindex),str(kmaxchr),str(kmaxkd),str(kmax),str(waveseqstr))
        #print waveformat
        #self.kma = np.mean(K[-self.MAX_WAVE_COUNT/2:])
        self.period = period
        self.waveindex = waveindex
        self.wavechr = wavechr
        self.k = k
        self.kd = kd
        self.kmaxindex = kmaxindex
        self.kmaxchr = kmaxchr
        self.kmax = kmax
        self.kmaxkd = kmaxkd
        self.waveseq = waveseq
        self.waveseqstr =waveseqstr
        #calculate week bound
        self.cciw = CCI_DATA(context,self.__security__, 'W', data, 1)[-1]
        self.calcStrongRange()
        
    def calcStrongRange(self):
        #calculate wavedirect in last 3 wave
        wavelen = len(self.waveseq)
        bcdlen = 3
        if wavelen > 0:
            bcd = []
            for i in range(0, bcdlen):
                index = wavelen-1-i
                if index >= 0 and index < wavelen:
                    wavechar = self.waveseq[index]
                    if wavechar == self.WAVE_CHAR_GOLD:
                        bcd.append('1')
                    if wavechar in self.WAVE_CHAR_UP:
                        bcd.append('1')
                    if wavechar in self.WAVE_CHAR_DN:
                        bcd.append('0')
                else:
                    bcd.append('0')
            bcdstr = ''.join(bcd)
            if bcdstr == '':
                self.wavedirectflag = 0
            else:
                self.wavedirectflag = int(bcdstr, 2)
        #calculate strong range
        if np.isnan(self.k) or self.k == 100:
            #no daily data enough
            self.waverangeflag = self.FLAG_WAVE_NOENOUGH
        elif self.k >= 80:
            self.waverangeflag = self.FLAG_WAVE_STRONG
        elif self.k >= 50:
            self.waverangeflag = self.FLAG_WAVE_MIDSTR
        elif self.k >= 20:
            self.waverangeflag = self.FLAG_WAVE_MIDWEAK
        else:
            self.waverangeflag = self.FLAG_WAVE_WEAK
            
        if np.isnan(self.cciw) :
            #no weekly data enough
            self.waveboundflag = self.FLAG_WAVE_NOENOUGH
        elif self.cciw >= 100:
            self.waveboundflag = self.FLAG_WAVE_STRONG
        elif self.cciw >= 0:
            self.waveboundflag = self.FLAG_WAVE_MIDSTR
        elif self.cciw >= -100:
            self.waveboundflag = self.FLAG_WAVE_MIDWEAK
        else:
            self.waveboundflag = self.FLAG_WAVE_WEAK
        
    def getWaveEnough(self):
        if self.waverangeflag == self.FLAG_WAVE_NOENOUGH or self.waveboundflag == self.FLAG_WAVE_NOENOUGH:
            return False
        else:
            return True
            
    def getScore(self, ref=0):
        if len(self.scorerangedeque) < ref+1:
            return -1
        return self.scorerangedeque[-1-ref]
    
    def getScoreMa(self, period=3, ref=0):
        if period+ref <= 1 or period+ref > len(self.scorerangedeque):
            return -1
        if ref == 0:
            ma = self.scorerangedeque[-period:]
        else:
            ma = self.scorerangedeque[-period-ref:-ref]
        if len(ma) <= 0:
            return 0
        return np.mean(np.array(ma))
    
    def getScoreBBI(self):
        bbilist = []
        for i in range(0, len(self.FIB_ARRAY)):
            mafib = self.getScoreMa(self.FIB_ARRAY[i])
            if mafib > 0:
                bbilist.append(mafib)
        if len(bbilist) <= 0:
            return 0
        return np.mean(np.array(bbilist))
    
    def getScoreRaise(self):
        #ignore no stable raise
        if not (self.waveenough and self.getWaveEnough()):
            return 0
        scoreref = self.getScore(1)
        if scoreref < 0:
            # no more than raise data
            return 0
        scorecurrent = self.getScore()
        return scorecurrent - scoreref
        
    def getScoreMaRaise(self, period=3):
        #ignore no stable raise
        if not self.waveenough:
            return 0
        scoremaref = self.getScoreMa(period, 1)
        if scoremaref < 0:
            return 0
        scoremacurrent = self.getScoreMa(period)
        return scoremacurrent - scoremaref
    
    def getScoreFibReverter(self):
        fiblist = []
        for i in range(0, len(self.FIB_ARRAY)):
            scorefib = self.getScoreMaRaise(self.FIB_ARRAY[i])
            fiblist.append(scorefib)
        #print fiblist
        return fiblist
        
    def getExcessIndex(self):
        indexscore = 0 if Waver.index == None else Waver.index.getScore()
        return self.getScore() > indexscore
            
    def getScoreMark(self):
        scoremk = ''
        if self.getExcessIndex():
            scoremk += '?'
        else:
            scoremk += '!'
        #wavebound first
        if self.waveboundflag == self.FLAG_WAVE_STRONG:
            scoremk += '^'
        elif self.waveboundflag == self.FLAG_WAVE_WEAK:
            scoremk += 'v'
        elif self.waveboundflag == self.FLAG_WAVE_MIDSTR:
            scoremk += '/'
        elif self.waveboundflag == self.FLAG_WAVE_MIDWEAK:
            scoremk += '\\'
        elif self.waveboundflag == self.FLAG_WAVE_NOENOUGH:
            scoremk += '*'
        else:
            pass
        #waverange second
        if self.waverangeflag == self.FLAG_WAVE_STRONG:
            scoremk += '^'
        elif self.waverangeflag == self.FLAG_WAVE_WEAK:
            scoremk += 'v'
        elif self.waverangeflag == self.FLAG_WAVE_NOENOUGH:
            scoremk += '*'
            return scoremk
        elif self.waverangeflag == self.FLAG_WAVE_MIDSTR:
            scoremk += '+'
        elif self.waverangeflag == self.FLAG_WAVE_MIDWEAK:
            scoremk += '='
        else:
            pass
        #gold cross
        if self.kd >= 0:
            scoremk +='$'
        #wavedirection last
        scoremk += self.TRIGRAMS421R[self.wavedirectflag]['mark']
        return scoremk
     
    def getScoreStr(self):
        scorestr = ''
        scorecurrent = self.getScore()
        if scorecurrent >= 0:
            scorestr += str(self.strdec(scorecurrent))
            socrecurrentbbi = self.getScoreBBI()
            if socrecurrentbbi > 0:
                scorestr += '/'
                scorestr += str(self.strdec(socrecurrentbbi))
        scoreraise = self.getScoreRaise()
        if scoreraise > 0:
            scorestr += '^+' + str(self.strdec(scoreraise))
        if scoreraise < 0:
            scorestr += 'v-' + str(self.strdec(-scoreraise))
        #fiblist = self.getScoreFibReverter()
        #for i in range(0, len(fiblist)):
        #    scorefib = fiblist[i]
        #    if scorefib > 0:
        #        scorestr += 'M'+str(self.FIB_ARRAY[i])+'^+' + str(self.strdec(scorefib))
        #    if scorefib < 0:
        #        scorestr += 'M'+str(self.FIB_ARRAY[i])+'v-' + str(self.strdec(-scorefib))
        return scorestr
        
    def updateDequeScore(self, score, dt, overwrited=False):
        lendequeue = len(self.scorerangedeque)
        #dequeue scorerange
        if overwrited and (not self.sameDay(dt)):
            #flag data enough
            self.waveenough = self.getWaveEnough()
            if lendequeue > 0:
                #update socre to use aftertrade data
                self.scorerangedeque[-1] = score
            #resume a new same data for next begin
            self.scorerangedeque.append(score)
            if lendequeue >= self.MAX_SCORERANGE_DEQUE:
                del self.scorerangedeque[0]
            self.aimed_time = dt
        #update the lastest data
        else:
            if lendequeue == 0:
                self.scorerangedeque.append(score)
            else:
                self.scorerangedeque[-1] = score
        
    @classmethod
    def getWaveRaiseList(cls, poollist, cmpindex=False, pretrade=False):
        if not cmpindex:
            waverslist = poollist[:] if cls.indexPos == 0 else poollist[0:cls.indexPos]
        else:
            waverslist = poollist[:]
        waverslist.sort(key=cmp_to_key(lambda a,b: cls.cmpScoreRaise(a, b, cmpindex, pretrade)))
        return waverslist
    
    @classmethod
    def getWaveSubnewList(cls, poollist):
        return [w for w in poollist if w.waveboundflag == Waver.FLAG_WAVE_NOENOUGH]
    
    @classmethod
    def getBbiList(cls, poollist, cmpindex=False):
        if not cmpindex:
            bbilist = poollist[:] if cls.indexPos == 0 else poollist[0:cls.indexPos]
        else:
            bbilist = poollist[:]
        bbilist.sort(key=cmp_to_key(lambda a,b: cls.cmpBbi(a, b, cmpindex)))
        return bbilist
    
    @classmethod
    def getWaveMaRaiseList(cls, poollist, cmpindex=False):
        if cmpindex:
            wavemarslist = poollist[:] if cls.indexPos == 0 else poollist[0:cls.indexPos]
        else:
            wavemarslist = poollist[:]
        wavemarslist.sort(key=cmp_to_key(lambda a,b: cls.cmpScoreMaRaise(a, b, cmpindex)))
        return wavemarslist
    
    @classmethod
    def getSecurityIndex(cls, poollist, security):
        ret = -1
        for i in range(0, len(poollist)):
            if poollist[i].security() == security:
                ret = i
                break
        return ret
    
    @classmethod
    def updateWaverPoolOrder(cls, poollist, dt, aftertrade=False):
        poollist.sort(key=cmp_to_key(lambda a,b: Waver.cmpitem(a, b, True)))
        poollen = len(poollist)
        cls.logd("updateWaverPoolOrder poollen:%s" %(str(poollen)))
        if poollen <= 1:
            return
        for i in range(0, poollen):
            scorepercent = 100 - 100*1.0/(poollen-1)*i
            #scorepercent = cls.RET_BUY
            poollist[i].updateDequeScore(scorepercent, dt, aftertrade)
        
    @classmethod  
    def updateWaverOtherOrder(cls, poollist, other, dt, aftertrade=False):
        if other == None:
            return
        poollen = len(poollist)
        cls.logd("updateWaverIndexOrder poollen:%s" %(str(poollen)))
        if poollen == 0:
            return
        scorepercent = 0
        for i in range(0, poollen):
            scorecurrent = poollist[i].getScore()
            if scorecurrent < 0:
                continue
            elif poollist[i] >= other:
                scorepercent = scorecurrent
                cls.indexPos = i
                break
        other.updateDequeScore(scorepercent, dt, aftertrade)
        
    @staticmethod
    def getIndexScore():
        if Waver.index == None:
            return 0
        return Waver.strdec(Waver.index.getScore())
    
    @staticmethod
    def refreshWaverPool(context, data, poollist, stocklist, pretrade=False, aftertrade=False, notmain=True):
        Waver.logd("%s refreshWaverPool" %(str(datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S'))))
        if pretrade:
            if len(stocklist) == 0:
                Waver.logd("empty stocklist, pretrade!")
                #return Waver.getIndexScore()
            if len(poollist) == 0:
                Waver.logd("empty poollist! begin to init pool")
            else:
                Waver.logd("poollist has been inited before, begin to refresh")
        callauction = False
        if context == None:
            context = dsobj.GET_CONTEXT()
            Waver.logd("refreshWaverPool for context:%s" %(str(context)))
        runTimeCA = GET_CALLAUCTION_MINUTES(context)
        if runTimeCA >= 0 and runTimeCA < 15:
            Waver.logd("%s refreshWaverPool for callauction" %(str(runTimeCA)))
            callauction = True
        d_count = len(stocklist)
        #init index for avg compare
        if not callauction:
            if Waver.index == None:
                #NO KEEP score dequeue for temp use
                szzs = GET_ALL_INDEXES()[0]
                Waver.index = Waver(context, szzs)
            else:
                Waver.index.refresh(context, data)
        #only refresh for empty stocklist
        if d_count == 0:
            for wave in poollist:
                wave.refresh(context, data, 'D', callauction)
        #add del refresh poollist by stocklist 
        else:
            Waver.logd("begin count:%s" % (d_count))
            d_i = 0
            newadd = []
            todel= []
            toref = []
            #remove no trade security
            for wave in poollist:
                if wave.security() not in stocklist:
                    todel.append(wave.security())
                    #poollist.remove(wave)
                else:
                    toref.append(wave.security())
                    wave.refresh(context, data)
            Waver.logd("len:%s,refresh to todel:%s\n" %(str(len(todel)), str(todel)))
            #inverted order todel
            if len(todel) > 0:
                for i in range(len(poollist)-1, -1, -1):
                    if poollist[i].security() in todel:
                        wave = poollist.pop(i)
                        Waver.logd("poollist del:%s" %(str(wave.security())))
                        todel.remove(wave.security())
            #add on trade security
            newadd = [s for s in stocklist if s not in toref]
            Waver.logd("len:%s,refresh to newadd:%s\n" %(str(len(newadd)), str(newadd)))
            for s in newadd:
                d_i = d_i + 1;
                if d_i % (d_count//100 + 1) == 0:
                    Waver.logd("doing:%s %%" % str(d_i/(d_count//100 + 1)))
                wave = Waver(context, s)
                poollist.append(wave)
            Waver.logd("end count:%s" % len(poollist))
        if not callauction:
            dt = context.current_dt
            Waver.updateWaverPoolOrder(poollist, dt, aftertrade)
            Waver.updateWaverOtherOrder(poollist, Waver.index, dt, aftertrade)
            Waver.logd("shindex:%s,indexPos:%s\n" %(str(Waver.index), str(Waver.indexPos)))
        #print poollist
        #print Waver.index
        #send after trade data for next day
        #Waver.sendWaverPool(context, data, poollist, True, True)
        if pretrade:
            wavefirstlist = [Waver.index] + poollist[0:Waver.MAX_SEND_COUNT]
            wavelastlist = Waver.getWaveSubnewList(poollist)
            sendlist = [wavefirstlist,wavelastlist]
            return Waver.sendWaverPool(context, data, sendlist, False, notmain)
        if aftertrade:
            sendlist = [Waver.index]+poollist
            Waver.sendWaverPool(context, data, sendlist, True, notmain)
            return Waver.getIndexScore()
        
    @staticmethod
    def handleWaverPoolBegin(context, data, poollist, stocklist):
        runTime = GET_RUN_MINUTES(context)
        if runTime != 0:
            return Waver.getIndexScore()
        Waver.refreshWaverPool(context, data, poollist, [])
        #print poollist
        if Waver.HANDLE_SEND:
            #current raise order list
            waverslist = Waver.getWaveRaiseList(poollist, True, True)[0:Waver.MAX_SEND_COUNT/2]
            #current order list tail
            wavelastlist = Waver.getWaveRaiseList(Waver.getWaveSubnewList(poollist), True, True)[0:Waver.MAX_SEND_COUNT/2]
            Waver.sendWaverPool(context, data, [waverslist, wavelastlist], False, True)
            
    @staticmethod
    def handleWaverPoolEnd(context, data, poollist):
        runTime = GET_RUN_MINUTES(context)
        if runTime != 240:
            return Waver.getIndexScore()
        Waver.refreshWaverPool(context, data, poollist, [])
        #print poollist
        if Waver.HANDLE_SEND:
            #current raise order list
            waverslist = Waver.getWaveRaiseList(poollist, True)[0:Waver.MAX_SEND_COUNT*2]
            #ma3 raise order list
            #wavemarslist = Waver.getWaveMaRaiseList(poollist, True)[0:Waver.MAX_SEND_COUNT]
            #bbi order list
            bbilist = [Waver.index] +Waver.getBbiList(poollist, True)[0:Waver.MAX_SEND_COUNT]
            #current all list 
            wavealllist = poollist
            #push order list in once
            Waver.sendWaverPool(context, data, [waverslist, bbilist, wavealllist], False, True)
            
    @staticmethod
    def handleWaverPool(context, data, poollist, sellcb, buycb):
        runTime = GET_RUN_MINUTES(context)
        if runTime % 5 != 0:
            return Waver.getIndexScore()
        Waver.refreshWaverPool(context, data, poollist, [])
        #print poollist
        if Waver.HANDLE_SEND:
            #current raise order list
            waverslist = Waver.getWaveRaiseList(poollist, True)[0:Waver.MAX_SEND_COUNT*2]
            #ma3 raise order list
            #wavemarslist = Waver.getWaveMaRaiseList(poollist, True)[0:Waver.MAX_SEND_COUNT]
            #bbi order list
            bbilist = [Waver.index] +Waver.getBbiList(poollist, True)[0:Waver.MAX_SEND_COUNT]
            #current order list head
            wavefirstlist = poollist[0:Waver.MAX_SEND_COUNT*2]
            #current order list tail
            wavelastlist = Waver.getWaveSubnewList(poollist)
            #push order list in once
            Waver.sendWaverPool(context, data, [waverslist, bbilist, wavelastlist, wavefirstlist], False, True)
        return Waver.getIndexScore()
    
    @staticmethod
    def sendWaverPool(context, data, poollist, aftertrade=False, sendMail=False):
        Waver.logd("%s sendWaverPool" %(str(datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S'))))
        #REDSTAR_ORDERSP_NORMAL = '?'
        #REDSTAR_ORDERSP_INDEX = '!'
        #REDSTAR_DEL = '-'
        #REDSTAR_FIRE = '$'
        def redStar(security, idx, bundle, mutiindex=-1):
            if mutiindex >= 0:
                wave = poollist[mutiindex][idx]
            else:
                wave = poollist[idx]
            rs = ''
            rs += wave.getScoreMark()
            rs += wave.getScoreStr()
            bundle['name'] += rs
        sendlist = []
        if len(poollist) > 0 and isinstance(poollist[0], list):
            for muti in poollist:
                mutilist = [s.security() for s in muti]
                sendlist.append(mutilist)
        else:
            sendlist = [s.security() for s in poollist]
        return DSUtil.sendSecurities(context, data, sendlist, False, sendMail, aftertrade, redStar)
    
    # for local handle
    gstocks = []
    gpoolfd = []
    
    @staticmethod
    def handle(context=None, stocklist=None):
        if context == None:
            context = dsobj.GET_CONTEXT()
            Waver.logd("Waver handle for context:%s" %(str(context)))
        data = {}
        if stocklist:
            Waver.gstocks = stocklist
        if len(Waver.gstocks) == 0:
            Waver.gstocks = GET_ALL_SECURITIES()
            return Waver.refreshWaverPool(context, data, Waver.gpoolfd, Waver.gstocks, True)
        Waver.refreshWaverPool(context, data, Waver.gpoolfd, [])
        waverslist = Waver.getWaveRaiseList(Waver.gpoolfd, True)[0:Waver.MAX_SEND_COUNT]
        #ignore bbilist for notebook!
        wavefirstlist = [Waver.index] + Waver.gpoolfd[0:Waver.MAX_SEND_COUNT*2]
        #current order list tail
        wavelastlist = Waver.getWaveSubnewList(Waver.gpoolfd)
        #push order list in once
        return Waver.sendWaverPool(context, data, [waverslist, wavelastlist, wavefirstlist], False, False)
    
def cmp_to_key(mycmp):
    """Convert a cmp= function into a key= function"""
    class K(object):
        __slots__ = ['obj']
        def __init__(self, obj):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
        __hash__ = None
    return K

if __name__ == '__main__':
    Waver.logd("run in main");
    #stocklist = GET_ALL_SECURITIES(True, True, 100)
    stocklist = ['600000','000001','600519','601857','002510']
    poollist = []
    context = data = None
    #pre trade for init or update list
    Waver.refreshWaverPool(context, data, poollist, stocklist, True, False, False)
    #9:25 update list
    #Waver.refreshWaverPool(context, data, poollist, stocklist, False, False, False)
    Waver.handleWaverPoolBegin(context, data, poollist, stocklist)
    #intrade
    Waver.handleWaverPool(context, data, poollist, None, None)
    #end trade
    Waver.handleWaverPoolEnd(context, data, poollist)
    #after trade
    Waver.refreshWaverPool(context, data, poollist, stocklist, False, True, False)
    #pre trade next day
    Waver.refreshWaverPool(context, data, poollist, stocklist, True, False, False)
