# -*- coding: utf-8 -*- 
# @Time : 2022/10/1 10:47 
# @Author : 能飞会打智勇双全的才高八斗 
# @File : P8MAX_声波配网.py
import os
import threading
import time
import serial #导入模块
from datetime import datetime
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait #导入显性等待的包
Serial_num = 'COM36'

camera_Redmi10 = {  # 安心家庭
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
    "waitForIdleTimeout":1,
    # adb devices # cmd输入此命令 查看手机编号
    # 'udid':"1977957e"
}

class P8_MAX():
    def __init__(self):
        self.driver = None
        self.ser =None
    def UP_APP(self):
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', camera_Redmi10)
        time.sleep(6)
        # print(self.driver.start_activity("com.qihoo.smart", "ActivityName"))

    def Append_P8MAX(self):
        try:
            print('P8:----进入确认绑定流程!')
            WebDriverWait(self.driver, 15, 1).until(
                lambda el2: self.driver.find_element(By.XPATH, '//android.widget.Button[@content-desc="添加设备"]'))
            # self.driver.find_element(By.XPATH, '//android.widget.Button[@content-desc="添加设备"]').click()
            self.Append_P8_process()
        except:
            try:
                print('P8:----没找到添加.')
                WebDriverWait(self.driver, 15, 1).until(
                    lambda el2: self.driver.find_element(By.XPATH, '//android.view.View[@content-desc="设置"]'))
                print('P8:----但是找到了设置,管他3721先解绑.')
                self.Remove_P8()
                time.sleep(5)
                self.driver.quit()
                return self.UP_APP(),self.Append_P8MAX()
            except:
                print('啥元素都没找到,重新唤醒.反正是在Append_P8MAX这个方法里崩溃')
                return self.UP_APP(),self.Append_P8MAX()
    def Append_P8_process(self):
        # 选择P8设备
        try:
            print('P8:----添加P8设备')
            WebDriverWait(self.driver, 10, 1).until(
                lambda el2: self.driver.find_element(By.XPATH, '//android.widget.Button[@content-desc="添加设备"]'))
            self.driver.find_element(By.XPATH, '//android.widget.Button[@content-desc="添加设备"]').click()
            WebDriverWait(self.driver, 10, 1).until(
                lambda el2: self.driver.find_element(By.XPATH, '//android.widget.ImageView[@content-desc="360摄像机P8Max"]'))
            self.driver.find_element(By.XPATH, '//android.widget.ImageView[@content-desc="360摄像机P8Max"]').click()
            time.sleep(2)
            # 下一步 2 遍
            WebDriverWait(self.driver, 10, 1).until(
                lambda el2: self.driver.find_element(By.XPATH,
                                                     '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View[2]/android.widget.Button'))
            self.driver.find_element(By.XPATH,
                                     '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View[2]/android.widget.Button').click()
            WebDriverWait(self.driver, 10, 1).until(
                lambda el2: self.driver.find_element(By.XPATH,
                                                     '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View[2]/android.widget.Button'))
            self.driver.find_element(By.XPATH,
                                     '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View[2]/android.widget.Button').click()
            # 输入账号密码
            WebDriverWait(self.driver, 15, 1).until(
                lambda el2: self.driver.find_element(By.ID, "com.qihoo.smart:id/et_id"))
            self.driver.find_element(By.ID, "com.qihoo.smart:id/et_id").click()
            self.driver.find_element(By.ID, "com.qihoo.smart:id/et_id").send_keys("666AIC")
            WebDriverWait(self.driver, 15, 1).until(
                lambda el2: self.driver.find_element(By.ID, "com.qihoo.smart:id/et_pw"))
            self.driver.find_element(By.ID, "com.qihoo.smart:id/et_pw").click()
            self.driver.find_element(By.ID, "com.qihoo.smart:id/et_pw").send_keys("66666666")
            self.driver.keyevent(66)  # 回车
            # 发送声波的下一步
            WebDriverWait(self.driver, 15, 1).until(
                lambda el2: self.driver.find_element(By.ID, "com.qihoo.smart:id/btn_next"))
            self.driver.find_element(By.ID, "com.qihoo.smart:id/btn_next").click()

            # 已将手机靠近设备
            WebDriverWait(self.driver, 15, 1).until(
                lambda el2: self.driver.find_element(By.ID, "com.qihoo.smart:id/cb_confirm"))
            self.driver.find_element(By.ID, "com.qihoo.smart:id/cb_confirm").click()
            self.Send_SoundWaves()
        except:
            print(f'P8:----绑定流程崩溃了,重新进入.{datetime.now()}')
            return self.UP_APP(), self.Append_P8_process()

    def Send_SoundWaves(self):
            print(f'P8:----准备发送声波{datetime.now()}')
            # # 发送声波按钮
            WebDriverWait(self.driver, 15, 1).until(
                lambda el2: self.driver.find_element(By.ID, "com.qihoo.smart:id/cdb_send_sound"))
            self.driver.find_element(By.ID, "com.qihoo.smart:id/cdb_send_sound").click()
            time.sleep(15)
            print(f'P8:----发送声波成功,等待绑定{datetime.now()}')
            self.SuccessfulOrFail()

            # WebDriverWait(self.driver, 180, 5).until(
            #     lambda el2: self.driver.find_element(By.ID, "com.qihoo.smart:id/cdb_send_sound"))
            # self.driver.find_element(By.ID, "com.qihoo.smart:id/cdb_send_sound").click()

    def SuccessfulOrFail(self):
        # print(1)
        # 绑定成功
        # com.qihoo.smart:id/ll_device_binding
        #/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout[2]/android.widget.RelativeLayout[2]/android.webkit.WebView/android.webkit.WebView/android.view.View/android.widget.Image
        try:
            # print(2)
            WebDriverWait(self.driver, 190, 5).until(
                lambda el2: self.driver.find_element(By.ID,"com.qihoo.smart:id/tv_use_immediately"))
            print('\n==================================')
            print(f'P8:----绑定成功{datetime.now()}')
            print('==================================\n')

            # WebDriverWait(self.driver, 180, 5).until(
            #     lambda el2: self.driver.find_element(By.ID, "com.qihoo.smart:id/cdb_send_sound"))
            # self.driver.find_element(By.ID, "com.qihoo.smart:id/cdb_send_sound").click()
            time.sleep(3)
            self.driver.back()
            time.sleep(3)
            self.driver.back()
            time.sleep(3)
            self.driver.back()
            time.sleep(3)
        except:
            self.JieTu()
            self.Serial_kill_P8()
            try:
                WebDriverWait(self.driver, 60, 5).until(
                    lambda el2: self.driver.find_element(By.ID, "com.qihoo.smart:id/cdb_retry"))
                print(f'P8:----绑定失败{datetime.now()}')
            except:
                self.Serial_kill_P8()
                print('真失败')

    def JieTu(self):
        try:
            # time.sleep(10)
            video_time = time.strftime("%Y%m%d%H%M%S", time.localtime())  # %m-%d
            self.driver.get_screenshot_as_file(f'./配网失败/{video_time}.png')
            print('配网截图成功,保存位置为配网失败')
            # time.sleep(1)
        except:pass

        # 超时失败   再试一次按钮com.qihoo.smart:id/cdb_retry
        # 绑定成功的 开始使用  com.qihoo.smart:id/tv_use_immediately  成功后,可三次退出.
        # 绑定成功开始使用的 下一步  	//android.widget.Button[@content-desc="下一步"]  	//android.widget.Button[@content-desc="开始体验"]
        # AP绑定弹出的设备	com.qihoo.smart:id/btn_device_connect_wifi 为设备联网      弹出上面的标签名字com.qihoo.smart:id/tv_fc_module_only_device_name

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
    def Remove_P8(self):
        try:
            WebDriverWait(self.driver, 15, 1).until(
                lambda el2: self.driver.find_element(By.XPATH, '//android.view.View[@content-desc="设置"]'))
            self.driver.find_element(By.XPATH, '//android.view.View[@content-desc="设置"]').click()
            time.sleep(5)
            self.swipe_down_up()
            time.sleep(5)
            # 删除设备
            WebDriverWait(self.driver, 15, 1).until(
                lambda el2: self.driver.find_element(By.XPATH, '//android.view.View[@content-desc="删除设备"]'))
            self.driver.find_element(By.XPATH, '//android.view.View[@content-desc="删除设备"]').click()
            # 确认删除
            WebDriverWait(self.driver, 15, 1).until(
                lambda el2: self.driver.find_element(By.XPATH, '//android.view.View[@content-desc="删除设备并清除用户信息"]'))
            self.driver.find_element(By.XPATH, '//android.view.View[@content-desc="删除设备并清除用户信息"]').click()
            try:
                WebDriverWait(self.driver, 15, 1).until(
                    lambda el2: self.driver.find_element(By.XPATH, '//android.widget.Button[@content-desc="继续删除"]'))
                self.driver.find_element(By.XPATH, '//android.widget.Button[@content-desc="继续删除"]').click()
                # print(f'P8:----解绑成功{datetime.now()}')
                # time.sleep(10)
                # self.driver.quit()
                print(f'P8:----解绑成功{datetime.now()}')
                time.sleep(5)
                self.driver.quit()
            except:
                print(f'P8:----解绑成功{datetime.now()}')
                pass
        except:
            try:
                WebDriverWait(self.driver, 15, 1).until(
                    lambda el2: self.driver.find_element(By.XPATH, '//android.widget.Button[@content-desc="添加设备"]'))
                print(111111222)
                pass
            except:
                print(3333333)
                self.UP_APP(), self.Remove_P8()



    def Pass_All(self):
        # 忽略设备 间隔1s 线程判断
        while True:
            try:

                # print('Pass_all_fail')
                # WebDriverWait(self.driver, 5, 1).until(
                #     lambda el2: self.driver.find_element(By.ID, 'com.qihoo.smart:id/tv_tips'))
                time.sleep(1)
                self.driver.find_element(By.ID, 'com.qihoo.smart:id/tv_tips').click()
                # break
            except:
                time.sleep(1)
                # print('paas_all')
                pass


    def P8_num(self):
        try:
            self.Append_P8_process()
            self.SuccessfulOrFail()
        except:return self.UP_APP(), self.Append_P8MAX(),self.P8_num()

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
                        with open('P8_声波配网日志.log', 'a', encoding='UTF-8', errors='ignore') as log:
                            log.writelines(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' ' + c5)
                        if 'CPU: 0 PID' in c5:
                            print(f'OOM:{c5}')
                        if 'SIL_fcsdbird success' in c5:
                            print('P8串口:----声波解析成功!')
                        if 'wifi_connect_success' in c5:
                            print('P8串口:----wifi链接成功')
                        if 'Connect to cloud' in c5:
                            print('P8串口:----长链,链接成功')
                        if 'DEVICE_OWNER_UNBIND' in c5:
                            print('P8串口:----设备解绑成功')
            # print('超时退出')
            self.ser.close()  # 关闭串口
        except Exception as e:
            print("---异常---：", e)
            pass

    def Serial_send(self):
        self.ser.write('\r'.encode("utf-8"))
        time.sleep(0.1)
        self.ser.write('root\r'.encode("utf-8"))
        time.sleep(0.1)
        self.ser.write('iot_ipc@360\r'.encode("utf-8"))
        time.sleep(0.1)
        # self.ser.write('iot_ipc@360\r'.encode("utf-8"))
        self.ser.write('\r'.encode("utf-8"))
        time.sleep(0.1)
        self.ser.write('killall tail\r'.encode("utf-8"))
        time.sleep(0.1)
        self.ser.write('\r'.encode("utf-8"))
        time.sleep(0.1)
        self.ser.write('tail -f /tmp/log/ipcam.log &\r'.encode("utf-8"))
        time.sleep(0.1)
        self.ser.write('\r'.encode("utf-8"))
        print('P8串口:----发送命令成功')

    def Serial_kill_P8(self):
        self.ser.write('\r'.encode("utf-8"))
        time.sleep(0.1)
        self.ser.write('root\r'.encode("utf-8"))
        time.sleep(0.1)
        self.ser.write('iot_ipc@360\r'.encode("utf-8"))
        time.sleep(0.1)
        # self.ser.write('iot_ipc@360\r'.encode("utf-8"))
        self.ser.write('\r'.encode("utf-8"))
        time.sleep(0.1)
        self.ser.write('rm /config/network.ini\r'.encode("utf-8"))
        time.sleep(0.1)
        self.ser.write('\r'.encode("utf-8"))
        time.sleep(0.1)
        self.ser.write('killall ipcam\r'.encode("utf-8"))
        time.sleep(0.1)
        self.ser.write('\r'.encode("utf-8"))
        print('P8串口:----发送清除配网成功')



    # 释放driver.quit()
AIC = P8_MAX()
t2 = threading.Thread(target=AIC.P8_Serial)
t2.start()
i = 0
while True:
    AIC.UP_APP()
    t = threading.Thread(target=AIC.Pass_All)
    t.start()
    time.sleep(5)
    i += 1
    print(f'\n===================={i}=================,{datetime.now()}')
    AIC.Serial_send()
    time.sleep(5)
    # try:
    AIC.Append_P8MAX()
    time.sleep(30)
    AIC.Serial_kill_P8()
    # AIC.P8_num()
    AIC.Remove_P8()

    time.sleep(10)
    # except:pass

