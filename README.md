# DeepSeek API Demo

![CI](https://github.com/liuhao-hn/deepseek-api-demo/actions/workflows/ci.yml/badge.svg)

A minimal Python demo calling DeepSeek V4 API to extract 3D component names from text, using the OpenAI-compatible SDK.

## 特性

- 可测试的 `extract_components()` 函数（单测用 mock，不消耗 API 额度）
- 缺少 API Key 时给出明确报错
- 支持 `--text` / `--model` / `--base-url` 参数
- 网络/鉴权异常友好提示

## Usage

```bash
export DEEPSEEK_API_KEY="your-api-key"
python apitest.py                        # 默认示例文本
python apitest.py --text "你的文本"       # 指定文本
python apitest.py --model deepseek-v4-flash

# 批量提取：逐行读取文件
python batch_extract.py --input texts.txt                    # 打印
python batch_extract.py --input texts.txt --output out.txt   # 写文件
```

## Example

```
Input:  "人物的左手臂和身后的红色披风出现了穿模现象"
Output: 左手臂, 红色披风
```

## Test

```bash
python -m unittest tests.test_apitest    # mock API，无需真实调用
```

## License

MIT
