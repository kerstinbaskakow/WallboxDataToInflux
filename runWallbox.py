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
    
schedule.every(10).seconds.do(runWallboxSchedule)


if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
