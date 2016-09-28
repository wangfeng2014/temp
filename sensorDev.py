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
import commands

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
        self.version = '1.26.8'
        self.cf.set('toserverconf','version',self.version)
        self.uri = '/sd/backend/web/index.php?'



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
        #http://localhost:8088/sd/backend/web/index.php?r=sensorclient/init&SN=1
        route ={'r':'sensorclient/init'}
        data = {'SN':self.sn, 'CMD':'init', 'VER':self.version}
        ret = self.sendSensorData(self.uri,route, data)
        if ret.find('GET OPTION') != -1:
            self.applyOptions(ret)
            self.isInitialized = True
            return True
        return False


    def getCmdRequest(self):
        route={'r':'sensorclient/getcmdrequest'}
        data = {'SN':self.sn}
        ret = self.sendSensorData(self.uri, route, data)
        if ret.find('C:') != -1:
                self.runCmd(ret)

    def reportData(self,temp,humi):
        route={'r':'sensorclient/report'}
        data = { 'SN':self.sn, 'TM':temp, 'HM':humi, 'CMD':''}

        return self.sendSensorData(self.uri, route, data)

    def sendCmdResult(self, index,result,cmd,extdata={}):
        route={'r':'sensorclient/sensorcmd'}
        data = {'SN':self.sn, 'ID':index, 'RETURN':result, 'CMD':cmd}
        data.update(extdata)
        return self.sendSensorData(self.uri, route, data,"POST")

    def sendSensorData(self,path,route,data,sendtype="GET"):
        try:
            if(sendtype == "GET"):
                route.update(data)
                url = "http://" + self.server + ":" + self.server_port + path + urllib.urlencode(route)
                ret =  myHttp.getRequest(url)
            else:
                url = "http://" + self.server + ":" + self.server_port + path + urllib.urlencode(route)
                ret =  myHttp.postRequest(url,urllib.urlencode(data)+'\n')

            self.logger.debug("send: " + url)
            self.logger.debug("data: " + urllib.urlencode(data))
            self.logger.debug("recv: " + ret)
            return ret
        except Exception as e:
            self.logger.error(str(e))
            return ''

    def runSingleCmd(self,cmdcontent):
        result=''
        cmdindex,cmd = cmdcontent
        if cmd.strip().upper().startswith('INIT'):
            result =self.initFromServer()
            self.sendCmdResult(cmdindex,result,cmd)
        elif cmd.strip().upper().startswith('REBOOT'):
            result = 'ok'
            self.sendCmdResult(cmdindex,result,cmd)
            os.system('sudo reboot')
        elif cmd.strip().upper().startswith('SHELL'):
            realcmd = cmd[5:]
            value, ret =  commands.getstatusoutput(realcmd)
            # save cmd result ot file shellout.txt??
            #print 'runcmd',realcmd,ret, value
            extdata = {"FILENAME":"shellout.txt", "CONTENT":ret}
            self.sendCmdResult(cmdindex, value,"SHELL",extdata)


    def runCmd(self,cmd):
        try:
            cmdlist = self.getCmdContent(cmd)
            for i in cmdlist:
                print 'getcmd:',i
                self.runSingleCmd(i)

        except Exception as e:
            self.logger.error(str(e))


    def getCmdContent(self,cmd):
        return map(lambda x:x.split(':')[1:3],
            filter(lambda x:x.startswith('C:') and x.count(':')>=2, cmd.splitlines()))

if __name__ == '__main__':
    logging.config.fileConfig("logger.conf")
    sensor = sensorDev()

    print sensor.getInterval()
    print sensor.isAlarmEnabled()
    print sensor.server
    print sensor.server_port
    print sensor.initFromServer()
    print sensor.getCmdRequest()
    print sensor.reportData(13.1,16.2)


    print '------test wrong sn------------------------'
    sensor.sn=232
    print sensor.initFromServer()
    print sensor.getCmdRequest()
    print sensor.reportData(13.3,16.4)


    #print '-----------'
    #print ret
   # print '==================='

   #     sensor.runCmd(ret)
    #sensor.runCmd('C:121:DATA INIT')
    sensor.sn=222
    sensor.runCmd('C:123:INIT')
    #sensor.runCmd('C:123:init xxyasdfaf')
    #sensor.runCmd('C:123:SHELL ls -l')
    #sensor.runCmd('C:123:SHELL sed -i s/shanghai/beijing/g aa')
    #sensor.runCmd('C:124:init \nC:125:init \nC:126:init ')


