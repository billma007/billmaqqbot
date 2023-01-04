import json
import requests

def history_today():
    try:
        getjson=requests.get("https://yuanxiapi.cn/api/history/?    format=json")
        jsonlo=json.loads(getjson.text)
        if jsonlo["code"]=="200":
            return jsonlo["day"]+"\n历史上的今天\n"+"\n".join(jsonlo["content"])
        else: return "未查询到相关信息:("
    except:
        return "发生错误：未能解析历史上的今天"


if __name__=="__main__":
    print(history_today())
    