# -*- coding: utf-8 -*- 
# @Time : 2022/3/1 20:16 
# @Author : 能飞会打智勇双全的才高八斗 
# @File : LiNan.py

import time
import serial #导入模块
import threading
from datetime import datetime
STA_Serial = input('串口号:')
# STA_Serial = 'COM4'
bps1 = input('波特率:')
STA_For_timeout = 240
class AIC():
    def __init__(self):
        self.ser = None
    def STA(self):
        try:
            portx = STA_Serial
            bps = bps1
            timex = None
            self.ser = serial.Serial(portx, bps, timeout=timex)
            self.ser.write('\r'.encode("utf-8"))
            time.sleep(0.2)
            self.ser.write('root\r'.encode("utf-8"))
            time.sleep(0.2)
            self.ser.write('iot_ipc@360\r'.encode("utf-8"))
            time.sleep(0.1)
            self.ser.write('\r'.encode("utf-8"))
            time.sleep(0.1)
            self.ser.write('watchdog &\r'.encode("utf-8"))
            time.sleep(0.1)
            self.ser.write('\r'.encode("utf-8"))
            while True:
                if self.ser.in_waiting:
                    c5 = self.ser.readline().decode(encoding='UTF-8', errors='ignore')
                    if (c5 == "exit"):  # 退出标志
                        break
                    else:
                        # print(c5)
                        with open('P8循环日志.txt', 'a',encoding='UTF-8', errors='ignore') as log:
                            log.writelines(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' ' + c5)
                        if 'CPU: 0 PID' in c5:
                            print(f'{datetime.now()}:P8串口:OOM{c5}')
                        if 'Out of memory' in c5:
                            print(f'{datetime.now()}P8串口:Out of memory:{c5}')
                            self.Serial_send()
                        if 'U-Boot SPL' in c5:
                            print(f'{datetime.now()}P8串口:主程序重启了:{c5}')
            self.ser.close()  # 关闭串口

        except Exception as e:
            print("---异常---：", e)
            pass

    def Serial_send(self):
        time.sleep(45)
        self.ser.write('\r'.encode("utf-8"))
        time.sleep(0.2)
        self.ser.write('root\r'.encode("utf-8"))
        time.sleep(0.2)
        self.ser.write('iot_ipc@360\r'.encode("utf-8"))
        time.sleep(0.1)
        self.ser.write('\r'.encode("utf-8"))
        time.sleep(0.1)
        self.ser.write('watchdog &\r'.encode("utf-8"))
        time.sleep(0.1)
        self.ser.write('\r'.encode("utf-8"))
        print('P8串口:----发送命令成功')

bb =AIC()
bb.STA()

# i = 0
# t = threading.Thread(target=bb.STA)
# t.start()
# time.sleep(5)
# def aa():
#     while True:
#
#         time.sleep(240)
# aa()
