# -*- coding: utf-8 -*
from bot_debug import success,info,error,warning,debug

from receive import rev_msg
info("开始导入模块...")
import sys,os
from time import sleep
import traceback
from save_settings import set_value,_init,get_value,init_settings
from bot_help import HELP
import bot_checkdata
success("模块导入成功！")
info("正在检查配置文件！")
bot_checkdata.checkit()
'''
初始化设置
'''
_init()
init_settings()
info("开始加载权限系统...")

# receive and send message
from send_msg import  changephone, new_test, send_msg_group, send_msg_guild,send_msg_private
#from receive import  rev_msg, root,data1
from bot_changename import changename
from bot_blacklist import adminlist, blacklist,superadmin,judge_taboo
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
from bot_plugin_qiandao import qiandaomain
from bot_plugin_whosays import whosays
from bot_plugin_gaoxiaoyulu import getgaoxiaoyulu
from bot_plugin_luxun import luxunshuoguo
from bot_plugin_shenhuifu import getshenhuifu
from bot_plugin_news import getnews
from deepseek import deepseek_chat
from bot_plugin_haiguitang import hgt_main
from bot_plugin_wangyiyun import getwangyiyun
from bot_plugin_jmcomic import jmchecheck
deepseekmode=bool(get_value("deepseekmode"))
success("插件加载成功！")
def analysisfunc(msg,group_id=None,private_id=None):
            '''
            判断消息类型并处理
            '''
            msg=msg.replace(".bot","").replace("。bot","")
            msgsend="FATAL ERROR:0001(UNKNOWN ERROR)"
            if msg=="1234567890":
                msgsend="对不起，您没有权限执行这个操作."
            elif "jmcomic" in msg:
                if group_id!=None:
                    msgsend=jmchecheck(msg,group_id)
                else:
                    msgsend="对不起，请在群聊操作."
            elif "help" in msg:
                msgsend=HELP()
            elif "jrrp" in msg: #代号为1
                msgsend=jrrp(msg)
            elif "鲁迅说过" in msg:
                msgsend=luxunshuoguo()
            elif "whosays" in msg:
                msgsend=whosays(msg)
            elif "getnews" in msg or "今日新闻" in msg:
                msgsend=getnews()
            elif "rc" in msg or "事件鉴定" in msg:#代号为2
                msgsend=check(msg)
            elif "毒鸡汤" in msg:#代号为3
                msgsend=dujitang()
            elif "人生重开"  in msg:#代号为4
                msgsend=lifemain()
            elif "方舟寻访" in msg or "arknight" in msg:#代号为5
                msgsend=arknightsanalysis(msg)
            elif "下载音乐" in msg:#代号为6
                msgsend=musicdown(msg)
            elif "history-today" in msg or "历史上的今天" in msg:#代号为7
                msgsend=history_today()
            elif "CQ:image" in msg:
                msgsend='图片无法识别'
            elif "狗屁不通" in msg:#代号为8
                msgsend=goupi_main(msg)
            elif "神回复" in msg:
                msgsend=getshenhuifu()
            elif "搞笑语录" in msg:
                msgsend=getgaoxiaoyulu()
            elif "网易云热评" in msg:
                msgsend=getwangyiyun()
            elif "海龟汤" in msg:
                if deepseekmode==True:
                    msgsend=hgt_main(msg, group_id)
                else:
                    msgsend="对不起，您没有开启这个功能。"
            else:#代号为9
                if deepseekmode==True:
                    msgsend=deepseek_chat(msg)
                else:
                    msgsend=aitalk(msg)
            if judge_taboo(msg)==True:
                msgsend="对不起，您的话中含有非法字符。"
            return msgsend


if __name__=="__main__":
    success("程序启动成功！")
    info("当前版本：1.4.0 alpha3")
    data_rev={}
    while True:
            
        try:
            info("正在连接http上报器...")
            new_test()
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
            debug(rev)
            msgsend=""
    #元信息相关处理
            if rev["post_type"]=='meta_event':
                debug(rev)
                continue
    #管理权
            info(rev)
            rev_msg_data=rev["message"][0]
            if rev["post_type"]=='message' and rev_msg_data["type"]=='text':

                rev_message=rev_msg_data["data"]["text"]
                if ("。bot set" in rev_message or ".bot set" in rev_message ) and rev['message_type']!='guild':
                    msg=adminlist(rev['user_id'],rev_message)
                    if rev['message_type']=="group":
                        send_msg_group({'msg_type':'group','group_id':str(rev['group_id']),'msg':msg})
                    else:
                        warning("管理权限使用失败：请在群聊内操作。")
                        raise Exception("管理权限使用失败：请在群聊内操作。")
                    continue
        #禁止黑名单操作
                if blacklist(rev['user_id'] )==True:
                    msg="1234567890"
        #过滤禁忌词
                if judge_taboo(rev_message)==True:
                    msg="1234567890"
        #群聊消息
                if rev['message_type']=='group':

                    if str(rev['group_id']) in get_value("group"):
                        if ".bot" in rev_message or "。bot" in rev_message:
                            msg=str(rev_message).replace(".bot","").replace("。bot","")
                            if "signin" in msg:
                                msgsend=qiandaomain(qun=rev['group_id'],qq=rev["user_id"],msg=msg.replace("signin",""))
                            else:
                                msgsend=analysisfunc(msg,rev['group_id'])
                            send_msg_group({'msg_type':'group','group_id':str(rev['group_id']),'msg':msgsend})

        #频道消息
                elif  rev['message_type']=='guild' :
                    if [rev["guild_id"],rev['channel_id']] in get_value("guild"):
                        msgsend=analysisfunc(rev_message)
                        send_msg_guild({'msg_type':'guild','guild_id':rev["guild_id"],'channel_id': rev["channel_id"],  'msg':msgsend})
                elif rev['message_type']=='private':
                    if  "all" in get_value("private") or str(rev['user_id']) in str(get_value("private")):
                        msgsend=analysisfunc(rev_message)
                        send_msg_private({'msg_type':'private','user_id':rev["user_id"],'msg':msgsend})

        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as e:
            error("发生错误：")
            warning(traceback.format_exc())
            continue
