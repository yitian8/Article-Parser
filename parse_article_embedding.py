import csv
from transformers import pipeline
from embedding import extractQuotes
import logging

def prepresponse(input):
    output = []
    for quote_list in input:
        str = ''
        for quote in quote_list:
            str += ('\'' + quote + '\'' + '\n')
        output.append(str)
    return output

Questions = ['Has (__place_holder__) mentioned/announced that it will stop its business in Russia?',
                 'Has (__place_holder__) largely maintained its sales in Russia?',
                'Has (__place_holder__) continued to export its products to Russia?']

if __name__ == '__main__':

    logging.basicConfig(filename='output/test.log', format='%(asctime)s %(message)s', filemode='w')
    logger = logging.getLogger()
    database = 'output/output.csv'
    output = 'results/results_embedding.csv'
    rows = []
    with open(database, 'r', newline = '', encoding = 'utf-8') as file:
        csv_reader = csv.reader(file, delimiter=',')
        length = sum(1 for line in csv_reader)
    with open(database, 'r', newline = '', encoding = 'utf-8') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter = ',')
        outputfile = open(output, 'w', newline = '', encoding = 'utf-8')
        csv_writer = csv.writer(outputfile, delimiter = ',', dialect = 'unix')
        csv_writer.writerow(['id', 'content', 'company_name', 'entry_id', 'question_1', 'question_2', 'question_3'])
        fields = next(csv_reader)
        Pipeline = pipeline("question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad")
        for (i, row) in enumerate(csv_reader):
            content = row[1]
            company_name = row[2]
            result = extractQuotes(company_name, content, Questions, Pipeline)
            try:
                question1 = result['1']
                question2 = result['2']
                question3 = result['3']
                string = prepresponse([question1, question2, question3])
                row.extend(string)
            except:
                logger.error(result)
                logger.error('parse error')
                continue
            print('Processed articles: ' + str(i + 1) + '/' + str(length - 1))
            csv_writer.writerow(row)

