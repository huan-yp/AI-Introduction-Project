## AI 导论大作业

### 文件结构

```
├── action (主动行为)
│
├── api (语音服务、大模型接口)
│
├── bin (编译好的语音唤醒主程序相关运行文件)
│
├── database (数据库接口)
│
├── listen (语音唤醒检测器)
│
├── presentation (论文)
│
├── task (任务处理接口)
│
├── utils (工具类)
|
├── config_example.yaml (示例配置文件)
|
├── main.py (主程序)
```

### 相关使用

#### 填写配置文件

填写 `config_example.yaml` 文件, 将其重命名为 `config.yaml`.

```yaml
MOONSHOT_API_KEY: your_key # kimi 接口 https://platform.moonshot.cn/console/account
WAKE_APP_ID: your_id # 科大讯飞语音唤醒 https://www.xfyun.cn/services/AIkit_awaken
FISH_AUDIO_KEY: your_key # FISH_AUDIO tts 服务 https://fish.audio/zh-CN/text-to-speech/
FISH_AUDIO_MODEL_ID: your_id # 同上, 所用模型的 ID
TENCENT_ID: your_id # 腾讯 asr appid https://cloud.tencent.com/document/product/1093/48982
TENCENT_SECRET: your_secret # 同上, secret
TENCENT_KEY: your_key # 同上, key
```

#### 启动数据库服务

参考 [数据库服务](database/README.md)

#### 启动语音唤醒

双击 `bin/wakeup.exe` 开启语音唤醒服务.

#### 启动小妍

```
python main.py
```

启动小妍主程序.