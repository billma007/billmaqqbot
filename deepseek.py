
from openai import OpenAI
from save_settings import get_value
deepseek_client = OpenAI(api_key=get_value("deepseekapi"), base_url="https://api.deepseek.com")
def deepseek_chat(keyword,role = "你是一个帮忙解决用户问题的助手"):
    response = deepseek_client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": role},
            {"role": "user", "content": keyword},
        ],
        stream=False
    )
    return response.choices[0].message.content