from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
import requests
from bs4 import BeautifulSoup
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/102.0.0.0 Safari/537.36'
}
def get_weather(request):
    response = requests.get("https://www.gismeteo.kz/weather-astana-5164/", headers=headers).text

    sep1 = '<div class="date">Сейчас</div>'
    text2 = response.split(sep=sep1)[1]

    sep2 = '</div></div><svg class'
    arr3 = text2.split(sep=sep2)
    text3 = arr3[0]

    sep3 = 'class="unit unit_temperature_c">'
    text4 = text3.split(sep=sep3)[1::]

    time_sep = '<div class="day" data-pattern="G:i">'
    time = text3.split(sep=time_sep)[1].split('</div>')[0]

    temp_sign = text4[0].split('</span>')[0][-1]


    temp_value = text4[1].split('<span class="sign">')[0]
    temp_value = text4[0].split('</span>')[1]

    print(f"Время: {time}")
    print(f"Знак температуры: {temp_sign}")
    print(f"Значение температуры: {temp_value}")

    return HttpResponse(f"{time},{temp_sign},{temp_value}")


def youtube(request):
    return redirect('https://www.youtube.com')

def instagram(request):
    return redirect('https://www.instagram.com')
