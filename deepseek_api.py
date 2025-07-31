from openai import OpenAI
import chardet


with open('key.env', 'r', newline='') as system:
    api_key = system.read()

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        detector = chardet.UniversalDetector()
        for line in file:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
        encoding = detector.result['encoding']
        return encoding

def solve_fast(s):
    if s[0] == '{' and s[-1] == '}':
        return s
    ind1 = s.find('\n')
    ind2 = s.rfind('\n')
    return s[ind1+1:ind2]

def inference(system_prompt_path, prompt, user, temp = 1.0):
    system_prompt = ''
    with open(system_prompt_path, 'r', newline='', encoding='utf-8') as system:
        system_prompt = system.read()
    response = user.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        stream=False,
        temperature=temp
    )
    s = response.choices[0].message.content
    return solve_fast(s)


if __name__ == '__main__':
    database = 'output/output.csv'
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    user_prompt_path = 'Prompts/user_prompt.txt'
    user_prompt = ''
    with open(user_prompt_path, 'r', newline = '', encoding = detect_encoding(user_prompt_path)) as user:
        user_prompt = user.read()
    response = inference(user_prompt, client, temp = 0.2)
    print(response)