import re


def full_to_half_re(text):

    text = re.sub(r'\u3000', ' ', text)
    text = re.sub(
        r'[\uFF01-\uFF5E]',
        lambda x: chr(ord(x.group(0)) - 0xFEE0),
        text
    )
    fullwidth_punctuation = {
        '，': ',',
        '。': '.',
        '；': ';',
        '：': ':',
        '？': '?',
        '！': '!',
        '（': '(',
        '）': ')',
        '【': '[',
        '】': ']',
        '｛': '{',
        '｝': '}',
        '《': '<',
        '》': '>',
        '＂': '"',
        '＇': "'",
        '～': '~',
        '｜': '|',
        '・': '·',
    }
    pattern = re.compile('|'.join(re.escape(p) for p in fullwidth_punctuation))
    text = pattern.sub(
        lambda x: fullwidth_punctuation[x.group(0)],
        text
    )
    return text


# 测试示例
if __name__ == "__main__":
    sample_text = "Ｈｅｌｌｏ，　Ｗｏｒｌｄ！　１２３　【ＡＢＣ】　《测试》　＆＊％＃＠"
    converted = full_to_half_re(sample_text)
    print(f"转换前: '{sample_text}'")
    print(f"转换后: '{converted}'")

    # 更多测试用例
    test_cases = [
        ("ＡＢＣＤＥＦＧ", "ABCDEFG"),
        ("１２３４５６", "123456"),
        ("！＠＃＄％＾＆＊", "!@#$%^&*"),
        ("全角，标点。测试；", "全角,标点.测试;"),
        ("【中文】《书名》", "[中文]<书名>"),
        ("混合文本：Ａ１ｂｂ２Ｃ３！", "混合文本:A1b2C3!")
    ]

    for input_text, expected in test_cases:
        result = full_to_half_re(input_text)
        print(f"\n输入: '{input_text}'")
        print(f"预期: '{expected}'")
        print(f"结果: '{result}'")
        print(f"匹配: {result == expected}")