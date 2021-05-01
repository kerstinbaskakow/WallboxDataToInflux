#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 15:02:12 2021

@author: kerstin
"""
from chargeApp import influxclient,modbusclientWallbox,logger
from chargeApp.config import Config

def readWallboxValuesMain():
    try:
        modbusclientWallbox.open()
        #print(modbusclientWallbox.write_single_register(258,4))
        modbusclientWallbox.write_single_register(Config.WALLBOX_REGISTER["STDBY_CONTROL"]
                                                ,Config.WALLBOX_REG_STDBYCONTROL["DISABLE"]) #set Stdby controll to "No Stdby"
    except KeyboardInterrupt: 
        logger.error("interrupted by keyboard")  
    except Exception as e:
        logger.error(e)
    else:
        for key,item in Config.MEASUREMENT_ITEMS_INPUTREG.items():
            try:
                regs = modbusclientWallbox.read_input_registers(key)[0]
                logger.debug("{}: {}".format(item,regs))
                body = [{
                    "measurement": item,
                    "fields":
                        {"value": regs}
                    }]
            except Exception as e:
                logger.error(e)
            else:
                influxclient.write_points(body, database=Config.DATABASE, time_precision='s'
                                          , batch_size=10000, protocol='json')
        
        for key,item in Config.MEASUREMENT_ITEMS_READHOLDING.items():
            try:
                regs = modbusclientWallbox.read_holding_registers(key)[0]
                logger.debug("{}: {}".format(item,regs))
                body = [{
                    "measurement": item,
                    "fields":
                        {"value": regs}
                    }]
            except Exception as e:
                logger.error(e)
            else:
                influxclient.write_points(body, database=Config.DATABASE, time_precision='s'
                                          , batch_size=10000, protocol='json')

    finally:
        modbusclientWallbox.close()
        

if __name__ == "__main__":
    readWallboxValuesMain()