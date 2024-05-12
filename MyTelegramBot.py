# -*- coding: utf-8 -*-
# now updated with telegrambot v20.8 

# Code by LateForTrain
from re import X
import time, datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler)
import logging
from random import *
import json
import requests
import threading
import socket
import subprocess
import os
import configparser

####################### General Functions ################################
def read_config(file_path):
    info = configparser.ConfigParser()
    info.read(file_path)
    return info

def send_to_user(message):
    chatID = config.get("TelegramBot","chat_id")
    apiURL = f'https://api.telegram.org/bot{config.get("TelegramBot","token")}/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
        logger.debug(response.text)
    except Exception as the_error:
        logger.error(the_error)

################### Telegram Prep Functions ##############################  
def weatherprep(cityname):
    res = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+cityname+'&appid='+config.get("WeatherAPI","api_id"))
    data = json.loads(res.text)

    if str(data["cod"]) == "404":
        msg="Oops...City not found!"
        return msg
    else:
        clouds = data["weather"]
        weather = data["main"]
        wind = data["wind"]
        try:
            rain = data["rain"]
        except:
            rain = False
        try:
            snow = data["snow"]
        except:
            snow = False
        sys=data["sys"]
        country =sys["country"]
        cityname=data["name"]
        # the result is a Python dictionary:
        msg = ("Conditions in " + cityname + " ("+country+"):\n"+
               "Temp: "+str(round(weather["temp"]- 273.15))+t+"C\n"+
               "Pressure: "+str(weather["pressure"])+"hPa\n"+
               "Humidity: "+str(weather["humidity"])+"%\n"+
               "Wind: "+str(wind["speed"])+"m/s "+str(wind["deg"])+t+"\n")
        if not rain:
            msg=msg
        else:
            msg=msg+"Rain 1h: "+ str(rain["1h"])+"mm\n"
        if not snow:
            msg=msg
        else:
            msg=msg+"Snow 1h: "+ str(snow["1h"])+"mm\n"
        return msg

def timeprep(countrynumber):
    try:
        cnumber=''.join(filter(str.isdigit, countrynumber))
        thecountry = config.get("TimeZones","Country_"+str(cnumber))
        RequestUrl = 'http://worldtimeapi.org/api/timezone/'+config.get("TimeZones","City_"+str(cnumber))
        
        res = requests.get(RequestUrl)
        
        # parse x:
        data = json.loads(res.text)
        #data = json.loads(res)
        thedatetime = data['datetime']
        thedate = thedatetime[:thedatetime.find('T')]
        thetime = thedatetime[thedatetime.find('T')+1:thedatetime.find('T')+6]
        dst=data['dst']
        theweek = data['week_number']
        msg= ("It is now in " + thecountry + " :\n" +
              "Date: "+thedate+"\n"+
              "Time: "+thetime+"\n"+
              "DST: "+str(dst)+"\n"+
              "Week: "+str(theweek))
        return msg
    except:
        msg="Oops...Something went wrong"
        return msg

def definewordprep(theword):
    msg=''
    # using the Free Dictionary API https://dictionaryapi.dev/
    res = requests.get('https://api.dictionaryapi.dev/api/v2/entries/en/'+theword)
    data = json.loads(res.text)
    try:
        if data[0]['word'] == theword:
            i=0
            while i < len(data[0]['meanings']):
                partofspeach = data[0]['meanings'][i]['partOfSpeech']
                j=0
                while j < len(data[0]['meanings'][i]['definitions']):
                    msg = msg + partofspeach + ': ' + data[0]['meanings'][i]['definitions'][j]['definition']+'\n'
                    j=j+1
                i=i+1
            return msg
        else:
            msg = ('Strange!!')
            return msg       
    except:    
        try:
            msg= data['title']
            return msg
        except:
            msg = 'Ooops...something went wrong!'
            return msg

def holidayprep(countrynumber):
    try:
        cnumber=''.join(filter(str.isdigit, countrynumber))
        x = datetime.datetime.now()
        yearstr=x.strftime("%Y")
        RequestUrl = 'https://date.nager.at/api/v3/publicholidays/'+yearstr+'/'+config.get("HolidayCountries","CountryCode_"+str(cnumber))

        res = requests.get(RequestUrl)

        # parse x:
        data = json.loads(res.text)
        #data = json.loads(res)
        TheHolidays =''
        i=0
        test_month = x.strftime("%Y-%m")
        while i < len(data):
            TheHolidays_test = data[i]['date']
            if TheHolidays_test[:7] == test_month:
                TheHolidays = TheHolidays + data[i]['date'] + ' -- ' + data[i]['name'] + '\n'
            i=i+1
            
    
        msg= ("This month has the following holidays:\n" +
              TheHolidays)
        return msg
    except:
        msg="Oops...Something went wrong with the holidays"
        return msg

