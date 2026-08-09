#!/usr/bin/env python3
"""DeepSeek API Demo — 从文本提取 3D 组件名称（OpenAI 兼容接口）。

用法：
    python apitest.py                            # 默认示例文本
    python apitest.py --text "你的文本"          # 指定文本
    python apitest.py --model deepseek-v4-flash  # 指定模型

需要环境变量 DEEPSEEK_API_KEY。
"""

import argparse
import os
import sys


def build_client(api_key=None, base_url="https://api.deepseek.com"):
    """构造 OpenAI 兼容客户端；缺少 API Key 时明确报错退出。"""
    key = api_key or os.environ.get("DEEPSEEK_API_KEY")
    if not key:
        sys.exit("❌ 未设置 DEEPSEEK_API_KEY 环境变量（export DEEPSEEK_API_KEY=your-key）")
    from openai import OpenAI

    return OpenAI(api_key=key, base_url=base_url)


def extract_components(text, model="deepseek-v4-flash", client=None):
    """调用 DeepSeek 提取文本中的组件名称，返回模型回答字符串。"""
    if client is None:
        client = build_client()
    messages = [
        {"role": "system", "content": "你是一个严谨的数据处理助手，负责提取文本里的 3D 组件名称。"},
        {"role": "user", "content": f"请提取这段话里的组件部位：'{text}'。"},
    ]
    response = client.chat.completions.create(model=model, messages=messages)
    return response.choices[0].message.content


def main():
    parser = argparse.ArgumentParser(description="DeepSeek API 3D 组件名称提取 demo")
    parser.add_argument("--text", default="人物的左手臂和身后的红色披风出现了穿模现象", help="要分析的文本")
    parser.add_argument("--model", default="deepseek-v4-flash", help="模型名")
    parser.add_argument("--base-url", default="https://api.deepseek.com", help="API 地址")
    args = parser.parse_args()

    try:
        answer = extract_components(args.text, args.model, build_client(base_url=args.base_url))
    except Exception as e:  # 网络/鉴权/限流等
        print(f"❌ 调用失败：{e}", file=sys.stderr)
        sys.exit(1)

    print("\n--- 大模型的回答 ---")
    print(answer)


if __name__ == "__main__":
    main()
