import os
from pprint import pprint
import time

import requests


HEADERS = {
    'Accept': 'application/json, text/javascript, */*;',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0',
    'Referer': 'https://e-dostavka.by/'
}
ENDPOINT = 'https://e-dostavka.by/dzone/'
NO_TIME_STR = 'Доступное время для заказа отсутствует.'
BOT_TOKEN = os.environ['BOT_TOKEN']
TG_CHAT_ID = os.environ['TG_CHAT_ID']
ZONE = os.environ.get(
    'ZONE',
    'Интернет-магазин 50160 Минск (Западный промузел, ТЭЦ 4), зона обслуживания А, интервал доставки 2 часа'
)

TG_MESSAGE = """
Доставка: {0}
Экспресс: {1}
"""


def telegram_bot_sendtext(message, bot_token, chat_id, retry=6):
    """Send text via telegram."""
    send_text = (
        'https://api.telegram.org/bot' +
        bot_token +
        '/sendMessage?chat_id=' +
        chat_id +
        '&parse_mode=Markdown&text=' +
        message
    )
    try:
        response = requests.get(send_text)
    except Exception as exc:
        print('TG send exception {0}'.format(exc))
        if retry > 0:
            retry -= 1
            time.sleep(1)
            telegram_bot_sendtext(message, bot_token, chat_id, retry=retry)
    return response.json()


def get_shops_data(city='Минск и Минская область'):
    """Emulate browser request to get json data."""
    params = {
        'action': 'zonesDataJson',
        'city': city
    }
    req = requests.get(
        ENDPOINT, params=params, headers=HEADERS
    )

    if req.status_code == 200:
        return req.json()
    else:
        raise RuntimeError(req.status_code)


def check_status(shops_data, check_zone=ZONE):
    """Check records."""
    for record_id, record_data in shops_data.items():
        if isinstance(record_data, dict):
            zone_name = record_data.get('description')
            next_free_slot = record_data.get('next_free_slot')
            next_free_slot_express = record_data.get('next_free_slot_express')

            if zone_name == check_zone:
                if (next_free_slot != NO_TIME_STR or
                        next_free_slot_express):
                        telegram_bot_sendtext(
                            TG_MESSAGE.format(next_free_slot, next_free_slot_express),
                            BOT_TOKEN,
                            TG_CHAT_ID
                        )


if __name__ == '__main__':
    print('Checking time slots')
    shops_data = get_shops_data()
    check_status(shops_data)
