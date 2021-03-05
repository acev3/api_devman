import requests
from requests.exceptions import ConnectionError
import telegram
from dotenv import load_dotenv
import os
import time
import logging


logger = logging.getLogger("BotLogger")


class MyLogsHandler(logging.Handler):
    def __init__(self, bot, chat_id):
        super().__init__()
        self.bot = bot
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=str(log_entry))


def bot_worker(bot, devman_api_token, chat_id):
    logger.info('Бот запущен')
    time_for_sleep = 60
    payload = {}
    headers = {'Authorization': 'Token {}'.format(devman_api_token)}
    while True:
        try:
            response = requests.get('https://dvmn.org/api/long_polling/',
                                    params=payload, headers=headers
                                    )
            response.raise_for_status()
            decoded_response = response.json()
            if decoded_response['status'] == 'timeout':
                payload['timestamp'] = decoded_response['timestamp_to_request']
            else:
                payload['timestamp'] = decoded_response['last_attempt_timestamp']
                new_attempts = decoded_response['new_attempts']
                for attempt in new_attempts:
                    title = attempt['lesson_title']
                    text = """Преподавателю все понравилось,
                        можно приступать к следующему уроку!"""
                    if attempt['is_negative']:
                        text = "К сожалению в работе нашлись ошибки."
                    bot.send_message(chat_id=chat_id,
                                     text='У вас проверили работу "{}".\n\n{}'
                                     .format(title, text)
                                     )
        except requests.exceptions.ReadTimeout as err:
            logger.error(err, exc_info=True)
        except ConnectionError:
            time.sleep(time_for_sleep)



def main():
    load_dotenv()
    devman_api_token = os.environ['DEVMAN_API_TOKEN']
    api_tme_token = os.environ['TELEGRAM_API_TOKEN']
    chat_id = os.environ['CHAT_ID']
    bot = telegram.Bot(token=api_tme_token)
    logger.addHandler(MyLogsHandler(bot, chat_id))
    logger.setLevel(logging.INFO)
    bot_worker(bot, devman_api_token, chat_id)


if __name__ == '__main__':
    main()

