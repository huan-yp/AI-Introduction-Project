# mySQL使用文档
本文档将指导您如何操作本文件夹数据库
# 一.环境配置

- **Python版本**：3.12.7及以上  
  **须安装的库**: flask, flask_sqlalchemy, requests, pyyaml 
> pip install flask flask_sqlalchemy requests pyyaml  

  **data.db数据库地址**:修改`database/config.yaml`文件内容为你设定的存储位置  
  例如:`E:/Code/Python/AI-Introduction-Project/database/data.db`

# 二.数据库运行

直接在任意python idle上运行`AI_web.py`文件即可

# 三.接入方式
database通过 HTTP 接口对外提供数据存储服务。  
database HTTPS 地址:
http://+ 你的主机ip(一般为127.0.0.1:5000)  

> 例如  
http://127.0.0.1:5000

数据库支持以下操作: 
- **creat**:创建一个新的表
- **post**:向已有的表中传入一组数据
- **get**:查询一个表中所有数据或者查询一组特定数据
- **put**:更新已有的一组数据
- **delete**:删去已有的一组数据

### 可以参考`Input_Terminal.py`中的函数操作数据库
例如:
    
```
def creat(data):
    url = f'http://127.0.0.1:5000/creattable/{data['table']}'
    response = requests.post(url, json=data)
    print(response.text)
```
# 四.输入参数
## creat:  
http://127.0.0.1:5000/creattable/ + 你的表名(tablename)  
例如 `http://127.0.0.1:5000/creattable/成绩`  
**每个表须先创建再进行其他操作,否则会返回**`Table is not existed`
## POST:
http://127.0.0.1:5000/ + 你的表名(tablename)  
例如 `http://127.0.0.1:5000/成绩`  
传入由你确定的 `tablename`(所属表的名称), `key`, `value`数组  

`key`的值由用户确定,且同一个表中的任一组数据`key`必须**唯一**  
`value`所含元素(可为空)不超过五个, 且默认分别为：

- **任务名称**
- **开始时间**
- **结束时间**
- **描述**
- **附加信息**

例如：

- `value=['成绩', '20240905', '20240905', '94', 'English']`
  **各元素都为字符串**

**返回值**：成功添加后，将返回包含`tablename`,`key`和`value`的响应。  
例如：

>  {  
  "key": "1",  
  "table": "成绩",  
  "value": [ 
    "英语考试",
    "20240101",
    "20240101", '94', 'English'
  ]  
}  

`value`中值为null的不会返回,你也可以自己定义他的内容  
例如：

>  {  
  "key": "1",  
  "table": "129874698",  
  "value": [ 
    "123",
    "123"
  ]  
}  


## GET：
### 1.查询一个表中所有数据
http://127.0.0.1:5000/by_table/ + 你的表名(tablename)  
例如 `http://127.0.0.1:5000/by_table/成绩`  
- **返回值**：n组(n为表中数据组数) 包含`tablename`,`key`和`value`的响应, 与`post`返回值相同。

### 2.查询一个表中一组特定数据
http://127.0.0.1:5000/by_key/ + 你的表名(tablename) + /你的key值  
例如 `http://127.0.0.1:5000/by_key/成绩/1` 
- **返回值**：1组包含`tablename`,`key`和`value`的响应,与`post`返回值相同。

## PUT：
http://127.0.0.1:5000/put/ + 你的表名(tablename) + /你的key值  
例如 `http://127.0.0.1:5000/put/成绩/1`  
- 须提供`tablename`, `key`和修改后的`value`数组

**注意** 这组数据必须原本就存在
- **返回值**：包含`tablename`,`key`和`value`的响应。

## Delete：
http://127.0.0.1:5000/delete/ + 你的表名(tablename) + /你的key值  
例如 `http://127.0.0.1:5000/delete/成绩/1` 
- **返回值**：删除成功后，返回空响应（即HTTP状态码204，响应体为空）

# 五.常见问题
1.**为什么我无法创建db**  
请确认`database/config.yaml`文件中的地址合法  
2.**为什么我无法通过post上传数据**  
请确认在post之前您已经通过creat创建了一个表并且传入了正确格式的数据  