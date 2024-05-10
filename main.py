import random  # Импорт модуля random для генерации случайных чисел
import time  # Импорт модуля time для работы с задержками
from telegram import InlineKeyboardMarkup, InlineKeyboardButton  # Импорт классов InlineKeyboardMarkup и InlineKeyboardButton из модуля telegram
from telegram.ext import Updater, CommandHandler, ConversationHandler, CallbackQueryHandler, MessageHandler, Filters  # Импорт необходимых классов из модуля telegram.ext

WEAPON_CHOICE = 1  # Константа, обозначающая начало выбора оружия
FIRE = 2  # Константа, обозначающая состояние выстрела

# Функция, инициирующая начало игры и предлагающая пользователю выбрать оружие
def start(update, context):
    context.user_data['name'] = update.message.from_user.first_name  # Получаем имя пользователя из объекта сообщения
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Привет, {context.user_data['name']}! Сыграем в русскую рулетку?")  # Отправляем приветственное сообщение с именем пользователя
    time.sleep(1)  # Задержка 1 секунда перед отправкой следующего сообщения
    context.bot.send_message(chat_id=update.effective_chat.id, text="Выбери оружие:\n1. Colt Python (6 камор)\n2. Smith & Wesson Model 29 (5 камор)\n3. Taurus Judge (3 каморы)\n4. Пистолет Макарова (магазин)")  # Отправляем сообщение с предложением выбрать оружие
    return WEAPON_CHOICE  # Переходим к следующему состоянию выбора оружия

# Функция, обрабатывающая выбор оружия от пользователя
def handle_choice(update, context):
    choice = update.message.text  # Получаем текст сообщения от пользователя
    if choice in ["1", "2", "3"]:  # Если выбрано оружие с каморами
        weapon_name = {  # Словарь с названиями оружия
            "1": "Colt Python",
            "2": "Smith & Wesson Model 29",
            "3": "Taurus Judge"
        }[choice]  # Выбираем название оружия по номеру
        context.user_data['weapon_name'] = weapon_name  # Записываем название оружия в данные пользователя
        chambers = {  # Словарь с каморами для каждого вида оружия
            "1": [0, 0, 0, 0, 0, 1],  # Colt Python
            "2": [0, 0, 0, 0, 1],  # Smith & Wesson Model 29
            "3": [0, 0, 1]  # Taurus Judge
        }[choice]  # Выбираем каморы для данного вида оружия
        random.shuffle(chambers)  # Перемешиваем барабан
        context.user_data['chambers'] = chambers  # Записываем каморы в данные пользователя
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ты выбрал {weapon_name}")  # Отправляем сообщение с выбранным оружием
        context.bot.send_message(chat_id=update.effective_chat.id, text="Игра начинается...")  # Отправляем сообщение о начале игры
        time.sleep(1)  # Задержка 1 секунда перед отправкой следующего сообщения
        context.bot.send_message(chat_id=update.effective_chat.id, text="Нажми ОГОНЬ для выстрела...", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ОГОНЬ", callback_data="fire")]]))  # Отправляем сообщение с кнопкой для выстрела
        return FIRE  # Переходим к состоянию выстрела
    elif choice == "4":  # Если выбран Пистолет Макарова
        context.user_data['weapon_name'] = "Пистолет Макарова"  # Записываем название оружия в данные пользователя
        chambers = [1]  # В пистолете Макарова один боевой патрон
        context.user_data['chambers'] = chambers  # Записываем каморы в данные пользователя
        context.bot.send_message(chat_id=update.effective_chat.id, text="Ты выбрал Пистолет Макарова")  # Отправляем сообщение о выборе оружия
        context.bot.send_message(chat_id=update.effective_chat.id, text="Игра начинается...")  # Отправляем сообщение о начале игры
        time.sleep(1)  # Задержка 1 секунда перед отправкой следующего сообщения
        context.bot.send_message(chat_id=update.effective_chat.id, text="Нажми ОГОНЬ для выстрела...", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ОГОНЬ", callback_data="fire")]]))  # Отправляем сообщение с кнопкой для выстрела
        return FIRE  # Переходим к состоянию выстрела
    else:  # Если выбор оружия некорректен
        context.bot.send_message(chat_id=update.effective_chat.id, text="Неверный выбор. Выбери число от 1 до 4.")  # Отправляем сообщение о некорректном выборе
        return WEAPON_CHOICE  # Остаемся в состоянии выбора оружия

# Функция, обрабатывающая текстовые сообщения о выстреле
def handle_fire_text(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Нажми ОГОНЬ для выстрела...", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ОГОНЬ", callback_data="fire")]]))  # Отправляем сообщение с кнопкой для выстрела
    return FIRE  # Переходим к состоянию выстрела