def aircraftprep():
    l = u"\u007C"
    
    if config.get("Aircraft","API_source")=="dump1090":
        res = requests.get(config.get("Aircraft","API_url"))
        data = json.loads(res.text)
    elif config.get("Aircraft","API_source")=="OpenSky":
        url=config.get("Aircraft","API_url")
        url=url.replace("{lat_min}",config.get("Aircraft","lat_min"))
        url=url.replace("{lat_max}",config.get("Aircraft","lat_max"))
        url=url.replace("{long_min}",config.get("Aircraft","long_min"))
        url=url.replace("{long_max}",config.get("Aircraft","long_max"))

        res = requests.get(url)
        input_data=json.loads(res.text)

        #convert data do dump1090 format, to ease the dump1090 implementation
        data = {
            "now": input_data["time"],
            "messages": 0,
            "aircraft": []
        }

        for aircraft_data in input_data["states"]:
            aircraft = {
                "hex": aircraft_data[0],
                "flight": aircraft_data[1],
                "lat": aircraft_data[6],
                "lon": aircraft_data[5],
                "nucp": 0,
                "seen_pos": 0,
                "altitude": aircraft_data[7],
                "vert_rate": aircraft_data[10],
                "track": 0,
                "speed": 0,
                "category": "--",
                "mlat": [],
                "tisb": [],
                "messages": 0,
                "seen": 0,
                "rssi": 0
            }
            data["aircraft"].append(aircraft)
    else:
        msg="OpenSky or dump1090 not selected in config file."
        return msg

    data_list = data["aircraft"]        

    i=0
    msg="<pre>"
    msg+=l+"  Hex  "+l+" Flight "+l+"\n"
    msg+=l+"-------"+l+"--------"+l+"\n"
    
    while i < len(data_list):
        try:
            msg+=l+data_list[i]["hex"]+" "+l+data_list[i]["flight"]+l+"\n"
            i=i+1
        except:
            msg+=l+data_list[i]["hex"]+" "+l+"XXXXXXX "+l+"\n"
            i=i+1
    msg+=l+"-------"+l+"--------"+l
    msg+="</pre>\n"
    msg+="<a href='http://www.airframes.org/'>Visit Airframes</a>\n"
    if config.get("Aircraft","API_source")=="OpenSky":
        msg+="<a href='https://opensky-network.org'>The OpenSky Network</a>"
    
    return msg
######################## Telegram Menus ##################################
async def menu(update, context):
  await update.message.reply_text("Select option from menu:",
                            reply_markup=main_menu_keyboard())

async def main_menu(update,context):
  query = update.callback_query
  await query.answer()
  await query.edit_message_text(
                        text="Select option from menu:",
                        reply_markup=main_menu_keyboard())

async def weather_menu(update,context):
  query = update.callback_query
  await query.answer()
  await query.edit_message_text(
                        text="Select city:",
                        reply_markup=weather_menu_keyboard())
  
async def time_menu(update,context):
  query = update.callback_query
  await query.answer()
  await query.edit_message_text(
                        text="Select country:",
                        reply_markup=time_menu_keyboard())

async def holiday_menu(update,context):
  query = update.callback_query
  await query.answer()
  await query.edit_message_text(
                        text="Select country:",
                        reply_markup=holiday_menu_keyboard())

async def dice_menu(update,context):
  query = update.callback_query
  await query.answer()
  roll = randint(1,6)
  msg="Dice roll:  " + str(roll)+"\n"
  await query.edit_message_text(
                        text=msg,
                        parse_mode='HTML')

async def define_word_menu(update,context):
  query = update.callback_query
  await query.answer()
  msg="To get the definition of a word, type /word <word to define>."
  await query.edit_message_text(
                        text=msg,
                        reply_markup=None)

async def map_menu(update,context):
  query = update.callback_query
  await query.answer()
  await query.edit_message_text(
                        text="Select map:",
                        reply_markup=map_menu_keyboard())
     
