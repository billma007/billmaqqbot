#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
from time import sleep
from bot_debug import success,info,error
from urllib.parse import quote,unquote
from save_settings import get_value

def send_msg_guild(resp_dict):
    ip = get_value("ip")
    port=get_value("send")

    msg_type = resp_dict['msg_type']  # 回复类型（群聊/私聊）
    #number = resp_dict['number']  # 回复账号（群号/好友号）
    msg = resp_dict['msg']  # 要回复的消息
    if '\n\n' in msg:
        msgg=str(msg).split("\n\n")
        for msggg in msgg:
            msggg = quote(msggg, encoding="utf-8")
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((ip, port))
            info("即将发送以下信息：\n"+unquote(msggg,encoding="utf-8"))
            if msg_type == "guild":
                payload = "GET /send_guild_channel_msg?guild_id=" + str(
            resp_dict['guild_id']) +"&channel_id="+str(resp_dict['channel_id'])+"&message=" + msggg+ " HTTP/1.1\r\nHost:" + ip + ":"+str(port)+"\r\nConnection: close\r\n\r\n"
                client.send(payload.encode("utf-8"))
                success("发送成功")
                sleep(0.2)
                client.close()
        return 0
    else:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        # 将字符中的特殊字符进行url编码
        msg = quote(msg, encoding="utf-8")
        if msg_type == "guild":
            payload = "GET /send_guild_channel_msg?guild_id=" + str(
                resp_dict['guild_id']) +"&channel_id="+str(resp_dict['channel_id'])+"&message=" + msg+ " HTTP/1.1\r\nHost:" + ip +  ":"+str(port)+"\r\nConnection: close\r\n\r\n"
        info("即将发送以下信息：\n"+unquote(msg,encoding="utf-8"))
        client.send(payload.encode("utf-8"))
        client.close()
        success("发送成功！")
        return 0

def send_msg_group(resp_dict):
    ip = get_value("ip")
    port=get_value("send")
    msg_type = resp_dict['msg_type']  # 回复类型（群聊/私聊）
    number = resp_dict['group_id']  # 回复账号（群号/好友号）
    msg = resp_dict['msg']  # 要回复的消息
    if '\n\n' in msg:
        msgg=str(msg).split("\n\n")
        for msggg in msgg:
            msggg = quote(msggg, encoding="utf-8")
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((ip, port))
            info("即将发送以下信息：\n"+unquote(msggg,encoding="utf-8"))
            if msg_type == "group":
                payload = "GET /send_group_msg?group_id=" + str(
            resp_dict['group_id']) +"&message=" + msggg+ " HTTP/1.1\r\nHost:" + ip + ":"+str(port)+"\r\nConnection: close\r\n\r\n"
                client.send(payload.encode("utf-8"))
                success("发送成功")
                sleep(1)
                client.close()
        return 0
    else:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        # 将字符中的特殊字符进行url编码
        msg = quote(msg, encoding="utf-8")
        if msg_type == "group":
            payload = "GET /send_group_msg?group_id=" + str(
            resp_dict['group_id']) +"&message=" + msg+ " HTTP/1.1\r\nHost:" + ip + ":"+str(port)+"\r\nConnection: close\r\n\r\n"
        info("即将发送以下信息：\n"+unquote(msg,encoding="utf-8"))
        client.send(payload.encode("utf-8"))
        client.close()
        success("发送成功！")
        return 0
def send_msg_private(resp_dict):
    ip = get_value("ip")
    port=get_value("send")
    msg_type = resp_dict['msg_type']  # 回复类型（群聊/私聊）
    number = resp_dict['user_id']  # 回复账号（群号/好友号）
    msg = resp_dict['msg']  # 要回复的消息
    if '\n\n' in msg:
        msgg=str(msg).split("\n\n")
        for msggg in msgg:
            msggg = quote(msggg, encoding="utf-8")
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((ip, port))
            info("即将发送以下信息：\n"+unquote(msggg,encoding="utf-8"))
            if msg_type == "private":
                payload = "GET /send_private_msg?user_id=" + str(
            resp_dict['user_id']) +"&message=" + msggg+ " HTTP/1.1\r\nHost:" + ip + ":"+str(port)+"\r\nConnection: close\r\n\r\n"
                client.send(payload.encode("utf-8"))
                success("发送成功！")
                sleep(1)
                client.close()
        return 0
    else:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        # 将字符中的特殊字符进行url编码
        msg = quote(msg, encoding="utf-8")
        if msg_type == "private":
                info("即将发送以下信息：\n"+unquote(msg,encoding="utf-8"))
                payload = "GET /send_private_msg?user_id=" + str(
            resp_dict['user_id']) +"&message=" + msg+ " HTTP/1.1\r\nHost:" + ip + ":"+str(port)+"\r\nConnection: close\r\n\r\n"
        client.send(payload.encode("utf-8"))
        client.close()
        success("发送成功！")
        return 0
def changephone(phone):
        ip = get_value("ip")
        port=get_value("send")
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        # 将字符中的特殊字符进行url编码
        payload = "GET /_set_model_show?model=" +phone + " HTTP/1.1\r\nHost:" + ip + ":"+str(port)+"\r\nConnection: close\r\n\r\n"
        client.send(payload.encode("utf-8"))
        client.close()
        return 0



#test
rev_test={'post_type': 'message', 
'message_type': 'private', 
'time': 1672740810, 
'self_id': 1475326665, 
'sub_type': 'friend', 
'raw_message': '嗨害嗨', 
'font': 0, 'sender': {'age': 0, 
    'nickname': 'BillMa007', 
    'sex': 'unknown', 
    'user_id': 36937975}, 
'message_id': -1363199072, 
'user_id': 36937975, 
'target_id': 1475326665, 
'message': '嗨害嗨'}