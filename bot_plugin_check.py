#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import random
def check(object) -> str: 
    f=open(r"data/bot_ext_mingyan.json",encoding="utf-8")
    sss=json.load(f)
    f.close()
    mingyan=random.choice(sss["mingzhu"])
    object=str(object).replace("rc","").replace(" ","").replace("事件鉴定","")
    ran=random.randint(0,100)
    if ran<=10:
        return str("鉴定成功！"+object+"鉴定："+str(ran)+"/100，为“完全失败”\n")+mingyan
    elif ran<=20:
        return str("鉴定成功！"+object+"鉴定："+str(ran)+"/100，为“大失败”\n")+mingyan
    elif ran<=30:
        return str("鉴定成功！"+object+"鉴定："+str(ran)+"/100，为“失败”\n")+mingyan
    elif ran<=40:
        return str("鉴定成功！"+object+"鉴定："+str(ran)+"/100，为“小失败”\n")+mingyan
    elif ran<=60:
        return str("鉴定成功！"+object+"鉴定："+str(ran)+"/100，为“成功失败”\n")+mingyan
    elif ran<=70:
        return str("鉴定成功！"+object+"鉴定："+str(ran)+"/100，为“困难成功”\n")+mingyan
    elif ran<=80:
        return str("鉴定成功！"+object+"鉴定："+str(ran)+"/100，为“小成功”\n")+mingyan
    elif ran<=90:
        return str("鉴定成功！"+object+"鉴定："+str(ran)+"/100，为“成功”\n")+mingyan
    elif ran<=100:
        return str("鉴定成功！"+object+"鉴定："+str(ran)+"/100，为“大成功！”\n")+mingyan
    else:
        return str("啊哦，"+"鉴定失败！"+object+"没法测\n")+mingyan

if __name__=="__main__":
    print(check("秦富康"))