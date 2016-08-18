#!/usr/bin/python
    

import ConfigParser
import sys
import os

import myHttp  


class sensorDev:
    def __init__(self):
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(sys.path[0]+'/config.ini')

    def getInterval(self):
            return self.cf.get('fromserverconf','transinterval')
        
        
    def loadOptionsFromFile(self):    
        self.cf.read('config.ini')

    def saveOptionsToFile(self):
        self.cf.write(open('config.ini','w'))        
        
if __name__ == '__main__':
    sensor = sensorDev()
    sensor.cf.set("baseconf",'haha', 'it is fun')
    sensor.cf.set("baseconf",'lala', None)
    sensor.cf.set("toserverconf",'haha', 'it is fun')
    sensor.cf.set("toserverconf",'lala', None)
    s = sensor.cf.get("baseconf",'seq_9')
    print 's is ', type(s), s, len(s)
    sensor.saveOptionsToFile()
    print sensor.getInterval()
        
    
