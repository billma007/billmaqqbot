import requests
import json
def getnews():
    try:
        a=requests.get("https://v.api.aa1.cn/api/topbaidu/index.php")
        aaa=list(a.text)
        while aaa[-1]=="1" or aaa[-1]=="\n" or aaa[-1]=="\r" or aaa[-1]=="\s" or aaa[-1]=="\t":
                aaa.pop()
        aaa=''.join(aaa)
        aa=json.loads(aaa)
        returnit=""
        iiiii=0
        for ii in aa["newslist"]:
            returnit+=ii["title"]+'\n'+ii['digest']+'\n'
            iiiii+=1
            if iiiii==10 or iiiii==20 or iiiii==39:
                returnit+="\n"
        return returnit
    except:
        return "新闻爬取错误"
if __name__=="__main__":
    print(getnews())