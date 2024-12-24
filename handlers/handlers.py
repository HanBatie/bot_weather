import asyncio
import logging
import subprocess  # Добавлено для запуска app.py

from aiogram import types, F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import keyboards.kb as kb
import keyboards.inl as inl
from services.weather_service import get_weather_forecast

router = Router()

class WeatherForecast(StatesGroup):
    user_id = State()
    start_point = State()
    end_point = State()
    other_points = State()
    time_interval = State() # в днях 


@router.message(CommandStart())
async def command_start_handler(message: types.Message):
    await message.answer(f'Привет, {message.from_user.first_name}!', reply_markup=kb.get_forecast)

@router.message(Command("help"))
async def help_handler(message: types.Message):
    help_text = (
        "Доступные команды:\n"
        "/start - Начать работу с ботом\n"
        "/help - Получить справку по командам\n"
        "/weather - Запросить прогноз погоды\n\n"
        "Используйте /weather, чтобы запросить прогноз погоды. Следуйте инструкциям бота для ввода начальной и конечной точек маршрута, временного интервала и других параметров."
    )
    await message.answer(help_text)

#Получение города отправления
@router.message(Command("weather"))
@router.message(F.text == 'Ввести данные для прогноза')
async def weather_handler(message: types.Message, state: FSMContext):
    await message.answer("Пожалуйста, введите город отправления.")
    await state.update_data(user_id=message.from_user.id)
    await state.set_state(WeatherForecast.start_point)

@router.callback_query(F.data == 'rewrite_start_point')
async def rewrite_start_point(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Пожалуйста, введите город отправления.")
    await state.set_state(WeatherForecast.start_point)

@router.message(WeatherForecast.start_point)
async def process_start_point(message: types.Message, state: FSMContext):
    await state.update_data(start_point=message.text)
    await message.answer(f"Город отправления: {message.text}\nВведите город назначения", reply_markup=inl.rewrite_start_point)
    await state.set_state(WeatherForecast.end_point)

#Получение города назначения
@router.callback_query(F.data == 'rewrite_end_point')
async def rewrite_end_point(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Введите город назначения.")
    await state.set_state(WeatherForecast.end_point)

@router.message(WeatherForecast.end_point)
async def process_end_point(message: types.Message, state: FSMContext):
    await state.update_data(end_point=message.text)
    await message.answer(f"Город назначения: {message.text}",
                         reply_markup=inl.rewrite_end_point)
    
#Получение временного интервала
@router.callback_query(F.data == 'give_time_interval')
async def give_time_interval(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Выберите временной интервал", reply_markup=kb.time_interval)
    await state.set_state(WeatherForecast.time_interval)

#Вывод данных от пользователя
@router.message(WeatherForecast.time_interval)
async def process_time_interval(message: types.Message, state: FSMContext):
    await state.update_data(time_interval=message.text)
    data = await state.get_data()
    await message.answer(f"Проверьте правильность введенных данных:\n"
                         f"Пункт отправления: {data['start_point']}\n"
                         f"Пункт назначения: {data['end_point']}\n"
                         f"Промежуточные пункты: {data.get('other_points', '')}\n"
                         f"Временной интервал: {data['time_interval']}\n"
                         f"Проверьте введённую информацию",
                         reply_markup=inl.check_data)

async def check_data(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(f"Проверьте правильность введенных данных:\n"
                         f"Пункт отправления: {data['start_point']}\n"
                         f"Пункт назначения: {data['end_point']}\n"
                         f"Промежуточные пункты: {data.get('other_points', '')}\n"
                         f"Временной интервал: {data['time_interval']}\n"
                         f"Проверьте введённую информацию",
                         reply_markup=inl.check_data)

#Получение промежуточных точек
@router.callback_query(F.data == 'other_points')
async def other_points(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите промежуточные точки(через запятую)", reply_markup=None)
    await state.set_state(WeatherForecast.other_points)

@router.message(WeatherForecast.other_points)
async def process_other_points(message: types.Message, state: FSMContext):
    await state.update_data(other_points=message.text)
    await message.answer(await check_data(message, state))

#Получение прогноза
@router.callback_query(F.data == 'correct_data')
async def correct_data(callback: types.CallbackQuery, state: FSMContext):

    await callback.message.answer("Получение прогноза погоды...")
    data = await state.get_data()
    logging.debug(f"Данные пользователя: {data}")
    logging.info(f"Получен запрос на получение прогноза погоды. id: {data['user_id']}")

    start_city = data.get('start_point')
    end_city = data.get('end_point')
    intermediate_cities = data.get('other_points', '')
    days_text = data.get('time_interval').strip()
    days = int(days_text.split()[0])

    # Формируем URL для графиков
    graph_url = f"http://127.0.0.1:5000/?start={start_city}&end={end_city}&days={days}"
    if intermediate_cities:
        graph_url += f"&via={intermediate_cities}"

    # Создаем инлайн-кнопку для графиков
    graphs_keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="📊 Интерактивные графики", url=graph_url)]
    ])

    # Получение прогноза погоды
    forecast_message = await get_weather_forecast(
        start_city=start_city,
        end_city=end_city,
        intermediate_cities=intermediate_cities,
        days=days
    )

    try:
        subprocess.Popen(['python', 'services/web_weather/app.py'])  # Замените путь на актуальный
        logging.info("Dash-приложение запущено.")
    except Exception as e:
        logging.error(f"Ошибка при запуске Dash-приложения: {e}")
        await callback.message.answer(forecast_message, "Не удалось построить графики", reply_markup=None)
        return
    
    await callback.message.answer(forecast_message, parse_mode='Markdown', reply_markup=graphs_keyboard)

