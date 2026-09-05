import json
from aiogram import Router, F, types
import secrets
import sqlite3
from aiogram.filters import Command
import aiohttp
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import BufferedInputFile
import os
from aiogram.types import Message, CallbackQuery
import asyncio
from aiogram.types import FSInputFile
from keyboards import get_request_type_panel, get_result_panel

router = Router()

photo = FSInputFile("kris_photo.jpg")

class QuestionState (StatesGroup):
    waiting_for_first_base_question = State()
    waiting_for_second_base_question = State()
    waiting_for_third_base_question = State()
    waiting_for_first_health_question = State()
    waiting_for_second_health_question = State()
    waiting_for_first_relationship_question = State()
    waiting_for_second_relationship_question = State()
    waiting_for_first_finance_question = State()
    waiting_for_second_finance_question = State()


@router.message(Command("start"))
async def start(message: Message, state : FSMContext):

    await message.answer_photo(
        photo=photo,
        caption="""
    Привет, давай познакомимся? 

Я Кристина Шабанова, психолог, специалист нейрографики и 
трансформационных игр, системный расстановщик, 
организатор трансформационных ретритов и ты 
почувствуешь результат после 1 сессии.

Приглашаю в свои социальные сети

Инстаграм  https://www.instagram.com/psyholog.shabanova

Телеграм канал https://t.me/izmeni_gzizn

Ретриты https://www.instagram.com/retreat_kris
    """,
    )
    await state.clear()
    await asyncio.sleep(3)
    await message.answer('Выбери тему своего запроса, нажав на кнопку ниже ⬇️',
                                reply_markup=get_request_type_panel())


@router.callback_query(F.data.contains('request_type_'))
async def start_test(callback : CallbackQuery, state : FSMContext):
    await callback.answer()
    rt = callback.data.split('_')[2]
    await state.update_data(request_type=rt)
    await callback.message.answer("""
    Что сейчас больше всего забирает вашу энергию и внимание?
• Отношения / личная жизнь
• Здоровье / состояние
• Деньги / бизнес / реализация
• Самооценка / внутреннее состояние
• Не могу понять, но чувствую, что что-то не так
• Или напиши свой вариант
    """)

    #await callback.message.answer(rt)
    await state.set_state(QuestionState.waiting_for_first_base_question)


@router.message(QuestionState.waiting_for_first_base_question)
async def run_first_base_question (message : Message, state : FSMContext):
    client_answer = message.text
    await state.update_data(first_base_question=client_answer)
    await message.answer('Если ничего не менять в ближайшие 3-6-12 месяцев, ваш вопрос/проблема решится сама?')
    await state.set_state(QuestionState.waiting_for_second_base_question)

@router.message(QuestionState.waiting_for_second_base_question)
async def run_second_base_question (message : Message, state : FSMContext):
    client_answer = message.text
    await state.update_data(second_base_question=client_answer)
    await message.answer('Какой результат/ состояние/ решение вы хотите получить?')
    await state.set_state(QuestionState.waiting_for_third_base_question)

@router.message(QuestionState.waiting_for_third_base_question)
async def run_third_base_question (message : Message, state : FSMContext):
    client_answer = message.text
    await state.update_data(third_base_question=client_answer)

    data = await state.get_data()
    request_type = data.get('request_type')

    if request_type == 'health':
        await message.answer("""
        Как ваше внутреннее состояние сейчас отражается на теле и самочувствии?

• Постоянно чувствую напряжение/усталость
• Есть проблемы со сном или восстановлением
• Заедаю/ Появляется лишний вес
• Часто игнорирую сигналы тела
• Раздражительность/ полное безразличие 
• Нежелание секса/отсутствие возбуждения
• Свой вариант
        """)
        await state.set_state(QuestionState.waiting_for_first_health_question)

    elif request_type == 'relationship':
        await message.answer("""
        Что чаще всего повторяется в ваших отношениях?

• Я выбираю похожих партнёров
• Мне сложно говорить о своих желаниях/чувствах/ просить о помощи
• Боюсь потерять человека и подстраиваюсь
• Мне сложно доверять и расслабляться
• Я часто оказываюсь в роли "спасающей" или «жертвы»
• Мне сложно построить близкие отношения
• Ваш вариант решение 
        """)
        await state.set_state(QuestionState.waiting_for_first_relationship_question)

    elif request_type == 'finance':
        await message.answer("""
        Что сейчас больше всего мешает вам выйти на более высокий финансовый или профессиональный уровень?

• Не решаюсь поднять цену / просить больше
• Много делаю, но доход не растёт
• Боюсь проявляться и продавать себя
• Мне сложно выбрать направление
• Постоянно откладываю важные шаги
• Не понимаю, что именно меня останавливает
• Ваш вариант
        """)
        await state.set_state(QuestionState.waiting_for_first_finance_question)

@router.message(QuestionState.waiting_for_first_health_question)
async def run_first_health_question(message : Message, state : FSMContext):
    client_answer = message.text
    await state.update_data(first_health_question=client_answer)
    await message.answer("""
        Как вы уже пробовали это решать?
    """)
    await state.set_state(QuestionState.waiting_for_second_health_question)

@router.message(QuestionState.waiting_for_first_relationship_question)
async def run_first_relationship_question(message : Message, state : FSMContext):
    client_answer = message.text
    await state.update_data(first_relationship_question=client_answer)
    await message.answer("""
        Как вы уже пробовали это решать?
    """)
    await state.set_state(QuestionState.waiting_for_second_relationship_question)

