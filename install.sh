#!/bin/bash

sudo apt install python3 python3-tk python3-pip python3-dateutil python3-termcolor mpg123 git

git clone https://github.com/Struma/PEON_Clock.git

pip3 install pygubu

cd PEON_Clock 

chmod +x PEON_Clock.py

#Run these lines if you wan to reconfigure the clock
#chmod +x PEON_Config.py
#./PEON_Config.py

./PEON_Clock.py
