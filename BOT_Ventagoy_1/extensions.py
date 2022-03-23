import requests
import json
from setup import ACCESS_KEY, keys # импорт констант для работы функции

class APIException(Exception):
    pass

class Convert:
    @staticmethod
    def get_price(n: str, v1: str, v2: str):
        try:
            n_tic = float(n)
        except ValueError:
            raise APIException(f'ошибка в указании количества валюты-{n}')
        try:
            v1_tic = keys[v1]
        except KeyError:
            raise APIException(f'нет данной валюты в базе бота-{v1}')
        try:
            v2_tic = keys[v2]
        except KeyError:
            raise APIException(f'нет данной валюты в базе бота-{v2}')
        if v1 == v2:
            raise APIException(f'конверсия одинаковой валюты--> {keys[v1]}')
        r = requests.get(f"http://api.exchangeratesapi.io/v1/latest?access_key={ACCESS_KEY}&symbols={v1_tic},{v2_tic}")
        # получение курса валют базовой и конечной по отношению к евро ( привязка к евро так как бесплатное API
        a = json.loads(r.content) # преобразование полученных данных в словарь
        v1_cot=float(a['rates'][v1_tic]) # получение из а курса базовой валюты
        v2_cot = float(a['rates'][v2_tic])# получение из а курса конечной валюты
        return round((v2_cot/v1_cot)*n_tic,2) # вычисление результата в конечной валюте
