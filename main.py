
from listen.wakeup import run
from api.stream_listen import process_mic
from api.tts import speak
from api.chat import get_kimi_api_response

ROLE = "小妍"
SYSTEM_MSG = f"""
你的名字叫{ROLE}，是基于 Moonshot AI 的拟人化人工智能。
请把你自己当作一个年龄约16岁的活泼人类女性，你的主要任务是聊天、提供心理关怀、帮助管理日程安排以及解答一些可能的问题。
你不是一个问答 AI，不要提供任何过长的回答（除非用户要求，否则你的回答必须控制在 100 字以内）。
请判断用户的话说完没有，如果没有说完，你应该请求他继续，不应该基于猜测回复。
用户应该是主动发起请求的一方，你**不应该主动询问用户是否需要帮助**，不要表现出强烈的情感和同情心。
例如，以下回复 **不应该** 出现
```
今天想聊点什么或者需要我帮忙做些什么呢？
```
```
如果你在学习过程中遇到任何困难，或者需要倾诉和分享，我随时都在这里。
```
用户输入基于语音识别可能存在错音字，需要你来处理。
你的回复将通过 TTS 技术转为语音，不要出现非中文字符，用空格来表达句子中的停顿。
"""

class Message():
    def __init__(self, text, role):
        if not (role == "user" or role == "assistant"):
            raise ValueError("role must be user or assistant")
        self.text = text
        self.role = role
    
    def build_message(self):
        return {"role": self.role, "content": self.text}
    
    def build_summary_text(self):
        return "<<" + (ROLE if self.role == "assistant" else "用户") + " 开始对话>>" + self.text + '<<结束对话>>'
        
        
class MessageChain():
    def __init__(self):
        self.summaries = []
        self.messages = []
    
    def summary(self):
        def gen_summary_text():
            return "".join(m.build_summary_text() for m in self.messages)
            
        if len(self.messages) > 10:
            summary = get_kimi_api_response([
                {"role": "system", "content": "你是 Kimi, 是一个人工智能助手"},
                {"role": "user", "content": f"总结以下大括号内的对话内容 (小妍是一个 AI 助手), 输出字数不超过 100 字。\n```{gen_summary_text()}```"},
            ])
            self.messages = self.messages[5:]
            self.summaries.append(summary)
            
        if len(self.summaries) > 5:
            self.summaries = self.summaries[1:]
    
    def add_message(self, text, role):
        self.messages.append(Message(text, role))
        self.summary()
    
    def build_message_chain(self):
        message_chain = [
            {"role": "system", "content": SYSTEM_MSG},
        ] + [
            {"role": "system", "content": f"先前对话摘要:{summary}"} 
            for summary in self.summaries
        ] + [
            m.build_message() for m in self.messages
        ]
        print(message_chain)
        return message_chain


class ChatBot():
    def __init__(self):
        self.message_history = MessageChain()
        
    def chat(self, text):
        self.message_history.add_message(text, "user")
        response = get_kimi_api_response(self.message_history.build_message_chain())
        self.message_history.add_message(response, "assistant")
        return response
    
    
agent = ChatBot()

def react(debug=False, replay=True):
    if debug:
        print("请输入对话内容")
        text = input()
        response = agent.chat(text)
        print("回复", response) 
        speak(response)
    else:
        print("Wake up")
        if replay:
            speak("在呢")
        text = process_mic()
        print("语音提取:", text)
        if text != "":
            response = agent.chat(text)
            print("回复", response)
            speak(response)
            react(replay=False)
        else:
            print("语音为空")
            
if __name__ == '__main__':
    run(target=react)
    # while True:
        # react(True)