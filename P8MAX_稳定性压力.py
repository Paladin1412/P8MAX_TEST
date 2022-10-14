# -*- coding: utf-8 -*- 
# @Time : 2022/10/12 19:51 
# @Author : 能飞会打智勇双全的才高八斗 
# @File : P8MAX_稳定性压力.py
import threading
import serial #导入模块
import time
import requests
from datetime import datetime
import inspect
import tkinter.messagebox as msgbox   # 窗口

P8_cookie_A = input('请输入智慧生活网页对应账号的cookie:')
P8_SN =input('请输入设备SN. #必须是测试设备或加白设备:')
Serial_num = input('请输入串口COM号, 例如"COM33":')
P8_timeout = int(input('请输入接口访问,间隔, 反正我是1:'))
print('===================================================================')
print('日志自动保存在当前文件夹下,如出现段错误/重启/oom/我会弹窗提示你的')
print('===================================================================')
# _huid=111sJmTzBhjgifY9mw7YEZOgR8tZSdLDVqRn4o753i0Jo=; __guid=95498437.1213156474748100096.1665298430001.1028; online_ticket=OT-cb99b39c-235a-47ae-b5cf-b366e74ec844; Qs_lvt_369019=1665298430%2C1665370486; Qs_pv_369019=1685368794928168000%2C2737228500947096000%2C2094936792332145700%2C1510529706558163500%2C1069181371392656000; Q=u%3D360H3293566442%26n%3D%26le%3D%26m%3DZGtjWGWOWGWOWGWOWGWOWGWOAwL0%26qid%3D3293566442%26im%3D1_t01a6d072182d68691c%26src%3D360chrome_weixin%26t%3D1; T=s%3D9de7fbca26ebb26316ff577737e73691%26t%3D1660527054%26lm%3D%26lf%3D%26sk%3Dcc00bd94f0cb98a5d4bdf318c1cafdb3%26mt%3D1660527054%26rc%3D2%26v%3D2.0%26a%3D1; hasShowLiving=1; __DC_monitor_count=26; __DC_sid=123679891.1187142252985375000.1665641712097.414; IOT_MOCK=; __DC_gid=192758817.898550505.1665298430416.1665641807606.180

# COM69


