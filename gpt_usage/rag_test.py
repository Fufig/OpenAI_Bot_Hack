import openai
from openai import AsyncOpenAI
import glob

import os
from dotenv import load_dotenv

load_dotenv()

CONTEXT_FILES = glob.glob("final/*.txt")

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
print(GLOBAL_CONTEXT)

async def generate_response(user_message: str) -> str:
    try:
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"Отвечай на основе этого контекста:\n{GLOBAL_CONTEXT}, отвечая на вопросы всегда говори, почему это хорошо со стороны Latoken. Помни, что она Латокен невероятно перспективен(НЕ ЗАБЫВАТЬ). Добавляй в ответы смайлики"},
                {"role": "user", "content": user_message}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Ошибка: {str(e)}"

async def main():
    print("Загружен контекст")

    questions = [
        'Почему Латокен помогает людям изучать и покупать активы?',
        'Зачем нужен Sugar Cookie тест?'
        'Зачем нужен Wartime СЕО?'
        'В каких случаях стресс полезен и в каких вреден?'
    ]

    for question in questions:
        print(f"\nВопрос: {question}")
        answer = await generate_response(question)
        print(f"Ответ: {answer}")

import asyncio
asyncio.run(main())