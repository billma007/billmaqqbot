#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

from bot_debug import warning,error
from save_settings import set_value,get_value
def  blacklist(qq):
    '''
    返回一个qq是不是黑名单
    返回格式：bool
    '''
    with open('data/force.json','r',encoding='utf-8') as f :
        blacklist=json.load(f)
        f.close()
    if str(qq) in str(blacklist["blacklist"]):
        return True
    else: return False

def printblacklist():
    '''
    返回所有被列入黑名单的成员QQ
    返回值：str
    '''
    try:
        with open('data/force.json','r',encoding='utf-8') as f :
            blacklist=json.load(f)
            f.close()
            returnit="\n".join(blacklist["blacklist"])
            return returnit
    except:
        return "发生错误：查询失败"
def printadminlist():
    '''
    返回所有被列入管理的QQ
    返回值：str
    '''
    try:
        with open('data/force.json','r',encoding='utf-8') as f :
            blacklist=json.load(f)
            f.close()
            returnit="以下是超级管理员："
            returnit=returnit+"\n".join(blacklist["superadmin"])
            returnit=returnit+"以下是管理员:"
            returnit=returnit+"\n".join(blacklist["admin"])
            return returnit
    except:
        return "发生错误：查询失败"
def superadmin(qq):
    '''
    判断某用户是否为超级管理员
    返回值：bool
    '''
    f=open('data/force.json','r',encoding='utf-8')
    superadmin=json.load(f)
    f.close()
    if str(qq) in str(superadmin["superadmin"]):
        return True
    else: return False

def adminreturn(qq):
    '''
    判断某用户是否为管理员(包括超级管理员)
    返回值：bool
    '''
    with open('data/force.json','r',encoding='utf-8') as f :
        superadmin=json.load(f)
        f.close()
    if str(qq) in str(superadmin["superadmin"]) or str(qq) in str(superadmin["admin"]):
        return True
    else: return False

def add_black(msg) -> str:
    '''
    将某QQ加入黑名单
    入参：任意含有QQ的字符串
    '''
    try:
        with open('data/force.json','r',encoding='utf-8') as f :
            blacklist=json.load(f)
            f.close()
            blist=blacklist["blacklist"]
            qqnum=''.join(filter(str.isdigit, msg))
            if str(qqnum) in blist:
                return "加入失败："+str(qqnum)+"已经被加入黑名单"
            elif adminreturn(str(qqnum))==True:
                return "加入失败："+str(qqnum)+"是管理员，无法加入"
            else:
                blist.append(str(qqnum))
                blacklist["blacklist"]=blist
                a_file=open(r'data/force.json',"w")
                json.dump(blacklist,a_file,indent=4)
                a_file.close()
                return "成功将"+str(qqnum)+"加入到黑名单"
    except :
        return "加入失败：未知原因"

def add_admin(msg,qq) -> str:
    '''
    将某QQ加入管理
    入参：任意含有QQ的字符串
    '''
    try:
        f=open(r'data/force.json','r',encoding='utf-8')
        adminlist=json.load(f)
        f.close()
        blist=adminlist["admin"]
        qqnum=''.join(filter(str.isdigit, msg))
        if superadmin(str(qq))==False:
            return "加入失败：您没有权限执行这个操作。"
        elif str(qqnum) in blist:
            return "加入失败："+str(qqnum)+"已经被加入管理员"
        elif blacklist(str(qqnum))==True:
            return "加入失败："+str(qqnum)+"是管理成员，无法加入"
        else:
            blist.append(str(qqnum))
            adminlist["admin"]=blist
            a_file=open(r'data/force.json',"w")
            json.dump(adminlist,a_file,indent=4)
            a_file.close()
            return "成功将"+str(qqnum)+"加入到管理"
    except :
        return "加入失败：未知原因"


def delete_black(msg) -> str:
    '''
    删除黑名单成员
    入参：含有QQ的任意字符串
    返回值：str
    '''
    try:
        with open('data/force.json','r',encoding='utf-8') as f :
            blacklist=json.load(f)
            f.close()
            blist=blacklist["blacklist"]
            qqnum=''.join(filter(str.isdigit, msg))
            if str(qqnum) not in blist:
                return "删除失败："+str(qqnum)+"不在黑名单"
            else:
                blist.remove(str(qqnum))
                blacklist["blacklist"]=blist
                a_file=open(r'data/force.json',"w")
                json.dump(blacklist,a_file,indent=4)
                a_file.close()
                return "成功将"+str(qqnum)+"从黑名单删除"
    except :
        return "删除失败：未知原因"

