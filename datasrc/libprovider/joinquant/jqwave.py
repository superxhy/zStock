'''
Created on 2017-8-25

@author: yuql
'''
#version 1207
#性能分析开关
#enable_profile()
#my own lib
from dsadapter import *
from waver import Waver
#import talib as tl

def CONFIG_BASE_INIT():
    # 设定沪深300作为基准
    set_benchmark('000300.XSHG')
    # 开启动态复权模式(真实价格)
    set_option('use_real_price', True)
    # 输出内容到日志 log.info()
    log.info('CONFIG_BASE_INIT')
    # 过滤掉order系列API产生的比error级别低的log
    # log.set_level('order', 'error')
    
def CONFIG_POOL_INIT(context):
    g.debug =''
    g.l_pool_fd = []
    g.fire_fd_max = 3
    #g.stocks = ['002386.XSHE','600295.XSHG','600125.XSHG']
    #g.stocks =['600295.XSHG']
    # 选择所有股票（代码、名称、简称）
    #g.pd_stocks= get_all_securities(['stock'])
    # 000001(股票:平安银行)
    #g.security = g.pd_stocks.index[0]
    #g.security='000001.XSHG'
    #g.security='603333.XSHG'
    #g.security='600149.XSHG'
    #g.security='600802.XSHG'
    #g.security='603330.XSHG'
    #g.security='000065.XSHE'
    
def initialize(context):
    log.info("==> initialize @ %s", str(context.current_dt))
    CONFIG_BASE_INIT()
    CONFIG_POOL_INIT(context)
    # 指定在每天的10:00运行
    run_daily(begin_trading, '9:26')
    run_daily(end_trading, '15:01')
 
def after_code_changed(context):
    log.info("==> after_code_changed @ %s", str(context.current_dt))
    CONFIG_BASE_INIT()
    #CONFIG_POOL_INIT(context)
    
def begin_trading(context):
    log.info("==> begin_trading @ %s", str(context.current_dt))
    curdata = get_current_data()
    Waver.handleWaverPoolBegin(context, curdata, g.l_pool_fd, g.stocks)
    
def end_trading(context):
    curdata = get_current_data()
    log.info("==> end_trading @ %s", str(context.current_dt))
    Waver.handleWaverPoolEnd(context, curdata, g.l_pool_fd)
    
def before_trading_start(context):
    log.info("==> before_trading_start @ %s", str(context.current_dt))
    g.fire_fd_now = 0
    g.fire_fd_value_day = context.portfolio.total_value
    g.fire_fd_value = g.fire_fd_value_day
    g.stocks = GET_ALL_SECURITIES()
    Waver.refreshWaverPool(context, {}, g.l_pool_fd, g.stocks, True)
    
def after_trading_end(context):
    weekday = context.current_dt.isoweekday()
    day = context.current_dt.day
    log.info("==> after_trading_end @ %s weekday %s", str(context.current_dt),weekday)
    indexscore = Waver.refreshWaverPool(context, {}, g.l_pool_fd, g.stocks, False, True)
    record(indexscore=indexscore)
    
# 每个单位时间(如果按天回测,则每天调用一次,如果按分钟,则每分钟调用一次)调用一次
def handle_data(context, data):
    #log.info("==> handle_data @ %s", str(context.current_dt))
    runTime = GET_RUN_MINUTES(context)
    if runTime == 0 and len(g.stocks) == 0:
        g.stocks = GET_ALL_SECURITIES()
        Waver.refreshWaverPool(context, {}, g.l_pool_fd, g.stocks, True)
    def sell(context, security):
        print "sell#################:"+security
        ORDER_SELL(context, security)
    def buy(context, security):
        print "buy##################:"+security
        buy_value = g.fire_fd_value_day/g.fire_fd_max
        #no more value today except high weight 
        if buy_value > g.fire_fd_value:
            buy_value = g.fire_fd_value
        if (g.fire_fd_now < g.fire_fd_max):
            ORDER_BUY(context,security,data[security].close,buy_value)
            g.fire_fd_value -=  buy_value
            g.fire_fd_now += 1
        else:
            log.info("has no more count to buy today:", security)
    indexscore = Waver.handleWaverPool(context, data, g.l_pool_fd, sell, buy)
    if runTime % 5 == 0:
        print "indexscore:"+ str(indexscore)
        
# until func
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
    log.info("security:%s target_value:%s,price:%s" %(security, str(target_value),str(price)))
    MIN_AMOUNT  = 100
    target_amount = int((target_value / price)//MIN_AMOUNT*MIN_AMOUNT)
    log.info("security:%s buy_amount:%s " %(security, str(target_amount)))
    if target_amount == 0:
        return
    target_value = (target_amount+MIN_AMOUNT) * price
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
