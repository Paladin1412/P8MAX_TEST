# -*- coding: utf-8 -*- 
# @Time : 2022/9/22 11:42 
# @Author : 能飞会打智勇双全的才高八斗 
# @File : 继电器_控制.py
import threading
import time
import serial #导入模块
from datetime import datetime
STA_Serial = 'COM3'
def Power():
    portx = STA_Serial
    bps = 9600
    timex = None
    ser = serial.Serial(portx, bps, timeout=timex)
    # ser.write('\r'.encode("utf-8"))
    # ser.write(bytes.fromhex('AE 20 01 28 02 01 01 AC'))  # 16进制 1路开.
    # ser.write(bytes.fromhex('AE 20 01 28 02 01 00 AC'))  # 16进制 1路关.
    # ser.write(bytes.fromhex('AE 20 01 29 03 FF FF 00 AC'))  # 16进制 总开关 全开.
    ser.write(bytes.fromhex('AE 20 01 29 03 FF 00 00 AC'))  # 16进制 总开关 全关.
Power()

""""
协议格式：(波特率9600)
 发送均为 16进制.  python控制写法: ser.write(bytes.fromhex('AE 20 01 28 02 01 01 AC')) # 16进制


通道1   关：   AE 20 01 28 02 01 00 AC  开：   AE 20 01 28 02 01 01 AC

通道2   关：   AE 20 01 28 02 02 00 AC  开：   AE 20 01 28 02 02 01 AC

通道3   关：   AE 20 01 28 02 03 00 AC  开：   AE 20 01 28 02 03 01 AC

通道4   关：    AE 20 01 28 02 04 00 AC  开：   AE 20 01 28 02 04 01 AC

通道5   关：  AE 20 01 28 02 05 00 AC  开：   AE 20 01 28 02 05 01 AC

通道6   关：  AE 20 01 28 02 06 00 AC  开：   AE 20 01 28 02 06 01 AC

通道7   关：  AE 20 01 28 02 07 00 AC  开：   AE 20 01 28 02 07 01 AC

通道8   关：  AE 20 01 28 02 08 00 AC  开：   AE 20 01 28 02 08 01 AC
2.单机总按键:（序列开关） 全关:  AE 20 01 29 03 FF 00 00 AC  全开：AE 20 01 29 03 FF FF 00 AC

3.单机的全部通道:（先把下面设置开和关命令各发送一遍作为保存    这样下面全开/全关才起作用）
               设置 关：   AE 20 01 BB 0B 00 40 08 40 40 40 40 40 40 40 40 AC
               设置 开：   AE 20 01 BB 0B 00 30 08 40 40 40 40 40 40 40 40 AC
				全关：   AE 20 01 29 03 FF 00 02 AC
	    全开：   AE 20 01 29 03 FF FF 01 AC

"""