import random
from bot_debug import error
import json

def add(msg):
        msg=msg.replace(".bot","").replace("。bot","").replace("whosays","").   replace("add","")
        ffffff=open(r"data/whosays.json","r",encoding="utf-8")
        js=json.load(ffffff)
        ffffff.close()
        msgg=[x for x in msg.split(' ') if x]
        msggg=msgg[0]
        msgg.pop(0)
        try:
            js[msggg]+=msgg
        except:
            js[msggg]=msgg
        with open(r"data/whosays.json","w",encoding="utf-8") as ffff:
            json.dump(js,ffff,indent=4,ensure_ascii=False)
            ffff.close()
        return "添加成功！"
        
def search(msg):
    try:
        msgg=msg.replace(".bot","").replace("。bot","").replace("whosays","").   replace("list","").replace(" ","")
        ffffff=open(r"data/whosays.json","r",encoding="utf-8")
        js=json.load(ffffff)
        ffffff.close()
        jjs=random.choice(js[msgg])
        return msgg+"曾经说过，"+jjs

    except:
        return "查询失败"

def whosays(msg):
    if "add" in msg:
        msgsend=add(msg)
    elif "list" in msg:
        msgsend=search(msg)
    else:
        msgsend="指令错误。"
    return msgsend