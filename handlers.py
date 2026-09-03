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
from keyboards import get_request_type_panel

router = Router()

photo = FSInputFile("kris_photo.jpg")


@router.message(Command("start"))
async def start(message: Message):

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
    await asyncio.sleep(3)
    await message.answer('Выбери тему своего запроса, нажав на кнопку ниже ⬇️',
                                reply_markup=get_request_type_panel())

@router.callback_query(F.data == 'request_type_health')
async def start_test_health(callback : CallbackQuery, state : FSMContext):
    await callback.answer()
    await callback.message.answer('Скоро')


@router.callback_query(F.data == 'request_type_relationship')
async def start_test_relationship(callback : CallbackQuery, state : FSMContext):
    await callback.answer()
    await callback.message.answer('Скоро')

@router.callback_query(F.data == 'request_type_finance')
async def start_test_finance(callback : CallbackQuery, state : FSMContext):
    await callback.answer()
    await callback.message.answer('Скоро')
