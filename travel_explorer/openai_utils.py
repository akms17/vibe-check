import openai


def translate_to_sql(user_query: str) -> str:
    """Use OpenAI to translate a natural language query to SQL."""
    prompt = (
        'Translate the following natural language query into a SQL query for '
        'SQLite. Only provide the SQL query.\nQuery: ' + user_query
    )
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': prompt}],
        temperature=0
    )
    return response['choices'][0]['message']['content'].strip()
