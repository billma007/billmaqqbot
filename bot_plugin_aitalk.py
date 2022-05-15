import requests
def aitalk(a):
    if "谁" in a:
            return "FATAL ERROR:发生错误\nERROR CODE==7802(SHEI_IN_MESSAGE)\n请联系马哥解决"
    else:
            url='http://api.qingyunke.com/api.php?key=free&appid=0&msg=%s'%a
            te=requests.get(url).json()
            data=te['content']
            return str(data.replace("{br}","\n").replace("梦想机器人","聊天机器人").replace("www.xiami.com","")).replace("菲菲","机器人")