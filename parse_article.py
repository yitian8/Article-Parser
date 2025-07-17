import csv
from openai import OpenAI
from deepseek_api import inference
import json
import logging
def prepresponse(input):
    output = []
    for quote_list in input:
        str = ''
        for quote in quote_list:
            str += ('\'' + quote + '\'' + '\n')
        output.append(str)
    return output


if __name__ == '__main__':
    logging.basicConfig(filename='output/test.log', format='%(asctime)s %(message)s', filemode='w')
    logger = logging.getLogger()
    with open('key.env', 'r', newline='') as system:
        api_key = system.read()
    database = 'output/output_small.csv'
    output = 'output/parse_small.csv'
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    rows = []
    with open(database, 'r', newline = '', encoding = 'utf-8') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter = ',')
        outputfile = open(output, 'w', newline = '', encoding = 'utf-8')
        csv_writer = csv.writer(outputfile, delimiter = ',', dialect = 'unix')
        csv_writer.writerow(['id', 'content', 'company_name', 'entry_id', 'question_1', 'question_2', 'question_3'])
        for row in csv_reader:
            content = row[1]
            result = inference(content, client, temp=0.2)
            try:
                logger.info(result)
                json_result = json.loads(result)
                question1 = json_result['1']
                question2 = json_result['2']
                question3 = json_result['3']
                string = prepresponse([question1, question2, question3])
                row.extend(string)
            except:
                print(result)
                print('parse error')
                continue
            print(result)
            csv_writer.writerow(row)

