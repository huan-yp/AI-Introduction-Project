import re
import jieba
import jieba.analyse

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


# 定义提取时间信息的函数 返回一个时间列表
def extract_time(text):
    # 正则表达式匹配年月日
    time_pattern = r'\b(\d{4}-\d{1,2}-\d{1,2}|\d{1,2}-\d{1,2}-\d{4}|\d{1,2}:\d{1,2}(:\d{1,2})?)\b'
    time_matches = re.findall(time_pattern, text)
    if time_matches: 
        return time_matches
    else:
        return -1
# 支持 年-月-日 月-日-年 分-秒的表达
# 定义提取任务信息的函数 返回一个关键词列表
def extract_task(text):
    task_keywords = ['作业','考试','出行','比赛','活动']
    extracted_keywords = []
    for keyword in task_keywords:
        if keyword in text:  # 检查关键词是否在文本中
            extracted_keywords.append(keyword)  # 添加找到的关键词到列表中
    if extracted_keywords:
        return extracted_keywords
    else:
        return -1
# 使用函数的示例
input_str = "你好，Kimi！"
response_text = get_kimi_api_response(input_str)
print(response_text)