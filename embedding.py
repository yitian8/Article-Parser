# import necessary libraries
import tensorflow_hub as hub
from langdetect import detect
import re
import spacy
from rapidfuzz import fuzz
# Load pre-trained universal sentence encoder model
embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

def normalize(name):
    name = name.lower().strip()

    # Step 1: Remove punctuation at word boundaries (e.g., "Inc." → "Inc")
    name = re.sub(r'\b([^\w\s]|\.|,)\b', '', name)

    # Step 2: Remove ONLY standalone corporate suffixes (whole words)
    suffixes = r'\b(inc|ltd|llc|corp|plc|co|company|corporation|limited|group|holdings)\b'
    name = re.sub(suffixes, '', name)

    # Step 3: Clean residual characters and spaces
    name = re.sub(r'[^\w\s]', '', name)  # Remove non-alphanumeric
    name = re.sub(r'\s+', ' ', name).strip()  # Collapse whitespace
    return name

def extractQuotes(company, article, question):
    print('')

def extractEntitity(aritcle, type = 'ORG', name = None, threshold = 70):
    nlp = None
    language = detect(aritcle)
    if language == 'en':
        nlp = spacy.load("en_core_web_sm")
    elif language == 'ru':
        nlp = spacy.load("ru_core_news_sm")
    elif language == 'uk':
        nlp = spacy.load("uk_core_web_sm")
    doc = nlp(aritcle)
    entries = []
    for ent in doc.ents:
        if ent.label_ == type:
            if name is not None:
                org_name = normalize(ent.text)
                similarity = fuzz.partial_ratio(org_name, name.lower())
                print(ent.text.ljust(20, ' '), similarity)
                print(org_name)
                if similarity >= threshold:
                    entries.append(ent)
            else:
                entries.append(ent)
    return entries

user_prompt_path = 'Prompts/user_prompt.txt'
user_prompt = ''
with open(user_prompt_path, 'r', newline = '', encoding = 'utf-8') as user:
    user_prompt = user.read()
Question = ['(__place_holder__) has continued to export its products to Russia.',
            '(__place_holder__) has mentioned/announced that it will stop its business in Russia.'
            '(__place_holder__) has continued to export its products to Russia.']
#AGC has mentioned/announced that it will stop its business in Russia.
#.
Sentences = re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', user_prompt)
extractEntitity(user_prompt, name = 'japan tobacco international')
query = embed(Question)
embeddings = embed(Sentences)


# for i in range(len(Sentences)):
#     cosine_loss = tf.keras.losses.CosineSimilarity(axis=-1, reduction='none')
#     similarity = -cosine_loss(query[0], embeddings[i])
#     print(Sentences[i])
#     print(str(similarity)+'\n')