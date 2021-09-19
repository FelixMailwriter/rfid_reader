# -*- coding: utf-8 -*-
from rfid_reader import Rfid_reader
import sys
import reader_driver as reader
import crcmod


def getCrc(msg):
    crc = crcmod.new()
    crc.update(msg)
    return crc.digest()

def getcrc(command):
    xmodem_crc_func = crcmod.mkCrcFun(0x18005, rev=False, initCrc=0xFFFF, xorOut=0x0000)
    a = xmodem_crc_func(command)
    lb = a&0xFF
    hb = a>>8
    return lb, hb

if __name__ == '__main__':
    #reader = Rfid_reader("/dev/ttyAMA0")

    # if len(sys.argv) != 2:
    #     print("usage: uhf TTY_SERIAL")
    #     sys.exit(2)quit

    a = b'\x04\x01\x00\x12\x04'
    reader = reader.UHReader()
    # reader.openPort()
    reader.sendCommand(a)

    answer = reader.getDataFromPort()
    print(answer)
    reader.sr.close()


    # uhfr = reader.UHFReader18()
    # # uhfr.openPort(sys.argv[1], 57600)
    # uhfr.openPort("/dev/ttyAMA0", 115200)
    #
    # reader.UI(uhfr).run()
