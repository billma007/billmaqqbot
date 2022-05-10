#!/usr/bin/python
# -*- coding: utf-8 -*-
import msvcrt
import os
from bot_debug import info,success,warning,error
import socket
import json
from save_settings import get_value
try:
    info("开始初始化监听端口...")
    ListenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ListenSocket.bind((get_value("ip"), get_value("listen")))
    ListenSocket.listen(100)
    success("成功初始化监听端口：http://"+(str(get_value("ip"))+":"+str(get_value("listen"))))
except:
    error("初始化监听端口失败，请检查配置文件。")
    info("按任意键退出程序进行配置。。。")
    msvcrt.getch()
    os._exit(0)
    
HttpResponseHeader = '''HTTP/1.1 200 OK\r\n
Content-Type: text/html\r\n\r\n
'''

def request_to_json(msg):
    for i in range(len(msg)):
        if msg[i]=="{" and msg[-1]=="\n":
            return json.loads(msg[i:])
    return None

#需要循环执行，返回值为json格式
def rev_msg():# json or None
    Client, Address = ListenSocket.accept()
    Request = Client.recv(1024).decode(encoding='utf-8')
    rev_json=request_to_json(Request)
    Client.sendall((HttpResponseHeader).encode(encoding='utf-8'))
    Client.close()
    return rev_json