def delete_admin(msg,qq) -> str:
    '''
    删除管理员成员
    入参：含有QQ的任意字符串
    返回值：str
    '''
    try:
        with open('data/force.json','r',encoding='utf-8') as f :
            blacklist=json.load(f)
            f.close()
            blist=blacklist["admin"]
            qqnum=''.join(filter(str.isdigit, msg))
            if superadmin(str(qq))==False:
                return "删除失败：您没有权限执行这个操作。"
            if str(qqnum) not in blist and adminlist(str(qqnum))==False:
                return "删除失败："+str(qqnum)+"不在管理员"
            else:
                blist.remove(str(qqnum))
                blacklist["admin"]=blist
                a_file=open(r'data/force.json',"w")
                json.dump(blacklist,a_file,indent=4)
                a_file.close()
                return "成功将"+str(qqnum)+"从管理员删除"
    except :
        return "删除失败：未知原因"

def set_taboo(word) -> str:
    '''
    将某禁忌词语添加至设置
    '''
    word=str(word).replace(".bot","").replace("。bot","").replace("admin","").replace("set","").replace("add","").replace("delete","").replace("search","").replace(" ","").replace("+","").replace("taboo","").replace("bot","")
    try:
        f=open(r"data/remote_settings.json","r",encoding="utf-8")
        ret=json.load(f)
        f.close()
        if  ret["taboo"]==None:
             ret["taboo"]=[]
        if word in ret["taboo"]:
            return "该关键词已被收录"
        else :
            ret["taboo"].append(word)
            g=open(r"data/remote_settings.json","w",encoding="utf-8")
            json.dump(ret,g,indent=4)
            return "成功添加该关键词。"
    except:
        error("管理员试图添加一个禁忌词，但是失败了")
        return "添加失败：（"

def del_taboo(word):
    '''
    将某禁忌词语删除至设置
    '''
    word=str(word).replace(".bot","").replace("。bot","").replace("admin","").replace("set","").replace("add","").replace("delete","").replace("search","").replace(" ","").replace("+","").replace("taboo","").replace("bot","")
    try:
        f=open(r"data/remote_settings.json","r",encoding="utf-8")
        ret=json.load(f)
        f.close()
        if word not  in ret["taboo"]:
            return "该关键词还不在禁忌词范围内"
        else :

            kkk=list(ret["taboo"].remove(word))
            ret["taboo"]=kkk
            g=open(r"data/remote_settings.json","w",encoding="utf-8")
            json.dump(ret,g,indent=4)
            return "成功添加该关键词。"
    except:
        error("管理员试图删除一个禁忌词，但是失败了")
        return "删除失败：（"

def get_taboo():
    '''
    将已经添加的禁忌词输出
    '''
    try:
        f=open(r"data/remote_settings.json","r",encoding="utf-8")
        ret=json.load(f)
        f.close()
        a="\n".join(ret["taboo"])
        return a 
        
    except:
        error("管理员试图查询禁忌词，但是失败了")
        return "查询失败：（"    
def judge_taboo(word):
    '''
    查询word是否包含禁忌词
    返回布尔函数
    '''
    try:
        f=open(r"data/remote_settings.json","r",encoding="utf-8")
        ret=json.load(f)
        f.close()
        for ii in ret["taboo"]:
            if ii in word:
                return True
        return False
    except:
        error("无法搜索禁忌词")
        return False
def adminlist(qq,msg) -> str:
    if adminreturn(qq=qq)==False:
        return "您没有权限进行这个操作。"
    else:
        msg=str(msg).replace(" ","").replace(".","").replace("。","").replace("set","").replace("+","")
        msgreturn="Administrator身份校验成功！\n"
        warning("警告：管理员"+str(qq)+"正在试图进行管理员和黑名单的操作")
        if "blacklist" in msg:
            if "add" in msg:
                msgreturn=msgreturn+str(add_black(msg))
            elif "delete" in msg or "remove" in msg:
                msgreturn=msgreturn+str(delete_black(msg))
            elif "search" in msg:
                msgreturn=msgreturn+str(printblacklist())
            else:
                msgreturn=msgreturn+"blacklist指令错误"
        elif "admin" in msg:
            if "add" in msg:
                msgreturn=msgreturn+str(add_admin(msg,qq))
            elif "delete" in msg or "remove" in msg:
                msgreturn=msgreturn+str(delete_admin(msg,qq))
            elif "search" in msg:
                msgreturn=msgreturn+str(printadminlist())
            else:
                msgreturn=msgreturn+"admin 指令错误"
        elif "taboo" in msg:
            if "add" in msg:
                msgreturn=msgreturn+str(set_taboo(msg))
            elif "delete" in msg or "remove" in msg:
                msgreturn=msgreturn+str(del_taboo(msg))
            elif "search" in msg:
                msgreturn=msgreturn+str(get_taboo())
            else:
                msgreturn=msgreturn+"admin 指令错误"
        return msgreturn
