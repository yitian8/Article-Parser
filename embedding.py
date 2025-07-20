# import necessary libraries
import tensorflow_hub as hub
from langdetect import detect
import re
import spacy
from rapidfuzz import fuzz
import et_dep_ud_sm
from language_router import routeLanguage
import tensorflow as tf
from sentence_transformers.cross_encoder import CrossEncoder
from transformers import pipeline
import json
# Load pre-trained universal sentence encoder model


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

def extractQuotes(company, article, questions, qa_pipeline):
    results = {}
    filtered_sentences = filterSentences(article, company)
    for i, question in enumerate(questions):
        question_processed = question.replace('(__place_holder__)', company)
        answers = []
        for context in filtered_sentences:
            result = qa_pipeline(question=question, context=context)
            if result['score'] >= 0.3:
                answers.append(context)
        results[str(i+1)] = answers
    return results

def filterSentences(article, name):
    nlp = None
    language = detect(article)
    print(language)
    nlp = routeLanguage(article)
    if nlp is None:
        return []
    Sentences = re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', article)
    results = []
    for sentence in Sentences:
        entities = extractEntitity(sentence, name = name, nlp = nlp)
        if entities:
            results.append(sentence)
    return results

def extractEntitity(aritcle, type = 'ORG', name = None, threshold = 70, nlp = spacy.load('en_core_web_sm')):
    doc = nlp(aritcle)
    entries = []
    for ent in doc.ents:
        if ent.label_ == type:
            if name is not None:
                org_name = normalize(ent.text)
                similarity = fuzz.partial_ratio(org_name, name.lower())

                if similarity >= threshold:
                    entries.append(ent)
                    # print(ent.text.ljust(20, ' '),
                    #       ent.label_.ljust(10, ' '),
                    #       ent.start_char, ent.end_char)
            else:
                entries.append(ent)
    return entries
