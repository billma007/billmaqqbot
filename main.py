#!/usr/bin/python
# -*- coding: utf-8 -*-

from bot_debug import success,info,error,warning
info("开始导入模块...")
import msvcrt
import sys,os
from time import sleep
import traceback
import json
from save_settings import set_value,_init,get_value,init_settings
success("模块导入成功！")
info("正在检查配置文件！")
'''
检查配置文件是否存在
'''
sting=True
if not os.path.isfile("settings.json"):
    with open("settings.json","w",encoding="utf-8") as f:
        zzz={
    "listen" : 8000,
    "send"   : 5700,
    "ip"     : "127.0.0.1",
    "group"  : ["834027482","820433165"],
    "guild"  : [["10264721650848156","5682529"]],
    "private": ["36937975","237103015"],
    "device" : "iphonr13.2",
    "taboo"  : ["SB","nmd"]
}
        json.dump(zzz,f,indent=4)
        f.close()
    sting=False
if not os.path.isfile("force.json"):
    with open("force.json","w",encoding="utf-8") as ff:
        zzzz={
    "blacklist": [],
    "superadmin": [
        "36937975",
        "237103015",
        "2981686635"
    ],
    "admin": [
        "2981686635",
        "964146474",
        "36937975"
    ]
}
        json.dump(zzzz,ff,indent=4)
        f.close()
    sting=False

if sting==False:
    warning("首次启动该程序检测到有配置文件缺失，将会释放三个文件；请按照https://github.com/billma007/billmaqqbot 的配置文件进行配置。")
    info("按任意键退出程序进行配置...")
    msvcrt.getch()
    os._exit(0)
success("配置文件检查成功！")
'''
初始化设置
'''

_init()
init_settings()

info("开始加载权限系统...")

# receive and send message
from send_msg import  changephone, send_msg_group, send_msg_guild,send_msg_private
from receive import rev_msg

from bot_changename import changename
from bot_blacklist import adminlist, blacklist,superadmin
success("权限系统加载成功！")
info("开始加载plugin插件....")

# plugin and adapters
from bot_plugin_jrrp import jrrp
from bot_plugin_aitalk import aitalk
from bot_plugin_goupibutong import goupi_main
from bot_plugin_musicdown import musicdown
from bot_plugin_liferestart import lifemain
from bot_plugin_dujitang import dujitang
from bot_plugin_check import check
from bot_plugin_arknight import arknightsanalysis
from bot_plugin_historytoday import history_today
success("插件加载成功！")
def analysisfunc(msg):
            '''
            判断消息类型并处理
            '''
            msgsend="FATAL ERROR:0001(UNKNOWN ERROR)"
            if msg=="1234567890":
                msgsend="对不起，您没有权限执行这个操作."
            elif "jrrp" in msg:
                msgsend=jrrp(msg)
            elif "rc" in msg or "事件鉴定" in msg:
                msgsend=check(msg)
            elif "毒鸡汤" in msg:
                msgsend=dujitang()
            elif "人生重开"  in msg:
                msgsend=lifemain()
            elif "方舟寻访" in msg or "arknight" in msg:
                msgsend=arknightsanalysis(msg)
            elif "下载音乐" in msg:
                msgsend=musicdown(msg)
            elif "history-today" in msg or "历史上的今天" in msg:
                msgsend=history_today()
            elif "CQ:image" in msg:
                msgsend='图片无法识别'
            elif "狗屁不通" in msg:
                msgsend=goupi_main(msg)
            else:
                msgsend=aitalk(msg)
            for i in get_value("taboo"):
                if i in msg:
                    msgsend="对不起，您的话中含有非法字符。"
            return msgsend


