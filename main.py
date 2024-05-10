import random
import time
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, ConversationHandler, CallbackQueryHandler, MessageHandler, Filters

WEAPON_CHOICE = 1
FIRE = 2

def start(update, context):
    context.user_data['name'] = update.message.from_user.first_name
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Привет, {context.user_data['name']}! Сыграем в русскую рулетку?")
    time.sleep(1)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Выбери оружие:\n1. Colt Python (6 камор)\n2. Smith & Wesson Model 29 (5 камор)\n3. Taurus Judge (3 каморы)\n4. Пистолет Макарова (магазин)")
    return WEAPON_CHOICE

def handle_choice(update, context):
    choice = update.message.text
    if choice in ["1", "2", "3"]:
        weapon_name = {
            "1": "Colt Python",
            "2": "Smith & Wesson Model 29",
            "3": "Taurus Judge"
        }[choice]
        context.user_data['weapon_name'] = weapon_name
        chambers = {
            "1": [0, 0, 0, 0, 0, 1],
            "2": [0, 0, 0, 0, 1],
            "3": [0, 0, 1]
        }[choice]
        random.shuffle(chambers)  # перемешиваем барабан
        context.user_data['chambers'] = chambers
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ты выбрал {weapon_name}")
        context.bot.send_message(chat_id=update.effective_chat.id, text="Игра начинается...")
        time.sleep(1)  
        context.bot.send_message(chat_id=update.effective_chat.id, text="Нажми ОГОНЬ для выстрела...", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ОГОНЬ", callback_data="fire")]]))
        return FIRE
    elif choice == "4":
        context.user_data['weapon_name'] = "Пистолет Макарова"
        chambers = [1]  # в пистолете Макарова один боевой патрон
        context.user_data['chambers'] = chambers
        context.bot.send_message(chat_id=update.effective_chat.id, text="Ты выбрал Пистолет Макарова")
        context.bot.send_message(chat_id=update.effective_chat.id, text="Игра начинается...")
        time.sleep(1) 
        context.bot.send_message(chat_id=update.effective_chat.id, text="Нажми ОГОНЬ для выстрела...", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ОГОНЬ", callback_data="fire")]]))
        return FIRE
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Неверный выбор. Выбери число от 1 до 4.")
        return WEAPON_CHOICE

def handle_fire_text(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Нажми ОГОНЬ для выстрела...", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ОГОНЬ", callback_data="fire")]]))
    return FIRE


def start_over(update, context):
    user = update.effective_user  # Получаем объект пользователя
    chat_id = update.effective_chat.id  # Получаем идентификатор чата
    if user:
        context.user_data['name'] = user.first_name  # Получаем имя пользователя
    else:
        context.user_data['name'] = "Unknown"  # Если имя пользователя недоступно, устанавливаем "Unknown"
    context.bot.send_message(chat_id=chat_id, text=f"Привет, {context.user_data['name']}! Сыграем в русскую рулетку?")
    time.sleep(1)
    context.bot.send_message(chat_id=chat_id, text="Выбери оружие:\n1. Colt Python (6 камор)\n2. Smith & Wesson Model 29 (5 камор)\n3. Taurus Judge (3 каморы)\n4. Пистолет Макарова (магазин)")
    return WEAPON_CHOICE

def handle_fire(update, context):
    if update.callback_query:
        if update.callback_query.data == "fire":
            time.sleep(2)  # задержка 2 секунды
            chambers = context.user_data['chambers']
            name = context.user_data['name']
            weapon_name = context.user_data['weapon_name']
            empty_chambers = len(chambers) - 1

            current_chamber = chambers.pop(0)  # удаляем и возвращаем первый элемент списка

            if current_chamber == 1:
                context.bot.send_message(chat_id=update.effective_chat.id, text="БАХ!")
                if weapon_name == "Пистолет Макарова":
                    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ты проиграл, {name}! Ты реально хотел играть в русскую рулетку пистолетом Макарова?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Начать заново?", callback_data="start_over")]]))
                else:
                    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ты проиграл, {name}!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Начать заново?", callback_data="start_over")]]))
            else:
                empty_chambers -= 1
                context.bot.send_message(chat_id=update.effective_chat.id, text=f"Фух, ты выжил, {name}!")
                if empty_chambers == 0:
                    context.bot.send_message(chat_id=update.effective_chat.id, text=f"В стволе остался один боевой патрон! Ты выиграл, {name}!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Начать заново?", callback_data="start_over")]]))
                else:
                    context.bot.send_message(chat_id=update.effective_chat.id, text="Нажми ОГОНЬ для выстрела...", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ОГОНЬ", callback_data="fire")]]))  # Сообщение для следующего выстрела
                    return FIRE
        elif update.callback_query.data == "start_over":
            return start_over(update, context)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Неверный выбор. Нажми ОГОНЬ для выстрела...", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ОГОНЬ", callback_data="fire")]]))
        return FIRE
    
def main():
    updater = Updater(token='7004037923:AAEqUxhHSpvOEiw6Yv8GRjyuM87lnQz1iVI', use_context=True)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            WEAPON_CHOICE: [MessageHandler(Filters.text & ~Filters.command, handle_choice)],
            FIRE: [
                CallbackQueryHandler(handle_fire),
                MessageHandler(Filters.text & ~Filters.command, handle_fire_text)
            ]
        },
        fallbacks=[],
    )
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()