async def end_menu(update,context):
  query = update.callback_query
  await query.answer()
  await query.edit_message_text(
                        text="See later!",
                        reply_markup=None)
  
################################### Keyboards #########################################
def main_menu_keyboard():
    col_count = 0
    active_buttons = []

    # Define keyboard buttons
    buttons = {
        'WeatherOn': InlineKeyboardButton('Weather', callback_data='weather_menu'),
        'DateTimeOn': InlineKeyboardButton('Date/Time', callback_data='time_menu'),
        'HolidaysOn': InlineKeyboardButton('Holidays', callback_data='holiday_menu'),
        'AircraftOn': InlineKeyboardButton('Aircraft', callback_data='air'),
        'DiceOn': InlineKeyboardButton('Dice', callback_data='dice_menu'),
        'WebcamOn': InlineKeyboardButton('Webcam', callback_data='webcam2'),
        'DefineOn': InlineKeyboardButton('Define word', callback_data='define_word_menu'),
        'TrafficOn': InlineKeyboardButton('Traffic', callback_data='traffic_menu'),
        'PoliceOn': InlineKeyboardButton('Police', callback_data='police_menu'),
        'MapOn': InlineKeyboardButton('Map', callback_data='map_menu'),
        'close': InlineKeyboardButton('Close', callback_data='close')
    }

    # Build the active keyboard
    for element, value in server_app_flags.items():
        if element.endswith('On') and value == "True":
            active_buttons.append(buttons[element])
            col_count += 1
            if col_count == 2:  # Adjust column count as needed
                col_count = 0
    # If there are no active buttons, add an empty button to ensure Close button placement
    if not active_buttons:
        active_buttons.append(InlineKeyboardButton(text='', callback_data='empty'))

    # Create keyboard markup
    keyboard = [active_buttons[i:i+2] for i in range(0, len(active_buttons), 2)]

    # Always add the Close button
    keyboard.append([buttons['close']])
    return InlineKeyboardMarkup(keyboard)

def weather_menu_keyboard():
    column = 0
    section_name = 'Weather'
    num_elements = len(config[section_name])
    
    active_keyboard = '['
    for n in range(0,num_elements):
        if column == 0:
            active_keyboard = active_keyboard + "[InlineKeyboardButton('"+config.get("Weather","City_"+str(n))+"', callback_data='"+config.get("Weather","City_"+str(n))+"'),"
            column += 1
        elif column == 1:
            active_keyboard = active_keyboard + "InlineKeyboardButton('"+config.get("Weather","City_"+str(n))+"', callback_data='"+config.get("Weather","City_"+str(n))+"'),"
            column += 1
        elif column == 2:
             active_keyboard = active_keyboard + "InlineKeyboardButton('"+config.get("Weather","City_"+str(n))+"', callback_data='"+config.get("Weather","City_"+str(n))+"')],"
             column = 0
    if column ==0:
        active_keyboard = active_keyboard + ",[InlineKeyboardButton('Back', callback_data='main')]"
    else:
        active_keyboard = active_keyboard + "],[InlineKeyboardButton('Back', callback_data='main')]]"

    keyboard = eval(active_keyboard )

    return InlineKeyboardMarkup(keyboard)

def time_menu_keyboard():
    column = 0
    section_name = 'TimeZones'
    num_elements = len(config[section_name])
    num_elements = num_elements//2

    active_keyboard = '['
    for n in range(0,num_elements):
        if column == 0:
            active_keyboard = active_keyboard + "[InlineKeyboardButton('"+config.get(section_name,"Country_"+str(n))+"', callback_data='Country_"+str(n)+"'),"
            column += 1
        elif column == 1:
            active_keyboard = active_keyboard + "InlineKeyboardButton('"+config.get(section_name,"Country_"+str(n))+"', callback_data='Country_"+str(n)+"'),"
            column += 1
        elif column == 2:
             active_keyboard = active_keyboard + "InlineKeyboardButton('"+config.get(section_name,"Country_"+str(n))+"', callback_data='Country_"+str(n)+"')],"
             column = 0
    if column ==0:
        active_keyboard = active_keyboard + ",[InlineKeyboardButton('Back', callback_data='main')]"
    else:
        active_keyboard = active_keyboard + "],[InlineKeyboardButton('Back', callback_data='main')]]"

    keyboard = eval(active_keyboard )
    
    return InlineKeyboardMarkup(keyboard)

