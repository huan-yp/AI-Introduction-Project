AI_web.py 中
POST：
	传入一个value数组
	len(value)==5 且分别为
		任务名称（必有项，中英皆可,自动翻译为英文）
		开始时间（可为null）
		结束时间（可为null）
		描述，即内容（可为null）
		附加信息（可为null）
	[key,start_time,end_time,Description,added message] 
        E.g value=['成绩','20240905','20240905','94','English']
        all in string form

	返回值 为唯一的id和value

GET：
	可以用key（任务名称）获取所有该类型的数据
	也可以用id来获取确定的一组数据

	返回值为value

PUT：
	须提供id和修改后的value数组

	返回值为value

Trans.py 为腾讯云接口的翻译，百万字符内免费
Trans.slower 为自带库的翻译，缺点是较慢	