@router.message(QuestionState.waiting_for_first_finance_question)
async def run_first_finance_question(message : Message, state : FSMContext):
    client_answer = message.text
    await state.update_data(first_finance_question=client_answer)
    await message.answer("""
        Как вы обычно реагируете, когда нужно сделать шаг, который может увеличить ваш доход?
        
• Начинаю сомневаться в себе
• Откладываю
• Ищу ещё информацию и готовлюсь/ Иду ещё обучаться
• Боюсь критики или осуждения
• Беру на себя слишком много и выгораю
• Начинаю заниматься другими людьми
• Ваш вариант 
    """)
    await state.set_state(QuestionState.waiting_for_second_finance_question)

@router.message(QuestionState.waiting_for_second_health_question)
async def run_second_health_question(message : Message, state : FSMContext):
    client_answer = message.text
    await state.update_data(second_health_question=client_answer)

    await asyncio.sleep(1)
    await message.answer('Спасибо за уделенное время 🙏, нажмите на кнопку что бы получить результат',
                            reply_markup=get_result_panel())

@router.message(QuestionState.waiting_for_second_relationship_question)
async def run_second_relationship_question(message : Message, state : FSMContext):
    client_answer = message.text
    await state.update_data(second_relationship_question=client_answer)

    await asyncio.sleep(1)
    await message.answer('Спасибо за уделенное время 🙏, нажмите на кнопку что бы получить результат',
                            reply_markup=get_result_panel())

@router.message(QuestionState.waiting_for_second_finance_question)
async def run_second_finance_question(message : Message, state : FSMContext):
    client_answer = message.text
    await state.update_data(second_finance_question=client_answer)

    await asyncio.sleep(1)
    await message.answer('Спасибо за уделенное время 🙏, нажмите на кнопку что бы получить результат',
                            reply_markup=get_result_panel())

@router.callback_query(F.data == 'get_result')
async def get_result(callback : CallbackQuery, state : FSMContext):
    await callback.answer()
    data = await state.get_data()
    request_type = data.get('request_type')




"""
[9/2/2026 7:07 PM] Мальдивы~ЮАР |Кристина Шабанова ~ ПСИХОЛОГ. РЕТРИТЫ. РАССТАНОВКИ. НЕЙРОГРАФИКА: 3 общих вопроса:

1. Что сейчас больше всего забирает вашу энергию и внимание?
• Отношения / личная жизнь
• Здоровье / состояние
• Деньги / бизнес / реализация
• Самооценка / внутреннее состояние
• Не могу понять, но чувствую, что что-то не так
• Свой вариант ____

2. Если ничего не менять в ближайшие 3-6-12 месяцев, ваш вопрос/проблема решится сама?

3. Какой результат/ состояние/ решение вы хотите получить?

По здоровью

4. Как ваше внутреннее состояние сейчас отражается на теле и самочувствии?

• Постоянно чувствую напряжение/усталость
• Есть проблемы со сном или восстановлением
• Заедаю/ Появляется лишний вес
• Часто игнорирую сигналы тела
• Раздражительность/ полное безразличие 
• Нежелание секса/отсутствие возбуждения
• Ваш вариантна теле и
5. Как вы уже пробовали это решать?

По отношениям 

4. Что чаще всего повторяется в ваших отношениях?

• Я выбираю похожих партнёров
• Мне сложно говорить о своих желаниях/чувствах/ просить о помощи
• Боюсь потерять человека и подстраиваюсь
• Мне сложно доверять и расслабляться
• Я часто оказываюсь в роли "спасающей" или «жертвы»
• Мне сложно построить близкие отношения
• Ваш вариант решение 
5. Как вы уже пробовали это решать?


По бизнесу/финансам

4. Что сейчас больше всего мешает вам выйти на более высокий финансовый или профессиональный уровень?

• Не решаюсь поднять цену / просить больше
• Много делаю, но доход не растёт
• Боюсь проявляться и продавать себя
• Мне сложно выбрать направление
• Постоянно откладываю важные шаги
• Не понимаю, что именно меня останавливает
• Ваш варианттите пол
5. Как вы обычно реагируете, когда нужно сделать шаг, который может увеличить ваш доход?
• Начинаю сомневаться в себе
• Откладываю
• Ищу ещё информацию и готовлюсь/ Иду ещё обучаться
• Боюсь критики или осуждения
• Беру на себя слишком много и выгораю
• Начинаю заниматься другими людьми
• Ваш вариант __


а после рекомендация⬇️
[9/2/2026 7:12 PM] Мальдивы~ЮАР |Кристина Шабанова ~ ПСИХОЛОГ. РЕТРИТЫ. РАССТАНОВКИ. НЕЙРОГРАФИКА: Например:

По вашим ответам видно, что сейчас основная точка напряжения - отношения. При этом вы не просто сталкиваетесь с конфликтами, а скорее повторяете определённый способ строить близость. Самостоятельно увидеть такой сценарий бывает сложно, потому что он кажется привычной частью характера.


На сессии мы можем разобрать, откуда он взялся, как именно проявляется в ваших отношениях и что можно начать менять уже сейчас.

Хотите разобрать вашу ситуацию лично со мной?
"""