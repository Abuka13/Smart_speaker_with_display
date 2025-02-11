from django.shortcuts import redirect
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}


def get_weather(request):
    url = "https://www.gismeteo.kz/weather-astana-5164/now/"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Ищем элемент temperature-value
        temp_element = soup.find('temperature-value', attrs={'from-unit': 'c'})
        if temp_element:
            temp_value = temp_element.get('value', 'N/A')
        else:
            temp_value = "N/A"

        # Ищем время
        time_element = soup.find('div', class_='now-localdate')
        time = time_element.text.strip() if time_element else "N/A"

        # Добавим дополнительную информацию о погоде
        feel_temp_element = soup.find('div', class_='now-feel').find('temperature-value')
        feel_temp = feel_temp_element.get('value', 'N/A') if feel_temp_element else "N/A"

        desc_element = soup.find('div', class_='now-desc')
        weather_desc = desc_element.text.strip() if desc_element else "N/A"

        # Формируем ответ
        response_text = (
            f"{temp_value[:]}°C\n"
        )

        print(response_text)  # Для отладки
        return HttpResponse(response_text.replace('\n', '<br>'), content_type='text/html')

    except requests.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        return HttpResponse("Ошибка при подключении к сервису погоды.")
    except Exception as e:
        print(f"Общая ошибка: {e}")
        return HttpResponse("Ошибка при получении данных о погоде.")


def youtube(request):
    return redirect('https://www.youtube.com')


def instagram(request):
    return redirect('https://www.instagram.com')