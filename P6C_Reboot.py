# -*- coding: utf-8 -*- 
# @Time : 2022/7/15 16:23 
# @Author : 能飞会打智勇双全的才高八斗 
# @File : P6C_Reboot.py
import os
import threading
import time
import serial  # 导入模块
from datetime import datetime
from numpy import *
import tkinter.messagebox as msgbox   # 窗口
# COM_Serial = 'COM44'
# COM_bps = 115200
timeout_mean = []

COM_Serial = 'COM29'
COM_bps = 115200
XianShi = 60
class WangWang_Sang():
    def __init__(self):
        self.ser =None

    def Serial_COM(self):
        portx = COM_Serial
        bps = COM_bps
        timex = None
        self.ser = serial.Serial(portx, bps, timeout=timex)
        print('SB----:串口链接成功')
        while True:
            if self.ser.in_waiting:
                c5 = self.ser.readline().decode(encoding='gbk', errors='ignore')
                if (c5 == "exit"):  # 退出标志
                    break
                else:
                    with open('SBWangHui_kill.log', 'a', encoding='gbk', errors='ignore') as log:
                        log.writelines(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' ' + c5)
                    # print(c5)
                    if 'stream off' in c5:  #stream off 杀主程序的用这个   Requesting system reboot 重启用这个
                        Requesting_system_reboot = datetime.now()
                    if 'ONLINE' in c5:
                        ONLINE = datetime.now()
                        try:
                            Reboot_time_out = (ONLINE - Requesting_system_reboot).seconds
                            timeout_mean.append(Reboot_time_out)
                            print(f'当前重启耗时{Reboot_time_out}s,平均重启耗时{mean(timeout_mean)}s')
                            with open('P6数据SBWangHui.log', 'a', encoding='gbk', errors='ignore') as log:
                                log.writelines(str(Requesting_system_reboot) + ' ' +f'当前执行第{i}次 ,本次重启耗时{Reboot_time_out}s, 总平均重启耗时{mean(timeout_mean)}s\r')
                        except:
                            print('没收到Requesting system reboot或stream off打印')
                            pass

    def COM_Write(self):
        self.ser.write('\r'.encode("utf-8"))
        time.sleep(0.2)
        # self.ser.write('reboot\r'.encode("utf-8"))
        self.ser.write('killall -9 camera\r'.encode("utf-8"))
        time.sleep(0.2)
        self.ser.write('\r'.encode("utf-8"))
        print('发送kill成功')

    def User_Password(self):
        self.ser.write('\r'.encode("utf-8"))
        time.sleep(1)
        self.ser.write('\r'.encode("utf-8"))
        time.sleep(1)
        self.ser.write('root\r'.encode("utf-8"))
        time.sleep(0.1)
        self.ser.write('iot_ipc@360\r'.encode("utf-8"))

SB_WangHui = WangWang_Sang()
sb1 = threading.Thread(target=SB_WangHui.Serial_COM)
sb1.start()
i = 0
time.sleep(5)
while True:
    i += 1
    print(f'======执行第{i}次=======')
    # msgbox.showinfo('双工已唤醒:', '请语音大声呼喊:我是大傻逼,否则关机')  # 弹窗提示
    # os.system('shutdown -t 10 -s')
    SB_WangHui.User_Password()
    SB_WangHui.COM_Write()
    time.sleep(int(XianShi))    # 300
