from openai import OpenAI
if_inbot = True
deepseek_api = "your api key"
if __name__=="__main__":
    if_inbot = False
if if_inbot:
    from save_settings import get_value
    client = OpenAI(api_key=get_value("deepseekapi"), base_url="https://api.deepseek.com")
else:
    client = OpenAI(api_key=deepseek_api, base_url="https://api.deepseek.com")
hgt_doing = {"group_id": ["msg",[],0]}
now_start_group = []
hgt_example = '''1、《闺蜜》
汤面：毕业后，和学校里的闺蜜一直未见。那天她来找我了，但随着啪的一声…我们阴阳相隔。

汤底：曾经的她是我在盲人学校里最好的闺蜜，毕业后便各奔东西，我很幸运的接受了复明手术，而她却没有这种幸运，许久未见的她说来找我，我满怀期待可打开门后，曾经最熟悉的声音竟然是从一个样子丑陋的男人口中发出，顿时让我作呕，我怎能忍受这样的欺骗，于是我便把他引向了天台...

2、《生日礼物》
汤面：我参加了最喜欢的作家的生日会。生日会结束后，我心满意足的回到家。可当作家也回到家后…我疯了。

汤底：我是一个心理变态的偷窥狂，喜欢看恐怖小说。我最喜欢的恐怖小说作者写的小说都是关于杀人，分尸一类的，写的都很真实很残暴，我很爱看。那天，我去参加了作者的生日会，并送了一只装了摄像头的笔作为礼物，作者笑纳了。生日会结束后，作者拿出我送的礼物。我通过礼物上的摄像头看到了作者家的场景：墙上挂满了人头四肢，地板上全是血。我被吓的发疯了，原来他写的不仅仅是恐怖小说，还是他自己的传记…

3、《好“兄弟”》
汤面：她喜欢男人很久了。有一天，她终于鼓起勇气对他表白了，但是男人对她说了一句话…她瞬间就崩溃了。

汤底：他们是从小一起长大的好兄弟，但是他对男人一直有不一样的感情，他一直很想和他在一起，所以他去做了变性手术，变性后的她站在男人面前表白，男人看着她却说道：“我喜欢原来的你。”


4、《新娘》
汤面：新娘子穿着白纱，缓步走在红地毯上。终于到了交换戒指的时刻…她却突然死掉了。

汤底：新娘穿的婚纱是从二手店买来的。将婚纱卖给二手店的人，是一个殡葬业者。他将死人的衣服偷走拿去卖，借此赚了一笔不小的外快。但是他没有想到，这件婚纱里渗透了高浓度的防腐剂，会使穿这件衣服的人，因为防腐剂渗入皮肤而死。

5、《破案》
汤面：我和朋友正聊着最近的案子，顺便聊了聊他口干舌燥但什么都没问出来的事，当我回到家后…我吓昏了过去。

汤底：我是一名心理医生，那天局里安排我为一名在灭门惨案中幸存下来的男人做心理辅导，可是我无论说什么，他都始终保持沉默。直到我说出了: 你的遭遇我感同身受时，他却突然抬起头冲我笑了一下，我不明白他在笑什么，直到我回到家，打开门的那瞬间，看到墙上用血写着: 现在你才能感同身受。


6、《崇拜》
汤面：男孩十分崇拜他的父亲。有一天，他将他的妈妈杀害了，并对爸爸说了一句话，爸爸听后便自杀了。

汤底：男孩的爸爸是一位魔术师、经常表演用刀切开人体后，再复活的魔术。男孩因为年龄小，就信以为真。一天，爸爸不在家，男孩便尝试用妈妈来制作这个魔术，他不会表演魔术，所以男孩真的将妈妈切开了。等到爸爸回来的时候，男孩就跟爸爸说：“你快把妈妈变回来。”爸爸看到眼前这个场景，再看到儿子若无其事的样子，便自杀了。

8、《午夜》
汤面：

离午夜还有五分钟

一个男子上了列车，但他的神情很奇怪

他看了看车上的几个人，然后开始问起乘客的年龄

“女士 您今年28岁吗?”“你怎么知道?”

“先生 您今年55吗?”“恩。”

然后男人一个个地猜对了乘客的年龄

“婆婆 您今年69岁吗?”

“不是的 但再过5分钟我就69岁了。”

男子听完，脸色惨白。

汤底：男子可以看见别人的死亡日期！这位婆婆69岁时就会去世！这代表过5分钟， 车会出车祸，在车上的人都会去世。'''
def hgt_main(msg, group_id=None):
    roundnum = 0
    ifin = False
    if group_id is None:
        return "请在群聊中使用该功能。"
    group_id = str(group_id)
    if group_id not in now_start_group:
        now_start_group.append(group_id)
        hgt_doing[group_id] = ["","",""]
        roundnum = 1
        hgt_doing[group_id][2] = roundnum
    roundnum = hgt_doing[group_id][2]
    if "开始" in msg:
        if roundnum == 1:
            roundnum = 2
            hgt_doing[group_id][2] = roundnum
            return round1(msg, group_id)
        else:
            return "游戏已经开始，请继续回答。"
    elif "提问" in msg:
        if roundnum == 2 or roundnum == 3:
            roundnum = 3
            hgt_doing[group_id][2] = roundnum
            return round2(str(msg).replace(".bot","").replace("。bot","".replace(" ","").replace("提问","")).replace("海龟汤",""), group_id)

        else:
            return "当前游戏不在这个阶段。" 
    
    elif "猜答案" in msg:
        if roundnum == 2 or roundnum == 3:
            return round3(str(msg).replace(".bot","").replace("。bot","".replace(" ","").replace("猜答案","")).replace("海龟汤",""), group_id)
        else:
            return "当前游戏不在这个阶段。"
    elif "结束" in msg:
        return roundend(group_id)
    

    return "指令错误。"

    

