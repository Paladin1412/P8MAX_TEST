# -*- coding: utf-8 -*- 
# @Time : 2022/10/14 14:13 
# @Author : 能飞会打智勇双全的才高八斗 
# @File : test.py
# -*- coding: utf-8 -*-
# @Time : 2022/10/14 11:40
# @Author : 能飞会打智勇双全的才高八斗
# @File : cloud_services.py
#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
描述
http://wiki.360iot.qihoo.net/pages/viewpage.action?pageId=29730122

"""

import re
import requests
import threading
import serial #导入模块
import time
import requests
from datetime import datetime
import time
import random
import hashlib
import time
import random
import base64
import json
import urllib.parse
import csv
P8_timeout = float(0.5)
P8_SN_list = ['86XCP8M12370000049','P8MAX_12']
setProperty = ['{"TalkingVolume":100}', '{"TalkingVolume":50}', '{"TalkingVolume":0}', '{"Switch":true}',
               '{"Switch":false}', '{"PtzMotionTracking":false}', '{"PtzMotionTracking":true}',
               '{"PtzCruiseSwitch":false}', '{"PtzCruiseSwitch":true}', '{"PromptVolume":100}', '{"PromptVolume":50}',
               '{"PromptVolume":0}', '{"Nightvision":1}', '{"Nightvision":0}', '{"MotionDetectSensitivity":2}',
               '{"MotionDetectSensitivity":1}', '{"MotionDetectSensitivity":0}', '{"MotionDetectSwitch":true}',
               '{"MotionDetectSwitch":false}', '{"MicSwitch":true}', '{"MicSwitch":false}', '{"IpcWDRSwitch":true}',
               '{"IpcWDRSwitch":false}', '{"IpcVoiceWatch":true}', '{"IpcVoiceWatch":false}', 'IpcVoiceUpgrade":true}',
               '{"IpcVoiceUpgrade":false}', '{"IpcMuteRecord":true}', '{"IpcMuteRecord":false}', '{"Indicator":true}',
               '{"Indicator":false}', '{"ImageFlip":1}', '{"ImageFlip":2}', '{"DeviceVolume":0}', '{"DeviceVolume":50}',
               '{"DeviceVolume":100}', '{"DetectSensitivity":2}', '{"DetectSensitivity":1}', '{"DetectSensitivity":0}',
               '{"DetectionSwitch":true}', '{"DetectionSwitch":false}', '{"CustomCallIndicator":true}',
               '{"CustomCallIndicator":false}', '{"ClarityMode":5}', '{"ClarityMode":2}', '{"ClarityMode":1}', ]


class AIC():
    def __init__(self):
        self.base_url = "http://cn-iot-api.iot.360.cn"  # openapi测试环境
        self.api = "/device/setProperty"
        self.url = self.base_url + self.api
        self.appkey = "147cb0cea801c54f01c17cc40c8ccc4f"
        self.appsecret = "137c49fb7c4799fbfa7d4715c2bd978c"
        self.ver = "1.0"
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded',
                   'User-Agent': 'Go-http-client/1.1',
                   }
        self.nonce = self.generate_code()
    def md5value(self,s):
        md5 = hashlib.md5()
        md5.update(s.encode("utf-8"))
        return md5.hexdigest()

    #   六位唯一随机数
    def generate_code(self,code_len=6):
        all_char = '0123456789qazwsxedcrfvtgbyhnujmikolpQAZWSXEDCRFVTGBYHNUJMIKOLP'
        index = len(all_char) - 1
        code = ''
        for _ in range(code_len):
            num = random.randint(0, index)
            code += all_char[num]
        return code

    def lower_key_in_params(self,params_to_be_signed):
        new_params = {}
        for i, j in params_to_be_signed.items():
            new_params[i.lower()] = j
        return new_params

    def build_sign(self,new_params):
        tmp_dict = self.lower_key_in_params(new_params)
        temp_list = sorted(tmp_dict.items(), key=lambda x: x[0], reverse=False)
        # 将参数名称和参数值分别进行 URL encoded 编码
        temp_list1 = urllib.parse.urlencode(temp_list)
        return temp_list1


    def CustomCallIndicator_true1(self, P8_SN,SetProperty_ID):
        sign_params = {
            "appkey": self.appkey,
            "nonce": self.nonce,
            "r": int(time.time()),
            "ver": "1.0",
            "product_key": "2b7e7feff233",
            "device_name": P8_SN,
            "items": SetProperty_ID,

        }
        params_to_be_signed = dict(sign_params)
        new_params = self.lower_key_in_params(params_to_be_signed)
        params = self.build_sign(new_params)
        params1 = params + "&" + self.appsecret
        replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
        after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
                                       lambda m: replacements[m.group()], params1)
        sign = self.md5value(after_replace_params1)
        post_params = {
            "appkey": self.appkey,
            "sign": sign,
            "nonce": self.nonce,
            "r": int(time.time()),
            "ver": "1.0",
            "product_key": "2b7e7feff233",
            "device_name": P8_SN,
            "items": SetProperty_ID,
        }
        requests.post(self.url, data=post_params, headers=self.headers)
        print(f'P8接口{P8_SN},{SetProperty_ID}:----推送完毕,时间:{str(datetime.now())}')
        time.sleep(P8_timeout)
    def start1(self):
        for SetProperty_ID in setProperty:

            for P8_SN in P8_SN_list:
                time.sleep(P8_timeout)
                t = threading.Thread(target=self.CustomCallIndicator_true1, args=(P8_SN, SetProperty_ID))
                t.start()

    # def CustomCallIndicator_true(self, P8_SN):
    #     # 高清
    #     sign_params = {
    #         "appkey": self.appkey,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"ClarityMode":1}',
    #
    #     }
    #     params_to_be_signed = dict(sign_params)
    #     new_params = self.lower_key_in_params(params_to_be_signed)
    #     params = self.build_sign(new_params)
    #     params1 = params + "&" + self.appsecret
    #     replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
    #     after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
    #                                    lambda m: replacements[m.group()], params1)
    #     sign = self.md5value(after_replace_params1)
    #     post_params = {
    #         "appkey": self.appkey,
    #         "sign": sign,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"ClarityMode":1}',
    #     }
    #     requests.post(self.url, data=post_params, headers=self.headers)
    #     print(f'P8接口{P8_SN}:----高清,时间:{str(datetime.now())}')
    #     time.sleep(P8_timeout)
    #
    #
    #     # 超清
    #     sign_params = {
    #         "appkey": self.appkey,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"ClarityMode":2}',
    #
    #     }
    #     params_to_be_signed = dict(sign_params)
    #     new_params = self.lower_key_in_params(params_to_be_signed)
    #     params = self.build_sign(new_params)
    #     params1 = params + "&" + self.appsecret
    #     replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
    #     after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
    #                                    lambda m: replacements[m.group()], params1)
    #     sign = self.md5value(after_replace_params1)
    #     post_params = {
    #         "appkey": self.appkey,
    #         "sign": sign,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"ClarityMode":2}',
    #     }
    #     requests.post(self.url, data=post_params, headers=self.headers)
    #     print(f'P8接口{P8_SN}:----超清,时间:{str(datetime.now())}')
    #     time.sleep(P8_timeout)
    #
    #     # 2.5k
    #     sign_params = {
    #         "appkey": self.appkey,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"ClarityMode":5}',
    #
    #     }
    #     params_to_be_signed = dict(sign_params)
    #     new_params = self.lower_key_in_params(params_to_be_signed)
    #     params = self.build_sign(new_params)
    #     params1 = params + "&" + self.appsecret
    #     replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
    #     after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
    #                                    lambda m: replacements[m.group()], params1)
    #     sign = self.md5value(after_replace_params1)
    #     post_params = {
    #         "appkey": self.appkey,
    #         "sign": sign,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"ClarityMode":5}',
    #     }
    #     requests.post(self.url, data=post_params, headers=self.headers)
    #     print(f'P8接口{P8_SN}:----2.5k,时间:{str(datetime.now())}')
    #     time.sleep(P8_timeout)
    #
    #     # 呼叫指示灯 关闭
    #     sign_params = {
    #         "appkey": self.appkey,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"CustomCallIndicator":false}',
    #
    #     }
    #     params_to_be_signed = dict(sign_params)
    #     new_params = self.lower_key_in_params(params_to_be_signed)
    #     params = self.build_sign(new_params)
    #     params1 = params + "&" + self.appsecret
    #     replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
    #     after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
    #                                    lambda m: replacements[m.group()], params1)
    #     sign = self.md5value(after_replace_params1)
    #     post_params = {
    #         "appkey": self.appkey,
    #         "sign": sign,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"CustomCallIndicator":false}',
    #     }
    #     requests.post(self.url, data=post_params, headers=self.headers)
    #     print(f'P8接口{P8_SN}:----呼叫指示灯-关,时间:{str(datetime.now())}')
    #     time.sleep(P8_timeout)
    #
    #     # 呼叫指示灯 开启
    #     sign_params = {
    #         "appkey": self.appkey,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"CustomCallIndicator":true}',
    #
    #     }
    #     params_to_be_signed = dict(sign_params)
    #     new_params = self.lower_key_in_params(params_to_be_signed)
    #     params = self.build_sign(new_params)
    #     params1 = params + "&" + self.appsecret
    #     replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
    #     after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
    #                                    lambda m: replacements[m.group()], params1)
    #     sign = self.md5value(after_replace_params1)
    #     post_params = {
    #         "appkey": self.appkey,
    #         "sign": sign,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"CustomCallIndicator":true}',
    #     }
    #     requests.post(self.url, data=post_params, headers=self.headers)
    #     print(f'P8接口{P8_SN}:----呼叫指示灯-开,时间:{str(datetime.now())}')
    #     time.sleep(P8_timeout)
    #
    #     # 侦测开关 关闭
    #     sign_params = {
    #         "appkey": self.appkey,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"DetectionSwitch":false}',
    #
    #     }
    #     params_to_be_signed = dict(sign_params)
    #     new_params = self.lower_key_in_params(params_to_be_signed)
    #     params = self.build_sign(new_params)
    #     params1 = params + "&" + self.appsecret
    #     replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
    #     after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
    #                                    lambda m: replacements[m.group()], params1)
    #     sign = self.md5value(after_replace_params1)
    #     post_params = {
    #         "appkey": self.appkey,
    #         "sign": sign,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"DetectionSwitch":false}',
    #     }
    #     requests.post(self.url, data=post_params, headers=self.headers)
    #     print(f'P8接口{P8_SN}:----侦测开关-关,时间:{str(datetime.now())}')
    #     time.sleep(P8_timeout)
    #
    #     # 侦测开关 开
    #     sign_params = {
    #         "appkey": self.appkey,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"DetectionSwitch":true}',
    #
    #     }
    #     params_to_be_signed = dict(sign_params)
    #     new_params = self.lower_key_in_params(params_to_be_signed)
    #     params = self.build_sign(new_params)
    #     params1 = params + "&" + self.appsecret
    #     replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
    #     after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
    #                                    lambda m: replacements[m.group()], params1)
    #     sign = self.md5value(after_replace_params1)
    #     post_params = {
    #         "appkey": self.appkey,
    #         "sign": sign,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"DetectionSwitch":true}',
    #     }
    #     requests.post(self.url, data=post_params, headers=self.headers)
    #     print(f'P8接口{P8_SN}:----侦测开关-开,时间:{str(datetime.now())}')
    #     time.sleep(P8_timeout)
    #
    #     # 侦测灵敏度 低
    #     sign_params = {
    #         "appkey": self.appkey,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"DetectSensitivity":0}',
    #
    #     }
    #     params_to_be_signed = dict(sign_params)
    #     new_params = self.lower_key_in_params(params_to_be_signed)
    #     params = self.build_sign(new_params)
    #     params1 = params + "&" + self.appsecret
    #     replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
    #     after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
    #                                    lambda m: replacements[m.group()], params1)
    #     sign = self.md5value(after_replace_params1)
    #     post_params = {
    #         "appkey": self.appkey,
    #         "sign": sign,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"DetectSensitivity":0}',
    #     }
    #     requests.post(self.url, data=post_params, headers=self.headers)
    #     print(f'P8接口{P8_SN}:----侦测灵敏度-低,时间:{str(datetime.now())}')
    #     time.sleep(P8_timeout)
    #
    #     # 侦测灵敏度 中
    #     sign_params = {
    #         "appkey": self.appkey,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"DetectSensitivity":1}',
    #
    #     }
    #     params_to_be_signed = dict(sign_params)
    #     new_params = self.lower_key_in_params(params_to_be_signed)
    #     params = self.build_sign(new_params)
    #     params1 = params + "&" + self.appsecret
    #     replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
    #     after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
    #                                    lambda m: replacements[m.group()], params1)
    #     sign = self.md5value(after_replace_params1)
    #     post_params = {
    #         "appkey": self.appkey,
    #         "sign": sign,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"DetectSensitivity":1}',
    #     }
    #     requests.post(self.url, data=post_params, headers=self.headers)
    #     print(f'P8接口{P8_SN}:----侦测灵敏度-中,时间:{str(datetime.now())}')
    #     time.sleep(P8_timeout)
    #
    #     # 侦测灵敏度 高
    #     sign_params = {
    #         "appkey": self.appkey,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"DetectSensitivity":2}',
    #
    #     }
    #     params_to_be_signed = dict(sign_params)
    #     new_params = self.lower_key_in_params(params_to_be_signed)
    #     params = self.build_sign(new_params)
    #     params1 = params + "&" + self.appsecret
    #     replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
    #     after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
    #                                    lambda m: replacements[m.group()], params1)
    #     sign = self.md5value(after_replace_params1)
    #     post_params = {
    #         "appkey": self.appkey,
    #         "sign": sign,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"DetectSensitivity":2}',
    #     }
    #     requests.post(self.url, data=post_params, headers=self.headers)
    #     print(f'P8接口{P8_SN}:----侦测灵敏度-高,时间:{str(datetime.now())}')
    #     time.sleep(P8_timeout)
    #     # 设备音量控制 100
    #     sign_params = {
    #         "appkey": self.appkey,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"DeviceVolume":100}',
    #
    #     }
    #     params_to_be_signed = dict(sign_params)
    #     new_params = self.lower_key_in_params(params_to_be_signed)
    #     params = self.build_sign(new_params)
    #     params1 = params + "&" + self.appsecret
    #     replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
    #     after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
    #                                    lambda m: replacements[m.group()], params1)
    #     sign = self.md5value(after_replace_params1)
    #     post_params = {
    #         "appkey": self.appkey,
    #         "sign": sign,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"DeviceVolume":100}',
    #     }
    #     requests.post(self.url, data=post_params, headers=self.headers)
    #     print(f'P8接口{P8_SN}:----侦测灵敏度-高,时间:{str(datetime.now())}')
    #     time.sleep(P8_timeout)
    #
    #     # 设备音量控制 50
    #     sign_params = {
    #         "appkey": self.appkey,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"DeviceVolume":50}',
    #
    #     }
    #     params_to_be_signed = dict(sign_params)
    #     new_params = self.lower_key_in_params(params_to_be_signed)
    #     params = self.build_sign(new_params)
    #     params1 = params + "&" + self.appsecret
    #     replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
    #     after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
    #                                    lambda m: replacements[m.group()], params1)
    #     sign = self.md5value(after_replace_params1)
    #     post_params = {
    #         "appkey": self.appkey,
    #         "sign": sign,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"DeviceVolume":50}',
    #     }
    #     requests.post(self.url, data=post_params, headers=self.headers)
    #     print(f'P8接口{P8_SN}:----设备音量控制-50,时间:{str(datetime.now())}')
    #     time.sleep(P8_timeout)
    #
    #     # 设备音量控制 20
    #     sign_params = {
    #         "appkey": self.appkey,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"DeviceVolume":50}',
    #
    #     }
    #     params_to_be_signed = dict(sign_params)
    #     new_params = self.lower_key_in_params(params_to_be_signed)
    #     params = self.build_sign(new_params)
    #     params1 = params + "&" + self.appsecret
    #     replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
    #     after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
    #                                    lambda m: replacements[m.group()], params1)
    #     sign = self.md5value(after_replace_params1)
    #     post_params = {
    #         "appkey": self.appkey,
    #         "sign": sign,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"DeviceVolume":20}',
    #     }
    #     requests.post(self.url, data=post_params, headers=self.headers)
    #     print(f'P8接口{P8_SN}:----设备音量控制-20,时间:{str(datetime.now())}')
    #     time.sleep(P8_timeout)
    #
    #     # 垂直翻转
    #     sign_params = {
    #         "appkey": self.appkey,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"ImageFlip":2}',
    #
    #     }
    #     params_to_be_signed = dict(sign_params)
    #     new_params = self.lower_key_in_params(params_to_be_signed)
    #     params = self.build_sign(new_params)
    #     params1 = params + "&" + self.appsecret
    #     replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
    #     after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
    #                                    lambda m: replacements[m.group()], params1)
    #     sign = self.md5value(after_replace_params1)
    #     post_params = {
    #         "appkey": self.appkey,
    #         "sign": sign,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"ImageFlip":2}',
    #     }
    #     requests.post(self.url, data=post_params, headers=self.headers)
    #     print(f'P8接口{P8_SN}:----画面翻转-垂直翻转,时间:{str(datetime.now())}')
    #     time.sleep(P8_timeout)
    #
    #     # 水平翻转
    #     sign_params = {
    #         "appkey": self.appkey,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"ImageFlip":1}',
    #
    #     }
    #     params_to_be_signed = dict(sign_params)
    #     new_params = self.lower_key_in_params(params_to_be_signed)
    #     params = self.build_sign(new_params)
    #     params1 = params + "&" + self.appsecret
    #     replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
    #     after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
    #                                    lambda m: replacements[m.group()], params1)
    #     sign = self.md5value(after_replace_params1)
    #     post_params = {
    #         "appkey": self.appkey,
    #         "sign": sign,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"ImageFlip":1}',
    #     }
    #     requests.post(self.url, data=post_params, headers=self.headers)
    #     print(f'P8接口{P8_SN}:----画面翻转-水平翻转,时间:{str(datetime.now())}')
    #     time.sleep(P8_timeout)
    #
    #     # 状态指示灯 关
    #     sign_params = {
    #         "appkey": self.appkey,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"Indicator":false}',
    #
    #     }
    #     params_to_be_signed = dict(sign_params)
    #     new_params = self.lower_key_in_params(params_to_be_signed)
    #     params = self.build_sign(new_params)
    #     params1 = params + "&" + self.appsecret
    #     replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
    #     after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
    #                                    lambda m: replacements[m.group()], params1)
    #     sign = self.md5value(after_replace_params1)
    #     post_params = {
    #         "appkey": self.appkey,
    #         "sign": sign,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"Indicator":false}',
    #     }
    #     requests.post(self.url, data=post_params, headers=self.headers)
    #     print(f'P8接口{P8_SN}:----状态指示灯-关,时间:{str(datetime.now())}')
    #     time.sleep(P8_timeout)
    #
    #     # 状态指示灯 开
    #     sign_params = {
    #         "appkey": self.appkey,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"Indicator":true}',
    #
    #     }
    #     params_to_be_signed = dict(sign_params)
    #     new_params = self.lower_key_in_params(params_to_be_signed)
    #     params = self.build_sign(new_params)
    #     params1 = params + "&" + self.appsecret
    #     replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
    #     after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
    #                                    lambda m: replacements[m.group()], params1)
    #     sign = self.md5value(after_replace_params1)
    #     post_params = {
    #         "appkey": self.appkey,
    #         "sign": sign,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"Indicator":true}',
    #     }
    #     requests.post(self.url, data=post_params, headers=self.headers)
    #     print(f'P8接口{P8_SN}:----状态指示灯-开,时间:{str(datetime.now())}')
    #     time.sleep(P8_timeout)
    #
    #     # 无声录制 关
    #     sign_params = {
    #         "appkey": self.appkey,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"IpcMuteRecord":true}',
    #
    #     }
    #     params_to_be_signed = dict(sign_params)
    #     new_params = self.lower_key_in_params(params_to_be_signed)
    #     params = self.build_sign(new_params)
    #     params1 = params + "&" + self.appsecret
    #     replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
    #     after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
    #                                    lambda m: replacements[m.group()], params1)
    #     sign = self.md5value(after_replace_params1)
    #     post_params = {
    #         "appkey": self.appkey,
    #         "sign": sign,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"IpcMuteRecord":true}',
    #     }
    #     requests.post(self.url, data=post_params, headers=self.headers)
    #     print(f'P8接口{P8_SN}:----无声录制-开,时间:{str(datetime.now())}')
    #     time.sleep(P8_timeout)
    #
    #     # 无声录制 开
    #     sign_params = {
    #         "appkey": self.appkey,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"IpcMuteRecord":false}',
    #
    #     }
    #     params_to_be_signed = dict(sign_params)
    #     new_params = self.lower_key_in_params(params_to_be_signed)
    #     params = self.build_sign(new_params)
    #     params1 = params + "&" + self.appsecret
    #     replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
    #     after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
    #                                    lambda m: replacements[m.group()], params1)
    #     sign = self.md5value(after_replace_params1)
    #     post_params = {
    #         "appkey": self.appkey,
    #         "sign": sign,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"IpcMuteRecord":false}',
    #     }
    #     requests.post(self.url, data=post_params, headers=self.headers)
    #     print(f'P8接口{P8_SN}:----无声录制-关,时间:{str(datetime.now())}')
    #     time.sleep(P8_timeout)
    #
    #     # 升级语音提示
    #     sign_params = {
    #         "appkey": self.appkey,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"IpcVoiceUpgrade":false}',
    #
    #     }
    #     params_to_be_signed = dict(sign_params)
    #     new_params = self.lower_key_in_params(params_to_be_signed)
    #     params = self.build_sign(new_params)
    #     params1 = params + "&" + self.appsecret
    #     replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
    #     after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
    #                                    lambda m: replacements[m.group()], params1)
    #     sign = self.md5value(after_replace_params1)
    #     post_params = {
    #         "appkey": self.appkey,
    #         "sign": sign,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"IpcMuteRecord":false}',
    #     }
    #     requests.post(self.url, data=post_params, headers=self.headers)
    #     print(f'P8接口{P8_SN}:----升级语音提示-关,时间:{str(datetime.now())}')
    #     time.sleep(P8_timeout)
    #
    #     # 升级语音提示
    #     sign_params = {
    #         "appkey": self.appkey,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{IpcVoiceUpgrade":false}',
    #
    #     }
    #     params_to_be_signed = dict(sign_params)
    #     new_params = self.lower_key_in_params(params_to_be_signed)
    #     params = self.build_sign(new_params)
    #     params1 = params + "&" + self.appsecret
    #     replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
    #     after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
    #                                    lambda m: replacements[m.group()], params1)
    #     sign = self.md5value(after_replace_params1)
    #     post_params = {
    #         "appkey": self.appkey,
    #         "sign": sign,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"IpcMuteRecord":true}',
    #     }
    #     requests.post(self.url, data=post_params, headers=self.headers)
    #     print(f'P8接口{P8_SN}:----升级语音提示-开,时间:{str(datetime.now())}')
    #     time.sleep(P8_timeout)
    #
    #     sign_params = {
    #         "appkey": self.appkey,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"IpcVoiceWatch":false}',
    #
    #     }
    #     params_to_be_signed = dict(sign_params)
    #     new_params = self.lower_key_in_params(params_to_be_signed)
    #     params = self.build_sign(new_params)
    #     params1 = params + "&" + self.appsecret
    #     replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
    #     after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
    #                                    lambda m: replacements[m.group()], params1)
    #     sign = self.md5value(after_replace_params1)
    #     post_params = {
    #         "appkey": self.appkey,
    #         "sign": sign,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"IpcVoiceWatch":false}',
    #     }
    #     requests.post(self.url, data=post_params, headers=self.headers)
    #     print(f'P8接口{P8_SN}:----播放提示音-关,时间:{str(datetime.now())}')
    #     time.sleep(P8_timeout)
    #
    #     sign_params = {
    #         "appkey": self.appkey,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"IpcVoiceWatch":true}',
    #
    #     }
    #     params_to_be_signed = dict(sign_params)
    #     new_params = self.lower_key_in_params(params_to_be_signed)
    #     params = self.build_sign(new_params)
    #     params1 = params + "&" + self.appsecret
    #     replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
    #     after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
    #                                    lambda m: replacements[m.group()], params1)
    #     sign = self.md5value(after_replace_params1)
    #     post_params = {
    #         "appkey": self.appkey,
    #         "sign": sign,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"IpcVoiceWatch":true}',
    #     }
    #     requests.post(self.url, data=post_params, headers=self.headers)
    #     print(f'P8接口{P8_SN}:----播放提示音-开,时间:{str(datetime.now())}')
    #     time.sleep(P8_timeout)
    #
    #     # WDR 关
    #     sign_params = {
    #         "appkey": self.appkey,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"IpcWDRSwitch":false}',
    #
    #     }
    #     params_to_be_signed = dict(sign_params)
    #     new_params = self.lower_key_in_params(params_to_be_signed)
    #     params = self.build_sign(new_params)
    #     params1 = params + "&" + self.appsecret
    #     replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
    #     after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
    #                                    lambda m: replacements[m.group()], params1)
    #     sign = self.md5value(after_replace_params1)
    #     post_params = {
    #         "appkey": self.appkey,
    #         "sign": sign,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"IpcWDRSwitch":false}',
    #     }
    #     requests.post(self.url, data=post_params, headers=self.headers)
    #     print(f'P8接口{P8_SN}:----WDR-开,时间:{str(datetime.now())}')
    #     time.sleep(P8_timeout)
    #
    #     # WDR 开
    #     sign_params = {
    #         "appkey": self.appkey,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"IpcWDRSwitch":true}',
    #
    #     }
    #     params_to_be_signed = dict(sign_params)
    #     new_params = self.lower_key_in_params(params_to_be_signed)
    #     params = self.build_sign(new_params)
    #     params1 = params + "&" + self.appsecret
    #     replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
    #     after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
    #                                    lambda m: replacements[m.group()], params1)
    #     sign = self.md5value(after_replace_params1)
    #     post_params = {
    #         "appkey": self.appkey,
    #         "sign": sign,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"IpcWDRSwitch":true}',
    #     }
    #     requests.post(self.url, data=post_params, headers=self.headers)
    #     print(f'P8接口{P8_SN}:----WDR-开,时间:{str(datetime.now())}')
    #     time.sleep(P8_timeout)
    #
    #     # 麦克风 关
    #     sign_params = {
    #         "appkey": self.appkey,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"MicSwitch":false}',
    #
    #     }
    #     params_to_be_signed = dict(sign_params)
    #     new_params = self.lower_key_in_params(params_to_be_signed)
    #     params = self.build_sign(new_params)
    #     params1 = params + "&" + self.appsecret
    #     replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
    #     after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
    #                                    lambda m: replacements[m.group()], params1)
    #     sign = self.md5value(after_replace_params1)
    #     post_params = {
    #         "appkey": self.appkey,
    #         "sign": sign,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"MicSwitch":false}',
    #     }
    #     requests.post(self.url, data=post_params, headers=self.headers)
    #     print(f'P8接口{P8_SN}:----Mic-关,时间:{str(datetime.now())}')
    #     time.sleep(P8_timeout)
    #
    #     # 麦克风 开
    #     sign_params = {
    #         "appkey": self.appkey,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"MicSwitch":true}',
    #
    #     }
    #     params_to_be_signed = dict(sign_params)
    #     new_params = self.lower_key_in_params(params_to_be_signed)
    #     params = self.build_sign(new_params)
    #     params1 = params + "&" + self.appsecret
    #     replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
    #     after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
    #                                    lambda m: replacements[m.group()], params1)
    #     sign = self.md5value(after_replace_params1)
    #     post_params = {
    #         "appkey": self.appkey,
    #         "sign": sign,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"MicSwitch":true}',
    #     }
    #     requests.post(self.url, data=post_params, headers=self.headers)
    #     print(f'P8接口{P8_SN}:----Mic-开,时间:{str(datetime.now())}')
    #     time.sleep(P8_timeout)
    #
    #     # 移动侦测开关
    #     sign_params = {
    #         "appkey": self.appkey,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"MotionDetectSwitch":false}',
    #
    #     }
    #     params_to_be_signed = dict(sign_params)
    #     new_params = self.lower_key_in_params(params_to_be_signed)
    #     params = self.build_sign(new_params)
    #     params1 = params + "&" + self.appsecret
    #     replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
    #     after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
    #                                    lambda m: replacements[m.group()], params1)
    #     sign = self.md5value(after_replace_params1)
    #     post_params = {
    #         "appkey": self.appkey,
    #         "sign": sign,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"MotionDetectSwitch":false}',
    #     }
    #     requests.post(self.url, data=post_params, headers=self.headers)
    #     print(f'P8接口{P8_SN}:----移动侦测-关,时间:{str(datetime.now())}')
    #     time.sleep(P8_timeout)
    #
    #     # 移动侦测开关
    #     sign_params = {
    #         "appkey": self.appkey,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"MotionDetectSwitch":true}',
    #
    #     }
    #     params_to_be_signed = dict(sign_params)
    #     new_params = self.lower_key_in_params(params_to_be_signed)
    #     params = self.build_sign(new_params)
    #     params1 = params + "&" + self.appsecret
    #     replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
    #     after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
    #                                    lambda m: replacements[m.group()], params1)
    #     sign = self.md5value(after_replace_params1)
    #     post_params = {
    #         "appkey": self.appkey,
    #         "sign": sign,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"MotionDetectSwitch":true}',
    #     }
    #     requests.post(self.url, data=post_params, headers=self.headers)
    #     print(f'P8接口{P8_SN}:----移动侦测-开,时间:{str(datetime.now())}')
    #     time.sleep(P8_timeout)
    #
    #     # 移动侦测灵敏度
    #     sign_params = {
    #         "appkey": self.appkey,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"MotionDetectSensitivity":0}',
    #
    #     }
    #     params_to_be_signed = dict(sign_params)
    #     new_params = self.lower_key_in_params(params_to_be_signed)
    #     params = self.build_sign(new_params)
    #     params1 = params + "&" + self.appsecret
    #     replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
    #     after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
    #                                    lambda m: replacements[m.group()], params1)
    #     sign = self.md5value(after_replace_params1)
    #     post_params = {
    #         "appkey": self.appkey,
    #         "sign": sign,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"MotionDetectSensitivity":0}',
    #     }
    #     requests.post(self.url, data=post_params, headers=self.headers)
    #     print(f'P8接口{P8_SN}:----移动侦测灵敏度-低,时间:{str(datetime.now())}')
    #     time.sleep(P8_timeout)
    #     # 移动侦测灵敏度 中
    #     sign_params = {
    #         "appkey": self.appkey,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"MotionDetectSensitivity":1}',
    #
    #     }
    #     params_to_be_signed = dict(sign_params)
    #     new_params = self.lower_key_in_params(params_to_be_signed)
    #     params = self.build_sign(new_params)
    #     params1 = params + "&" + self.appsecret
    #     replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
    #     after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
    #                                    lambda m: replacements[m.group()], params1)
    #     sign = self.md5value(after_replace_params1)
    #     post_params = {
    #         "appkey": self.appkey,
    #         "sign": sign,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"MotionDetectSensitivity":1}',
    #     }
    #     requests.post(self.url, data=post_params, headers=self.headers)
    #     print(f'P8接口{P8_SN}:----移动侦测灵敏度-中,时间:{str(datetime.now())}')
    #     time.sleep(P8_timeout)
    #
    #     # 移动侦测灵敏度-高
    #     sign_params = {
    #         "appkey": self.appkey,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"MotionDetectSensitivity":2}',
    #
    #     }
    #     params_to_be_signed = dict(sign_params)
    #     new_params = self.lower_key_in_params(params_to_be_signed)
    #     params = self.build_sign(new_params)
    #     params1 = params + "&" + self.appsecret
    #     replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
    #     after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
    #                                    lambda m: replacements[m.group()], params1)
    #     sign = self.md5value(after_replace_params1)
    #     post_params = {
    #         "appkey": self.appkey,
    #         "sign": sign,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"MotionDetectSensitivity":2}',
    #     }
    #     requests.post(self.url, data=post_params, headers=self.headers)
    #     print(f'P8接口{P8_SN}:----移动侦测灵敏度-高,时间:{str(datetime.now())}')
    #     time.sleep(P8_timeout)
    #
    #     # 红外夜视
    #     sign_params = {
    #         "appkey": self.appkey,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"Nightvision":0}',
    #
    #     }
    #     params_to_be_signed = dict(sign_params)
    #     new_params = self.lower_key_in_params(params_to_be_signed)
    #     params = self.build_sign(new_params)
    #     params1 = params + "&" + self.appsecret
    #     replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
    #     after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
    #                                    lambda m: replacements[m.group()], params1)
    #     sign = self.md5value(after_replace_params1)
    #     post_params = {
    #         "appkey": self.appkey,
    #         "sign": sign,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"Nightvision":0}',
    #     }
    #     requests.post(self.url, data=post_params, headers=self.headers)
    #     print(f'P8接口{P8_SN}:----红外夜视-关,时间:{str(datetime.now())}')
    #     time.sleep(P8_timeout)
    #
    #     # 红外夜视
    #     sign_params = {
    #         "appkey": self.appkey,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"Nightvision":1}',
    #
    #     }
    #     params_to_be_signed = dict(sign_params)
    #     new_params = self.lower_key_in_params(params_to_be_signed)
    #     params = self.build_sign(new_params)
    #     params1 = params + "&" + self.appsecret
    #     replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
    #     after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
    #                                    lambda m: replacements[m.group()], params1)
    #     sign = self.md5value(after_replace_params1)
    #     post_params = {
    #         "appkey": self.appkey,
    #         "sign": sign,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"Nightvision":1}',
    #     }
    #     requests.post(self.url, data=post_params, headers=self.headers)
    #     print(f'P8接口{P8_SN}:----红外夜视-开,时间:{str(datetime.now())}')
    #     time.sleep(P8_timeout)
    #
    #     # 提示音
    #     sign_params = {
    #         "appkey": self.appkey,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"PromptVolume":0}',
    #
    #     }
    #     params_to_be_signed = dict(sign_params)
    #     new_params = self.lower_key_in_params(params_to_be_signed)
    #     params = self.build_sign(new_params)
    #     params1 = params + "&" + self.appsecret
    #     replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
    #     after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
    #                                    lambda m: replacements[m.group()], params1)
    #     sign = self.md5value(after_replace_params1)
    #     post_params = {
    #         "appkey": self.appkey,
    #         "sign": sign,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"PromptVolume":0}',
    #     }
    #     requests.post(self.url, data=post_params, headers=self.headers)
    #     print(f'P8接口{P8_SN}:----提示音量-0,时间:{str(datetime.now())}')
    #     time.sleep(P8_timeout)
    #
    #     # 提示音
    #     sign_params = {
    #         "appkey": self.appkey,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"PromptVolume":50}',
    #
    #     }
    #     params_to_be_signed = dict(sign_params)
    #     new_params = self.lower_key_in_params(params_to_be_signed)
    #     params = self.build_sign(new_params)
    #     params1 = params + "&" + self.appsecret
    #     replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
    #     after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
    #                                    lambda m: replacements[m.group()], params1)
    #     sign = self.md5value(after_replace_params1)
    #     post_params = {
    #         "appkey": self.appkey,
    #         "sign": sign,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"PromptVolume":50}',
    #     }
    #     requests.post(self.url, data=post_params, headers=self.headers)
    #     print(f'P8接口{P8_SN}:----提示音量-50,时间:{str(datetime.now())}')
    #     time.sleep(P8_timeout)
    #
    #     # 提示音
    #     sign_params = {
    #         "appkey": self.appkey,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"PromptVolume":100}',
    #
    #     }
    #     params_to_be_signed = dict(sign_params)
    #     new_params = self.lower_key_in_params(params_to_be_signed)
    #     params = self.build_sign(new_params)
    #     params1 = params + "&" + self.appsecret
    #     replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
    #     after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
    #                                    lambda m: replacements[m.group()], params1)
    #     sign = self.md5value(after_replace_params1)
    #     post_params = {
    #         "appkey": self.appkey,
    #         "sign": sign,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"PromptVolume":100}',
    #     }
    #     requests.post(self.url, data=post_params, headers=self.headers)
    #     print(f'P8接口{P8_SN}:----提示音量-100,时间:{str(datetime.now())}')
    #     time.sleep(P8_timeout)
    #
    #     # 巡航 关
    #     sign_params = {
    #         "appkey": self.appkey,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"PtzCruiseSwitch":true}',
    #
    #     }
    #     params_to_be_signed = dict(sign_params)
    #     new_params = self.lower_key_in_params(params_to_be_signed)
    #     params = self.build_sign(new_params)
    #     params1 = params + "&" + self.appsecret
    #     replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
    #     after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
    #                                    lambda m: replacements[m.group()], params1)
    #     sign = self.md5value(after_replace_params1)
    #     post_params = {
    #         "appkey": self.appkey,
    #         "sign": sign,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"PtzCruiseSwitch":true}',
    #     }
    #     requests.post(self.url, data=post_params, headers=self.headers)
    #     print(f'P8接口{P8_SN}:----巡航-开,时间:{str(datetime.now())}')
    #     time.sleep(P8_timeout)
    #
    #     # 巡航 关
    #     sign_params = {
    #         "appkey": self.appkey,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"PtzCruiseSwitch":false}',
    #
    #     }
    #     params_to_be_signed = dict(sign_params)
    #     new_params = self.lower_key_in_params(params_to_be_signed)
    #     params = self.build_sign(new_params)
    #     params1 = params + "&" + self.appsecret
    #     replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
    #     after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
    #                                    lambda m: replacements[m.group()], params1)
    #     sign = self.md5value(after_replace_params1)
    #     post_params = {
    #         "appkey": self.appkey,
    #         "sign": sign,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"PtzCruiseSwitch":false}',
    #     }
    #     requests.post(self.url, data=post_params, headers=self.headers)
    #     print(f'P8接口{P8_SN}:----巡航-开,时间:{str(datetime.now())}')
    #     time.sleep(P8_timeout)
    #
    #     # 自动追踪
    #     sign_params = {
    #         "appkey": self.appkey,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"PtzMotionTracking":true}',
    #
    #     }
    #     params_to_be_signed = dict(sign_params)
    #     new_params = self.lower_key_in_params(params_to_be_signed)
    #     params = self.build_sign(new_params)
    #     params1 = params + "&" + self.appsecret
    #     replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
    #     after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
    #                                    lambda m: replacements[m.group()], params1)
    #     sign = self.md5value(after_replace_params1)
    #     post_params = {
    #         "appkey": self.appkey,
    #         "sign": sign,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"PtzMotionTracking":true}',
    #     }
    #     requests.post(self.url, data=post_params, headers=self.headers)
    #     print(f'P8接口{P8_SN}:----自动追踪-开,时间:{str(datetime.now())}')
    #     time.sleep(P8_timeout)
    #
    #     # 自动追踪
    #     sign_params = {
    #         "appkey": self.appkey,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"PtzMotionTracking":false}',
    #
    #     }
    #     params_to_be_signed = dict(sign_params)
    #     new_params = self.lower_key_in_params(params_to_be_signed)
    #     params = self.build_sign(new_params)
    #     params1 = params + "&" + self.appsecret
    #     replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
    #     after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
    #                                    lambda m: replacements[m.group()], params1)
    #     sign = self.md5value(after_replace_params1)
    #     post_params = {
    #         "appkey": self.appkey,
    #         "sign": sign,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"PtzMotionTracking":false}',
    #     }
    #     requests.post(self.url, data=post_params, headers=self.headers)
    #     print(f'P8接口{P8_SN}:----自动追踪-关,时间:{str(datetime.now())}')
    #     time.sleep(P8_timeout)
    #
    #     # 开关
    #     sign_params = {
    #         "appkey": self.appkey,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"Switch":false}',
    #
    #     }
    #     params_to_be_signed = dict(sign_params)
    #     new_params = self.lower_key_in_params(params_to_be_signed)
    #     params = self.build_sign(new_params)
    #     params1 = params + "&" + self.appsecret
    #     replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
    #     after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
    #                                    lambda m: replacements[m.group()], params1)
    #     sign = self.md5value(after_replace_params1)
    #     post_params = {
    #         "appkey": self.appkey,
    #         "sign": sign,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"Switch":false}',
    #     }
    #     requests.post(self.url, data=post_params, headers=self.headers)
    #     print(f'P8接口{P8_SN}:----开关-关,时间:{str(datetime.now())}')
    #     time.sleep(P8_timeout)
    #
    #     sign_params = {
    #         "appkey": self.appkey,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"Switch":true}',
    #
    #     }
    #     params_to_be_signed = dict(sign_params)
    #     new_params = self.lower_key_in_params(params_to_be_signed)
    #     params = self.build_sign(new_params)
    #     params1 = params + "&" + self.appsecret
    #     replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
    #     after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
    #                                    lambda m: replacements[m.group()], params1)
    #     sign = self.md5value(after_replace_params1)
    #     post_params = {
    #         "appkey": self.appkey,
    #         "sign": sign,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"Switch":true}',
    #     }
    #     requests.post(self.url, data=post_params, headers=self.headers)
    #     print(f'P8接口{P8_SN}:----开关-开,时间:{str(datetime.now())}')
    #     time.sleep(P8_timeout)
    #
    #     # 双工童话音量 0
    #     sign_params = {
    #         "appkey": self.appkey,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"TalkingVolume":0}',
    #
    #     }
    #     params_to_be_signed = dict(sign_params)
    #     new_params = self.lower_key_in_params(params_to_be_signed)
    #     params = self.build_sign(new_params)
    #     params1 = params + "&" + self.appsecret
    #     replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
    #     after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
    #                                    lambda m: replacements[m.group()], params1)
    #     sign = self.md5value(after_replace_params1)
    #     post_params = {
    #         "appkey": self.appkey,
    #         "sign": sign,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"TalkingVolume":0}',
    #     }
    #     requests.post(self.url, data=post_params, headers=self.headers)
    #     print(f'P8接口{P8_SN}:----双工通话音量-0,时间:{str(datetime.now())}')
    #     time.sleep(P8_timeout)
    #
    #     # 双工童话音量 0
    #     sign_params = {
    #         "appkey": self.appkey,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"TalkingVolume":50}',
    #
    #     }
    #     params_to_be_signed = dict(sign_params)
    #     new_params = self.lower_key_in_params(params_to_be_signed)
    #     params = self.build_sign(new_params)
    #     params1 = params + "&" + self.appsecret
    #     replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
    #     after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
    #                                    lambda m: replacements[m.group()], params1)
    #     sign = self.md5value(after_replace_params1)
    #     post_params = {
    #         "appkey": self.appkey,
    #         "sign": sign,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"TalkingVolume":50}',
    #     }
    #     requests.post(self.url, data=post_params, headers=self.headers)
    #     print(f'P8接口{P8_SN}:----双工通话音量-50,时间:{str(datetime.now())}')
    #     time.sleep(P8_timeout)
    #
    #     # 双工童话音量 0
    #     sign_params = {
    #         "appkey": self.appkey,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"TalkingVolume":100}',
    #
    #     }
    #     params_to_be_signed = dict(sign_params)
    #     new_params = self.lower_key_in_params(params_to_be_signed)
    #     params = self.build_sign(new_params)
    #     params1 = params + "&" + self.appsecret
    #     replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
    #     after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
    #                                    lambda m: replacements[m.group()], params1)
    #     sign = self.md5value(after_replace_params1)
    #     post_params = {
    #         "appkey": self.appkey,
    #         "sign": sign,
    #         "nonce": self.nonce,
    #         "r": int(time.time()),
    #         "ver": "1.0",
    #         "product_key": "2b7e7feff233",
    #         "device_name": P8_SN,
    #         "items": '{"TalkingVolume":100}',
    #     }
    #     requests.post(self.url, data=post_params, headers=self.headers)
    #     print(f'P8接口{P8_SN}:----双工通话音量-100,时间:{str(datetime.now())}')
    #     time.sleep(P8_timeout)

    # def start(self):
    #     for P8_SN in P8_SN_list:
    #         t = threading.Thread(target=self.CustomCallIndicator_true, args=(P8_SN,))
    #         t.start()




AIC =AIC()
AIC.start1()




