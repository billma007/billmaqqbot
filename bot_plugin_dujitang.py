from urllib import request
import random,json
def dujitang() :
    try:
        f=open(r"data/bot_ext_mingyan.json",encoding="utf-8")
        sss=json.load(f)
        f.close()
        b=random.choice(sss["dujitang"])
    except:
        b="对不起，获取毒鸡汤失败：("
    return b
if __name__=="__main__":
    print(dujitang())