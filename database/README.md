# 一.环境配置与python库安装

- **Python版本**：3.12.7及以上  
  **须安装的库**: flask, flask_sqlalchemy, requests, pyyaml

> pip install flask flask_sqlalchemy requests pyyaml

# 二.主文件(AI_web.py)使用
## data.db数据库地址
通过修改`database/config.yaml`文件来修改数据库存储位置

## 运行方式
直接使用在任意python idle上运行该文件即可

# 三.数据库操作方式
## POST:

传入由你确定的 `tablename`(所属表的名称), `key`(可为任意字符串,唯一), `value`数组, 其中`len(value)<=5`, 且默认分别为：

- **任务名称**
- **开始时间**
- **结束时间**
- **描述**
- **附加信息**

不要求传入元素数一定为5,值为null的不会返回,你也可以自己定义他的内容,注意value<=5即可
例如：

- `value=['成绩', '20240905', '20240905', '94', 'English']`
  **各元素都为字符串**

**返回值**：成功添加后，将返回包含`tablename`唯一`key`和`value`的响应。

## GET：

- 可以用`tablename`获取所有该表的数据
  也可以用`tablename`, `key`来获取确定的一组数据
- **返回值**：包含`tablename`唯一`key`和`value`的响应。

## PUT：

- 须提供`tablename`, `key`和修改后的`value`数组
- **返回值**：包含`tablename`唯一`key`和`value`的响应。

## Delete：

- 提供`tablename`, `key`
- **返回值**：删除成功后，返回空响应（即HTTP状态码204，响应体为空）