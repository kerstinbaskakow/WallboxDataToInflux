#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 13:38:25 2021

@author: kerstin
"""

from pyModbusTCP.client import ModbusClient
import pandas as pd
import time

from influxdb import InfluxDBClient
import datetime
import pandas as pd
#import numpy as np
from config import Config


#bodyDB = [{
#        "measurement": '{}_statistik'.format(modul.rsplit("_")[1]),
#        "time": storingtime,
#        "fields":
#        {
#            "gespeicherteWerteProTag": df.describe().loc['count'],
#            "LeistungMittelwert": df.describe().loc['mean'],
#            "LeistungStandardabweichung": df.describe().loc['std'],
#            "LeistungQuartile25": df.describe().loc['25%'],
#            "LeistungQuartile50": df.describe().loc['50%'],
#            "LeistungQuartile75": df.describe().loc['75%'],
#            "LeistungMaxProTag": df.describe().loc['max'],
#            "LeistungMinProTag": df.describe().loc['min'],
#            "Energie_pos": df[df['value']>0]['value'].sum(),
#            "Energie_neg": df[df['value']<0]['value'].sum(),
#            "EnergiedurchsatzProTag": df['value'].abs().sum()
#            
#        }
#    }]




#define storing time as timebase in influx and grafana
#storingtime = datetime.datetime.utcnow()
#initialize list of datapoints that should be stored in influxdb
influxdata=[]

#dbname = Config.DATABASE
#protocol = 'line'
port=Config.INFLUX_PORT
host='localhost'
#open influx client
influxclient = InfluxDBClient(host=host, port=port)
#influxclient.switch_database(dbname)

modbusclientWallbox=ModbusClient(host="192.168.2.137",port=502)
#modbusclientPV=ModbusClient(host="192.168.2.108",port=502)


try:
    while True:
        modbusclientWallbox.open()
        #modbusclientPV.open()
        
        #print(modbusclientWallbox.write_single_register(261,100))
        #print(modbusclientWallbox.write_single_register(258,4))
        
        
        registerliste = []
#        for key,item in Config.MEASUREMENT_ITEMS_PV.items():
#            try:
#                regs = modbusclientPV.read_holding_registers(key)[0]
#                registerliste.append(("PV",item,key,regs))
#            except:
#                pass

        for key,item in Config.MEASUREMENT_ITEMS_READHOLDING.items():

            try:
                regs = modbusclientWallbox.read_holding_registers(key)[0]
                registerliste.append(("wallbox",item,key,regs))
            except:
                pass
        df_register = pd.DataFrame(registerliste,columns=['geraet','name','register','rawValue']) 
        print(df_register)
        
        modbusclientWallbox.close()
        #modbusclientPV.close()
        time.sleep(6)


except KeyboardInterrupt: 
    modbusclientWallbox.close()
    modbusclientPV.close()
    print("interrupted by keyboard")      
#modbusclient.open()

#print(modbusclient.read_holding_registers(261)[0])
#time.sleep(2)

#print(modbusclient.read_input_registers(5)[0])

#    df = pd.DataFrame(energy_value)   
#    return df
 

#a = modbusclient.write_single_register(261,0)
#print(a)
#time.sleep(2)

#print(modbusclient.read_holding_registers(261)[0])

