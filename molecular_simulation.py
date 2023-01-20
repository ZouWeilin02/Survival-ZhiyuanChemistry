import os
import math
from numba import jit 
# import taichi as ti #需要自己安装，如果没装记得注释掉
import matplotlib.pyplot as plt
# import numpy as npy（雾
import numpy as np

import timeit
start=timeit.default_timer()
# 导入数据
file = open("water_273.trj")
water_data = file.readlines() 
# 确定常量，如果想多研究可以改成list然后遍历
sampling_density = 500
max_r = 10
hood_number = 100
dr = max_r / hood_number
# print(water_data[9])
# print(water_data[45099])
x_data = []
sample = []
for i in range(1001):
    if i % sampling_density == 0:
        sample.append(int(i))
for i in range(len(sample)):
    x_data.append(i)

print(sample[2])

# x_position_primary = []
# y_position_primary = []
# z_position_primary = []
x_position = []
y_position = []
z_position = []
# 获得初始帧的坐标位置
x_initial_position = []
y_initial_position = []
z_initial_position = []
for i in range(4500):
    x_initial_position.append(float(water_data[i + 9].split()[2]))
    y_initial_position.append(float(water_data[i + 9].split()[3]))
    z_initial_position.append(float(water_data[i + 9].split()[4]))


# 获得某一帧的坐标数据
def get_frame_data(n):
    first_atom_index = n * 4509 + 9
    for i in range(4500):
        x_position.append(float(water_data[first_atom_index + i].split()[2]))
        y_position.append(float(water_data[first_atom_index + i].split()[3]))
        z_position.append(float(water_data[first_atom_index + i].split()[4]))
    return x_position,y_position,z_position
# get_frame_data(0)
# get_frame_data(10)
# print(x_position[0],x_position[4500])
# print(y_position[0],y_position[4500])
# print(z_position[0],z_position[4500])

for sam in sample:
    get_frame_data(sam)


r_square = []
MSD_result = []

# def MSD_cal(x_position,y_position,z_position):
#     num = int(len(x_position) / 4500)
#     count = 0
#     for i in range(num):
#         for j in range(4500):
#             r_square.append(pow(x_position[4500* i + j]-x_initial_position[j],2)+pow(y_position[4500 * i + j]-y_initial_position[j],2)+pow(z_position[4500 * i + j]-z_initial_position[j],2))
#         for k in range(4500):
#             count += r_square[4500 * i + k]
#         MSD_result.append(float(count / 4500))
#         count = 0
#     return MSD_result

# MSD_cal(x_position=x_position,y_position=y_position,z_position=z_position)    
# print(MSD_result)
# print(len(MSD_result))
# # MSD绘图
# plt.plot(MSD_result)
# plt.show()

# print(len(x_initial_position))

print(max(x_initial_position),max(y_initial_position),max(z_initial_position))
print(min(x_initial_position),min(y_initial_position),min(z_initial_position))

distance = []
count = 0
RDF_count = [0] * hood_number
# @jit
def RDF_cal(x_position,y_positon,z_position,count):
    num = int(len(x_position) / 4500)
    r_distance = 0

    for i in range(num):
        for j in range(4500):
            for k in range(4500):
                if j != k:
                    # distance.append(math.sqrt(pow(x_position[4500* i + j]-x_position[4500 * i + k],2)+pow(y_position[4500 * i + j]-y_position[4500 * i + k],2)+pow(z_position[4500 * i + j]-z_position[4500 * i +k],2)))
                    r_distance = math.sqrt(pow(x_position[4500* i + j]-x_position[4500 * i + k],2)+pow(y_position[4500 * i + j] - y_position[4500 * i + k],2)+pow(z_position[4500 * i + j]-z_position[4500 * i +k],2))
                layer = int(r_distance // dr)
                if r_distance <= max_r:
                    RDF_count[layer] +=1
                    count +=1
    print(len(RDF_count))



RDF_cal(x_position=x_initial_position,y_positon=y_initial_position,z_position=z_initial_position,count=count)
# RDF_cal(x_position=x_position,y_positon=y_position,z_position=z_position)
volume = count / (4 * math.pi *pow(max_r,3) / 3)
for i in range(len(RDF_count)):
    RDF_count[i] /= (4/3 * math.pi *(pow((i+1)*dr,3)-pow(i*dr,3)) * volume)
RDF_count[hood_number-1] = 1

plt.plot(RDF_count)
plt.show()


# print(len(distance))
# print(distance[10])
# print(max(distance))
# for i in len(distance):




end=timeit.default_timer()
print('Running time: %s Seconds'%(end-start))

# print(x_initial_position[0])    
# print(x_position[0])
# print(len(x_position))
# # # def find_data():


