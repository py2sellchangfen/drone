#!/usr/bin/envpython 
# -*- coding: utf-8-*- 
"""
© Copyright2015-2016, 3D Robotics.
simple_goto.py:GUIDED mode "simple goto" example (Copter Only)
Demonstrates how toarm and takeoff in Copter and how to navigate to points usingVehicle.simple_goto.
""" 
from __future__ import print_function
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil


connection_string = '192.168.8.127:14550'
print('正在%s端口与飞行器链接' % connection_string)
# connect函数将会返回一个Vehicle类型的对象，即此处的vehicle
# 即可认为是无人机的主体，通过vehicle对象，我们可以直接控制无人机
vehicle = connect(connection_string, wait_ready= True)

# 定义arm_and_takeoff函数，使无人机解锁并起飞到目标高度 
# 参数aTargetAltitude即为目标高度，单位为米


def arm_and_takeoff(aTargetAltitude):
    # 进行起飞前检查
    print("起飞前检查")
    # vehicle.is_armable会检查飞控是否启动完成、有无GPS fix、卡曼滤波器
    # 是否初始化完毕。若检查通过，则会返回True
    while not vehicle.is_armable:
        print("飞行器初始化...")
        time.sleep(1)
    # 解锁无人机(电机将开始旋转)
    print("电机开始旋转")
    # 将无人机的飞行模式切换成"GUIDED"（一般建议在GUIDED模式下控制无人机） 
    vehicle.mode = VehicleMode("GUIDED")
    # 通过设置vehicle.armed状态变量为True，解锁无人机 
    vehicle.armed = True 
    # 在无人机起飞之前，确认电机已经解锁 
    while not vehicle.armed: 
        print(" Waiting for arming ...")
        time.sleep(1) 
    # 发送起飞指令
    print("Taking off!") 
    # simple_takeoff将发送指令，使无人机起飞并上升到目标高度 
    vehicle.simple_takeoff(aTargetAltitude)
    # 在无人机上升到目标高度之前，阻塞程序
    while True: 
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # 当高度上升到目标高度的0.95倍时，即认为达到了目标高度，退出循环 
        # vehicle.location.global_relative_frame.alt为相对于home点的高度
        if vehicle.location.global_relative_frame.alt>= aTargetAltitude * 0.95: 
            print("Reached target altitude")
            break 
        # 等待1s 
        time.sleep(1) 


arm_and_takeoff(10)
# 通过调用函数send_body_ned_velocity方法，可以实现不同方向的指定运动。


def send_body_ned_velocity(velocity_x, velocity_y, velocity_z, duration=0):
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,  # time_boot_ms(not used)
        0, 0,  # target system, target component
        mavutil.mavlink.MAV_FRAME_BODY_NED,  # frame Needs to be MAV_FRAME_BODY_NED for forward/back left/right control.
        0b0000111111000111,  # type_mask
        0, 0, 0,  # 坐标系里位置(not used)
        velocity_x, velocity_y, velocity_z,  # 单位米每秒
        0, 0, 0,  # x,y,z 加速度
        0, 0)
    for x in range(0, duration):
        vehicle.send_mavlink(msg)
        time.sleep(1)

# 起飞成功后，按照指令飞行


send_body_ned_velocity(0, -10, 0, 10)
time.sleep(10)
send_body_ned_velocity(10, 0, 0, 10)
time.sleep(10)
send_body_ned_velocity(0, 10, 0, 10)
time.sleep(10)
send_body_ned_velocity(-10, 0, 0, 10)
time.sleep(10)
# print("开始返航")
# vehicle.mode = VehicleMode("RTL")

print("Close vehicle object")
vehicle.close()