class AIC():
    def __init__(self):    # 让类里面的每个方法都能调用
        self.ser = None
        self.P8_cookie = P8_cookie_A
        self.url_SheZhi = 'https://iot.zyun.360.cn/iot/api/common/device/setProperty'
        self.url_service = 'https://iot.zyun.360.cn/iot/api/common/device/invokeService'
        self.P8_cookies ={
            'Content-Type': 'application/json',
            'cookie': self.P8_cookie
        }

    # 清晰度高清_超清 2.5k
    def ClaritMode(self):
        # 高清
        P8_body = {
            'corp_id': "212",
            'device_name': P8_SN,
            'items': '{"ClarityMode":1}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland"
        }
        print(f'P8接口:----高清,时间:{str(datetime.now())}')
        requests.post(url=self.url_SheZhi, json=P8_body, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)
        # 高清
        P8_body = {
            'corp_id': "212",
            'device_name': P8_SN,
            'items': '{"ClarityMode":2}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland"
        }
        print(f'P8接口:----超清,时间:{str(datetime.now())}')
        requests.post(url=self.url_SheZhi, json=P8_body, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)
        # 2.5k
        P8_body = {
            'corp_id': "212",
            'device_name': P8_SN,
            'items': '{"ClarityMode":5}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland"
        }
        print(f'P8接口:----2.5K,时间:{str(datetime.now())}')
        requests.post(url=self.url_SheZhi, json=P8_body, headers=self.P8_cookies).json()  # Install

    # 呼叫指示灯
    def CustomCall(self):
        # 关闭
        P8_body = {
            'corp_id': "212",
            'device_name': P8_SN,
            'items': '{"CustomCallIndicator":false}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland"
        }
        print(f'P8接口:----呼叫指示灯-关,时间:{str(datetime.now())}')
        requests.post(url=self.url_SheZhi, json=P8_body, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)
        # 开
        P8_body = {
            'corp_id': "212",
            'device_name': P8_SN,
            'items': '{"CustomCallIndicator":true}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland"
        }
        print(f'P8接口:----呼叫指示灯-开,时间:{str(datetime.now())}')
        requests.post(url=self.url_SheZhi, json=P8_body, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)

    # 侦测开关
    def DetectionSwitch(self):
        # 关闭
        P8_body = {
            'corp_id': "212",
            'device_name': P8_SN,
            'items': '{"DetectionSwitch":false}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland"
        }
        print(f'P8接口:----侦测开关-开,时间:{str(datetime.now())}')
        requests.post(url=self.url_SheZhi, json=P8_body, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)
        # 开
        P8_body = {
            'corp_id': "212",
            'device_name': P8_SN,
            'items': '{"DetectionSwitch":true}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland"
        }
        print(f'P8接口:----侦测开关-开,时间:{str(datetime.now())}')
        requests.post(url=self.url_SheZhi, json=P8_body, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)

    # 侦测灵敏度
    def DetectSensitivity(self):
        # 低
        P8_body = {
            'corp_id': "212",
            'device_name': P8_SN,
            'items': '{"DetectSensitivity":0}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland"
        }
        print(f'P8接口:----侦测灵敏度-低,时间:{str(datetime.now())}')
        requests.post(url=self.url_SheZhi, json=P8_body, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)
        # 中
        P8_body = {
            'corp_id': "212",
            'device_name': P8_SN,
            'items': '{"DetectSensitivity":1}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland"
        }
        print(f'P8接口:----侦测灵敏度-中,时间:{str(datetime.now())}')
        requests.post(url=self.url_SheZhi, json=P8_body, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)
        # 高
        P8_body = {
            'corp_id': "212",
            'device_name': P8_SN,
            'items': '{"DetectSensitivity":2}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland"
        }
        print(f'P8接口:----侦测灵敏度-高,时间:{str(datetime.now())}')
        requests.post(url=self.url_SheZhi, json=P8_body, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)

    # 设备音量控制
    def DeviceVolume(self):
        # 100
        P8_body = {
            'corp_id': "212",
            'device_name': P8_SN,
            'items': '{"DeviceVolume":100}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland"
        }
        print(f'P8接口:----设备音量控制-100,时间:{str(datetime.now())}')
        requests.post(url=self.url_SheZhi, json=P8_body, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)
        # 50
        P8_body = {
            'corp_id': "212",
            'device_name': P8_SN,
            'items': '{"DeviceVolume":50}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland"
        }
        print(f'P8接口:----设备音量控制-50,时间:{str(datetime.now())}')
        requests.post(url=self.url_SheZhi, json=P8_body, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)
        # 0
        P8_body = {
            'corp_id': "212",
            'device_name': P8_SN,
            'items': '{"DeviceVolume":0}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland"
        }
        print(f'P8接口:----设备音量控制-0,时间:{str(datetime.now())}')
        requests.post(url=self.url_SheZhi, json=P8_body, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)

    # 画面翻转
    def ImageFlip(self):
        # 垂直翻转
        P8_body = {
            'corp_id': "212",
            'device_name': P8_SN,
            'items': '{"ImageFlip":2}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland"
        }
        print(f'P8接口:----画面翻转-垂直翻转,时间:{str(datetime.now())}')
        requests.post(url=self.url_SheZhi, json=P8_body, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)
        # 水平翻转
        P8_body = {
            'corp_id': "212",
            'device_name': P8_SN,
            'items': '{"ImageFlip":1}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland"
        }
        print(f'P8接口:----画面翻转-垂直翻转,时间:{str(datetime.now())}')
        requests.post(url=self.url_SheZhi, json=P8_body, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)

    # 状态指示灯
    def Indicator(self):
        # 关
        P8_body = {
            'corp_id': "212",
            'device_name': P8_SN,
            'items': '{"Indicator":false}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland"
        }
        print(f'P8接口:----状态指示灯-关,时间:{str(datetime.now())}')
        requests.post(url=self.url_SheZhi, json=P8_body, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)
        # 干
        P8_body = {
            'corp_id': "212",
            'device_name': P8_SN,
            'items': '{"Indicator":true}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland"
        }
        print(f'P8接口:----状态指示灯-开,时间:{str(datetime.now())}')
        requests.post(url=self.url_SheZhi, json=P8_body, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)

    # 无声录制
    def IpcMuteRecord(self):
        # 关
        P8_body = {
            'corp_id': "212",
            'device_name': P8_SN,
            'items': '{"IpcMuteRecord":false}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland"
        }
        print(f'P8接口:----无声录制-关,时间:{str(datetime.now())}')
        requests.post(url=self.url_SheZhi, json=P8_body, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)
        # 干
        P8_body = {
            'corp_id': "212",
            'device_name': P8_SN,
            'items': '{"IpcMuteRecord":true}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland"
        }
        print(f'P8接口:----无声录制-开,时间:{str(datetime.now())}')
        requests.post(url=self.url_SheZhi, json=P8_body, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)

    # 升级语音提示
    def IpcVoiceUpgrade(self):
        # 关
        P8_body = {
            'corp_id': "212",
            'device_name': P8_SN,
            'items': 'IpcVoiceUpgrade":false}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland"
        }
        print(f'P8接口:----升级语音提示-关,时间:{str(datetime.now())}')
        requests.post(url=self.url_SheZhi, json=P8_body, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)
        # 干
        P8_body = {
            'corp_id': "212",
            'device_name': P8_SN,
            'items': 'IpcVoiceUpgrade":true}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland"
        }
        print(f'P8接口:----升级语音提示-开,时间:{str(datetime.now())}')
        requests.post(url=self.url_SheZhi, json=P8_body, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)

    # 播放提示音
    def IpcVoiceWatch(self):
        # 关
        P8_body = {
            'corp_id': "212",
            'device_name': P8_SN,
            'items': '{"IpcVoiceWatch":false}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland"
        }
        print(f'P8接口:----播放提示音-关,时间:{str(datetime.now())}')
        requests.post(url=self.url_SheZhi, json=P8_body, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)
        # 干
        P8_body = {
            'corp_id': "212",
            'device_name': P8_SN,
            'items': '{"IpcVoiceWatch":true}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland"
        }
        print(f'P8接口:----播放提示音-开,时间:{str(datetime.now())}')
        requests.post(url=self.url_SheZhi, json=P8_body, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)

    # WDR
    def IpcWDRSwitch(self):
        # 关
        P8_body = {
            'corp_id': "212",
            'device_name': P8_SN,
            'items': '{"IpcWDRSwitch":false}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland"
        }
        print(f'P8接口:----WDR-关,时间:{str(datetime.now())}')
        requests.post(url=self.url_SheZhi, json=P8_body, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)
        # 干
        P8_body = {
            'corp_id': "212",
            'device_name': P8_SN,
            'items': '{"IpcWDRSwitch":true}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland"
        }
        print(f'P8接口:----WDR-开,时间:{str(datetime.now())}')
        requests.post(url=self.url_SheZhi, json=P8_body, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)

    # 麦克风开关
    def MicSwitch(self):
        # 关
        P8_body = {
            'corp_id': "212",
            'device_name': P8_SN,
            'items': '{"MicSwitch":false}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland"
        }
        print(f'P8接口:----麦克风-关,时间:{str(datetime.now())}')
        requests.post(url=self.url_SheZhi, json=P8_body, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)
        # 干
        P8_body = {
            'corp_id': "212",
            'device_name': P8_SN,
            'items': '{"MicSwitch":true}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland"
        }
        print(f'P8接口:----麦克风-开,时间:{str(datetime.now())}')
        requests.post(url=self.url_SheZhi, json=P8_body, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)

    # 移动侦测开关
    def MotionDetectSwitch(self):
        # 关
        P8_body = {
            'corp_id': "212",
            'device_name': P8_SN,
            'items': '{"MotionDetectSwitch":false}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland"
        }
        print(f'P8接口:----移动侦测-关,时间:{str(datetime.now())}')
        requests.post(url=self.url_SheZhi, json=P8_body, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)
        # 干
        P8_body = {
            'corp_id': "212",
            'device_name': P8_SN,
            'items': '{"MotionDetectSwitch":true}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland"
        }
        print(f'P8接口:----移动侦测-开,时间:{str(datetime.now())}')
        requests.post(url=self.url_SheZhi, json=P8_body, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)

    # 移动侦测灵敏度
    def MotionDetectSensitivity(self):
        # di
        P8_body = {
            'corp_id': "212",
            'device_name': P8_SN,
            'items': '{"MotionDetectSensitivity":0}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland"
        }
        print(f'P8接口:----移动侦测灵敏度-低,时间:{str(datetime.now())}')
        requests.post(url=self.url_SheZhi, json=P8_body, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)
        # zhong
        P8_body = {
            'corp_id': "212",
            'device_name': P8_SN,
            'items': '{"MotionDetectSensitivity":1}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland"
        }
        print(f'P8接口:----移动侦测灵敏度-中,时间:{str(datetime.now())}')
        requests.post(url=self.url_SheZhi, json=P8_body, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)
        # gao
        P8_body = {
            'corp_id': "212",
            'device_name': P8_SN,
            'items': '{"MotionDetectSensitivity":2}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland"
        }
        print(f'P8接口:----移动侦测灵敏度-高,时间:{str(datetime.now())}')
        requests.post(url=self.url_SheZhi, json=P8_body, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)

    # 红外夜视
    def Nightvision(self):
        # 关
        P8_body = {
            'corp_id': "212",
            'device_name': P8_SN,
            'items': '{"Nightvision":0}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland"
        }
        print(f'P8接口:----红外夜视-关,时间:{str(datetime.now())}')
        requests.post(url=self.url_SheZhi, json=P8_body, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)
        # 干
        P8_body = {
            'corp_id': "212",
            'device_name': P8_SN,
            'items': '{"Nightvision":1}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland"
        }
        print(f'P8接口:----红外夜视-开,时间:{str(datetime.now())}')
        requests.post(url=self.url_SheZhi, json=P8_body, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)

    # 提示音量
    def PromptVolume(self):
        # 关
        P8_body = {
            'corp_id': "212",
            'device_name': P8_SN,
            'items': '{"PromptVolume":0}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland"
        }
        print(f'P8接口:----提示音量-0,时间:{str(datetime.now())}')
        requests.post(url=self.url_SheZhi, json=P8_body, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)
        # 干
        P8_body = {
            'corp_id': "212",
            'device_name': P8_SN,
            'items': '{"PromptVolume":50}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland"
        }
        print(f'P8接口:----提示音量-50,时间:{str(datetime.now())}')
        requests.post(url=self.url_SheZhi, json=P8_body, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)
        # 干
        P8_body = {
            'corp_id': "212",
            'device_name': P8_SN,
            'items': '{"PromptVolume":100}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland"
        }
        print(f'P8接口:----提示音量-100,时间:{str(datetime.now())}')
        requests.post(url=self.url_SheZhi, json=P8_body, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)

    # 巡航
    def PtzCruiseSwitch(self):
        # 关
        P8_body = {
            'corp_id': "212",
            'device_name': P8_SN,
            'items': '{"PtzCruiseSwitch":true}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland"
        }
        print(f'P8接口:----巡航-开,时间:{str(datetime.now())}')
        requests.post(url=self.url_SheZhi, json=P8_body, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)
        # 干
        P8_body = {
            'corp_id': "212",
            'device_name': P8_SN,
            'items': '{"PtzCruiseSwitch":false}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland"
        }
        print(f'P8接口:----巡航-关,时间:{str(datetime.now())}')
        requests.post(url=self.url_SheZhi, json=P8_body, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)

    # 自动追踪
    def PtzMotionTracking(self):
        # 关
        P8_body = {
            'corp_id': "212",
            'device_name': P8_SN,
            'items': '{"PtzMotionTracking":true}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland"
        }
        print(f'P8接口:----自动追踪-开,时间:{str(datetime.now())}')
        requests.post(url=self.url_SheZhi, json=P8_body, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)
        # 干
        P8_body = {
            'corp_id': "212",
            'device_name': P8_SN,
            'items': '{"PtzMotionTracking":false}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland"
        }
        print(f'P8接口:----自动追踪-关,时间:{str(datetime.now())}')
        requests.post(url=self.url_SheZhi, json=P8_body, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)

    # 开关
    def Switch(self):
        # 关
        P8_body = {
            'corp_id': "212",
            'device_name': P8_SN,
            'items': '{"Switch":false}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland"
        }
        print(f'P8接口:----软开关-关,时间:{str(datetime.now())}')
        requests.post(url=self.url_SheZhi, json=P8_body, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)
        # 干
        P8_body = {
            'corp_id': "212",
            'device_name': P8_SN,
            'items': '{"Switch":true}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland"
        }
        print(f'P8接口:----软开关-开,时间:{str(datetime.now())}')
        requests.post(url=self.url_SheZhi, json=P8_body, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)

    # 双工通话音量
    def TalkingVolume(self):
        # 关
        P8_body = {
            'corp_id': "212",
            'device_name': P8_SN,
            'items': '{"TalkingVolume":0}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland"
        }
        print(f'P8接口:----双工通话音量-0,时间:{str(datetime.now())}')
        requests.post(url=self.url_SheZhi, json=P8_body, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)
        # 干
        P8_body = {
            'corp_id': "212",
            'device_name': P8_SN,
            'items': '{"TalkingVolume":50}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland"
        }
        print(f'P8接口:----双工通话音量-50,时间:{str(datetime.now())}')
        requests.post(url=self.url_SheZhi, json=P8_body, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)
        # 干
        P8_body = {
            'corp_id': "212",
            'device_name': P8_SN,
            'items': '{"TalkingVolume":100}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland"
        }
        print(f'P8接口:----双工通话音量-100,时间:{str(datetime.now())}')
        requests.post(url=self.url_SheZhi, json=P8_body, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)

    # 技能_安装/更新/卸载
    def P8_Install(self):
        P8_body_Install = {
            'corp_id': "212",
            'device_name': P8_SN,
            'identifier': "AiLabAction",
            'input_data': '{"Action":"Install","SkillId":"627011944199475200","SkillVersion":"1.0.0"}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland",
        }
        print(f'P8接口:----技能触发安装,时间:{str(datetime.now())}')
        requests.post(url=self.url_service, json=P8_body_Install, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)
        P8_body_Install = {
            'corp_id': "212",
            'device_name': P8_SN,
            'identifier': "AiLabAction",
            'input_data': '{"Action":"Upgrade","SkillId":"627011944199475200","SkillVersion":"1.0.4"}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland",
        }
        print(f'P8接口:----技能触发更新,时间:{str(datetime.now())}')
        requests.post(url=self.url_service, json=P8_body_Install, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)
        P8_body_Install = {
            'corp_id': "212",
            'device_name': P8_SN,
            'identifier': "AiLabAction",
            'input_data': '{"Action":"Uninstall","SkillId":"627011944199475200","SkillVersion":"1.0.4"}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland",
        }
        print(f'P8接口:----技能触发更新,时间:{str(datetime.now())}')
        requests.post(url=self.url_service, json=P8_body_Install, headers=self.P8_cookies).json()  # Install
        time.sleep(P8_timeout)

    # 设备串口
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
                        with open('E:\Python_Projects\压测LOG\P8_稳定性压力.log', 'a', encoding='UTF-8', errors='ignore') as log:
                            log.writelines(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' ' + c5)
                        if 'CPU: 0 PID' in c5:
                            print(f'{datetime.now()}:P8串口:OOM{c5}')
                            t1.start()
                        if 'Out of memory' in c5:
                            print(f'{datetime.now()}P8串口:Out of memory:{c5}')
                            t1.start()
                        if 'Ready sd upgrade' in c5:
                            print('P8MAX------------------------:进入回退版本流程,' + str(datetime.now()))
                            # break
                        # if 'soc-nna version' in c5:
                        #     print('P8MAX------------------------:回退完成,完成重启,' + str(datetime.now()))
                        if 'U-Boot SPL' in c5:
                            print('P8MAX------------------------:重启中,' + str(datetime.now()))
                            t1.start()
                        if 'SIGSEGV' in c5:
                            print('P8MAX------------------------:断错误' + str(datetime.now()))
                            t1.start()
                            # break
            # print('超时退出')
            self.ser.close()  # 关闭串口
        except Exception as e:
            print("---异常---：", e)
            pass

    def Showinfo(self):
        msgbox.showinfo('芭比Q', '串口异常打印啦')  # 弹窗提示


AIC = AIC()
i = 0
t = threading.Thread(target=AIC.P8_Serial)
t.start()
t1 = threading.Thread(target=AIC.Showinfo)

time.sleep(5)
while True:
    i+=1
    print(f'\n===================={i}=================,{datetime.now()}')
    try:
        AIC.ClaritMode()
        AIC.CustomCall()
        AIC.DetectionSwitch()
        AIC.DetectSensitivity()
        AIC.DeviceVolume()
        AIC.ImageFlip()
        AIC.Indicator()
        AIC.IpcMuteRecord()
        AIC.IpcVoiceUpgrade()
        AIC.IpcVoiceWatch()
        AIC.IpcWDRSwitch()
        AIC.MicSwitch()
        AIC.MotionDetectSwitch()
        AIC.MotionDetectSensitivity()
        AIC.Nightvision()
        AIC.PromptVolume()
        AIC.PtzCruiseSwitch()
        AIC.PtzMotionTracking()
        AIC.Switch()
        AIC.TalkingVolume()
        AIC.P8_Install()
    except:pass


# print(inspect.getmembers(AIC,inspect.isfunction))

