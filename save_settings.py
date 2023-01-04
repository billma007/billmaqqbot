#!/usr/bin/python
# -*- coding: utf-8 -*-
from bot_debug import info,success,error,warning,debug
import json
import traceback
import os
from bot_checkdata import pause_ter
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
        print("=============================")
        warning(traceback.format_exc())
        print("=============================")
        error("导入设置失败，可能会导致程序无法正常运行。建议将已有配置文件删除，再次启动本程序，本程序会自动释放标准配置文件。待修改完毕后再启动本软件，本软件会自动读取。")
        info("按任意键退出程序进行配置。。。")
        pause_ter()
        os._exit(0)
def init_settings():
    try:
        info("开始导入设置 从settings.json中")
        with open(r"data/settings.json","r",encoding="utf-8") as aaaaa:
            aaa=json.load(aaaaa)
            aaaaa.close()
        set_value("listen"  ,aaa["listen"]  ) #监听端口 int
        set_value("send"    ,aaa["send"]    ) #发送端口 int
        set_value("device"  ,aaa["device"]  ) #设备名称 str
        set_value("ip"      ,aaa["ip"]      ) #IP       str
        set_value("group"   ,aaa["group"]   ) #可用群聊 list[str]
        set_value("guild"   ,aaa["guild"]   ) #可用频道 list[list[guild_id(str),channal_id(str)]]
        set_value("private" ,aaa["private"] ) #聊天     list[str]
        success("成功导入所有设置！")
    except:
        error("致命错误：数据导入失败")
        print("=============================")
        error(traceback.format_exc())
        print("=============================")
        warning("导入设置失败，可能会导致程序无法正常运行。建议将已有配置文件删除，再次启动本程序，本程序会自动释放标准配置文件。待修改完毕后再启动本软件，本软件会自动读取。")
        info("按任意键退出程序进行配置。。。")
        pause_ter()
        os._exit(0)
def get_value(key):
    # 获得一个全局变量，不存在则提示读取对应变量失败
    try:
        return _global_dict[key]
    except:
        error("获取"+str(key)+"失败")
        print("=============================")
        error(traceback.format_exc())
        print("=============================")
        warning("导入设置失败，可能会导致程序无法正常运行。建议将已有配置文件删除，再次启动本程序，本程序会自动释放标准配置文件。待修改完毕后再启动本软件，本软件会自动读取。")
        info("按任意键退出程序进行配置。。。")
        pause_ter()
        os._exit(0)
