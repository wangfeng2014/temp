#!/usr/bin/python
#
# simulate multi-sensors to send temperature and huminity data to web server
# 

import urllib
import time
import random
import myHttp  


while True:
    for sn in range(40):
        server = "192.168.1.119"
        temp = 20 + float("%.1f"%random.random())
        humi = 60 + float("%.1f"%random.random())
        cmd = ''
        data = { 'SN':sn, 'TM':temp, 'HM':humi, 'CMD':cmd}
        url = "http://" + server + "/sensor?"+ urllib.urlencode(data)                   
        try:
            ret = myHttp.getRequest(url)
            print 'send:',url
            print 'recv:',ret
        except Exception as e:
            print 'get exception:',str(e)

    time.sleep(5)

        
	
