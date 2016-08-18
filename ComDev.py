#!/usr/bin/python
import serial
import binascii
import struct
import time

class ComDev:
    def __init__(self):
        self.com = None

    def Open(self,com):
        try:
            self.com = serial.Serial(com,baudrate=9600, bytesize=8,parity='N',
            stopbits=1,xonxoff=0, timeout=3)
            return True
        except:
            self.com = None
            print 'Open %s fail!' %com
            return False

    def Close(self):
        if type(self.com) != type(None):
            self.com.close()
            self.com = None
            return True
        return False

    def ReadData(self,RevBytes):
        if type(self.com) != type(None):
            try:
                data = self.com.read(RevBytes)
                return data
            except Exception as e:
                print 'ReadData fail!' + str(e)
                self.Close()
                return None
        return None

    def SendData(self,Data):
        if type(self.com) != type(None):
            try:
                self.com.write(Data)
                return True
            except Exception as e:
                print 'SendData fail!' + str(e)
                self.Close()
                return False
        return False

    def IsOpened(self):
            return not (self.com == None)
            

        
if __name__ == '__main__':
        senddata="01 03 00 00 00 02 C4 0B"
        dev = ComDev()
        dev.Open('/dev/ttyUSB0')
        if type(dev.com) != type(None):
                while 1:
                        time.sleep(1)
                        dev.SendData(binascii.a2b_hex(senddata.replace(' ','')))
                        recvdata=dev.ReadData(9)
                        if recvdata == None:
                            print 'recv data none'
                            continue
                        else:    
                            print 'recv data length =', len(recvdata)
                            print binascii.b2a_hex(recvdata)
                        if recvdata != None and len(recvdata) == 9:
                                print len(recvdata),
                                print binascii.b2a_hex(recvdata)
                                temp,humi = struct.unpack('!2h',recvdata[3:7])
                                print temp/10.0, humi/10.0
        dev.Close()