def holiday_menu_keyboard():
    column = 0
    section_name = 'HolidayCountries'
    num_elements = len(config[section_name])
    num_elements = num_elements//2

    active_keyboard = '['
    for n in range(0,num_elements):
        if column == 0:
            active_keyboard = active_keyboard + "[InlineKeyboardButton('"+config.get(section_name,"Country_"+str(n))+"', callback_data='CountryCode_"+str(n)+"'),"
            column += 1
        elif column == 1:
            active_keyboard = active_keyboard + "InlineKeyboardButton('"+config.get(section_name,"Country_"+str(n))+"', callback_data='CountryCode_"+str(n)+"'),"
            column += 1
        elif column == 2:
             active_keyboard = active_keyboard + "InlineKeyboardButton('"+config.get(section_name,"Country_"+str(n))+"', callback_data='CountryCode_"+str(n)+"')],"
             column = 0
    if column ==0:
        active_keyboard = active_keyboard + ",[InlineKeyboardButton('Back', callback_data='main')]"
    else:
        active_keyboard = active_keyboard + "],[InlineKeyboardButton('Back', callback_data='main')]]"

    keyboard = eval(active_keyboard )
    
    return InlineKeyboardMarkup(keyboard)

def map_menu_keyboard():
    keyboard = [
        [
            InlineKeyboardButton('SOS', callback_data='MapSOS'),
        ],
        [InlineKeyboardButton('Back', callback_data='main')]
    ]
    return InlineKeyboardMarkup(keyboard)

################################### Menu Commands #########################################
async def weatherspecial(update, context):
    query = update.callback_query
    await query.answer()
    cityname = update.callback_query.data
    msg=weatherprep(cityname)
    await query.edit_message_text(text=msg, reply_markup=None)       

async def timespecial(update, context):
    query = update.callback_query
    await query.answer()
    countrynumber = update.callback_query.data
    msg=timeprep(countrynumber)
    await query.edit_message_text(text=msg, reply_markup=None)         

async def holidaymain(update, context):
    query = update.callback_query
    await query.answer()
    countrynumber = update.callback_query.data
    msg=holidayprep(countrynumber)
    await query.edit_message_text(text=msg, reply_markup=None)

async def aircraft(update,context):
  query = update.callback_query
  await query.answer()
  msg="Aircraft now seen:\n"
  airinfomsg = aircraftprep()
  msg=msg+airinfomsg
  await query.edit_message_text(
                        text=msg,
                        parse_mode=ParseMode.HTML,
                        reply_markup=None)

async def map_function(update,context):
    query = update.callback_query
    await query.answer()
    mapname = update.callback_query.data
    chat_id = query.message.chat_id

    msg = "Your file"
    if mapname == "MapSOS":
        file_path = config.get("Settings","SOS_htmlfile")
    await context.bot.send_document(chat_id=chat_id, document=open(file_path, 'rb'))
    await query.edit_message_text(text=msg, parse_mode="HTML")

################################### Commands #########################################
async def helpmenu(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="The following commands are available \n" +
                             "/menu    Open menu inline keyboard\n"+
                             "/weather Add city to display current weather\n"+
                             "/time    Return the time of the Telegram Bot\n"+
                             "/dice    Roll a dice\n"+
                             "/word    Add word to get definition")

async def weather(update, context):
    if context.args:
        i=len(context.args)
        n=0
        cityname=""
        while n < i:
            cityname=cityname+str(context.args[n])+" "
            n=n+1
        cityname = cityname.strip()
        msg = weatherprep(cityname)
    else:
        msg="Please add city, for example /weather london"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

async def bottime(update, context):
    now = datetime.datetime.now()
    await context.bot.send_message(chat_id=update.effective_chat.id, text="It is now " + str(now.hour)+str(":")+str(now.minute) + " at the Bot")

async def dice(update, context) -> None:
    roll = randint(1,6)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Dice roll:  " + str(roll))

async def define_word(update, context):
    if context.args:
        i=len(context.args)
        n=0
        theword=""
        while n < i:
            theword=theword+str(context.args[n])+" "
            n=n+1
        theword = theword.strip()
        msg = definewordprep(theword)
    else:
        msg="Please add word, for example /word life"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

