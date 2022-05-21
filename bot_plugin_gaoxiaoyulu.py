import json
import random
def getgaoxiaoyulu():
    with open(r"data/gaoxiaoyulu.json","r",encoding="utf-8") as f:
        a=json.load(f)
    aa=random.choice(a["xiaohua"])
    return aa

if __name__=="__main__":
    print(getgaoxiaoyulu())