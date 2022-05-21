import json
import time
from bot_blacklist import adminreturn
from bot_plugin_generate import returnnum
def rettime() -> str :
    '''
    返回当前日期戳
    返回值：str
    '''
    ret=time.strftime("%Y%m%d") 
    return ret

def get_qiandao(qq,qun) -> int :
    '''
    获取某个QQ得到的积分（返回int值）
    '''
    ff=open(r"data/qiandao.json","r")
    fff=json.load(ff)
    ff.close()
    try:
        return fff[str(qun)][str(qq)]
    except:
        fff[str(qun)][str(qq)]=0
        return 0
def qiandao(qq,qun) -> str:
    '''
    签到主函数
    '''
    ff=open(r"data/qiandao.json","r")
    fff=json.load(ff)
    ff.close()
    try:
        todaylist_firsttest=fff[str(qun)]
    except:
        fff[str(qun)]={
            "today":{}
        }
    try:
        todaylist=fff[str(qun)]["today"][rettime()]
    except:
        todaylist=[]
        fff[str(qun)]["today"][rettime()]=[]
    if str(qq) in todaylist:
        return "你今天已经签过到了哦"
    else :
        fff[str(qun)]["today"][rettime()].append(str(qq))
        import random
        a=random.randint(1,100)
        try:
            fff[str(qun)][str(qq)]=int(fff[str(qun)][str(qq)])+a
        except:
            fff[str(qun)][str(qq)]=int(a)
        returnit="签到成功！"+str(qq)+"签到获得了"+str(a)+",现在你有积分"+str(fff[str(qun)][str(qq)])
        with open(r"data/qiandao.json","w") as ffff:
            json.dump(fff,ffff,indent=4)
            ffff.close()
        return returnit
def dubo(qun,qq,msg) -> str:
    '''
    赌博有害身心，谨慎赌博
    '''
    money=''.join(filter(str.isdigit, msg)).replace(" ","").replace("+","").replace(" ","")
    if money=="":
        return "请输入正确的数字！"
    money=int(money)
    ff=open(r"data/qiandao.json","r")
    fff=json.load(ff)
    ff.close()
    try:
        own=int(fff[str(qun)][str(qq)])
    except:
        own=0
    if own<money:
        return "你穷了，钱不够赌博了，回家挣钱吧"
    else:
        import random
        ran=random.randint(1,100)
        if ran<=30:
            own=own-money
            returnit="啊哦，赌博失败了，本金全没了"
        elif ran<=45:
            own=own-money/2
            returnit="本金少了一半:（"
        elif ran<=65:
            own=own
            returnit="本金不变"
        elif ran<=80:
            own=own+money/2
            returnit="多拿了一半：）"
        elif ran<=99:
            own=own+money
            returnit="ohhhhhhh,本金翻倍了！"
        elif ran==100:
            own=own+money*50
            returnit="Congratulations!50倍返还！！！"
        fff[str(qun)][str(qq)]=int(own)
    with open(r"data/qiandao.json","w") as ffff:
        json.dump(fff,ffff,indent=4)
        ffff.close()
    return returnit     
def admin_check(qun,adminqq,msg) -> str:
    '''
    （管理员权限）
    查看某个用户的余额
    '''
    if not adminreturn(adminqq):
        return "您没有权限使用这个指令。"
    else:
        return ''.join(filter(str.isdigit, msg)).replace(" ","").replace("+","").replace(" ","")+"剩余的积分数为"+str(get_qiandao(''.join(filter(str.isdigit, msg)).replace(" ","").replace("+","").replace(" ",""),qun=qun))

