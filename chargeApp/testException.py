#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  3 16:03:01 2021

@author: kerstin
"""

from influxdb import InfluxDBClient
from pyModbusTCP.client import ModbusClient
from config import Config



influxclient = InfluxDBClient(host=Config.INFLUX_HOST, port=Config.INFLUX_PORT)
influxclient.switch_database(Config.DATABASE)

modbusclientWallbox=ModbusClient(host=Config.MOD_HOST,port=Config.MOD_PORT)

while True:
    modbusclientWallbox.open()
    modbusclientWallbox.write_single_register(Config.WALLBOX_REGISTER["STDBY_CONTROL"]
                                                ,Config.WALLBOX_REG_STDBYCONTROL["DISABLE"])
    modbusclientWallbox.close()
    print("still works")
    