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
from keyboards import (get_request_type_panel, get_result_panel,
    get_first_base_question_panel, get_second_base_question_panel,
    get_first_health_question_panel, get_first_relationship_question_panel,
    get_first_finance_question_panel, get_second_finance_question_panel,
    get_final_panel)
from claude_api import get_claude_analysis
from aiogram.utils.media_group import MediaGroupBuilder

router = Router()

start_video = FSInputFile("video.mp4")
final_video = FSInputFile("video 2.mp4")

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

    await message.answer_video_note(
        video_note=start_video)
    await message.answer( """
<b>Кристина Шабанова | психолог</b>\n
➡️ <a href='https://www.instagram.com/psyholog.shabanova'>Instagram</a>
➡️ <a href='https://t.me/izmeni_gzizn'>Telegram</a>
➡️ <a href='https://www.instagram.com/retreat_kris'>Ретриты</a>

Помогаю увидеть причины повторяющихся сценариев в 
<b>отношениях, деньгах, реализации и внутреннем состоянии </b> и 
найти то, что мешает прийти к желаемому результату.

В работе мне важно не просто поговорить о проблеме, а помочь тебе <b> увидеть её глубже и запустить здоровое изменение. </b>

🤍 Эта диагностика - первый шаг
    """, disable_web_page_preview=True, parse_mode='HTML'
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
    
• Выбери из вариантов ответов
• Или напиши свой вариант
    """, reply_markup=get_first_base_question_panel())

    #await callback.message.answer(rt)
    await state.set_state(QuestionState.waiting_for_first_base_question)


@router.message(QuestionState.waiting_for_first_base_question)
async def run_first_base_question (message : Message, state : FSMContext):
    client_answer = message.text
    await state.update_data(first_base_answer=client_answer)
    await message.answer('Если ничего не менять в ближайшие 3-6-12 месяцев, ваш вопрос/проблема решится сама?',
                         reply_markup=get_second_base_question_panel())
    await state.set_state(QuestionState.waiting_for_second_base_question)

@router.message(QuestionState.waiting_for_second_base_question)
async def run_second_base_question (message : Message, state : FSMContext):
    client_answer = message.text
    await state.update_data(second_base_answer=client_answer)
    await message.answer('Напиши какой результат/ состояние/ решение хочешь получить? ⬇️')
    await state.set_state(QuestionState.waiting_for_third_base_question)

@router.message(QuestionState.waiting_for_third_base_question)
async def run_third_base_question (message : Message, state : FSMContext):
    client_answer = message.text
    await state.update_data(third_base_answer=client_answer)

    data = await state.get_data()
    request_type = data.get('request_type')

    if request_type == 'health':
        await message.answer("""
        Как ваше внутреннее состояние сейчас отражается на теле и самочувствии?

• Выбери из вариантов ответов
• Или напиши свой вариант
        """, reply_markup=get_first_health_question_panel())
        await state.set_state(QuestionState.waiting_for_first_health_question)

    elif request_type == 'relationship':
        await message.answer("""
        Что чаще всего повторяется в ваших отношениях?

• Выбери из вариантов ответов
• Ваш вариант решение 
        """, reply_markup=get_first_relationship_question_panel())
        await state.set_state(QuestionState.waiting_for_first_relationship_question)

    elif request_type == 'finance':
        await message.answer("""
        Что сейчас больше всего мешает вам выйти на более высокий финансовый или профессиональный уровень?


• Выбери из вариантов ответов
• Ваш вариант
        """, reply_markup=get_first_finance_question_panel())
        await state.set_state(QuestionState.waiting_for_first_finance_question)

@router.message(QuestionState.waiting_for_first_health_question)
async def run_first_health_question(message : Message, state : FSMContext):
    client_answer = message.text
    await state.update_data(first_health_answer=client_answer)
    await message.answer("""
        Как вы уже пробовали это решать?
    """)
    await state.set_state(QuestionState.waiting_for_second_health_question)

@router.message(QuestionState.waiting_for_first_relationship_question)
async def run_first_relationship_question(message : Message, state : FSMContext):
    client_answer = message.text
    await state.update_data(first_relationship_answer=client_answer)
    await message.answer("""
        Как вы уже пробовали это решать?
    """)
    await state.set_state(QuestionState.waiting_for_second_relationship_question)

@router.message(QuestionState.waiting_for_first_finance_question)
async def run_first_finance_question(message : Message, state : FSMContext):
    client_answer = message.text
    await state.update_data(first_finance_answer=client_answer)
    await message.answer("""
        Как вы обычно реагируете, когда нужно сделать шаг, который может увеличить ваш доход?
        
• Выбери из вариантов ответов
• Или напиши свой вариант
    """, reply_markup=get_second_finance_question_panel())
    await state.set_state(QuestionState.waiting_for_second_finance_question)

@router.message(QuestionState.waiting_for_second_health_question)
async def run_second_health_question(message : Message, state : FSMContext):
    client_answer = message.text
    await state.update_data(second_health_answer=client_answer)

    await asyncio.sleep(1)
    await message.answer('Спасибо за уделенное время 🙏, нажмите на кнопку что бы получить результат',
                            reply_markup=get_result_panel())

@router.message(QuestionState.waiting_for_second_relationship_question)
async def run_second_relationship_question(message : Message, state : FSMContext):
    client_answer = message.text
    await state.update_data(second_relationship_answer=client_answer)

    await asyncio.sleep(1)
    await message.answer('Спасибо за уделенное время 🙏, нажмите на кнопку что бы получить результат',
                            reply_markup=get_result_panel())

@router.message(QuestionState.waiting_for_second_finance_question)
async def run_second_finance_question(message : Message, state : FSMContext):
    client_answer = message.text
    await state.update_data(second_finance_answer=client_answer)

    await asyncio.sleep(1)
    await message.answer('Спасибо за уделенное время 🙏, нажмите на кнопку что бы получить результат',
                            reply_markup=get_result_panel())

@router.callback_query(F.data == 'get_result')
async def get_result(callback : CallbackQuery, state : FSMContext):
    await callback.answer()
    data = await state.get_data()
    request_type = data.get('request_type')

    answers = {
        'first_base_answer' : data.get('first_base_answer', ''),
        'second_base_answer' : data.get('second_base_answer', ''),
        'third_base_answer': data.get('third_base_answer', ''),
        'first_health_answer': data.get('first_health_answer', ''),
        'second_health_answer': data.get('second_health_answer', ''),
        'first_relationship_answer' : data.get('first_relationship_answer', ''),
        'second_relationship_answer': data.get('second_relationship_answer', ''),
        'first_finance_answer': data.get('first_finance_answer', ''),
        'second_finance_answer': data.get('second_finance_answer'),
    }

    result = get_claude_analysis(request_type, answers)
    await callback.message.answer(result, parse_mode="HTML")
    await callback.message.answer_video_note(video_note=final_video)
    await callback.message.answer('Можешь выбрать то что тебе больше подходит',
                            reply_markup=get_final_panel())


@router.callback_query(F.data == 'get_reviews')
async def run_show_reviews(callback : CallbackQuery, state : FSMContext):
    await callback.answer()
    media_group = MediaGroupBuilder(caption='Отзывы')
    media_group.add_photo(media=FSInputFile('reviews/photo_1_2026-09-09_15-15-03.jpg'))
    media_group.add_photo(media=FSInputFile('reviews/photo_2_2026-09-09_15-15-03.jpg'))
    media_group.add_photo(media=FSInputFile('reviews/photo_3_2026-09-09_15-15-03.jpg'))
    media_group.add_photo(media=FSInputFile('reviews/photo_4_2026-09-09_15-15-03.jpg'))
    media_group.add_photo(media=FSInputFile('reviews/photo_5_2026-09-09_15-15-03.jpg'))
    media_group.add_photo(media=FSInputFile('reviews/photo_6_2026-09-09_15-15-03.jpg'))
    media_group.add_photo(media=FSInputFile('reviews/photo_7_2026-09-09_15-15-03.jpg'))
    media_group.add_photo(media=FSInputFile('reviews/photo_8_2026-09-09_15-15-03.jpg'))
    media_group.add_photo(media=FSInputFile('reviews/photo_9_2026-09-09_15-15-03.jpg'))
    media_group.add_photo(media=FSInputFile('reviews/photo_10_2026-09-09_15-15-03.jpg'))

    await callback.message.answer_media_group(
        media=media_group.build()
    )

    await callback.message.answer('Можешь выбрать что тебе больше подходит',
                                reply_markup=get_final_panel())

@router.callback_query(F.data == 'get_payment_of_reflection_table')
async def run_payment_of_reflection_table(callback : CallbackQuery, state : FSMContext):
    await callback.answer()
    await callback.message.answer("""
    Отлично, хороший выбор.
Отправь оплату 199 рублей по реквизитам:
    
тут реквизиты 
    
Напиши с чеком @kris_shabanova, я ни применено отправлю тебе таблицу
    
    """)