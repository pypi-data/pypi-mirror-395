DEFAULT_SCORING_SHOTS = """Example:
INPUT
What percentage is considered a good rental yield?

STATEMENTS
0: How are you doing today?
1: Rental yield is how much you could expect to receive in rent each year from your buy to let investment.
2: Rental yield is expressed as a percentage - reflecting your rental income against the property's market value.
3: Anything around the 5-6% mark could be considered a good rental yield.
4: Anything above 6% could be considered a very good rental yield.

```json
{
    "verdicts": [
        {
            "reason": "The statement is unrelated to the input.",
            "score": 0
        },
        {
            "reason": "While the statement discusses rental yields, it does not indicate what constitutes a good rental yield.",
            "score": 0
        },
        {
            "reason": "While the statement mentions that yield is expressed as a percentage, it does not address the user question.",
            "score": 0
        },
        {
            "reason": "The statement addresses the user input, specifying what a good rental yield is.",
            "score": 1
        },
        {
            "reason": "The statement addresses the user input, specifying what a very good rental yield is.",
            "score": 1
        },
    ]
}```"""


SYSTEM = """You are an expert data reviewer.
You will be given a document, and a user input/question.
Your task is to classify whether the document contains information relevant to answering the user input.

IMPORTANT: Please make sure to only return in JSON format and with no further preamble explanation, with the `score` key providing the score, and the `reason` key providing the reason. The score can only be 0 or 1. Keep the reason short and concise.

You always output a JSON object with the following schema, and nothing else before or after:
{json_schema}

Examples:
{shots}"""

USER = """Your real task:
INPUT
{user_question}

DOCUMENT
{document}

```json"""

DEFAULT_SHOTS = """Example 1:
INPUT
What percentage is considered a good rental yield?

DOCUMENT
Rental yield is how much you could expect to receive in rent each year from your buy to let investment. Rental yield is expressed as a percentage - reflecting your rental income against the property's market value.
While calculating rental yield can give you an indication of whether investing in a buy-to-let property is worth it, there's other factors to consider. You'll also need to think about whether there might be any problem finding tenants, collecting rent or void periods, for example. Then, there's capital growth - the value by which your property is set to increase over time.
All of these can impact your decision on whether a property is worth your investment.

```json
{"score":0,"reason":"While the document explains the concept of rental yield, there is no indication as to what a good percentage yield is."}
```

Example 2:
INPUT
What percentage is considered a good rental yield?

DOCUMENT
As of 2024, the average rental yield in the UK is between 5% and 8%. Anything around the 5-6% mark could be considered a 'good' rental yield, while anything above 6% could be considered very good.
Some parts of the country can deliver significantly higher or lower returns to others. It's worth bearing in mind that you may get a lower yield in areas where the house prices are highest, such as in London and the South East.
This is because the potential for capital gains in the region pushes sale prices up, while rent levels are less affected.

```json
{"score":1,"reason":"The document indicates what can be considered a good rental yield percentage."}
```"""
