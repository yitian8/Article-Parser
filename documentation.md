Core task: extracting answers for certain questions from articles

Data preprocessing: Some rows are just “content requires subscription”, and some other rows contain messed up formats. I have to clean the whole dataset before moving on. Also have to determine encoding type.

Basically, I set up those standards to filter invalid entries:
1. each line should only contain 4 elements, which are id, content, company_name and entry_id.
2. id and entry_id should only consist of numbers and lowercase letters.

The preprocessing script is in csv_preprocessing.py. After running the script, I was left with 4135 entries.

**Method 1: Using a cheaper alternative to Chatgpt, Deepseek, to extract the quotes.**

Tried with the following system prompt:

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

this gave the following output: 

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




