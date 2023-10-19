from data.data import *
import telebot
from telebot import types

# create menu buttons
def create_inline_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    options = [types.InlineKeyboardButton("Выбрать опрос", callback_data="choose_poll"), 
               types.InlineKeyboardButton("Добавить новый опрос", callback_data="add_poll"),
               types.InlineKeyboardButton("Выбрать объявление", callback_data="choose_not"),
                types.InlineKeyboardButton("Добавить объявление", callback_data="add_not")]


    for option in options:
        keyboard.add(option)
    return keyboard

#generating of the name of action-buttons
def gen_action(label, data):
    return f"action:{label}:{data}"


def create_vertical_inline_keyboard(button_labels, data):
    keyboard = types.InlineKeyboardMarkup()
    for label in range(len(button_labels)):
        button = types.InlineKeyboardButton(button_labels[label], callback_data = gen_action(label,data))
        keyboard.add(button)
    return keyboard


#editing a message to go to menu
def toMenu (call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    print(call.message.id)
    text = "Меню управление ботом"

    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=create_inline_keyboard())


#save action
def toSave(call, text_):
    
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    # Змінюємо опції клавіатури після натискання кнопки "Выбрать опрос"
    new_keyboard = types.InlineKeyboardMarkup()
    option1 = types.InlineKeyboardButton("Сохранить", callback_data="save")
    option2 = types.InlineKeyboardButton("Отменить", callback_data="cancel")
    new_keyboard.add(option1, option2)


    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text_, reply_markup=new_keyboard)

#generation of the callback name
def generate_callback_data(button_number):
    return f"button_{button_number}"

def generate_callback_notif(label,data):
    return f"notif:{label}:{data}"

def generate_callback_notif_button(data):
    return f"notif_{data}"


def send_questionnaire(chat_id, name, poll):
    print("[LOG] Sending a questionnaire")
    bot.send_poll(chat_id,name,poll, is_anonymous=False)
    print("[LOG ]the questionnaire was suc")
    
    
#calcel action
@bot.callback_query_handler(func=lambda call: call.data == "cancel" or call.data == "Отменить")
def cancel_callback(call):
    toMenu(call)
