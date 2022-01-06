#!/usr/bin/env python
import time
import serial

ser = serial.Serial(
        port='/dev/ttyS0',
        baudrate = 19200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)

while 1:
        x=ser.readline()
        x_barray = bytearray(x)
        for i in range(len(x_barray)):
             if x_barray[i] == 0xfc:
                 x_barray[i] = 0x00
        x_str = x_barray.decode('UTF-8')
        if x_str.strip().startswith('Datum'):
             print('Datum received')
        elif x_str.strip().startswith('KLP'):
             print('Header1 received')
        elif x_str.strip().startswith('TKi'):
             print('Header2 received')
        print(x_str)
