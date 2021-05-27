#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 25 16:39:45 2021

@author: kerstin
"""

from influxdb import InfluxDBClient

from config import Config



influxclient = InfluxDBClient(host=Config.INFLUX_HOST, port=Config.INFLUX_PORT)
influxclient.switch_database(Config.DATABASE)

#a = {'time': '2021-04-25T20:43:43Z', 'value': 9734}
#print(a['value'])
#b = [{'time': '2021-04-25T20:43:43Z', 'value': 9734}, {'time': '2021-04-25T20:14:24Z', 'value': 4030}, {'time': '2021-04-25T20:14:15Z', 'value': 7030}, {'time': '2021-04-25T20:14:02Z', 'value': 7000}]
#print(list(map(lambda x: x['value'],b)))
#from numpy import mean

def queryDataFromInflux(query,meas,lim):
    import numpy as np
    limit = " LIMIT {}".format(lim)
    rawVal = influxclient.query(query+limit)
    valueList = list(rawVal.get_points(measurement='{}'.format(meas)))#[0]['value']
    values = list(map(lambda x: x['value'],valueList))
    print(values)
    return int(np.mean(values))

#
PV_POWER_INFLUX = "modbus.0.holdingRegisters.40067_PV_Leistung" 
PV_POWER_INFLUX_QUERY = 'SELECT * FROM "{}" ORDER BY time DESC'.format(PV_POWER_INFLUX)

testquery = queryDataFromInflux(PV_POWER_INFLUX_QUERY,PV_POWER_INFLUX,1)
print(testquery)