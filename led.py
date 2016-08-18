#!/usr/bin/python
import threading
import ConfigParser
import sys
import time
import RPi.GPIO as GPIO

class MyLed(threading.Thread):    
    def getpindata(self,pinname, defpinvalue,defpinsinksrcmode):
        pinvalue,pinmode = defpinvalue, defpinsinksrcmode   
        pinmodename = str(pinname) + 'mode'

        if not self.cf.has_section(self.cfgsection):
            self.cf.add_section(self.cfgsection)

        # get pin value
        if not self.cf.has_option(self.cfgsection, pinname):
            self.cf.set(self.cfgsection, pinname, str(defpinvalue))
        pinvalue = self.cf.get(self.cfgsection, pinname
           
        # get pinsinksrcmode
        if not self.cf.has_option(self.cfgsection, pinmodename):
            self.cf.set(self.cfgsection, pinmodename, defpinsinksrcmode)
        pinmode = self.cf.get(self.cfgsection, pinmodename)

        # save configfile 
        fp = open(self.configfile,"w")
        self.cf.write(fp)
        
        # return pin data
        return (int(pinvalue), pinmode)

    def getpinmode(self,pinname, sinksrcmode):
        pinmodename = str(pinname) + 'mode'
        if self.cf.has_option(self.cfgsection, pinmodename):
            return self.cf.getint(self.cfgsection, pinmodename)

        if not self.cf.has_section(self.cfgsection):
            self.cf.add_section(self.cfgsection)
        
        self.cf.set(self.cfgsection, pinmodename, sinksrcmode)
        fp = open(self.configfile,"w")
        self.cf.write(fp)
        return int(defpinvalue)
        
    def __init__(self, pinname, pinvalue,sinksrcmode='sink'):
        threading.Thread.__init__(self)
        self.cfgsection = 'ledconf'
        self.sinksrcmode = sinksrcmode
        
        # init configparser
        self.configfile = sys.path[0] + '/config.ini'
        self.cf = ConfigParser.ConfigParser(allow_no_value=True)
        self.cf.read(self.configfile)        
        
        # read pin
        self.ledpin,self.sinksrcmode = self.getpindata(pinname, pinvalue, sinksrcmode)        
        # read sequence info
        self.seqs = self.readSeqs()
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)        
        GPIO.setup(self.ledpin, GPIO.OUT)
        
        # set const sequence transfer info
        self.short = [0.3,0.3]
        self.long = [1,0.3]
        self.on = [1,0]
        self.off = [0,1]
        self.space = [1]
        self.error = self.off
        
        # set breath led paramters
        self.pwm = GPIO.PWM(self.ledpin, 200)
        self.bf = 16  # breath frequency
        self.br=range(0,100,10) + range(100,0,-10)
        self.bt = 60.0/self.bf #  60 secondes 
        self.st = self.bt/len(self.br)  # sleep time
        
        # initial status
        self.status = 0                

    def __del__(self):
        threading.Thread.__del__(self)
        GPIO.cleanup()

    def readSeqs(self):
        tmpList=[]
        for i in range(20):
            if self.cf.has_option(self.cfgsection,'seq_'+str(i)):
                seq = self.cf.get(self.cfgsection, 'seq_'+str(i))
                tmpList.append( map(str.strip, seq.split(',')))            
            else:                
                tmpList.append([])                
        return tmpList

    def transferseq(self,s):
        if s.upper() == 'S':
            return self.short
        if s.upper() == 'L':
            return self.long
        if s.upper() == 'ON':
            return self.on
        if s.upper() == 'OFF':
            return self.off
        else:
            return []
        
    def getseq(self):
        try:
            if int(self.status) in range(20):                                
                return reduce(lambda x,y: x+y, map(self.transferseq, self.seqs[self.status]))
            else:                
                return self.error
        except Exception as e:
            print str(e)
            return self.error                   
        
    def run(self):
        while True:
            seq = self.getseq()
            if seq == None or len(seq)==0:
                self.pwm.start(0)
                self.breath()
            else:
                self.pwm.stop(0)
                self.blink(seq)

    def blink(self, seq =[1, 1]):
        stat = GPIO.HIGH if self.sinksrcmode.upper() == 'SRC' else GPIO.LOW
        for i in seq:
            GPIO.output(self.ledpin, stat)
            time.sleep(i)
            stat = not stat

    def updateStatus(self, stat):
        self.status = stat

    # bf : breath Frequence  
    # bt : breath circle
    def breath(self ):
        for i in self.br: 
            self.pwm.ChangeDutyCycle(i)
            time.sleep(self.st)
            
    
if __name__ == '__main__': 
    myled = MyLed('ledpin', 23,sinksrcmode='sink')
    myled.setDaemon(True)    
    myled.start()
    mybuzzer = MyLed('buzzerpin', 24)
    mybuzzer.setDaemon(True)    
    mybuzzer.start()

    try:
        while True:
            stat = input("please input led mode index(0~9):")
            if stat in range(10):
                print  'led mode is :',myled.seqs[stat]
            else:
                break
            myled.updateStatus(stat)
            mybuzzer.updateStatus(stat)
    except Exception as e:
        print str(e)
    finally:
        GPIO.cleanup()
            
