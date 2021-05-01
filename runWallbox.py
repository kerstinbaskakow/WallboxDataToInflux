#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 20:24:30 2021

@author: kerstin
"""
from chargeApp import logger
from chargeApp.setWallboxChargeMode import setWallboxChargeModeMain
from chargeApp.readWallboxValues import readWallboxValuesMain
import schedule

def runWallboxSchedule():
    logger.debug("--------------- read value -------------")
    readWallboxValuesMain()
    logger.debug("------------------set value ------------")
    setWallboxChargeModeMain()
    
 
schedule.every(5).seconds.do(runWallboxSchedule)


if __name__ == "__main__":
    while True:
        schedule.run_pending()
