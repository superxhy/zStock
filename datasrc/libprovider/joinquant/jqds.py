#!/usr/bin/env python
# -*- coding:utf-8 -*- 
'''
Created on 2017-3-8

@author: yuql
'''
#import joinquant api
try:
    from kuanke.user_space_api import *
except Exception as e:
    #may used in notebook!
    print ("%s:%s" %(str(Exception),str(e)))
import numpy as np
import pandas as pd

#from datasrc import * 
#TODO jq not suport root path
from abcbase import *

class JqDatasrc(SecurityDataSrcBase):

    index_list = [
            '000001.XSHG',#[0]上证指数
            '399106.XSHE',#[1]深证综指
            #'399006.XSHE',#[2]创业板指
            ]
    index_dict = {
            index_list[0]:'上证指数',
            index_list[1]:'深证综指',
            }
    industry_dict = {
        'A01':'农林牧渔',#'农业',
        'A02':'农林牧渔',#'林业',
        'A03':'农林牧渔',#'畜牧业',
        'A04':'农林牧渔',#'渔业',
        'A05':'农林牧渔',#'农、林、牧、渔服务业',
        'B06':'煤炭',#'煤炭开采和洗选业',
        'B07':'石油',#'石油和天然气开采业',
        'B08':'矿业开采',#'黑色金属矿采选业',
        'B09':'有色开采',#'有色金属矿采选业',
        'B11':'采掘服务',#'开采辅助活动',
        'C13':'农产品加工',#'农副食品加工业',
        'C14':'食品饮料',#'食品制造业',
        'C15':'酿酒',#'酒、饮料和精制茶制造业',
        'C17':'纺织',#'纺织业',
        'C18':'纺织服饰',#'纺织服装、服饰业',
        'C19':'服装家纺',#'皮革、毛皮、羽毛及其制品和制鞋业',
        'C20':'家用轻工',#'木材加工及木、竹、藤、棕、草制品业',
        'C21':'家居用品',#'家具制造业',
        'C22':'造纸',#'造纸及纸制品业',
        'C23':'广告包装',#'印刷和记录媒介复制业',
        'C24':'文教休闲',#'文教、工美、体育和娱乐用品制造业',
        'C25':'基础化学',#'石油加工、炼焦及核燃料加工业',
        'C26':'化工',#'化学原料及化学制品制造业',
        'C27':'医药',#'医药制造业',
        'C28':'化纤',#'化学纤维制造业',
        'C29':'化学制品',#'橡胶和塑料制品业',
        'C30':'建材',#'非金属矿物制品业',
        'C31':'钢铁',#'黑色金属冶炼及压延加工业',
        'C32':'有色',#'有色金属冶炼和压延加工业',
        'C33':'工业机械',#'金属制品业',
        'C34':'通用机械',#'通用设备制造业',
        'C35':'工程机械',#'专用设备制造业',
        'C36':'汽车类',#'汽车制造业',
        'C37':'非汽交运',#'铁路、船舶、航空航天和其它运输设备制造业',
        'C38':'电气设备',#'电气机械及器材制造业',
        'C39':'通信设备',#'计算机、通信和其他电子设备制造业',
        'C40':'仪器仪表',#'仪器仪表制造业',
        'C41':'其它制造',#'其他制造业',
        'C42':'环境保护',#'废弃资源综合利用业',
        'D44':'电力',#'电力、热力生产和供应业',
        'D45':'燃气',#'燃气生产和供应业',
        'D46':'水务',#'水的生产和供应业',
        'E46':'建筑',#'建筑材料',
        'E47':'建筑',#'房屋建筑业',
        'E48':'建筑',#'土木工程建筑业',
        'E49':'建筑',#'建筑安装业',
        'E50':'建筑装饰',#'建筑装饰和其他建筑业',
        'F51':'商业连锁',#'批发业',
        'F52':'商业连锁',#'零售业',
        'G53':'交通运输',#'铁路运输业',
        'G54':'交通运输',#'道路运输业',
        'G55':'交通运输',#'水上运输业',
        'G56':'交通运输',#'航空运输业',
        'G58':'仓储物流',#'装卸搬运和运输代理业',
        'G59':'仓储物流',#'仓储业',
        'G60':'邮政',#'邮政业',
        'H61':'酒店餐饮',#'住宿业',
        'H62':'酒店餐饮',#'餐饮业',
        'I63':'传媒娱乐',#'电信、广播电视和卫星传输服务',
        'I64':'互联网',#'互联网和相关服务',
        'I65':'软件服务',#'软件和信息技术服务业',
        'J66':'银行',#'货币金融服务',
        'J67':'证券',#'资本市场服务',
        'J68':'保险',#'保险业',
        'J69':'多元金融',#'其他金融业',
        'K70':'房地产',#'房地产业',
        'L71':'其它金融',#'租赁业',
        'L72':'文化传媒',#'商务服务业',
        'M73':'生物制药',#'研究和试验发展',
        'M74':'专业技术',#'专业技术服务业',
        'N77':'环境保护',#'生态保护和环境治理业',
        'N78':'旅游',#'公共设施管理业',
        'P82':'文教休闲',#'教育',
        'Q83':'医疗保健',#'卫生',
        'R85':'文化传媒',#'新闻和出版业',
        'R86':'文化传媒',#'广播、电视、电影和影视录音制作业',
        'R87':'文化传媒',#,'文化艺术业',
        'S90':'综合',#'综合'
    }
    
    def __GET_SECURITY_INFO_BASE__(self, date, filtPaused=False, filtSt=False, filtIndustry=False):
        #today = datetime.date.today() if date==None else date
        # base code,name,displayname
        base = get_all_securities(['stock'])
        mart = get_fundamentals(
                query(valuation.code,          #代码(带后缀.XSHE/.XSHG)
                #valuation.id,                      #
                valuation.day,                     #日期
                valuation.capitalization,          #总股本(万股)
                valuation.circulating_cap,         #流通股本(万股)
                valuation.circulating_market_cap,  #流通市值(亿)
                valuation.market_cap,              #总市值(亿元)
                valuation.pb_ratio,                #市净率
                valuation.pcf_ratio,               #市现率
                valuation.pe_ratio,                #动态市盈率
                valuation.ps_ratio,                #市销率
                valuation.turnover_ratio,          #换手率(%)
                ),date).dropna().set_index('code')
        # join mart in base
        grid = pd.concat([base, mart], axis=1, join='inner')
        # query crew info
        if not filtPaused:
            crew = get_price(list(mart.index), start_date=date, end_date=date, fields=['paused'])
            crew = crew.paused.T
            crew.rename(columns={crew.columns[0]:'paused'}, inplace=True)
            grid = pd.concat([grid, crew], axis=1, join='inner')
        # query pack info
        if not filtSt:
            pack = get_extras('is_st', list(mart.index), start_date=date, end_date=date, df=True)
            pack = pack.T
            pack.rename(columns={pack.columns[0]:'is_st'}, inplace=True)
            grid = pd.concat([grid, pack], axis=1, join='inner')
        # query industry code
        if not filtIndustry:
            grid.loc[:,'industry_code'] = 'None'
            for code in self.industry_dict.keys():
                codepool = []
                try:
                    codepool = get_industry_stocks(code,date)
                except Exception as e:
                    print ("%s:%s" %(str(Exception),str(e)))
                if len(codepool) == 0:
                    continue
                for security in codepool:
                    grid.at[security,'industry_code'] = code
        return grid

    def GET_SECURITY_INFO_BASE(self, date=None):
        if self.__securitybaseinfo__.empty == True:
            context = self.GET_CONTEXT()
            date = context.current_dt
            print("%s GET_SECURITY_INFO_BASE" %(str(date.strftime('%Y-%m-%d-%H%M%S'))))
            self.__securitybaseinfo__ = self.__GET_SECURITY_INFO_BASE__(date)
        return self.__securitybaseinfo__
    
    def GET_SECURITY_DATA_DAY(self, code, date, dataCount=1, fields=None):
        security = normalize_code(code)
        return get_price(security, count=dataCount, end_date=date,fields=fields,frequency='1d',skip_paused=True,fq='pre')
        
    def GET_SECURITY_DATA_MIN(self, code, date, dataCount=1, fields=None):
        security = normalize_code(code)
        return get_price(security, count=dataCount, end_date=date,fields=fields,frequency='1m',skip_paused=True,fq='pre')
        
    def __init__(self, name):
        super(JqDatasrc, self).__init__(name)
        self.__securitybaseinfo__ = pd.DataFrame(columns=['code'])
        
    def getVersionName(self):
        return "1.12.21"
    
    def getDataSrcName(self):
        return "joinquant"
    
    # 获取所有指数代码
    #return list
    def GET_ALL_INDEXES(self):
        return self.index_list
    
    # 获取所有股票代码
    #return list
    def GET_ALL_SECURITIES(self, filtPaused=True, filtSt=True, filtMarketcap=0):
        l_stocks03 = get_index_stocks(self.index_list[0])
        l_stocks04 = get_index_stocks(self.index_list[1])
        l_stocks = l_stocks03 + l_stocks04
        print ("l_stocks %s in all" % (str(len(l_stocks))))
        if filtPaused or filtSt:
            hasCurrent = True
            try:
                #TODO jq not suport root path
                current_data = get_current_data()
            except Exception as e:
                #may used in notebook!
                hasCurrent = False
                #print ("%s:%s" %(str(Exception),str(e)))
            if not hasCurrent:
                basedf = self.GET_SECURITY_INFO_BASE()
                if filtPaused:
                    listpaused = list(basedf[basedf['paused']>0].index)
                    l_stocks = [s for s in l_stocks if not s in listpaused]
                    print ("l_stocks %s after filtPaused" % (str(len(l_stocks))))
                if filtSt:
                    listst = list(basedf[basedf['is_st']==True].index)
                    l_stocks = [s for s in l_stocks if not s in listst]
                    print ("l_stocks %s after filtSt" % (str(len(l_stocks))))
                if filtMarketcap>0:
                    listcap = list(basedf[basedf['circulating_market_cap']>filtMarketcap].index)
                    l_stocks = [s for s in l_stocks if not s in listcap]
                    print ("l_stocks %s after filtMarketcap" % (str(len(l_stocks))))
                return l_stocks
            if filtPaused:
                l_stocks = [s for s in l_stocks if not current_data[s].paused]
                print ("l_stocks %s after filtPaused" % (str(len(l_stocks))))
            if filtSt:
                l_stocks = [s for s in l_stocks if not current_data[s].is_st 
                            and 'ST' not in current_data[s].name
                            and '*' not in current_data[s].name
                            and '退' not in current_data[s].name]
                print ("l_stocks %s after filtSt" % (str(len(l_stocks))))
            if filtMarketcap>0:
                #date=context.current_dt.strftime("%Y-%m-%d")
                df = get_fundamentals(query(
                        valuation.code,valuation.circulating_market_cap
                    ).filter(
                        valuation.code.in_(l_stocks),
                        valuation.circulating_market_cap > filtMarketcap
                    ).order_by(
                        #valuation.circulating_market_cap.asc()
                        # 按市值降序排列
                        valuation.circulating_market_cap.desc()
                    ), date=None
                    ).dropna()
                filtMarketPool = list(df['code'])
                l_stocks = [s for s in l_stocks if not s in filtMarketPool]
                print ("l_stocks %s after filtMarketcap" % (str(len(l_stocks))))
        return l_stocks
    
    # 获取股票信息
    #security
    def GET_SECURITY_INFO(self, security):
        hasCurrent = True
        try:
            #TODO jq not suport root path
            current_data = get_current_data()
        except Exception as e:
            #may used in notebook!
            hasCurrent = False
            current_data = []
            #print ("%s:%s" %(str(Exception),str(e)))
        if not hasCurrent:
            basedf = self.GET_SECURITY_INFO_BASE()
            if security in self.index_list:
                return {'name':self.index_dict[security],'industry':'指数'}
            name  =  basedf.loc[security,'display_name']
            sname =  basedf.loc[security,'name']
            #timeToMarket = basedf.loc[security,'start_date']
            sindustry = basedf.loc[security,'industry_code']
        else:
            info =  get_security_info(security)
            name  = info.display_name
            if security in self.index_list:
                return {'name':name,'industry':'指数'}
            cur = current_data[security]
            sname =  info.name
            #timeToMarket = info.start_date
            sindustry = cur.industry_code
        securityInfo = {
        'name': name,
        'sname': sname,
        #'timeToMarket':datetime.datetime.fromtimestamp(timeToMarket).strftime("%Y-%m-%d"),
        'industry':self.industry_dict.get(sindustry,'行业'+str(sindustry)),
        'sindustry':sindustry}
        return securityInfo
    
    # 获取当前分时收盘价
    def GET_CLOSE_DATA_INTRADAY(self, context, security, data={}, freq=5, dataCount=1):
        run_minutes = self.GET_RUN_MINUTES(context)
        offset = run_minutes % freq
        get_count = dataCount * freq + offset
        ar_data = attribute_history(security, get_count, unit='1m', fields=('close'), skip_paused=True, df=False)
        if ar_data.get('close') is None:
            print ("security:%s in freq:%s NO GET_CLOSE_DATA_INTRADAY!" %(str(security),str(freq)))
            return np.array([np.nan])
        return self.GET_CLOSE_DATA_INTRADAY_DF(context, security, data, freq, ar_data)
        
    def GET_CLOSE_DATA_INTRADAY_DF(self, context, security, data, freq, ar_data):
        run_minutes = self.GET_RUN_MINUTES(context)
        offset = run_minutes % freq
        intra = (freq-1 if offset == 0 else offset-1)
        closeMin = ar_data['close']
        dataCount = len(closeMin)//freq
        closeLast = closeMin[-1]
        if run_minutes==240:
            closeLast = self.GET_CLOSE_DAY(context, security, 0, data)
        if run_minutes==0:
            close_intraday = self.SIMPLE_DATA(closeMin, dataCount-1, freq, 0)
            closeLast = self.GET_CLOSE_DAY(context, security, 0, data)
        else:
            close_intraday = self.SIMPLE_DATA(closeMin, dataCount-1, freq, intra+1)
        close_intraday = np.append(close_intraday, closeLast)
        return close_intraday

    # 获取当前分时最高价
    def GET_HIGH_DATA_INTRADAY(self, context, security, data={}, freq=5, dataCount=1):
        run_minutes = self.GET_RUN_MINUTES(context)
        offset = run_minutes % freq
        get_count = dataCount * freq + offset
        ar_data = attribute_history(security, get_count, unit='1m', fields=('high'), skip_paused=True, df=False)
        if ar_data.get('high') is None:
            print ("security:%s in freq:%s NO GET_HIGH_DATA_INTRADAY!" %(str(security),str(freq)))
            return np.array([np.nan])
        return self.GET_HIGH_DATA_INTRADAY_DF(context, security, data, freq, ar_data)
        
    def GET_HIGH_DATA_INTRADAY_DF(self, context, security, data, freq, ar_data):
        run_minutes = self.GET_RUN_MINUTES(context)
        offset = run_minutes % freq
        intra = (freq-1 if offset == 0 else offset-1)
        highMin = ar_data['high']
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
    
    # 获取当前分时最低价
    def GET_LOW_DATA_INTRADAY(self, context, security, data={}, freq=5, dataCount=1):
        run_minutes = self.GET_RUN_MINUTES(context)
        offset = run_minutes % freq
        get_count = dataCount * freq + offset
        ar_data = attribute_history(security, get_count, unit='1m', fields=('low'), skip_paused=True, df=False)
        if ar_data.get('low') is None:
            print ("security:%s in freq:%s NO GET_LOW_DATA_INTRADAY!" %(str(security),str(freq)))
            return np.array([np.nan])
        return self.GET_LOW_DATA_INTRADAY_DF(context, security, data, freq, ar_data)
        
    def GET_LOW_DATA_INTRADAY_DF(self, context, security, data, freq, ar_data):
        run_minutes = self.GET_RUN_MINUTES(context)
        offset = run_minutes % freq
        intra = (freq-1 if offset == 0 else offset-1)
        lowMin = ar_data['low']
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
    
    # 获取当前分时成交量
    def GET_VOL_DATA_INTRADAY(self, context, security, data={}, freq=5, dataCount=1):
        run_minutes = self.GET_RUN_MINUTES(context)
        offset = run_minutes % freq
        intra = (freq-1 if offset == 0 else offset-1)
        get_count = dataCount * freq + offset
        volMin = 0.01*attribute_history(security, get_count, unit='1m', fields=('volume'), skip_paused=True, df=False)['volume']
        volLast = volMin[-1]
        if np.isnan(volLast):
            return np.array([np.nan])
        if run_minutes==240:
            volLast += volMin[-1]*2.5
        if run_minutes==0:
            #TODO: no support 9:25 vol?
            #volLast = 0.01*get_current_data()[security].volume
            #amountLast = 0.01*get_current_data()[security].money
            volLast = 0
            #self.data[security]={'volume':volLast,'amount':amountLast} 
            vol_intraday = self.SIMPLE_DATA_SUM(volMin, dataCount, freq, offset)
        else:
            #TODO mock open data vol
            volMin[0] = 0
            volMin[1] = volMin[1]*2.0
            vol_intraday = self.SIMPLE_DATA_SUM(volMin, dataCount, freq, intra)
            volLast += np.sum(volMin[-intra:])
        vol_intraday = np.append(vol_intraday, volLast)
        return vol_intraday
    
    def GET_HIGH_DAY(self, context, security, ref=0, data={}):
        bcontext = self.IS_INNER_CONTEXT(context)
        if bcontext:
            return super(JqDatasrc, self).GET_HIGH_DAY(context, security, ref, data)
        if ref==0:
            run_minutes = self.GET_RUN_MINUTES(context)
            if run_minutes == 0:
                return self.GET_CLOSE_DAY(context, security, 0)
            highData = attribute_history(security, run_minutes, unit='1m', fields=('high'), skip_paused=True, df=False)['high']
            #highLast = MAX_CN(highData,run_minutes)
            highLast = highData.max()
            if run_minutes==240:
                curLast = get_current_data()[security].last_price
                if not np.isnan(curLast) and curLast > highLast:
                    highLast = curLast
            return highLast
        else:
            #df True 倒序
            return attribute_history(security, ref, '1d', ('high'), True)['high'][0]
            
    def GET_LOW_DAY(self, context, security, ref=0, data={}):
        bcontext = self.IS_INNER_CONTEXT(context)
        if bcontext:
            return super(JqDatasrc, self).GET_LOW_DAY(context, security, ref, data)
        if ref==0:
            run_minutes = self.GET_RUN_MINUTES(context)
            if run_minutes == 0:
                return self.GET_CLOSE_DAY(context, security, 0)
            lowData = attribute_history(security, run_minutes, unit='1m', fields=('low'), skip_paused=True, df=False)['low']
            #highLast = MIN_CN(lowData,run_minutes)
            lowLast = lowData.min()
            if run_minutes==240:
                curLast = get_current_data()[security].last_price
                if not np.isnan(curLast) and curLast < lowLast:
                    lowLast = curLast
            return lowLast
        else:
            #df True 倒序
            return attribute_history(security, ref, '1d', ('low'), True)['low'][0]
            
    def GET_OPEN_DAY(self, context, security, ref=0):
        bcontext = self.IS_INNER_CONTEXT(context)
        if bcontext:
            dataCount =  ref + 1
            df_data = self.GET_SECURITY_DATA_DAY(security, bcontext.getenddate(), dataCount, ('open'))
            if df_data.empty == True:
                print ("security:%s NO GET_OPEN_DAY!" %(str(security)))
                return np.array([np.nan])
            daylist = list(df_data.index)
            bcontext.setcurrent_dt(daylist[-1])
            d_open = list(df_data['open'])
            if len(d_open) == 0 or np.isnan(d_open[-1]):
                return np.nan
            if len(d_open) < ref + 1:
                return np.nan
            return d_open[-ref]
        if ref==0:
            run_minutes = self.GET_RUN_MINUTES(context)
            if run_minutes == 0:
                return self.GET_CLOSE_DAY(context, security, 0)
            return get_current_data()[security].day_open
        else:
            #df True 倒序
            return attribute_history(security, ref, '1d', ('open'), True)['open'][0]
        
    # 获取日线历史数据最大值
    def GET_HIGH_DATA_DAY(self, context,security,isLastest=True,data={},dataCount=1):
        bcontext = self.IS_INNER_CONTEXT(context)
        if bcontext:
            df_data = self.GET_SECURITY_DATA_DAY(security, bcontext.getenddate(), dataCount, ('high'))
            if df_data.empty == True:
                print ("security:%s NO GET_HIGH_DATA_DAY!" %(str(security)))
                return np.array([np.nan])
            daylist = list(df_data.index)
            bcontext.setcurrent_dt(daylist[-1])
            return np.array(list(df_data['high']))
        ar_data = attribute_history(security, dataCount, unit='1d', fields=('high'), skip_paused=True, df=False)
        if ar_data.get('high') is None:
            print ("security:%s in context:%s NO GET_HIGH_DATA_DAY!" %(str(security),str(context)))
            return np.array([np.nan])
        return self.GET_HIGH_DATA_DAY_DF(context, security, isLastest, data, ar_data)
    
    def GET_HIGH_DATA_DAY_DF(self, context,security,isLastest,data,ar_data):
        high = ar_data['high']
        if not isLastest:
            return high
        else:
            highDay = high[1:]
            run_minutes = self.GET_RUN_MINUTES(context)
            if run_minutes == 0:
                #highLast = attribute_history(security, 1, unit='1m', fields=('high'), skip_paused=True, df=False)['high']
                highLast = self.GET_CLOSE_DAY(context, security, 0)
            else:
                highData = attribute_history(security, run_minutes, unit='1m', fields=('high'), skip_paused=True, df=False)['high']
                #highLast = MAX_CN(highData,run_minutes)
                highLast = highData.max()
                if run_minutes==240:
                    curLast = get_current_data()[security].last_price
                    if not np.isnan(curLast) and curLast > highLast:
                        highLast = curLast
            if not np.isnan(highLast):
                highDay = np.append(highDay,highLast)
            return highDay
    
    # 获取日线历史数据最小值
    def GET_LOW_DATA_DAY(self, context,security,isLastest=True,data={},dataCount=1):
        bcontext = self.IS_INNER_CONTEXT(context)
        if bcontext:
            df_data = self.GET_SECURITY_DATA_DAY(security, bcontext.getenddate(), dataCount, ('low'))
            if df_data.empty == True:
                print ("security:%s NO GET_LOW_DATA_DAY!" %(str(security)))
                return np.array([np.nan])
            daylist = list(df_data.index)
            bcontext.setcurrent_dt(daylist[-1])
            return np.array(list(df_data['low']))
        ar_data = attribute_history(security, dataCount, unit='1d', fields=('low'), skip_paused=True, df=False)
        if ar_data.get('low') is None:
            print ("security:%s in context:%s NO GET_LOW_DATA_DAY!" %(str(security),str(context)))
            return np.array([np.nan])
        return self.GET_LOW_DATA_DAY_DF(context, security, isLastest, data, ar_data)
    
    def GET_LOW_DATA_DAY_DF(self, context,security,isLastest,data,ar_data):
        low = ar_data['low']
        if not isLastest:
            return low
        else:
            lowDay = low[1:]
            run_minutes = self.GET_RUN_MINUTES(context)
            if run_minutes == 0:
                #lowLast = attribute_history(security, 1, unit='1m', fields=('low'), skip_paused=True, df=False)['low']
                lowLast = self.GET_CLOSE_DAY(context, security, 0)
            else:
                lowData = attribute_history(security, run_minutes, unit='1m', fields=('low'), skip_paused=True, df=False)['low']
                #highLast = MIN_CN(lowData,run_minutes)
                lowLast = lowData.min()
                if run_minutes==240:
                    curLast = get_current_data()[security].last_price
                    if not np.isnan(curLast) and curLast < lowLast:
                        lowLast = curLast
            if not np.isnan(lowLast):
                lowDay = np.append(lowDay,lowLast)
            return lowDay

    
    # 获取当前日线或ref天前收盘价
    def GET_CLOSE_DAY(self, context, security, ref=0 ,data={}):
        bcontext = self.IS_INNER_CONTEXT(context)
        if bcontext:
            return super(JqDatasrc, self).GET_CLOSE_DAY(context, security, ref, data)
        if ref == 0:
            run_minutes = self.GET_RUN_MINUTES(context)
            if run_minutes==0:
                auction_minutes = self.GET_CALLAUCTION_MINUTES(context)
                #pre auction use yestoday close
                if auction_minutes < 10:
                    closeLast = np.nan
                #call auction end to pull day_open
                elif auction_minutes < 15:
                    closeLast = get_current_data()[security].day_open
                #use ontrade data
                else:
                    closeLast = get_current_data()[security].day_open
                    if np.isnan(closeLast):
                        closeLast = get_current_data()[security].last_price
                if np.isnan(closeLast):
                    closeLast = self.GET_CLOSE_DAY(context, security, 1, data)
            elif run_minutes==240:
                closeLast = get_current_data()[security].last_price
            else:
                try:
                    closeLast = data[security].close
                except Exception as e:
                    closeLast = attribute_history(security, 1,'1m', ('close'), True)['close'][0]
            return closeLast
        #elif ref == 1:
        #    run_minutes = self.GET_RUN_MINUTES(context)
        #    if run_minutes > 0:
        #        try:
        #            closeLast = data[security].pre_close
        #        except Exception as e:
        #            closeLast = attribute_history(security, 1,'1d', ('close'), True)['close'][0]
        #    else:
        #        closeLast = attribute_history(security, 1,'1d', ('close'), True)['close'][0]
        #    return closeLast
        else:
            #df True 倒序
            return attribute_history(security, ref, '1d', ('close'), True)['close'][0]
    
    def GET_PERIOD_DATA_DAY(self,context, security, data={}, dataCount=1):
        bcontext = self.IS_INNER_CONTEXT(context)
        if bcontext:
            df_data = self.GET_SECURITY_DATA_DAY(security, bcontext.getenddate(), dataCount, None)
            if df_data.empty == True:
                print ("security:%s NO GET_PERIOD_DATA_DAY!" %(str(security)))
                return np.array([np.nan])
            daylist = list(df_data.index)
            bcontext.setcurrent_dt(daylist[-1])
            return np.array(list(df_data['high'])), np.array(list(df_data['low'])) ,np.array(list(df_data['close']))
        return super(JqDatasrc, self).GET_PERIOD_DATA_DAY(context, security, data, dataCount)
    
    # 获取日线历史数据
    def GET_CLOSE_DATA_DAY(self, context, security, isLastest=True,data={},dataCount=20):
        bcontext = self.IS_INNER_CONTEXT(context)
        if bcontext:
            df_data = self.GET_SECURITY_DATA_DAY(security, bcontext.getenddate(), dataCount, ('close'))
            if df_data.empty == True:
                print ("security:%s NO GET_PERIOD_DATA_DAY!" %(str(security)))
                return np.array([np.nan])
            daylist = list(df_data.index)
            bcontext.setcurrent_dt(daylist[-1])
            return np.array(list(df_data['close']))
        ar_data = attribute_history(security, dataCount, unit='1d', fields=('close'), skip_paused=True, df=False)
        if ar_data.get('close') is None:
            print ("security:%s NO GET_CLOSE_DATA_DAY!" %(str(security)))
            return np.array([np.nan])
        return self.GET_CLOSE_DATA_DAY_DF(context, security, isLastest, data, ar_data)
    
    def GET_CLOSE_DATA_DAY_DF(self, context, security, isLastest,data,ar_data):
        close = ar_data['close']
        if not isLastest:
            return close
        else:
            closeDay = close[1:]
            closeLast = self.GET_CLOSE_DAY(context, security, 0, data)
            if not np.isnan(closeLast):
                closeDay = np.append(closeDay,closeLast)
            return closeDay
    
    def GET_PERIOD_DATA_MIN(self,context, security, data={}, dataCount=1, hasVol=False):
        bcontext = self.IS_INNER_CONTEXT(context)
        if bcontext:
            df_data = self.GET_SECURITY_DATA_MIN(security, bcontext.getenddate(), dataCount, None)
            if df_data.empty == True:
                print ("security:%s NO GET_PERIOD_DATA_DAY!" %(str(security)))
                return np.array([np.nan])
            daylist = list(df_data.index)
            bcontext.setcurrent_dt(daylist[-1])
            if hasVol:
                return np.array(list(df_data['high'])), np.array(list(df_data['low'])) ,np.array(list(df_data['close'])), np.array(list(df_data['volume']))
            else:
                return np.array(list(df_data['high'])), np.array(list(df_data['low'])) ,np.array(list(df_data['close']))
        ar_data = attribute_history(security, dataCount, unit='1m', fields=('close','high','low'), skip_paused=True, df=False)
        if ar_data.get('close') is None or ar_data.get('high') is None or ar_data.get('low') is None:
            return np.array([np.nan]),np.array([np.nan]),np.array([np.nan])
        return ar_data['high'], ar_data['low'] ,ar_data['close']
        
    # 获取日线周线月线收盘价历史数据
    def GET_CLOSE_DATA(self, context,security,isLastest=True,data={},dataCount=180*20):
        close = attribute_history(security, dataCount, unit='1d', fields=('close'), skip_paused=True, df=False)['close']
        weekday = context.current_dt.isoweekday()
        day = context.current_dt.day
        count = dataCount/20
        closeDay = close
        closeMonth = self.SIMPLE_DATA(close,count,20,day-1)
        closeWeek = self.SIMPLE_DATA(close,count,5,weekday-1)
        if not isLastest:
            return closeDay, closeMonth, closeWeek
        else:
            try:
                closeLast = data[security].close
            except Exception as e:
                closeLast = attribute_history(security, 1,'1m', ('close'), True)['close'][0]
            if not np.isnan(closeLast) and closeLast != 0:
                closeDay = np.append(closeDay,closeLast)
                closeMonth = np.append(closeMonth,closeLast)
                closeWeek= np.append(closeWeek,closeLast)
            return closeDay, closeMonth, closeWeek

    # 获取当前日线或ref天前成交量
    def GET_VOL_DAY(self, context, security, ref=0 ,data={}):
        bcontext = self.IS_INNER_CONTEXT(context)
        if bcontext:
            return super(JqDatasrc, self).GET_VOL_DAY(context, security, ref, data)
        if ref == 0:
            run_minutes = self.GET_RUN_MINUTES(context)
            if run_minutes == 0:
                #TODO: no support 9:25 vol?
                #volLast = 0.01*get_current_data()[security].volume
                #amountLast = 0.01*get_current_data()[security].money
                volumeLast = 0
                #self.data[security]={'volume':volumeLast,'amount':amountLast} 
            else:
                volumeMin =  0.01*attribute_history(security, run_minutes, unit='1m', fields=('volume'), skip_paused=True, df=False)['volume']
                volumeMin[0] = 0
                volumeLast = np.sum(volumeMin)
                dataJj = self.data.get(security,None)
                if dataJj:
                    #print volumeLast
                    volumeLast += dataJj['volume']
                    #print volumeLast
                else:
                    #TODO mock open data vol
                    volumeLast += volumeMin[1]*2.0
                    if run_minutes == 240:
                        if context.run_params.type == 'simple_backtest' or context.run_params.type == 'full_backtest':
                            #backtest can get close data
                            pass
                        else:
                            volumeLast += volumeMin[-1]*2.5
            return volumeLast
        else:
            #df True 倒序
            return attribute_history(security, ref, '1d', ('volume'), True)['volume'][0]

    # 获取日线历史成交量
    def GET_VOL_DATA_DAY(self, context, security,isLastest=True,data={},dataCount=20):
        bcontext = self.IS_INNER_CONTEXT(context)
        if bcontext:
            df_data = self.GET_SECURITY_DATA_DAY(security, bcontext.getenddate(), dataCount, ('volume'))
            if df_data.empty == True:
                print ("security:%s NO GET_VOL_DATA_DAY!" %(str(security)))
                return np.array([np.nan])
            daylist = list(df_data.index)
            bcontext.setcurrent_dt(daylist[-1])
            return np.array(list(df_data['volume']))
        volume = 0.01*attribute_history(security, dataCount, unit='1d', fields=('volume'), skip_paused=True, df=False)['volume']
        if not isLastest:
            return volume
        else:
            volumeLast = 0
            volumeDay = volume
            run_minutes = self.GET_RUN_MINUTES(context)
            if run_minutes == 0:
                #TODO: no support 9:25 vol?
                #volLast = 0.01*get_current_data()[security].volume
                #amountLast = 0.01*get_current_data()[security].money
                volumeLast = 0
                #self.data[security]={'volume':volumeLast,'amount':amountLast} 
            else:
                volumeMin =  0.01*attribute_history(security, run_minutes, unit='1m', fields=('volume'), skip_paused=True, df=False)['volume']
                volumeMin[0] = 0
                volumeLast = np.sum(volumeMin)
                dataJj = self.data.get(security,None)
                if dataJj:
                    #print volumeLast
                    volumeLast += dataJj['volume']
                    #print volumeLast
                else:
                    #TODO mock open data vol
                    volumeLast += volumeMin[1]*2.0
                    if run_minutes == 240:
                        volumeLast += volumeMin[-1]*2.5
            if not np.isnan(volumeLast):
                volumeDay = np.append(volume,volumeLast)
            return volumeDay

    # 获取日线历史成交额
    def GET_AMOUNT_DATA_DAY(self, context, security,isLastest=True,data={},dataCount=20):
        bcontext = self.IS_INNER_CONTEXT(context)
        if bcontext:
            df_data = self.GET_SECURITY_DATA_DAY(security, bcontext.getenddate(), dataCount, ('money'))
            if df_data.empty == True:
                print ("security:%s NO GET_HIGH_DATA_DAY!" %(str(security)))
                return np.array([np.nan])
            daylist = list(df_data.index)
            bcontext.setcurrent_dt(daylist[-1])
            return np.array(list(df_data['money']))
        amount = attribute_history(security, dataCount, unit='1d', fields=('money'), skip_paused=True, df=False)['money']
        if not isLastest:
            return amount
        else:
            amountLast = 0
            amountDay = amount
            run_minutes = self.GET_RUN_MINUTES(context)
            if run_minutes == 0:
                #TODO: no support 9:25 vol?
                #volLast = 0.01*get_current_data()[security].volume
                #amountLast = 0.01*get_current_data()[security].money
                amountLast = 0
                #self.data[security]={'volume':volumeLast,'amount':amountLast} 
            else:
                amountMin = attribute_history(security, run_minutes-1, unit='1m', fields=('money'), skip_paused=True, df=False)['money']
                #TODO mock open data vol
                amountMin[0] = 0
                amountLast = np.sum(amountMin)
                dataJj = self.data.get(security,None)
                if dataJj:
                    #print amountLast
                    amountLast += dataJj['amount']
                    #print amountLast
                else:
                    amountLast += amountMin[1]*2.0
                    if run_minutes == 240:
                        amountLast += amountMin[-1]*2.5
            if not np.isnan(amountLast):
                amountDay = np.append(amount,amountLast)
            return amountDay
    
    # other for config-----------------------
    def getConfigLoader(self):
        return JqConfigLoader()
    
