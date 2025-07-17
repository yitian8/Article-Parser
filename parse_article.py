import csv
from openai import OpenAI
from deepseek_api import inference
import json
import logging
from datetime import datetime
import time

def prepresponse(input):
    output = []
    for quote_list in input:
        str = ''
        for quote in quote_list:
            str += ('\'' + quote + '\'' + '\n')
        output.append(str)
    return output


if __name__ == '__main__':
    # while True:
    #     current_time = datetime.now()
    #     if current_time.hour == 0 and current_time.minute >= 30:
    #         break
    #     time.sleep(30)
    #     print('checking time')

    logging.basicConfig(filename='output/test.log', format='%(asctime)s %(message)s', filemode='w')
    logger = logging.getLogger()
    with open('key.env', 'r', newline='') as system:
        api_key = system.read()
    database = 'output/dataset_medium.csv'
    output = 'results/results_medium.csv'
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    rows = []
    with open(database, 'r', newline = '', encoding = 'utf-8') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter = ',')
        outputfile = open(output, 'w', newline = '', encoding = 'utf-8')
        csv_writer = csv.writer(outputfile, delimiter = ',', dialect = 'unix')
        csv_writer.writerow(['id', 'content', 'company_name', 'entry_id', 'question_1', 'question_2', 'question_3'])
        fields = next(csv_reader)
        for row in csv_reader:
            content = row[1]
            company_name = row[2]
            prompt = ('company:' + '\n' + company_name + '\n\n' + 'article:' + '\n' + content)
            result = inference(prompt, client, temp=0.2)
            try:
                json_result = json.loads(result)
                question1 = json_result['1']
                question2 = json_result['2']
                question3 = json_result['3']
                string = prepresponse([question1, question2, question3])
                row.extend(string)
            except:
                logger.error(result)
                logger.error('parse error')
                continue
            print(result)
            csv_writer.writerow(row)

