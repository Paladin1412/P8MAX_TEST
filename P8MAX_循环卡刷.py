# -*- coding: utf-8 -*- 
# @Time : 2022/10/11 20:12 
# @Author : 能飞会打智勇双全的才高八斗 
# @File : P8MAX_循环卡刷.py
import os
import sys
import time
import serial #导入模块
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By
import threading
from selenium.webdriver.support.wait import WebDriverWait #导入显性等待的包
from datetime import datetime
STA_old_VERSION = 'P8MAX_V1.1.12.8_20221005_191802_upgrade.bin'
Serial_num = 'COM11'
class All_huawei_p20_pro():
    def __init__(self):
        self.ser = None

    def P8_Serial(self):
        try:
            portx = Serial_num
            bps = 115200
            timex = None
            self.ser = serial.Serial(portx, bps, timeout=timex)
            self.Serial_UP_P8()
            print('P8串口:----链接串口成功')
            while True:
                if self.ser.in_waiting:
                    c5 = self.ser.readline().decode(encoding='UTF-8', errors='ignore')
                    if (c5 == "exit"):  # 退出标志
                        break
                    else:
                        # print(c5)
                        # print('open')
                        with open('P8_循环卡刷.log', 'a', encoding='UTF-8', errors='ignore') as log:
                            log.writelines(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' ' + c5)
                        if 'Ready sd upgrade' in c5:
                            print('P8MAX------------------------:进入回退版本流程,' + str(datetime.now()))
                            # break
                        if 'soc-nna version' in c5:
                            print('P8MAX------------------------:回退完成,完成重启,' + str(datetime.now()))
                            self.Serial_UP_P8()
                        if 'U-Boot SPL' in c5:
                            print('P8MAX------------------------:回退完成,重启中,' + str(datetime.now()))
                            # break
            # print('超时退出')
            self.ser.close()  # 关闭串口
        except Exception as e:
            print("---异常---：", e)
            pass

    def Serial_UP_P8(self):
        time.sleep(5)
        self.ser.write('\r'.encode("utf-8"))
        time.sleep(2)
        self.ser.write('root\r'.encode("utf-8"))  # 账号.
        time.sleep(0.2)
        self.ser.write('iot_ipc@360\r'.encode("utf-8"))  # 密码.
        self.ser.write('\r'.encode("utf-8"))
        time.sleep(0.2)
        self.ser.write('\r'.encode("utf-8"))
        time.sleep(0.2)
        self.ser.write(f'sd_upgrade.sh /mnt/sd/{STA_old_VERSION}\r'.encode("utf-8"))  #
        self.ser.write('\r'.encode("utf-8"))
        print('P8串口:----发送卡刷成功')

AIC =All_huawei_p20_pro()
target=AIC.P8_Serial()
