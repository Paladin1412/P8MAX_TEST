# -*- coding: utf-8 -*- 
# @Time : 2022/10/12 17:10 
# @Author : 能飞会打智勇双全的才高八斗 
# @File : P8MAX_频繁RESET键.py
import time
import serial #导入模块
from appium import webdriver
from selenium.webdriver.common.by import By
import threading
from selenium.webdriver.support.wait import WebDriverWait #导入显性等待的包
# from dateutil.parser import parse
import random  # 随机数
from datetime import datetime
# from numpy import *


Serial_num = 'COM69'
camera_Tuya_app = { #智能手臂 红米10
    "platformName": "Android",  # 测试手机为安卓
    "platformVersion": "10",    # 手机安卓版本
    "deviceName": "1977957e",  # 设备名称.  安卓手机可以留空
    "appPackage": "com.tuya.smartiot",  # 启动app的名称,adb shell dumpsys activity recents | find "intent={"      查看app名称 cmp=后面的 /前面的
    "appActivity": "com.smart.TuyaSplashActivity",  # 启动 appActivity名称activity是cmp斜杠后面的
    "automationName": "UiAutomator2",  #
    "newCommandTimeout": "1800",  # 连接超时
    "noReset": True,   # 不要重置app
    "resetKeyboard": True,   # 执行完程序恢复原来的输入法
    "unicodeKeyboard": True,  # 使用自带输入法 输入中文时填True
    'udid':"1977957e",
    "waitForIdleTimeout": 1 # 优化速度
    # 'udid':"AKC0218901000350"
}
abb= '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup[2]/android.view.ViewGroup[2]/android.view.ViewGroup[2]/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup/android.view.ViewGroup'

class AIC():
    def __init__(self):
        self.ser =None
        self.driver = None

    def JXB(self):
        try:
                self.driver = webdriver.Remote('http://localhost:4723/wd/hub', camera_Tuya_app)
                print('开启机械臂app')
                WebDriverWait(self.driver, 25, 1).until_not(lambda el2: self.driver.find_element(By.ID, "iv_ble_offline"))  # until_not 返回结果为false
                self.driver.find_element(By.XPATH,"//*[@content-desc='ty_home_device_name']").click()
                self.AN()
        except:
            return self.JXB()

    def AN(self):
        try:
            t2 = datetime.now()
            while (datetime.now() - t2).seconds <= 180:
                WebDriverWait(self.driver, 15, 1).until(lambda el2: self.driver.find_element(By.XPATH, abb))
                self.driver.find_element(By.XPATH,abb).click()
                print('P8MAX------------------------按键' + str(datetime.now()))
                time.sleep(60)
            self.driver.back()
        except:return  self.JXB() ,


    def P8_Serial(self):
        try:
            portx = Serial_num
            bps = 115200
            timex = None
            self.ser = serial.Serial(portx, bps, timeout=timex)
            print('P8串口:----链接串口成功')
            while True:
                if self.ser.in_waiting:
                    c5 = self.ser.readline().decode(encoding='UTF-8', errors='ignore')
                    if (c5 == "exit"):  # 退出标志
                        break
                    else:
                        # print(c5)
                        # print('open')
                        with open('P8_频繁RESET按键.log', 'a', encoding='UTF-8', errors='ignore') as log:
                            log.writelines(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' ' + c5)
                        # if 'Ready sd upgrade' in c5:
                        #     print('P8MAX------------------------:进入回退版本流程,' + str(datetime.now()))
                            # break
                        if 'soc-nna version' in c5:
                            print('P8MAX------------------------:,完成重启,' + str(datetime.now()))
                        if 'U-Boot SPL' in c5:
                            print('P8MAX------------------------:重启中,' + str(datetime.now()))
                            # break
            # print('超时退出')
            self.ser.close()  # 关闭串口
        except Exception as e:
            print("---异常---：", e)
            pass

AIC =AIC()
t3 = threading.Thread(target=AIC.P8_Serial)
t3.start()
time.sleep(5)
while True:
    AIC.AN()
