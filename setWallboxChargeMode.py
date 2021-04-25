#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 15:02:12 2021

@author: kerstin
"""

def queryData(query,meas):
    from influxdb import InfluxDBClient
    from config import Config
    #intialize influx client
    influxclient = InfluxDBClient(host=Config.INFLUX_HOST, port=Config.INFLUX_PORT)
    influxclient.switch_database(Config.DATABASE)
    rawVal = influxclient.query(query)
    value = list(rawVal.get_points(measurement='{}'.format(meas)))[0]['value']
    return value

def writeToInflux(value,nameOfValue):
    from influxdb import InfluxDBClient
    from config import Config
    influxclient = InfluxDBClient(host=Config.INFLUX_HOST, port=Config.INFLUX_PORT)
    influxclient.switch_database(Config.DATABASE)
    body = [{
    "measurement": nameOfValue,
    "fields":
        {"value": value}
    }]
    influxclient.write_points(body, database=Config.DATABASE, time_precision='s', batch_size=10000, protocol='json')
    

def setWallboxChargeMode():
#    from influxdb import InfluxDBClient
    from pyModbusTCP.client import ModbusClient
    from config import Config
    
    #initialize modbus client
    modbusclientWallbox=ModbusClient(host=Config.MOD_HOST,port=Config.MOD_PORT)
    
    print()
    
    try:
        
        modbusclientWallbox.open()
        modeSelector = queryData('select value from button ORDER BY time desc limit 1',"button")
        if modeSelector == 1:
            maxCurTarVal = 16
        #2 means pv surplus
        elif modeSelector == 2:
            batteryPower_W = queryData(Config.BATTERY_POWER_INFLUX_QUERY,Config.BATTERY_POWER_INFLUX)
            homePower_W = queryData(Config.HOME_POWER_INFLUX_QUERY,Config.HOME_POWER_INFLUX)
            pvPower_W = queryData(Config.PV_POWER_INFLUX_QUERY,Config.PV_POWER_INFLUX)
            availChargePower_W = pvPower_W -(homePower_W+batteryPower_W)
            availChargeCurrent_A = int(availChargePower_W/(230*3))
            #6A is minimum charge current, 16 is max
            if availChargeCurrent_A<6:
                maxCurTarVal = 0
            elif availChargeCurrent_A >= 6 and availChargeCurrent_A <=16:
                maxCurTarVal = availChargeCurrent_A
            else:
                maxCurTarVal = 16
            print("batteryPower_W ",batteryPower_W)
            print("homePower_W ",homePower_W)
            print("pvPower_W ",pvPower_W)
            print("availChargePower_W ",availChargePower_W)
            print("availChargeCurrent_A ",availChargeCurrent_A)
            writeToInflux(availChargePower_W,"calcAvailChargePower_W")
            writeToInflux(availChargeCurrent_A,"calcAvailChargeCurrent_A")
        else:
            maxCurTarVal = 12
        #current has Faktor 10 at read/write to modbus interface
        modbusclientWallbox.write_single_register(261,maxCurTarVal*10)
        modbusclientWallbox.close()

    except KeyboardInterrupt: 
        modbusclientWallbox.close()
        print("interrupted by keyboard")  

if __name__ == "__main__":
    setWallboxChargeMode()