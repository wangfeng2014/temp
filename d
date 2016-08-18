#!/bin/bash
pid=$(ps -ef|grep temp.py |grep -v grep|awk {'print $2'})
if [[ $pid ]] ; then
sudo kill $pid 
fi


