import threading
import serial #导入模块
import time
from datetime import datetime
Serial_num = 'COM36'
Serial__POWER_num = 'COM33'
class AIC():
    def __init__(self):
        self.ser1 = None
        self.ser =None

    def Power(self):
        portx = Serial__POWER_num
        bps = 9600
        timex = None
        self.ser1 = serial.Serial(portx, bps, timeout=timex)
        # ser.write('\r'.encode("utf-8"))
        # ser.write(bytes.fromhex('AE 20 01 28 02 01 01 AC'))  # 16进制 1路开.
        # ser.write(bytes.fromhex('AE 20 01 28 02 01 00 AC'))  # 16进制 1路关.
        self.ser1.write(bytes.fromhex('AE 20 01 29 03 FF FF 00 AC'))  # 16进制 总开关 全开.
        print(f'Power------串口链接成功,{str(datetime.now())}')
        # self.ser1.write(bytes.fromhex('AE 20 01 29 03 FF 00 00 AC'))  # 16进制 总开关 全关.

    def Power_On(self):
        self.ser1.write(bytes.fromhex('AE 20 01 28 02 01 01 AC'))  # 16进制 1路开.
        print(f'Power------1闸开启,{str(datetime.now())}')
    def Power_Off(self):
        self.ser1.write(bytes.fromhex('AE 20 01 28 02 01 00 AC'))  # 16进制 1路关
        print(f'Power------1闸关闭,{str(datetime.now())}')
    def P8_Serial(self):
        try:
            portx = Serial_num
            bps = 115200
            timex = None
            self.ser = serial.Serial(portx, bps, timeout=timex)
            print(f'P8串口:----链接串口成功,{str(datetime.now())}')
            while True:
                if self.ser.in_waiting:
                    c5 = self.ser.readline().decode(encoding='UTF-8', errors='ignore')
                    if (c5 == "exit"):  # 退出标志
                        break
                    else:
                        # print(c5)
                        # print('open')
                        with open('P8_硬重启.log', 'a', encoding='UTF-8', errors='ignore') as log:
                            log.writelines(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' ' + c5)
                        if 'Out of memory' in c5:
                            print(f'P8固件:------崩溃OOM,{str(datetime.now())}')
                            # self.Serial_send()
                        if 'soc-nna version is H20211130' in c5:
                            print(f'P8固件:------重启结束!,{str(datetime.now())}')
                            self.Serial_password()
                            self.Cat_online()
                        if 'U-Boot SPL 2013.07' in c5:
                            print(f'P8固件:------固件打印重启了,{str(datetime.now())}')
                        if 'Connect To Cloud: ' in c5:
                            print(f'P8固件:------联网成功,时间:{str(datetime.now())}')
                            # time_New  = c5.split('Connect To Cloud: ',1)[-1]
                            # print(time_New)
                        if 'cat: can' in c5:
                            print(f'P8固件:------联网fail,时间:{datetime.now()}')
                            self.Cat_iscm()
            self.ser.close()  # 关闭串口
        except Exception as e:
            print("---异常---：", e)
            pass

    def Serial_password(self):

        self.ser.write("\r".encode("utf-8"))
        self.ser.write("\r".encode("utf-8"))
        time.sleep(0.1)
        self.ser.write('root'.encode("utf-8"))
        time.sleep(0.1)
        self.ser.write("\r".encode("utf-8"))
        time.sleep(0.1)
        self.ser.write('iot_ipc@360'.encode("utf-8"))
        time.sleep(0.1)
        self.ser.write("\r".encode("utf-8"))

    def Cat_online(self):
        time.sleep(15)
        self.ser.write("\r".encode("utf-8"))
        time.sleep(0.1)
        self.ser.write('cat /tmp/online.log'.encode("utf-8"))
        time.sleep(0.1)
        self.ser.write("\r".encode("utf-8"))

    def Cat_iscm(self):
        self.ser.write("\r".encode("utf-8"))
        time.sleep(0.1)
        self.ser.write('cat /mnt/ext/ipcam.log')
        time.sleep(0.1)
        self.ser.write("\r".encode("utf-8"))

AIC =AIC()
t1 = threading.Thread(target=AIC.Power)
t1.start()
t2 = threading.Thread(target=AIC.P8_Serial)
t2.start()
time.sleep(5)
i= 0
while True:
    i +=1
    print(f'\n========================={i},时间:{str(datetime.now())}==========')
    AIC.Power_Off()
    time.sleep(10)
    AIC.Power_On()
    time.sleep(60)

