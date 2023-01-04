import json,random
def luxunshuoguo():
    fffff=open(r"data/luxun.json","r",encoding="utf-8")
    kkkkk=json.load(fffff)
    fffff.close()
    try:return "鲁迅说过，"+random.choice(kkkkk["luxun"])
    except:return "发生错误"

if __name__=="__main__":
    print(luxunshuoguo())