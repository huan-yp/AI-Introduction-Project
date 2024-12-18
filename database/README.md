

# 一.环境配置与python库安装

- python版本：3.12.7及以上  
  **须安装的库**:flask,flask_sqlalchemy,Trans,requests,tencentcloud-sdk-python

> pip install flask,flask_sqlalchemy,Trans,requests,tencentcloud-sdk-python

# 二.腾讯云获取翻译密钥

- 在[腾讯云](https://console.cloud.tencent.com/cam/capi)
  注册完自己的账户后可以申请一个免费密钥，200w字符翻译免费
  并在**Trans.py**中用你的密钥来替代SecretId和SecretKey
  
  ~~你也可以使用Trans_slower.py来替代Trans.py文件，无需密钥，但速度慢~~

# 三.主文件(AI_web.py)使用
## data.db地址
通过修改代码第六行中
> app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///E:/Code/Python/data.db'#data.db存储位置

的绝对地址来修改
## POST:

传入一个value数组

len(value)==5 且分别为

> 任务名称（必有项，中英皆可,自动翻译为英文）
> 开始时间（可为null）
> 结束时间（可为null）
> 描述，即内容（可为null）
> 附加信息（可为null）

- value=[key, start_time, end_time, Description, added message]

---

E.g

- value=['成绩', '20240905', '20240905', '94', 'English']
  **各元素都为字符串**

```
返回值 为唯一的id和value
```

## GET：



- 可以用key（任务名称）获取所有该类型的数据
  也可以用id来获取确定的一组数据
- 返回值为value


## PUT：


- 须提供id和修改后的value数组
- 返回值为value



## Delete:

- 提供id
- 返回值为 ‘’ （即为空）
