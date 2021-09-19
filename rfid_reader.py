# -*- coding:utf-8 -*-

import serial
from crc import CRC
# from enum import __repr__
import binascii
# import arcpy

class Rfid_reader(object):



    def __init__(self, uart_path):
        self.commCodeList={"getReaderInformation":0x21,}
        # self.prn_config = self._getSettings()
        self.uart_path = uart_path  # Путь к reader
        self.crc = CRC()
        self.status = []
        self.prn = self._getConnection(self.uart_path)

    def run(self, items, checkType='NotFisk'):
        self.items = items
        self.checkType = checkType
        self._printCheck()


    # def _getStatusBytes(self):
    #     status = []
    #     self._openPort()
    #     self._sendCommand(0x4A, '')
    #     self.msleep(100)
    #     answer = self._getAnswer()
    #     beginRead = False
    #     if answer is None:
    #         self.prn.close()
    #         raise RfidReaderHardwareException(u'Reader is not found')
    #         return
    #     for statusByte in answer:
    #         statusByte = statusByte.encode('hex')
    #         if statusByte == '04':
    #             beginRead = True
    #             continue
    #         if statusByte == '05':
    #             self.prn.close()
    #             return status
    #         if beginRead:
    #             byteStr = self._byte2bits(statusByte)
    #             byteStr = byteStr[2:]
    #             revertStr = byteStr[::-1]
    #             status.append(revertStr)
    #             print
    #             status
    #     self._closePort()
    #     return status

    def _getConnection(self, devPath):
        try:
            conn = serial.Serial()
            conn.port = devPath
        except:
            raise RfidReaderHardwareException(u'Reader is not found')

        conn.baudrate = 115200
        conn.bytesize = serial.EIGHTBITS  # number of bits per bytes
        conn.parity = serial.PARITY_NONE  # set parity check: no parity
        conn.stopbits = serial.STOPBITS_ONE  # number of stop bits
        conn.timeout = None  # block read
        conn.xonxoff = False  # disable software flow control
        conn.rtscts = True  # disable hardware (RTS/CTS) flow control
        conn.dsrdtr = True  # disable hardware (DSR/DTR) flow control
        return conn

    def _getCommand(self, name, data=[]):
        try:
            commCode = self.commCodeList['getReaderInformation']
        except:
            return 0

        commLength = len(data) + 4
        comm=bytearray(commLength+1)
        comm[0] = commLength
        comm[1] = 0xFF
        comm[2] = commCode
        counter = 3
        for d in data:
            comm[counter] = d
            counter + 1

        scmd = memoryview(comm)[1, commLength - 3]
        comm[commLength - 2], comm[commLength - 1] = self.crc.getcrc(scmd)


    def _openPort(self):
        try:
            self.prn.open()
        except:
            raise RfidReaderHardwareException(u'Reader is not found')

    def _closePort(self):
        if self.prn.isOpen():
            self.prn.close()

    def _getAnswer(self):
        # получение данных от принтера
        print
        'wait for answer...'
        for i in range(1, 4):
            print ('iter %d' % (i))
            l = self.prn.inWaiting()
            print (l)
            if l > 0:
                data = self.prn.read(l)
                print ('answer received')
                print ('data length ')
                print (len(data))
                self.showRecevedData(data)
                return data
            self.msleep(1000)

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