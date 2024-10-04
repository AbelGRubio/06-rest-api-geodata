import os

import openai


def chat_with_gpt(prompt):
    client = openai.OpenAI(
        # This is the default and can be omitted
        api_key=os.getenv("GPT_KEY", None),
    )
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )
    return response
