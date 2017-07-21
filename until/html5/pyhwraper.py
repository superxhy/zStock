#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2017-5-26

@author: yuql
'''

from .pyh import *
import datetime

#protect html keyword convert
def quote(s):
    return s.replace('&','&amp;').replace('<', '&lt;').replace('>', '&gt;').replace(' ','&nbsp;').replace('\n', '<br/>')

class HtmlPageMaker(object):
    
    STYLE_MOBREM = '\n'.join([
    'body,html {',
        'min-height:100%',
    '}'
    'body {',
        '-webkit-user-select:none;',
        ',user-select:none;'
        '/*background-color:#f5f5f9*/'
    '}'
    'body,button,input,select,textarea {'
        'font-size:.16rem;',
        'line-height:1.5;',
        'color:#000;',
        'font-family:"Helvetica Neue",Helvetica,STHeiTi,sans-serif',
    '}'
    'input {',
        'line-height:normal',
    '}',
    'a {',
        'color:#108ee9;',
        'text-decoration:none',
    '}',
    
    'html {',
        'font-size:100px',
    '}',
    '@media only screen and (min-width:320px) and (max-width:320px) {',
        'html {',
        'font-size:85.33px!important',
    '}',
    '}@media only screen and (min-width:384px) {',
        'html {',
        'font-size:106.67px!important',
    '}',
    '}@media only screen and (min-width:412px) {',
        'html {',
        'font-size:114.44px!important',
    '}',
    '}@media only screen and (min-width:414px) {',
        'html {',
        'font-size:110.4px!important',
    '}',
    '}@media only screen and (min-width:600px) {',
        'html {',
        'font-size:204.8px!important',
    '}',
    '}@media only screen and (min-width:1024px){',
        'html {',
        'font-size:100px!important',
    '}',
    '}',
    
    'html {',
      'font-family: sans-serif;',
      '-webkit-text-size-adjust: 100%;',
          '-ms-text-size-adjust: 100%;',
    '}',
    'body {',
      'margin: 0;',
    '}',
    ])
    
    STYLE_TABLE = '\n'.join([
    'table {',
      'border-spacing: 0;',
      'border-collapse: collapse;',
    '}',
    
    'td,',
    'th {',
      'padding: 0;',
    '}',
    '.table {',
      'width: 100%;',
      'max-width: 100%;',
      'margin-bottom: 20px;',
    '}',
    '.table > thead > tr > th,',
    '.table > tbody > tr > th,',
    '.table > tfoot > tr > th,',
    '.table > thead > tr > td,',
    '.table > tbody > tr > td,',
    '.table > tfoot > tr > td {',
      'padding: 8px;',
      'line-height: 1.42857143;',
      'vertical-align: top;',
      'border-top: 1px solid #ddd;',
    '}',
    '.table > thead > tr > th {',
      'vertical-align: bottom;',
      'border-bottom: 2px solid #ddd;',
    '}',
    '.table > caption + thead > tr:first-child > th,',
    '.table > colgroup + thead > tr:first-child > th,',
    '.table > thead:first-child > tr:first-child > th,',
    '.table > caption + thead > tr:first-child > td,',
    '.table > colgroup + thead > tr:first-child > td,',
    '.table > thead:first-child > tr:first-child > td {',
      'border-top: 0;',
    '}',
    '.table > tbody + tbody {',
      'border-top: 2px solid #ddd;',
    '}',
    ',table .table {',
      'background-color: #fff;',
    '}',
    
    'table-bordered {',
      'border: 1px solid #ddd;',
    '}',
    '.table-bordered > thead > tr > th,',
    '.table-bordered > tbody > tr > th,',
    '.table-bordered > tfoot > tr > th,',
    '.table-bordered > thead > tr > td,',
    '.table-bordered > tbody > tr > td,',
    '.table-bordered > tfoot > tr > td {',
      'border: 1px solid #ddd;',
    '}',
    '.table-bordered > thead > tr > th,',
    '.table-bordered > thead > tr > td {',
      'border-bottom-width: 2px;',
    '}',
    '.table-striped > tbody > tr:nth-of-type(odd) {',
      'background-color: #f9f9f9;',
    '}',
    '.table-hover > tbody > tr:hover {',
      'background-color: #f5f5f5;',
    '}',
    ])
    
    def __init__(self, title=None):
        if title == None:
            title = ''
        else:
            title += '_'
        self.__title__ = title + datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S')
        print self.__title__
        self.__page__ = PyH(self.__title__)
        self.__mainDiv__ = div(id='mainDiv')
        self.__stylecss__ = style(self.STYLE_MOBREM + self.STYLE_TABLE)
        self.__mainDiv__ << self.__stylecss__
        self.__curDom__ = self.__page__ << self.__mainDiv__
        
    def __repr__(self):
        return self.getHtml()
        
    def quote(self, s):
        return s.replace('&','&amp;').replace('<', '&lt;').replace('>', '&gt;').replace(' ','&nbsp;').replace('\n', '<br/>')
        
    def addDiv(self, content, st='',curDom=None):
        if curDom == None:
            curDom = self.__curDom__
        return curDom << div(content, style=st)
       
    def addTable(self, dictList, schema, st='',curDom=None):
        if curDom == None:
            curDom = self.__curDom__
        tab = table(cl='table table-striped',style="table-layout: fixed; overflow:hidden")
        hdtr = tab << tr()
        for headitem in schema:
            hdtr << th(headitem,style='text-align:left')
        if type(dictList) != list:
            return curDom << tab
        if len(dictList) == 0:
            return curDom << tab
        for item in dictList:
            if type(item) != dict:
                continue
            datatr = tab << tr()
            for colum in schema:
                datatr << td(item.get(colum,'-'))
            #appen meta data in ONE row
            meta = []
            spanlen = str(len(schema))
            for k in item.keys():
                if k not in schema:
                    meta.append(k)
            for metaitem in meta:
                metatr = tab << tr()
                metatd = metatr << td(colspan = spanlen)
                for m in item[metaitem]:
                    metatd << div(self.quote(m) ,style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;")
        return curDom << tab
    
    def getTitle(self):
        return self.__title__
             
    def getHtml(self):
        return self.__mainDiv__.render()
    
    def saveFile(self, name=None):
        if name == None:
            name = self.__title__
        fname = name
        if len(fname.split('.')) == 0:
            fname = name + '.html'
        self.__page__.printOut(fname)
        return fname
