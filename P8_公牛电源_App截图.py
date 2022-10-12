# -*- coding: utf-8 -*- 
# @Time : 2022/9/6 17:16 
# @Author : 能飞会打智勇双全的才高八斗 
# @File : P8_公牛电源_App截图.py
import time
import serial #导入模块
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait #导入显性等待的包
import threading
import serial #导入模块
import time
from datetime import datetime

Serial_num = 'COM11'
Serial__POWER_num = 'COM33'


Anxin_10 = { #安心家庭
    "platformName": "Android",  # 测试手机为安卓
    "platformVersion": "10",    # 手机安卓版本
    "deviceName": "AKC0218901000350",  # 设备名称.  安卓手机可以留空
    "appPackage": "com.qihoo.smart",  # 启动app的名称,adb shell dumpsys activity recents | find "intent={"      查看app名称 cmp=后面的 /前面的
    "appActivity": "com.qihoo.main.activity.SHSplashActivity",  # 启动 appActivity名称activity是cmp斜杠后面的
    "automationName": "UiAutomator2",  #
    "newCommandTimeout": "1800",  # 连接超时
    "noReset": True,   # 不要重置app
    "resetKeyboard": True,   # 执行完程序恢复原来的输入法
    "unicodeKeyboard": True,  # 使用自带输入法 输入中文时填True
    'udid':"8a455578",
    "waitForIdleTimeout": 1 # 优化速度
}
class AIC():
    def __init__(self):
        self.driver = None
        self.driver1=None
        self.ser = None
        self.ser1 = None

    def Power(self):
        portx = Serial__POWER_num
        bps = 9600
        timex = None
        self.ser1 = serial.Serial(portx, bps, timeout=timex)
        # ser.write('\r'.encode("utf-8"))
        # ser.write(bytes.fromhex('AE 20 01 28 02 01 01 AC'))  # 16进制 1路开.
        # ser.write(bytes.fromhex('AE 20 01 28 02 01 00 AC'))  # 16进制 1路关.
        self.ser1.write(bytes.fromhex('AE 20 01 29 03 FF FF 00 AC'))  # 16进制 总开关 全开.
        print(f'Power------串口链接成功,{str(datetime.now())}')
        # self.ser1.write(bytes.fromhex('AE 20 01 29 03 FF 00 00 AC'))  # 16进制 总开关 全关.

    def Power_On(self):
        self.ser1.write(bytes.fromhex('AE 20 01 28 02 01 01 AC'))  # 16进制 1路开.
        print(f'Power------1闸开启,{str(datetime.now())}')
    def Power_Off(self):
        self.ser1.write(bytes.fromhex('AE 20 01 28 02 01 00 AC'))  # 16进制 1路关
        print(f'Power------1闸关闭,{str(datetime.now())}')


    def Open_UPapp(self):
        try:
            self.driver = webdriver.Remote('http://localhost:4723/wd/hub', Anxin_10)
        except:
            return self.Open_UPapp()

    def open_1(self):  # 点击实时画面
        try:
            WebDriverWait(self.driver, 15, 3).until(
                lambda el1: self.driver.find_element(By.XPATH, '//android.view.View[@content-desc="实时画面"]'))
            self.driver.find_element(By.XPATH, '//android.view.View[@content-desc="实时画面"]').click()
        except:
            self.Open_UPapp()
            self.open_1()

    def JieTu(self):
        try:
            # time.sleep(10)
            video_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())  # %m-%d
            self.driver.get_screenshot_as_file(f'./红屏截图/login{video_time}.png')
            print('App截图成功,保存位置为红屏截图')
            time.sleep(1)
        except:
            self.Open_UPapp(), self.open_1()

    def PD(self):
        try:
            WebDriverWait(self.driver, 10, 1).until(
                lambda el2: self.driver.find_element(By.XPATH, "//*[contains(@content-desc,'卡录像')]"))  # 模糊定位大法
            time.sleep(20)
            self.JieTu()
        except:
            print('没有找到安心家庭的卡录图标,重启app')
            return self.open_1(),self.PD()

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
                        with open('P8_ircut.log', 'a', encoding='UTF-8', errors='ignore') as log:
                            log.writelines(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' ' + c5)
                        if 'Out of memory' in c5:
                            print(f'P8固件:------崩溃OOM,{str(datetime.now())}')
                            # self.Serial_send()
                        if 'RUN SDIO' in c5:
                            print(f'P8固件:------重启了!,{str(datetime.now())}')
                            self.Serial_send()
                        if 'CPU: 0 PID' in c5:
                            print(f'P8固件:------可能异常崩溃OOM了,{str(datetime.now())}')
            self.ser.close()  # 关闭串口
        except Exception as e:
            print("---异常---：", e)
            pass
    def Serial_send(self):
        # print('开启日志')
        time.sleep(60)
        self.ser.write("\r".encode("utf-8"))
        self.ser.write("\r".encode("utf-8"))
        time.sleep(0.1)
        self.ser.write('root'.encode("utf-8"))
        time.sleep(0.1)
        self.ser.write("\r".encode("utf-8"))
        time.sleep(0.1)
        self.ser.write('iot_ipc@360'.encode("utf-8"))
        time.sleep(0.1)
        self.ser.write("\r".encode("utf-8"))
        self.ser.write("\r".encode("utf-8"))
        time.sleep(0.1)
        self.ser.write('iot_ipc@360'.encode("utf-8"))
        time.sleep(0.1)
        self.ser.write("\r".encode("utf-8"))
        time.sleep(5)
        self.ser.write('watchdog &\r'.encode("utf-8"))
        time.sleep(0.1)
        self.ser.write("\r".encode("utf-8"))
aa = AIC()
i = 0
t1 = threading.Thread(target=aa.P8_Serial)
t1.start()
t2 = threading.Thread(target=AIC.Power)
t2.start()
time.sleep(5)

def start():
    i = 0
    while True:
        i+=1
        print(f'\n===================={i}=================,{datetime.now()}')
        aa.Power_Off()
        aa.PD()
        time.sleep(5)
start()