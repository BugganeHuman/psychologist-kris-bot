from aiogram import types
from aiogram.types import InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def get_request_type_panel():
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text="Здоровье", callback_data="request_type_health")
    )
    builder.row(
        InlineKeyboardButton(
            text="Отношения", callback_data="request_type_relationship"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Бизнесс / Финансы", callback_data="request_type_finance"
        )
    )
    return builder.as_markup()

def get_result_panel():
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text='Получить результат ✅', callback_data='get_result')
    )
    return builder.as_markup()

def get_first_base_question_panel():
    builder = ReplyKeyboardBuilder()

    builder.row(
        KeyboardButton(text='Отношения / личная жизнь')
    )
    builder.row(
        KeyboardButton(text='Здоровье / состояние')
    )
    builder.row(
        KeyboardButton(text='Деньги / бизнес / реализация')
    )
    builder.row(
        KeyboardButton(text='Самооценка / внутреннее состояние')
    )
    builder.row(
        KeyboardButton(text='Не могу понять, но чувствую, что что-то не так')
    )

    return builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Выберите действие...",
        one_time_keyboard=True
    )

def get_second_base_question_panel():
    builder = ReplyKeyboardBuilder()

    builder.row(
        KeyboardButton(text='Да')
    )
    builder.row(
        KeyboardButton(text='Нет')
    )

    return builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Выберите действие...",
        one_time_keyboard=True
    )

def get_first_health_question_panel():
    builder = ReplyKeyboardBuilder()

    builder.row(
        KeyboardButton(text='Постоянно чувствую напряжение/усталость')
    )
    builder.row(
        KeyboardButton(text='Есть проблемы со сном или восстановлением')
    )
    builder.row(
        KeyboardButton(text='Заедаю/ Появляется лишний вес')
    )
    builder.row(
        KeyboardButton(text='Часто игнорирую сигналы тела')
    )
    builder.row(
        KeyboardButton(text='Раздражительность/ полное безразличие')
    )
    builder.row(
        KeyboardButton(text='Нежелание секса/отсутствие возбуждения')
    )

    return builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Выберите действие...",
        one_time_keyboard=True
    )

def get_first_relationship_question_panel():
    builder = ReplyKeyboardBuilder()

    builder.row(
        KeyboardButton(text='Я выбираю похожих партнёров')
    )
    builder.row(
        KeyboardButton(text='Мне сложно говорить о своих желаниях/чувствах/ просить о помощи')
    )
    builder.row(
        KeyboardButton(text='Боюсь потерять человека и подстраиваюсь')
    )
    builder.row(
        KeyboardButton(text='Мне сложно доверять и расслабляться')
    )
    builder.row(
        KeyboardButton(text='Я часто оказываюсь в роли "спасающей" или «жертвы»')
    )
    builder.row(
        KeyboardButton(text='Мне сложно построить близкие отношения')
    )

    return builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Выберите действие...",
        one_time_keyboard=True
    )

def get_first_finance_question_panel():
    builder = ReplyKeyboardBuilder()

    builder.row(
        KeyboardButton(text='Не решаюсь поднять цену / просить больше')
    )
    builder.row(
        KeyboardButton(text='Много делаю, но доход не растёт')
    )
    builder.row(
        KeyboardButton(text='Боюсь проявляться и продавать себя')
    )
    builder.row(
        KeyboardButton(text='Мне сложно выбрать направление')
    )
    builder.row(
        KeyboardButton(text='Постоянно откладываю важные шаги')
    )
    builder.row(
        KeyboardButton(text='Не понимаю, что именно меня останавливает')
    )

    return builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Выберите действие...",
        one_time_keyboard=True
    )

def get_second_finance_question_panel():
    builder = ReplyKeyboardBuilder()

    builder.row(
        KeyboardButton(text='Начинаю сомневаться в себе')
    )
    builder.row(
        KeyboardButton(text='Откладываю')
    )
    builder.row(
        KeyboardButton(text='Ищу ещё информацию и готовлюсь/ Иду ещё обучаться')
    )
    builder.row(
        KeyboardButton(text='Боюсь критики или осуждения')
    )
    builder.row(
        KeyboardButton(text='Беру на себя слишком много и выгораю')
    )
    builder.row(
        KeyboardButton(text='Начинаю заниматься другими людьми')
    )

    return builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Выберите действие...",
        one_time_keyboard=True
    )

def get_final_panel():

    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text='👋 Созвон-знакомство 15-30 мин', url='https://t.me/kris_shabanova')
    )
    builder.row(
        InlineKeyboardButton(text='🧘 Записаться на сессию', url='https://t.me/kris_shabanova')
    )
    builder.row(
        InlineKeyboardButton(text='✍️ Заполнить таблицу само рефлексии 199₽',
                                callback_data='get_payment_of_reflection_table')
    )
    builder.row(
        InlineKeyboardButton(text='⭐ Посмотреть отзывы', callback_data='get_reviews')
    )

    return builder.as_markup()