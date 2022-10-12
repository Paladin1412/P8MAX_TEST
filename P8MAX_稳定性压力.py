# -*- coding: utf-8 -*- 
# @Time : 2022/10/12 19:51 
# @Author : 能飞会打智勇双全的才高八斗 
# @File : P8MAX_稳定性压力.py
import threading
import serial #导入模块
import time
import requests
from datetime import datetime

class AIC():
    def __init__(self):    # 让类里面的每个方法都能调用
        self.ser = None
        self.P8_cookie = '__huid=11vFyP6NQw3FKByy0lAW+6X+J0eI7KE5mlwGcdDdmaoHY=; bad_id73963b90-5cf1-11e9-9a78-b1dd2463a67d=adc4dee2-0409-11ec-b729-6987cce1077a; __gid=210553756.110165219.1629720015257.1639621893533.11; __guid=192758817.4361071964550641700.1655103420048.7302; Qs_lvt_369019=1658801133%2C1658892453%2C1659492684%2C1660706582%2C1660806369; online_ticket=OT-4ce15ddd-6f91-4b84-bd54-aa87cffb5e2d; Qs_pv_369019=4222360418775880700%2C1564559482436133600%2C4148260640837654000%2C3732652553618712600%2C4216067718312037000; Q=u%3D360H3293566442%26n%3D%26le%3D%26m%3DZGtjWGWOWGWOWGWOWGWOWGWOAwL0%26qid%3D3293566442%26im%3D1_t01a6d072182d68691c%26src%3D360chrome_weixin%26t%3D1; T=s%3D797f1805d0356dea7d725fae5fe817c9%26t%3D1660527054%26lm%3D%26lf%3D%26sk%3D47b5c9105aacd085dd62276876e39d8c%26mt%3D1660527054%26rc%3D%26v%3D2.0%26a%3D1; hasShowLiving=1; __DC_monitor_count=22; __DC_sid=123679891.2168691254899934700.1662105221651.0862; IOT_MOCK=; __DC_gid=264109457.602706629.1629184391927.1662105840531.7838'

        self.url = 'https://iot.zyun.360.cn/iot/api/common/device/invokeService'
        self.P8_cookies ={
            'Content-Type': 'application/json',
            'cookie': self.P8_cookie
        }

    def P8_Install(self):
        P8_body_Install = {
            'corp_id': "212",
            'device_name': "P8MAX_09",
            'identifier': "AiLabAction",
            'input_data': '{"Action":"Install","SkillId":"627011944199475200","SkillVersion":"1.0.0"}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland",
        }
        print(f'P8接口:----技能触发安装,时间:{str(datetime.now())}')
        aa =requests.post(url=self.url, json=P8_body_Install, headers=self.P8_cookies).json()  # Install