############################ Thread functions ###################################
def server():
    logger.info("TELEGRAMBOT: Started Server thread")
    # get the hostname
    host = "127.0.0.1"
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together
    logger.info("TELEGRAMBOT: Server socket binded to %s" %(port))

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    while True:
        conn, address = server_socket.accept()  # accept new connection
        logger.info("TELEGRAMBOT: Connection from: " + str(address))
        connected_flag = True
        while connected_flag:
            # receive data stream. it won't accept data packet greater than 1024 bytes
            try:
                data = conn.recv(1024).decode()
            except:
                connected_flag = False
                break
            if not data:
                # if data is not received break
                break
            
            # handle the flag settings from client 
            # the client could have sent a status request in which case the the serevr sends the status flags
            # or the client could have sent a new status condition, in which case the server process and sets new status
            x = json.loads(data)
            logger.debug("TELEGRAMBOT: Recieved: " + data)
            if x["Msg_type"] == "status_req":
                server_app_flags.update({"Msg_type":"server_init_resp"})
            elif x["Msg_type"] == "client_req":
                for element in x:
                    if x[element].find(">") != -1:
                        if x[element] == ">False":
                            server_app_flags.update({element:"False"})  
                        elif x[element] == ">True":
                            server_app_flags.update({element:"True"})    
            server_app_flags.update({"Msg_type":"server_resp"})
            msg = json.dumps(server_app_flags)
            logger.debug("TELEGRAMBOT: Server Resp: " + msg)
            conn.send(msg.encode())  # send data to the client
    conn.close()  # close the connection

def client(e):
    # this client function is used to send messages to the GUI when no request was recieved
    logger.info("TELEGRAMBOT: Started Client thread")
    global Client_Connected
    global Alarm_msg   
    
    host = "127.0.0.1"  # as both code is running on same pc
    port = 5001  # socket server port number

    while True:
        try:
            if not Client_Connected:
                client_socket = socket.socket()  # instantiate
                client_socket.connect((host, port))  # connect to the server
                Client_Connected = True
                logger.info("TELEGRAMBOT: Client connected")
            event_is_set = e.wait()
            e.clear()
            logger.debug('TELEGRAMBOT: Send to server: '+Alarm_msg)
            client_socket.send(Alarm_msg.encode())  # send message
        except:
            logger.warning("TELEGRAMBOT: failed connect try")
            Client_Connected = False
            time.sleep(10)
    client_socket.close()  # close the connection

def sendalarm():
    logger.info("TELEGRAMBOT: Alarm thread started")
    global Alarm_msg
    global dispatcher

    changedtimeold = os.stat(config.get("Settings","Alarm_File")).st_mtime

    while True:
        if server_app_flags["SOS_ON_Btn"]=="True":
            logger.info("TELEGRAMBOT: Check alarm")
            
            changedtimenew = os.stat(config.get("Settings","Alarm_File")).st_mtime

            if changedtimenew > changedtimeold:
                f = open(config.get("Settings","Alarm_File"), encoding='utf-8', mode="r")
                Alarm_msg = f.read()
                f.close()
                send_to_user(Alarm_msg)
                logger.debug(Alarm_msg)
                e.set()
                logger.info("TELEGRAMBOT: Send alarm msg")
                changedtimeold=changedtimenew

            time.sleep(int(server_app_flags["Alarm_Sleep"]))

############################# Init Functions ###################################
def init_app():
    name="init_app()"
    logger.debug("DEBUG: "+ name + " enter")

    global t
    global Alarm_flag
    global Client_Connected
    global GUI_app
    global e
    global server_app_flags
    global Alarm_msg
    global development
    global config
    global script_directory

    script_path = os.path.realpath(__file__)
    script_directory = os.path.dirname(script_path)

    script_directory = script_directory+'\\'

    config = read_config(script_directory+"test_config.ini")
 
    development=True

    t = u"\u00b0"

    Alarm_flag = False
    Client_Connected = False

    GUI_app ="python3 "+script_directory+"MyTelegramBotGUI.py"

    e = threading.Event()
    
    x = '''{"Msg_type":"none", "Bot_Btn":"True", "SOS_ON_Btn":"False", "WeatherOn":"False", "HolidaysOn":"False",
        "DateTimeOn":"False", "AircraftOn":"False", "DiceOn":"False",
        "WebcamOn":"False", "DefineOn":"False", "TrafficOn":"False", "PoliceOn":"False", 
        "MapOn":"False", "Alarm_Sleep":"%s''' % config.get("Settings","Alarm_Sleep")+'''"}'''
  
    server_app_flags = json.loads(x)
    Alarm_msg = ""

    logger.debug("DEBUG: "+ name + " leave")
    logger.info("TELEGRAMBOT: App init")

