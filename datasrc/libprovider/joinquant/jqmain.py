'''
Created on 2017-3-11

@author: yuql
'''
#version 0304
#性能分析开关
enable_profile()
from prettytable import PrettyTable
#my own lib
from dsadapter import *
from dragonfly import FlyDragon
from observer import PresentObserver
#import talib as tl
def CONFIG_POOL_STOCK(context):
    g.debug =''
    # 选择所有股票（代码、名称、简称）
    #g.pd_stocks= get_all_securities(['stock'])
    # 000001(股票:平安银行)
    #g.security = g.pd_stocks.index[0]
    #g.security='000001.XSHG'
    #g.security='603333.XSHG'
    #g.security='002321.XSHE'
    #g.security='600149.XSHG'
    #g.security='600802.XSHG'
    #g.security='603330.XSHG'
    #g.security='000065.XSHE'
    #g.security='600169.XSHG'
    #g.security='600251.XSHG'
    #g.security='603393.XSHG'
    #g.security='000065.XSHE'
    #g.security='603031.XSHG'
    #g.security='601101.XSHG'
    #g.security='300427.XSHE'
    g.security='600802.XSHG'
    g.l_pool_macd = []
    g.l_pool_fd = []
    g.fire_fd_now = 0
    g.fire_fd_max = 3
    log.info("g.security %s", g.security)
    index_list = [
        '000001.XSHG',#[0]上证指数
        '399106.XSHE',#[1]深证综指
        #'399006.XSHE',#[2]创业板指
        ]
    #l_stocks03 = get_index_stocks(index_list[0])
    #l_stocks04 = get_index_stocks(index_list[1])
    #g.l_stocks = l_stocks03 + l_stocks04
    #g.l_stocks = GET_ALL_SECURITIES()
    g.l_stocks = []
    #print g.l_stocks
    log.info("g.l_stocks %s in all", len(g.l_stocks))
    #log.info("g.l_stocks %s", g.l_stocks)
    
def initialize(context):
    log.info("==> initialize @ %s", str(context.current_dt))
    CONFIG_POOL_STOCK(context)
    #REFFRESH_POOL_MACD(context)
    
def before_trading_start(context):
    log.info("==> before_trading_start @ %s", str(context.current_dt))
    BEFORE_POOL_FLY_DRAGON(context)
    g.myob = PresentObserver.getPresentObserver()
    #MODE_MACD(context, stocks1)
    #weekday = context.current_dt.isoweekday()
    #day = context.current_dt.day
    #log.info("==> before_trading_start @ %s weekday %s", str(context.current_dt),weekday)
    #print day
    #print weekday
    #c = attribute_history(g.security, 1,'1m', ('close'), True)['close'][0]
    #print c
    
def after_trading_end(context):
    weekday = context.current_dt.isoweekday()
    stock = g.security
    day = context.current_dt.day
    log.info("==> after_trading_end @ %s weekday %s", str(context.current_dt),weekday)
    #stocks = FILT_PAUSED(FILT_ST(FILT_VALUE(context,g.l_stocks)))
    #stocks1 = FILT_PAUSED(FILT_ST(g.l_stocks))
    #print len(stocks)
    #print len(stocks1)
    stocks2 = GET_ALL_SECURITIES()
    print len(stocks2)
    #test_wavechr(context,['000001.XSHG'])
    #DSUtil.sendSecurities(context, ['000001.XSHG'],True)
    DSUtil.sendSecurities(context, ['000001.XSHG'] + test_speedup(context,stocks2), True)
    return
    #print stocks1
    #print stocks1[:10]
    #vol = GET_VOL_DAY(context, stock, 0)
    #print vol
    #state, keyvalue = BOLL_DAY_STATE(stock)
    #print state
    #print keyvalue
    #return 
    #MODE_MACD(context,stocks1)
    REFFRESH_POOL_MACD(context)
    #REFFRESH_POOL_FLY_DRAGON(context)
    return
    ma10 = MA_N_DAY(stock,10)
    record(ma10=ma10)
    return
    for security in stocks1:
        wr9 = WR_DAY(context, security)
        print wr9
    #record(wr9=wr)
    return
    #test rsi
    rsi = RSI_DATA_DAY(stock,10)
    print rsi
    record(rsi10=rsi[-1])
    return
    closem1 = GET_CLOSE_DATA_INTRADAY(context, stock, {}, 1, 4*12*5)
    closem5 = GET_CLOSE_DATA_INTRADAY(context, stock, {}, 5, 4*12)
    closem60 = GET_CLOSE_DATA_INTRADAY(context, stock, {}, 60, 4)
    print closem1
    print closem5
    print closem60
    record(closem60=closem60[-1])
    return 
    #for security in stocks1:
    upper, middle, lower = BOLL_DATA_DAY(stock)
    print upper
    print middle
    print lower
    #record(upper=upper,lower=lower,mean=middle,price=GET_CLOSE_DAY(stock))
    
    
