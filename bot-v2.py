# API еще не готово

import telebot
import json

API_TOKEN = '7230737615:AAH2PwsnMRpSRz6kIkLbn4pOhCM4-jhkuOI'

bot = telebot.TeleBot(API_TOKEN)

# state - через него передаются статусы пользователя, например: пользователь хочет залогиниться, в state добавляется пользователь
# и его статус, так бот понимает, для чего ему отправляются сообщения
# также туда можно пихать любые временные параметры вместо args
state = {
    "example": {
        "state": "example-state",
        "args": "example-args"
    }
}

# send - функция которая всегда отправляет сообщение с parse mode HTML (я заебусь его каждый раз писать)
def send(message, text, **kwargs):
    return bot.send_message(message.chat.id, text, parse_mode='HTML', **kwargs)

# save - функция которая открывает и сохраняет json файлы (я того рот ебал каждый раз писать открытие файла, я такую функцию делаю в каждом проекте)
def save(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# load - альтернатива функции save
def load(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

@bot.message_handler(commands=['start'])
def send_welcome(message: telebot.types.Message):
    send(
            message, 
            f"Привет, я <strong>{bot_info.first_name}</strong> - полная замена <strong>Atom Mobility</strong>.\nC помощью меня ты можешь:\n    <strong>· отправлять команды на самокат\n    · менять статус самоката\n    · оставлять заметки на самокате\n    · добавлять таски\n    · смотреть таски\n    · получать IMEI по номеру самоката\n    · получать номер самоката по IMEI'ю\n    · генерировать qr-код по номеру</strong>\n   и <strong>многое</strong> другое!\n\nОтправь мне <strong>/help</strong> чтобы узнать как им пользоватся."
        )

@bot.message_handler(commands=['login'])
def send_login(message: telebot.types.Message):
    global state

    send(
            message, 
            f"Сначала, мне необходимо войти в твой <strong>аккаунт</strong>.\nНужно это для того чтобы все твои действия в Атоме отображались от <strong>твоего имени</strong> в Атоме.\n(бот эти данные <strong>никак не обрабатывает</strong>, исходный код есть на github)\n\nОтправь мне почту и пароль одним сообщением через <strong>перенос строки</strong>.\n\nПример:\nshef.podnimite.zarplatu@gmail.com\nFastFox228!"
        )
    state[message.from_user.id] = {"state": "login"}

@bot.message_handler(func=lambda message: True)
def echo_all(message: telebot.types.Message):
    global state

    user_id = message.from_user.id
    username = message.from_user.username
    if user_id in state:
        if state[user_id]['state'] == 'login':
            mail, password = map(message.text.split('\n'))
            bot.delete_message(message.chat.id, message.id)
            send(message, f"Отправляю запрос в <strong>Атом</strong>...")
            # запрос на сервер через api

if __name__ == '__main__':
    bot_info = bot.get_me()
    print(f"atom fox api bot started!\nBot name:\n  {bot_info.first_name}\nBot username:\n  @{bot_info.username}\nsdelano hackerom dmitriem")
    bot.infinity_polling()