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

if __name__ == '__main__':

	print len(getRequest("http://www.bing.com"))
	print len(postRequest("http://www.baidu.com",''))
	
	
