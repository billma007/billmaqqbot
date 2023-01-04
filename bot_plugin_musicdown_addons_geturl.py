#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
right_path = __file__.rstrip(os.path.basename(__file__))    # 获取当前文件的所在路径
os.chdir(right_path)    # 将工作路径改至目标路径
from bot_plugin_musicdown_addons_musicdl import  getit
from bot_plugin_musicdown_addons_musicdl import musicdlv1
from bot_debug import info,error, success,warning


def maingeturl(songname):
        info("初始化音乐下载模块...")
        warning("该部分处于测试阶段，解析时间可能较长，在此当中可能会有bug，请谨慎使用")
        getit._init()
        getit.set_value("song",songname)
        dl_client = musicdlv1.musicdl('config.json')
        success("成功初始化音乐模块")
        info("正在解析URL...")
        dl_client.run()
        info("成功获取音乐URL")
        return getit.get_value("url")


if __name__=="__main__":
    print(maingeturl("周杰伦"))