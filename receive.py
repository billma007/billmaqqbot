#!/usr/bin/python
# -*- coding: utf-8 -*-


import os
from bot_debug import info,success,warning,error
import socket
import json
from save_settings import get_value
from bot_checkdata import pause_ter
info("开始初始化监听端口...")
ListenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    ListenSocket.bind((get_value("ip"), get_value("listen")))
except OSError:
    error("通常每个套接字地址只能使用一次")
    warning("检测到端口冲突，请检查本软件是否已经启动过；如果没有，请修改settings.json的listen数字（随机4位数），再打开go-cqhttp的config.yml拉到最底下的url的数字改成相同数字。")
    pause_ter()
    os._exit(0x0)
ListenSocket.listen(100)
success("成功初始化监听端口：http://"+(str(get_value("ip"))+":"+str(get_value("listen"))))


HttpResponseHeader = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'

def request_to_json(msg):
    msg=str(msg).split("\r\n\r\n")
    for i in msg:
        if i[0]=="{":
            return json.loads(i)
    return msg
#需要循环执行，返回值为json格式
def rev_msg():# json or None
    try:
        Client, Address = ListenSocket.accept()
        Request = Client.recv(1024).decode(encoding='utf-8')
        rev_json=request_to_json(Request)
        Client.sendall((HttpResponseHeader).encode(encoding='utf-8'))
        Client.close()
        return rev_json
    except:
        pass

if __name__=="__main__":
    while True:
        print(rev_msg())
        