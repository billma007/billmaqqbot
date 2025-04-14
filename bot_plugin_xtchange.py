
from openai import OpenAI
#try:
#    from save_settings import get_value
#    deepseek_client = OpenAI(api_key=get_value("deepseekapi"), base_url="https://api.deepseek.com")
#except:
deepseek_client = OpenAI(api_key="sk-8d3e30510ed84b28a07eb8526fae2962", base_url="https://api.deepseek.com")
def deepseek_chat(keyword,role = """我接下来会给你一些句子，请你帮我转化成下列格式：
语气词+回车
前因+回车
现在的情况


例如：
我下一首要打的X居然是完美挑战曲，怎么办，转化成：
我tm
下一个要打的x居然是完美挑战曲
那可难办

我tm的
今天在hll出勤断网了
那可咋办

特别的，如果句子中没有语气词，可以加上一个比较激烈的语气词，比如：我tm，我草之类的      
            """):
    response = deepseek_client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": role},
            {"role": "user", "content": keyword},
        ],
        stream=False
    )
    return response.choices[0].message.content


if __name__=="__main__":
    while True:
        print(deepseek_chat(input()))