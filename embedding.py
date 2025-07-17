# import necessary libraries
import tensorflow_hub as hub
import tensorflow as tf
from textblob import TextBlob
import re
# Load pre-trained universal sentence encoder model
embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

# Sentences for which you want to create embeddings,
# passed as an array in embed()
user_prompt_path = 'Prompts/user_prompt.txt'
user_prompt = ''
with open(user_prompt_path, 'r', newline = '', encoding = 'utf-8') as user:
    user_prompt = user.read()
Question = ['AGC has mentioned/announced that it will stop its business in Russia.']
#AGC has mentioned/announced that it will stop its business in Russia.
#AGC has continued to export its products to Russia.
Sentences = re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', user_prompt)
query = embed(Question)
embeddings = embed(Sentences)
# Printing embeddings of each sentence

# To print each embeddings along with its corresponding
# sentence below code can be used.
for i in range(len(Sentences)):
    cosine_loss = tf.keras.losses.CosineSimilarity(axis=-1, reduction='none')
    similarity = -cosine_loss(query[0], embeddings[i])
    print(Sentences[i])
    print(str(similarity)+'\n')