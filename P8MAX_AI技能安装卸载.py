# -*- coding: utf-8 -*- 
# @Time : 2022/8/23 15:06 
# @Author : 能飞会打智勇双全的才高八斗  test git
# @File : P8MAX_AI技能安装卸载.py
import threading
import serial #导入模块
import time
import requests
from datetime import datetime
Serial_num = 'COM32'
Trigger_interval = int(15)  # 任务间隔
Version_1_0_0 = 'P8Max宠物检测","skill_version":"1.0.0'
Version_1_0_1 = 'P8Max宠物检测","skill_version":"1.0.1' # e32a57e00572a40305de143d055499b5
Version_1_0_2 = 'P8Max宠物检测","skill_version":"1.0.2' # f97c2424171c20c5b1a9a9c57bafa13b # 67cda443e363b431333c233c92bf9784
Version_1_0_3 = ''  # 升级不了
Version_1_0_4 = 'P8Max宠物检测","skill_version":"1.0.4'
Version_1_0_5 = 'P8Max宠物检测","skill_version":"1.0.5'
Version_1_0_0_list = []
Version_1_0_1_list = []
Version_1_0_2_list = []
Version_1_0_3_list = []  # 升级不了
Version_1_0_4_list = []
Version_1_0_5_list = []
class AIlab_Install_Uninstall():
    def __init__(self):    # 让类里面的每个方法都能调用
        self.ser = None
        self.P8_cookie = '__huid=11vFyP6NQw3FKByy0lAW+6X+J0eI7KE5mlwGcdDdmaoHY=; bad_id73963b90-5cf1-11e9-9a78-b1dd2463a67d=adc4dee2-0409-11ec-b729-6987cce1077a; __gid=210553756.110165219.1629720015257.1639621893533.11; __guid=192758817.4361071964550641700.1655103420048.7302; Qs_lvt_369019=1658801133%2C1658892453%2C1659492684%2C1660706582%2C1660806369; online_ticket=OT-4ce15ddd-6f91-4b84-bd54-aa87cffb5e2d; Qs_pv_369019=4222360418775880700%2C1564559482436133600%2C4148260640837654000%2C3732652553618712600%2C4216067718312037000; Q=u%3D360H3293566442%26n%3D%26le%3D%26m%3DZGtjWGWOWGWOWGWOWGWOWGWOAwL0%26qid%3D3293566442%26im%3D1_t01a6d072182d68691c%26src%3D360chrome_weixin%26t%3D1; T=s%3D797f1805d0356dea7d725fae5fe817c9%26t%3D1660527054%26lm%3D%26lf%3D%26sk%3D47b5c9105aacd085dd62276876e39d8c%26mt%3D1660527054%26rc%3D%26v%3D2.0%26a%3D1; hasShowLiving=1; __DC_monitor_count=22; __DC_sid=123679891.2168691254899934700.1662105221651.0862; IOT_MOCK=; __DC_gid=264109457.602706629.1629184391927.1662105840531.7838'
        self.url = 'https://iot.zyun.360.cn/iot/api/common/device/invokeService'
        self.P8_cookies ={
            'Content-Type': 'application/json',
            'cookie': self.P8_cookie
        }
    # 安装宠物技能1.0.0
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

    # 更新宠物技能 从1.0.0 升级到1.0.4
    def P8_Upgrade_0(self):
        P8_body_Uninstall = {
            'corp_id': "212",
            'device_name': "P8MAX_09",
            'identifier': "AiLabAction",
            'input_data': '{"Action":"Upgrade","SkillId":"627011944199475200","SkillVersion":"1.0.0"}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland",
        }
        print(f'P8接口:----技能触发更新1.0.0,{str(datetime.now())}')
        aa = requests.post(url=self.url, json=P8_body_Uninstall, headers=self.P8_cookies).json()  # Install

    def P8_Upgrade_1(self):
        P8_body_Uninstall = {
            'corp_id': "212",
            'device_name': "P8MAX_09",
            'identifier': "AiLabAction",
            'input_data': '{"Action":"Upgrade","SkillId":"627011944199475200","SkillVersion":"1.0.1"}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland",
        }
        print(f'P8接口:----技能触发更新1.0.1,时间:{str(datetime.now())}')
        aa = requests.post(url=self.url, json=P8_body_Uninstall, headers=self.P8_cookies).json()  # Install

    def P8_Upgrade_2(self):
        P8_body_Uninstall = {
            'corp_id': "212",
            'device_name': "P8MAX_09",
            'identifier': "AiLabAction",
            'input_data': '{"Action":"Upgrade","SkillId":"627011944199475200","SkillVersion":"1.0.2"}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland",
        }
        print(f'P8接口:----技能触发更新1.0.2,时间:{str(datetime.now())}')
        aa = requests.post(url=self.url, json=P8_body_Uninstall, headers=self.P8_cookies).json()  # Install

    def P8_Upgrade_3(self):
        P8_body_Uninstall = {
            'corp_id': "212",
            'device_name': "P8MAX_09",
            'identifier': "AiLabAction",
            'input_data': '{"Action":"Upgrade","SkillId":"627011944199475200","SkillVersion":"1.0.3"}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland",
        }
        print(f'P8接口:----技能触发更新1.0.3,时间:{str(datetime.now())}')
        aa = requests.post(url=self.url, json=P8_body_Uninstall, headers=self.P8_cookies).json()  # Install

    def P8_Upgrade_4(self):
        P8_body_Uninstall = {
            'corp_id': "212",
            'device_name': "P8MAX_09",
            'identifier': "AiLabAction",
            'input_data': '{"Action":"Upgrade","SkillId":"627011944199475200","SkillVersion":"1.0.4"}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland",
        }
        print(f'P8接口:----技能触发更新1.0.4,时间:{str(datetime.now())}')
        aa = requests.post(url=self.url, json=P8_body_Uninstall, headers=self.P8_cookies).json()  # Install

    # 卸载宠物技能 1.0.4
    def P8_Uninstall(self):
        P8_body_Uninstall = {
            'corp_id': "212",
            'device_name': "P8MAX_09",
            'identifier': "AiLabAction",
            'input_data': '{"Action":"Uninstall","SkillId":"627011944199475200","SkillVersion":"1.0.4"}',
            'product_key': "2b7e7feff233",
            'seasAndInDomain': "inland",
        }
        print(f'P8接口:----技能触发卸载,时间:{str(datetime.now())}')
        aa = requests.post(url=self.url, json=P8_body_Uninstall, headers=self.P8_cookies).json()  # Install

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
                        with open('P8_技能更新log.log', 'a', encoding='UTF-8', errors='ignore') as log:
                            log.writelines(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' ' + c5)
                        if 'qai_iot_srvcall_handle {' in c5:
                            if 'Uninstall' in c5:
                                print(f'P8固件:------技能触发卸载,{str(datetime.now())}')
                                self.Status()
                            if 'Install' in c5:
                                print(f'P8固件:------技能触发安装,{str(datetime.now())}')
                                self.Status()
                            if 'Update' in c5:
                                print(f'P8固件:------技能触发修改,{str(datetime.now())}')
                                self.Status()
                            # if 'Upgrade' in c5:
                            #     print(f'P8固件:------技能触发更新,{str(datetime.now())}')
                            #     self.demsg()
                            if 'SkillVersion":"1.0.0' in c5:
                                print(f'P8固件:------技能触发更新1.0.0,{str(datetime.now())}')
                                self.Status()
                            if 'SkillVersion":"1.0.1' in c5:
                                print(f'P8固件:------技能触发更新1.0.1,{str(datetime.now())}')
                                self.Status()
                            if 'SkillVersion":"1.0.2' in c5:
                                print(f'P8固件:------技能触发更新1.0.2,{str(datetime.now())}')
                                self.Status()
                            if 'SkillVersion":"1.0.4' in c5:
                                print(f'P8固件:------技能触发更新1.0.4,{str(datetime.now())}')
                                self.Status()
                        if 'qai_iot_srvcall_handle ok' in c5:
                            print(f'P8固件:------技能触发更新 OK,{str(datetime.now())}')
                            self.Status()
                        if 'Out of memory' in c5:
                            print(f'P8固件:------崩溃OOM,{str(datetime.now())}')
                            # self.Serial_send()
                        if 'RUN SDIO' in c5:
                            print(f'P8固件:------重启了!,{str(datetime.now())}')
                            self.Serial_send()
                        if 'CPU: 0 PID' in c5:
                            print(f'P8固件:------可能异常崩溃OOM了,{str(datetime.now())}')
                        if 'install_state":1,"schema' in c5:
                            if Version_1_0_0 in c5:
                                Version_1_0_0_list.append(c5)
                                print(f'P8固件校验:------校验config,触发数量{len(Version_1_0_0_list)},确认技能版本为1.0.0,时间:{str(datetime.now())}\n')
                            if Version_1_0_1 in c5:
                                Version_1_0_1_list.append(c5)
                                print(f'P8固件校验:------校验config,触发数量{len(Version_1_0_1_list)},确认技能版本为1.0.1,时间:{str(datetime.now())}\n')
                            if Version_1_0_2 in c5:
                                Version_1_0_2_list.append(c5)
                                print(f'P8固件校验:------校验config,触发数量{len(Version_1_0_2_list)},确认技能版本为1.0.2,时间:{str(datetime.now())}\n')
                                # if Version_1_0_3 in c5:
                                #     Version_1_0_3_list.append(c5)
                                #     print(f'P8固件校验:------校验configMD5,触发数量{len(Version_1_0_3_list)},确认技能版本为1.0.3,时间:{str(datetime.now())}')
                            if Version_1_0_4 in c5:
                                Version_1_0_4_list.append(c5)
                                print(f'P8固件校验:------校验config,触发数量{len(Version_1_0_4_list)},确认技能版本为1.0.4,时间:{str(datetime.now())},\n')
                            if Version_1_0_5 in c5:
                                Version_1_0_5_list.append(c5)
                                print(f'P8固件校验:------校验config,触发数量{len(Version_1_0_5_list)},确认技能版本为1.0.4,时间:{str(datetime.now())},\n')
                        # if 'MemAvailable' in c5:  # 低于3M会崩溃
                        #     print(f'P8固件:----内存：{c5}')
            # print('超时退出')
            self.ser.close()  # 关闭串口
        except Exception as e:
            print("---异常---：", e)
            pass

    def Serial_send(self):
        # print('开启日志')
        time.sleep(60)
        self.ser.write("\r".encode("utf-8"))
        time.sleep(0.1)
        self.ser.write('root'.encode("utf-8"))
        time.sleep(0.1)
        self.ser.write("\r".encode("utf-8"))
        time.sleep(0.1)
        self.ser.write('iot_ipc@360'.encode("utf-8"))
        time.sleep(0.1)
        self.ser.write("\r".encode("utf-8"))
        # time.sleep(5)
        # self.ser.write('watchdog &'.encode("utf-8"))
        # time.sleep(0.1)
        # self.ser.write("\r".encode("utf-8"))
        # print(f'P8固件:------发送watchdog &成功,再次等待15s,{str(datetime.now())}')
        time.sleep(15)

    def Serial_meminfo(self):
        self.ser.write("\r".encode("utf-8"))
        time.sleep(0.1)
        self.ser.write('cat /proc/meminfo\r'.encode("utf-8"))
        time.sleep(0.1)

    def demsg(self):
        self.ser.write("\r".encode("utf-8"))
        time.sleep(0.1)
        self.ser.write('cat /proc/meminfo'.encode("utf-8"))
        time.sleep(0.1)
        self.ser.write("\r".encode("utf-8"))
        time.sleep(0.1)
        self.ser.write('top -n 1'.encode("utf-8"))
        time.sleep(0.1)
        self.ser.write("\r".encode("utf-8"))
        time.sleep(2)
        self.ser.write(chr(0x03).encode("utf-8"))

    def Serial_Install_config(self):
        # self.ser.write("\r".encode("utf-8"))
        # time.sleep(0.1)
        # self.ser.write('md5sum /data/plugin/627011944199475200/config.json\r'.encode("utf-8"))
        # time.sleep(0.1)
        self.ser.write("\r".encode("utf-8"))
        time.sleep(0.1)
        self.ser.write('cat /data/plugin/627011944199475200/config.json\r'.encode("utf-8"))
        time.sleep(0.1)
        self.ser.write("\r".encode("utf-8"))

    def Kill_ipcam(self):
        self.ser.write("\r".encode("utf-8"))
        time.sleep(0.1)
        self.ser.write('killall tail\r'.encode("utf-8"))
        time.sleep(0.1)
        self.ser.write("\r".encode("utf-8"))
        time.sleep(0.1)
        self.ser.write('tail -f /mnt/ext/ipcam.log &\r'.encode("utf-8"))
        time.sleep(0.1)
        self.ser.write("\r".encode("utf-8"))

    def Status(self):
        self.ser.write("\r".encode("utf-8"))
        time.sleep(0.1)
        self.ser.write('status\r'.encode("utf-8"))
        time.sleep(0.1)
        self.ser.write("\r".encode("utf-8"))
        time.sleep(0.1)
        self.ser.write('top -n 1'.encode("utf-8"))
        time.sleep(0.1)
        self.ser.write("\r".encode("utf-8"))

