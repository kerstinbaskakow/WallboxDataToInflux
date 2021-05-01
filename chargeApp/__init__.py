# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 12:19:33 2019

@author: FBASKKE-ADM
"""

import sys
sys.path.append('../')  

import logging
from influxdb import InfluxDBClient
from pyModbusTCP.client import ModbusClient
from chargeApp.config import Config

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fileHandler = logging.FileHandler("logfiles/wallbox.log")
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)


influxclient = InfluxDBClient(host=Config.INFLUX_HOST, port=Config.INFLUX_PORT)
influxclient.switch_database(Config.DATABASE)

modbusclientWallbox=ModbusClient(host=Config.MOD_HOST,port=Config.MOD_PORT)




