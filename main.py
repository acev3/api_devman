import requests
from requests.exceptions import ConnectionError
import telegram
from dotenv import load_dotenv
import os


def main():
    load_dotenv()
    devman_api_token = os.environ['DEVMAN_API_TOKEN']
    api_tme_token = os.environ['TELEGRAM_API_TOKEN']
    chat_id = os.environ['CHAT_ID']
    bot = telegram.Bot(token=api_tme_token)
    payload = {}
    headers = {'Authorization': 'Token {}'.format(devman_api_token)}
    while True:
        try:
            response = requests.get('https://dvmn.org/api/long_polling/',
                                    params=payload, headers=headers
                                    )
            response.raise_for_status()
            response_json = response.json()
            if response_json['status'] == 'timeout':
                payload['timestamp'] = response_json['timestamp_to_request']
            else:
                payload['timestamp'] = response_json['last_attempt_timestamp']
                new_attempts = response_json['new_attempts']
                for attempt in new_attempts:
                    title = attempt['lesson_title']
                    text = "Преподавателю все понравилось, можно приступать к следующему уроку!"
                    if attempt['is_negative']==True:
                        text = "К сожалению в работе нашлись ошибки."
                    bot.send_message(chat_id=chat_id,
                                     text='У вас проверили работу "{}".\n\n{}'\
                                     .format(title,text)
                                     )
        except requests.exceptions.ReadTimeout:
            pass
        except ConnectionError:
            pass


if __name__ == '__main__':
    main()
