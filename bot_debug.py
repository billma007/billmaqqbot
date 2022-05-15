#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
def timenow():
                local_times = time.localtime(time.time())
                local_time_asctimes = time.asctime(local_times)
                return str(local_time_asctimes)
def info(msg):# info
                print("["+timenow()+"][INFO]"+str(msg))
def success(msg):
                print("\033[92m"+"["+timenow()+"][SUCCESS]"+str(msg)+'\033[0m')
def error(msg):
                print("\033[91m"+"["+timenow()+"][ERROR]"+str(msg)+'\033[0m')
def warning(msg):
                print("\033[93m"+"["+timenow()+"][WARNING]"+str(msg)+'\033[0m')