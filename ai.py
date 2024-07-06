import os

from openai import AsyncOpenAI, OpenAIError

# models
GPT_MODEL = "gpt-3.5-turbo"

client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


async def ask_openai(question) -> str:
    try:
        response = await client.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content
    except OpenAIError as ai_error:
        raise ai_error