if __name__=="__main__":
    success("程序启动成功！")
    info("当前版本：1.0.0-rc12 Release")

    while True:
        try:
            info("正在连接http上报器...")
            changephone("iphone13.2")
            success("成功连接到http上报器。")
            break
        except:
            error("连接失败，5秒钟后重新连接...")
            info("提示：如果多次连接失败，请尝试重启go-cqhttp。")
            sleep(5)
            continue

    info("开始接受和处理信息")
    while True:

        try:
            rev = rev_msg()
            if rev == None:
                continue
            msgsend=""
    #管理权限
            if ("。bot set" in rev["message"] or ".bot set" in rev["message"] ) and rev['message_type']!='guild':
                msg=adminlist(rev['user_id'],rev['message'])
                if rev['message_type']=="group":
                    send_msg_group({'msg_type':'group','group_id':str(rev['group_id']),'msg':msg})
                else:
                    warning("管理权限使用失败：请在群聊内操作。")
                    raise Exception("管理权限使用失败：请在群聊内操作。")
    #禁止黑名单操作
            elif blacklist(rev['user_id'] )==True:
                if rev['message_type']=="group" and ("。bot set" in rev["message"] or ".bot set" in rev["message"]):
                    send_msg_group({'msg_type':'group','group_id':str(rev['group_id']),'msg':"您没有权限执行这个操作。"}    )
                else:
                    raise 
    #群聊消息
            elif rev['message_type']=='group':


                if str(rev['group_id']) in get_value("group"):
                    if ".bot" in rev['message'] or "。bot" in rev['message']:
                        msg=str(rev['message']).replace(".bot","").replace("。bot","")
                        msgsend=analysisfunc(msg)
                        send_msg_group({'msg_type':'group','group_id':str(rev['group_id']),'msg':msgsend})

    #频道消息
            elif  rev['message_type']=='guild' :
                if [rev["guild_id"],rev['channel_id']] in get_value("guild"):
                    msgsend=analysisfunc(rev['message'])
                    send_msg_guild({'msg_type':'guild','guild_id':rev["guild_id"],'channel_id': rev["channel_id"],  'msg':msgsend})
            elif rev['message_type']=='private':
                if  "all" in get_value("private") or rev['user_id'] in get_value("private"):
                    msgsend=analysisfunc(rev['message'])
                    send_msg_private({'msg_type':'private','user_id':rev["user_id"],'msg':msgsend})

        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as e:
            error("发生错误：")
            warning(traceback.format_exc())
            continue

'''
一个频道消息实例：


{'channel_id': '5682529', 
'guild_id': '10264721650848156', 
'message': '忐忐忑忑所拖', 
'message_id': 'BAAkd7W/t5GcAAAAAABWtWEAAAAAAAAAHQ==', 
'message_type': 'guild', 
'post_type': 'message', 
'self_id': 1475326665, 
'self_tiny_id': '144115218703272260', 
'sender': {'nickname': 'BillMa007', 
    'tiny_id': '144115218703263397', 
    'user_id': 144115218703263397}, 
'sub_type': 'channel', 
'time': 1651021328, 
'user_id': '144115218703263397'}

一个群聊消息实例：

{'anonymous': None, 
'font': 0, 
'group_id': 834027482, 
'message': '1', 
'message_id': 247448390, 
'message_seq': 70262, 
'message_type': 'group', 
'post_type': 'message', 
'raw_message': '1', 
'self_id': 1475326665, 
'sender': {'age': 0, 'area': '', 
    'card': '我一定要抽到三周年限定觉得语文作业好多23', 
    'level': '', 
    'nickname': 'ma', 
    'role': 'admin', 
    'sex': 'unknown', 
    'title': '', 
    'user_id': 36937975}, 
'sub_type': 'normal', 
'time': 1651629458, 
'user_id': 36937975}

@某人消息：
{'anonymous': None, 
'font': 0, 
'group_id': 834027482, 
'message': '[CQ:at,qq=964146474]', 
'message_id': 2042164176, 
'message_seq': 70263, 
'message_type': 'group', 
'post_type': 'message', 
'raw_message': '[CQ:at,qq=964146474]', 
'self_id': 1475326665, 
'sender': {'age': 0, 
    'area': '', 
    'card': '我一定要抽到三周年限定觉得语文作业好多23', 
    'level': '', 
    'nickname': 'ma', 
    'role': 'admin', 
    'sex': 'unknown', 
    'title': '',
    'user_id': 36937975}, 
'sub_type': 'normal', 
'time': 1651629641, 
'user_id': 36937975}
'''