def admin_add(qun,adminqq,msg):
    '''此处加紧施工中orz'''
    if not adminreturn(adminqq):
        return "您没有权限使用这个指令。"
    else:
        try:
            qqlist=str(msg).split(" ")
            qq=int(qqlist[-2])
            num=int(qqlist[-1])
        except:
            return "参数格式输入错误"
        ff=open(r"data/qiandao.json","r")
        fff=json.load(ff)
        ff.close()
        try:
            todaylist_firsttest=fff[str(qun)]
        except:
            fff[str(qun)]={
                "today":{}
            }
        try:
            todaylist=fff[str(qun)]["today"][rettime()]
        except:
            todaylist=[]
            fff[str(qun)]["today"][rettime()]=[]
        fff[str(qun)]["today"][rettime()].append(str(qq))
        a=num
        try:
            fff[str(qun)][str(qq)]=int(fff[str(qun)][str(qq)])+a
        except:
            fff[str(qun)][str(qq)]=int(a)
        returnit="添加成功！给"+str(qq)+"添加了"+str(a)+",现在ta有积分"+str(fff[str(qun)][str(qq)])
        with open(r"data/qiandao.json","w") as ffff:
            json.dump(fff,ffff,indent=4)
            ffff.close()
        return returnit
def admin_delete(qun,adminqq,msg):
    '''此处加紧施工中orz'''
    if not adminreturn(adminqq):
        return "您没有权限使用这个指令。"
    else:
        try:
            qqlist=str(msg).split(" ")
            qq=int(qqlist[-2])
            num=int(qqlist[-1])
        except:
            return "参数格式输入错误"
        ff=open(r"data/qiandao.json","r")
        fff=json.load(ff)
        ff.close()
        try:
            todaylist_firsttest=fff[str(qun)]
        except:
            fff[str(qun)]={
                "today":{}
            }
        try:
            todaylist=fff[str(qun)]["today"][rettime()]
        except:
            todaylist=[]
            fff[str(qun)]["today"][rettime()]=[]
        fff[str(qun)]["today"][rettime()].append(str(qq))
        a=num
        try:
            fff[str(qun)][str(qq)]=int(fff[str(qun)][str(qq)])-a
        except:
            fff[str(qun)][str(qq)]=0
        if  fff[str(qun)][str(qq)]<=0: fff[str(qun)][str(qq)]=0
        returnit="删除成功现在ta有积分"+str(fff[str(qun)][str(qq)])
        with open(r"data/qiandao.json","w") as ffff:
            json.dump(fff,ffff,indent=4)
            ffff.close()
        return returnit
def caishuzi(qun,qq,msg) ->str :
    money=int(str(msg).split(" ")[-1].replace(" ",""))
    msgg=msg.replace(str(money),"")
    ff=open(r"data/qiandao.json","r")
    fff=json.load(ff)
    ff.close()
    try:
        own=int(fff[str(qun)][str(qq)])
    except:
        own=0
    if own<money:
        return "你穷了，钱不够赌博了，回家挣钱吧"
    else:
        aaaa=returnnum(msgg)
        aaa=aaaa[0]
        returnit="本轮抽取数字为："
        if aaa==-2:return "发生未知错误"
        elif aaa==-1:return "参数错误：必须至少有4个数字。详情请输入help/.bot help"
        returnit=returnit+str(aaaa[1])+str(aaaa[2])+str(aaaa[3])+str(aaaa[4])
        if aaa==0:
            own=own-money
            returnit+="猜对0个，本赔光了：（"
        elif aaa==1:
            own=own-money/2
            returnit+="猜对一个，赔了一半：（"
        elif aaa==2:
            returnit+="猜对2个，金额不变--_--"
        elif aaa==3:
            own=own+money
            returnit+="猜对三个，赚了一倍：）"
        elif aaa==4:
            own=own+money*3
            returnit+="猜对四个，奖金翻三倍！"
        else:
            return "发生未知数据错误"
        with open(r"data/qiandao.json","w") as ffff:
            json.dump(fff,ffff,indent=4)
            ffff.close()
    return returnit     


def qiandaomain(qun,qq,msg) ->str:
    if "qd" in msg or "qiandao" in msg:
        return qiandao(qq,qun)
    elif "search" in msg:
        return str(qq)+"现在拥有积分"+str(get_qiandao(qq,qun))
    elif "db" in msg or "dubo" in msg:
        return dubo(qun,qq,msg)
    elif "admin" in msg:
        if "check" in msg:
            return admin_check(qun,qq,msg)
        if "add" in msg:
            return admin_add(qun,qq,msg)
    elif "guess" in msg:
        return caishuzi(qun,qq,msg)
    else:
        return "未知指令"

