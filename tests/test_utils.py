#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 20:24:30 2021

@author: kerstin
"""


import sys
sys.path.append('../')  
import numpy as np
import unittest
from influxdb import InfluxDBClient
from pyModbusTCP.client import ModbusClient
from chargeApp.config import Config
influxclient = InfluxDBClient(host="192.168.2.127", port=Config.INFLUX_PORT)
influxclient.switch_database(Config.DATABASE)
modbusclientWallbox=ModbusClient(host=Config.MOD_HOST,port=Config.MOD_PORT)
from chargeApp.utils import writeDataToInflux,queryDataFromInflux

meas = "TestValues"
value= np.random.randint(0,10000)
query= 'SELECT * FROM "{}" ORDER BY time DESC LIMIT 1'.format(meas)




class TestUtils(unittest.TestCase):
    
    def test_writeDataToInflux(self):   
        meas = "TestValues"
        value= np.random.randint(0,10000)
        result = writeDataToInflux(value,meas)
        self.assertTrue(result)
        influxclient.query("DELETE from {}".format(meas))
        
    def test_queryDataFromInflux(self):
        meas = "TestValues"
        value= np.random.randint(0,10000)
        writeDataToInflux(value,meas)
        query= 'SELECT * FROM "{}" ORDER BY time DESC LIMIT 1'.format(meas)
        result = queryDataFromInflux(query,meas)
        self.assertEqual(result,value)
        influxclient.query("DELETE from {}".format(meas))

    def test_findActivePhases(self):  
        resultTarget = []
        for phase in range(1,4,1):
            values= np.random.randint(2, size=1)
            meas = "L{}_Current_A".format(phase)
            for value in values:
                resultTarget.append(value)
                writeDataToInflux(int(value*230),meas)
        from chargeApp.utils import findActivePhases
        for i in range(100):
            result = findActivePhases()
            self.assertEqual(result,sum(resultTarget))
        for phase in range(1,4,1):      
            meas = "L{}_Current_A".format(phase)
            influxclient.query("DELETE from {}".format(meas))
