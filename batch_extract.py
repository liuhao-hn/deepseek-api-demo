#!/usr/bin/env python3
"""批量提取：逐行读取文本文件，调用 DeepSeek 提取每行的 3D 组件名称。

用法：
    export DEEPSEEK_API_KEY=your-key
    python batch_extract.py --input texts.txt                    # 打印结果
    python batch_extract.py --input texts.txt --output out.txt   # 写文件
    python batch_extract.py --input texts.txt --model deepseek-v4-flash
"""

import argparse
import sys
from pathlib import Path

from apitest import build_client, extract_components


def extract_lines(lines, model="deepseek-v4-flash", client=None):
    """对每行文本提取组件，返回 [(原文, 组件回答), ...]；跳过空行。"""
    if client is None:
        client = build_client()
    results = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        answer = extract_components(line, model=model, client=client)
        results.append((line, answer))
    return results


def main():
    parser = argparse.ArgumentParser(description="批量从文本文件提取 3D 组件名称")
    parser.add_argument("--input", required=True, help="输入文本文件（每行一条）")
    parser.add_argument("--output", help="输出文件（默认打印到 stdout）")
    parser.add_argument("--model", default="deepseek-v4-flash", help="模型名")
    args = parser.parse_args()

    lines = Path(args.input).read_text(encoding="utf-8").splitlines()
    try:
        results = extract_lines(lines, args.model)
    except Exception as e:  # 网络/鉴权/限流
        print(f"❌ 批量提取失败：{e}", file=sys.stderr)
        sys.exit(1)

    out_lines = [f"{src}\t→\t{ans}" for src, ans in results]
    if args.output:
        Path(args.output).write_text("\n".join(out_lines) + "\n", encoding="utf-8")
        print(f"已写入 {args.output}（{len(results)} 条）")
    else:
        print("\n".join(out_lines) or "（无有效输入行）")


if __name__ == "__main__":
    main()
