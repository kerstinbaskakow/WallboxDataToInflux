#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 15:02:12 2021

@author: kerstin
"""

from chargeApp.config import Config
from chargeApp.utils import queryDataFromInflux,writeDataToInflux
from chargeApp import modbusclientWallbox

    
def calcCurrentTargetValue(modeSelector):
    #1 means "SofortLaden" mit max. Leistung
    if modeSelector == Config.MODESELECTOR_VALUES["IMMEDIATE_CHARGE"]:
        availChargeCurrent_A = Config.WALLBOX_SETTINGS["MAX_CHARGE_CURRENT"]
        availChargePower_W = availChargeCurrent_A*3*230
        maxCurTarVal = availChargeCurrent_A
    #2 means pv surplus
    elif modeSelector == Config.MODESELECTOR_VALUES["SURPLUS_CHARGE"]:
        batteryPower_W = queryDataFromInflux(Config.BATTERY_POWER_INFLUX_QUERY,Config.BATTERY_POWER_INFLUX)
        homePower_W = queryDataFromInflux(Config.HOME_POWER_INFLUX_QUERY,Config.HOME_POWER_INFLUX)
        pvPower_W = queryDataFromInflux(Config.PV_POWER_INFLUX_QUERY,Config.PV_POWER_INFLUX)
        chargePower_W = queryDataFromInflux(Config.CHARGE_POWER_INFLUX_QUERY,Config.CHARGE_POWER_INFLUX)
        if batteryPower_W < 0:
                batteryPower_W = 0
        availChargePower_W = (pvPower_W -(homePower_W+batteryPower_W))+chargePower_W
        availChargeCurrent_A = int(availChargePower_W/(230*3))
        #6A is minimum charge current, 16 is max
        if availChargeCurrent_A<Config.WALLBOX_SETTINGS["MIN_CHARGE_CURRENT"]:
            maxCurTarVal = 0
        elif availChargeCurrent_A >= Config.WALLBOX_SETTINGS["MIN_CHARGE_CURRENT"] and availChargeCurrent_A <=Config.WALLBOX_SETTINGS["MAX_CHARGE_CURRENT"]:
            maxCurTarVal = availChargeCurrent_A
        else:
            maxCurTarVal = Config.WALLBOX_SETTINGS["MAX_CHARGE_CURRENT"]

    else:
        availChargePower_W = Config.WALLBOX_SETTINGS["FAIL_SAFE_CURRENT"]*3*230
        availChargeCurrent_A = Config.WALLBOX_SETTINGS["FAIL_SAFE_CURRENT"]
        maxCurTarVal = availChargeCurrent_A
    return int(maxCurTarVal),int(availChargePower_W),int(availChargeCurrent_A)

def writeCalcCurToCharger(value):
    try:
        modbusclientWallbox.open()
        #current has Faktor 10 at read/write to modbus interface
        modbusclientWallbox.write_single_register(Config.WALLBOX_REGISTER["MAX_CUR_COMMAND"],value*Config.WALLBOX_SETTINGS["CURRENT_SCALE"])
        modbusclientWallbox.close()

    except: 
        modbusclientWallbox.close()

def setWallboxChargeModeMain():
    #check out the actual wished charge mode, and write it back to influx for 
    # visualization in grafana
    # 1: instantly 
    # 2: by surplus
    # 3. no charging current
    mode = queryDataFromInflux('select value from button ORDER BY time desc limit 1',"button")
    writeDataToInflux(mode,"button")
    maxCurTarVal,availChargePower_W,availChargeCurrent_A = calcCurrentTargetValue(mode)

    writeDataToInflux(availChargePower_W,"calcAvailChargePower_W")
    writeDataToInflux(availChargeCurrent_A,"calcAvailChargeCurrent_A")
    #initialize modbus client
    #set charge current via modbus connection
    writeCalcCurToCharger(maxCurTarVal)
    

if __name__ == "__main__":
    setWallboxChargeModeMain()
