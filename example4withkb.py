#!/usr/bin/envpython 
# -*- coding: utf-8-*- 
"""
© Copyright2015-2016, 3D Robotics.
simple_goto.py:GUIDED mode "simple goto" example (Copter Only)
Demonstrates how toarm and takeoff in Copter and how to navigate to points usingVehicle.simple_goto.
""" 
from __future__ import print_function
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative, Command, LocationGlobal
from pymavlink import mavutil
import Tkinter as tk


connection_string = 'udp:127.0.0.1:14551'
print('正在%s端口与飞行器链接' % connection_string)
# connect函数将会返回一个Vehicle类型的对象，即此处的vehicle
# 即可认为是无人机的主体，通过vehicle对象，我们可以直接控制无人机
vehicle = connect(connection_string, wait_ready=True)

# 设置飞行速度5m/s
gnd_speed = 5
# 定义arm_and_takeoff函数，使无人机解锁并起飞到目标高度 
# 参数aTargetAltitude即为目标高度，单位为米
def arm_and_takeoff(aTargetAltitude):
    # 进行起飞前检查
    print("起飞前检查")
    # vehicle.is_armable会检查飞控是否启动完成、有无GPS fix、卡曼滤波器
    # 是否初始化完毕。若以上检查通过，则会返回True
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

# 定义发送mavlink速度命令得功能

# 定义发送mavlink速度命令的功能
def set_velocity_body(vehicle, vx, vy, vz):
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,
        0, 0,
        mavutil.mavlink.MAV_FRAME_BODY_NED,
        0b0000111111000111,
        0, 0, 0,
        vx, vy, vz,
        0, 0, 0,
        0, 0)
    vehicle.send_mavlink(msg)
    vehicle.flush()

# 定义按键事件功能
def key(event):
    if event.char == event.keysym:  # 标准按键
        if event.keysym == 'r':
            print("r键按下>>设置返航模式")
            vehicle.mode = VehicleMode("RTL")
        elif event.keysym == 'l':
            print("l键按下>>设置着陆模式")
            vehicle.mode = VehicleMode("LAND")
    else:  # 非标准按键
        if event.keysym == 'Up':
            set_velocity_body(vehicle,gnd_speed, 0, 0)
        elif event.keysym == 'Down':
            set_velocity_body(vehicle, -gnd_speed, 0, 0)
        elif event.keysym == 'Left':
            set_velocity_body(vehicle, 0, -gnd_speed, 0)
        elif event.keysym == 'Right':
            set_velocity_body(vehicle, 0, gnd_speed, 0)

# 主程序
# 起飞，目标高度10米
arm_and_takeoff(10)

# 等待键盘输入
root = tk.Tk()
print(">>通过方向键控制无人机。按r键返航")
print(">>通过方向键控制无人机。按l键着陆")
root.bind_all('<Key>', key)
root.mainloop()

print("Close vehicle object")
vehicle.close()
