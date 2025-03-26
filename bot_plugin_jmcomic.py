JMOPENCHECK = True
import re
from send_msg import send_msg_jm
def jmchecheck(msg,group_id):
    global JMOPENCHECK
    if JMOPENCHECK:
        import jmcomic
        print("检测到禁漫下载请求")
        jmdownload(msg,group_id)
        return "已完成下载。"
    else:
        return "已关闭该功能。"

def jmdownload(jmmesss,group_id):
    # 提取数字部分
    numbers = re.sub(r'\D', '', jmmesss)
    # 检查是否为6位
    if len(numbers) == 6:
        manhua = [str(numbers)]  
        for id in manhua:
            import jmcomic
            print(f"开始下载禁漫{id}")
            jmcomic.download_album(id,'data/jmdown')
            send_msg_jm("data/jmdown/{id}.pdf",group_id,str(id))

    else:
        return False
    

if __name__=="__main__":
    jmchecheck(".bot jm 123456","784506492")
    