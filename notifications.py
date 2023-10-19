import json
from data import *
from commands import *
from functions import *
from telebot import types

#adding notification
@bot.callback_query_handler(func=lambda call: call.data == "add_not")
def add_not(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    new_keyboard = types.InlineKeyboardMarkup()
    option2 = types.InlineKeyboardButton("Отменить", callback_data="cancel")
    new_keyboard.add(option2)

    text = "Введите объявление"

    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=new_keyboard)
    bot.register_next_step_handler(call.message, save_not)


#saving the notification
@bot.message_handler(func=lambda message: message.text and not message.text.startswith('/'))
def save_not(message):
    chat_id = message.chat.id
    with open('data/data.json') as f:
        data = json.load(f)

    data["nots"].append(message.text)
    with open('data/data.json', 'w') as f:
        json.dump(data, f)
    bot.send_message(chat_id, "Вы успешно добавили объявление") 
    settings(message) 



#choose notification
@bot.callback_query_handler(func=lambda call: call.data == "choose_not")
def choose_poll_callback(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    new_keyboard = types.InlineKeyboardMarkup()

    with open('data/data.json') as f:
        data = json.load(f)     
    for notif in range(len(data["nots"])):
        callback_data = generate_callback_notif_button(notif)

        new_keyboard.add (types.InlineKeyboardButton(data["nots"][notif],callback_data=callback_data))
    new_keyboard.add( types.InlineKeyboardButton("Отмена", callback_data="cancel"))
    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="Выберите объявление", reply_markup=new_keyboard)


def create_nots_action(button_labels, data):
    keyboard = types.InlineKeyboardMarkup()
    for label in range(len(button_labels)):
        button = types.InlineKeyboardButton(button_labels[label], callback_data = generate_callback_notif(label,data))
        keyboard.add(button)
    return keyboard

#button actions
@bot.callback_query_handler(func=lambda call: call.data.startswith("notif_"))
def select_poll(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    button_number = int(call.data.split("_")[1])  # Витягуємо номер кнопки з callback_data
    buttons = ["Отправить объявление", "Редактировать объявление", "Удалить объявление", "Отменить"]
    keyboard = create_nots_action(buttons, button_number)
    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="Выберите действие", reply_markup=keyboard)


#notification actions
@bot.callback_query_handler(func=lambda call: call.data.startswith("notif"))
def button_callback(call):
    action = int(call.data.split(":")[1])
    data = int(call.data.split(":")[2])
    chat_id = call.message.chat.id
    print(action,data)
    
    #send notification
    if action == 0:
        with open('data/data.json') as f:
            notif = json.load(f)["nots"][data]
        bot.send_message(chat_id, notif)
        toMenu(call)
    #edit notification
    elif action == 1:
        chat_id = call.message.chat.id
        message_id = call.message.message_id
        new_keyboard = types.InlineKeyboardMarkup()
        option2 = types.InlineKeyboardButton("Отменить", callback_data="cancel")
        new_keyboard.add(option2)
        with open('data/data.json') as f:
            notif = json.load(f)["nots"][data]

        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"Введите объявление на замену:\n{notif}", reply_markup=new_keyboard)
        bot.register_next_step_handler(call.message, edit_notif, data)


    #delete poll
    elif action == 2:

        chat_id = call.message.chat.id
        message_id = call.message.message_id
        new_keyboard = types.InlineKeyboardMarkup()
        option1 = types.InlineKeyboardButton("Удалить", callback_data=f"ndel:{data}")
        option2 = types.InlineKeyboardButton("Отменить", callback_data="cancel")
        new_keyboard.add(option1, option2)
        with open('data/data.json') as f:
            notif = json.load(f)["nots"][data]

        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"Вы действительно хочете удалить объявление {notif}?", reply_markup=new_keyboard)
    #cancel
    elif action == 3:
        toMenu(call)


#edit name action
@bot.message_handler(func=lambda message: message.text and not message.text.startswith('/'))
def edit_notif(message, id):
    chat_id = message.chat.id
    with open('data/data.json') as f:
        nots = json.load(f)

    nots["nots"][id] = message.text
    with open('data/data.json', 'w') as f:
        json.dump(nots, f)

    bot.send_message(chat_id, "Объявление было успешно изменено")
    settings(message)

#delete action
@bot.callback_query_handler(func=lambda call: call.data.startswith("ndel"))
def del_poll(call):
    chat_id = call.message.chat.id

    data = int(call.data.split(":")[1])
    with open('data/data.json') as f:
        nots = json.load(f)
    nots["nots"].pop(data)
    with open('data/data.json', 'w') as f:
        json.dump(nots, f)
    bot.send_message(chat_id, "Объявление было успешно удалён")
    toMenu(call)