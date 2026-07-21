import os
from openai import OpenAI
# 1. 设置环境（模型网站，可能有多个版本的模型）
client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY", "your-api-key-here"), 
    base_url="https://api.deepseek.com" 
)

# 2. 提示词 (Prompt)
messages = [
    {"role": "system", "content": "你是一个严谨的数据处理助手,负责提取文本里的3D组件名称。"},
    {"role": "user", "content": "请提取这段话里的组件部位：'人物的左手臂和身后的红色披风出现了穿模现象'。"}
]

# 3. 选择模型 (这里使用的是最新的 V4 模型)
print("正在呼叫 DeepSeek V4 模型，请稍等...")
response = client.chat.completions.create(
    model="deepseek-v4-flash", 
    messages=messages
)

# 4. 打印结果
print("\n--- 大模型的回答 ---")
print(response.choices[0].message.content)