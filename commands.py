from data.data import bot
from functions import create_inline_keyboard
#start command
@bot.message_handler(commands=["start"])
def initBot(message):
    print("[LOG] /start")
    group_chat_id = message.chat.id
    print(group_chat_id)



#setting command
@bot.message_handler(commands=["settings"])
def settings(message):
    welcome_message = "Меню управление ботом"
    keyboard = create_inline_keyboard()
    bot.send_message(message.chat.id, welcome_message, reply_markup=keyboard)


