from api.chat import get_kimi_api_response
import requests

TABLE_NAME = "dialogue"
CHECK_DEL = "请分析以下文本是否包含删除任务的指令，并根据以下规则处理：\n"
CHECK_DEL += "1. 如果不是指令，返回 None。\n"
CHECK_DEL += "2. 如果是指令，检查数据库中是否存在对应的任务。\n"
CHECK_DEL += "   - 如果任务存在，执行删除并返回 (True, 删掉的任务, AI回复)。\n"
CHECK_DEL += "   - 如果任务不存在，返回 (False, None, AI回复)。\n"
CHECK_ADD = "请分析文本以下是否包含添加任务的指令，并根据以下规则处理：\n"
CHECK_ADD += "1. 如果不是指令，返回 None。\n"
CHECK_ADD += "2. 如果是指令，检查数据库中是否存在冲突的任务。\n"
CHECK_ADD += "   - 如果没有冲突，执行添加并返回 (True, 增加的任务, AI回复)。\n"
CHECK_ADD += "   - 如果存在冲突，返回 (False, None, AI回复)。"
CHECK_KEY = "以下任务的时间是什么时候（以年-月-日形式输出）"
UPDATE_HISTORY = "在任务列表中加入以下任务\n"

class UserTask:
    def __init__(self):
        pass

    def add_task(self, input_task):
        url = f'http://127.0.0.1:5000/{TABLE_NAME}'
        payload = {'key': get_kimi_api_response(CHECK_KEY + input_task), 'value': input_task}
        response = requests.post(url, json=payload)
        return response.json()
    
    def delete_task(self, input_task):
        url = f'http://127.0.0.1:5000/delete/{input_task}'
        response = requests.delete(url)
        return response.status_code
    
    def get_all_data(tablename):
        url = f'http://127.0.0.1:5000/by_table/{tablename}'
        response = requests.get(url)
        return response.json()
   

def try_del_task(text):
    table = UserTask()  
    history = ""
    list = table.get_all_data(TABLE_NAME)
    for task in list:
        history += task[3] + "\n"
    response = get_kimi_api_response(UPDATE_HISTORY + history + CHECK_DEL + text).split()
    if response.length() != 3:
        return None
    if response[0] == True:
        table.delete_task(response[1])
    return [response[0], response[1], response[2]]

def try_add_task(text):
    table = UserTask()  
    history = ""
    list = table.get_all_data(TABLE_NAME)
    for task in list:
        history += task[3] + "\n"
    response = get_kimi_api_response(UPDATE_HISTORY + history + CHECK_ADD + text).split()
    if response.length() != 3:
        return None
    if response[0] == True:
        table.add_task(response[1])
    return [response[0], response[1], response[2]]
