users = {}
questions = {
    0: {
        "question": "Твой любимый продукт?😋",
        "answers": ["Мясо🥩", "Все, что попадется под руку👹", "Рыба🐟", "Растительная пища🌱"],
    },
    1: {
        "question": "Какая черта тебе ближе?🎭",
        "answers": ["Быстрота⚡️", "Сила💪", "Ум💡", "Неторопливость😴"],
    },
    2: {
        "question": "Что ты чувствуешь к зиме?❄️",
        "answers": ["Ненавижу ее🤬", "Люблю ее🥰", "Зависит от обстоятельств😇", "Ничего🤷"],
    },
    3: {
        "question": "Какой вид досуга тебе ближе?🌆",
        "answers": ["Экстремальные виды спорта🪂", "Неспешные прогулки🌱", "Общение с друзьями😝🤟",
                    "Чтение книг или медитация🧘"],
    },
    4: {
        "question": "Как ты относишься к новым знакомствам?🤝",
        "answers": ["Осторожно, но открыто🤫", "Не люблю такое🤮", "С интересом и радостью🤩",
                    "Спокойно и без фанатизма🥴"],
    },
    5: {
        "question": "Как ты реагируешь на стрессовые ситуации?😰",
        "answers": ["Быстро принимаю решения😼", "Ищу поддержку у друзей и близких🫂", "Импровизирую🤠",
                    "Плыву по течению🫠"],
    },
    6: {
        "question": "Какая ценность наиболее важна для тебя?⚖️",
        "answers": ["Власть👑", "Семья👨‍👩‍👦", "Свобода🍟",
                    "Умиротворение☯️"],
    },
    7: {
        "question": "Какой цвет ты предпочитаешь?🤡️",
        "answers": ["Красный🧨", "Оранжевый🏀", "Желтый🧽",
                    "Синий🧿"],
    },
}


class DataBase:
    def __init__(self):
        self.users = users
        self.questions = questions

        self.questions_count = len(self.questions)

    def get_user(self, chat_id):
        user = self.users
        if user:
            return user
        user = {
            "chat_id": chat_id,
            "is_passing": False,
            "is_passed": False,
            "question_index": None,
            "answers": []
        }
        users.update(user)

        return user

    def set_user_start(self, is_passing, question_index):
        self.users["question_index"] = question_index
        self.users["is_passing"] = is_passing

    def set_user_finish(self, is_passing, is_passed):
        self.users["is_passed"] = is_passed
        self.users["is_passing"] = is_passing

    def set_user_ans(self, answers):
        self.users["answers"] = answers

    def set_user_quest(self):
        self.users["question_index"] += 1

    def get_question(self, index):
        return self.questions[index]

    def delete_user(self):
        self.users.clear()
