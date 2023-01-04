#!/usr/bin/python
# -*- coding: utf-8 -*-

def musicdown(msg):
    msg=str(msg)
    msgg=msg.replace("下载音乐","").replace("+","")
    from bot_plugin_musicdown_addons_geturl import maingeturl
    return maingeturl(msgg)