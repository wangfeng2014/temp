#!/usr/bin/python
import urllib
import urllib2

def getRequest(url,timeout=10):    
        req = urllib2.Request(url)
        res_data = urllib2.urlopen(req,timeout=timeout)
        res = res_data.read()
        return res

def postRequest(url,data,timeout=10):
        req = urllib2.Request(url = url,data =data)
        res_data = urllib2.urlopen(req,timeout=timeout)
        res = res_data.read()
        return res    


def post(url,data):
    data='ID=520&Return=0&CMD=DATA\r\n'
    url = "http://192.168.1.119:80/iclock/devicecmd?SN=3292162300001"
    print postRequest(url,data)
    
if __name__ == '__main__':

        #url = "http://localhost/getrequest?SN=3292162300001"
        #req = urllib2.Request(url)
        #res_data = urllib2.urlopen(req)
        #a= res_data.read()
        #print len(a), a
        post('','')
        print 'xxx'
        
	
	#b=getRequest("http://192.168.1.119:8080/iclock/getrequest?SN=3292162300001")
	#print a
	#print b
	
	
	
