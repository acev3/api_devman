# Бот уведомитель
Скрипт, который запускает бота, отправляющего уведомление о проверенных работах на сайте [devman](https://dvmn.org/modules/).
# Как запустить
* Для запуска сайта вам понадобится Python третьей версии.
* Скачайте код с GitHub. Затем установите зависимости
```sh
pip install -r requirements.txt
```
* Создайте файл `.env` в директории с проектом.
* Заполните `.env` следующими переменными:
```sh
CHAT_ID=chat_id
TELEGRAM_API_TOKEN=telegram_token
DEVMAN_API_TOKEN=devman_token
```
chat_id - можно получить, написав боту `@userinfobot`
 
telegram_token - можно получить при создании бота через `@BotFather`

devman_token - в [api devman](https://dvmn.org/api/docs/)

Запустите код
```sh
python main.py
```
### Цель проекта
Код написан в образовательных целях на курсе для веб-разработчиков [dvmn.org](https://dvmn.org/modules/).



