#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 15:17:48 2020

@author: kerstin
"""
class Config:
    DATABASE='iobroker'
    MOD_PORT=502
    MOD_HOST="192.168.2.137"
    INFLUX_PORT=8086
    INFLUX_HOST='localhost'
    

    MEASUREMENT_ITEMS_INPUTREG = {5:'ChargingState',
                         6:'L1_Current_A',
                         7:'L2_Current_A',
                         8:'L3_Current_A',
                         9:'PCB_Temperatur_dC',
                         10:'L1_Voltage_V',
                         11:'L2_Voltage_V',
                         12:'L3_Voltage_V',
                         13:'Extern_lock_state',
                         14:'ChargePower_W',
                         15:'Energy_since_PowerON_highbyte_Wh',
                         16:'Energy_since_PowerON_lowbyte_Wh',
                         17:'Energy_since_installation_highbyte_Wh',
                         18:'Energy_since_installation_lowbyte_Wh',
                         100:'HW_config_max_current_A',
                         101:'HW_config_min_current_A'               
                         
                         }


    MEASUREMENT_ITEMS_READHOLDING = {257:'Watchdog_Timeout_ms',
                         259:'Remote_Lock_State',
                         261:'Max_Current_Command_A',
                         262:'Failsafe_Current_A'
                         }
    
    MODESELECTOR_VALUES={"IMMEDIATE_CHARGE":1,
                         "SURPLUS_CHARGE":2,
                         "ANYTHING_ELSE":3
                         }
    
    WALLBOX_SETTINGS = {"MIN_CHARGE_CURRENT":6,
                        "MAX_CHARGE_CURRENT":16,
                        "FAIL_SAFE_CURRENT":6,
                        "CURRENT_SCALE":10,
                        "NUMBER_OF_PHASES_MAX":3
            }
    WALLBOX_REGISTER = {"STDBY_CONTROL":258,
                        "MAX_CUR_COMMAND":261
            }
    WALLBOX_REG_STDBYCONTROL={"ENABLE":0,
                              "DISABLE":4}
    
    
    
    CURRENT_INFLUX = "L{}_Current_A"
#    CURRENT_INFLUX_QUERY = 'SELECT * FROM {} ORDER BY time DESC LIMIT 1'.format(CURRENT_INFLUX)
#    L2_CURRENT_INFLUX = "L2_Current_A" 
#    L2_CURRENT_INFLUX_QUERY = 'SELECT * FROM {} ORDER BY time DESC LIMIT 1'.format(L2_CURRENT_INFLUX)
#    L3_CURRENT_INFLUX = "L3_Current_A" 
#    L3_CURRENT_INFLUX_QUERY = 'SELECT * FROM {} ORDER BY time DESC LIMIT 1'.format(L3_CURRENT_INFLUX)
    CHARGE_POWER_INFLUX = "ChargePower_W" 
    CHARGE_POWER_INFLUX_QUERY = 'SELECT * FROM {} ORDER BY time DESC LIMIT 1'.format(CHARGE_POWER_INFLUX)
    PV_POWER_INFLUX = "modbus.0.holdingRegisters.40067_PV_Leistung" 
    PV_POWER_INFLUX_QUERY = 'SELECT * FROM "{}" ORDER BY time DESC LIMIT 1'.format(PV_POWER_INFLUX)
    BATTERY_POWER_INFLUX = "modbus.0.holdingRegisters.40069_Batterie_Leistung"
    BATTERY_POWER_INFLUX_QUERY = 'SELECT * FROM "{}" ORDER BY time DESC LIMIT 1'.format(BATTERY_POWER_INFLUX)
    HOME_POWER_INFLUX = "modbus.0.holdingRegisters.40071_Hausverbrauch_Leistung"
    HOME_POWER_INFLUX_QUERY = 'SELECT * FROM "{}" ORDER BY time DESC LIMIT 1'.format(HOME_POWER_INFLUX)