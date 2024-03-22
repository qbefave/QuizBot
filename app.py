import telebot
from quiz_data import DataBase
from config import *
from telebot import types
from utils import most_common_digit

bot = telebot.TeleBot(TOKEN)

db = DataBase()
@bot.message_handler(commands=['start', 'help'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Пройти викторину")
    btn2 = types.KeyboardButton("Контакты")
    btn3 = types.KeyboardButton("Обратная связь")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.from_user.id,
                     "Привет!👋  В этом боте ты сможешь определить свое тотемное животное, пройдя небольшой тест😃",
                     reply_markup=markup)


def get_question_message(user):
    if user["question_index"] == db.questions_count:
        result = most_common_digit(user["answers"])

        if result == 0:
            animal = "Ягуар🐆"
            lore = animal1

        elif result == 1:
            animal = "Медведь🐻"
            lore = animal2

        elif result == 2:
            animal = "Дельфин🐬"
            lore = animal3
        else:
            animal = "Ленивец🦥"
            lore = animal4



        text = f"Твое тотемное животное: {animal} \n\n{lore}\n\nПодробнее узнать о своем тотемном и других животных ты можешь на сайте Московкого зоопарка и даже взять под опеку обитателя!Подробнее по [ссылке]({main_url})❤️"

        db.set_user_finish(False, True)

        return {
            "text": text,
            "keyboard": None,
        }

    question = db.get_question(user["question_index"])
    if question is None:
        return

    keyboard = telebot.types.InlineKeyboardMarkup()
    for answer_index, answer in enumerate(question["answers"]):
        keyboard.row(telebot.types.InlineKeyboardButton(f"{chr(answer_index + 97)}) {answer}",
                                                        callback_data=f"?ans&{answer_index}"))

    text = f"Вопрос №{user['question_index'] + 1}\n\n{question['question']}"

    return {
        "text": text,
        "keyboard": keyboard
    }


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == 'Пройти викторину':
        user = db.get_user(message.chat.id)
        if user['is_passed']:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Заново", callback_data="?restart"))
            bot.send_message(message.from_user.id, "Вы уже прошли эту викторину. Второй раз пройти нельзя 😥",
                             reply_markup=markup)
            return
        if user['is_passing']:
            return
        db.set_user_start(True, 0)

        user = db.get_user(message.chat.id)

        post = get_question_message(user)
        if post is not None:
            bot.send_message(message.from_user.id, post["text"], reply_markup=post["keyboard"])

    elif message.text == 'Контакты':
        markup_link = types.InlineKeyboardMarkup()
        btn_link = types.InlineKeyboardButton(text='Наш сайт', url=main_url)
        markup_link.add(btn_link)
        bot.send_message(message.from_user.id, "По кнопке ниже можно перейти на сайт Московского зоопарка",
                         reply_markup=markup_link)
    elif message.text == 'Обратная связь':
        bot.send_message(message.from_user.id,
                         'Ваше мнение очень важно для нас <a href="https://avatars.dzeninfra.ru/get-zen_doc/9116192/pub_6431ae44006c795e056806ab_6431ae8c006c795e05689d81/scale_1200">&#8205;</a>',
                         parse_mode='HTML')

@bot.callback_query_handler(func=lambda query: query.data.startswith("?ans"))
def answered(query):
    user = db.get_user(query.message.chat.id)
    if user["is_passed"] or not user["is_passing"]:
        return

    user["answers"].append(int(query.data.split("&")[1]))
    db.set_user_ans(user["answers"])

    post = get_answered_message(user)
    if post is not None:
        bot.edit_message_text(post["text"], query.message.chat.id, query.message.id,
                              reply_markup=post["keyboard"])

def get_answered_message(user):
    question = db.get_question(user["question_index"])

    text = f"Вопрос №{user['question_index'] + 1}\n\n{question['question']}\n"

    for answer_index, answer in enumerate(question["answers"]):
        text += f"{chr(answer_index + 97)}) {answer}"

        if answer_index == user["answers"][-1]:
            text += " ✅"
        text += "\n"

    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(telebot.types.InlineKeyboardButton("Далее", callback_data="?next"))

    return {
        "text": text,
        "keyboard": keyboard
    }

@bot.callback_query_handler(func=lambda query: query.data == "?next")
def next(query):
    user = db.get_user(query.message.chat.id)
    if user["is_passed"] or not user["is_passing"]:
        return

    user["question_index"] += 1
    post = get_question_message(user)
    if post is not None:
        bot.edit_message_text(post["text"], query.message.chat.id, query.message.id, parse_mode='Markdown',
                              disable_web_page_preview=True,
                              reply_markup=post["keyboard"])

@bot.callback_query_handler(func=lambda query: query.data == "?restart")
def restart(query):
    db.delete_user()
    bot.edit_message_text("Резульат удален, попробуй заново😁", query.message.chat.id, query.message.id)

bot.polling(none_stop=True, interval=0)
