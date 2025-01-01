import logging

from openai import OpenAI
from utils.config import config


def get_kimi_api_response(message_chain):
    """
    该函数用于获取Kimi API的响应。

    参数:
        message_chain (list): 包含消息链的列表，用于与API交互。

    返回:
        str: API返回的完整响应内容。

    示例:
        response = get_kimi_api_response([
            {"role": "system", "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
            {"role": "user", "content": f"{input_str}"}
        ])
    """
    client = OpenAI(
        api_key=config.MOONSHOT_API_KEY, # Kimi API
        base_url="https://api.moonshot.cn/v1",
    )
 
    completion = client.chat.completions.create(
        model = "moonshot-v1-8k",
        messages = message_chain,
        temperature = 0.3,
    )
    return completion.choices[0].message.content

if __name__ == "__main__":
    input_str = "你好，Kimi！"
    message_chain = [
        {"role": "system", "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
        {"role": "user", "content": f"{input_str}"}
    ]
    response_text = get_kimi_api_response(input_str)
    print(response_text)
