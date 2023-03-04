# подключение библиотеки telebot
# В google colab добавить: !pip install pyTelegramBotAPI
# для установки необходимо в файл requirements.text добавить строку
# 'PyTelegramBotApi'
from telebot import TeleBot, types
import json

bot = TeleBot(token='Вставь_свой_токен', parse_mode='html') # создание бота


# обработчик команды '/start'
@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)
    #def start_command_handler(message: types.Message):
    # отправляем ответ на команду '/start'
    bot.send_message(
        chat_id=message.chat.id, # id чата, в который необходимо направить сообщение
        text='Привет 👋, {0.first_name}! \n\nНе узнаешь?\n\nЭто я – Бот-ассистент 🤖!\n'.format(message.from_user, bot.get_me()), # текст сообщения
    )

    bot.send_message(
        chat_id=message.chat.id, # id чата, в который необходимо направить сообщение
        text='Вот, что я умею:\n\n✅ - помогу проверить твой JSON;\n\n✅ - помогу оформить его красиво;\n\n✅ - подскажу, если что-то пойдет не так.', # текст сообщения
    )
    bot.send_message(
        chat_id=message.chat.id, # id чата, в который необходимо направить сообщение
        text='Присылай свой JSON и посмотрим 🔍, что у тебя там:', # текст сообщения
    )

# обработчик всех остальных сообщений
@bot.message_handler()
def message_handler(message: types.Message):
    try:
        # пытаемся распарсить JSON из текста сообщения
        payload = json.loads(message.text)
    except json.JSONDecodeError as ex:
        # при ошибке взникнет исключение 'json.JSONDecodeError'
        # преобразовываем исключение в строку и выводим пользователю
        bot.send_message(
            chat_id=message.chat.id,
            text=f'У тебя есть ошибки:\n<code>{str(ex)}</code>'
        )
        # выходим из функции
        return
    
    # если исключения не возникло - значит был введен корректный JSON
    # форматируем его в красивый текст :) (отступ 2 пробела на уровень, сортировать ключи по алфавиту)
    text = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False)
    # и выводим пользователю
    bot.send_message(
        chat_id=message.chat.id,
        text=f'Все отлично, вот твой JSON:\n<code>{text}</code>'
    )


# главная функция программы
def main():
    # запускаем нашего бота
    bot.infinity_polling()


if __name__ == '__main__':
    main()