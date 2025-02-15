from aiogram import F, Router
from aiogram.types import Message, FSInputFile, ReplyKeyboardRemove
from aiogram.filters import CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import bot.app.database.requests as rq
from bot.app.gpt.gpt_handler import get_chatgpt_response
from bot.app.keyboards import get_main_keyboard

router = Router()


class Interview(StatesGroup):
    question1 = State()
    question2 = State()
    question3 = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)

    photo = FSInputFile(r"app/files/img_1.png")

    await message.answer_photo(
        photo=photo,
        caption=(
            "Привет! Я **Fufig**, ваш дружелюбный помощник. 😊\n\n"
            "Я могу рассказать вам все о **Latoken**, нашей платформе и процессе интервью, а также о нашем хакатоне. "
            "После знакомства я задам вам 3 вопроса, которые помогут нам принять решение о найме. "
            "Готовы? Давайте начнем!\n\n"
            "Жду ваших вопросов! 👋"
        ),
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )


@router.message(F.text == "🔥 Готов ответить на 3 вопроса! 🔥")
async def start_questions(message: Message, state: FSMContext):
    await state.set_state(Interview.question1)
    photo = FSInputFile(r"app/files/img_1.png")

    await message.answer_photo(
        photo=photo,
        caption=(
            "Постарайтесь отвечать максимально подробно в одном сообщении.\n\n"
            "**Отлично! Вот первый вопрос:**\n\n"
            "**1. Почему вы хотите работать в Latoken?** 🤔\n\n"
            "Расскажите, что вас привлекает в нашей компании. "
            "Это может быть миссия, культура, продукты или технологии. "
            "Поделитесь своими мотивами и ожиданиями!"
        ),
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Interview.question1)
async def answer_question1(message: Message, state: FSMContext):
    await rq.save_user_answer(message.from_user.id, message.text, 1)
    await state.set_state(Interview.question2)
    photo = FSInputFile(r"app/files/img_4.png")

    await message.answer_photo(
        photo=photo,
        caption=(
            "Отличный ответ! Теперь второй вопрос:\n\n"
            "**2. Какие у вас сильные стороны?** 💪\n\n"
            "Опишите ключевые навыки и качества, которые помогают вам в работе. "
            "Это могут быть технические знания, креативность, умение решать проблемы или работа в команде."
        ),
        parse_mode="Markdown"
    )


@router.message(Interview.question2)
async def answer_question2(message: Message, state: FSMContext):
    await rq.save_user_answer(message.from_user.id, message.text, 2)
    await state.set_state(Interview.question3)
    photo = FSInputFile(r"app/files/img_3.png")

    await message.answer_photo(
        photo=photo,
        caption=(
            "Отлично! И последний вопрос:\n\n"
            "**3. Где вы видите себя через 5 лет?** 🚀\n\n"
            "Поделитесь своими карьерными целями и амбициями. "
            "Как вы представляете свой профессиональный путь? "
            "Какие новые навыки хотите развивать, какие проекты реализовывать?"
        ),
        parse_mode="Markdown"
    )


@router.message(Interview.question3)
async def answer_question3(message: Message, state: FSMContext):
    await rq.save_user_answer(message.from_user.id, message.text, 3)
    photo = FSInputFile(r"app/files/img_2.png")

    await message.answer_photo(
        photo=photo,
        caption=(
            "Спасибо за ваши ответы! 🎉\n\n"
            "Мы внимательно их изучим и свяжемся с вами в ближайшее время. "
            "Если у вас есть вопросы, не стесняйтесь задавать! 😊"
        ),
        parse_mode="Markdown"
    )
    await state.clear()


@router.message(F.text)
async def handle_text_message(message: Message):
    flag, chatgpt_response = await get_chatgpt_response(message.text)
    if flag:
        await rq.add_message(tg_id=message.from_user.id, message=message.text, response=chatgpt_response)
    else:
        await rq.add_message(tg_id=message.from_user.id, message=message.text, response=None)
    await message.answer(chatgpt_response)


@router.message()
async def handle_unknown_message(message: Message):
    """Обработка сообщений неизвестного типа в стиле Fufig"""
    await message.answer(
        "Ой-ой! 😲 Я пока что не умею работать с таким типом сообщений... "
        "Но я учусь! 📚\n\n"
        "Попробуйте задать мне вопрос текстом – так мне будет проще вам помочь. 😊"
    )
