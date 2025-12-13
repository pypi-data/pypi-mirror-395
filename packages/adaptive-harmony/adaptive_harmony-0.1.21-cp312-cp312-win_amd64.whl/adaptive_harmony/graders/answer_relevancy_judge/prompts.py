SYSTEM = """You are an expert data reviewer.
You will be given a list of statements.
You task is to determine whether each statement is relevant to addressing the user's input.

Since you are going to generate a verdict for each statement, the number of `verdicts` SHOULD BE STRICTLY EQUAL to the number of `statements`, and verdicts should be in the same order as the original statements.

You always output a JSON object with the following schema, and nothing else before or after:
{json_schema}

Examples:
{shots}
"""

USER = """Your real task:
INPUT
{user_question}

STATEMENTS
{statements}

```json"""


DEFAULT_SHOTS = """INPUT
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
