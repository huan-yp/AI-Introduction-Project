from api.api import get_kimi_api_response as api
import time
import database.AI_web
from datetime import datetime

def care_decides():
    if not hasattr(care_decides, "care_record"):
        care_decides.care_record = []
    message = ""
    current_time = datetime.now()
    current_time = str(current_time.strftime("%Y-%m-%d %H:%M:%S"))
    message += ( 
        "你需要根据该用户的近期日程安排与活动对他/她主动进行一些关心或者问候,"
        "该用户的个人信息，近期日程安排与活动是："
        )        

    content=database.AI_web.get_by_key('成绩')
    for buffer in content:
        for buff in buffer:
            message += buff
        message +='\n'

    message += "\n现在时间是"
    message += current_time

    if not care_decides.care_record:
        message += "\n你此前尚未问候过该用户\n"
    else:
        message += "你此前对该用户进行的问候时间与问候是：\n"
        for mess in care_decides.care_record:
            message += mess

    message += "请决定下次对用户进行问候的时间与相关的问候内容\n"
    message += (
        "要求：请将时间以相同于2024-11-23 08:55:29的格式写在最前面，"
        "在其后方用一个|符号与问候内容进行分割\n"
        "例如：2024-12-06 08:00:00|早上好，李华！新的一周又开始了，"
        "希望你今天充满活力。记得今天有数学课和英语课，准备好了吗？"
        "另外，我注意到你之前线性代数考试的成绩出来了，"
        "虽然你觉得自己没有发挥好，但84分已经很不错了，不要对自己太苛刻。"
        "工科数学分析的成绩还没公布，我相信你一定可以的。加油，期待你更好的表现！"
        )
    response = api.get_kimi_api_response(message)
    care_decides.care_record.append(response)
    response = response.split("|")
    return response
if(__name__!="__main__"):
    print(care_decides())