# 每个单位时间(如果按天回测,则每天调用一次,如果按分钟,则每分钟调用一次)调用一次
def handle_data(context, data):
    #return
    g.myob.observe(context)
    #log.info("==> handle_data @ %s", str(context.current_dt))
    security = g.security
    #vol = GET_VOL_DAY(context, security, 0 , data)
    #print vol
    #volPre = VOL_PRE(context, security, data)
    #print volPre
    #volPv = VOL_PV(context, security, 20, data)
    #print volPv
    #volumePre = VOL_PRE(context, security, data, False)
    #print volumePre
    #volumeMa = MAVOL_N_DAY(context, security, 20, 1, data)
    #print volumeMa
    #minute = context.current_dt.minute
    minute = GET_RUN_MINUTES(context)
    if minute % 30 == 0:
        #test_kdj(context,'000001.XSHG','S')
        #test_wavechr(context,['000001.XSHG'])
        #DSUtil.sendSecurities(context, ['000001.XSHG'],True)
        return
    HANDLE_POOL_FLY_DRAGON(context, data)
    return
    #    log_index_info(context, data)
    #----------- Sample Code --------------------------------------------------/
    #stock = security
    #hData = attribute_history(stock, 180*20, unit='1d'
    #                , fields=('close', 'volume', 'open', 'high', 'low')
    #                , skip_paused=True
    #                , df=False)
    #volume = hData['volume']
    #volume = np.array(volume, dtype='f8')
    #close = hData['close']
    #open = hData['open']
    #high = hData['high']
    #low = hData['low']
    
    #kValue, dValue, jValue = KDJ_CN(high, low, close, 9, 3, 3) 
    #rsiValue = RSI_CN(close, 13) 
    #print close
    #macdDIFF, macdDEA, macd = MACD_CN(close, 12, 26, 9)
    #print macdDIFF
    #print macdDEA
    #print macd

    # 画出上一时间点价格
    #record(kValue=kValue[-1], dValue=dValue[-1], jValue=jValue[-1], rsiValue=rsiValue[-1], macdDIFF=macdDIFF[-1], macdDEA=macdDEA[-1], macd=macd[-1])
    #record(macdDIFF=macdDIFF[-1], macdDEA=macdDEA[-1], macd=macd[-1])
    
    #----------- Sample Code --------------------------------------------------/
    return
    closem5 = GET_CLOSE_DATA_INTRADAY(context, stock, data,5)
    #print closem5
    #record(closem5=closem5[-1])
    
    # 取得过去五天的平均价格
    average_price = data[security].mavg(5, 'close')
    # 取得上一时间点价格
    current_price = data[security].close
    # 取得当前的现金
    cash = context.portfolio.cash

    print current_price
    print closem5
    # 如果上一时间点价格高出五天平均价1%, 则全仓买入
    #if current_price > 1.01*average_price:
        # 用所有 cash 买入股票
    #    order_value(security, cash)
        # 记录这次买入
    #    log.info("Buying %s" % (security))
    # 如果上一时间点价格低于五天平均价, 则空仓卖出
    #elif current_price < average_price and context.portfolio.positions[security].sellable_amount > 0:
        # 卖出所有股票,使这只股票的最终持有量为0
    #    order_target(security, 0)
        # 记录这次卖出
    #    log.info("Selling %s" % (security))


def test_kdj(context,security,period):
    print "test_kdj"
    #security = 'sh'
    #security = '002346'
    #security = '000001.XSHG'
    #close = GET_CLOSE_DATA_INTRADAY(context, security, {}, period, 30)
    #print close
    K,D,J= KDJ_DATA(context,security, period, {}, 30)
    #print K
    #print D
    #print J
    KD = K-D
    KD = np.array([str(s) for s in KD])
    print KD
    record(KD=KD[-1])

def test_wavechr(context,stocks):
    for security in stocks:
        name = GET_SECURITY_INFO(security)['name']
        print "%s %s" % (security, name)
        #wave5 = GET_WAVE_CRYPTO(context,security,5)
        #print wave5
        wave30 = GET_WAVE_CRYPTO(context,security,30)
        print wave30
        waveD = GET_WAVE_CRYPTO(context,security,'D')
        print waveD
        waveW = GET_WAVE_CRYPTO(context,security,'W')
        print waveW
        waveM = GET_WAVE_CRYPTO(context,security,'M')
        print waveM
        waveS = GET_WAVE_CRYPTO(context,security,'S')
        print waveS
        waveY = GET_WAVE_CRYPTO(context,security,'Y')
        print waveY

