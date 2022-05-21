import json
import random


def getwangyiyun():
    with open(r"data/wangyiyun.json","r",encoding="utf-8") as f:
        fff=json.load(f)
        return random.choice(fff['wangyiyun'])