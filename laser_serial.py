import serial
import struct
import numpy as np
# 打开串口
ser = serial.Serial('COM3', 115200, timeout=1)

# 创建数组用于存储数据
data_list = []
j = 0
a_d = np.zeros((360, 1), dtype=int)
# 读取串口内容
while True:
    # 读取一个字节
    byte = ser.read()

    # 判断是否为0x05
    if byte == b'\xAA':
        # 读取后续的个字节
        byte1 = ser.read(1)
        if byte1 == b'\x55':
            CT = ser.read(1)
            LSN = ser.read(1)
            FSA_L = ser.read(1)
            FSA_H = ser.read(1)
            LSA_L = ser.read(1)
            LSA_H = ser.read(1)
            CHECK = ser.read(2)
            Number = ord(LSN)
            DATA = ser.read(Number*2)
        # 将数据存入数组
            data_list.extend(DATA)
            b = []
            for i in range(len(data_list)):
                b.append(np.array(data_list[i]))
            data_array = np.array(b)
            FSA = (ord(FSA_H) * pow(2, 7) + ord(FSA_L) / 2)/64
            LSA = (ord(LSA_H) * pow(2, 7) + ord(LSA_L) / 2)/64
            angle_diff = LSA - FSA


            if angle_diff < 0:
                angle_diff = 360 + angle_diff
            if Number != 1:
                for i in range(Number):
                    d = (data_array[2*i+1] * pow(2, 8) + data_array[2*i])/4
                    angle = (angle_diff/(Number-1))*i+FSA
                    if d != 0:
                        angle_correct = np.degrees(np.arctan(21.8*(155.3-d)/(155.3*d)))
                    else:
                        angle_correct = 0
                    angle = angle + angle_correct
                    if angle >= 360:
                        angle = angle - 360
                    a_d[int(angle)] = d




        # 打印数据
        #(data_array)
        #print(FSA,LSA)

    data_list = []
    print(a_d)
# 关闭串口
ser.close()