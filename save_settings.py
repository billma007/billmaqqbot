#!/usr/bin/python
# -*- coding: utf-8 -*-
from bot_debug import info,success,error
import json

def _init():  # 初始化
    info("初始化设置中")
    global _global_dict
    _global_dict = {}
    success("初始化设置成功")
 
 
def set_value(key, value):
    # 定义一个全局变量
    try:
        _global_dict[key] = value
        success("成功导入设置"+str(key))
    except:
        error("导入设置失败")
        raise Exception("导入设置失败")
def init_settings():
    try:
        info("开始导入设置 从settings.json中")
        aaaaa=open("settings.json","r",encoding="utf-8")
        aaa=json.load(aaaaa)
        aaaaa.close()
        set_value("listen"  ,aaa["listen"]  ) #监听端口 int
        set_value("send"    ,aaa["send"]    ) #发送端口 int
        set_value("device"  ,aaa["device"]  ) #设备名称 str
        set_value("ip"      ,aaa["ip"]      ) #IP       str
        set_value("group"   ,aaa["group"]   ) #可用群聊 list[str]
        set_value("guild"   ,aaa["guild"]   ) #可用频道 list[list[guild_id(str),channal_id(str)]]
        set_value("private" ,aaa["private"] ) #聊天     list[str]
        set_value("taboo"   ,aaa["taboo"] )   #非法字符 list[str]
    except:
        error("致命错误：数据导入失败")
        raise Exception("致命错误：数据导入失败")

def get_value(key):
    # 获得一个全局变量，不存在则提示读取对应变量失败
    try:
        return _global_dict[key]
    except:
        error("获取"+str(key)+"失败")
        raise Exception("发生错误：获取数据失败")
