# -*- coding: utf-8 -*- 
# @Time : 2022/8/17 14:42 
# @Author : 能飞会打智勇双全的才高八斗 
# @File : P8_夜视切换截图.py
import os
import time
from datetime import datetime
from appium import webdriver
from selenium.webdriver.common.by import By
import threading
import serial #导入模块
from selenium.webdriver.support.wait import WebDriverWait #导入显性等待的包
import time
import requests
from datetime import datetime
Serial_num = 'COM11'
Serial__POWER_num = 'COM33'
camera_redmi_10 = { #安心家庭
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


class yi_giao_wu_li_giao_giao():
    def __init__(self):
        self.driver = None  # 让类里面的每个方法都能调用
        self.ser = None
        self.ser1 = None
        self.url = 'https://iot.zyun.360.cn/iot/api/common/device/setProperty'
        self.P8_cookie = '__huid=11vFyP6NQw3FKByy0lAW+6X+J0eI7KE5mlwGcdDdmaoHY=; bad_id73963b90-5cf1-11e9-9a78-b1dd2463a67d=adc4dee2-0409-11ec-b729-6987cce1077a; __gid=210553756.110165219.1629720015257.1639621893533.11; __guid=192758817.4361071964550641700.1655103420048.7302; Qs_lvt_369019=1658801133%2C1658892453%2C1659492684%2C1660706582%2C1660806369; online_ticket=OT-4ce15ddd-6f91-4b84-bd54-aa87cffb5e2d; Qs_pv_369019=4222360418775880700%2C1564559482436133600%2C4148260640837654000%2C3732652553618712600%2C4216067718312037000; Q=u%3D360H3293566442%26n%3D%26le%3D%26m%3DZGtjWGWOWGWOWGWOWGWOWGWOAwL0%26qid%3D3293566442%26im%3D1_t01a6d072182d68691c%26src%3D360chrome_weixin%26t%3D1; T=s%3Dbba42a56efe6370247212d6e0e836810%26t%3D1660527054%26lm%3D%26lf%3D%26sk%3D7c927075dbec605f168a35faf8a51322%26mt%3D1660527054%26rc%3D1%26v%3D2.0%26a%3D1; hasShowLiving=1; IOT_MOCK=; __DC_monitor_count=1; __DC_sid=123679891.1673888441840586500.1663032818363.8228; __DC_gid=264109457.602706629.1629184391927.1663032837050.7967'
        self.P8_cookies = {
            'Content-Type': 'application/json',
            'cookie': self.P8_cookie
        }

    def Bai(self):
        P8_body_0 = {
            "corp_id": "212",
            "device_name": "86XCP8M12220000172",
            'items': '{"Nightvision":0}', # 0关 1 开
            'input_data': "{}",
            "product_key": "2b7e7feff233",
            "seasAndInDomain": "inland"
        }

        bb =requests.post(url=self.url, json=P8_body_0, headers=self.P8_cookies).json()  # 白
        print(f'白{bb}')

    def Hei(self):
        P8_body_1 = {
            "corp_id": "212",
            "device_name": "86XCP8M12220000172",
            'items': '{"Nightvision":1}',  # 0关 1 开
            'input_data': "{}",
            "product_key": "2b7e7feff233",
            "seasAndInDomain": "inland"
        }

        bb =requests.post(url=self.url, json=P8_body_1, headers=self.P8_cookies).json()  # hei
        print(f'黑{bb}')

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

    def Open_UP(self):
        try:
            self.driver = webdriver.Remote('http://localhost:4723/wd/hub', camera_redmi_10)
        except:
            return self.Open_UP()

    def open_1(self):  # 点击实时画面
        try:
            WebDriverWait(self.driver, 15, 3).until(
                lambda el1: self.driver.find_element(By.XPATH, '//android.view.View[@content-desc="实时画面"]'))
            self.driver.find_element(By.XPATH, '//android.view.View[@content-desc="实时画面"]').click()
        except:
            self.Open_UP()
            self.open_1()

    def JieTu(self):
        try:
            # time.sleep(10)
            video_time = time.strftime("%Y%m%d%H%M%S", time.localtime())  # %m-%d
            self.driver.get_screenshot_as_file(f'./红屏截图3/{video_time}.png')
            print('App截图成功,保存位置为红屏截图3')
            # time.sleep(1)
        except:
            self.Open_UP(),self.open_1()

    def PD(self):
        try:
            WebDriverWait(self.driver, 6, 1).until(
                lambda el2: self.driver.find_element(By.XPATH, "//*[contains(@content-desc,'卡录像')]"))  # 模糊定位大法
            time.sleep(6)
            self.JieTu()
        except:
            self.Open_UP(),self.open_1(),
            time.sleep(5)
            self.JieTu()

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
                        with open('P8夜视切换log.log', 'a', encoding='UTF-8', errors='ignore') as log:
                            log.writelines(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' ' + c5)
            # print('超时退出')
            self.ser.close()  # 关闭串口
        except Exception as e:
            print("---异常---：", e)
            pass

    def Serial_send(self):
        self.ser.write('\r'.encode("utf-8"))
        time.sleep(0.1)
        self.ser.write('killall tail\r'.encode("utf-8"))
        time.sleep(0.1)
        self.ser.write('\r'.encode("utf-8"))
        time.sleep(0.1)
        self.ser.write('tail -f /mnt/ext/ipcam.log &\r'.encode("utf-8"))
        time.sleep(0.1)
        self.ser.write('\r'.encode("utf-8"))
        print('P8串口:----发送命令成功')


aa = yi_giao_wu_li_giao_giao()
t = threading.Thread(target=aa.P8_Serial)
t.start()
t2 = threading.Thread(target=aa.Power)
t2.start()
i =0

aa.Open_UP()
aa.open_1()
time.sleep(5)
while True:
    i += 1
    print(f'\n==============={i},时间:{datetime.now()}')

    time.sleep(1)
    aa.Power_Off()
    time.sleep(1)
    aa.PD()
    aa.Power_On()
    aa.PD()



