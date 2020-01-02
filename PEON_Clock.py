#!/usr/bin/python3
'''
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MW::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::WM
MN                                                                            NM
MN      cXXXXXK0kl.    xXXXXXXXXXXc      :kKNNNNKk:       KXXd       kXc      NM
MN      oMN    .lWMl   OMO             oWNl.    .lWWl     WMXMO      KMo      NM
MN      oMX      dMW   OMk            xMX.        .NMd    WM;oMK.    KMo      NM
MN      oMX     .XMO   OMK::::::::   .MM:          cMM.   WM; :MX.   KMo      NM
MN      oMW0000NWKl    OMXoooooooo   'MM'          ,MM.   WM;  ,WN'  KMo      NM
MN      oMN....        OMk            WMo          dMN    WM;   .NW; KMo      NM
MN      oMX            OMk            :MW:        cMW;    WM;    .XMcKMo      NM
MN      oMX            OMKcccccccc,    .OMKl;'';lKMO.     WM;      0MMMo      NM
MN      'lc            ;llllllllll;      .;lxxxdl;        ll.       cll'      NM
MN                                                                            NM
MN                                                                            NM
MW:::::::::::::::::::::::::::::::::::clock::::::::::::::::::::::::::::::::::::WM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
'''

'''
A PEON Clock is a clock that reminds you of your Personal Economic Offering to
the Nation. Such a Clock is meant to be simple but effective in reminding each
PEON of their debts and the time until their release.

The clock chimes in agony every hour and the time of release flashes red if 
the debt is not estimated to be paid back in the peons lifetime.

The clock is flexible and can accommodate any abominable debt or combinations 
thereof.

This PEON Clock was made by Julio(Struma) late Dec 2019.
'''
 

import os
import tkinter as tk
import pygubu
import time
import pickle
from datetime import datetime
from datetime import date
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import random

CURDIR = os.path.dirname(__file__)
UI_FILE = os.path.join(CURDIR, 'PEON_Clock.ui')
IMAGE_FILE = os.path.join(CURDIR, 'peon1.gif')  #puts img path in resources

