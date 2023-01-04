#!/usr/bin/python
# -*- coding: UTF-8 -*-
import random,bot_plugin_goupibutong_addons_readJSON

data = bot_plugin_goupibutong_addons_readJSON.readjson()
whospeak = data["famous"] # a 代表前面垫话，b代表后面垫话
beforeit = data["before"] # 在名人名言前面弄点废话
afterit = data['after']  # 在名人名言后面弄点废话
feihua = data['bosh'] # 代表文章主要废话来源
xx = "上海"

repeatit = 2 # 重复度
resultit=''
def dfs(dfs):
    global repeatit
    hhh = list(dfs) * repeatit
    while True:
        random.shuffle(hhh)
        for data in hhh:
            yield data

nextfeihua = dfs(feihua)#下一句废话
scmrmy = dfs(whospeak)

def comeon():
    global scmrmy#名人名言
    xx = next(scmrmy)
    xx = xx.replace(  "a",random.choice(beforeit) )
    xx = xx.replace(  "b",random.choice(afterit) )
    return xx

def nextpara():
    xx = ". "
    xx += "\r\n"
    xx += "    "
    return xx

def goupi_main(rev):
    rev=str(rev).replace(" ","").replace("狗屁不通","").replace("+","")
    if rev=="":
        return "FATAL ERROR:8998(BULLSHITGENERATOR_EMPTY_ERROR),请联系马哥解决"
    return start_main(xx=rev)



def start_main(xx='上海',rep=2):
    for x in xx:
        tmp = str()
        while ( len(tmp) < 260 ) :
            branch = random.randint(0,100)
            if branch < 5:
                tmp += nextpara()
            elif branch < 20 :
                tmp += comeon()
            else:
                tmp += next(nextfeihua)
        tmp = tmp.replace("x",xx)
        return tmp



if __name__=="__main__":
    print(goupi_main("狗屁不通 + 上海"))