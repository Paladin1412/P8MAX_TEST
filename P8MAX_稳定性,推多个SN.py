# -*- coding: utf-8 -*-
# @Time : 2022/10/14 11:40
# @Author : 能飞会打智勇双全的才高八斗
# @File : cloud_services.py
# -*- coding: utf-8 -*-
import re
import threading
import requests
from datetime import datetime
import hashlib
import time
import random
import urllib.parse
P8_timeout = float(1)
P8_SN_list = ['86XCP8M12370000049','P8MAX_12','86XCP8M12370000011','86XCP8M12370000049','86XCP8M12370000017','86XCP8M12370000005','86XCP8M12370000032','86XCP8M12370000051','86XCP8M12370000043']
setProperty = ['{"TalkingVolume":100}', '{"TalkingVolume":50}', '{"TalkingVolume":0}',
               '{"Switch":false}', '{"Switch":true}', '{"PtzMotionTracking":true}','{"PtzMotionTracking":false}',
               '{"PtzCruiseSwitch":true}','{"PtzCruiseSwitch":false}',  '{"PromptVolume":0}', '{"PromptVolume":50}',
               '{"PromptVolume":100}', '{"Nightvision":1}', '{"Nightvision":0}', '{"MotionDetectSensitivity":0}',
               '{"MotionDetectSensitivity":1}', '{"MotionDetectSensitivity":2}', '{"MotionDetectSwitch":false}','{"MotionDetectSwitch":true}',
                '{"MicSwitch":false}','{"MicSwitch":true}',  '{"IpcWDRSwitch":true}',
               '{"IpcWDRSwitch":false}',  '{"IpcVoiceWatch":false}','{"IpcVoiceWatch":true}',
               '{"IpcVoiceUpgrade":false}','IpcVoiceUpgrade":true}', '{"IpcMuteRecord":true}', '{"IpcMuteRecord":false}', '{"Indicator":false}','{"Indicator":true}',
                '{"ImageFlip":1}', '{"ImageFlip":2}', '{"DeviceVolume":0}', '{"DeviceVolume":50}',
               '{"DeviceVolume":100}', '{"DetectSensitivity":0}', '{"DetectSensitivity":1}', '{"DetectSensitivity":2}',
               '{"DetectionSwitch":false}','{"DetectionSwitch":true}',
               '{"CustomCallIndicator":false}','{"CustomCallIndicator":true}', '{"ClarityMode":1}', '{"ClarityMode":2}', '{"ClarityMode":5}', ]


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
            time.sleep(P8_timeout)
            for P8_SN in P8_SN_list:
                t = threading.Thread(target=self.CustomCallIndicator_true1, args=(P8_SN, SetProperty_ID))
                t.start()
            print('==============================================================')

AIC =AIC()
i =0






while True:
    try:
        i+= 1
        print(f'\n===================={i}=================,{datetime.now()}')
        AIC.start1()
        time.sleep(60)
    except:pass

# while True:
#
#     time.sleep(70)