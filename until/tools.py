#!/usr/bin/env python
# -*- coding:utf-8 -*- 
'''
Created on 2017-5-5

@author: yuql
'''

from prettytable import PrettyTable
from .html5.pyhwraper import HtmlPageMaker,quote
#from pyhwraper import HtmlPageMaker,quote
from .sender import MailSender
#from sender import MailSender
'''
exp:
dictList=[]
dictList.append({"City name":"Adelaide","Area":1295,"Population":1158259,"Annual Rainfall":600.5})
dictList.append({"City name":"Brisbane","Area":5905,"Population":1857594,"Annual Rainfall":1146.4})
'''
def getPrettyTable(dictList, schema=[]):
    if type(dictList) != list:
        return None
    if len(dictList) == 0:
        return None
    i = 0
    result = None
    for item in dictList:
        if type(item) != dict:
            continue
        if i == 0:
            if len(schema) == 0:
                schema = item.keys()
            if len(schema) == 0:
                break
            result = PrettyTable(schema)
            result.align[schema[0]] ="l"# Left align city names
            result.padding_width =1# One space between column edges and contents (default)
        row = []
        for colum in schema:
            row.append(item.get(colum,'-'))
        result.add_row(row)
        i += 1
    return result

def getMarkDownTable(dictList, schema=[]):
    if type(dictList) != list:
        return None
    if len(dictList) == 0:
        return None
    i = 0
    result = []
    for item in dictList:
        if type(item) != dict:
            continue
        if i == 0:
            if len(schema) == 0:
                schema = item.keys()
            if len(schema) == 0:
                break
            for colum in schema:
                result.append('|')
                result.append(colum)
            result.append('|')
            result.append('\n')
            for i in range(0, len(schema)):
                result.append('|----------')
            result.append('|')
            result.append('\n')
        row = []
        for colum in schema:
            row.append('|')
            row.append(str(item.get(colum,'-')))
        row.append('|')
        row.append('\n')
        result += row
        i += 1
    return "".join(result)

def getMarkDownTitle(title,sub=1):
    if type(title) != str or len(title) == 0:
        return ''
    result = '#'
    for i in range(1,sub):
        result += '#'
    result += ' '
    result += title
    result += '\n'
    return result
    
def getMarkDownTableLine(dicttab, schema=[]):
    if type(dicttab) != dict:
        return ''
    result = ''
    hrule = '---'
    result += hrule
    result += '\n'
    row = []
    for colum in schema:
        row.append(colum)
        row.append(': ')
        row.append(str(dicttab.get(colum,'-')))
        row.append('\n')
    result += ("".join(row))
    result += hrule
    result += '\n'
    return result

def getMarkDownTableFromPretty(tab):
    if tab == None:
        return ''
    datastr = tab.get_string()
    junction_char = '+'
    headerjunction = junction_char + '\n'
    headerindex = datastr.find(headerjunction)
    if headerindex < 0 :
        return ''
    hrule = datastr[:headerindex+1]
    substr = datastr[headerindex+2:]
    sp = substr.split(hrule)
    if len(sp) == 0 :
        return ''
    header = sp[0]
    content =sp[1].strip(hrule)
    border = hrule.replace(junction_char, '|')
    return header + border + content

def getBlogMd(title,category,comments,tab,tabname=''):
    mdtable  = getMarkDownTableFromPretty(tab)
    mdtitle = getMarkDownTitle(tabname)
    comments = 'false'
    mdprof = getMarkDownTableLine({'layout':'post','title':title,'category':category,'comments':comments},
        ['layout','title','category','comments'])
    mdblog = mdprof + mdtitle + mdtable
    return mdblog
    
def quoteHtml(s):
    return quote(s)

def getHtmlTable(dictList, schema):
    maker = HtmlPageMaker()
    maker.addTable(dictList,schema)
    return maker

def sendHtmlMail(subject , contentHtml, attachments, config=None):
    if (config == None):
        config = "emailconfig.json"
    MailSender.sendHtmlMail(config, subject, contentHtml, attachments)
    
def sendTable(subject, dictList, schema, config=None):
    maker = getHtmlTable(dictList, schema)
    #fname = maker.getTitle() + '.html'
    fname = 'curattach.html'
    tab = getPrettyTable(dictList, schema)
    title = maker.getTitle()
    comments = 'false'
    mdblog = getBlogMd(title, 'stock', comments, tab)
    '''maker.getHtml()'''
    sendHtmlMail(subject, quoteHtml(mdblog) , [maker.saveFile(fname)], config)
    return mdblog
