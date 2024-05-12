#! /usr/bin/env python3
#  -*- coding: utf-8 -*-
#
# Support code for MyTelegramBot
# version started 2024-05-10

import tkinter as tk
from tkinter.constants import *
from tkinter.messagebox import *
import MyTelegramBotGUI
import time
import threading
import json
import socket
import logging

################################### init App ##########################################
def init_app():
    global root
    global App_flags, Client_Connected
    global e
    global _top1, _w1

    Cient_Connected = False
    e = threading.Event()
    x = """{"Msg_type":"status_req", "Bot_Btn":"none", "SOS_ON_Btn":"none", "WeatherOn":"none", "HolidaysOn":"none",
                    "DateTimeOn":"none", "AircraftOn":"none", "DiceOn":"none",
                    "WebcamOn":"none", "DefineOn":"none", "TrafficOn":"none", "PoliceOn":"none", 
                    "MapOn":"none","Alarm_Sleep":"0"}"""
    App_flags = json.loads(x)

    root = tk.Tk()
    root.protocol( 'WM_DELETE_WINDOW' , root.destroy)
    
    # Creates a toplevel widget.
    _top1 = root
    _w1 = MyTelegramBotGUI.Toplevel1(_top1)
    init(_top1, _w1)

def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top

############################### General Functions ####################################
def Update_flags(flag: str):
    obj = w.OutputLable
    flag_status=App_flags[flag]
    try:
        eval(flag_status)
        if eval(flag_status):
            x = {flag :">False"}
            App_flags.update(x)
            App_flags.update({"Msg_type":"client_req"})
            e.set()
            obj.configure(text=flag + " stop signal sent ...")
        else:
            x = {flag:">True"}
            App_flags.update(x)
            App_flags.update({"Msg_type":"client_req"})
            e.set()
            obj.configure(text=flag + " start signal sent ...")
    except:
        return

def Update_check_flags(flag: str, ck_state: int):
    obj = w.OutputLable
    if ck_state:
        x = {flag:">True"}
        App_flags.update(x)
        App_flags.update({"Msg_type":"client_req"})
        e.set()
        obj.configure(text=flag + " start signal sent ...")
    elif not ck_state:
        x = {flag :">False"}
        App_flags.update(x)
        App_flags.update({"Msg_type":"client_req"})
        e.set()
        obj.configure(text=flag + " stop signal sent ...")

################################ Menu handlers ########################################
def clear_messages():
    obj = w.ScrollStatus
    obj.configure(state ='normal')
    obj.delete('1.0',END)
    obj.configure(state ='disabled')
    return

def close_app():
    root.destroy()

def about_msg():
    about_txt= "This is a control app for the MyTelegramBot.  It is a\n"
    about_txt+="application written by LateForTrain in 2024.  The main funcion\n"
    about_txt+="is to enable controll of which functions are available.\n"
    print(showinfo("About TBC", about_txt))

############################### Button handlers #######################################
def Button_Press(*args):
    App_flags.update({"Msg_type":"client_req"})
    Update_flags(args[1])

def Check_Press(*args):
    evaltext="w."+args[0]+"_var"
    obj=eval(evaltext)
    ck_state=obj.get()
    Update_check_flags(args[0],ck_state)

################################### Thread ##########################################
def Update_Button(element: str):
    obj1 = w.OutputLable
    eval_text = "w." + element
    try:
        obj = eval(eval_text)
        if App_flags[element] == "True":
            obj.configure(background="Green")
            obj1.configure(text=element + " start set.")
        elif App_flags[element] == "False":
            obj.configure(background="Red")
            obj1.configure(text=element + " stop set.")
    except:
        return

def Update_Check(element: str):
    obj1 = w.OutputLable
    eval_text = "w." + element+"_var"
    try:
        obj = eval(eval_text)
        if App_flags[element] == "True":
            obj.set(True)
            obj1.configure(text=element + " start set.")
        elif App_flags[element] == "False":
            obj.set(False)
            obj1.configure(text=element + " stop set.")
    except:
        return
        
def client(e):
    logger.info("GUI: Started client thread")
    global App_flags, App_Connected
    host = "127.0.0.1"  # as both code is running on same pc
    port = 5000  # socket server port number

    while True:
        try:
            if not Client_Connected:
                client_socket = socket.socket()  # instantiate
                client_socket.connect((host, port))  # connect to the server
                Client_Connected = True
                logger.info("GUI: Client connected")
            event_is_set = e.wait()
            
            e.clear()
            msg = json.dumps(App_flags)
            logger.debug('GUI: Send to server: ' + msg)
            client_socket.send(msg.encode())  # send message
            data = client_socket.recv(1024).decode()  # receive response
            logger.debug('Gui: Received from server: ' + data)
            App_flags_new=json.loads(data)
            for element in App_flags_new:
                if App_flags[element] != App_flags_new[element]:
                    App_flags[element] = App_flags_new[element]
                    if element.find("Btn") >= 0:
                        Update_Button(element)
                    else:
                        Update_Check(element)
            e.clear()
            logger.debug('GUI: After Processing: ' + json.dumps(App_flags))
        except:
            logger.warning("GUI: failed connect try")
            Client_Connected = False
            time.sleep(1)

    client_socket.close()  # close the connection

def server():
    logger.info("GUI: Started server thread")
    obj = w.ScrollStatus
    # get the hostname
    host = "127.0.0.1"
    port = 5001  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together
    logger.info("GUI: Socket binded to %s" %(port))

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    while True:
        conn, address = server_socket.accept()  # accept new connection
        logger.info("GUI: Connection from: " + str(address))
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
            obj.configure(state ='normal')
            obj.insert(INSERT,data+"\n")
            obj.insert(INSERT,"--------------------------------------------------------------"+"\n")
            obj.configure(state ='disabled')
            obj.see(END)
    conn.close()  # close the connection

def init_threads():
    MyClient = threading.Thread(target=client,args=(e,))
    MyClient.daemon = True
    MyClient.start()
    
    MyServer = threading.Thread(target=server)
    MyServer.daemon = True
    MyServer.start()

############################### Main definition #####################################
def main(*args):
    global logger

    # Enable logging for telegram bot
    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
    # set higher logging level for httpx to avoid all GET and POST requests being logged
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logger = logging.getLogger(__name__)

    init_app()
    init_threads()
    time.sleep(1)
    e.set()
    logger.info("GUI: Main loop started...")
    root.mainloop()

#executer when class is created
if __name__ == '__main__':
    MyTelegramBotGUI.start_up()