AIC =AIlab_Install_Uninstall()
# AIC.P8_Upgrade_0()
# AIC.P8_Upgrade_1()
i = 0
t1 = threading.Thread(target=AIC.P8_Serial)

t1.start()
time.sleep(5)
# # AIC.P8_Upgrade_1()
# # time.sleep(15)
# # AIC.Serial_Install_md5sum()
# AIC.Serial_send()


#
while i <= 2000:
    i += 1
    print(f'\n===================={i}=================,{datetime.now()}')
    AIC.Kill_ipcam()
    time.sleep(3)
    AIC.P8_Upgrade_0()
    AIC.Status()
    time.sleep(Trigger_interval)
    AIC.Status()
    AIC.Serial_Install_config()
    AIC.Status()
    time.sleep(Trigger_interval)
    AIC.Status()
    # AIC.P8_Upgrade_1()  # 7bdc986ee2d6598cb9b816437f7c54eb
    # time.sleep(Trigger_interval)
    # AIC.Serial_Install_config()
    # time.sleep(5)
    # AIC.P8_Upgrade_2()  # f97c2424171c20c5b1a9a9c57bafa13b
    # time.sleep(Trigger_interval)
    # AIC.Serial_Install_config()
    # time.sleep(5)
    # AIC.P8_Upgrade_3() # 升不上去
    AIC.P8_Upgrade_4()  # 5976c2c988efa3199b4a287c8cee8996
    AIC.Status()
    time.sleep(Trigger_interval)
    AIC.Status()
    AIC.Serial_Install_config()
    AIC.Status()
    time.sleep(Trigger_interval)
    AIC.Status()