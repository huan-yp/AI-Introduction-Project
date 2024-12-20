from openai import OpenAI

def get_kimi_api_response(input_string):
    client = OpenAI(
    api_key="sk-qeSybUg1d0nhy8h89zx4oX998K7wCFFXos0P3aKK67Nb5NVd", # 在这里将 MOONSHOT_API_KEY 替换为你从 Kimi 开放平台申请的 API Key
    base_url="https://api.moonshot.cn/v1",
)
 
    completion = client.chat.completions.create(
        model = "moonshot-v1-8k",
        messages = [
            {"role": "system", "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
            {"role": "user", "content": f"{input_string}"}
        ],
        temperature = 0.3,
    )
    return completion.choices[0].message.content


# 使用函数的示例
input_str = "你好，Kimi！"
response_text = get_kimi_api_response(input_str)
print(response_text)