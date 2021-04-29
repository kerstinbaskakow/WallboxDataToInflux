# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 12:19:33 2019

@author: FBASKKE-ADM
"""

import sys
sys.path.append('../')  

from influxdb import InfluxDBClient
from pyModbusTCP.client import ModbusClient
from chargeApp.config import Config



influxclient = InfluxDBClient(host=Config.INFLUX_HOST, port=Config.INFLUX_PORT)
influxclient.switch_database(Config.DATABASE)

modbusclientWallbox=ModbusClient(host=Config.MOD_HOST,port=Config.MOD_PORT)


