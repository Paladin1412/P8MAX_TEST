# -*- coding: utf-8 -*-
# @Time : 2022/1/12 18:24
# @Author : 能飞会打智勇双全的才高八斗
# @File : R5Max_OTA_Test.py
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


# 串口波特率
STA_Serial = 'COM11'
# 旧版本门铃文件改名为 :ipc_firmware.bin
# 基站新老版本  移动基站版本名称  注意基站的版本下划线_和-
STA_old_VERSION = 'P8MAX_V1.1.12.8_20221005_191802_upgrade.bin'
New_VERSION = 'V1.1.13.0_20221008'

# 门铃老版本(SD卡内置的固件版本号)
Old_VERSION = 'V1.1.12.8_20221005'



click_ota = []  # 点击升级时间
ipc_oom = []
ipc_upgrade_error = []
ipc_upgrade_fail = []
online_timeout = []
dDownload_ipc_upgrade_error = []
click_ota_list = []

#手机参数
camera_huawei_p20_pro = { #安心家庭
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
    # adb devices
    # 'udid':"1977957e"
    # 'udid':"AKC0218901000350"
    "waitForIdleTimeout":1,
    'udid':"8a455578"
}

class All_huawei_p20_pro():
    def __init__(self):
        self.driver =None
        self.ser = None

    # 回退IPC版本方法.
    def Com_IPC_rollback(self):
        try:
            portx = STA_Serial
            bps = 115200
            timex = None
            ser = serial.Serial(portx, bps, timeout=timex)
            print('P8MAX------------------------:串口链接成功,开始回退P8版本,'+str(datetime.now()))
            ser.write('\r'.encode("utf-8"))
            time.sleep(2)
            ser.write('root\r'.encode("utf-8"))  # 账号.
            time.sleep(0.2)
            ser.write('iot_ipc@360\r'.encode("utf-8"))  # 密码.
            ser.write('\r'.encode("utf-8"))
            time.sleep(2)
            ser.write('\r'.encode("utf-8"))
            time.sleep(2)
            ser.write(f'sd_upgrade.sh /mnt/sd/{STA_old_VERSION}\r'.encode("utf-8"))  #
            ser.write('\r'.encode("utf-8"))

            t2 = datetime.now()
            while (datetime.now() - t2).seconds <= 300:
                if ser.in_waiting:
                    c5 = ser.readline().decode(encoding='gbk',errors='ignore')
                    if(c5=="exit"):#退出标志
                        break
                    else:
                        with open('P8_UPlog.txt', 'a',encoding='gbk',errors='ignore') as log:
                            log.writelines(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+' '+c5)
                        # print(c5)
                        if 'Ready sd upgrade' in c5:
                            print('P8MAX------------------------:进入回退版本流程,'+str(datetime.now()))
                            # break
                        if 'soc-nna version' in c5:
                            print('P8MAX------------------------:回退完成,完成重启,' + str(datetime.now()))
                            break
                        if 'U-Boot SPL' in c5:
                            print('P8MAX------------------------:回退完成,重启中,' + str(datetime.now()))
                            # break
        except:
            pass

    # 回退IPC版本,校验回退是否成功.如果不成功.再次返回重新回退
    def Cat_IPC_version(self):
        portx = STA_Serial
        bps = 115200
        timex = None
        ser = serial.Serial(portx, bps, timeout=timex)
        # print('STA----:串口链接成功,开始查看IPC回退版本')
        ser.write('\r'.encode("utf-8"))
        time.sleep(2)
        ser.write('root\r'.encode("utf-8"))  # 账号.
        time.sleep(0.2)
        ser.write('iot_ipc@360\r'.encode("utf-8"))  # 密码.
        ser.write('\r'.encode("utf-8"))
        time.sleep(2)
        ser.write('\r'.encode("utf-8"))
        time.sleep(2)
        ser.write('cat app/etc/version.ini\r'.encode("utf-8"))  #
        ser.write('\r'.encode("utf-8"))
        t2 = datetime.now()
        while (datetime.now() - t2).seconds <= 60:
            if ser.in_waiting:
                c5 = ser.readline().decode(encoding='gbk', errors='ignore')
                if (c5 == "exit"):  # 退出标志
                    break
                else:
                    with open('P8_UPlog.txt', 'a', encoding='gbk', errors='ignore') as log:
                        log.writelines(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' ' + c5)
                    # print(c5)
                    if Old_VERSION in c5:
                        # print(c5)
                        print('P8MAX------------------------:版本回退成功,进行下一步,'+str(datetime.now()))
                        break

                    if New_VERSION in c5:
                        print('P8MAX------------------------:IPC版本回退失败.重新回退,'+str(datetime.now()))
                        ser.close()  # 关闭串口
                        return self.Com_IPC_rollback() , self.Cat_IPC_version()



    # APP进入升级界面流程
    def APP_Set_up_the(self):
        try:
            self.driver = webdriver.Remote('http://localhost:4723/wd/hub', camera_huawei_p20_pro)
            # print('APP----:开启应用')
            time.sleep(6)
            self.Pass_All()
            self.driver.tap([(0, 81), (132, 213)])  # 点空白处,防止蹦应用 这里总弹出
            time.sleep(0.0001)
            WebDriverWait(self.driver, 30, 1).until(lambda el1: self.driver.find_element(By.XPATH, "//*[@content-desc='设置']")) # 搜索设置
            # 在30s内，每隔0.5s检查一次所需要的元素是否被加载出来，加载出来了就执行下一步，没有加载出来就继续等待，
            self.driver.find_element(By.XPATH, "//*[@content-desc='设置']").click()  # 进入设置
            # self.swipeUp(self.driver) # 向下滑动
            time.sleep(2)
            self.swipe_down_up()
            time.sleep(5)
            WebDriverWait(self.driver, 10, 1).until(
                lambda el2: self.driver.find_element(By.XPATH, "//*[contains(@content-desc,'固件升级')]"))  # 模糊定位大法
            self.driver.find_element(By.XPATH, "//*[contains(@content-desc,'固件升级')]").click()
        except Exception as e:
            # print("APP----:app崩了 再次启动 10内再次重启")
            time.sleep(10)
            return self.APP_Set_up_the()

    # 向下滑动屏幕
    def swipe_down_up(self, start_y=1, stop_y=0.01, duration=2000):  # 如果start_y=0.75, stop_y=0.25，则向上滑动屏幕
        # 按下手机屏幕，向下滑动
        # 注意，向下滑时，x轴不变，要不然就变成了斜向下滑动了
        # @duration：持续时间
        x = self.driver.get_window_size()["width"]  # 获取屏幕的宽
        y = self.driver.get_window_size()["height"]
        x1 = int(x * 0.5)
        y1 = int(y * start_y)
        x2 = int(x * 0.5)
        y2 = int(y * stop_y)
        self.driver.swipe(x1, y1, x2, y2, duration)

    # APP点击升级
    def APP_click(self):
        try:
            time.sleep(10)
            WebDriverWait(self.driver, 30, 1).until(lambda el2: self.driver.find_element(By.XPATH, "//*[@content-desc='马上升级']"))  # 找到马上升级
            # 在30s内，每隔0.5s检查一次所需要的元素是否被加载出来，加载出来了就执行下一步，没有加载出来就继续等待，
            self.driver.find_element(By.XPATH, "//*[@content-desc='马上升级']").click()  # 执行找到的元素
            click_ota1 = datetime.now()
            click_ota.append(click_ota1)
            print(f'APP------------------------:点击升级,{str(click_ota1)}')
        except:
            return self.APP_Set_up_the() ,  self.APP_click()

    # 校验APP升级是否成功
    def APP_UPSTA_IPC_process(self):
        try:
            try:
                # 升级文字不在了. 执行查找下一个元素.
                WebDriverWait(self.driver, 180, 10).until_not(lambda el2: self.driver.find_element(By.XPATH,'//android.view.View[@content-desc="升级需要几分钟时间 不要断开设备电源及网络，直到升级结束"]'))
                WebDriverWait(self.driver, 15, 5).until(lambda el2: self.driver.find_element(By.XPATH,f"//*[@content-desc='检测到新版本']"))# 如果找到此版本升级成功,否则失败
                ota_fail = time.strftime("%Y-%m-%d %H_%M_%S", time.localtime())
                self.driver.get_screenshot_as_file(f'./OTA_fail/login{ota_fail}.png')
                print('APP------------------------:固件版本升级失败,'+ota_fail)
                self.driver.quit()
                # self.ser.close()
                pass
            except:
                WebDriverWait(self.driver, 15, 5).until(lambda el2: self.driver.find_element(By.XPATH,f"//*[@content-desc='{New_VERSION}']"))  # 如果找到此版本升级成功,否则失败
                print('APP------------------------:固件版本升级成功,'+str(datetime.now()))
                # self.ser.close()
                self.driver.quit()
                pass
        except:
                return self.APP_Set_up_the(), self.APP_UPSTA_IPC_process()

    def Pass_All(self):
        # 忽略设备 间隔1s 线程判断
        # while True:
        try:

            # print('Pass_all_fail')
            WebDriverWait(self.driver, 10, 1).until(
                lambda el2: self.driver.find_element(By.ID, 'com.qihoo.smart:id/tv_tips'))
            time.sleep(1)
            self.driver.find_element(By.ID, 'com.qihoo.smart:id/tv_tips').click()
            # break
        except:
            time.sleep(1)
            # print('paas_all')
            pass

    # 基站
    def Com_STA(self):
        try:
            # print('STA----:串口链接成功')
            portx = STA_Serial
            bps = 115200
            timex = None
            self.ser = serial.Serial(portx, bps, timeout=timex)
            self.ser.write('\r'.encode("utf-8"))
            self.ser.write('killall tail\r'.encode("utf-8"))
            time.sleep(0.1)
            self.ser.write('\r'.encode("utf-8"))
            time.sleep(0.1)
            self.ser.write('tail -f /tmp/log/ipcam.log &\r'.encode("utf-8"))
            time.sleep(0.1)
            self.ser.write('\r'.encode("utf-8"))
            print('P8MAX------------------------:开启ipcam日志,'+str(datetime.now()))
            # print('查看')
            # while True:
            t1 = datetime.now()
            while (datetime.now() - t1).seconds <= 300:
                if self.ser.in_waiting:
                    c4 = self.ser.readline().decode(encoding='UTF-8',errors='ignore')
                    #errors="ignore") 忽略其中有异常的编码，仅显示有效的编码,errors="replace") 替换其中异常的编码，这个相对来可能一眼就知道那些字符编码出问题了。
                    if 'Please choose the operation: ' == c4:  # 退出标志
                        print('升级完成重启中')
                        break
                    else:
                        # print(c4)
                        with open('P8_UPlog.txt', 'a', encoding='UTF-8', errors='ignore') as log:
                            log.writelines(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+' '+c4)
                        if 'qipc_ota_upgrade start,pleas free mem' in c4:
                            print('P8MAX------------------------:设备收到升级指令,'+str(datetime.now()))
                        if 'upgrade start download file' in c4:
                            print('P8MAX------------------------:开始下载固件,' + str(datetime.now()))
                        if 'curl download firmware len'in c4:
                            print('P8MAX------------------------:固件下载完成,' + str(datetime.now()))
                        if 'percent = 100' in c4:
                            print('P8MAX------------------------:进度100,' + str(datetime.now()))
                        if 'over, Ready get upgrade bin' in c4:
                            print('P8MAX------------------------:准备升级,' + str(datetime.now()))
                        if 'upgrade ready over,Wait for upgrade' in c4:
                            print('P8MAX------------------------:开始升级,' + str(datetime.now()))
                        if 'soc-nna version' in c4:
                            print('P8MAX------------------------:升级重启完毕,' + str(datetime.now()))
                            break
            self.ser.close()  # 关闭串口
        except Exception as e:
            pass

    def STA_firmware_version(self):
        portx = STA_Serial
        bps = 115200
        timex = None
        ser = serial.Serial(portx, bps, timeout=timex)
        # print('STA----:串口链接成功,开始校验STA版本是否升级成功')
        ser.write('\r'.encode("utf-8"))
        time.sleep(2)
        ser.write('root\r'.encode("utf-8"))  # 账号.
        time.sleep(0.2)
        ser.write('iot_ipc@360\r'.encode("utf-8"))  # 密码.
        ser.write('\r'.encode("utf-8"))
        time.sleep(2)
        ser.write('\r'.encode("utf-8"))
        time.sleep(2)
        ser.write('cat app/etc/version.ini\r'.encode("utf-8"))  # 删除上一次升级文件.
        ser.write('\r'.encode("utf-8"))
        t2 = datetime.now()
        while (datetime.now() - t2).seconds <= 60:
            if ser.in_waiting:
                c5 = ser.readline().decode(encoding='gbk', errors='ignore')
                if (c5 == "exit"):  # 退出标志
                    break
                else:
                    with open('P8_UPlog.txt', 'a', encoding='gbk', errors='ignore') as log:
                        log.writelines(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' ' + c5)
                    # print(c5)
                    if Old_VERSION in c5:
                        # print(c5)
                        print('P8MAX------------------------:固件版本升级失败')
                        ser.close()
                        break
                    if New_VERSION in c5:
                        print('P8MAX------------------------:固件版本升级成功')
                        ser.close()  # 关闭串口
                        break


bb = All_huawei_p20_pro()

# 搞死循环中的死循环


# 固件版本回退
def The_firmware_back():
    bb.Com_IPC_rollback()
    time.sleep(10)
    bb.Cat_IPC_version()



# STA线程, 在回退升级完毕后, 接入

def Kais():
    i = 0
    try:
        while True:
            i += 1
            print('\n================='+str(i)+'=================')
            The_firmware_back()
            # APP流程线程开始
            bb.APP_Set_up_the()
            # 线程APP点击
            t4 = threading.Thread(target=bb.APP_click)
            t4.start()
            bb.Com_STA()
            # 验证APP展示版本
            bb.APP_UPSTA_IPC_process()
            # 验证cat固件版本
            bb.STA_firmware_version()
            print('=====================================\n')
    except:
        pass
        # 不可能出问题!,所以不递归!
        # return Kais()
Kais()

# t4.start()
# bb.APP_Set_up_the()
# bb.APP_UPSTA_IPC_process()
# bb.GG()
# bb.Cat_IPC_version()
# bb.Cat_STA_version()
# bb.APP_UPIPC_process()
# bb.STA_firmware_version()
# bb.IPC_firmware_version()
