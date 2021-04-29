#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 20:24:30 2021

@author: kerstin
"""

from chargeApp.setWallboxChargeMode import setWallboxChargeModeMain
from chargeApp.readWallboxValues import readWallboxValuesMain
import time

import schedule

def runWallboxSchedule():
    print("read value")
    readWallboxValuesMain()
    time.sleep(1)
    setWallboxChargeModeMain()
    print("set value")
    


#def job():
#    print("I'm working...")

schedule.every(10).seconds.do(runWallboxSchedule)
#schedule.every(10).minutes.do(job)
#schedule.every().hour.do(job)
#schedule.every().day.at("10:30").do(job)
#schedule.every(5).to(10).minutes.do(job)
#schedule.every().monday.do(job)
#schedule.every().wednesday.at("13:15").do(job)
#schedule.every().minute.at(":17").do(job)



if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
