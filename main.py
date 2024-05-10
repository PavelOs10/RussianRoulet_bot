import random
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

WEAPON_CHOICE = 1
FIRE = 2

def start(update, context):
    context.user_data['name'] = update.message.from_user.first_name
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Привет, {context.user_data['name']}! Добро пожаловать в русскую рулетку!")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Выберите оружие:\n1. Colt Python (6 камор)\n2. Smith & Wesson Model 29 (5 камор)\n3. Taurus Judge (3 каморы)\n4. Пистолет Макарова (магазин)")
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
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Вы выбрали {weapon_name}")
        context.bot.send_message(chat_id=update.effective_chat.id, text="Игра начинается...")
        return FIRE
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Неверный выбор. Пожалуйста, введите число от 1 до 4.")
        return WEAPON_CHOICE

def play_game(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Нажмите F для выстрела...")

def handle_fire(update, context):
    if update.message.text.upper() == "F":
        chambers = context.user_data['chambers']
        name = context.user_data['name']
        empty_chambers = len(chambers) - 1

        current_chamber = chambers.pop(0)  # удаляем и возвращаем первый элемент списка

        if current_chamber == 1:
            update.message.reply_text("БАХ!")
            update.message.reply_text(f"Вы проиграли, {name}!")
            return start(update, context)
        else:
            empty_chambers -= 1
            update.message.reply_text(f"Фух, вы выжили, {name}!")
            if empty_chambers == 0:
                update.message.reply_text(f"В стволе остался один боевой патрон! Вы выиграли, {name}!")
                return start(update, context)
    else:
        update.message.reply_text("Неверный выбор. Нажмите F для выстрела...")

def main():
    updater = Updater(token='7004037923:AAEqUxhHSpvOEiw6Yv8GRjyuM87lnQz1iVI', use_context=True)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            WEAPON_CHOICE: [MessageHandler(Filters.text & ~Filters.command, handle_choice)],
            FIRE: [MessageHandler(Filters.text & ~Filters.command, handle_fire)]
        },
        fallbacks=[],
    )
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
