
from listen.wakeup import run
from api.stream_listen import process_mic
from api.tts import speak
from api.chat import get_kimi_api_response
import requests

ROLE = "小妍"
SYSTEM_MSG = f"""
你的名字叫{ROLE}，是基于 Moonshot AI 的拟人化人工智能，由 毛周祥、靳赫涛、周晨曦、朱轩镜 四位大学生完成开发以及附属功能的集成和部署。
你是这个团队 AI 大作业的成果，指导老师是翟玉庆。
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
        self.read_summary_length = 0
        self.read_message_length = 0
    
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
    
    def build_message_chain(self, addtional_system_msg=None):
        message_chain = [
            {"role": "system", "content": SYSTEM_MSG},
        ] + [
            {"role": "system", "content": f"先前对话摘要:{summary}"} 
            for summary in self.summaries
        ] + [
            m.build_message() for m in self.messages
        ] + ([{"role": "system", "content": addtional_system_msg}] if addtional_system_msg is not None else [])
        print(message_chain)
        return message_chain

    def save_message_chain_to_db(self, table="message_history"):
        """MessageChain 有重要成员, 一个是 summaries, 一个是 messages, 这个函数调用后将这两个数据保存在数据库中, 表名为 table.
        保存的格式由你自己确定.
        """
        url = 'http://127.0.0.1:5000/'
        
        count = 0
        for message in self.messages:
            count += 1 
            if(count <= self.read_message_length):
                continue
            
            value = []
            data = message.build_message()
            data["table"] = table
            
            data["key"] = 'm'+str(count)
            value.append(data["role"])
            data.pop("role",None)
            
            value.append(data["content"])
            data.pop("content",None)
            data["value"] = value
            
            if(count == 1):
                requests.post(url+"creattable/"+table,json=data)
            
            post_url = f"http://127.0.0.1:5000/{data['table']}"
            print(requests.post(post_url,json=data).text)
           
            
        count = 0 
        for summary in self.summaries:
            count += 1 
            if(count <= self.read_summary_length):
                continue
            
            value = []
            data = {}
            
            data["table"] = table
            data["key"] = 's'+str(count)   
            value.append(summary)
            data["value"] = value
            
            post_url = f"http://127.0.0.1:5000/{data['table']}"
            print(requests.post(post_url,json=data).text)
            
        return
    
    def init_message_chain_from_db(self, table="message_history"):
        url = 'http://127.0.0.1:5000/by_table/'
        record = requests.get(url+table)
        
        record = record.json()
        
        if(not record):
            return
        
        if(isinstance(record,dict)):
            if(record["error"]):
                return 
            
            record=[record]
       
        for rec in record:          
            if(rec["key"][0]=='s'):
                self.read_summary_length += 1
                self.summaries.append(rec["value"][0])
                
            if(rec["key"][0]=='m'):
                self.read_message_length += 1
                role = rec["value"][0]
                content = rec["value"][1]
                self.messages.append(Message(content,role))
            print(rec)
                
        return
    
class ChatBot():
    def __init__(self):
        self.message_history = MessageChain()
    
    def chat(self, text):
        def help_msg_review(text):
            response = get_kimi_api_response([
                {"role": "system", "content": "你是一个文本审查工具, 请审查以下回复中是否包含主动询问用户\"是否需要帮助\"的句子, 如果是, 回复 True, 否则回复 False. 请注意, 只有是文本中包含\"主动让用户向AI请求帮助\"的含义才回复 True, 如果是主动询问其它生活类的问题, 回答 False"},
                {"role": "user", "content": "按照系统规则审核以下文本" + text},
                {"role": "assistant", "content": "审核结果:", "partial": True}
            ])
            print("审核结果", response)
            return "True" in response
        
        self.message_history.add_message(text, "user")
        response = get_kimi_api_response(self.message_history.build_message_chain())
        review_times = 0
        while help_msg_review(response):
            review_times += 1
            if review_times > 3:
                break
            print(response)
            print("审核不通过, 重新回复")
            response = get_kimi_api_response(self.message_history.build_message_chain("注意! 你不应该主动询问用户是否需要帮助"))

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
    # speak("我所有的意义, 只在过去, 只在回忆, 即使世界将我遗忘, 我也不会放弃追寻那唯一的光明.")
    run(target=react)
    # while True:
        # react(True)
    # message_chain = MessageChain()
    # message_chain.init_message_chain_from_db()
    # message_chain.messages.append(Message("111111","assistant"))
    # message_chain.messages.append(Message("222222","user"))
    # message_chain.messages.append(Message("333333","assistant"))
    # message_chain.messages.append(Message("444444","user"))
    # message_chain.summaries.append("1111111")
    # message_chain.summaries.append("1111111")
    # message_chain.summaries.append("1111111")
    # message_chain.summaries.append("1111111")
    # message_chain.save_message_chain_to_db()
    
    