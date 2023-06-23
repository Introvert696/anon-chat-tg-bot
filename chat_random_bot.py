import telebot
import db_work

BOT_TOKEN = "YOUTOKENHERE"

bot = telebot.TeleBot(BOT_TOKEN)

db_work.createDb()

# первый запуск бота


@bot.message_handler(commands=["start"])
def start_message(message):
    bot.reply_to(
        message, "Добро пожаловать на рандом чат бота, здесь ты можешь найти рандомных людей для болтовни")
    if not db_work.getUser(message.from_user.id):
        db_work.addUser(message.from_user.username, message.from_user.id)
        print(f"Пользователь {message.from_user.id} добавлен в базу")
    else:
        print("Пользователь есть в базе данных")

# поиск следующего пользователя


@bot.message_handler(commands=['next'])
def next_message(message):
    # Получаем текущий диалог
    currentDialog = db_work.currentDialog(message.from_user.id)
    # проверка на существование диалога
    if not currentDialog:
        pass

    else:
        # Если есть активный диалог, то удаляем его
        result = db_work.deleteDialog(currentDialog[0][1], currentDialog[0][2])

    free_user = db_work.selectRandomUser()
    # если есть свободный юзер
    if not free_user:
        bot.send_message(message.from_user.id,
                         "Все пользователи заняты, попробуйте попозже")
    else:
        # если этот пользователь не тот же самый
        if db_work.createDialog(message.from_user.id, free_user[0][2]):
            bot.send_message(message.from_user.id,
                             "Найден пользователь! Общайтесь")
            bot.send_message(
                free_user[0][2], "Вас выбрали в качестве собеседника")

        else:
            bot.send_message(message.from_user.id,
                             "Все пользователи заняты, попробуйте попозже")


@bot.message_handler(commands=["stop"])
def stop_func(message):
    # Получаем текущий диалог
    currentDialog = db_work.currentDialog(message.from_user.id)

    # проверка на существование диалога
    if not currentDialog:
        pass

    else:
        # Если есть активный диалог, то удаляем его
        # говорим собеседнику что юзер остановил чат

        if int(currentDialog[0][1]) != int(message.from_user.id):
            bot.send_message(currentDialog[0][1],
                             "Собеседник остановил диалог =(")
        elif int(currentDialog[0][2] != int(message.from_user.id)):
            bot.send_message(currentDialog[0][2],
                             "Собеседник остановил диалог =(")

        result = db_work.deleteDialog(currentDialog[0][1], currentDialog[0][2])
    db_work.stopSearch(message.from_user.id)
    bot.send_message(message.from_user.id,
                     "Поиск пользователей остановлен. Чтобы возообновить поиск напишите /resume")


@bot.message_handler(commands=["resume"])
def resume_func(message):
    db_work.startSerch(message.from_user.id)
    bot.send_message(message.from_user.id,
                     "Поиск пользователей возообновлен, что бы найти пользователя, введите /next")
# обработка всего текста


@bot.message_handler(func=lambda _: True)
def handle_message(message):
    currentDialog = db_work.currentDialog(message.from_user.id)
    if not currentDialog:
        bot.send_message(
            message.from_user.id, "Вы не в диалоге, для того, что бы найти новго собеседника введите /next")
    else:
        if message.from_user.id == int(currentDialog[0][1]):
            bot.send_message(currentDialog[0][2], message.text)
        elif message.from_user.id == int(currentDialog[0][2]):
            bot.send_message(currentDialog[0][1], message.text)


bot.polling()
