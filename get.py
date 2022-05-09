from urllib import request
with open("dujitang.json",'w',encoding="utf-8") as fff:
    for i in range(1,1000):
        a=request.urlopen("https://api.oick.cn/dutang/api.php",timeout=4)
        b=a.read().decode("utf-8")
        b=b.replace("\n","")
        print(b)
        fff.write(b+',\n')