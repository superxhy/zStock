
# 波浪密码
**by superxhy**
https://github.com/superxhy/zStock


```python
from IPython.display import HTML
from dsadapter import *
from waver import Waver
# lstocks = GET_ALL_SECURITIES()
# context = None
```

    <class 'Exception'>:No module named 'kuanke.user_space_api'
    SecurityDataSrcBase inherit find
    class:<class 'jqds.JqDatasrc'> find inherit baseclazz:<class 'abcbase.SecurityDataSrcBase'>
    joinquant
    1.12.24
    ['BOLL_CN', 'BOLL_DATA_DAY', 'BOLL_DAY', 'BOLL_DAY_STATE', 'BOLL_STATE', 'CCI_CN', 'CCI_DATA', 'CCI_DATA_DAY', 'CCI_DAY', 'CROSS_LAST_COUNT', 'GET_ALL_INDEXES', 'GET_ALL_SECURITIES', 'GET_AMOUNT_DATA_DAY', 'GET_AVG_DATA_DAY', 'GET_BUNDLE', 'GET_CALLAUCTION_MINUTES', 'GET_CLOSE_DATA', 'GET_CLOSE_DATA_DAY', 'GET_CLOSE_DATA_DAY_DF', 'GET_CLOSE_DATA_INTRADAY', 'GET_CLOSE_DATA_INTRADAY_DA', 'GET_CLOSE_DATA_INTRADAY_DF', 'GET_CLOSE_DATA_MONTH', 'GET_CLOSE_DATA_MONTH_DA', 'GET_CLOSE_DATA_SEASON', 'GET_CLOSE_DATA_SEASON_DA', 'GET_CLOSE_DATA_WEEK', 'GET_CLOSE_DATA_WEEK_DA', 'GET_CLOSE_DATA_YEAR', 'GET_CLOSE_DATA_YEAR_DA', 'GET_CLOSE_DAY', 'GET_CONTEXT', 'GET_HIGH_DATA_DAY', 'GET_HIGH_DATA_DAY_DF', 'GET_HIGH_DATA_INTRADAY', 'GET_HIGH_DATA_INTRADAY_DA', 'GET_HIGH_DATA_INTRADAY_DF', 'GET_HIGH_DATA_MONTH', 'GET_HIGH_DATA_MONTH_DA', 'GET_HIGH_DATA_SEASON', 'GET_HIGH_DATA_SEASON_DA', 'GET_HIGH_DATA_WEEK', 'GET_HIGH_DATA_WEEK_DA', 'GET_HIGH_DATA_YEAR', 'GET_HIGH_DATA_YEAR_DA', 'GET_HIGH_DAY', 'GET_INDEXO_CRYPTO', 'GET_INERT_CRYPTO', 'GET_LOW_DATA_DAY', 'GET_LOW_DATA_DAY_DF', 'GET_LOW_DATA_INTRADAY', 'GET_LOW_DATA_INTRADAY_DA', 'GET_LOW_DATA_INTRADAY_DF', 'GET_LOW_DATA_MONTH', 'GET_LOW_DATA_MONTH_DA', 'GET_LOW_DATA_SEASON', 'GET_LOW_DATA_SEASON_DA', 'GET_LOW_DATA_WEEK', 'GET_LOW_DATA_WEEK_DA', 'GET_LOW_DATA_YEAR', 'GET_LOW_DATA_YEAR_DA', 'GET_LOW_DAY', 'GET_OPEN_DAY', 'GET_PERIOD_DATA', 'GET_PERIOD_DATA_DAY', 'GET_PERIOD_DATA_MIN', 'GET_PERIOD_DATA_OLD', 'GET_RUN_MINUTES', 'GET_SECURITY_DATA_DAY', 'GET_SECURITY_DATA_MIN', 'GET_SECURITY_INFO', 'GET_SECURITY_INFO_BASE', 'GET_VOL_CRYPTO', 'GET_VOL_DATA_DAY', 'GET_VOL_DATA_INTRADAY', 'GET_VOL_DATA_INTRADAY_DA', 'GET_VOL_DAY', 'GET_WAVE_CRYPTO', 'HHV_COM', 'IS_INNER_CONTEXT', 'KDJ_CN', 'KDJ_COM', 'KDJ_DATA', 'KDJ_DATA_DAY', 'KDJ_DAY', 'LLV_COM', 'MACD_CN', 'MAVOL_N_DATA_DAY', 'MAVOL_N_DAY', 'MAX_CN', 'MA_CN', 'MA_N_DATA_DAY', 'MA_N_DAY', 'MIN_CN', 'PERCENT_DAY', 'RSI_CN', 'RSI_CN_COM', 'RSI_DATA_DAY', 'RSI_DAY', 'SIMPLE_DATA', 'SIMPLE_DATA_HIGH', 'SIMPLE_DATA_LOW', 'SIMPLE_DATA_SUM', 'SINVOKEMETHODS', 'SMA_CN', 'SMA_COM', 'STD_CN', 'STD_DATA_DAY', 'STD_DAY', 'VOL_PRE', 'VOL_PV', 'WR_CN', 'WR_DATA_DAY', 'WR_DAY', '__GET_SECURITY_INFO_BASE__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__le__', '__lt__', '__metaclass__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__securitybaseinfo__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'calRate', 'data', 'getConfigLoader', 'getDataSrcName', 'getMethodNames', 'getVersionName', 'index_dict', 'index_list', 'industry_dict', 'invokeMethod', 'name']



```python
mdstr,htmstr = Waver.handle()
#print (mdstr)
HTML(htmstr)
```

    Waver<debug>:2017-12-24-202445 refreshWaverPool
    Waver<debug>:refreshWaverPool for context:current_dt:2017-12-24 20:24:45.640968,start_date:2017-12-24 20:24:45.640968,end_date2017-12-24 20:24:45.640968,type:notebook
    Waver<debug>:updateWaverPoolOrder poollen:3456
    Waver<debug>:updateWaverIndexOrder poollen:3456
    Waver<debug>:shindex:000001.XSHG !v=$≡D#4:@7.58%56.36/4:@7.58%56.36|@4?39.33
    ,indexPos:2096
    
    Waver<debug>:2017-12-24-202531 sendWaverPool
    {'name': '上证指数', 'close': 3297.0599999999999, 'vol': ['P#-47.88/0.42|0%1.24E+10:⌈’ 87.28~39.99%26.9', '[±‘v]. ⌊’^. ⌋’^. ⌈‘v. ⌉‘v. ⌊’^. (⌋‘). ⌈’', '[地陽v]. 雷陰^. 澤陰^. 風陽v. 山陽v. 雷陰^. (澤陽). 風陰', [[-6.88, -6.0, -0.45, 10.76], [-5.26, 2.77, 7.74, -9.94]], [-0.68, 8.75]], 'bidx': ['O#13.4%6.48/7.16E+6:ψ 反覆高', '[3.61],-2.59,(3.71)', '5.77‘,3.37’,4.49‘', ['3302.67', '3296.19']], 'wave': ['30#13:B-16.21%39.67/7:A5.02%81.91|@2A10B', 'D#4:@7.58%56.36/4:@7.58%56.36|@4', 'W#11:F-12.13%22.72/3:B2.93%89.0|@ABCDE3F3', 'M#6:A-0.57%81.45/5:A7.54%89.85|@4A2', 'S#1:@6.24%43.7/1:@6.24%43.7|@', 'Y#1:@0.91%39.2/1:@0.91%39.2|@'], 'per': -0.09, 'inert': ['30#2:<=/0.01/0.06%0.05|54.88/47.25~60.16%1.26', 'D#-1:\\>-3.82/2.1%-1.72|45.7/41.27~58.24%2.48', 'W#1:/>v-2.96/-1.65%1.31|32.18/13.42~37.49%6.85'], 'industry': '指数', 'code': '000001'}
    <class 'Exception'>:the JSON object must be str, not 'bytes'
    2017-12-24-202533
    notebook





<div id="mainDiv">
<style>
body,html {
min-height:100%
}body {
-webkit-user-select:none;
,user-select:none;/*background-color:#f5f5f9*/}body,button,input,select,textarea {font-size:.16rem;
line-height:1.5;
color:#000;
font-family:"Helvetica Neue",Helvetica,STHeiTi,sans-serif
}input {
line-height:normal
}
a {
color:#108ee9;
text-decoration:none
}
html {
font-size:100px
}
@media only screen and (min-width:320px) and (max-width:320px) {
html {
font-size:85.33px!important
}
}@media only screen and (min-width:384px) {
html {
font-size:106.67px!important
}
}@media only screen and (min-width:412px) {
html {
font-size:114.44px!important
}
}@media only screen and (min-width:414px) {
html {
font-size:110.4px!important
}
}@media only screen and (min-width:600px) {
html {
font-size:204.8px!important
}
}@media only screen and (min-width:1024px){
html {
font-size:100px!important
}
}
html {
font-family: sans-serif;
-webkit-text-size-adjust: 100%;
-ms-text-size-adjust: 100%;
}
body {
margin: 0;
}table {
border-spacing: 0;
border-collapse: collapse;
}
td,
th {
padding: 0;
}
.table {
width: 100%;
max-width: 100%;
margin-bottom: 20px;
}
.table > thead > tr > th,
.table > tbody > tr > th,
.table > tfoot > tr > th,
.table > thead > tr > td,
.table > tbody > tr > td,
.table > tfoot > tr > td {
padding: 8px;
line-height: 1.42857143;
vertical-align: top;
border-top: 1px solid #ddd;
}
.table > thead > tr > th {
vertical-align: bottom;
border-bottom: 2px solid #ddd;
}
.table > caption + thead > tr:first-child > th,
.table > colgroup + thead > tr:first-child > th,
.table > thead:first-child > tr:first-child > th,
.table > caption + thead > tr:first-child > td,
.table > colgroup + thead > tr:first-child > td,
.table > thead:first-child > tr:first-child > td {
border-top: 0;
}
.table > tbody + tbody {
border-top: 2px solid #ddd;
}
,table .table {
background-color: #fff;
}
table-bordered {
border: 1px solid #ddd;
}
.table-bordered > thead > tr > th,
.table-bordered > tbody > tr > th,
.table-bordered > tfoot > tr > th,
.table-bordered > thead > tr > td,
.table-bordered > tbody > tr > td,
.table-bordered > tfoot > tr > td {
border: 1px solid #ddd;
}
.table-bordered > thead > tr > th,
.table-bordered > thead > tr > td {
border-bottom-width: 2px;
}
.table-striped > tbody > tr:nth-of-type(odd) {
background-color: #f9f9f9;
}
.table-hover > tbody > tr:hover {
background-color: #f5f5f5;
}
</style>
<table style="table-layout: fixed; overflow:hidden" class="table table-striped">
<tr>
<th style="text-align:left">
code
</th>
<th style="text-align:left">
name
</th>
<th style="text-align:left">
industry
</th>
<th style="text-align:left">
close
</th>
<th style="text-align:left">
per
</th>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600917" target="_blank">
600917
</a>

</td>
<td>
重庆燃气?^^$⌈99.62
</td>
<td>
燃气
</td>
<td>
11.18
</td>
<td>
10.04
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603986" target="_blank">
603986
</a>

</td>
<td>
兆易创新?^^$⌉99.36
</td>
<td>
通信设备
</td>
<td>
163.12
</td>
<td>
9.74
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600600" target="_blank">
600600
</a>

</td>
<td>
青岛啤酒?^^$⌊99.02
</td>
<td>
酿酒
</td>
<td>
38.79
</td>
<td>
7.75
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/000729" target="_blank">
000729
</a>

</td>
<td>
燕京啤酒?^^$⌊99.68
</td>
<td>
酿酒
</td>
<td>
6.97
</td>
<td>
6.09
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/000703" target="_blank">
000703
</a>

</td>
<td>
恒逸石化?^^$±99.22
</td>
<td>
化纤
</td>
<td>
20.65
</td>
<td>
5.79
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/601113" target="_blank">
601113
</a>

</td>
<td>
华鼎股份?^^$⌉99.31
</td>
<td>
化纤
</td>
<td>
14.7
</td>
<td>
5.6
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002248" target="_blank">
002248
</a>

</td>
<td>
*ST东数?^^$±99.1
</td>
<td>
通用机械
</td>
<td>
8.13
</td>
<td>
4.1
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300225" target="_blank">
300225
</a>

</td>
<td>
金力泰?^^$⌋99.94
</td>
<td>
化工
</td>
<td>
16.69
</td>
<td>
3.15
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002713" target="_blank">
002713
</a>

</td>
<td>
东易日盛?^^$⌋99.88
</td>
<td>
建筑装饰
</td>
<td>
24.53
</td>
<td>
3.07
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002543" target="_blank">
002543
</a>

</td>
<td>
万和电气?^^$⌋99.83
</td>
<td>
电气设备
</td>
<td>
23.11
</td>
<td>
3.03
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300108" target="_blank">
300108
</a>

</td>
<td>
吉药控股?^^$§98.81
</td>
<td>
医药
</td>
<td>
9.8
</td>
<td>
2.83
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/601899" target="_blank">
601899
</a>

</td>
<td>
紫金矿业?^^$±98.73
</td>
<td>
有色开采
</td>
<td>
4.16
</td>
<td>
2.72
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603032" target="_blank">
603032
</a>

</td>
<td>
德新交运?^^$⌊99.71
</td>
<td>
交通运输
</td>
<td>
54.26
</td>
<td>
2.63
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002493" target="_blank">
002493
</a>

</td>
<td>
荣盛石化?^^$±99.13
</td>
<td>
化纤
</td>
<td>
15.24
</td>
<td>
2.21
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600333" target="_blank">
600333
</a>

</td>
<td>
长春燃气?^=$⌋98.12
</td>
<td>
燃气
</td>
<td>
7.82
</td>
<td>
9.99
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600530" target="_blank">
600530
</a>

</td>
<td>
交大昂立?^=$⌊97.92
</td>
<td>
医药
</td>
<td>
7.37
</td>
<td>
9.67
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002001" target="_blank">
002001
</a>

</td>
<td>
新和成?^=$⌊97.86
</td>
<td>
医药
</td>
<td>
39.31
</td>
<td>
6.59
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603501" target="_blank">
603501
</a>

</td>
<td>
韦尔股份?^=$⌊97.74
</td>
<td>
通信设备
</td>
<td>
43.63
</td>
<td>
6.44
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600661" target="_blank">
600661
</a>

</td>
<td>
新南洋?^=$⌊97.66
</td>
<td>
文教休闲
</td>
<td>
25.45
</td>
<td>
6.09
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603393" target="_blank">
603393
</a>

</td>
<td>
新天然气?^=$⌊97.83
</td>
<td>
燃气
</td>
<td>
42.29
</td>
<td>
5.75
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002267" target="_blank">
002267
</a>

</td>
<td>
陕天然气?^=$§97.4
</td>
<td>
燃气
</td>
<td>
9.24
</td>
<td>
5.6
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/000006" target="_blank">
000006
</a>

</td>
<td>
深振业Ａ?^=$⌉97.25
</td>
<td>
房地产
</td>
<td>
9.85
</td>
<td>
5.46
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600634" target="_blank">
600634
</a>

</td>
<td>
富控互动?^=$⌊97.89
</td>
<td>
互联网
</td>
<td>
19.42
</td>
<td>
5.14
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603938" target="_blank">
603938
</a>

</td>
<td>
三孚股份?^=$≡98.18
</td>
<td>
化工
</td>
<td>
41.97
</td>
<td>
5.03
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/601003" target="_blank">
601003
</a>

</td>
<td>
柳钢股份?^=$≡98.23
</td>
<td>
钢铁
</td>
<td>
7.98
</td>
<td>
4.59
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600378" target="_blank">
600378
</a>

</td>
<td>
天科股份?^=$⌋98.09
</td>
<td>
化工
</td>
<td>
13.65
</td>
<td>
4.12
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603286" target="_blank">
603286
</a>

</td>
<td>
日盈电子?^=$⌊97.68
</td>
<td>
汽车类
</td>
<td>
36.6
</td>
<td>
3.77
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300388" target="_blank">
300388
</a>

</td>
<td>
国祯环保?^=$⌊97.8
</td>
<td>
环境保护
</td>
<td>
23.9
</td>
<td>
3.69
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600593" target="_blank">
600593
</a>

</td>
<td>
大连圣亚?^=$⌊97.63
</td>
<td>
旅游
</td>
<td>
27.29
</td>
<td>
2.44
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300270" target="_blank">
300270
</a>

</td>
<td>
中威电子?^=$⌊97.54
</td>
<td>
通信设备
</td>
<td>
13.12
</td>
<td>
2.26
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600239" target="_blank">
600239
</a>

</td>
<td>
云南城投?^=$±96.85
</td>
<td>
房地产
</td>
<td>
5.22
</td>
<td>
2.15
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600438" target="_blank">
600438
</a>

</td>
<td>
通威股份?/^$≡94.24
</td>
<td>
农产品加工
</td>
<td>
13.15
</td>
<td>
9.31
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/000503" target="_blank">
000503
</a>

</td>
<td>
海虹控股?/^$§93.05
</td>
<td>
互联网
</td>
<td>
44.79
</td>
<td>
5.76
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/000893" target="_blank">
000893
</a>

</td>
<td>
东凌国际?/^$⌉93.66
</td>
<td>
农产品加工
</td>
<td>
9.73
</td>
<td>
5.08
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/000869" target="_blank">
000869
</a>

</td>
<td>
张裕Ａ?/^$⌊93.34
</td>
<td>
酿酒
</td>
<td>
37.82
</td>
<td>
3.62
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002697" target="_blank">
002697
</a>

</td>
<td>
红旗连锁?/^$⌊94.04
</td>
<td>
商业连锁
</td>
<td>
6.38
</td>
<td>
3.07
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002320" target="_blank">
002320
</a>

</td>
<td>
海峡股份?/^$⌊94.01
</td>
<td>
交通运输
</td>
<td>
21.46
</td>
<td>
2.93
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300666" target="_blank">
300666
</a>

</td>
<td>
江丰电子?/^$ψ94.15
</td>
<td>
通信设备
</td>
<td>
71.8
</td>
<td>
2.57
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600183" target="_blank">
600183
</a>

</td>
<td>
生益科技?/^$§93.72
</td>
<td>
通信设备
</td>
<td>
16.68
</td>
<td>
2.52
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/000731" target="_blank">
000731
</a>

</td>
<td>
四川美丰?/^$⌊93.29
</td>
<td>
化工
</td>
<td>
8.22
</td>
<td>
2.24
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600642" target="_blank">
600642
</a>

</td>
<td>
申能股份?/^$⌋94.21
</td>
<td>
燃气
</td>
<td>
5.97
</td>
<td>
2.23
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603689" target="_blank">
603689
</a>

</td>
<td>
皖天然气?/=$⌋91.98
</td>
<td>
燃气
</td>
<td>
17.26
</td>
<td>
10.01
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600856" target="_blank">
600856
</a>

</td>
<td>
中天能源?/=$⌊90.8
</td>
<td>
燃气
</td>
<td>
11.55
</td>
<td>
10.0
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002576" target="_blank">
002576
</a>

</td>
<td>
通达动力?/=$⌊90.59
</td>
<td>
电气设备
</td>
<td>
24.67
</td>
<td>
9.99
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/601222" target="_blank">
601222
</a>

</td>
<td>
林洋能源?/=$⌋91.92
</td>
<td>
仪器仪表
</td>
<td>
10.15
</td>
<td>
9.97
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002015" target="_blank">
002015
</a>

</td>
<td>
霞客环保?/=$⌊90.45
</td>
<td>
纺织
</td>
<td>
8.41
</td>
<td>
9.08
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/601877" target="_blank">
601877
</a>

</td>
<td>
正泰电器?/=$≡92.45
</td>
<td>
电气设备
</td>
<td>
27.0
</td>
<td>
9.0
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/000031" target="_blank">
000031
</a>

</td>
<td>
中粮地产?/=$⌊90.74
</td>
<td>
房地产
</td>
<td>
8.0
</td>
<td>
8.7
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002430" target="_blank">
002430
</a>

</td>
<td>
杭氧股份?/=$≡92.59
</td>
<td>
工程机械
</td>
<td>
14.46
</td>
<td>
7.11
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/601139" target="_blank">
601139
</a>

</td>
<td>
深圳燃气?/=$≡92.56
</td>
<td>
燃气
</td>
<td>
8.79
</td>
<td>
7.06
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/601012" target="_blank">
601012
</a>

</td>
<td>
隆基股份?/=$⌋91.17
</td>
<td>
建材
</td>
<td>
39.07
</td>
<td>
6.84
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/000963" target="_blank">
000963
</a>

</td>
<td>
华东医药?/=$≡92.39
</td>
<td>
商业连锁
</td>
<td>
53.36
</td>
<td>
6.06
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002058" target="_blank">
002058
</a>

</td>
<td>
威尔泰?/=$⌊90.77
</td>
<td>
仪器仪表
</td>
<td>
21.19
</td>
<td>
6.0
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300181" target="_blank">
300181
</a>

</td>
<td>
佐力药业?/=$⌊89.09
</td>
<td>
医药
</td>
<td>
7.42
</td>
<td>
5.85
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600745" target="_blank">
600745
</a>

</td>
<td>
闻泰科技?/=$⌋91.4
</td>
<td>
通信设备
</td>
<td>
35.23
</td>
<td>
5.48
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002648" target="_blank">
002648
</a>

</td>
<td>
卫星石化?/=$⌊90.19
</td>
<td>
化工
</td>
<td>
15.88
</td>
<td>
5.44
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002700" target="_blank">
002700
</a>

</td>
<td>
新疆浩源?/=$≡92.16
</td>
<td>
燃气
</td>
<td>
11.58
</td>
<td>
5.27
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002605" target="_blank">
002605
</a>

</td>
<td>
姚记扑克?/=$⌋91.46
</td>
<td>
文教休闲
</td>
<td>
13.67
</td>
<td>
5.23
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300604" target="_blank">
300604
</a>

</td>
<td>
长川科技?/=$⌊90.48
</td>
<td>
工程机械
</td>
<td>
59.8
</td>
<td>
5.06
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600145" target="_blank">
600145
</a>

</td>
<td>
nan?/=$⌋91.37
</td>
<td>
建材
</td>
<td>
7.4
</td>
<td>
4.96
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002798" target="_blank">
002798
</a>

</td>
<td>
帝王洁具?/=$⌊90.68
</td>
<td>
家居用品
</td>
<td>
53.8
</td>
<td>
4.73
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603595" target="_blank">
603595
</a>

</td>
<td>
东尼电子?/=$⌊90.3
</td>
<td>
通信设备
</td>
<td>
80.84
</td>
<td>
4.61
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300577" target="_blank">
300577
</a>

</td>
<td>
开润股份?/=$⌊90.39
</td>
<td>
纺织
</td>
<td>
62.09
</td>
<td>
4.2
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002313" target="_blank">
002313
</a>

</td>
<td>
日海通讯?/=$⌊89.84
</td>
<td>
通信设备
</td>
<td>
28.0
</td>
<td>
4.09
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002775" target="_blank">
002775
</a>

</td>
<td>
文科园林?/=$⌋91.26
</td>
<td>
建筑
</td>
<td>
21.96
</td>
<td>
4.08
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300274" target="_blank">
300274
</a>

</td>
<td>
阳光电源?/=$≡92.07
</td>
<td>
电气设备
</td>
<td>
19.41
</td>
<td>
4.02
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/000407" target="_blank">
000407
</a>

</td>
<td>
胜利股份?/=$⌈89.61
</td>
<td>
燃气
</td>
<td>
8.1
</td>
<td>
3.98
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600267" target="_blank">
600267
</a>

</td>
<td>
海正药业?/=$ψ90.91
</td>
<td>
医药
</td>
<td>
14.51
</td>
<td>
3.35
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600123" target="_blank">
600123
</a>

</td>
<td>
兰花科创?/=$⌊90.71
</td>
<td>
煤炭
</td>
<td>
9.17
</td>
<td>
3.27
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600216" target="_blank">
600216
</a>

</td>
<td>
浙江医药?/=$⌊90.27
</td>
<td>
医药
</td>
<td>
13.29
</td>
<td>
3.26
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/000096" target="_blank">
000096
</a>

</td>
<td>
广聚能源?/=$⌊90.33
</td>
<td>
商业连锁
</td>
<td>
14.14
</td>
<td>
3.21
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600187" target="_blank">
600187
</a>

</td>
<td>
国中水务?/=$≡92.3
</td>
<td>
水务
</td>
<td>
4.68
</td>
<td>
3.08
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002371" target="_blank">
002371
</a>

</td>
<td>
北方华创?/=$⌊89.9
</td>
<td>
工程机械
</td>
<td>
40.15
</td>
<td>
3.03
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600875" target="_blank">
600875
</a>

</td>
<td>
东方电气?/=$⌊90.25
</td>
<td>
通用机械
</td>
<td>
10.95
</td>
<td>
2.72
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/000786" target="_blank">
000786
</a>

</td>
<td>
北新建材?/=$⌋91.95
</td>
<td>
建材
</td>
<td>
22.77
</td>
<td>
2.61
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/000546" target="_blank">
000546
</a>

</td>
<td>
金圆股份?/=$⌊90.62
</td>
<td>
建材
</td>
<td>
16.96
</td>
<td>
2.48
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002428" target="_blank">
002428
</a>

</td>
<td>
云南锗业?/=$⌊90.36
</td>
<td>
有色
</td>
<td>
11.9
</td>
<td>
2.41
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002025" target="_blank">
002025
</a>

</td>
<td>
航天电器?/=$⌊90.22
</td>
<td>
通信设备
</td>
<td>
21.9
</td>
<td>
2.38
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002061" target="_blank">
002061
</a>

</td>
<td>
浙江交科?/=$≡92.04
</td>
<td>
化工
</td>
<td>
15.29
</td>
<td>
2.21
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/000695" target="_blank">
000695
</a>

</td>
<td>
滨海能源?/=$⌊90.56
</td>
<td>
电力
</td>
<td>
11.73
</td>
<td>
2.18
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300606" target="_blank">
300606
</a>

</td>
<td>
金太阳?/=$⌊89.96
</td>
<td>
建材
</td>
<td>
33.76
</td>
<td>
2.18
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300638" target="_blank">
300638
</a>

</td>
<td>
广和通?/=$⌋91.64
</td>
<td>
通信设备
</td>
<td>
44.98
</td>
<td>
2.11
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/601636" target="_blank">
601636
</a>

</td>
<td>
旗滨集团?/=$⌋91.55
</td>
<td>
建材
</td>
<td>
5.82
</td>
<td>
2.11
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600617" target="_blank">
600617
</a>

</td>
<td>
国新能源?/=$⌊90.65
</td>
<td>
燃气
</td>
<td>
9.27
</td>
<td>
2.09
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002207" target="_blank">
002207
</a>

</td>
<td>
*ST准油?\^$⌊81.88
</td>
<td>
采掘服务
</td>
<td>
8.36
</td>
<td>
5.03
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002070" target="_blank">
002070
</a>

</td>
<td>
*ST众和?\^$±81.48
</td>
<td>
纺织
</td>
<td>
5.28
</td>
<td>
4.97
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600794" target="_blank">
600794
</a>

</td>
<td>
保税科技?\^$⌊81.97
</td>
<td>
仓储物流
</td>
<td>
4.45
</td>
<td>
3.25
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300350" target="_blank">
300350
</a>

</td>
<td>
华鹏飞?\^$⌈81.79
</td>
<td>
软件服务
</td>
<td>
9.92
</td>
<td>
2.9
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300164" target="_blank">
300164
</a>

</td>
<td>
通源石油?\^$⌊81.91
</td>
<td>
采掘服务
</td>
<td>
6.53
</td>
<td>
2.51
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300149" target="_blank">
300149
</a>

</td>
<td>
量子高科?\^$⌊81.27
</td>
<td>
食品饮料
</td>
<td>
15.35
</td>
<td>
2.27
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002709" target="_blank">
002709
</a>

</td>
<td>
天赐材料?\^$§81.16
</td>
<td>
化工
</td>
<td>
45.62
</td>
<td>
2.24
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603617" target="_blank">
603617
</a>

</td>
<td>
君禾股份?\^$±80.98
</td>
<td>
通用机械
</td>
<td>
23.79
</td>
<td>
2.06
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002660" target="_blank">
002660
</a>

</td>
<td>
茂硕电源?\^$ψ82.08
</td>
<td>
通信设备
</td>
<td>
10.45
</td>
<td>
2.05
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002505" target="_blank">
002505
</a>

</td>
<td>
大康农业?\=$⌊76.99
</td>
<td>
农林牧渔
</td>
<td>
2.85
</td>
<td>
10.04
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600339" target="_blank">
600339
</a>

</td>
<td>
中油工程?\=$⌊76.96
</td>
<td>
采掘服务
</td>
<td>
5.82
</td>
<td>
10.02
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603727" target="_blank">
603727
</a>

</td>
<td>
博迈科?\=$⌊76.61
</td>
<td>
采掘服务
</td>
<td>
24.61
</td>
<td>
10.01
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603676" target="_blank">
603676
</a>

</td>
<td>
卫信康?\=$⌊76.76
</td>
<td>
医药
</td>
<td>
13.1
</td>
<td>
9.99
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603322" target="_blank">
603322
</a>

</td>
<td>
超讯通信?\=$⌊76.35
</td>
<td>
软件服务
</td>
<td>
48.54
</td>
<td>
9.99
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002199" target="_blank">
002199
</a>

</td>
<td>
东晶电子?\=$⌊76.79
</td>
<td>
通信设备
</td>
<td>
15.01
</td>
<td>
7.68
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/000593" target="_blank">
000593
</a>

</td>
<td>
大通燃气?\=$≡79.62
</td>
<td>
燃气
</td>
<td>
10.16
</td>
<td>
7.51
</td>

</tr>

</table>
<table style="table-layout: fixed; overflow:hidden" class="table table-striped">
<tr>
<th style="text-align:left">
code
</th>
<th style="text-align:left">
name
</th>
<th style="text-align:left">
industry
</th>
<th style="text-align:left">
close
</th>
<th style="text-align:left">
per
</th>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300721" target="_blank">
300721
</a>

</td>
<td>
怡达股份!*^$⌋2.87
</td>
<td>
化工
</td>
<td>
43.03
</td>
<td>
0.05
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600903" target="_blank">
600903
</a>

</td>
<td>
贵州燃气!*^$⌉2.84
</td>
<td>
行业None
</td>
<td>
12.67
</td>
<td>
9.98
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300732" target="_blank">
300732
</a>

</td>
<td>
设研院!*^⌊2.81
</td>
<td>
专业技术
</td>
<td>
81.08
</td>
<td>
-2.5
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300731" target="_blank">
300731
</a>

</td>
<td>
科创新源!*^⌊2.78
</td>
<td>
化学制品
</td>
<td>
36.0
</td>
<td>
-5.73
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300725" target="_blank">
300725
</a>

</td>
<td>
药石科技!*^⌈2.75
</td>
<td>
化工
</td>
<td>
118.0
</td>
<td>
3.08
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603378" target="_blank">
603378
</a>

</td>
<td>
亚士创能!*=$≡2.72
</td>
<td>
汽车类
</td>
<td>
23.26
</td>
<td>
1.71
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603970" target="_blank">
603970
</a>

</td>
<td>
中农立华!*=$≡2.69
</td>
<td>
商业连锁
</td>
<td>
31.33
</td>
<td>
0.93
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603396" target="_blank">
603396
</a>

</td>
<td>
金辰股份!*=$⌋2.66
</td>
<td>
工程机械
</td>
<td>
41.69
</td>
<td>
10.0
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603722" target="_blank">
603722
</a>

</td>
<td>
阿科力!*=$⌋2.63
</td>
<td>
化工
</td>
<td>
38.32
</td>
<td>
-1.94
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603619" target="_blank">
603619
</a>

</td>
<td>
中曼石油!*=$⌋2.6
</td>
<td>
采掘服务
</td>
<td>
35.58
</td>
<td>
6.56
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300700" target="_blank">
300700
</a>

</td>
<td>
岱勒新材!*=$⌋2.58
</td>
<td>
建材
</td>
<td>
63.85
</td>
<td>
3.79
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300720" target="_blank">
300720
</a>

</td>
<td>
海川智能!*=$⌋2.55
</td>
<td>
仪器仪表
</td>
<td>
30.64
</td>
<td>
2.37
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300706" target="_blank">
300706
</a>

</td>
<td>
阿石创!*=$⌋2.52
</td>
<td>
其它制造
</td>
<td>
86.3
</td>
<td>
5.01
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603605" target="_blank">
603605
</a>

</td>
<td>
珀莱雅!*=$⌋2.49
</td>
<td>
化工
</td>
<td>
26.89
</td>
<td>
0.98
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300711" target="_blank">
300711
</a>

</td>
<td>
广哈通信!*=$⌋2.46
</td>
<td>
通信设备
</td>
<td>
27.49
</td>
<td>
3.15
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300705" target="_blank">
300705
</a>

</td>
<td>
九典制药!*=$⌋2.43
</td>
<td>
医药
</td>
<td>
24.14
</td>
<td>
0.79
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603607" target="_blank">
603607
</a>

</td>
<td>
京华激光!*=$⌋2.4
</td>
<td>
造纸
</td>
<td>
38.44
</td>
<td>
-0.03
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603110" target="_blank">
603110
</a>

</td>
<td>
东方材料!*=$⌋2.37
</td>
<td>
化工
</td>
<td>
25.25
</td>
<td>
2.6
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300722" target="_blank">
300722
</a>

</td>
<td>
新余国科!*=$⌋2.34
</td>
<td>
其它制造
</td>
<td>
30.91
</td>
<td>
0.91
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002864" target="_blank">
002864
</a>

</td>
<td>
盘龙药业!*=$⌋2.32
</td>
<td>
医药
</td>
<td>
25.12
</td>
<td>
0.16
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300716" target="_blank">
300716
</a>

</td>
<td>
国立科技!*=$⌋2.29
</td>
<td>
化学制品
</td>
<td>
22.72
</td>
<td>
0.13
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300713" target="_blank">
300713
</a>

</td>
<td>
英可瑞!*=$⌋2.26
</td>
<td>
电气设备
</td>
<td>
78.15
</td>
<td>
-0.7
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603289" target="_blank">
603289
</a>

</td>
<td>
泰瑞机器!*=$ψ2.23
</td>
<td>
工程机械
</td>
<td>
17.77
</td>
<td>
1.89
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603499" target="_blank">
603499
</a>

</td>
<td>
翔港科技!*=$⌊2.2
</td>
<td>
广告包装
</td>
<td>
22.75
</td>
<td>
0.4
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002893" target="_blank">
002893
</a>

</td>
<td>
华通热力!*=$⌊2.17
</td>
<td>
电力
</td>
<td>
27.95
</td>
<td>
5.0
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603507" target="_blank">
603507
</a>

</td>
<td>
振江股份!*=$⌊2.14
</td>
<td>
工业机械
</td>
<td>
38.9
</td>
<td>
2.4
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603685" target="_blank">
603685
</a>

</td>
<td>
晨丰科技!*=$⌊2.11
</td>
<td>
电气设备
</td>
<td>
32.47
</td>
<td>
1.5
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300717" target="_blank">
300717
</a>

</td>
<td>
华信新材!*=$⌊2.08
</td>
<td>
化学制品
</td>
<td>
33.46
</td>
<td>
0.48
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002911" target="_blank">
002911
</a>

</td>
<td>
佛燃股份!*=$§2.05
</td>
<td>
燃气
</td>
<td>
28.23
</td>
<td>
2.17
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300723" target="_blank">
300723
</a>

</td>
<td>
一品红!*=$§2.03
</td>
<td>
医药
</td>
<td>
34.96
</td>
<td>
-0.63
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603937" target="_blank">
603937
</a>

</td>
<td>
丽岛新材!*=$±2.0
</td>
<td>
工业机械
</td>
<td>
22.77
</td>
<td>
-2.23
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/601108" target="_blank">
601108
</a>

</td>
<td>
财通证券!*=$±1.97
</td>
<td>
证券
</td>
<td>
17.7
</td>
<td>
0.17
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603367" target="_blank">
603367
</a>

</td>
<td>
辰欣药业!*=$⌋1.94
</td>
<td>
医药
</td>
<td>
17.98
</td>
<td>
-0.06
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603829" target="_blank">
603829
</a>

</td>
<td>
洛凯股份!*=$⌊1.91
</td>
<td>
电气设备
</td>
<td>
16.63
</td>
<td>
1.28
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002910" target="_blank">
002910
</a>

</td>
<td>
庄园牧场!*=$±1.88
</td>
<td>
食品饮料
</td>
<td>
17.44
</td>
<td>
0.35
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603856" target="_blank">
603856
</a>

</td>
<td>
东宏股份!*=$±1.85
</td>
<td>
化学制品
</td>
<td>
18.7
</td>
<td>
-0.48
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002901" target="_blank">
002901
</a>

</td>
<td>
大博医疗!*=⌋1.82
</td>
<td>
工程机械
</td>
<td>
35.88
</td>
<td>
3.31
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300702" target="_blank">
300702
</a>

</td>
<td>
天宇股份!*=⌋1.79
</td>
<td>
医药
</td>
<td>
38.9
</td>
<td>
-0.08
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300719" target="_blank">
300719
</a>

</td>
<td>
安达维尔!*=⌋1.77
</td>
<td>
非汽交运
</td>
<td>
23.59
</td>
<td>
0.86
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002907" target="_blank">
002907
</a>

</td>
<td>
华森制药!*=⌋1.74
</td>
<td>
医药
</td>
<td>
15.65
</td>
<td>
-0.95
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300707" target="_blank">
300707
</a>

</td>
<td>
威唐工业!*=⌋1.71
</td>
<td>
工程机械
</td>
<td>
44.11
</td>
<td>
1.64
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300715" target="_blank">
300715
</a>

</td>
<td>
凯伦股份!*=⌋1.68
</td>
<td>
建材
</td>
<td>
30.86
</td>
<td>
-0.13
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300703" target="_blank">
300703
</a>

</td>
<td>
创源文化!*=⌋1.65
</td>
<td>
文教休闲
</td>
<td>
30.96
</td>
<td>
0.13
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603533" target="_blank">
603533
</a>

</td>
<td>
掌阅科技!*=⌋1.62
</td>
<td>
互联网
</td>
<td>
40.87
</td>
<td>
-2.62
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603260" target="_blank">
603260
</a>

</td>
<td>
合盛硅业!*=⌋1.59
</td>
<td>
化工
</td>
<td>
52.04
</td>
<td>
0.04
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603922" target="_blank">
603922
</a>

</td>
<td>
金鸿顺!*=⌋1.56
</td>
<td>
汽车类
</td>
<td>
26.68
</td>
<td>
-0.93
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002908" target="_blank">
002908
</a>

</td>
<td>
德生科技!*=⌋1.53
</td>
<td>
软件服务
</td>
<td>
25.46
</td>
<td>
-1.32
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002912" target="_blank">
002912
</a>

</td>
<td>
中新赛克!*=⌋1.51
</td>
<td>
软件服务
</td>
<td>
99.0
</td>
<td>
-1.11
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603659" target="_blank">
603659
</a>

</td>
<td>
璞泰来!*=⌊1.48
</td>
<td>
电气设备
</td>
<td>
55.02
</td>
<td>
1.96
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603683" target="_blank">
603683
</a>

</td>
<td>
晶华新材!*=⌊1.45
</td>
<td>
化工
</td>
<td>
18.86
</td>
<td>
0.86
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603711" target="_blank">
603711
</a>

</td>
<td>
香飘飘!*=⌊1.42
</td>
<td>
酿酒
</td>
<td>
27.06
</td>
<td>
8.85
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603963" target="_blank">
603963
</a>

</td>
<td>
大理药业!*=⌊1.39
</td>
<td>
医药
</td>
<td>
25.04
</td>
<td>
0.36
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603055" target="_blank">
603055
</a>

</td>
<td>
台华新材!*=⌊1.36
</td>
<td>
纺织
</td>
<td>
15.22
</td>
<td>
-0.07
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300727" target="_blank">
300727
</a>

</td>
<td>
润禾材料!*=⌊1.33
</td>
<td>
化工
</td>
<td>
27.83
</td>
<td>
10.0
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603890" target="_blank">
603890
</a>

</td>
<td>
春秋电子!*=⌊1.3
</td>
<td>
通信设备
</td>
<td>
38.51
</td>
<td>
1.58
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002917" target="_blank">
002917
</a>

</td>
<td>
金奥博!*=⌊1.27
</td>
<td>
化工
</td>
<td>
24.8
</td>
<td>
2.44
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603848" target="_blank">
603848
</a>

</td>
<td>
好太太!*=⌊1.24
</td>
<td>
工业机械
</td>
<td>
19.96
</td>
<td>
0.91
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603083" target="_blank">
603083
</a>

</td>
<td>
剑桥科技!*=§1.22
</td>
<td>
通信设备
</td>
<td>
42.33
</td>
<td>
-2.44
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002902" target="_blank">
002902
</a>

</td>
<td>
铭普光磁!*=§1.19
</td>
<td>
通信设备
</td>
<td>
39.49
</td>
<td>
-2.61
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300709" target="_blank">
300709
</a>

</td>
<td>
精研科技!*=§1.16
</td>
<td>
通信设备
</td>
<td>
72.84
</td>
<td>
-1.19
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002905" target="_blank">
002905
</a>

</td>
<td>
金逸影视!*=§1.13
</td>
<td>
文化传媒
</td>
<td>
33.56
</td>
<td>
-0.71
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002903" target="_blank">
002903
</a>

</td>
<td>
宇环数控!*=±1.1
</td>
<td>
通用机械
</td>
<td>
36.56
</td>
<td>
-0.79
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002899" target="_blank">
002899
</a>

</td>
<td>
英派斯!*=±1.07
</td>
<td>
文教休闲
</td>
<td>
26.35
</td>
<td>
-0.53
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603157" target="_blank">
603157
</a>

</td>
<td>
拉夏贝尔!*=±1.04
</td>
<td>
纺织服饰
</td>
<td>
15.38
</td>
<td>
-0.77
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603916" target="_blank">
603916
</a>

</td>
<td>
苏博特!*=±1.01
</td>
<td>
化工
</td>
<td>
15.75
</td>
<td>
-0.19
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603278" target="_blank">
603278
</a>

</td>
<td>
大业股份!*=±0.98
</td>
<td>
工业机械
</td>
<td>
22.04
</td>
<td>
0.23
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300654" target="_blank">
300654
</a>

</td>
<td>
世纪天鸿!*=±0.96
</td>
<td>
文化传媒
</td>
<td>
29.46
</td>
<td>
-3.41
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002900" target="_blank">
002900
</a>

</td>
<td>
哈三联!*=±0.93
</td>
<td>
医药
</td>
<td>
26.78
</td>
<td>
-1.0
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603106" target="_blank">
603106
</a>

</td>
<td>
恒银金融!*=±0.9
</td>
<td>
通信设备
</td>
<td>
23.81
</td>
<td>
-2.14
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603363" target="_blank">
603363
</a>

</td>
<td>
傲农生物!*=±0.87
</td>
<td>
农产品加工
</td>
<td>
12.53
</td>
<td>
-0.08
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603103" target="_blank">
603103
</a>

</td>
<td>
横店影视!*=±0.84
</td>
<td>
文化传媒
</td>
<td>
26.13
</td>
<td>
0.15
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300710" target="_blank">
300710
</a>

</td>
<td>
万隆光电!*=±0.81
</td>
<td>
通信设备
</td>
<td>
40.35
</td>
<td>
-2.35
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300718" target="_blank">
300718
</a>

</td>
<td>
长盛轴承!*=±0.78
</td>
<td>
通用机械
</td>
<td>
37.18
</td>
<td>
-0.35
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603813" target="_blank">
603813
</a>

</td>
<td>
原尚股份!*=±0.75
</td>
<td>
交通运输
</td>
<td>
27.92
</td>
<td>
-1.17
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603466" target="_blank">
603466
</a>

</td>
<td>
风语筑!*=±0.72
</td>
<td>
文化传媒
</td>
<td>
50.9
</td>
<td>
-0.8
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603912" target="_blank">
603912
</a>

</td>
<td>
佳力图!*=±0.69
</td>
<td>
工程机械
</td>
<td>
25.63
</td>
<td>
-3.68
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002909" target="_blank">
002909
</a>

</td>
<td>
集泰股份!*=±0.67
</td>
<td>
化工
</td>
<td>
19.26
</td>
<td>
-3.31
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300708" target="_blank">
300708
</a>

</td>
<td>
聚灿光电!*=±0.64
</td>
<td>
通信设备
</td>
<td>
26.75
</td>
<td>
-3.11
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/601086" target="_blank">
601086
</a>

</td>
<td>
国芳集团!*=±0.61
</td>
<td>
通信设备
</td>
<td>
7.58
</td>
<td>
-1.94
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/601019" target="_blank">
601019
</a>

</td>
<td>
山东出版!*v$⌋0.58
</td>
<td>
文化传媒
</td>
<td>
12.33
</td>
<td>
0.65
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603365" target="_blank">
603365
</a>

</td>
<td>
水星家纺!*v$⌋0.55
</td>
<td>
纺织
</td>
<td>
21.09
</td>
<td>
-1.17
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603809" target="_blank">
603809
</a>

</td>
<td>
豪能股份!*v$⌊0.52
</td>
<td>
汽车类
</td>
<td>
33.64
</td>
<td>
0.66
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002906" target="_blank">
002906
</a>

</td>
<td>
华阳集团!*v$⌊0.49
</td>
<td>
通信设备
</td>
<td>
20.97
</td>
<td>
-0.19
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603136" target="_blank">
603136
</a>

</td>
<td>
天目湖!*v$§0.46
</td>
<td>
旅游
</td>
<td>
40.7
</td>
<td>
-1.48
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603661" target="_blank">
603661
</a>

</td>
<td>
恒林股份!*v$§0.43
</td>
<td>
家居用品
</td>
<td>
67.16
</td>
<td>
-0.62
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300712" target="_blank">
300712
</a>

</td>
<td>
永福股份!*v⌋0.41
</td>
<td>
专业技术
</td>
<td>
21.89
</td>
<td>
0.05
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603076" target="_blank">
603076
</a>

</td>
<td>
乐惠国际!*v⌋0.38
</td>
<td>
工程机械
</td>
<td>
33.14
</td>
<td>
-0.27
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300612" target="_blank">
300612
</a>

</td>
<td>
宣亚国际!*v⌋0.35
</td>
<td>
文化传媒
</td>
<td>
39.18
</td>
<td>
-9.97
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300726" target="_blank">
300726
</a>

</td>
<td>
宏达电子!*v⌊0.32
</td>
<td>
通信设备
</td>
<td>
26.42
</td>
<td>
0.46
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600933" target="_blank">
600933
</a>

</td>
<td>
爱柯迪!*v⌊0.29
</td>
<td>
汽车类
</td>
<td>
14.63
</td>
<td>
0.14
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002913" target="_blank">
002913
</a>

</td>
<td>
奥士康!*v⌊0.26
</td>
<td>
通信设备
</td>
<td>
45.21
</td>
<td>
0.98
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603917" target="_blank">
603917
</a>

</td>
<td>
合力科技!*v⌊0.23
</td>
<td>
工程机械
</td>
<td>
24.66
</td>
<td>
0.49
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300729" target="_blank">
300729
</a>

</td>
<td>
乐歌股份!*v⌊0.2
</td>
<td>
家居用品
</td>
<td>
30.13
</td>
<td>
0.23
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600025" target="_blank">
600025
</a>

</td>
<td>
华能水电!**0.17
</td>
<td>
电力
</td>
<td>
5.03
</td>
<td>
10.07
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002915" target="_blank">
002915
</a>

</td>
<td>
中欣氟材!**0.14
</td>
<td>
化工
</td>
<td>
21.85
</td>
<td>
10.02
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603477" target="_blank">
603477
</a>

</td>
<td>
振静股份!**0.12
</td>
<td>
服装家纺
</td>
<td>
11.76
</td>
<td>
10.01
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002919" target="_blank">
002919
</a>

</td>
<td>
名臣健康!**0.09
</td>
<td>
化工
</td>
<td>
26.49
</td>
<td>
10.01
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300730" target="_blank">
300730
</a>

</td>
<td>
科创信息!**0.06
</td>
<td>
软件服务
</td>
<td>
41.55
</td>
<td>
10.01
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002916" target="_blank">
002916
</a>

</td>
<td>
深南电路!**0.03
</td>
<td>
通信设备
</td>
<td>
54.16
</td>
<td>
9.99
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002918" target="_blank">
002918
</a>

</td>
<td>
蒙娜丽莎!**0.0
</td>
<td>
建材
</td>
<td>
59.98
</td>
<td>
9.99
</td>

</tr>

</table>
<table style="table-layout: fixed; overflow:hidden" class="table table-striped">
<tr>
<th style="text-align:left">
code
</th>
<th style="text-align:left">
name
</th>
<th style="text-align:left">
industry
</th>
<th style="text-align:left">
close
</th>
<th style="text-align:left">
per
</th>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/000001" target="_blank">
000001
</a>

</td>
<td>
上证指数!v=$≡39.33
</td>
<td>
指数
</td>
<td>
3297.06
</td>
<td>
-0.09
</td>

</tr>
<tr>
<td colspan="5">
<div style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">
P#-47.88/0.42|0%1.24E+10:&lceil;’&nbsp;87.28~39.99%26.9
</div>
<div style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">
[&plusmn;‘v].&nbsp;&lfloor;’^.&nbsp;&rfloor;’^.&nbsp;&lceil;‘v.&nbsp;&rceil;‘v.&nbsp;&lfloor;’^.&nbsp;(&rfloor;‘).&nbsp;&lceil;’
</div>
<div style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">
[地陽v].&nbsp;雷陰^.&nbsp;澤陰^.&nbsp;風陽v.&nbsp;山陽v.&nbsp;雷陰^.&nbsp;(澤陽).&nbsp;風陰
</div>
<div style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">
[[-6.88,&nbsp;-6.0,&nbsp;-0.45,&nbsp;10.76],&nbsp;[-5.26,&nbsp;2.77,&nbsp;7.74,&nbsp;-9.94]]
</div>
<div style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">
[-0.68,&nbsp;8.75]
</div>

</td>

</tr>
<tr>
<td colspan="5">
<div style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">
O#13.4%6.48/7.16E+6:&psi;&nbsp;反覆高
</div>
<div style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">
[3.61],-2.59,(3.71)
</div>
<div style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">
5.77‘,3.37’,4.49‘
</div>
<div style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">
['3302.67',&nbsp;'3296.19']
</div>

</td>

</tr>
<tr>
<td colspan="5">
<div style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">
30#13:B-16.21%39.67/7:A5.02%81.91|@2A10B
</div>
<div style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">
D#4:@7.58%56.36/4:@7.58%56.36|@4
</div>
<div style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">
W#11:F-12.13%22.72/3:B2.93%89.0|@ABCDE3F3
</div>
<div style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">
M#6:A-0.57%81.45/5:A7.54%89.85|@4A2
</div>
<div style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">
S#1:@6.24%43.7/1:@6.24%43.7|@
</div>
<div style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">
Y#1:@0.91%39.2/1:@0.91%39.2|@
</div>

</td>

</tr>
<tr>
<td colspan="5">
<div style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">
30#2:&lt;=/0.01/0.06%0.05|54.88/47.25~60.16%1.26
</div>
<div style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">
D#-1:\&gt;-3.82/2.1%-1.72|45.7/41.27~58.24%2.48
</div>
<div style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">
W#1:/&gt;v-2.96/-1.65%1.31|32.18/13.42~37.49%6.85
</div>

</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002311" target="_blank">
002311
</a>

</td>
<td>
海大集团?^^$≡100.0
</td>
<td>
农产品加工
</td>
<td>
23.05
</td>
<td>
0.44
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002050" target="_blank">
002050
</a>

</td>
<td>
三花智控?^^$⌋99.97
</td>
<td>
通用机械
</td>
<td>
19.35
</td>
<td>
0.83
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300225" target="_blank">
300225
</a>

</td>
<td>
金力泰?^^$⌋99.94
</td>
<td>
化工
</td>
<td>
16.69
</td>
<td>
3.15
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600176" target="_blank">
600176
</a>

</td>
<td>
中国巨石?^^$⌋99.91
</td>
<td>
建材
</td>
<td>
16.16
</td>
<td>
1.13
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002713" target="_blank">
002713
</a>

</td>
<td>
东易日盛?^^$⌋99.88
</td>
<td>
建筑装饰
</td>
<td>
24.53
</td>
<td>
3.07
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002071" target="_blank">
002071
</a>

</td>
<td>
长城影视?^^$⌋99.86
</td>
<td>
文化传媒
</td>
<td>
10.84
</td>
<td>
0.0
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002543" target="_blank">
002543
</a>

</td>
<td>
万和电气?^^$⌋99.83
</td>
<td>
电气设备
</td>
<td>
23.11
</td>
<td>
3.03
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600352" target="_blank">
600352
</a>

</td>
<td>
浙江龙盛?^^$⌋99.8
</td>
<td>
化工
</td>
<td>
12.16
</td>
<td>
0.66
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300055" target="_blank">
300055
</a>

</td>
<td>
万邦达?^^$⌋99.77
</td>
<td>
建筑
</td>
<td>
22.6
</td>
<td>
0.53
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600273" target="_blank">
600273
</a>

</td>
<td>
嘉化能源?^^$ψ99.74
</td>
<td>
化工
</td>
<td>
9.53
</td>
<td>
1.28
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603032" target="_blank">
603032
</a>

</td>
<td>
德新交运?^^$⌊99.71
</td>
<td>
交通运输
</td>
<td>
54.26
</td>
<td>
2.63
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/000729" target="_blank">
000729
</a>

</td>
<td>
燕京啤酒?^^$⌊99.68
</td>
<td>
酿酒
</td>
<td>
6.97
</td>
<td>
6.09
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002003" target="_blank">
002003
</a>

</td>
<td>
伟星股份?^^$⌊99.65
</td>
<td>
纺织服饰
</td>
<td>
11.28
</td>
<td>
0.36
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600917" target="_blank">
600917
</a>

</td>
<td>
重庆燃气?^^$⌈99.62
</td>
<td>
燃气
</td>
<td>
11.18
</td>
<td>
10.04
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300241" target="_blank">
300241
</a>

</td>
<td>
瑞丰光电?^^$⌈99.59
</td>
<td>
通信设备
</td>
<td>
18.31
</td>
<td>
1.05
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300015" target="_blank">
300015
</a>

</td>
<td>
爱尔眼科?^^$⌈99.57
</td>
<td>
医疗保健
</td>
<td>
30.37
</td>
<td>
-0.88
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002281" target="_blank">
002281
</a>

</td>
<td>
光迅科技?^^$§99.54
</td>
<td>
通信设备
</td>
<td>
31.93
</td>
<td>
-0.93
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300316" target="_blank">
300316
</a>

</td>
<td>
晶盛机电?^^$§99.51
</td>
<td>
工程机械
</td>
<td>
21.98
</td>
<td>
-0.54
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300009" target="_blank">
300009
</a>

</td>
<td>
安科生物?^^$§99.48
</td>
<td>
医药
</td>
<td>
27.1
</td>
<td>
1.08
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002650" target="_blank">
002650
</a>

</td>
<td>
加加食品?^^$§99.45
</td>
<td>
食品饮料
</td>
<td>
7.02
</td>
<td>
0.0
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/601333" target="_blank">
601333
</a>

</td>
<td>
广深铁路?^^$§99.42
</td>
<td>
交通运输
</td>
<td>
5.43
</td>
<td>
0.0
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600645" target="_blank">
600645
</a>

</td>
<td>
中源协和?^^$§99.39
</td>
<td>
生物制药
</td>
<td>
28.4
</td>
<td>
0.92
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603986" target="_blank">
603986
</a>

</td>
<td>
兆易创新?^^$⌉99.36
</td>
<td>
通信设备
</td>
<td>
163.12
</td>
<td>
9.74
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/601699" target="_blank">
601699
</a>

</td>
<td>
潞安环能?^^$⌉99.33
</td>
<td>
煤炭
</td>
<td>
10.93
</td>
<td>
0.18
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/601113" target="_blank">
601113
</a>

</td>
<td>
华鼎股份?^^$⌉99.31
</td>
<td>
化纤
</td>
<td>
14.7
</td>
<td>
5.6
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002042" target="_blank">
002042
</a>

</td>
<td>
华孚时尚?^^$⌉99.28
</td>
<td>
纺织
</td>
<td>
12.97
</td>
<td>
-0.23
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300572" target="_blank">
300572
</a>

</td>
<td>
安车检测?^^$⌉99.25
</td>
<td>
仪器仪表
</td>
<td>
62.38
</td>
<td>
0.29
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/000703" target="_blank">
000703
</a>

</td>
<td>
恒逸石化?^^$±99.22
</td>
<td>
化纤
</td>
<td>
20.65
</td>
<td>
5.79
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/601111" target="_blank">
601111
</a>

</td>
<td>
中国国航?^^$±99.19
</td>
<td>
交通运输
</td>
<td>
12.28
</td>
<td>
-0.57
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/000333" target="_blank">
000333
</a>

</td>
<td>
美的集团?^^$±99.16
</td>
<td>
电气设备
</td>
<td>
56.58
</td>
<td>
1.14
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002493" target="_blank">
002493
</a>

</td>
<td>
荣盛石化?^^$±99.13
</td>
<td>
化纤
</td>
<td>
15.24
</td>
<td>
2.21
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002248" target="_blank">
002248
</a>

</td>
<td>
*ST东数?^^$±99.1
</td>
<td>
通用机械
</td>
<td>
8.13
</td>
<td>
4.1
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002508" target="_blank">
002508
</a>

</td>
<td>
老板电器?^^$±99.07
</td>
<td>
电气设备
</td>
<td>
49.85
</td>
<td>
0.1
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002768" target="_blank">
002768
</a>

</td>
<td>
国恩股份?^^$ψ99.04
</td>
<td>
化学制品
</td>
<td>
27.71
</td>
<td>
0.76
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600600" target="_blank">
600600
</a>

</td>
<td>
青岛啤酒?^^$⌊99.02
</td>
<td>
酿酒
</td>
<td>
38.79
</td>
<td>
7.75
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002293" target="_blank">
002293
</a>

</td>
<td>
罗莱生活?^^$⌈98.99
</td>
<td>
纺织
</td>
<td>
13.19
</td>
<td>
-1.12
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600691" target="_blank">
600691
</a>

</td>
<td>
阳煤化工?^^$⌈98.96
</td>
<td>
化工
</td>
<td>
3.84
</td>
<td>
0.0
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600486" target="_blank">
600486
</a>

</td>
<td>
扬农化工?^^$§98.93
</td>
<td>
化工
</td>
<td>
48.79
</td>
<td>
-0.55
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600196" target="_blank">
600196
</a>

</td>
<td>
复星医药?^^$§98.9
</td>
<td>
医药
</td>
<td>
46.7
</td>
<td>
-0.43
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/000039" target="_blank">
000039
</a>

</td>
<td>
中集集团?^^$§98.87
</td>
<td>
工业机械
</td>
<td>
21.72
</td>
<td>
-1.9
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002383" target="_blank">
002383
</a>

</td>
<td>
合众思壮?^^$§98.84
</td>
<td>
通信设备
</td>
<td>
20.81
</td>
<td>
-1.47
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300108" target="_blank">
300108
</a>

</td>
<td>
吉药控股?^^$§98.81
</td>
<td>
医药
</td>
<td>
9.8
</td>
<td>
2.83
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603338" target="_blank">
603338
</a>

</td>
<td>
浙江鼎力?^^$⌉98.78
</td>
<td>
工程机械
</td>
<td>
76.96
</td>
<td>
-0.68
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600426" target="_blank">
600426
</a>

</td>
<td>
华鲁恒升?^^$⌉98.76
</td>
<td>
化工
</td>
<td>
15.88
</td>
<td>
-1.73
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/601899" target="_blank">
601899
</a>

</td>
<td>
紫金矿业?^^$±98.73
</td>
<td>
有色开采
</td>
<td>
4.16
</td>
<td>
2.72
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600887" target="_blank">
600887
</a>

</td>
<td>
伊利股份?^^$±98.7
</td>
<td>
食品饮料
</td>
<td>
33.16
</td>
<td>
-0.39
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002398" target="_blank">
002398
</a>

</td>
<td>
建研集团?^^$±98.67
</td>
<td>
专业技术
</td>
<td>
15.14
</td>
<td>
-2.45
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600330" target="_blank">
600330
</a>

</td>
<td>
天通股份?^^$±98.64
</td>
<td>
通信设备
</td>
<td>
12.08
</td>
<td>
-0.82
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603816" target="_blank">
603816
</a>

</td>
<td>
顾家家居?^^$±98.61
</td>
<td>
家居用品
</td>
<td>
58.35
</td>
<td>
-0.43
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002721" target="_blank">
002721
</a>

</td>
<td>
金一文化?^^⌊98.58
</td>
<td>
其它制造
</td>
<td>
16.21
</td>
<td>
3.31
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002258" target="_blank">
002258
</a>

</td>
<td>
利尔化学?^^§98.55
</td>
<td>
化工
</td>
<td>
16.54
</td>
<td>
0.49
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/000858" target="_blank">
000858
</a>

</td>
<td>
五粮液?^^⌉98.52
</td>
<td>
酿酒
</td>
<td>
80.58
</td>
<td>
-1.91
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002649" target="_blank">
002649
</a>

</td>
<td>
博彦科技?^^±98.49
</td>
<td>
软件服务
</td>
<td>
13.32
</td>
<td>
-0.89
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603288" target="_blank">
603288
</a>

</td>
<td>
海天味业?^^±98.47
</td>
<td>
食品饮料
</td>
<td>
53.49
</td>
<td>
-1.26
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002470" target="_blank">
002470
</a>

</td>
<td>
金正大?^^±98.44
</td>
<td>
化工
</td>
<td>
9.15
</td>
<td>
1.1
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/000418" target="_blank">
000418
</a>

</td>
<td>
小天鹅Ａ?^^±98.41
</td>
<td>
电气设备
</td>
<td>
66.27
</td>
<td>
-1.16
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002427" target="_blank">
002427
</a>

</td>
<td>
尤夫股份?^^±98.38
</td>
<td>
化纤
</td>
<td>
33.8
</td>
<td>
-0.27
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600201" target="_blank">
600201
</a>

</td>
<td>
生物股份?^^±98.35
</td>
<td>
医药
</td>
<td>
30.86
</td>
<td>
-0.16
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600753" target="_blank">
600753
</a>

</td>
<td>
东方银星?^^±98.32
</td>
<td>
商业连锁
</td>
<td>
30.0
</td>
<td>
0.1
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002423" target="_blank">
002423
</a>

</td>
<td>
中原特钢?^=$≡98.29
</td>
<td>
工程机械
</td>
<td>
14.39
</td>
<td>
1.34
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300260" target="_blank">
300260
</a>

</td>
<td>
新莱应材?^=$≡98.26
</td>
<td>
通用机械
</td>
<td>
14.43
</td>
<td>
0.56
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/601003" target="_blank">
601003
</a>

</td>
<td>
柳钢股份?^=$≡98.23
</td>
<td>
钢铁
</td>
<td>
7.98
</td>
<td>
4.59
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002738" target="_blank">
002738
</a>

</td>
<td>
中矿资源?^=$≡98.21
</td>
<td>
专业技术
</td>
<td>
28.66
</td>
<td>
1.49
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603938" target="_blank">
603938
</a>

</td>
<td>
三孚股份?^=$≡98.18
</td>
<td>
化工
</td>
<td>
41.97
</td>
<td>
5.03
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600048" target="_blank">
600048
</a>

</td>
<td>
保利地产?^=$⌋98.15
</td>
<td>
房地产
</td>
<td>
13.08
</td>
<td>
0.38
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600333" target="_blank">
600333
</a>

</td>
<td>
长春燃气?^=$⌋98.12
</td>
<td>
燃气
</td>
<td>
7.82
</td>
<td>
9.99
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600378" target="_blank">
600378
</a>

</td>
<td>
天科股份?^=$⌋98.09
</td>
<td>
化工
</td>
<td>
13.65
</td>
<td>
4.12
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/601155" target="_blank">
601155
</a>

</td>
<td>
新城控股?^=$⌋98.06
</td>
<td>
房地产
</td>
<td>
28.53
</td>
<td>
1.78
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600062" target="_blank">
600062
</a>

</td>
<td>
华润双鹤?^=$⌋98.03
</td>
<td>
医药
</td>
<td>
24.25
</td>
<td>
0.08
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600667" target="_blank">
600667
</a>

</td>
<td>
太极实业?^=$⌋98.0
</td>
<td>
通信设备
</td>
<td>
9.24
</td>
<td>
-0.86
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002245" target="_blank">
002245
</a>

</td>
<td>
澳洋顺昌?^=$⌋97.97
</td>
<td>
仓储物流
</td>
<td>
11.08
</td>
<td>
-0.98
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/000526" target="_blank">
000526
</a>

</td>
<td>
*ST紫学?^=$ψ97.95
</td>
<td>
文教休闲
</td>
<td>
36.68
</td>
<td>
1.89
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600530" target="_blank">
600530
</a>

</td>
<td>
交大昂立?^=$⌊97.92
</td>
<td>
医药
</td>
<td>
7.37
</td>
<td>
9.67
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600634" target="_blank">
600634
</a>

</td>
<td>
富控互动?^=$⌊97.89
</td>
<td>
互联网
</td>
<td>
19.42
</td>
<td>
5.14
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002001" target="_blank">
002001
</a>

</td>
<td>
新和成?^=$⌊97.86
</td>
<td>
医药
</td>
<td>
39.31
</td>
<td>
6.59
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603393" target="_blank">
603393
</a>

</td>
<td>
新天然气?^=$⌊97.83
</td>
<td>
燃气
</td>
<td>
42.29
</td>
<td>
5.75
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300388" target="_blank">
300388
</a>

</td>
<td>
国祯环保?^=$⌊97.8
</td>
<td>
环境保护
</td>
<td>
23.9
</td>
<td>
3.69
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600460" target="_blank">
600460
</a>

</td>
<td>
士兰微?^=$⌊97.77
</td>
<td>
通信设备
</td>
<td>
15.45
</td>
<td>
0.46
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603501" target="_blank">
603501
</a>

</td>
<td>
韦尔股份?^=$⌊97.74
</td>
<td>
通信设备
</td>
<td>
43.63
</td>
<td>
6.44
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/000830" target="_blank">
000830
</a>

</td>
<td>
鲁西化工?^=$⌊97.71
</td>
<td>
化工
</td>
<td>
16.26
</td>
<td>
0.06
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603286" target="_blank">
603286
</a>

</td>
<td>
日盈电子?^=$⌊97.68
</td>
<td>
汽车类
</td>
<td>
36.6
</td>
<td>
3.77
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600661" target="_blank">
600661
</a>

</td>
<td>
新南洋?^=$⌊97.66
</td>
<td>
文教休闲
</td>
<td>
25.45
</td>
<td>
6.09
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600593" target="_blank">
600593
</a>

</td>
<td>
大连圣亚?^=$⌊97.63
</td>
<td>
旅游
</td>
<td>
27.29
</td>
<td>
2.44
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300102" target="_blank">
300102
</a>

</td>
<td>
乾照光电?^=$⌊97.6
</td>
<td>
通信设备
</td>
<td>
10.66
</td>
<td>
0.76
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600568" target="_blank">
600568
</a>

</td>
<td>
中珠医疗?^=$⌊97.57
</td>
<td>
医药
</td>
<td>
7.59
</td>
<td>
1.74
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300270" target="_blank">
300270
</a>

</td>
<td>
中威电子?^=$⌊97.54
</td>
<td>
通信设备
</td>
<td>
13.12
</td>
<td>
2.26
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002437" target="_blank">
002437
</a>

</td>
<td>
誉衡药业?^=$⌈97.51
</td>
<td>
医药
</td>
<td>
7.26
</td>
<td>
0.0
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600029" target="_blank">
600029
</a>

</td>
<td>
南方航空?^=$⌈97.48
</td>
<td>
交通运输
</td>
<td>
11.69
</td>
<td>
-0.43
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600115" target="_blank">
600115
</a>

</td>
<td>
东方航空?^=$⌈97.45
</td>
<td>
交通运输
</td>
<td>
7.95
</td>
<td>
0.0
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002202" target="_blank">
002202
</a>

</td>
<td>
金风科技?^=$⌈97.42
</td>
<td>
通用机械
</td>
<td>
18.88
</td>
<td>
-0.89
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002267" target="_blank">
002267
</a>

</td>
<td>
陕天然气?^=$§97.4
</td>
<td>
燃气
</td>
<td>
9.24
</td>
<td>
5.6
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002531" target="_blank">
002531
</a>

</td>
<td>
天顺风能?^=$§97.37
</td>
<td>
电气设备
</td>
<td>
8.22
</td>
<td>
-0.6
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/000968" target="_blank">
000968
</a>

</td>
<td>
蓝焰控股?^=$⌉97.34
</td>
<td>
石油
</td>
<td>
17.49
</td>
<td>
1.22
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/601933" target="_blank">
601933
</a>

</td>
<td>
永辉超市?^=$⌉97.31
</td>
<td>
商业连锁
</td>
<td>
10.6
</td>
<td>
-1.85
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002297" target="_blank">
002297
</a>

</td>
<td>
博云新材?^=$⌉97.28
</td>
<td>
建材
</td>
<td>
11.28
</td>
<td>
0.53
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/000006" target="_blank">
000006
</a>

</td>
<td>
深振业Ａ?^=$⌉97.25
</td>
<td>
房地产
</td>
<td>
9.85
</td>
<td>
5.46
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300146" target="_blank">
300146
</a>

</td>
<td>
汤臣倍健?^=$±97.22
</td>
<td>
食品饮料
</td>
<td>
14.53
</td>
<td>
-0.14
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300639" target="_blank">
300639
</a>

</td>
<td>
凯普生物?^=$±97.19
</td>
<td>
医药
</td>
<td>
69.88
</td>
<td>
0.62
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600803" target="_blank">
600803
</a>

</td>
<td>
新奥股份?^=$±97.16
</td>
<td>
化工
</td>
<td>
17.07
</td>
<td>
1.67
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600256" target="_blank">
600256
</a>

</td>
<td>
广汇能源?^=$⌈97.13
</td>
<td>
石油
</td>
<td>
5.45
</td>
<td>
0.74
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600143" target="_blank">
600143
</a>

</td>
<td>
金发科技?^=$⌈97.11
</td>
<td>
化学制品
</td>
<td>
6.42
</td>
<td>
0.94
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/601599" target="_blank">
601599
</a>

</td>
<td>
鹿港文化?^=$§97.08
</td>
<td>
纺织
</td>
<td>
6.96
</td>
<td>
0.29
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002027" target="_blank">
002027
</a>

</td>
<td>
分众传媒?^=$§97.05
</td>
<td>
文化传媒
</td>
<td>
13.83
</td>
<td>
-1.21
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600835" target="_blank">
600835
</a>

</td>
<td>
上海机电?^=$§97.02
</td>
<td>
通用机械
</td>
<td>
27.07
</td>
<td>
-2.84
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/000592" target="_blank">
000592
</a>

</td>
<td>
平潭发展?^=$§96.99
</td>
<td>
农林牧渔
</td>
<td>
5.75
</td>
<td>
-0.17
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300064" target="_blank">
300064
</a>

</td>
<td>
豫金刚石?^=$⌉96.96
</td>
<td>
建材
</td>
<td>
13.9
</td>
<td>
-0.71
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300347" target="_blank">
300347
</a>

</td>
<td>
泰格医药?^=$⌉96.93
</td>
<td>
医疗保健
</td>
<td>
33.44
</td>
<td>
-1.21
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/601939" target="_blank">
601939
</a>

</td>
<td>
建设银行?^=$±96.9
</td>
<td>
银行
</td>
<td>
7.23
</td>
<td>
-0.14
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600188" target="_blank">
600188
</a>

</td>
<td>
兖州煤业?^=$±96.87
</td>
<td>
煤炭
</td>
<td>
14.21
</td>
<td>
-0.56
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600239" target="_blank">
600239
</a>

</td>
<td>
云南城投?^=$±96.85
</td>
<td>
房地产
</td>
<td>
5.22
</td>
<td>
2.15
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600271" target="_blank">
600271
</a>

</td>
<td>
航天信息?^=$±96.82
</td>
<td>
通信设备
</td>
<td>
23.01
</td>
<td>
-0.86
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/000504" target="_blank">
000504
</a>

</td>
<td>
南华生物?^=$±96.79
</td>
<td>
文化传媒
</td>
<td>
23.51
</td>
<td>
0.04
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600760" target="_blank">
600760
</a>

</td>
<td>
中航黑豹?^=$±96.76
</td>
<td>
汽车类
</td>
<td>
34.22
</td>
<td>
-0.98
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603883" target="_blank">
603883
</a>

</td>
<td>
老百姓?^=$±96.73
</td>
<td>
商业连锁
</td>
<td>
61.03
</td>
<td>
-1.29
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603010" target="_blank">
603010
</a>

</td>
<td>
万盛股份?^=$±96.7
</td>
<td>
化工
</td>
<td>
30.85
</td>
<td>
-1.22
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002866" target="_blank">
002866
</a>

</td>
<td>
传艺科技?^=≡96.67
</td>
<td>
通信设备
</td>
<td>
36.41
</td>
<td>
-1.27
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002178" target="_blank">
002178
</a>

</td>
<td>
延华智能?^=≡96.64
</td>
<td>
专业技术
</td>
<td>
13.88
</td>
<td>
-0.07
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002079" target="_blank">
002079
</a>

</td>
<td>
苏州固锝?^=≡96.61
</td>
<td>
通信设备
</td>
<td>
9.69
</td>
<td>
-1.42
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002656" target="_blank">
002656
</a>

</td>
<td>
摩登大道?^=⌋96.58
</td>
<td>
纺织服饰
</td>
<td>
24.83
</td>
<td>
0.53
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002856" target="_blank">
002856
</a>

</td>
<td>
美芝股份?^=⌋96.56
</td>
<td>
建筑装饰
</td>
<td>
46.3
</td>
<td>
0.09
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300054" target="_blank">
300054
</a>

</td>
<td>
鼎龙股份?^=⌋96.53
</td>
<td>
化工
</td>
<td>
12.4
</td>
<td>
-2.36
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300046" target="_blank">
300046
</a>

</td>
<td>
台基股份?^=⌋96.5
</td>
<td>
通信设备
</td>
<td>
22.92
</td>
<td>
-2.13
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002156" target="_blank">
002156
</a>

</td>
<td>
通富微电?^=⌋96.47
</td>
<td>
通信设备
</td>
<td>
13.79
</td>
<td>
0.22
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002221" target="_blank">
002221
</a>

</td>
<td>
东华能源?^=ψ96.44
</td>
<td>
商业连锁
</td>
<td>
12.77
</td>
<td>
4.76
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603936" target="_blank">
603936
</a>

</td>
<td>
博敏电子?^=⌊96.41
</td>
<td>
通信设备
</td>
<td>
28.85
</td>
<td>
5.29
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002760" target="_blank">
002760
</a>

</td>
<td>
凤形股份?^=⌊96.38
</td>
<td>
工业机械
</td>
<td>
36.71
</td>
<td>
1.55
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600695" target="_blank">
600695
</a>

</td>
<td>
绿庭投资?^=⌊96.35
</td>
<td>
证券
</td>
<td>
11.03
</td>
<td>
3.28
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600332" target="_blank">
600332
</a>

</td>
<td>
白云山?^=⌊96.32
</td>
<td>
医药
</td>
<td>
32.14
</td>
<td>
1.36
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300091" target="_blank">
300091
</a>

</td>
<td>
金通灵?^=⌊96.3
</td>
<td>
通用机械
</td>
<td>
17.09
</td>
<td>
0.41
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600346" target="_blank">
600346
</a>

</td>
<td>
恒力股份?^=⌊96.27
</td>
<td>
化纤
</td>
<td>
12.33
</td>
<td>
3.61
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603708" target="_blank">
603708
</a>

</td>
<td>
家家悦?^=⌊96.24
</td>
<td>
商业连锁
</td>
<td>
20.44
</td>
<td>
-2.48
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300038" target="_blank">
300038
</a>

</td>
<td>
梅泰诺?^=⌊96.21
</td>
<td>
互联网
</td>
<td>
49.59
</td>
<td>
3.55
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002840" target="_blank">
002840
</a>

</td>
<td>
华统股份?^=⌊96.18
</td>
<td>
农产品加工
</td>
<td>
37.35
</td>
<td>
1.49
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002630" target="_blank">
002630
</a>

</td>
<td>
华西能源?^=⌊96.15
</td>
<td>
通用机械
</td>
<td>
10.99
</td>
<td>
0.0
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603638" target="_blank">
603638
</a>

</td>
<td>
艾迪精密?^=⌊96.12
</td>
<td>
工程机械
</td>
<td>
32.78
</td>
<td>
0.58
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002251" target="_blank">
002251
</a>

</td>
<td>
步步高?^=⌈96.09
</td>
<td>
商业连锁
</td>
<td>
17.1
</td>
<td>
-0.93
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002294" target="_blank">
002294
</a>

</td>
<td>
信立泰?^=⌈96.06
</td>
<td>
医药
</td>
<td>
43.31
</td>
<td>
-1.7
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002408" target="_blank">
002408
</a>

</td>
<td>
齐翔腾达?^=⌈96.03
</td>
<td>
化工
</td>
<td>
13.35
</td>
<td>
-0.74
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300630" target="_blank">
300630
</a>

</td>
<td>
普利制药?^=⌈96.01
</td>
<td>
医药
</td>
<td>
73.08
</td>
<td>
-3.05
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600859" target="_blank">
600859
</a>

</td>
<td>
王府井?^=§95.98
</td>
<td>
商业连锁
</td>
<td>
21.14
</td>
<td>
-2.67
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/000818" target="_blank">
000818
</a>

</td>
<td>
方大化工?^=§95.95
</td>
<td>
化工
</td>
<td>
12.08
</td>
<td>
-0.58
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/601233" target="_blank">
601233
</a>

</td>
<td>
桐昆股份?^=§95.92
</td>
<td>
化纤
</td>
<td>
21.82
</td>
<td>
-3.41
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600521" target="_blank">
600521
</a>

</td>
<td>
华海药业?^=§95.89
</td>
<td>
医药
</td>
<td>
29.7
</td>
<td>
-2.27
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002422" target="_blank">
002422
</a>

</td>
<td>
科伦药业?^=§95.86
</td>
<td>
医药
</td>
<td>
25.29
</td>
<td>
-1.52
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600227" target="_blank">
600227
</a>

</td>
<td>
赤天化?^=§95.83
</td>
<td>
医药
</td>
<td>
7.09
</td>
<td>
0.0
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002614" target="_blank">
002614
</a>

</td>
<td>
奥佳华?^=§95.8
</td>
<td>
工程机械
</td>
<td>
18.95
</td>
<td>
-0.99
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/000681" target="_blank">
000681
</a>

</td>
<td>
视觉中国?^=§95.77
</td>
<td>
文化传媒
</td>
<td>
20.66
</td>
<td>
-1.15
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603899" target="_blank">
603899
</a>

</td>
<td>
晨光文具?^=§95.75
</td>
<td>
文教休闲
</td>
<td>
24.88
</td>
<td>
-1.82
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002330" target="_blank">
002330
</a>

</td>
<td>
得利斯?^=§95.72
</td>
<td>
农产品加工
</td>
<td>
9.44
</td>
<td>
-0.94
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600242" target="_blank">
600242
</a>

</td>
<td>
中昌数据?^=§95.69
</td>
<td>
互联网
</td>
<td>
17.27
</td>
<td>
-3.63
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300176" target="_blank">
300176
</a>

</td>
<td>
鸿特精密?^=§95.66
</td>
<td>
汽车类
</td>
<td>
135.2
</td>
<td>
-0.58
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600206" target="_blank">
600206
</a>

</td>
<td>
有研新材?^=§95.63
</td>
<td>
有色
</td>
<td>
12.87
</td>
<td>
-1.91
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603939" target="_blank">
603939
</a>

</td>
<td>
益丰药房?^=§95.6
</td>
<td>
商业连锁
</td>
<td>
43.69
</td>
<td>
-3.85
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300003" target="_blank">
300003
</a>

</td>
<td>
乐普医疗?^=§95.57
</td>
<td>
工程机械
</td>
<td>
24.1
</td>
<td>
-3.83
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002676" target="_blank">
002676
</a>

</td>
<td>
顺威股份?^=§95.54
</td>
<td>
化学制品
</td>
<td>
15.98
</td>
<td>
-9.97
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603005" target="_blank">
603005
</a>

</td>
<td>
晶方科技?^=§95.51
</td>
<td>
通信设备
</td>
<td>
36.16
</td>
<td>
-3.93
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002129" target="_blank">
002129
</a>

</td>
<td>
中环股份?^=§95.48
</td>
<td>
电气设备
</td>
<td>
11.58
</td>
<td>
-10.02
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002044" target="_blank">
002044
</a>

</td>
<td>
美年健康?^=⌉95.46
</td>
<td>
医疗保健
</td>
<td>
21.31
</td>
<td>
-1.39
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/000659" target="_blank">
000659
</a>

</td>
<td>
*ST中富?^=⌉95.43
</td>
<td>
化学制品
</td>
<td>
4.33
</td>
<td>
-1.81
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002377" target="_blank">
002377
</a>

</td>
<td>
国创高新?^=⌉95.4
</td>
<td>
基础化学
</td>
<td>
10.94
</td>
<td>
0.92
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/000688" target="_blank">
000688
</a>

</td>
<td>
建新矿业?^=⌉95.37
</td>
<td>
有色开采
</td>
<td>
10.95
</td>
<td>
-3.44
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002189" target="_blank">
002189
</a>

</td>
<td>
利达光电?^=⌉95.34
</td>
<td>
通信设备
</td>
<td>
18.08
</td>
<td>
-3.16
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002278" target="_blank">
002278
</a>

</td>
<td>
神开股份?^=⌉95.31
</td>
<td>
工程机械
</td>
<td>
14.81
</td>
<td>
-1.46
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603081" target="_blank">
603081
</a>

</td>
<td>
大丰实业?^=⌉95.28
</td>
<td>
工程机械
</td>
<td>
27.28
</td>
<td>
-2.57
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/000950" target="_blank">
000950
</a>

</td>
<td>
*ST建峰?^=⌉95.25
</td>
<td>
化工
</td>
<td>
10.72
</td>
<td>
-0.19
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300413" target="_blank">
300413
</a>

</td>
<td>
快乐购?^=⌉95.22
</td>
<td>
商业连锁
</td>
<td>
30.45
</td>
<td>
-1.46
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603900" target="_blank">
603900
</a>

</td>
<td>
莱绅通灵?^=⌉95.2
</td>
<td>
商业连锁
</td>
<td>
28.53
</td>
<td>
-1.55
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600845" target="_blank">
600845
</a>

</td>
<td>
宝信软件?^=±95.17
</td>
<td>
软件服务
</td>
<td>
18.22
</td>
<td>
-0.82
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603180" target="_blank">
603180
</a>

</td>
<td>
金牌厨柜?^=±95.14
</td>
<td>
家居用品
</td>
<td>
138.16
</td>
<td>
0.09
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002584" target="_blank">
002584
</a>

</td>
<td>
西陇科学?^=±95.11
</td>
<td>
化工
</td>
<td>
18.06
</td>
<td>
1.18
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/000425" target="_blank">
000425
</a>

</td>
<td>
徐工机械?^=±95.08
</td>
<td>
工程机械
</td>
<td>
4.04
</td>
<td>
-0.49
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300464" target="_blank">
300464
</a>

</td>
<td>
星徽精密?^=±95.05
</td>
<td>
工业机械
</td>
<td>
12.03
</td>
<td>
-1.55
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/000629" target="_blank">
000629
</a>

</td>
<td>
*ST钒钛?^=±95.02
</td>
<td>
矿业开采
</td>
<td>
3.07
</td>
<td>
1.32
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603138" target="_blank">
603138
</a>

</td>
<td>
海量数据?^=±94.99
</td>
<td>
软件服务
</td>
<td>
46.17
</td>
<td>
-4.63
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002179" target="_blank">
002179
</a>

</td>
<td>
中航光电?^=±94.96
</td>
<td>
通信设备
</td>
<td>
38.8
</td>
<td>
-1.7
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/000410" target="_blank">
000410
</a>

</td>
<td>
*ST沈机?^=±94.93
</td>
<td>
通用机械
</td>
<td>
10.03
</td>
<td>
-0.89
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002506" target="_blank">
002506
</a>

</td>
<td>
协鑫集成?^=±94.91
</td>
<td>
通信设备
</td>
<td>
4.45
</td>
<td>
-0.45
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002151" target="_blank">
002151
</a>

</td>
<td>
北斗星通?^=±94.88
</td>
<td>
通信设备
</td>
<td>
32.84
</td>
<td>
-0.99
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603599" target="_blank">
603599
</a>

</td>
<td>
广信股份?^=±94.85
</td>
<td>
化工
</td>
<td>
18.86
</td>
<td>
-1.57
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300308" target="_blank">
300308
</a>

</td>
<td>
中际旭创?^=±94.82
</td>
<td>
工程机械
</td>
<td>
56.3
</td>
<td>
-2.76
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603011" target="_blank">
603011
</a>

</td>
<td>
合锻智能?^=±94.79
</td>
<td>
通用机械
</td>
<td>
11.03
</td>
<td>
-0.09
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/603579" target="_blank">
603579
</a>

</td>
<td>
荣泰健康?^=±94.76
</td>
<td>
工程机械
</td>
<td>
64.4
</td>
<td>
-0.89
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/000793" target="_blank">
000793
</a>

</td>
<td>
华闻传媒?^=±94.73
</td>
<td>
文化传媒
</td>
<td>
10.39
</td>
<td>
-2.07
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300240" target="_blank">
300240
</a>

</td>
<td>
飞力达?^=±94.7
</td>
<td>
仓储物流
</td>
<td>
10.96
</td>
<td>
-0.63
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/000759" target="_blank">
000759
</a>

</td>
<td>
中百集团?^=±94.67
</td>
<td>
商业连锁
</td>
<td>
9.8
</td>
<td>
-2.58
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600171" target="_blank">
600171
</a>

</td>
<td>
上海贝岭?^=±94.65
</td>
<td>
通信设备
</td>
<td>
16.7
</td>
<td>
-5.28
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/000056" target="_blank">
000056
</a>

</td>
<td>
皇庭国际?^=±94.62
</td>
<td>
房地产
</td>
<td>
13.27
</td>
<td>
0.68
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300280" target="_blank">
300280
</a>

</td>
<td>
南通锻压?^=±94.59
</td>
<td>
通用机械
</td>
<td>
34.26
</td>
<td>
-0.03
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300431" target="_blank">
300431
</a>

</td>
<td>
暴风集团?^=±94.56
</td>
<td>
互联网
</td>
<td>
24.61
</td>
<td>
-4.83
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600725" target="_blank">
600725
</a>

</td>
<td>
ST云维?^=±94.53
</td>
<td>
基础化学
</td>
<td>
3.14
</td>
<td>
0.0
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600520" target="_blank">
600520
</a>

</td>
<td>
文一科技?^=±94.5
</td>
<td>
电气设备
</td>
<td>
22.29
</td>
<td>
-5.03
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002321" target="_blank">
002321
</a>

</td>
<td>
华英农业?^=±94.47
</td>
<td>
农林牧渔
</td>
<td>
13.25
</td>
<td>
-2.93
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600208" target="_blank">
600208
</a>

</td>
<td>
新湖中宝?^=±94.44
</td>
<td>
房地产
</td>
<td>
5.41
</td>
<td>
-2.17
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002458" target="_blank">
002458
</a>

</td>
<td>
益生股份?^=±94.41
</td>
<td>
农林牧渔
</td>
<td>
26.14
</td>
<td>
-1.69
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/300188" target="_blank">
300188
</a>

</td>
<td>
美亚柏科?^=±94.38
</td>
<td>
软件服务
</td>
<td>
21.01
</td>
<td>
-1.22
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/000663" target="_blank">
000663
</a>

</td>
<td>
永安林业?^=±94.36
</td>
<td>
家居用品
</td>
<td>
17.58
</td>
<td>
-1.9
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600283" target="_blank">
600283
</a>

</td>
<td>
钱江水利?^=±94.33
</td>
<td>
水务
</td>
<td>
12.84
</td>
<td>
-0.47
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002540" target="_blank">
002540
</a>

</td>
<td>
亚太科技?^=±94.3
</td>
<td>
有色
</td>
<td>
7.47
</td>
<td>
0.0
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/002517" target="_blank">
002517
</a>

</td>
<td>
恺英网络?^v⌊94.27
</td>
<td>
互联网
</td>
<td>
25.94
</td>
<td>
0.04
</td>

</tr>
<tr>
<td>
<a href="http://data.10jqka.com.cn/market/lhbgg/code/600438" target="_blank">
600438
</a>

</td>
<td>
通威股份?/^$≡94.24
</td>
<td>
农产品加工
</td>
<td>
13.15
</td>
<td>
9.31
</td>

</tr>

</table>

</div>





```python

```


```python

```
