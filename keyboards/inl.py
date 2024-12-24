from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

rewrite_start_point = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Изменить город отправления', callback_data='rewrite_start_point')]
    ]
)

rewrite_end_point = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Изменить город назначения', callback_data='rewrite_end_point')], 
        [InlineKeyboardButton(text='Выбрать временной промежуток', callback_data='give_time_interval')]
    ]
)

check_data = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Всё верно, получить прогноз', callback_data='correct_data')],
        [InlineKeyboardButton(text='Изменить город отправления', callback_data='rewrite_start_point')],
        [InlineKeyboardButton(text='Изменить город назначения', callback_data='rewrite_end_point')],
        [InlineKeyboardButton(text='Изменить временной промежуток', callback_data='give_time_interval')],
        [InlineKeyboardButton(text='Добавить промежуточные точки', callback_data='other_points')]
    ]
)
