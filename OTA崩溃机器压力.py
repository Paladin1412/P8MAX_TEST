# -*- coding: utf-8 -*- 
# @Time : 2022/2/28 10:11 
# @Author : 能飞会打智勇双全的才高八斗 
# @File : OTA崩溃机器压力.py
# -*- coding: utf-8 -*-
# @Time : 2022/1/12 18:24
# @Author : 能飞会打智勇双全的才高八斗
# @File : R5Max_OTA_Test.py
import os
import sys
import time
import serial #导入模块
from appium import webdriver
from selenium.webdriver.common.by import By
import threading
from selenium.webdriver.support.wait import WebDriverWait #导入显性等待的包


IPC_Serial = 'COM42'
STA_Serial = 'COM35'

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
    'udid':"1977957e"
    # 'udid':"AKC0218901000350"
}
sta_oom = []
ipc_oom = []
ipc_upgrade_error = []
ipc_upgrade_fail = []
do_upgrade = []
download_ipc = []
download_curl = []
End_send_file = []
upgrading_system = []
ApCli0_Connected = []
Please_choose_the_operation = []
safeupgrade_up = []
AT_REBOOT = []
online_timeout = []


class All_huawei_p20_pro():
    def Tail_f_iscm(self):
        try:
            portx = STA_Serial
            bps = 115200
            timex = None
            ser = serial.Serial(portx, bps, timeout=timex)
            # print("衔接串口成功:详情参数：", ser)
            ser.write('\r'.encode("utf-8"))
            ser.write('killall tail\r'.encode("utf-8"))
            ser.write('\r'.encode("utf-8"))
            ser.write('tail -f /var/log/iscm.log &\r'.encode("utf-8"))
            ser.write('\r'.encode("utf-8"))
            ser.write('tail -f /var/log/iscm_iot.log &\r'.encode("utf-8"))
            ser.write('\r'.encode("utf-8"))
            ser.write('tail -f /var/log/libqtrans.log &\r'.encode("utf-8"))
            print('STA----:开启iscm,iot,libqtrans日志')
            ser.close()  # 关闭串口
        except Exception as e:
            print("---异常---：", e)
            self.Tail_f_iscm()

    def Open_UP(self):
        try:
            driver = webdriver.Remote('http://localhost:4723/wd/hub', camera_huawei_p20_pro)
            print('APP----:开启应用')
            time.sleep(6)
            driver.tap([(0, 81), (132, 213)])  # 点空白处,防止蹦应用 这里总弹出
            time.sleep(0.0001)
            WebDriverWait(driver, 30, 0.5).until(lambda el1: driver.find_element(By.XPATH, "//*[@content-desc='设置']"))
            # 在30s内，每隔0.5s检查一次所需要的元素是否被加载出来，加载出来了就执行下一步，没有加载出来就继续等待，
            driver.find_element(By.XPATH, "//*[@content-desc='设置']").click()  # 执行找到的元素
            self.swipeUp(driver)
            time.sleep(3)
            # driver.tap([(0, 1225), (1080, 1384)]) #华为
            driver.tap([(0,1450),(1080,1601)]) # 红米
            WebDriverWait(driver, 30, 0.5).until(lambda el2: driver.find_element(By.XPATH, "//*[@content-desc='马上升级']"))
            print('APP----:点击升级'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            # 在30s内，每隔0.5s检查一次所需要的元素是否被加载出来，加载出来了就执行下一步，没有加载出来就继续等待，
            driver.find_element(By.XPATH, "//*[@content-desc='马上升级']").click()  # 执行找到的元素
            # time.sleep(900)
        except Exception as e:
            # main_time.clear()
            # print("---异常---：", e)
            print("APP----:app崩了 再次启动 10内再次重启")
            time.sleep(3)
            return self.Open_UP()

    def swipeUp(self,driver, t=500, n=1):
        '''向上滑动屏幕'''
        l = driver.get_window_size()
        x1 = l['width'] * 0.5 # x坐标
        y1 = l['height'] * 0.85 # 起始y坐标
        y2 = l['height'] * 0.15 # 终点y坐标
        for i in range(n):
            driver.swipe(x1, y1, x1, y2, t)
        # print('往下划')

    # 基站
    def Com_STA(self):
        try:
            print('STA----:串口链接成功')
            portx = STA_Serial
            bps = 115200
            timex = None
            ser = serial.Serial(portx, bps, timeout=timex)
            # print('查看')
            while True:
                if ser.in_waiting:
                    # c4 = ser.in_waiting().decode(encoding='UTF-8',errors='ignore')
                    c4 = ser.readline().decode(encoding='UTF-8',errors='ignore')
                    #errors="ignore") 忽略其中有异常的编码，仅显示有效的编码,errors="replace") 替换其中异常的编码，这个相对来可能一眼就知道那些字符编码出问题了。
                    if 'Please choose the operation: ' == c4:  # 退出标志
                        print('升级完成重启中')
                        break
                    # elif 'Out of memory' in c4:
                    #     print('STA,oom了,保留现场,退出程序')
                    #     sys.exit()
                    else:
                        # print(c4)
                        with open('STA_UPlog_分区.txt', 'a') as log:
                            log.writelines(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+' '+c4)
                        if ' do_upgrade start' in c4:
                            do_upgrade.append('do_upgrade start')
                            print('STA----:基站升级开始'+str(len(do_upgrade)))
                        elif 'Out of memory' in c4:
                            sta_oom.append('Out of memory')
                            print('STA------------------------:STA,oom了,保留现场,退出程序'+str(len(sta_oom)))
                            # sys.exit()
                        elif 'Notify ipc upgrade error' in c4:
                            ipc_upgrade_error.append('Notify ipc upgrade error')
                            print('STA----:ipc传输失败了'+str(len(ipc_upgrade_error))+time.strftime("%Y-%m-%d %H:%M:%S"))
                            # sys.exit()
                            # sys.exit()
                        elif 'ipc upgrade fail, donot upgrade station!' in c4:
                            ipc_upgrade_fail.append('ipc upgrade fail, donot upgrade station!')
                            print('ipc upgrade fail, donot upgrade station!'+str(len(ipc_upgrade_fail))+time.strftime("%Y-%m-%d %H:%M:%S"))
                            break
                            # sys.exit()
                        elif ' download_ipc_firmware leave' in c4:
                            download_ipc.append('download_ipc_firmware leave')
                            print('STA----:下载IPC固件完成'+str(len(download_ipc)))
                        elif ' download_curl leave' in c4:
                            download_curl.append(' download_curl leave')
                            print('STA----:下载STA固件包完成'+str(len(download_curl)))
                        elif 'End send file' in c4:
                            End_send_file.append('End send file')
                            print('STA----:STA向IPC发送固件包完成'+str(len(End_send_file)))
                        elif 'Somebody is upgrading system ..' in c4:
                            upgrading_system.append('Somebody is upgrading system ..')
                            print('STA----:正在升级STA固件'+str(len(upgrading_system)))
                        # elif '[wifi.doorbell.connect]' or ' [Hbeat]accpet conn:' or ' [Hbeat]sta MAC ' in c4:
                        #     print('门铃链接基站成功')
                        elif ' ApCli0 Connected AP : ' in c4:
                            ApCli0_Connected.append(' ApCli0 Connected AP : ')
                            print('STA----:升级完成路由链接成功'+str(len(ApCli0_Connected)))
                            break
                        if 'Please choose the operation: ' in c4:  # 退出标志
                            Please_choose_the_operation.append('Please choose the operation: ')
                            print('STA----:升级完成重启中'+str(len(Please_choose_the_operation)))
                        if 'waiting doorbell online timeout' in c4:  # 退出标志
                            online_timeout.append('waiting doorbell online timeout')
                            print('STA----:等待门铃上线超时'+str(len(online_timeout)))
            ser.close()  # 关闭串口
        except Exception as e:
            print("---异常---：", e)
            pass

    def Com_T40(self):
        try:
            portx = IPC_Serial
            bps = 115200
            timex = None
            ser = serial.Serial(portx, bps, timeout=timex)
            print('IPC----:串口链接成功')
            while True:
                if ser.in_waiting:
                    c5 = ser.readline().decode(encoding='gbk',errors='ignore')
                    if(c5=="exit"):#退出标志
                        break
                    else:
                        with open('T40_UPlog分区.txt', 'a') as log:
                            log.writelines(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+' '+c5)
                        if 'safeupgrade up' in c5:
                            safeupgrade_up.append('safeupgrade up')
                            print('IPC----:门铃收到升级,'+str(len(safeupgrade_up)))
                        if 'Out of memory' in c5:
                            ipc_oom.append('Out of memory')
                            print('IPC--------------------:IPC,oom了,退出程序,保留现场'+str(len(ipc_oom)))
                            # sys.exit()
                        # if (' upgrade appfs0' or 'upgrade appfs1' or 'upgrade kernel1' or ' upgrade atbm') in c5:
                        #     print('IPC----:IPC,开始升级')
                        if ' AT+REBOOT' in c5:
                            AT_REBOOT.append(' AT+REBOOT')
                            print('IPC----:升级完成执行重启'+str(len(AT_REBOOT)))
                            break
            ser.close()  # 关闭串口

        except Exception as e:
            print("---异常---：", e)
            pass

    def XC(self):
        # t1 = threading.Thread(target=self.Open_UP)
        t2 = threading.Thread(target=self.Com_STA)
        t3 = threading.Thread(target=self.Com_T40)
        # t1.start()
        t2.start()
        t3.start()

bb = All_huawei_p20_pro()

def Kais():
    i = 0
    try:
        while True:
            time.sleep(5)
            i += 1
            print('\n================='+str(i)+'=================')
            bb.Tail_f_iscm()
            time.sleep(5)
            bb.XC()
            bb.Open_UP()
            time.sleep(620)
            print('=====================================\n')
    except:
        return Kais()

Kais()