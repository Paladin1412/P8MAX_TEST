# -*- coding: utf-8 -*- 
# @Time : 2022/8/3 19:28 
# @Author : 能飞会打智勇双全的才高八斗 
# @File : 开流测速.py
import os
from numpy import *
import time
import serial #导入模块
import threading
from datetime import datetime
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait #导入显性等待的包
Serial_num = 'COM77'
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
    # 'udid':"1977957e",
    "waitForIdleTimeout": 1 # 优化速度
}

camera_redmi_10_360 = { #安心家庭
    "platformName": "Android",  # 测试手机为安卓
    "platformVersion": "10",    # 手机安卓版本
    "deviceName": "AKC0218901000350",  # 设备名称.  安卓手机可以留空
    "appPackage": "com.qihoo.camera",  # 启动app的名称,adb shell dumpsys activity recents | find "intent={"      查看app名称 cmp=后面的 /前面的
    "appActivity": "com.qihoo.jia.ui.activity.SplashActivity",  # 启动 appActivity名称activity是cmp斜杠后面的
    "automationName": "UiAutomator2",  #
    "newCommandTimeout": "1800",  # 连接超时
    "noReset": True,   # 不要重置app
    "resetKeyboard": True,   # 执行完程序恢复原来的输入法
    "unicodeKeyboard": True,  # 使用自带输入法 输入中文时填True
    # 'udid':"1977957e",
    "waitForIdleTimeout": 1 # 优化速度
}
HS_time = []
class openflow():
    def __init__(self):
        self.driver = None  # 让类里面的每个方法都能调用
        self.ser = None
    def Open_UP(self):
        try:
            self.driver = webdriver.Remote('http://localhost:4723/wd/hub', camera_redmi_10)
        except:
            return self.Open_UP()
    def open_1(self):  # 点击实时画面
        try:
            WebDriverWait(self.driver, 15, 3).until(
                lambda el1: self.driver.find_element(By.XPATH, '//android.view.View[@content-desc="360摄像机P8Max"]'))
            self.driver.find_element(By.XPATH, '//android.view.View[@content-desc="360摄像机P8Max"]').click()
            t1 = time.time()
            video_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
            try:
                WebDriverWait(self.driver, 10, 0.1).until(
                    lambda el1: self.driver.find_element(By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View[2]/android.view.View/android.view.View[4]/android.view.View/android.view.View/android.view.View[3]'))
                time_HS = (time.time() - t1)
                HS_time.append(time_HS)
                New_time =datetime.now()
                print(f'开始时间{New_time},本次APP开流耗时:{time_HS}s,平均开流耗时:{mean(HS_time)}s,最短耗时{min(HS_time)},10s内最长耗时:{max(HS_time)}')
                time.sleep(10)
                self.driver.back()
                time.sleep(5)
            except:
                self.driver.back()
                self.driver.back()
                print(f'{video_time}超过10S,未开流')
                # self.Copy_Applog() # # 导出视频文件来
        except:
            print('app崩溃,拉起')
            self.Open_UP()
            self.open_1()

    def Open_UP360(self):
        try:
            self.driver = webdriver.Remote('http://localhost:4723/wd/hub', camera_redmi_10_360)
        except:
            return  self.Open_UP360()

    def Open_360(self):
        try:
            WebDriverWait(self.driver, 15, 3).until(
                lambda el1: self.driver.find_element(By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/androidx.viewpager.widget.ViewPager/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[3]/android.view.ViewGroup/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.ImageButton'))
            self.driver.find_element(By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/androidx.viewpager.widget.ViewPager/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[3]/android.view.ViewGroup/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.ImageButton').click()
            t1 = time.time()
            video_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
            try:
                WebDriverWait(self.driver, 10, 0.1).until(
                    lambda el1: self.driver.find_element(By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[2]/android.widget.RelativeLayout/android.widget.FrameLayout[1]/android.widget.RelativeLayout[4]/android.widget.LinearLayout/android.widget.ImageView'))
                time_HS = (time.time() - t1)
                HS_time.append(time_HS)
                print(f'本次APP开流耗时:{time_HS}s,平均开流耗时:{mean(HS_time)}s,最短耗时{min(HS_time)},10s内最长耗时:{max(HS_time)}')
                time.sleep(5)
                self.driver.back()
                time.sleep(5)
            except:
                self.driver.back()
                self.driver.back()
                print(f'{video_time}超过5S,未开流')
                self.Copy_Applog() # # 导出视频文件来
        except:
            print('app崩溃,拉起')
            self.Open_UP360()
            self.Open_360()
    def Copy_Applog(self):
        try:
            print('正在进行拷贝app日志')
            os.system(f"adb -s 1977957e pull /sdcard/Android/data/com.qihoo.smart/cache/ ./openflow_log/{i}")  # 拷贝指定手机指定目录 到 pc指定目录 安心家庭
            # os.system(f"adb -s 1977957e pull /sdcard/Android/data/com.qihoo.camera/ ./openflow_log/{i}")  # 360摄像机
            print('App日志拷贝成功')
        except:
            print('App日志拷贝失败')
            pass

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
                        with open('P8_开流_log_标清.log', 'a', encoding='UTF-8', errors='ignore') as log:
                            log.writelines(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' ' + c5)
                        if 'CPU: 0 PID' in c5:
                            print(f'OOM:{c5}')
                        # if 'SIL_fcsdbird success' in c5:
                        #     print('P8串口:----声波解析成功!')
                        # if 'wifi_connect_success' in c5:
                        #     print('P8串口:----wifi链接成功')
                        # if 'Connect to cloud' in c5:
                        #     print('P8串口:----长链,链接成功')
                        # if 'DEVICE_OWNER_UNBIND' in c5:
                        #     print('P8串口:----设备解绑成功')
            # print('超时退出')
            self.ser.close()  # 关闭串口
        except Exception as e:
            print("---异常---：", e)
            pass

    def Serial_send(self):
        self.ser.write('\r'.encode("utf-8"))
        time.sleep(0.2)
        self.ser.write('root\r'.encode("utf-8"))
        time.sleep(0.2)
        self.ser.write('iot_ipc@360\r'.encode("utf-8"))
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

aaaa = openflow()
i = 0
t = threading.Thread(target=aaaa.P8_Serial)
t.start()
time.sleep(5)
# 安心家庭
while i<=250:
    i+=1
    print(f'======================第{i}次,=================\r')
    # aaaa.Serial_send()
    time.sleep(5)
    aaaa.open_1()

# 360摄像机
# while True:
#     i+=1
#     print(f'======================第{i}次,=================\r')
#     aaaa.Open_360()
