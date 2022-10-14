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
import time
import random
import hashlib
import time
import random
import base64
import json
import urllib.parse
import csv


base_url = "http://cn-iot-api.iot.360.cn"      # openapi测试环境

api = "/device/setProperty"
url = base_url + api
print("请求url  ---> ", url)

appkey = "147cb0cea801c54f01c17cc40c8ccc4f"
appsecret = "137c49fb7c4799fbfa7d4715c2bd978c"
ver = "1.0"


def md5value(s):
    md5 = hashlib.md5()
    md5.update(s.encode("utf-8"))
    return md5.hexdigest()


#   六位唯一随机数
def generate_code(code_len=6):
    all_char = '0123456789qazwsxedcrfvtgbyhnujmikolpQAZWSXEDCRFVTGBYHNUJMIKOLP'
    index = len(all_char) - 1
    code = ''
    for _ in range(code_len):
        num = random.randint(0, index)
        code += all_char[num]
    return code


def signts():
    ts = int(time.time())
    return str(ts)


nonce = generate_code()
print("nonce ---> ", nonce)

r = signts()
print('r ---> ', r)

headers = {'Content-Type': 'application/x-www-form-urlencoded',
           'User-Agent': 'Go-http-client/1.1',
           }


sign_params = {
    "appkey": appkey,
    "nonce": nonce,
    "r": r,
    "ver": "1.0",
    "product_key": "2b7e7feff233",
    "device_name": "P8MAX_12",
    "items": '{"PromptVolume":30}',

}


params_to_be_signed = dict(sign_params)
print("params_to_be_signed ---> ", params_to_be_signed)


def lower_key_in_params(params_to_be_signed):
    new_params = {}
    for i, j in params_to_be_signed.items():
        new_params[i.lower()] = j
    #     print("j ---> ", j)
    # print("转换成小写的key ---> ", new_params)
    return new_params


def build_sign(new_params):
    temp_list = ''
    tmp_dict = lower_key_in_params(new_params)
    print("打印tmp_dict ---> {}".format(tmp_dict))
    print("打印tmp_dict.items() ---> {}".format(tmp_dict.items()))
    temp_list = sorted(tmp_dict.items(), key=lambda x: x[0], reverse=False)
    print("temp_list ---> ", temp_list)
    # 将参数名称和参数值分别进行 URL encoded 编码
    temp_list1 = urllib.parse.urlencode(temp_list)
    print("temp_list1 ---> ", temp_list1)
    return temp_list1


new_params = lower_key_in_params(params_to_be_signed)
print("待sign校验的参数转换成小写后的key ---> ", new_params)

params = build_sign(new_params)
print("按键从小到大排序后 ---> ", params)

params1 = params + "&" + appsecret
print("最终待做sign的参数 ---> ", params1)

"""
将params1中的+、*、%7E进行替换
加号+替换为%20
星号*替换为%2A
%7E替换为波浪号~
"""
replacements = {'+': '%20', '*': '%2A', '%7E': '~'}
after_replace_params1 = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))), lambda m: replacements[m.group()], params1)
print("替换后的字符串 ---> ", after_replace_params1)

sign = md5value(after_replace_params1)
print("sign的值 ---> ", sign)

publicParams = {
    "appkey": appkey,
    "sign": sign,
    "nonce": nonce,
    "r": r,
    "ver": "1.0"
}

post_params = {
    "appkey": appkey,
    "sign": sign,
    "nonce": nonce,
    "r": r,
    "ver": "1.0",
    "product_key": "2b7e7feff233",
    "device_name": "P8MAX_12",
    "items": '{"PromptVolume":30}',
}

payload = urllib.parse.urlencode(dict(publicParams))
print("payload  --->" + payload)

url1 = ''.join([url, payload])
print("拼接后的url--->", url1)

r = requests.post(url, data=post_params, headers=headers)




# r = requests.get(url, params=payload, headers=headers)
print(r.url)

response_data = r.text
print("response_data的类型是 ---> ", type(response_data))
print("请求的响应时间为%i毫秒" % (r.elapsed.total_seconds() * 1000) + "\n")

print("response_data ---> ", response_data)
print(json.dumps(response_data, ensure_ascii=False))

