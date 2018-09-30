from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import telebot
import time
import datetime
from telebot import types
bot_token = "646643183:AAF-nkj3t46rtZXNJbWZAnE0jrKzeIlpnqM"
bot = telebot.TeleBot(token=bot_token)
phone_numbers = {}
data = {}
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('sheets', 'v4', http=creds.authorize(Http()))

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    itembtn1 = types.KeyboardButton(text="Register", request_contact=True)
    markup.add(itembtn1)
    msg = bot.reply_to(message,text="Would you mind sharing your contact with me?",reply_markup=markup)
    bot.register_next_step_handler(msg, getContact)
def getContact(message):
    phone_numbers[message.chat.id] = message.contact.phone_number
    data[message.contact.phone_number] = []
    mainMenu(message)
def mainMenu(message):
    k = types.ReplyKeyboardRemove(selective=False)
    bot.reply_to(message, "Now let's start to work hard!", reply_markup=k)
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    itembtn1 = types.KeyboardButton(text="Fill out Form")
    itembtn2 = types.KeyboardButton(text="See Report")
    itembtn3 = types.KeyboardButton(text="Configure")
    markup.add(itembtn1,itembtn2,itembtn3)
    msg = bot.reply_to(message,text="Please choose one of the options below: ",reply_markup=markup)
    bot.register_next_step_handler(msg, chooseMenu)
    
def chooseMenu(message):
    if(message.text=="Fill out Form"):
        k = types.ReplyKeyboardRemove(selective=False)
        addRes(message,k)    
def addRes(message,k):
    res = bot.reply_to(message, "Please enter number of research paperes you finished today: ",reply_markup=k)
    bot.register_next_step_handler(message, addBook)
def addBook(message):
    book = bot.reply_to(message, "Please enter number of book pages you finished today: ")
    data[phone_numbers[message.chat.id]].append(message.text)
    bot.register_next_step_handler(message, addTh)
def addTh(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    itembtn1 = types.KeyboardButton(text="Yes")
    itembtn2 = types.KeyboardButton(text="No")
    markup.add(itembtn1,itembtn2)
    th = bot.reply_to(message, "Did you meet your proff today?", reply_markup=markup)
    data[phone_numbers[message.chat.id]].append(message.text)
    bot.register_next_step_handler(message, addOr)
def addOr(message):
    k = types.ReplyKeyboardRemove(selective=False)
    bot.reply_to(message, "Cool, let's continue!", reply_markup=k)
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    itembtn1 = types.KeyboardButton(text="Yes")
    itembtn2 = types.KeyboardButton(text="No")
    markup.add(itembtn1,itembtn2)
    th = bot.reply_to(message, "Did you work on research today?", reply_markup=markup)
    data[phone_numbers[message.chat.id]].append(message.text)
    bot.register_next_step_handler(message, addAcad)
def addAcad(message):
    k = types.ReplyKeyboardRemove(selective=False)
    bot.reply_to(message, "Wow, you should do your best!", reply_markup=k)
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    itembtn1 = types.KeyboardButton(text="Yes")
    itembtn2 = types.KeyboardButton(text="No")
    markup.add(itembtn1,itembtn2)
    th = bot.reply_to(message, "Have you studied your research for 30mins today?", reply_markup=markup)
    data[phone_numbers[message.chat.id]].append(message.text)
    bot.register_next_step_handler(message, addReal)
def addReal(message):
    k = types.ReplyKeyboardRemove(selective=False)
    bot.reply_to(message, "I know, you will do your best!", reply_markup=k)
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    itembtn1 = types.KeyboardButton(text="Yes")
    itembtn2 = types.KeyboardButton(text="No")
    markup.add(itembtn1,itembtn2)
    th = bot.reply_to(message, "Have you finished your main work today?", reply_markup=markup)
    data[phone_numbers[message.chat.id]].append(message.text)
    bot.register_next_step_handler(message, finishAll)
def finishAll(message):
    k = types.ReplyKeyboardRemove(selective=False)
    bot.reply_to(message, "Thanks for your answers", reply_markup=k)
    data[phone_numbers[message.chat.id]].append(message.text)
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    resultData = []
    resultData.append([date])
    resultData.append([phone_numbers[message.chat.id]])
    for i in (data[phone_numbers[message.chat.id]]):
        resultData.append([i])
    spreadsheetId = '1CNpAfbG7y2Ewcsnn6hqZ9sinCX5T0RxDfA1FZ2G7WE8'
    range_name = 'A:H'
    resource = {
      "majorDimension": "COLUMNS",
      "values": resultData
    }
    service.spreadsheets().values().append(
      spreadsheetId=spreadsheetId,
      range=range_name,
      body=resource,
      valueInputOption="USER_ENTERED"
    ).execute()
    data[phone_numbers[message.chat.id]] = []
    mainMenu(message)
    
while(True):
    try:
        bot.polling()
    except Exception:
        time.sleep(15)