def init_threads():
    name="init_threads()"
    logger.debug("DEBUG: "+ name + " enter")
    MyServer = threading.Thread(target=server)
    MyServer.daemon = True
    MyServer.start()

    MyClient = threading.Thread(target=client,args=(e,))
    MyClient.daemon = True
    MyClient.start()
    
    # This function runs at a rate specified Alarm_Sleep in the config file
    # The idea is that some website or file is monitored and when the state changed 
    # the alarm is send to telegram and also display in the GUI
    # for now only monitor file is implemented 
    MyAlarm = threading.Thread(target=sendalarm)
    MyAlarm.daemon = True
    MyAlarm.start()

def init_GUI():
    name="init_GUI()"
    logger.debug("DEBUG: "+ name + " enter")

    TheGui = subprocess.Popen(GUI_app, shell=True)
    logger.info("TELEGRAMBOT: GUI init")

def init_telegrambot():    
    name="init_telegrambot()"
    logger.debug("DEBUG: "+ name + " enter")

    global dispatcher
    global job_queue
     
    dispatcher = Application.builder().token(config.get("TelegramBot","token")).build()
    job_queue = dispatcher.job_queue
    logger.info("TELEGRAMBOT: Telegrambot init")

def init_CommandHandler():
    name="init_CommandHandler()"
    logger.debug("DEBUG: "+ name + " enter")

    dispatcher.add_handler(CommandHandler('help', helpmenu))
    dispatcher.add_handler(CommandHandler('menu', menu))
    dispatcher.add_handler(CommandHandler('weather', weather))
    dispatcher.add_handler(CommandHandler('time', bottime))
    dispatcher.add_handler(CommandHandler('dice', dice))
    dispatcher.add_handler(CommandHandler('word', define_word))
    
    logger.info("TELEGRAMBOT: CommandHandler init")

def init_CallBackHandler():    
    name="init_CallBackHandler()"
    logger.debug("DEBUG: "+ name + " enter")

    dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
    
    dispatcher.add_handler(CallbackQueryHandler(weather_menu, pattern='weather_menu'))
    section_name = 'Weather'
    num_elements = len(config[section_name])
    for n in range(0,num_elements):
        dispatcher.add_handler(CallbackQueryHandler(weatherspecial, pattern=config.get(section_name,"City_"+str(n))))

    dispatcher.add_handler(CallbackQueryHandler(time_menu, pattern='time_menu'))
    section_name = 'TimeZones'
    num_elements = len(config[section_name])
    num_elements = num_elements//2
    for n in range(0,num_elements):
        dispatcher.add_handler(CallbackQueryHandler(timespecial, pattern='Country_'+str(n)))

    dispatcher.add_handler(CallbackQueryHandler(holiday_menu, pattern='holiday_menu'))
    section_name = 'HolidayCountries'
    num_elements = len(config[section_name])
    num_elements = num_elements//2
    for n in range(0,num_elements):
        dispatcher.add_handler(CallbackQueryHandler(holidaymain, pattern='CountryCode_'+str(n)))

    dispatcher.add_handler(CallbackQueryHandler(dice_menu, pattern='dice_menu'))
    dispatcher.add_handler(CallbackQueryHandler(define_word_menu, pattern='define_word_menu'))
    dispatcher.add_handler(CallbackQueryHandler(aircraft, pattern='air'))
    dispatcher.add_handler(CallbackQueryHandler(map_menu , pattern='map_menu'))
    dispatcher.add_handler(CallbackQueryHandler(map_function , pattern='MapSOS')) 
    dispatcher.add_handler(CallbackQueryHandler(end_menu, pattern='close'))
    
    logger.info("TELEGRAMBOT: CallBackHandlers init")

############################# start Telegram Bot ################################
def start_telegrambot():
    name="start_telegrambot()"
    logger.debug("DEBUG: "+ name + " enter")

    logger.info("TELEGRAMBOT: Started telegrambot")
    dispatcher.run_polling(allowed_updates=Update.ALL_TYPES)

################################## Main #########################################
def main() -> None:
    global logger

    # Enable logging for telegram bot
    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
    # set higher logging level for httpx to avoid all GET and POST requests being logged
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logger = logging.getLogger(__name__)
    
    init_app()
    init_threads()
    init_GUI()
    init_telegrambot()
    init_CommandHandler()
    init_CallBackHandler()
    start_telegrambot()

if __name__ == '__main__':
    main()