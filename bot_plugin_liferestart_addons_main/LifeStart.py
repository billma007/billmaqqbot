
from bot_plugin_liferestart_addons_main.Life import Life,HandlerException
returnit = ""
Life.load('data/bot_plugin_liferestart_addons_main/data')
def add_return(info):
    global returnit
    returnit+=str(info)

def genp(prop):
    if(prop < 1):
        return { 'CHR': 0, 'INT': 0, 'STR': 0, 'MNY': 0 }
    ps = []
    for i in range(3):
        ps.append(id(i) % (int(prop * 2 / (4 - i)) + 1))
        if(10 < ps[-1]):
            ps[-1] = 10
        prop -= ps[-1]
    if(10 < prop):
        prop+=sum(ps)
        ps = [int(prop / 4)] * 3
        prop-=sum(ps)
    return {
        'CHR': ps[0],
        'INT': ps[1],
        'STR': ps[2],
        'MNY': prop
    }

life = Life()

def on_error(e):
    raise e

def pick_talent(ts):

    while True:
        s = 1
        if s == '':
            return ts[0].id
        try:
            t = ts[int(s) - 1]
            return t.id
        except HandlerException as e:
            add_return(e)
        except Exception as e:
            add_return('无法识别，请重新选择')

def run():
    life.setErrorHandler(on_error)
    life.setTalentHandler(pick_talent)
    life.setPropertyhandler(genp)
    
    #from TalentManager import TalentManager
    #life.talent.talents.append(TalentManager.talentDict[1122])
    
    life.choose()
    
    add_return(f'\n本轮获得以下天赋：')
    for t in life.talent.talents:
        add_return(t)
    add_return(life.property)

    return life.run()

def lifemain():
    global returnit
    if returnit=="12345":
        life._init_managers()
    returnit = ""
    i = 0
    a=1
    for x in run():
        a+=1
        add_return(f'\n{x[0]}{"——".join(x[1:])}')
        if a==5:
            a=0
            add_return(" \n\n")
        if(0 < i):
            i-=1
            continue
#           if(msvcrt.getch() == b' '):
#               i = 9
    returnn=returnit
    returnit="12345"
    return returnn
if __name__=="__main__":
    while True:
        print(lifemain())
