from api.chat import get_kimi_api_response as api
import time
import requests
from datetime import datetime
url = "http://127.0.0.1:5000/by_table/"
delete_url="http://127.0.0.1:5000/delete/decides/"
prompt = """
 任务要求: 你需要根据现在的时间,
 用户目前的行程安排和之前已经做出的主动交流决定,
 判断现在是否需要再加一次主动交流或暂时不需要更多的主动交流
 又或是用户的行程安排发生了改变，需要删除之前作出的主动交流决定
 主动交流内容包括对用户目前的任务做时间提醒, 日常问候, 或者情感关怀
 若不需要更多的主动交流, 你只需要返回 false 这个单词就好
 若需要新增一次主动交流, 你需要返回两块内容:
 首先, 是下一次主动交流的时间,
 请将时间以相同于2024-11-23 08:55:29的格式给出,
 然后, 是主动交流的内容.
 在两块内容之间, 以一个 | 符号作为分隔
 若需要删除某个标号所对应的，尚未执行的主动交流决定
 你需要返回 delete 这个单词和决定的标号, 中间用|分割
 注意: 若后方的日程安排,聊天记录或主动交流决定后面没有记录,
 表示目前暂无内容, 并非异常情况
 尽量避免在同一个时间点作出多次相同的主动交流
 作为ai伴侣, 尽量主动一些, 也可以根据用户反馈作出调整,
 下方为一些回复示例:
 eg1. (调用时恰好是中午) -> 2024-12-06 12:00:00|喵喵喵, 主人记得吃饭哦.
 eg2. (调用时发现某个 Task 的开始时间快到了) -> 2024-12-06 14:00:00|主人记得去开会哦, 今天下午五点
 eg3. (调用时发现最近的对话信息中用户情绪不对劲) -> 2024-12-07 22:00:00|有什么难过的事情吗?小妍可以听听吗?一个人憋着很难受吧...
 eg4. (调用时发现没什么可说的/之前主动交流决定记录中以及有过类似问候了) -> false
 eg5. (调用时发现标号为 12 的,目前 尚未执行 的主动交流决定因为日程变动而不再合适 -> delete|12
 """
def process(returned):
    message = ''
    if(isinstance(returned,list)):
        for item in returned:
            message += item['key'] 
            message += ' '     
            for val in item['value']:
                message += val
                message += ' '
            message += '\n'
    else:  
        if (returned['error']=='Table is not existed'):
            return message
        message += returned['key']
        message += ' '
        for val in returned['value']:
            message += val
            message += ' ' 
        message += '\n'

    return message
        
def next_active():

    message = ""
    response=[]
    message += prompt
    chain = []
    dic = {}  
    dic["role"] = "system"

    current_time = datetime.now()
    current_time = str(current_time.strftime("%Y-%m-%d %H:%M:%S"))
    message += "现在时间是:"
    message += current_time
    
    dialogue = requests.get(url+"dialogue")
    dialogue = dialogue.json()
    message += "\n此前的对话记录是\n"

    message += process(dialogue)

    task = requests.get(url+"Task")
    message += "\n默认的任务属性为 任务名称 开始时间 结束时间 描述 附加信息 但是不一定如此\n"
    message += "目前用户的日程安排是:\n"
    task = task.json()
    message += "\nTask: \n"

    message += process(task) 

    decides = requests.get(url+"decides")
    message += "\n此前作出过的主动交流决定时间及其内容为:\n"
    decides = decides.json()

    message  += process(decides)
    #print(message)
    dic["content"] = message
    chain.append(dic)

    reply = api(chain)
    print(reply)
    time.sleep(30)

    if(reply=="false"):
        response=[False,"",current_time]
        return response
    
    reply = reply.split("|")
    if(reply[0]=="delete"):
        requests.delete(delete_url+reply[1])
        response=[False,"",current_time]
        return response
        
    response.append(True)
    response.append(reply[1])
    response.append(reply[0])
    
    key = hash(reply[1])
    key = str(abs(key))
    data={}
    data["table"] = "decides"
    data["key"] = key
    data["value"] = [reply[1],reply[0]]

    url_post = f'http://127.0.0.1:5000/{data["table"]}'
    url_create =f'http://127.0.0.1:5000/creattable/{data["table"]}'
    requests.post(url_create,json=data)
    requests.post(url_post,json=data)

    return response    

if(__name__=="__main__"):
    print(next_active())