def test_speedup(context,stocklist):
    d_count = len(stocklist)
    print "MODE_CCI begin count:%s", d_count
    d_i = 0
    ccilist = []
    #tt = ['600000.XSHG']
    for security in stocklist:
        g.debug =  security
        d_i = d_i + 1;
        if d_i % (d_count//100 + 1) == 0:
            print "MODE_CCI doing:%s %%" %str(d_i/(d_count//100 + 1))
        SPEED_TIME = 4
        DATA_COUNT = SPEED_TIME + 1
        cci = CCI_DATA(context,security, 'M', {}, DATA_COUNT)
        #月线不对
        if cci[-1] < 100 or CROSS_LAST_COUNT(cci, 100, True) == 0 or CROSS_LAST_COUNT(cci, 100, True) > SPEED_TIME:
            continue
        cci = CCI_DATA(context,security, 'W', {}, DATA_COUNT)
        #周线不对
        if cci[-1] < 100 or CROSS_LAST_COUNT(cci, 100, True) == 0 or CROSS_LAST_COUNT(cci, 100, True) > SPEED_TIME:
            continue
        cci = CCI_DATA(context,security, 'D', {}, DATA_COUNT)
        #日线不对
        #print cci
        if cci[-1] > 100 and CROSS_LAST_COUNT(cci, 100, True) > SPEED_TIME:
            continue
        #忽略次新股无日线数据
        if np.isnan(cci[-1]):
            #log.info("MODE_CCI security:%s null data Day!", security)
            continue
        #macd period month week day OK
        ccilist.append(security) 
    print "MODE_CCI end count:%s", len(ccilist)
    print len(ccilist)
    print ccilist
    return ccilist
    
# until func
def LOG_TABLE_SECURITY(context, list, name=None):
    if name == None:
        name = 'len=' + str(len(list))
    log.info("TABLE_SECURITY: %s", name)
    table = PrettyTable(["代码", "名称", "现价"])
    table.align["代码"] = "1" 
    table.padding_width = 2 

    for index in list:
        row = []
        row.append(index)
        row.append(get_security_info(index).display_name)
        #row.append(get_security_info(index).name)
        row.append(GET_CLOSE_DAY(index))
        #row.append(str(context.current_dt))
        table.add_row(row)
    log.info(table)
    return table
    

def FILT_PAUSED(stockslist):
    current_data = get_current_data()
    return [s for s in stockslist if not current_data[s].paused]
    
def FILT_ST(stockslist):
    current_data = get_current_data()
    return [s for s in stockslist if not current_data[s].is_st]  
    
def FILT_VALUE(context,stocklist):
    date=context.current_dt.strftime("%Y-%m-%d")
    # 选出低市值的股票，buylist
    df = get_fundamentals(query(
            valuation.code,valuation.market_cap
        ).filter(
            valuation.code.in_(stocklist)
        ).order_by(
            #valuation.market_cap.asc()
            # 按市值降序排列
            valuation.market_cap.desc()
        ), date=date
        ).dropna()
    return list(df['code'])

## 个股止损
def ORDER_STOPLOSS(context,loss=0.07):
    if len(context.portfolio.positions)>0:
        for stock in context.portfolio.positions.keys():
            avg_cost = context.portfolio.positions[stock].avg_cost
            current_price = context.portfolio.positions[stock].price
            if 1 - current_price/avg_cost >= loss:
                log.info(str(stock) + '  跌幅达个股止损线，平仓止损！')
                order_target_value(stock, 0)
                
def ORDER_BUY(context, security, price, value):
    if security in context.portfolio.positions:
        log.info("security:%s has in portfolio", security)
    #target_value = (context.portfolio.cash * percent)/100
    target_value = value
    log.info("security:%s target_value:%s " %(security, str(target_value)))
    target_amount = int((target_value / price)//100*100)
    log.info("security:%s buy_amount:%s " %(security, str(target_amount)))
    if target_amount == 0:
        return
    target_value = target_amount * price
    order_value(security, +target_value)
    
def ORDER_SELL(context, security, percent=100):
    if security not in context.portfolio.positions:
        log.info("security:%s not in portfolio", security)
        return
    p = context.portfolio.positions[security]
    sell_amount = int(p.closeable_amount * percent/100)
    target_amount = p.closeable_amount - sell_amount
    log.info("security:%s sell_amount:%s " %(security, str(target_amount*100)))
    order_target(security, target_amount)
     
def MODE_MACD(context, stocklist):
    d_count = len(stocklist)
    log.info("MODE_MACD begin count:%s", d_count)
    d_i = 0
    macdlist = []
    for security in stocklist:
        #g.debug =  security
        #d_i = d_i + 1;
        #if d_i % (d_count//100 + 1) == 0:
            #log.info("MODE_MACD doing:%s %%", d_i/(d_count//100 + 1))
        close,closeMonth,closeWeek = GET_CLOSE_DATA(context,security,True)
        #忽略无当天数据
        if isnan(close[-1]):
            #log.info("MODE_MACD security:%s null data!", security)
            continue
        macdDIFF, macdDEA, macd = MACD_CN(closeMonth)
        #月线不对
        if macd[-1] < 0 or macdDIFF[-1] < 0:
            continue
        macdDIFF, macdDEA, macd = MACD_CN(closeWeek)
        #周线不对
        if macd[-1] < 0 or macdDIFF[-1] < 0:
            continue
        macdDIFF, macdDEA, macd = MACD_CN(close)
        #日线不对
        if macd[-1] < 0 or macdDIFF[-1] < 0:
            continue
        #忽略次新股无日线数据
        if isnan(macdDIFF[-1]):
            #log.info("MODE_MACD security:%s null data Day!", security)
            continue
        #macd period month week day OK
        macdlist.append(security) 
    log.info("MODE_MACD end count:%s", len(macdlist))
    print macdlist
    return macdlist
    
def REFFRESH_POOL_MACD(context):
    #stocklist = FILT_PAUSED(FILT_ST(FILT_VALUE(context,g.l_stocks)))
    stocklist = FILT_PAUSED(FILT_ST(g.l_stocks))
    lastlist = MODE_MACD(context, stocklist)
    toadd = []
    todel= []
    for security in g.l_pool_macd:
        if security not in lastlist:
            todel.append(security)
    for security in lastlist:
        if security not in g.l_pool_macd:
            toadd.append(security)
            
    #print todel
    msg = ''
    msg = msg + str(LOG_TABLE_SECURITY(context,todel,'del'))
    msg = msg + str(LOG_TABLE_SECURITY(context,toadd,'add'))
    send_message(msg)
    g.l_pool_macd = lastlist
    LOG_TABLE_SECURITY(context,g.l_pool_macd,'g.l_pool_macd')
    #print g.l_pool_macd
    
def REFFRESH_POOL_FLY_DRAGON(context):
    #stocklist = FILT_PAUSED(FILT_ST(FILT_VALUE(context,g.l_stocks)))
    stocklist = FILT_PAUSED(FILT_ST(g.l_stocks))
    #newlist = FlyDragon.getDragonPool(context, [g.security])
    newlist = FlyDragon.getDragonPool(context, stocklist)
    newadd = []
    todel= []
    for fd in newlist:
        if fd not in g.l_pool_fd:
            newadd.append(fd.security())
            
    for fd in g.l_pool_fd:
        if fd.refresh(context):
            if fd in newlist:
                print "exist fd:"+str(fd)
            else:
                newlist.append(fd)
        else:
            todel.append(fd.security())
    msg = ''
    msg = msg + str(LOG_TABLE_SECURITY(context,todel,'todel'))
    #msg = msg + str(LOG_TABLE_SECURITY(context,newadd,'newadd'))
    #send_message(msg)
    
    for fd in newlist:
        if fd.security() in g.l_pool_macd:
            print "%s in macd poll!" % str(fd.security())
            fd.setFlag(1)
    newlist.sort()
    g.l_pool_fd = newlist
    print newlist
    msg = msg + str(LOG_TABLE_SECURITY(context,[s.security() for s in g.l_pool_fd]))
    send_message(msg)

def BEFORE_POOL_FLY_DRAGON(context):
    g.fire_fd_now = 0
    g.fire_fd_value_day = context.portfolio.total_value/(FlyDragon.FLYDAY_MAX - 1)
    g.fire_fd_value = g.fire_fd_value_day 
    list_fd = [s.security() for s in g.l_pool_fd]
    for security in context.portfolio.positions:
        if security not in list_fd:
            log.info("target clean:%s", security)
            order_target(security, 0)
            
def HANDLE_POOL_FLY_DRAGON(context, data):
    for fd in  g.l_pool_fd:
        res = fd.handleTarget(context, data)
        security = fd.security()
        if res < 0 and security in context.portfolio.positions:
            #sell
            ORDER_SELL(context,security)
        if res > 0 and security not in context.portfolio.positions:
            ORDER_BUY(context,security,data[security].close,10000)
            return 
            buy_value = 0
            #try to get a little!
            if res == 1 :
                buy_value = g.fire_fd_value_day/g.fire_fd_max/3
            #can be carefull    
            elif res < 3:
                buy_value = g.fire_fd_value_day/g.fire_fd_max
            #hight weight to show hand!
            else:
                buy_value = g.fire_fd_value_day
            #no more value today except high weight 
            if res < 3 and buy_value > g.fire_fd_value:
                buy_value = g.fire_fd_value
            if (g.fire_fd_now < g.fire_fd_max or res > 1):
                ORDER_BUY(context,security,data[security].close,buy_value)
                g.fire_fd_value -=  buy_value
                g.fire_fd_now += 1
            else:
                log.info("has no more count to buy today:", security)
                
