import csv
import et_dep_ud_sm
import logging
import subprocess
from langdetect import detect
import spacy
if __name__ == '__main__':

    logging.basicConfig(filename='output/test.log', format='%(asctime)s %(message)s', filemode='w')
    logger = logging.getLogger()
    database = 'output/output.csv'
    languages = {'en','ru','uk','fi','de', 'sk'}
    with open(database, 'r', newline = '', encoding = 'utf-8') as file:
        csv_reader = csv.reader(file, delimiter=',')
        length = sum(1 for line in csv_reader)
    with open(database, 'r', newline = '', encoding = 'utf-8') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter = ',')
        fields = next(csv_reader)
        for (i, row) in enumerate(csv_reader):
            content = row[1]
            language = detect(content)
            if language not in languages:
                model = language + '_core_news_md'
                result = subprocess.run(['python', '-m', 'spacy', 'download', model])
                print(model)
                if not result.stderr:
                    languages.add(language)
            print('Processed articles: ' + str(i + 1) + '/' + str(length - 1), language)
    print(languages)

def routeLanguage(article):
    language = detect(article)
    languages = {'sv', 'da', 'uk', 'ko',
                 'sl', 'es', 'hr', 'de',
                 'it', 'nl', 'lt', 'fi', 'ja', 'pl',
                 'ru', 'pt', 'en', 'fr'}
    if language == 'en':
        nlp = spacy.load("en_core_web_md")
    elif language in languages:
        nlp = spacy.load(language + '_core_news_md')
    elif language == 'et':
        nlp = et_dep_ud_sm.load()
    else:
        nlp = None
    return nlp
