#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 22:08:33 2021

@author: kerstin
"""

#modbus.0.holdingRegisters.40067_PV_Leistung
#modbus.0.holdingRegisters.40069_Batterie_Leistung
#modbus.0.holdingRegisters.40071_Hausverbrauch_Leistung

from influxdb import InfluxDBClient
from config import Config
#intialize influx client
influxclient = InfluxDBClient(host=Config.INFLUX_HOST, port=Config.INFLUX_PORT)
influxclient.switch_database(Config.DATABASE)
body = [{
    "measurement": Config.BATTERY_POWER_INFLUX,
    "fields":
        {"value": 3201}
    }]
influxclient.write_points(body, database=Config.DATABASE, time_precision='s', batch_size=10000, protocol='json')
body2 = [{
    "measurement": Config.HOME_POWER_INFLUX,
    "fields":
        {"value": 684}
    }]
influxclient.write_points(body2, database=Config.DATABASE, time_precision='s', batch_size=10000, protocol='json')
body3 = [{
    "measurement": Config.PV_POWER_INFLUX,
    "fields":
        {"value": 9734}
    }]
influxclient.write_points(body3, database=Config.DATABASE, time_precision='s', batch_size=10000, protocol='json')
