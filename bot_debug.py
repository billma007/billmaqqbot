#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from colorama import init, Fore
def timenow():
    local_times = time.localtime(time.time())
    local_time_asctimes = time.asctime(local_times)
    return str(local_time_asctimes)
def info(msg):# info
        init(autoreset=True)    
        print("["+timenow()+"][INFO]"+str(msg))
def success(msg):
        init(autoreset=True)    
        print(Fore.GREEN+"["+timenow()+"][SUCCESS]"+str(msg))
def error(msg):
        init(autoreset=True)    
        print(Fore.RED+"["+timenow()+"][ERROR]"+str(msg))
def warning(msg):
        init(autoreset=True)    
        print(Fore.YELLOW+"["+timenow()+"][WARNING]"+str(msg))