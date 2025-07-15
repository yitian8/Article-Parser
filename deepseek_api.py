import csv
from openai import OpenAI
import chardet

database = 'output/output.csv'

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
    ind1 = s.find('\n')
    ind2 = s.rfind('\n')
    return s[ind1+1:ind2]

def inference(prompt, user, temp = 1.0):
    global system_prompt
    response = user.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        stream=False,
        temperature=temp
    )
    s = response.choices[0].message.content
    return solve_fast(s)

client = OpenAI(api_key="sk-5fc2806676204c9eae428b5d5d48419f", base_url="https://api.deepseek.com")
system_prompt_path = 'Prompts/system_prompt.txt'
user_prompt_path = 'Prompts/user_prompt.txt'

system_prompt, user_prompt = '', ''
with open(system_prompt_path, 'r', newline = '', encoding = 'latin1') as system:
    system_prompt = system.read()

with open(user_prompt_path, 'r', newline = '', encoding = detect_encoding(user_prompt_path)) as user:
    user_prompt = user.read()
response = inference(user_prompt, client, temp = 0.2)
print(response)