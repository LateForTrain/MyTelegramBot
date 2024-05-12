#! /usr/bin/env python3
#  -*- coding: utf-8 -*-
#
# GUI definition for MyTelegramBot
# version started 2024-05-10

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext
from tkinter.constants import *
import MyTelegramBotGUI_support

#This class configures and populates the toplevel window.
#top is the toplevel containing window
class Toplevel1:
     def __init__(self, top=None):
          #checkbox var
          self.WeatherOn_var=tk.BooleanVar()
          self.HolidaysOn_var=tk.BooleanVar()
          self.DateTimeOn_var=tk.BooleanVar()
          self.AircraftOn_var=tk.BooleanVar()
          self.DiceOn_var=tk.BooleanVar()
          self.DefineOn_var=tk.BooleanVar()
          self.MapOn_var=tk.BooleanVar()

          #frame information
          app_width=550
          app_height=350
          top.title("MyTelegramBot - Telegram Bot Control")
          top.geometry(str(app_width)+"x"+str(app_height))
          top.resizable(0,  0)

          # Menu setup
          menubar = tk.Menu(top)
          # Adding Main Menu 
          main = tk.Menu(menubar, tearoff = 0) 
          menubar.add_cascade(label ='File', menu = main) 
          main.add_command(label ='Clear Messages', command = lambda:MyTelegramBotGUI_support.clear_messages()) 
          main.add_command(label ='Exit', command = lambda:MyTelegramBotGUI_support.close_app())

          # Adding Help Menu 
          help_ = tk.Menu(menubar, tearoff = 0) 
          menubar.add_cascade(label ='Help', menu = help_) 
          help_.add_command(label ='Tk Help', command = None) 
          help_.add_separator() 
          help_.add_command(label ='About TBC', command = lambda:MyTelegramBotGUI_support.about_msg())

          top.config(menu = menubar) 

          #items in the frame
          self.top = top

          self.Labelframe1 = tk.LabelFrame(self.top)
          self.Labelframe1.place(x=5, y=5, height=100, width=430)
          self.Labelframe1.configure(relief='groove')
          self.Labelframe1.configure(text="Select Function")

          self.WeatherOn = tk.Checkbutton(self.Labelframe1)
          self.WeatherOn.place(x=0, y=10, height=20, width=100)
          self.WeatherOn.configure(text="Weather")
          self.WeatherOn.configure(anchor="w")
          self.WeatherOn.configure(offvalue=False)
          self.WeatherOn.configure(onvalue=True)
          self.WeatherOn.configure(variable=self.WeatherOn_var)
          self.WeatherOn.configure(command=lambda:MyTelegramBotGUI_support.Check_Press("WeatherOn"))
          
          self.HolidaysOn = tk.Checkbutton(self.Labelframe1)
          self.HolidaysOn.place(x=0, y=30, height=20, width=100)
          self.HolidaysOn.configure(text="Holidays")
          self.HolidaysOn.configure(anchor="w")
          self.HolidaysOn.configure(offvalue=False)
          self.HolidaysOn.configure(onvalue=True)
          self.HolidaysOn.configure(variable=self.HolidaysOn_var)
          self.HolidaysOn.configure(command=lambda:MyTelegramBotGUI_support.Check_Press("HolidaysOn"))

          self.PoliceOn = tk.Checkbutton(self.Labelframe1)
          self.PoliceOn.place(x=0, y=50, height=20, width=100)
          self.PoliceOn.configure(text="Map")
          self.PoliceOn.configure(anchor="w")
          self.PoliceOn.configure(offvalue=False)
          self.PoliceOn.configure(onvalue=True)
          self.PoliceOn.configure(variable=self.MapOn_var)
          self.PoliceOn.configure(command=lambda:MyTelegramBotGUI_support.Check_Press("MapOn"))

          self.DateTimeOn = tk.Checkbutton(self.Labelframe1)
          self.DateTimeOn.place(x=100, y=10, height=20, width=100)
          self.DateTimeOn.configure(text="Date/Time")
          self.DateTimeOn.configure(anchor="w")
          self.DateTimeOn.configure(offvalue=False)
          self.DateTimeOn.configure(onvalue=True)
          self.DateTimeOn.configure(variable=self.DateTimeOn_var)
          self.DateTimeOn.configure(command=lambda:MyTelegramBotGUI_support.Check_Press("DateTimeOn"))

          self.AircraftOn = tk.Checkbutton(self.Labelframe1)
          self.AircraftOn.place(x=100, y=30, height=20, width=100)
          self.AircraftOn.configure(text="Aircraft")
          self.AircraftOn.configure(anchor="w")
          self.AircraftOn.configure(offvalue=False)
          self.AircraftOn.configure(onvalue=True)
          self.AircraftOn.configure(variable=self.AircraftOn_var)
          self.AircraftOn.configure(command=lambda:MyTelegramBotGUI_support.Check_Press("AircraftOn"))

          #self.AircraftOn = tk.Checkbutton(self.Labelframe1)
          #elf.AircraftOn.place(x=100, y=50, height=20, width=100)
          #self.AircraftOn.configure(text="xxx")
          #self.AircraftOn.configure(anchor="w")
          #self.AircraftOn.configure(offvalue=False)
          #self.AircraftOn.configure(onvalue=True)
          #self.AircraftOn.configure(variable=self.xxxOn_var)
          #self.AircraftOn.configure(command=lambda:MyTelegramBotGUI_support.Check_Press("xxxOn"))
          
          self.DiceOn = tk.Checkbutton(self.Labelframe1)
          self.DiceOn.place(x=200, y=10, height=20, width=100)
          self.DiceOn.configure(text="Dice")
          self.DiceOn.configure(anchor="w")
          self.DiceOn.configure(offvalue=False)
          self.DiceOn.configure(onvalue=True)
          self.DiceOn.configure(variable=self.DiceOn_var)
          self.DiceOn.configure(command=lambda:MyTelegramBotGUI_support.Check_Press("DiceOn"))

          self.DefineOn = tk.Checkbutton(self.Labelframe1)
          self.DefineOn.place(x=200, y=30, height=20, width=100)
          self.DefineOn.configure(text="Define Word")
          self.DefineOn.configure(anchor="w")       
          self.DefineOn.configure(offvalue=False)
          self.DefineOn.configure(onvalue=True)
          self.DefineOn.configure(variable=self.DefineOn_var)
          self.DefineOn.configure(command=lambda:MyTelegramBotGUI_support.Check_Press("DefineOn"))

          #self.DefineOn = tk.Checkbutton(self.Labelframe1)
          #self.DefineOn.place(x=200, y=50, height=20, width=100)
          #self.DefineOn.configure(text="xxx")
          #self.DefineOn.configure(anchor="w")       
          #self.DefineOn.configure(offvalue=False)
          #self.DefineOn.configure(onvalue=True)
          #self.DefineOn.configure(variable=self.xxxOn_var)
          #self.DefineOn.configure(command=lambda:MyTelegramBotGUI_support.Check_Press("xxxOn"))
          
          #self.WebcamOn = tk.Checkbutton(self.Labelframe1)
          #self.WebcamOn.place(x=300, y=10, height=20, width=100)
          #self.WebcamOn.configure(text="xxx")
          #self.WebcamOn.configure(anchor="w")
          #self.WebcamOn.configure(offvalue=False)
          #self.WebcamOn.configure(onvalue=True)
          #self.WebcamOn.configure(variable=self.xxxOn_var)
          #self.WebcamOn.configure(command=lambda:MyTelegramBotGUI_support.Check_Press("xxxOn"))

          #self.WebcamOn = tk.Checkbutton(self.Labelframe1)
          #self.WebcamOn.place(x=300, y=30, height=20, width=100)
          #self.WebcamOn.configure(text="xxx")
          #self.WebcamOn.configure(anchor="w")
          #self.WebcamOn.configure(offvalue=False)
          #self.WebcamOn.configure(onvalue=True)
          #self.WebcamOn.configure(variable=self.xxxOn_var)
          #self.WebcamOn.configure(command=lambda:MyTelegramBotGUI_support.Check_Press("xxxOn"))

          #self.WebcamOn = tk.Checkbutton(self.Labelframe1)
          #self.WebcamOn.place(x=300, y=50, height=20, width=100)
          #self.WebcamOn.configure(text="xxx")
          #self.WebcamOn.configure(anchor="w")
          #self.WebcamOn.configure(offvalue=False)
          #self.WebcamOn.configure(onvalue=True)
          #self.WebcamOn.configure(variable=self.xxxOn_var)
          #self.WebcamOn.configure(command=lambda:MyTelegramBotGUI_support.Check_Press("xxxOn"))
          
          self.Bot_Btn = tk.Button(self.top)
          self.Bot_Btn.place(x=440, y=10, height=25, width=100)
          self.Bot_Btn.configure(activebackground="#d9d9d9")
          self.Bot_Btn.configure(activeforeground="black")
          self.Bot_Btn.configure(background="gray")
          self.Bot_Btn.configure(disabledforeground="#a3a3a3")
          self.Bot_Btn.configure(font="-family {Segoe UI} -size 9")
          self.Bot_Btn.configure(foreground="#000000")
          self.Bot_Btn.configure(highlightbackground="#d9d9d9")
          self.Bot_Btn.configure(highlightcolor="#000000")
          self.Bot_Btn.configure(text="Run Bot")
          self.Bot_Btn.bind('<Button-1>',lambda e:MyTelegramBotGUI_support.Button_Press(e,"Bot_Btn"))

          self.SOS_ON_Btn = tk.Button(self.top)
          self.SOS_ON_Btn.place(x=440, y=40, height=25, width=100)
          self.SOS_ON_Btn.configure(activebackground="#d9d9d9")
          self.SOS_ON_Btn.configure(activeforeground="black")
          self.SOS_ON_Btn.configure(background="gray")
          self.SOS_ON_Btn.configure(disabledforeground="#a3a3a3")
          self.SOS_ON_Btn.configure(font="-family {Segoe UI} -size 9")
          self.SOS_ON_Btn.configure(foreground="#000000")
          self.SOS_ON_Btn.configure(highlightbackground="#d9d9d9")
          self.SOS_ON_Btn.configure(highlightcolor="#000000")
          self.SOS_ON_Btn.configure(text="Send SOS Msgs")
          self.SOS_ON_Btn.bind('<Button-1>',lambda e:MyTelegramBotGUI_support.Button_Press(e,"SOS_ON_Btn"))

          self.ScrollStatus = scrolledtext.ScrolledText(self.top)
          self.ScrollStatus.place(x=5, y=105, height=app_height-130, width=540)
          self.ScrollStatus.configure(background = 'light gray')
          self.ScrollStatus.configure(state ='disabled')
          
          self.OutputLable = tk.Label(self.top)
          self.OutputLable.place(x=5, y=app_height-20, height=20, width=345)
          self.OutputLable.configure(text="Waiting ...")
          self.OutputLable.configure(anchor="w")

#init app
def start_up():
    MyTelegramBotGUI_support.main()

if __name__ == '__main__':
    MyTelegramBotGUI_support.main()