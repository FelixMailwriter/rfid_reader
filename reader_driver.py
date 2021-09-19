#!/usr/bin/env python3
import time
import serial
import sys


class UHReader(object):

    def __init__(self):
        self.openPort("/dev/ttyAMA0", 57600)

    def openPort(self, path, baud):
        self.port = path
        self.sr = serial.Serial()
        self.sr.baudrate = baud
        self.sr.port = path
        self.sr.stopbits = 2
        self.sr.dsrdtr = 1
        self.sr.startbits = 1
        self.sr.parity = 'N'

        self.sr.open()

    def sendCommand(self, command):
        self.sr.write(command)

    def getDataFromPort(self):
        for i in range(1, 4):
            try:
                l = self.sr.inWaiting()
                if l > 0:
                    data = self.sr.read(l)
                    print('answer received')
                    self.showRecevedData(data)
                    return data
                time.sleep(1)
            except:
                self.sr.close()
        self.sr.close()
        raise RfidReaderHardwareException(u'Devise not responding')

    def showRecevedData(self, data):
        # распечатка данных от принтера
        print ('---------------')
        print ('Reseived data:')
        s = ''
        for i in range(0, len(data)):
            s += data[i].encode('hex') + ' '
        print (s)
        print ('---------------')




class RfidReaderHardwareException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "" + self.value