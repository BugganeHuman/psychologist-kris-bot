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

router = Router()