import logging
import asyncio

from fsspec.asyn import loop
from googletrans import Translator
import csv
from langdetect import detect
async def translate_text(text, translator):
    result = await translator.translate(text, dest='en')
    return result.text

if __name__ == '__main__':
    translator = Translator()
    loop = asyncio.get_event_loop()

    logging.basicConfig(filename='output/test.log', format='%(asctime)s %(message)s', filemode='w')
    logger = logging.getLogger()
    database = 'results/results_embedding.csv'
    output = 'results/results_embedding_translated.csv'
    rows = []
    with open(database, 'r', newline = '', encoding = 'utf-8') as file:
        csv_reader = csv.reader(file, delimiter=',')
        length = sum(1 for line in csv_reader)
    with (open(database, 'r', newline = '', encoding = 'utf-8') as csvfile):
        csv_reader = csv.reader(csvfile, delimiter = ',')
        outputfile = open(output, 'w', newline = '', encoding = 'utf-8')
        csv_writer = csv.writer(outputfile, delimiter = ',', dialect = 'unix')
        csv_writer.writerow(['id', 'content', 'company_name', 'entry_id',
                             'question_1', 'question_2', 'question_3',
                             'question_1_translated', 'question_2_translated', 'question_3_translated',
                             'source_language', 'translated'])
        fields = next(csv_reader)
        for (i, row) in enumerate(csv_reader):
            content = row[1]
            company_name = row[2]
            language = detect(content)
            attempts = 1
            while True:
                try:
                    if language != 'en':
                        tasks = (translate_text(row[4], translator),
                                 translate_text(row[5], translator),
                                 translate_text(row[6], translator))
                        a, b, c = loop.run_until_complete(asyncio.gather(*tasks))
                        row.extend([a, b, c, language,1])
                    else:
                        row.extend(['','','','en',0])
                    break
                except:
                    logger.error('Connection error. Attempt #{}'.format(attempts))
            print('Processed entries: ' + str(i + 1) + '/' + str(length - 1))
            csv_writer.writerow(row)
