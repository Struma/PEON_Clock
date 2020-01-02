#!/usr/bin/python3

j = '''MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
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
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM'''
#helper script to generate new config json for peon clock
#Written by Julio(Struma) as part of the PEON Clock project


import pickle
import os
import time
import re
import sys 
from termcolor import colored, cprint 
from PIL import Image
from shutil import copyfile

CURDIR = os.path.dirname(__file__)
IMAGE_FILE = os.path.join(CURDIR, 'peon1.gif') 


def time_of_death():
    valid_date = "^(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$"
    while True:
        tod = input("Please enter your predicted time of death\nFormat dd-mm-yyyy  ex. 13-8-1936\n")
        check = re.search(valid_date, tod)
        try:
            check.group()
            return tod
        except:
            continue
   
def debt_total():
    valid_num = "^(\d+\d+)$|^(\d+)$"
    while True:
        dto = input("Please enter your total debt\nFormat dddddddddd  ex. 1000000\n")
        check = re.search(valid_num, dto)
        try:
            check.group()
            return dto
        except:
            continue

def monthly_payment():
    valid_num = "^(\d+\d+)$|^(\d+)$"
    while True:
        dto = input("Please enter your monthly payment amount\nFormat dddddddddd  ex. 333\n")
        check = re.search(valid_num, dto)
        try:
            check.group()
            return dto
        except:
            continue


def interest_rate():
    valid_num = "^(\d{1,2}\.\d{1,2})$|^(\d{1,2}$)"
    while True:
        dto = input("Please enter your percent interest rate\nFormat dd.dd  ex. 7 or 7.7 or 77.07\n")
        check = re.search(valid_num, dto)
        try:
            check.group()
            return dto
        except:
            continue


def profile_image(): 
    while True:
        pathname = input("Please enter complete path to profile image\nFormat /link/to/path.gif\nENTER to skip\nNone for no image\n")
        try:
            if os.path.exists(pathname) & os.path.isfile(pathname):
                return pathname
            elif pathname == "":
                return pathname
            elif pathname == "None":
                return pathname
            else:
                print("path \"%s\" not exist, include the image name, must be gif format" % pathname)   
        except:
            print("path \"%s\" not exist, include the image name, must be gif format" % pathname)
            continue
   

def theme():
    while True:
        theme_s = input("Select theme\nType dark or light\n\n Press enter for default dark theme\n")
        try:
            if theme_s == "dark" or theme_s == "light":
                return theme_s
            elif theme_s == "":
                return "dark"
            else:
                print("Error, please select light or dark")
        except:
            print("Error, please select light or dark")
            continue

def reset():
    while True:
        choice = input("Do you wanna reset the clock?\n\nPlease answer y/n\n")
        if choice == "y":
            return False
        elif choice == "n":
            return True
        else:
            print("error, please type y or n followed by enter")
            continue #do nothing

os.system('cls' if os.name == 'nt' else 'clear')
text = colored(j, 'red', attrs=['bold']) 
print(text) 
time.sleep(2)
print("Hello fellow debt slave!")
time.sleep(3)

os.system('cls' if os.name == 'nt' else 'clear')
flag = reset()
os.system('cls' if os.name == 'nt' else 'clear')
if flag:
    print("When will you kick the bucket?")
    time.sleep(2)
    print("Find out here!!!! -> https://www.death-clock.org/ <-")
    time.sleep(2)
    timeOfDeath = time_of_death()
    os.system('cls' if os.name == 'nt' else 'clear')
    debt = debt_total()
    os.system('cls' if os.name == 'nt' else 'clear')
    monthlyPayments = monthly_payment()
    os.system('cls' if os.name == 'nt' else 'clear')
    interestRate = interest_rate()
    os.system('cls' if os.name == 'nt' else 'clear')
    clock_theme = theme()
    os.system('cls' if os.name == 'nt' else 'clear')
    mugShot = profile_image()

    if mugShot == "": 
        pass
    elif mugShot == "None":
        copyfile("none.default", "peon1.gif")
    else:
        try:
            picture = Image.open(mugShot)
            picture = picture.resize((330, 330))
            picture.save(IMAGE_FILE, "gif")
            print("image converted and saved")
        except:
            print("error saving mugshot")
            pass

    GoldenYoke = [ timeOfDeath, debt, monthlyPayments, interestRate, mugShot, clock_theme ]

    print("config saved successfully")

    pickle.dump(GoldenYoke, open("PEON_conf", "wb"))
else:
    copyfile("peon1.default", "peon1.gif")
    copyfile("PEON_conf.default", "PEON_conf")