def round1(msg, group_id):
    messages = [{"role": "user", "content": "来个海龟汤。请注意只需要输出海龟汤汤面，不要输出其他东西（包括汤底）。海龟汤尽量难一点.我将会给你几个海龟汤示例：\n" + hgt_example}]
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages
    )

    messages.append(response.choices[0].message)
    hgt_doing[group_id][1] = messages
    return response.choices[0].message.content

# Round 2
def round2(msg,group_id):
    messages = hgt_doing[group_id][1]
    messages.append({"role": "user", "content": "我现在要基于海龟汤的汤面进行提问了。我的问题是：" + msg + "。你只能回答：是，否，部分正确。如果提问者的提问不能用以上三种回答方式回答，请回答：无法回答。请严格按照刚刚的要求回复"})
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages
    )

    messages.append(response.choices[0].message)
    hgt_doing[group_id][1] = messages
    return response.choices[0].message.content

def roundend(group_id):
    messages = hgt_doing[group_id][1]
    messages.append({"role": "user", "content": "现在我结束这个游戏了。请告诉我最终的答案和推理过程。我只需要答案和推理本身，不需要其他内容。你需要注意的是，返回的值是这个海龟汤的答案！返回的不是FALSE！！！"})
    print(messages)
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages
    )
    print(response)
    now_start_group.remove(group_id)
    hgt_doing.pop(group_id)
    return "游戏已结束。答案是：\n" + response.choices[0].message.content

def round3(msg, group_id):
    messages = hgt_doing[group_id][1]
    messages.append({"role": "user", "content": "我现在要猜测答案了。答案是：" + msg + "。如果我的答案和正确的答案相差很大或者我的答案和海龟汤没有关系，请返回FALSE（需要注意只能返回FALSE，不要返回其他内容）。如果我的答案和正确的答案相差不大，请告诉我我的答案和正确答案基本正确，并告诉我最标准的正确答案"})
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages
    )
    if "FALSE" in  response.choices[0].message.content:
        messages.append(response.choices[0].message)
        hgt_doing[group_id][1] = messages
        return "你的答案是错误的。"
    else:
        returnit =  "你的答案是正确的。正确答案是：" + response.choices[0].message.content
        now_start_group.remove(group_id)
        hgt_doing.pop(group_id)
        return returnit
        
    

if __name__ == "__main__":
    while True:

        msg = input("输入：")
        print(hgt_main(msg, group_id=1))

