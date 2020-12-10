#!/usr/bin/envpython
# -*- coding: utf-8-*-
"""
项目001，使用simple_goto.py函数实现
无人机自动前往指定地点装载外卖并返回出发点
出发点(31.84719109,117.23534612,30.1,0)
目的点(31.84704621 117.23625396,29.7,0)
"""
# 加载函数
from __future__ import print_function
from dronekit import connect, VehicleMode, LocationGlobalRelative
import time

# 设置连接仿真程序输出端口,并在控制台展示
connection_string = '192.168.8.127:14550'
print('正在%s端口与飞行器连接' % connection_string)

# 生成无人机对象:WaiMaiDD
WaiMaiDD = connect(connection_string, wait_ready=True)

# 定义arm_and_takeoff(解锁起飞)函数
def arm_and_takeoff(aTargetAltitude):
    # 自动进行起飞前检查
    print('起飞前检查')
    # 通过读取is_armable来判断初始化是否完成
    while not WaiMaiDD.is_armable:
        print('外卖弟弟正在初始化')
        time.sleep(1)
    # 电机开始旋转
    print('电机开始旋转')
    # 将飞行模式切换铖“GUIDED”
    WaiMaiDD.mode = VehicleMode("GUIDED")
    # 解锁无人机
    WaiMaiDD.armed = True
    # 确认电机已经解锁
    while not WaiMaiDD.armed:
        print('等待外卖弟弟解锁')
        time.sleep(1)
    # 发送起飞指令
    print("外卖弟弟起飞！")
    # simple_takeoff发送指令，使无人机起飞并上升到目标高度
    WaiMaiDD.simple_takeoff(aTargetAltitude)
    # 上升到指定高度，堵塞程序
    while True:
        # 每5秒展示当前高度，直到达到目标高度 95%
        print("Altitude:", WaiMaiDD.location.global_relative_frame.alt)
        # 判断当前高度是否满足条件
        if WaiMaiDD.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("到达目标高度")
            break
        time.sleep(5)

# 定义is_target_point_reach(达到目的点)函数
def is_reach_target_point(aTargetPoint):
    # 按照我的猜测做的一个判断无人机实时地理坐标与目标点坐标匹配的函数
    if WaiMaiDD.location.global_frame.lon - aTargetPoint.lon <= 0.0000001:
        if WaiMaiDD.location.global_frame.lat - aTargetPoint.lat <= 0.0000001:
            return True
    return False
# 主程序
# 解锁并起飞至相对地面高度25米
# 设置无人机起飞空速15m/s
print("设置起飞空速为15m/s")
WaiMaiDD.airspeed = 15
arm_and_takeoff(25)

# 设置飞行空速
print("设置飞行空速20m/s")
WaiMaiDD.airspeed = 20
time.sleep(1)

# 设置目标点
tp = LocationGlobalRelative(31.84703374, 117.23625384, 25)

# 调用simple_goto函数，发送目标点tp给外卖弟弟
print("弟弟出发！")
WaiMaiDD.simple_goto(tp)

# 调用is_reach_target_point函数判断是否到达目标点
while not is_reach_target_point(tp):
    print("弟弟正在前往目的点位")
    time.sleep(6)
print("弟弟已到位，准备降落~")
time.sleep(1)

# 设置VehicleMode = LAND 降落模式，执行降落。
print("弟弟降落")
WaiMaiDD.mode = VehicleMode("LAND")
# 通过地面距离判断是否降落成功
while True:
    if WaiMaiDD.location.global_relative_frame.alt <= 1.5:
        break
# 给外卖小哥15秒时间装载外卖
print("离地小于1.5米，外卖小哥有15秒时间装载外卖...")
time.sleep(15)

# 设置外卖弟弟返回起始位置
print('主人稍等，弟弟正在返回~')
WaiMaiDD.airspeed = 10
arm_and_takeoff(25)
hp = LocationGlobalRelative(31.84719109, 117.23534612, 25)
WaiMaiDD.airspeed = 20
WaiMaiDD.simple_goto(hp)
while not is_reach_target_point(hp):
    print("外卖马上到了，主人稍等！")
    time.sleep(6)
print("正在降落~")
WaiMaiDD.mode = VehicleMode("LAND")
time.sleep(30)
print("外卖到手！")
WaiMaiDD.close()

