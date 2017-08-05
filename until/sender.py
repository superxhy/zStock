#!/usr/bin/env python
# -*- coding:utf-8 -*- 
'''
Created on 2017-5-5

@author: yuql
'''
 
from email.mime.multipart import MIMEMultipart
#from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.header import Header
from email.utils import COMMASPACE,formatdate
#from email import encoders
import smtplib
import threading
import os
 
class MailSender(object):
    '''
    minemultipart struct:
    *mixed
        *alternative
            *text
            *related
                *html
                *inline image
                *inline image
        *attachment
        *attachment
    '''
    MGS_ALT = 'alternative'
    MGS_REL = 'related'
    
    MAX_RETRY = 5
    
    '''
    #json format
    {u'addr': {u'fromAddr': u'my.test.com', u'toAddrs': [u'des1.test.com', u'des2.test.com']}, u'server': {u'passwd': u'mailpwd', u'user': u'mailuser', u'name': u'smtp.test.com', u'port': u'994'}}
    '''
    def __init__(self, config):
        self.__servername__ = ""
        self.__serverport__ = ""
        self.__user__ = ""
        self.__passwd__= ""
        self.__fromAddr__ = ""
        self.__toAddrs__= [""]
        self.__attachment__ = None
        if type(config) == str:
            self.__parsefile__(config)
        else:
            self.__parseconfig__(config)
        self.__checkconfig__()
        self.__initmessage__()
        self.__retry__ = 0
    
    def __parsefile__(self, fname):
        configobj = None
        f = open(fname)
        try:
            import json
            configobj = json.load(f)
            self.__parseconfig__(configobj)
        except Exception,e:
            print Exception,":",e
        finally:
            f.close()
        
    def __parseconfig__(self, config):
        server = config['server']
        addr = config['addr']
        self.__servername__ = server['name']
        self.__serverport__ = server['port']
        self.__user__ = server['user']
        self.__passwd__ = server['passwd']        
        self.__fromAddr__ = addr['fromAddr']
        self.__toAddrs__ = addr['toAddrs']
        
    def __checkconfig__(self):
        assert self.__servername__ != ""
        assert self.__serverport__ != ""
        assert self.__user__ != ""
        assert self.__passwd__!= ""
        assert self.__fromAddr__ != ""
        assert self.__toAddrs__ != [""]
        
    def __initmessage__(self): 
        msg = MIMEMultipart()
        msg['From'] = self.__fromAddr__ 
        msg['To'] = COMMASPACE.join(self.__toAddrs__) #COMMASPACE==',' 
        msg['Date'] = formatdate(localtime=True)
        #msg['Subject'] = Header("", 'utf-8')
        self.__msg__ = msg
        self.__msgalt__ = MIMEMultipart(self.MGS_ALT)
        self.__msgrel__ = MIMEMultipart(self.MGS_REL)
        #self.__msgalt__.attach(self.__msgrel__)
        #self.__msg__.attach(self.__msgalt__)
        
    def writePlain(self, subject, message):
        if subject != "":
            self.__msg__['Subject'] =  Header(subject, 'utf-8')
        self.__msgalt__.attach(MIMEText(message))
        
    def writeHtml(self, subject, html):
        if subject != "":
            self.__msg__['Subject'] = Header(subject, 'utf-8')
        self.__msgrel__.attach(MIMEText(html,'html','utf-8')) 
    
    def addAttach(self, files=[]):
        for fname in files: 
            f = open(fname, 'rb')
            try:
                #att = MIMEText(f.read(), 'base64', 'gb2312')
                att = MIMEText(f.read())      
                att["Content-Type"] = 'application/octet-stream'    
                att.add_header("Content-Disposition", "attachment", filename = os.path.basename(fname))
                self.__attachment__ = att
            except Exception,e:
                print Exception,":",e
            finally:
                f.close()  
            
    def send_block(self):
        ret = False
        try:
            #smtp = smtplib.SMTP()
            #port = int(self.__serverport__)
            #print "connect: %s:%s" %(self.__servername__,port)
            #if port == 0:
            #    smtp.connect(self.__servername__)
            #else:
            #    smtp.connect(self.__servername__,port)
            smtp = smtplib.SMTP_SSL(self.__servername__)
            print "login: %s:%s" %(self.__user__, "******")
            smtp.login(self.__user__, self.__passwd__) 
            print "sending...: %s" %(self.__fromAddr__)
            self.__msgalt__.attach(self.__msgrel__)
            self.__msg__.attach(self.__msgalt__)
            if self.__attachment__:
                print "add  attachment"
                self.__msgalt__.attach(self.__attachment__)
            #print self.__msg__
            smtp.sendmail(self.__fromAddr__, self.__toAddrs__, self.__msg__.as_string())
            print "sendend"
            ret = True
        except Exception,e:
            print Exception,":",e
        finally:
            try:
                smtp.quit()
            except Exception,e:
                print Exception,":",e 
                smtp.close()
        print "smtp end ret %s,retry %s" %(str(ret),str(self.__retry__))
        if ret:
            self.__retry__ = 0
        else:
            self.__retry__ += 1
            if self.__retry__ <= self.MAX_RETRY:
                self.send()
            else:
                print "smtp end retry !!" 
                self.__retry__ = 0
        return ret
    
    def send(self):
        print "thread start begin:"
        t = threading.Thread(target=MailSender.send_block, args=(self,))
        t.setDaemon(False)
        t.start()
        #no block
        t.join(300)
        print "thread %s start end" %(str(t))
        
    @staticmethod
    def sendPlainMail(config, subject , contentText, attachments=[]):
        sender = MailSender(config)
        sender.writePlain(subject, contentText)
        sender.addAttach(attachments)
        sender.send()

    @staticmethod
    def sendHtmlMail(config, subject , contentHtml, attachments=[]):
        sender = MailSender(config)
        sender.writeHtml(subject, contentHtml)
        sender.addAttach(attachments)
        sender.send()
        
