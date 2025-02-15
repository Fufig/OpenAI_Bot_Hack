import openai
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

CONTEXT_FILES = ["files/context.txt"]

client = AsyncOpenAI(api_key=os.getenv('GPT_TOKEN'))

def load_context_files():
    context = ""
    for file_path in CONTEXT_FILES:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                context += f.read() + "\n"
        except Exception as e:
            print(f"Ошибка загрузки файла {file_path}: {str(e)}")
    return context

GLOBAL_CONTEXT = load_context_files()

async def generate_response(user_message: str) -> str:
    try:
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"Отвечай на основе этого контекста:\n{GLOBAL_CONTEXT}"},
                {"role": "user", "content": user_message}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Ошибка: {str(e)}"

async def main():
    print("Загружен контекст:\n", GLOBAL_CONTEXT[:500], "...")

    questions = [
        "Какие файлы контекста у тебя есть"
    ]

    for question in questions:
        print(f"\nВопрос: {question}")
        answer = await generate_response(question)
        print(f"Ответ: {answer}")

import asyncio
asyncio.run(main())