class Application:
    def __init__(self, master):

        #1: Create a builder
        self.builder = builder = pygubu.Builder()

        #2: Load an ui file
        builder.add_from_file(UI_FILE)

        #3: Create the widget using a master as parent
        self.mainwindow = builder.get_object('Frame_1', master)

        master.rowconfigure(0, weight=1)
        master.columnconfigure(0, weight=1)
        master.title("Peon Clock")

        #load in the clock variables
        GoldenYoke = pickle.load(open("PEON_conf", "rb"))

        self.timeOfDeath = GoldenYoke[0]
        self.debt = GoldenYoke[1]
        self.monthlyPayments = GoldenYoke[2] 
        self.interestRate = GoldenYoke[3]
        self.mugShot = GoldenYoke[4]
        self.clock_theme = GoldenYoke[5]

        if self.clock_theme == "dark":
            self.bk = "black"
            self.fg = "white"
        else:
            self.fg = "black"
            self.bk = "white"

        self.toggle = False
        self.flash = False
        self.wail = False
        self.update = False

        style = tk.ttk.Style()
        style.configure("BW.TLabel", background=self.bk, foreground=self.fg, font='helvetica 18 bold')
        
        style1 = tk.ttk.Style()
        style1.configure("BACK.TFrame", background=self.bk)
        
        style2 = tk.ttk.Style()
        style2.configure("TIME.TLabel", background=self.bk, foreground=self.fg, font='helvetica 65 bold')

        style3 = tk.ttk.Style()
        style3.configure("TIMER.TLabel", background=self.bk, foreground=self.fg, font='helvetica 65 bold')


        death_list = self.timeOfDeath.split("-")  #dd-mm-yy
        self.timeOfDeath = datetime(int(death_list[2]), int(death_list[1]), int(death_list[0]))

        self.current_time = datetime.fromtimestamp(time.time())

        self.time_to_release = self.peonage()
        self.time_to_release = self.current_time + relativedelta(months=self.time_to_release)

        builder.connect_callbacks(self)
        self.times()

        
    def times(self):

        self.current_time = datetime.fromtimestamp(time.time())
        if self.time_to_release >= self.timeOfDeath:
            self.time_to_release = self.timeOfDeath
            self.toggle = True
        else:
            self.toggle = False
        time_delt = self.time_to_release - self.current_time
        total_sec = int(time_delt.total_seconds())

        string_time = self.current_time.strftime('%A %b %d - %I:%M:%S %p')         
        death_pred = "Estimated Death : " + self.timeOfDeath.strftime("%A %b %d %Y")
        debt_amount = "Debt Owed $%s - get to work." % self.debt 
        
        self.builder.tkvariables["loan_value"].set(debt_amount)
        self.builder.tkvariables["death_time"].set(death_pred)
        self.builder.tkvariables["TD_label"].set(string_time)

        self.builder.tkvariables["seconds"].set("Seconds : %s" % total_sec)
        self.builder.tkvariables["minutes"].set("Minutes : %i" % (total_sec/60))
        self.builder.tkvariables["hours"].set("Hours : %i" % (total_sec/3600))
        self.builder.tkvariables["days"].set("Days : %i" % (total_sec/(3600 * 24)))
        self.builder.tkvariables["years"].set("Years : %i" % (total_sec/(3600 * 24 * 365)))
        self.builder.tkvariables["months"].set("Months : %i" % ((total_sec * 12)/(3600 * 24 * 365)))
        self.builder.tkvariables["decades"].set("Decades : %i" % (total_sec/(3600 * 24 * 365 * 10)))

        self.builder.tkvariables["release_time"].set(self.time_to_release.strftime("%A %b %d %Y"))

        self.toggle_red()
        self.waily()
        self.updater()
        
        self.builder.get_object("TimeDate").after(150, self.times)
        
    def peonage(self):
        monthIntr_dec = float(self.interestRate)/(12*100)  #12months and 100toconv to decimal
        count = 0
        debt_int = int(self.debt)
        while True:
            remaining = int(self.monthlyPayments) - (monthIntr_dec * debt_int)  #money from pauyment remaining after interest
            debt_int = debt_int - remaining                                     #capital debt paid off 
            count += 1
            if (count/12 > 150): #Assume the max lifespan for a human debt is >150years
                return int(count)    
            if debt_int <= 0:
                return int(count)
           

    def waily(self):
        if self.wail == False:
            if self.current_time.strftime('%M')   == "00":
                #Play a random whail sound hourly
                name = str(random.randint(0, 62))
                name = name.zfill(3) + ".mp3"
                file = CURDIR + "/Screams/" + name
                os.system("mpg123 " + file + " &")
                self.wail = True
        else:
            if self.current_time.strftime('%M')  != "00": #block funtion for next minute
                self.wail = False

    def updater(self):
        if self.update == False:
            if self.current_time.strftime('%H:%M')   == "00:00":
                #perform update once a day at midnight
                #load in the clock variables
                GoldenYoke = pickle.load(open("PEON_conf", "rb"))

                self.timeOfDeath = GoldenYoke[0]
                self.debt = GoldenYoke[1]
                self.monthlyPayments = GoldenYoke[2] 
                self.interestRate = GoldenYoke[3]
                self.mugShot = GoldenYoke[4]
                self.clock_theme = GoldenYoke[5]

                if self.clock_theme == "dark":
                    self.bk = "black"
                    self.fg = "white"
                else:
                    self.fg = "black"
                    self.bk = "white"

                self.toggle = False
                self.flash = False

                style = tk.ttk.Style()
                style.configure("BW.TLabel", background=self.bk, foreground=self.fg, font='helvetica 18 bold')
                
                style1 = tk.ttk.Style()
                style1.configure("BACK.TFrame", background=self.bk)
                
                style2 = tk.ttk.Style()
                style2.configure("TIME.TLabel", background=self.bk, foreground=self.fg, font='helvetica 65 bold')

                style3 = tk.ttk.Style()
                style3.configure("TIMER.TLabel", background=self.bk, foreground=self.fg, font='helvetica 65 bold')


                death_list = self.timeOfDeath.split("-")  #dd-mm-yy
                self.timeOfDeath = datetime(int(death_list[2]), int(death_list[1]), int(death_list[0]))
                self.update = True
                self.current_time = datetime.fromtimestamp(time.time())

                self.time_to_release = self.peonage()
                self.time_to_release = self.current_time + relativedelta(months=self.time_to_release)                

        else:
            if self.current_time.strftime('%H:%M')  != "00:00": #block function until next minute
                self.update = False
            
        
    def toggle_red(self):
        if self.toggle == True:
            if self.flash == False:
                style3 = tk.ttk.Style()
                style3.configure("TIMER.TLabel", background=self.bk, foreground="red", font='helvetica 65 bold')
                self.flash = True
            else:
                style3 = tk.ttk.Style()
                style3.configure("TIMER.TLabel", background=self.bk, foreground=self.fg, font='helvetica 65 bold')  
                self.flash = False        
        

if __name__ == '__main__':

    def fullscreen():
          root.attributes('-fullscreen', True)  
          root.config(cursor="none")
    def normscreen():
          root.attributes('-fullscreen', False)  
          root.config(cursor="")


    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.config(cursor="none")
    root.bind('<Escape>',lambda e: normscreen())
    root.bind('<F11>', lambda e: fullscreen())
    imgicon = tk.PhotoImage(file=os.path.join(CURDIR,'PEONicon.gif'))
    root.tk.call('wm', 'iconphoto', root._w, imgicon)  

    app = Application(root)
    root.mainloop()
