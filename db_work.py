import sqlite3
import datetime


# Функция для создания базы данных и таблиц


def createDb():
    try:
        connection = sqlite3.connect("telegarm_chat_bot.db")
        cursor = connection.cursor()
        create_table_query = ''' CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            telegram_id TEXT NOT NULL UNIQUE,
            join_date datetime,
            free INTEGER DEFAULT 1
        );
       
        '''
        cursor.execute(create_table_query)
        create_table_dialog = '''
         CREATE TABLE IF NOT EXISTS now_dialog (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_user TEXT NOT NULL,
            second_user TEXT NOT NULL,
            start_date datetime
        )'''
        cursor.execute(create_table_dialog)
        sqlite3_connection.commit()
        cursor.close()
        connection.close()
        return True

    except Exception as ex:
        return ex

# добавление юзера в бд


def addUser(username, telegram_id):
    try:
        connection = sqlite3.connect("telegarm_chat_bot.db")
        cursor = connection.cursor()
        insert_sql = '''
        insert into users (username, telegram_id, join_date) values (?,?,?)
        '''
        cursor.execute(
            insert_sql, (username, telegram_id, datetime.datetime.now()))
        connection.commit()
        cursor.close()
        connection.close()
        return True

    except Exception as ex:
        return ex

# Получение рагдомного юзера


def selectRandomUser():
    try:
        connection = sqlite3.connect('telegarm_chat_bot.db')
        cursor = connection.cursor()
        sql_select = '''SELECT * FROM users WHERE free = 1 ORDER BY RANDOM() LIMIT 1'''
        cursor.execute(sql_select)
        random = cursor.fetchall()
        cursor.close()
        connection.close()
        return random
    except Exception as ex:
        return ex

# Создание диалога


def createDialog(first_user, second_user):
    if int(first_user) != int(second_user):
        try:
            connection = sqlite3.connect('telegarm_chat_bot.db')
            cursor = connection.cursor()
            create_dialog = '''
            Insert into now_dialog (first_user, second_user, start_date) VALUES (?,?,?)
            '''
            cursor.execute(create_dialog, (first_user,
                                           second_user, datetime.datetime.now()))
            first_user_not_be_free = f"Update users SET free = 0 where telegram_id = {first_user}"
            second_user_not_be_free = f"Update users SET free = 0 where telegram_id = {second_user}"
            cursor.execute(first_user_not_be_free)
            cursor.execute(second_user_not_be_free)
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Exception as ex:
            return ex
    else:
        return False

# Удаление диалога


def deleteDialog(first_user, second_user):
    try:
        connection = sqlite3.connect('telegarm_chat_bot.db')
        cursor = connection.cursor()
        delete_sql = f"delete from now_dialog where (first_user = {first_user} AND second_user={second_user}) OR ( first_user = {second_user} AND second_user={first_user})"
        cursor.execute(delete_sql)
        first_user_not_be_free = f"Update users SET free = 1 where telegram_id = {first_user}"
        second_user_not_be_free = f"Update users SET free = 1 where telegram_id = {second_user}"
        cursor.execute(first_user_not_be_free)
        cursor.execute(second_user_not_be_free)
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as ex:
        return ex

# получение пользователя по id


def getUser(user_id):
    try:
        connection = sqlite3.connect('telegarm_chat_bot.db')
        cursor = connection.cursor()
        get_sql = f"select * from users where telegram_id = {user_id}"
        cursor.execute(get_sql)
        user = cursor.fetchall()
        connection.commit()
        cursor.close()
        connection.close()
        return user
    except Exception as ex:
        return ex

# получение не занятого пользователя


def getFreeUser():
    try:
        connection = sqlite3.connect('telegarm_chat_bot.db')
        cursor = connection.cursor()
        get_urls = "SELECT * FROM users WHERE free = 1"
        cursor.execute(get_urls)
        users = cursor.fetchall()
        connection.commit()
        cursor.close()
        connection.close()
        return users
    except Exception as ex:
        return ex
# получение текущего диалога


def currentDialog(user_id):
    try:
        connection = sqlite3.connect('telegarm_chat_bot.db')
        cursor = connection.cursor()
        get_dialog = f"select * from now_dialog where (first_user = {user_id}) OR (second_user = {user_id})"
        cursor.execute(get_dialog)
        dialog = cursor.fetchall()
        connection.commit()
        cursor.close()
        connection.close()
        return dialog
    except Exception as ex:
        return ex

# Перестать искать


def stopSearch(user_id):
    try:
        connection = sqlite3.connect('telegarm_chat_bot.db')
        cursor = connection.cursor()
        stop_sql = f"Update users SET free = 0 where telegram_id = {user_id}"
        cursor.execute(stop_sql)
        cursor.close()
        connection.commit()
        connection.close()
        return True
    except Exception as ex:
        return ex

# Начать поиск


def startSerch(user_id):
    try:
        connection = sqlite3.connect('telegarm_chat_bot.db')
        cursor = connection.cursor()
        start_sql = f"Update users set free = 1 where telegram_id = {user_id}"
        cursor.execute(start_sql)
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as ex:
        return ex


def main():

    pass


if __name__ == "__main__":
    main()
