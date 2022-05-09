import random

def jrrp(msg):
    msg=str(msg).replace("jrrp","").replace("今日人品","").replace(" ","").replace("+","")
    if msg=="":whois="你"
    else:whois=msg
    ran=random.randint(0,100)
    if ran<=10:
        return str(whois+"今日的人品系数是"+str(ran)+"分（满分100），为“诸事不宜”")
    elif ran<=20:
        return str(whois+"今日的人品系数是"+str(ran)+"分（满分100），为“大凶”")
    elif ran<=30:
        return str(whois+"今日的人品系数是"+str(ran)+"分（满分100），为“凶”")
    elif ran<=40:
        return str(whois+"今日的人品系数是"+str(ran)+"分（满分100），为“小凶”")
    elif ran<=60:
        return str(whois+"今日的人品系数是"+str(ran)+"分（满分100），为“中平”")
    elif ran<=70:
        return str(whois+"今日的人品系数是"+str(ran)+"分（满分100），为“小吉”")
    elif ran<=80:
        return str(whois+"今日的人品系数是"+str(ran)+"分（满分100），为“中吉”")
    elif ran<=90:
        return str(whois+"今日的人品系数是"+str(ran)+"分（满分100），为“大吉”")
    elif ran<=100:
        return str(whois+"今日的人品系数是"+str(ran)+"分（满分100），为“诸事皆宜”")
    else:
        return str("啊哦，"+whois+"今天运势好奇怪，没法测")