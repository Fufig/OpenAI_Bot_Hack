from bot.app.database.models import async_session
from bot.app.database.models import User, Counter, History, InterviewAnswers
from sqlalchemy import select


async def set_user(tg_id):
    async with async_session() as session:
        try:
            user = await session.execute(select(User).filter(User.tg_id == tg_id))
            user = user.scalar_one_or_none()

            if not user:
                user = User(tg_id=tg_id)
                session.add(user)
                await session.commit()
                await session.refresh(user)
            return user
        except Exception as e:
            print(f"Error in set_user: {e}")
            return None


async def add_message(tg_id: int, message: str, response: str = None):
    async with async_session() as session:
        try:
            async with session.begin():
                user = await set_user(tg_id)

                if user is None:
                    return

                history = History(user_id=user.id, message=message, response=response)
                session.add(history)

                if response and response.strip():
                    counter = await session.execute(select(Counter).filter(Counter.user_id == user.id))
                    counter_record = counter.scalar_one_or_none()

                    if counter_record:
                        counter_record.message_count += 1
                    else:
                        counter_record = Counter(user_id=user.id, message_count=1)
                        session.add(counter_record)

                await session.commit()
        except Exception as e:
            print(f"Error in add_message: {e}")


async def save_user_answer(tg_id: int, answer: str, question_number: int):
    async with async_session() as session:
        try:
            async with session.begin():
                user = await set_user(tg_id)
                if user is None:
                    print(f"User with tg_id={tg_id} not found or could not be created.")
                    return

                answer_entry = InterviewAnswers(
                    user_id=user.id,
                    question_number=question_number,
                    answer=answer
                )
                session.add(answer_entry)
                await session.commit()
        except Exception as e:
            print(f"Error in save_user_answer: {e}")