# Функция, инициирующая начало игры заново
def start_over(update, context):
    user = update.effective_user  # Получаем объект пользователя
    chat_id = update.effective_chat.id  # Получаем идентификатор чата
    if user:  # Если объект пользователя доступен
        context.user_data['name'] = user.first_name  # Получаем имя пользователя
    else:  # Если объект пользователя недоступен
        context.user_data['name'] = "Unknown"  # Устанавливаем имя "Unknown"
    context.bot.send_message(chat_id=chat_id, text=f"Привет, {context.user_data['name']}! Сыграем в русскую рулетку?")  # Отправляем приветственное сообщение с именем пользователя
    time.sleep(1)  # Задержка 1 секунда перед отправкой следующего сообщения
    context.bot.send_message(chat_id=chat_id, text="Выбери оружие:\n1. Colt Python (6 камор)\n2. Smith & Wesson Model 29 (5 камор)\n3. Taurus Judge (3 каморы)\n4. Пистолет Макарова (магазин)")  # Отправляем сообщение с предложением выбрать оружие
    return WEAPON_CHOICE  # Переходим к состоянию выбора оружия

# Функция, обрабатывающая выстрел от пользователя
def handle_fire(update, context):
    if update.callback_query:  # Если запрос пришел от callback
        if update.callback_query.data == "fire":  # Если пользователь нажал на кнопку выстрела
            time.sleep(2)  # Задержка 2 секунды
            chambers = context.user_data['chambers']  # Получаем каморы из данных пользователя
            name = context.user_data['name']  # Получаем имя пользователя из данных пользователя
            weapon_name = context.user_data['weapon_name']  # Получаем название оружия из данных пользователя
            empty_chambers = len(chambers) - 1  # Вычисляем количество пустых камор

            current_chamber = chambers.pop(0)  # Удаляем и возвращаем первый элемент списка камор

            if current_chamber == 1:  # Если в каморе был боевой патрон
                context.bot.send_message(chat_id=update.effective_chat.id, text="БАХ!")  # Отправляем сообщение с звуком выстрела
                if weapon_name == "Пистолет Макарова":  # Если выбран Пистолет Макарова
                    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ты проиграл, {name}! Ты реально хотел играть в русскую рулетку пистолетом Макарова?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Начать заново?", callback_data="start_over")]]))  # Отправляем сообщение о поражении
                else:  # Если выбрано другое оружие
                    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ты проиграл, {name}!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Начать заново?", callback_data="start_over")]]))  # Отправляем сообщение о поражении
            else:  # Если в каморе был пустой патрон
                empty_chambers -= 1  # Уменьшаем количество пустых камор
                context.bot.send_message(chat_id=update.effective_chat.id, text=f"Фух, ты выжил, {name}!")  # Отправляем сообщение о выживании
                if empty_chambers == 0:  # Если остался только один боевой патрон
                    context.bot.send_message(chat_id=update.effective_chat.id, text=f"В стволе остался один боевой патрон! Ты выиграл, {name}!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Начать заново?", callback_data="start_over")]]))  # Отправляем сообщение о победе
                else:  # Если остались еще каморы
                    context.bot.send_message(chat_id=update.effective_chat.id, text="Нажми ОГОНЬ для выстрела...", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ОГОНЬ", callback_data="fire")]]))  # Отправляем сообщение с кнопкой для следующего выстрела
                    return FIRE  # Остаемся в состоянии выстрела
        elif update.callback_query.data == "start_over":  # Если пользователь хочет начать заново
            return start_over(update, context)  # Вызываем функцию начала игры заново
    else:  # Если запрос не callback
        context.bot.send_message(chat_id=update.effective_chat.id, text="Неверный выбор. Нажми ОГОНЬ для выстрела...", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ОГОНЬ", callback_data="fire")]]))  # Отправляем сообщение о некорректном выборе
        return FIRE  # Остаемся в состоянии выстрела
    
# Основная функция, запускающая бота и обработчики сообщений
def main():
    updater = Updater(token='TOKEN', use_context=True)  # Создаем объект Updater с указанием токена
    dp = updater.dispatcher  # Получаем диспетчер для регистрации обработчиков
    conv_handler = ConversationHandler(  # Создаем объект ConversationHandler для управления состояниями беседы
        entry_points=[CommandHandler('start', start)],  # Начальное состояние - вызов команды /start
        states={  # Словарь состояний и соответствующих им обработчиков
            WEAPON_CHOICE: [MessageHandler(Filters.text & ~Filters.command, handle_choice)],  # Состояние выбора оружия
            FIRE: [  # Состояние выстрела
                CallbackQueryHandler(handle_fire),  # Обработчик callback для выстрела
                MessageHandler(Filters.text & ~Filters.command, handle_fire_text)  # Обработчик текстовых сообщений для выстрела
            ]
        },
        fallbacks=[],  # Пустой список возвратов
    )
    dp.add_handler(conv_handler)  # Регистрируем объект ConversationHandler в диспетчере
    updater.start_polling()  # Запускаем бота
    updater.idle()  # Бот работает до принудительной остановки

if __name__ == '__main__':
    main()  # Вызываем основную функцию при запуске скрипта
