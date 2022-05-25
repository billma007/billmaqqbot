import json
import os
import platform
import sys
from time import sleep
import requests
from bot_debug import error, info, success, warning
SYSTEM=platform.system()

def pause_ter():
    if SYSTEM=="Windows" or SYSTEM=="windows":
        import msvcrt
        msvcrt.getch()
    else:
        import termios
        fd = sys.stdin.fileno()
        old_ttyinfo = termios.tcgetattr(fd)
        new_ttyinfo = old_ttyinfo[:]
        new_ttyinfo[3] &= ~termios.ICANON
        new_ttyinfo[3] &= ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, new_ttyinfo)

datalist=[
    r'data/bot_ext_mingyan.json',
    r'data/bot_plugin_arknight_addons_agent.json',
    r'data/dujitang.json',
    r'data/gaoxiaoyulu.json',
    r'data/goodreturn.json',
    r'data/goupibutongdata.json',
    r'data/luxun.json',
    r'data/bot_plugin_liferestart_addons_main/data/achievement.json',
    r'data/bot_plugin_liferestart_addons_main/data/age.json',
    r'data/bot_plugin_liferestart_addons_main/data/events.json',
    r'data/bot_plugin_liferestart_addons_main/data/talents.json',
    r'data/wangyiyun.json'
]
settingslist=[
    r'data/whosays.json',
    r'data/qiandao.json',
]
def downloaddata():
    if not os.path.isdir("data"):
        os.mkdir("data")
    if not os.path.isdir("/data/bot_plugin_liferestart_addons_main/data"):
        try:
            os.mkdir("data/bot_plugin_liferestart_addons_main")
        except:pass
        try:
            os.mkdir("data/bot_plugin_liferestart_addons_main/data")
        except:pass
    for i in datalist:
        if not os.path.isfile(i):
            warning("注意：检测到文件"+i+"缺失，正在下载该文件.....")
            with open(i,"wb") as iii:
                try:
                    url=r'https://fastly.jsdelivr.net/gh/billma007/billmaqqbot_datasave/'+i
                    rr=requests.get(url)
                    iii.write(rr.content)
                    iii.close()
                except:
                    iii.close()
                    error("连接失败，请前往https://github.com/billma007/billmaqqbot_datasave/ 或者 https://fastly.jsdelivr.net/gh/billma007/billmaqqbot_datasave/ 下载文件到本文件夹下data文件夹里")
                    pause_ter()
                    os._exit(0x0)
            success("成功下载数据文件"+i)
            success("成功检查数据文件"+i)
        else:
            success("成功检查数据文件:"+str(i))
            
def checkit():
    downloaddata()
    for iiiii in settingslist:
        if not os.path.isfile(iiiii):
            with open(iiiii,"w",encoding="utf-8") as clsss:
                clsss.write("{}")
                clsss.close()
    sting=True
    if not os.path.isfile(r'data/remote_settings.json'):
        with open(r'data/remote_settings.json',"w",encoding="utf-8") as f:
            zzzzz={
    "taboo": [
        "botSB",
        "SB"
    ],
    "function": []
}
            json.dump(zzzzz,f,indent=4)
            f.close()
    if not os.path.isfile(r"data/settings.json"):
        with open(r"data/settings.json","w",encoding="utf-8") as f:
            zzz={
        "listen" : 8000,
        "send"   : 5700,
        "ip"     : "127.0.0.1",
        "group"  : ["834027482","820433165"],
        "guild"  : [["10264721650848156","5682529"]],
        "private": ["36937975","237103015"],
        "device" : "iphonr13.2",
    }
            json.dump(zzz,f,indent=4)
            f.close()
        sting=False
    if not os.path.isfile(r"data/force.json"):
        with open(r"data/force.json","w",encoding="utf-8") as ff:
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
        pause_ter()
        os._exit(0)
    success("配置文件检查成功！")