import json  
class JqConfigLoader(object):
    
    def __init__(self):
        self.__emailconfigf__ = 'emailconfig.json'
        self.__obsererconfigf__ = 'obsererconfig.json'
        #self.__xxconfig__ = 
        
    def getEmailConfig(self):
        try:
            config = read_file(self.__emailconfigf__)
            configobj = json.loads(config)
        except Exception as e:
            print ("%s:%s" %(str(Exception),str(e)))
            configobj = {}
        finally:
            return configobj
    
    def getObserverConfig(self):
        try:
            config = read_file(self.__obsererconfigf__)
            configobj = json.loads(config)
        except Exception as e:
            print ("%s:%s" %(str(Exception),str(e)))
            configobj = {}
        finally:
            return configobj
    
    def getRunConfig(self,context):
        params = context.run_params
        config = {
            'start_date' : params.start_date, #回测/模拟开始日期, datetime.date对象
            'end_date' : params.end_date,  #回测/模拟结束日期, datetime.date对象
            'type' :params.type, #simple_backtest’: 回测, 通过点击’编译运行’运行 full_backtest’: 回测, 通过点击’运行回测’运行 sim_trade’: 模拟交易
            'frequency':params.frequency, #运行频率
            'onbacktest': params.type == 'simple_backtest' or params.type == 'full_backtest'
        }
        return config
    #def getXXConfig():
