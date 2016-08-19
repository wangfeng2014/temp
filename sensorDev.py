#!/usr/bin/python
    
import urllib
import time
import random

import logging  
import logging.config
import ConfigParser
import sys
import os

import myHttp  


class sensorDev:
    def __init__(self):
        self.logger = logging.getLogger('root.sensor')           
        self.isInitialized = False
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(sys.path[0]+'/config.ini')
        self.server = self.cf.get('baseconf','server_ip')
        self.server_port = self.cf.get('baseconf', 'server_port')
        self.sn = self.cf.get('baseconf','serial_number')
        self.interval = self.getInterval()
        self.alarm = self.isAlarmEnabled()
        self.t_ltd = self.cf.getfloat('fromserverconf','t_ltd')
        self.t_htd = self.cf.getfloat('fromserverconf','t_htd')
        self.h_ltd = self.cf.getfloat('fromserverconf','h_ltd')
        self.h_htd = self.cf.getfloat('fromserverconf','h_htd')

    def getInterval(self):
        try:
            return self.cf.getfloat('fromserverconf','transinterval')
        except Exception as e:
            self.logger.error(str(e))
            return 20
        
    def isAlarmEnabled(self):
        try:
            return self.cf.getboolean('fromserverconf','alarm')
        except Exception as e:
            self.logger.debug(str(e))
            return False            
        
    def loadOptionsFromFile(self):    
        self.cf.read('config.ini')

    def saveOptionsToFile(self):
        self.cf.write(open('config.ini','w'))        
    
    def applyOptions(self,options):
        try:
            for i in options.split('\n'):
                j = i.strip().split('=')
                if len(j) == 2:
                    if self.cf.has_option('fromserverconf',j[0]):                    
                        self.cf.set('fromserverconf', j[0], j[1])
                    else:
                        self.logger.error("not support option: " + str(j))

        except Exception as e:
            self.logger.error(str(e))
        finally:
            self.saveOptionsToFile()
        
    def initFromServer(self):
        path = '/sensor?'
        data = {'SN':self.sn, 'CMD':'init'}        
        ret = self.sendSensorData(path, data)
        if ret.find('GET OPTION') != -1:
            self.applyOptions(ret)
            self.isInitialized = True
            return True
        return False
        
    def reportData(self,temp,humi):
        path = '/sensor?'                   
        data = { 'SN':self.sn, 'TM':temp, 'HM':humi, 'CMD':''}        
        return self.sendSensorData(path, data)        

    def sendCmdResult(self, index,result,cmd):
        path = '/sensorcmd'
        data = {'SN':self.sn, 'ID':index, 'Return':result, 'CMD':cmd}     
        try:
            url = "http://" + self.server + ":" + self.server_port + path
            ret =  myHttp.postRequest(url,urllib.urlencode(data)+'\n')            
            self.logger.debug("send: " + url)
            self.logger.debug("recv: " + ret)
            return ret
        except Exception as e:
            self.logger.error( url+'\n'+str(e))
            return ''
                
    def sendSensorData(self,path,data):
        try:
            url = "http://" + self.server + ":" + self.server_port + path + urllib.urlencode(data)
            ret =  myHttp.getRequest(url)            
            self.logger.debug("send: " + url)
            self.logger.debug("recv: " + ret)
            return ret
        except Exception as e:
            self.logger.error( url+'\n'+str(e))
            return ''

    def runSingleCmd(self,cmdcontent):
        result=''
        cmdindex,cmd = cmdcontent
        cmd = cmd.strip().upper() 
        if cmd == 'INIT':       
            result =self.initFromServer()
            self.sendCmdResult(cmdindex,result,cmd)        
        elif cmd == 'REBOOT':
            result = 'ok'
            self.sendCmdResult(cmdindex,result,cmd)        
            os.system('sudo reboot')
    
    
    def runCmd(self,cmd):        
        try:
            cmdlist = self.getCmdContent(cmd)
            for i in cmdlist:
                print i
                self.runSingleCmd(i)

        except Exception as e:
            logger.error(str(e))


    def getCmdContent(self,cmd):        
        return map(lambda x:x.split(':')[1:3],
            filter(lambda x:x.startswith('C:') and x.count(':')>=2, cmd.splitlines()))
        
if __name__ == '__main__':
    logging.config.fileConfig("logger.conf")
    sensor = sensorDev()
    print sensor.getInterval()
    print sensor.isAlarmEnabled()
    #sensor.initFromServer()
    sensor.runCmd('C:121:DATA INIT')    
    sensor.runCmd('C:123:INIT')
    sensor.runCmd('C:123:init xxyasdfaf')
    sensor.runCmd('C:124:init \nC:125:init \nC:126:init ')
        
    
