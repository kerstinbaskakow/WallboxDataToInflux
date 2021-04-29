#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 15:23:10 2021

@author: kerstin
"""
from chargeApp import influxclient,modbusclientWallbox
from chargeApp.config import Config


def queryDataFromInflux(query,meas):
    rawVal = influxclient.query(query)
    value = list(rawVal.get_points(measurement='{}'.format(meas)))[0]['value']
    return value

def writeDataToInflux(value,nameOfValue):
    body = [{
    "measurement": nameOfValue,
    "fields":
        {"value": value}
    }]
    return influxclient.write_points(body, database=Config.DATABASE, time_precision='s', batch_size=10000, protocol='json')