# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI

client = OpenAI(api_key="sk-5fc2806676204c9eae428b5d5d48419f", base_url="https://api.deepseek.com")
system_prompt = \
"""You are a professional market analyst. You are asked to process certain articles to extract answer for certain questions.

In the prompt, you will be given an article and the name of a company. You shall extract quotes from the article related to those three questions:

1. The company has mentioned/announced that it will stop its business in Russia. Note that this one is about what companies say, not necessarily what companies actually do.

2. The company has largely maintained its sales in Russia. Note that this one is about the action, not what companies say.

3. The company has continued to export its products to Russia. Note that this one is about the action, not what companies say.

The quotes should directly answer those questions; if not, the answer must be inferable from the quote.

Your answers shall only contain quotes to those answers. The quotes shall be strictly copies from the original text, without any modifications.

Your output should be in json format."""

user_prompt = """company:
basf

article:
BASF strongly condemns the Russian war of aggression against Ukraine. We stand in solidarity with the people of Ukraine and hope that this war will end as soon as possible. In response to the war, the company has wound down its activities in Russia and Belarus. One exception is the business to support food production - a measure to ensure security of supply for agricultural products and, in particular, to enable poorer countries to continue to have access to inexpensive food. In 2022, BASF supported both the Red Cross and Ukrainian refugees through donation campaigns and emergency aid. In addition, a crisis team continues to support BASF employees in Ukraine. BASF to wind down activities in Russia and Belarus except for business that supports food production. As announced on March 3, 2022, BASF has not conducted new business in Russia and Belarus, in light of the war of aggression against Ukraine ordered by the Russian government. BASF and its employees donate an additional €4.2 million for people in Ukraine. 2,110,156 €: This is how much BASF employees donated to the BASF Stiftung (BASF Foundation) as part of the company-wide initiative #ColleaguesForUkraine – by far the highest result of an employee donation campaign in BASF's history. The company will double the amount. BASF donates €1 million in emergency humanitarian aid to Ukraine. Following the attack on Ukraine ordered by the Russian government, the civilian population is suffering from the escalating violence. Hundreds of thousands are on the run. To help the people in the country, BASF has provided €1 million in emergency aid."""

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ],
    stream=False,
    temperature=1
)

print(response.choices[0].message.content)