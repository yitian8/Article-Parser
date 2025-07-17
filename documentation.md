# Quote Extraction

## Core task: extracting answers for certain questions from articles

## **Data preprocessing**

Some rows are just “content requires subscription”, and some other rows contain messed up formats. I have to clean the whole dataset before moving on.

Basically, I set up those standards to filter invalid entries:
1. each line should only contain 4 elements, which are id, content, company_name and entry_id.
2. id and entry_id should only consist of numbers and lowercase letters.

The preprocessing script is in csv_preprocessing.py. After running the script, I was left with 4135 entries.

## **Method 1:Deepseek**

Since its release in 2025 March 24th, Deepseek V3-0324 has been proven to be a cheap alternative for SOTA non-thinking LLMs
such as GPT-4.1 or claude 3.7 Sonnet, while having similar performances. In this project, I will use
Deepseek to extract quotes for me by calling Deepseek api provided by api.deepseek.com. 

The reason I chose a non-thinking LLM is thinking LLMs, such as Deepseek-R1-0528 or Gemini 2.5 Pro tend to "overthink" 
and hallucinate non-existent quotes while performing simple tasks such as parsing articles.
Apart from hallucinations, thinking LLMs are also worse at following instructions such as "Your output must be in JSON format."
While non-thinking LLMs can follow this instruction hundreds of times in a row without failing once, 
thinking LLMs fail quite often.


This is my initial system prompt:

    You are a professional market analyst. You are asked to process certain articles to extract answer for certain questions.
    
    In the prompt, you will be given an article and the name of a company. You shall extract quotes from the article related to those three questions:

    1. The company has mentioned/announced that it will stop its business in Russia. Note that this one is about what companies say, not necessarily what companies actually do.

    2. The company has largely maintained its sales in Russia. Note that this one is about the action, not what companies say.

    3. The company has continued to export its products to Russia. Note that this one is about the action, not what companies say.

    The quotes should directly answer those questions; if not, the answer must be inferable from the quote.

    Your answers shall only contain quotes to those answers. The quotes shall be strictly copies from the original text, without any modifications.

Then I entered the following user prompt:

>company:
>basf
>
>article:
>BASF strongly condemns the Russian war of aggression against Ukraine. We stand in solidarity with the people of Ukraine and hope that this war will end as soon as possible. In response to the war, the company has wound down its activities in Russia and Belarus. One exception is the business to support food production - a measure to ensure security of supply for agricultural products and, in particular, to enable poorer countries to continue to have access to inexpensive food. In 2022, BASF supported both the Red Cross and Ukrainian refugees through donation campaigns and emergency aid. In addition, a crisis team continues to support BASF employees in Ukraine. BASF to wind down activities in Russia and Belarus except for business that supports food production. As announced on March 3, 2022, BASF has not conducted new business in Russia and Belarus, in light of the war of aggression against Ukraine ordered by the Russian government. BASF and its employees donate an additional €4.2 million for people in Ukraine. 2,110,156 €: This is how much BASF employees donated to the BASF Stiftung (BASF Foundation) as part of the company-wide initiative #ColleaguesForUkraine – by far the highest result of an employee donation campaign in BASF's history. The company will double the amount. BASF donates €1 million in emergency humanitarian aid to Ukraine. Following the attack on Ukraine ordered by the Russian government, the civilian population is suffering from the escalating violence. Hundreds of thousands are on the run. To help the people in the country, BASF has provided €1 million in emergency aid.

And Deepseek gave the following output:


>1. "In response to the war, the company has wound down its activities in Russia and Belarus."  
   "BASF to wind down activities in Russia and Belarus except for business that supports food production."  
   "As announced on March 3, 2022, BASF has not conducted new business in Russia and Belarus, in light of the war of aggression against Ukraine ordered by the Russian government."  

>2. "One exception is the business to support food production - a measure to ensure security of supply for agricultural products and, in particular, to enable poorer countries to continue to have access to inexpensive food."  

>3. "One exception is the business to support food production - a measure to ensure security of supply for agricultural products and, in particular, to enable poorer countries to continue to have access to inexpensive food."

Which seems decent.

Then I tried to force the output in Json format, so the outputs can be processed by automated scripts.

This gave the following output: 

```json
{
  "1": [
    "In response to the war, the company has wound down its activities in Russia and Belarus.",
    "BASF to wind down activities in Russia and Belarus except for business that supports food production.",
    "As announced on March 3, 2022, BASF has not conducted new business in Russia and Belarus, in light of the war of aggression against Ukraine ordered by the Russian government."
  ],
  "2": [
    "One exception is the business to support food production - a measure to ensure security of supply for agricultural products and, in particular, to enable poorer countries to continue to have access to inexpensive food."
  ],
  "3": []
}
```
which is good.

However, sometimes the character ” would appear as â in the output. I found out that
this is due to opening an utf-8 encoded file as a latin-1 encoded file, so I implemented an
function that re-encodes the input file as UTF-8, and the problem was solved.

Then, I wrote a program to automatically reads from csv files and invokes deepseek
api, then writes out found quotes to a separate csv file, which is structured like this:

### **Output structure**

```
| id | content | company_name | entry_id | question_1 | question_2 | question_ 3 |
----------------------------------------------------------------------------------
|    |         |              |          |            |            |             |

```
>Question 1 corresponds to quotes for "(Name of company) has mentioned/announced that it will stop its business in Russia."
> 
>Question 2 corresponds to quotes for "(Name of company) has largely maintained its sales in Russia."
> 
>Question 3 corresponds to quotes for "(Name of company) has continued to export its products to Russia."

If multiple quotes are found for one question, each quote is surrounded by
single quotation marks, and quotes are separated by the newline character '\n'.

So the quotes are similar to this structure:

```
'quote 1'
'quote 2'
'quote 3'
...
```

### Problem encountered: unspecified result

After some testing, I found out that the output quotes are related to all companies
present in the article, rather than related to a single company. It turns out that I forgot to
include the name of the company in my prompt. So I added the company name in the prompt
and everything is fixed.

I also made small modifications to the system prompt to make the whole inference process more robust.
The updated system prompt is in Prompts/system_prompt.txt.


## **Method 2: Sentence Embedding + Semantic Analysis**

I tried another method: Sentence Embedding.

Sentence embedding converts a sentence into a vector in high dimensional space,
so we can search for answers of the questions by calculating the similarity of the 
embedding vectors of sentences in the article and the embedding vector of query sentence.

However, this method has a lot of limitations. For example, for the query sentence below,

>AGC has mentioned/announced that it will stop its business in Russia.

The embeddings gave a similarity of 0.4 on the sentence

>Glass giant AGC Inc. said on Feb. 8 that it started considering selling its glass manufacturing and sales operations in Russia.

and gave a similarity of 0.48 on the sentence

> AGC has two plants in Russia.

While it is clearly visible that the former sentence is more related to the question.

Each embedding only carry the meanings of that exact sentence without any context.
This can be problematic since we have to infer its meaning from the context for
sentences similar to "This company has stopped exporting its products to Russia."



