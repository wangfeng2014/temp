#!/usr/bin/python
import logging
import logging.config
import ConfigParser
import sys

import sensorDev
import ComDev
import led
import binascii
import time
import struct
import socket
import commands

class Status:
    PowerOn = 0
    BuzzerSilence = 8
    NormalRun = 9
    # error
    OpenSensorFail = 1
    ReadSensorFail = 2
    NetWorkError = 3
    TempTooLow = 10
    TempTooHigh = 11
    HumiTooLow = 12
    HumiTooHigh = 13



def runOnlyOne():
    try:
        global s
        s = socket.socket()
        host = socket.gethostname()
        s.bind((host,12345))
    except:
        print 'program already has a instance. exit now'
        sys.exit()

def getTempAndHumi(comdev):
    comdev.SendData(senddata)
    recvdata=comdev.ReadData(9)
    if recvdata != None and len(recvdata) == 9:
            logger.debug("recv data: " + binascii.b2a_hex(recvdata))
            temp,humi = struct.unpack('!2h',recvdata[3:7])
            return (temp/10.0, humi/10.0)
    else:
        return (None,None)

def updateCommonError(status):
    myled.updateStatus(status)
    mybuzzer.updateStatus(status)

def getdevname():
    value, ret =  commands.getstatusoutput('ls -lh /dev/serial/by-id |grep -i serial')
    if  ret != '':
        dev = ret.split()[-1]
        dev = dev.split('/')[-1]
        return '/dev/'+dev
    else:
        return "/dev/ttyUSB0"



if __name__ == '__main__':
    try:
        runOnlyOne()
        logging.config.fileConfig(sys.path[0]+"/logger.conf")
        logger = logging.getLogger('root')

        CHECKMSG = "01 03 00 00 00 02 C4 0B"
        senddata = binascii.a2b_hex(CHECKMSG.replace(' ',''))

        comdev = ComDev.ComDev()
        sensor = sensorDev.sensorDev()

        mygreenled = led.MyLed('greenledpin', 21)
        mygreenled.updateStatus(Status.PowerOn)
        mygreenled.setDaemon(True)
        mygreenled.start()

        myled = led.MyLed('redledpin', 23)
        myled.updateStatus(Status.BuzzerSilence)
        myled.setDaemon(True)
        myled.start()

        mybuzzer = led.MyLed('byzzerpin', 24)
        mybuzzer.updateStatus(Status.BuzzerSilence)
        mybuzzer.setDaemon(True)
        mybuzzer.start()

        retryInterval = 15 # seconds

        devname =  getdevname()


        # main loop
        while True:

            # get cmd request from server. keep communiction with server even sensor is inaccessable.
            sensor.getCmdRequest()

            # check com device
            if not comdev.IsOpened():
                if not comdev.Open(devname):
                    logger.error("open usb com failed")
                    updateCommonError(Status.OpenSensorFail)
                    mygreenled.updateStatus(Status.PowerOn)
                    time.sleep(retryInterval)
                    continue

            # get data from sensor
            temp,humi = getTempAndHumi(comdev)
            if temp == None or humi == None:
                logger.error("no data get , reinitialize the com device.")
                comdev.Close()
                comdev.Open(devname)
                updateCommonError(Status.ReadSensorFail)
                mygreenled.updateStatus(Status.PowerOn)
                time.sleep(retryInterval)
                continue


            # get config from server
            if not sensor.isInitialized:
                if not sensor.initFromServer():
                    updateCommonError(Status.NetWorkError)
                    mygreenled.updateStatus(Status.PowerOn)
                    time.sleep(retryInterval*4)
                    continue

            # send sensor data to server
            ret = sensor.reportData(temp, humi)
            if ret == None or ret == '':
                updateCommonError(Status.NetWorkError)
                mygreenled.updateStatus(Status.PowerOn)
                time.sleep(retryInterval*3)
                continue



            # check the temp and humi range
            alarmstatus = Status.BuzzerSilence
            if sensor.alarm:
                if temp < sensor.t_ltd:
                    alarmstatus = Status.TempTooLow
                elif temp > sensor.t_htd:
                    alarmstatus = Status.TempTooHigh
                elif humi < sensor.h_ltd:
                    alarmstatus = Status.HumiTooLow
                elif humi > sensor.h_htd:
                    alarmstatus = Status.HumiTooHigh

            # set  led final status.
            updateCommonError(alarmstatus)
            mygreenled.updateStatus(Status.NormalRun)




            # send status???
            time.sleep(sensor.getInterval())
    finally:
            led.GPIO.cleanup()
