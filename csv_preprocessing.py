import csv
import re

from deepseek_api import detect_encoding


class Entry:
    def __init__(self,id, content, company_name,entry_id):
        self.id = id
        self.entry_id = entry_id
        self.content = content
        self.company_name = company_name

entries = []
input_file = "test_articles.csv"
print(detect_encoding(input_file))
output_file = 'output/dataset_medium.csv'
with open(input_file, 'r', newline = '', encoding = 'utf-8', errors='ignore') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter = ',')
    fields = next(csv_reader)
    for (index, row) in enumerate(csv_reader):
        if len(row) < 4:
            continue
        if len(row) >= 5 and row[4]:
            continue
        id = row[0]
        content = row[1]
        company = row[2]
        entry_id = row[3]
        if (not re.search('^[a-z0-9]+$', id)) or (not re.search('^[a-z0-9]+$', entry_id)):
            continue
        if content.startswith('Content requires') or (not content) or (not company):
            continue
        cnt += 1
        news_entry = Entry(id=id, content = content, company_name = company, entry_id = entry_id)
        entries.append(news_entry)
with open(output_file, 'w', encoding = 'utf-8') as csvfile:
    rows = []
    csvwriter = csv.writer(csvfile, delimiter = ',', dialect = 'unix')
    csvwriter.writerow(['id', 'content', 'company_name', 'entry_id'])
    for entry in entries:
        rows.append([entry.id, entry.content, entry.company_name, entry.entry_id])
    csvwriter.writerows(rows)




        
