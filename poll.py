from data.data import *
import json
from telebot import types
from functions import *
from commands import *



#choose poll
@bot.callback_query_handler(func=lambda call: call.data == "choose_poll")
def choose_poll_callback(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    new_keyboard = types.InlineKeyboardMarkup()

    with open('data/data.json') as f:
        data = json.load(f)     
    for poll in range(len(data["polls"])):
        callback_data = generate_callback_data(poll)

        new_keyboard.add (types.InlineKeyboardButton(data["polls"][poll]["name"],callback_data=callback_data))
    new_keyboard.add(types.InlineKeyboardButton("Отмена", callback_data="cancel"))
    
    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="Выберите опрос", reply_markup=new_keyboard)

#button actions
@bot.callback_query_handler(func=lambda call: call.data.startswith("button_"))
def select_poll(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    button_number = int(call.data.split("_")[1])  # Витягуємо номер кнопки з callback_data
    buttons = ["Отправить опрос", "Редактировать имя опроса", "Редактировать содержание опроса", "Удалить опрос", "Отменить"]
    keyboard = create_vertical_inline_keyboard(buttons, button_number)
    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="Выберите действие", reply_markup=keyboard)


#poll actions
@bot.callback_query_handler(func=lambda call: call.data.startswith("action"))
def button_callback(call):
    action = int(call.data.split(":")[1])
    data = int(call.data.split(":")[2])
    chat_id = call.message.chat.id
    print(action,data)
    
    #send poll
    if action == 0:
        with open('data/data.json') as f:
            poll = json.load(f)["polls"][data]
        send_questionnaire(chat_id, poll["name"],poll["data"]) 
        toMenu(call)
    #edit poll name
    elif action == 1:
        chat_id = call.message.chat.id
        message_id = call.message.message_id
        # Змінюємо опції клавіатури після натискання кнопки "Выбрать опрос"
        new_keyboard = types.InlineKeyboardMarkup()
        option2 = types.InlineKeyboardButton("Отменить", callback_data="cancel")
        new_keyboard.add(option2)
        with open('data/data.json') as f:
            poll_name = json.load(f)["polls"][data]["name"]

        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"Введите новое имя для опроса {poll_name}", reply_markup=new_keyboard)
        bot.register_next_step_handler(call.message, edit_name, data)


    #edit poll data
    elif action == 2:
        chat_id = call.message.chat.id
        message_id = call.message.message_id
        # Змінюємо опції клавіатури після натискання кнопки "Выбрать опрос"
        new_keyboard = types.InlineKeyboardMarkup()
        option2 = types.InlineKeyboardButton("Отменить", callback_data="cancel")
        new_keyboard.add(option2)
        with open('data/data.json') as f:
            poll_name = json.load(f)["polls"][data]["name"]
        
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"Введите новые варианты ответов для опроса {poll_name} в формате \n Вариант 1\n Вариант 2 \n Вариант 3:", reply_markup=new_keyboard)        
        bot.register_next_step_handler(call.message, edit_data, data)


    #delete poll
    elif action == 3:

        chat_id = call.message.chat.id
        message_id = call.message.message_id
        # Змінюємо опції клавіатури після натискання кнопки "Выбрать опрос"
        new_keyboard = types.InlineKeyboardMarkup()
        option1 = types.InlineKeyboardButton("Удалить", callback_data=f"delete:{data}")
        option2 = types.InlineKeyboardButton("Отменить", callback_data="cancel")
        new_keyboard.add(option1, option2)
        with open('data/data.json') as f:
            poll_name = json.load(f)["polls"][data]["name"]

        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"Вы действительно хочете удалить опрос {poll_name}?", reply_markup=new_keyboard)
    #cancel
    elif action == 4:
        toMenu(call)


#edit name action
@bot.message_handler(func=lambda message: message.text and not message.text.startswith('/'))
def edit_name(message, id):
    chat_id = message.chat.id
    with open('data/data.json') as f:
        polls = json.load(f)

    polls["polls"][id]["name"] = message.text
    with open('data/data.json', 'w') as f:
        json.dump(polls, f)

    bot.send_message(chat_id, "Имя опроса было успешно изменено")
    settings(message)

#edit data action
@bot.message_handler(func=lambda message: message.text and not message.text.startswith('/'))
def edit_data(message, id):
    chat_id = message.chat.id
    with open('data/data.json') as f:
        polls = json.load(f)

    polls["polls"][id]["data"] = message.text.split("\n")
    with open('data/data.json', 'w') as f:
        json.dump(polls, f)

    bot.send_message(chat_id, "Варианты ответов были успешно изменены")
    settings(message)

#delete action
@bot.callback_query_handler(func=lambda call: call.data.startswith("delete"))
def del_poll(call):
    chat_id = call.message.chat.id

    data = int(call.data.split(":")[1])
    with open('data/data.json') as f:
        polls = json.load(f)
    polls["polls"].pop(data)
    with open('data/data.json', 'w') as f:
        json.dump(polls, f)
    bot.send_message(chat_id, "Опрос был успешно удалён")
    toMenu(call)


#adding poll
@bot.callback_query_handler(func=lambda call: call.data == "add_poll")
def add_poll_callback(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    # Змінюємо опції клавіатури після натискання кнопки "Выбрать опрос"
    new_keyboard = types.InlineKeyboardMarkup()
    option2 = types.InlineKeyboardButton("Отменить", callback_data="cancel")
    new_keyboard.add(option2)

    text = "Введите название названиие опроса"

    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=new_keyboard)
    bot.register_next_step_handler(call.message, saveName)


#saving name
@bot.message_handler(func=lambda message: message.text and not message.text.startswith('/'))
def saveName(message):
    chat_id = message.chat.id


    # Змінюємо опції клавіатури після натискання кнопки "Выбрать опрос"
    new_keyboard = types.InlineKeyboardMarkup()
    option1 = types.InlineKeyboardButton("Назад", callback_data="next")
    option2 = types.InlineKeyboardButton("Отмена", callback_data="cancel")
    new_keyboard.add(option1, option2)
    

    #update json
    with open('data/data.json') as f:
        data = json.load(f) 
    data["polls"].append({"name" : message.text})
    bot.send_message(chat_id, "Введите варианты ответов в формате \n Вариант 1\n Вариант 2 \n Вариант 3:", reply_markup=new_keyboard)        
    bot.register_next_step_handler(message, savePoll, data)

    bot.send_message(chat_id, "Название должно быть хотя бы 3 символа")
    

#saving poll
@bot.message_handler(func=lambda message: message.text and not message.text.startswith('/'))
def savePoll(message, data):
    chat_id = message.chat.id
    message_id = message.message_id

    data["polls"][len(data["polls"]) - 1]["data"] = (message.text.split("\n"))
    with open('data/data.json', 'w') as f:
        json.dump(data, f)
    bot.send_message(chat_id, "Вы успешно добавили опрос")  
    with open('data/data.json') as f:
        poll = json.load(f)["polls"][-1]       
    send_questionnaire(chat_id,poll["name"],poll["data"])
    settings(message)
