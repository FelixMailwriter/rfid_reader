# -*- coding:utf-8 -*-

import crcmod


class CRC():

    def __init__(self):
        pass

    def getcrc(self, command):
        xmodem_crc_func = crcmod.mkCrcFun(0x18005, rev=False, initCrc=0xFFFF, xorOut=0x0000)
        a = xmodem_crc_func(command)
        lb = a & 0xFF
        hb = a >> 8
        return lb, hb