import json
import random
def getshenhuifu():
    with open(r"data/goodreturn.json","r",encoding="utf-8") as f:
        a=json.load(f)
    aa=random.choice(a["return"]).replace("<br>","\n")
    return aa

if __name__=="__main__":
    print(getshenhuifu())