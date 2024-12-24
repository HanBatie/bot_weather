import logging
from services.api_req import Weather
from config import WEATHER_API_KEY

async def get_weather_forecast(start_city: str, end_city: str, intermediate_cities: str, days: int):
    """
    Получает прогноз погоды для указанных городов и возвращает сформированное сообщение с прогнозом.
    
    """
    weather_api = Weather(api_key=WEATHER_API_KEY)
    
    # Обработка промежуточных городов
    cities = [start_city]
    if intermediate_cities:
        intermediates = [city.strip() for city in intermediate_cities.split(',') if city.strip()]
        cities.extend(intermediates)
    cities.append(end_city)
    print(cities)
    
    forecast_results = {}
    
    for city in cities:
        forecast = weather_api.get_forecast_weather_data(city, days=days)
        if isinstance(forecast, tuple) or isinstance(forecast, int):
            error_message = f"Ошибка при получении данных для города {city}: {forecast}"
            logging.error(error_message)
            return error_message
        elif not forecast:
            error_message = f"Нет данных для города {city}."
            logging.error(error_message)
            return error_message
        forecast_results[city] = forecast
    
    # Формирование сообщения с прогнозом
    forecast_message = "📅 Прогноз погоды:\n\n"
    for city, forecast in forecast_results.items():
        forecast_message += f"**{city}**\n"
        for day in forecast:
            date = day['date']
            temp_min = day['temp_min']
            temp_max = day['temp_max']
            wind_speed = day['wind_speed']
            humidity = day['humidity']
            precipitation_prob = day['precipitation_prob']
            forecast_message += (f"• {date}:\n      Температура: Мин {temp_min}°C, Макс {temp_max}°C \n     Ветер {wind_speed} км/ч \n "
                                 f"     Влажность {humidity}% \n    Возможность дождя {precipitation_prob}%\n")
        forecast_message += "\n"
    
    return forecast_message
