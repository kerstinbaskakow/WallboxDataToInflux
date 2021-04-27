#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 15:02:12 2021

@author: kerstin
"""
def queryData(query,meas,influxclient,Config):
    rawVal = influxclient.query(query)
    value = list(rawVal.get_points(measurement='{}'.format(meas)))[0]['value']
    return value

def writeToInflux(value,nameOfValue,influxclient,Config):
    body = [{
    "measurement": nameOfValue,
    "fields":
        {"value": value}
    }]
    return influxclient.write_points(body, database=Config.DATABASE, time_precision='s', batch_size=10000, protocol='json')
    
def calcCurrentTargetValue(modeSelector,influxclient,Config):
    #1 means "SofortLaden" mit max. Leistung
    if modeSelector == 1:
        availChargeCurrent_A = 16
        availChargePower_W = availChargeCurrent_A*3*230
        maxCurTarVal = availChargeCurrent_A
    #2 means pv surplus
    elif modeSelector == 2:
        batteryPower_W = queryData(Config.BATTERY_POWER_INFLUX_QUERY,Config.BATTERY_POWER_INFLUX,influxclient,Config)
        homePower_W = queryData(Config.HOME_POWER_INFLUX_QUERY,Config.HOME_POWER_INFLUX,influxclient,Config)
        pvPower_W = queryData(Config.PV_POWER_INFLUX_QUERY,Config.PV_POWER_INFLUX,influxclient,Config)
        chargePower_W = queryData(Config.CHARGE_POWER_INFLUX_QUERY,Config.CHARGE_POWER_INFLUX,influxclient,Config)
        if batteryPower_W < 0:
                batteryPower_W = 0
        availChargePower_W = (pvPower_W -(homePower_W+batteryPower_W))+chargePower_W
        availChargeCurrent_A = int(availChargePower_W/(230*3))
        #6A is minimum charge current, 16 is max
        if availChargeCurrent_A<6:
            maxCurTarVal = 0
        elif availChargeCurrent_A >= 6 and availChargeCurrent_A <=16:
            maxCurTarVal = availChargeCurrent_A
        else:
            maxCurTarVal = 16

    else:
        availChargePower_W = 0
        availChargeCurrent_A = 0
        maxCurTarVal = availChargeCurrent_A
    return int(maxCurTarVal),int(availChargePower_W),int(availChargeCurrent_A)

def writeCalcCurToCharger(value,Config):
    from pyModbusTCP.client import ModbusClient
    modbusclientWallbox=ModbusClient(host=Config.MOD_HOST,port=Config.MOD_PORT)
    try:
        modbusclientWallbox.open()
        #current has Faktor 10 at read/write to modbus interface
        modbusclientWallbox.write_single_register(261,value*10)
        modbusclientWallbox.close()

    except: 
        modbusclientWallbox.close()
    

def setWallboxChargeModeMain():
    
    import time
    
    from influxdb import InfluxDBClient
    from config import Config
    influxclient = InfluxDBClient(host=Config.INFLUX_HOST, port=Config.INFLUX_PORT)
    influxclient.switch_database(Config.DATABASE)
    
    #check out the actual wished charge mode, and write it back to influx for 
    # visualization in grafana
    # 1: instantly 
    # 2: by surplus
    # 3. no charging current
    mode = queryData('select value from button ORDER BY time desc limit 1',"button",influxclient,Config)
    writeToInflux(mode,"button",influxclient,Config)
    maxCurTarVal,availChargePower_W,availChargeCurrent_A = calcCurrentTargetValue(mode,influxclient,Config)

    writeToInflux(availChargePower_W,"calcAvailChargePower_W",influxclient,Config)
    writeToInflux(availChargeCurrent_A,"calcAvailChargeCurrent_A",influxclient,Config)
    influxclient.close()
    
    print("setWallboxChargeMode Runtime =", time.strftime("%H:%M:%S"))
    #initialize modbus client
    #set charge current via modbus connection
    writeCalcCurToCharger(maxCurTarVal,Config)
    



if __name__ == "__main__":
    setWallboxChargeModeMain()