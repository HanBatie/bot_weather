from aiogram.types import KeyboardButton, ReplyKeyboardMarkup 

get_forecast = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Ввести данные для прогноза')]],
                                  resize_keyboard=True, one_time_keyboard=True, input_field_placeholder='Выберите действие или введите команду')

time_interval = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='1 день')], 
                                              [KeyboardButton(text='3 дня')], 
                                              [KeyboardButton(text='5 дней')]],
                                    resize_keyboard=True, one_time_keyboard=True, input_field_placeholder='Выберите временной интервал')
