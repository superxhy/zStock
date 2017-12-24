# zStock
* 0719 add code struct base
* 0721 add main code except testcase
* 1224 wave crypto note book (support py3) DONE !

# Lib Require
```
#osx python2.7
sudo pip install PrettyTable
#tushare require:
sudo pip install request
sudo pip install pandas
sudo pip install lxml
sudo pip install tushare
#sudo pip install tushare --upgrade

#datasrc require:
#c lib support
brew install ta-lib
sudo pip install TA-Lib
```

# Interface
```
# 数据源版本号
@abstractmethod
def getVersionName(self):
    pass
# 数据源名称
@abstractmethod
def getDataSrcName(self):
    pass
'''

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
#context,security, ref=0 ,data={}
def GET_CLOSE_DAY(self):
    pass

@abstractmethod
#context,security,isLastest=True,data={},dataCount=20
# 获取日线历史数据
def GET_CLOSE_DATA_DAY(self):
    pass

@abstractmethod
#context,security,isLastest=True,data={},dataCount=20
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
```
