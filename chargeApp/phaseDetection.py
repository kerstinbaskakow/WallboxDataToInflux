#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 17:53:06 2021

@author: kerstin
"""
from chargeApp.config import Config
from chargeApp.utils import queryDataFromInflux

def findActivePhases():
    listOfActivePhases=[]
    for phase in range(1,4,1):
        CURRENT_INFLUX_QUERY = 'SELECT * FROM {} ORDER BY time DESC LIMIT 1'.format(Config.CURRENT_INFLUX.format(phase))
        #Lx = 1 if 5 >0 else 0
    
        Lx = 1 if queryDataFromInflux(CURRENT_INFLUX_QUERY,Config.CURRENT_INFLUX.format(phase)) >0 else 0
        listOfActivePhases.append(Lx)
    return listOfActivePhases

#print(findActivePhases())




"""
from statemachine import StateMachine, State

class PhaseDetectionMaschine(StateMachine):
    notPlugged = State('notPlugged', initial=True)
    plugged1Phase = State('plugged1Phase')
    plugged2Phase = State('plugged2Phase')
    plugged3Phase = State('plugged3Phase')

    doPlugVehicle = notPlugged.to(plugged1Phase)
    checkPhaseIs2 = plugged1Phase.to(plugged2Phase)
    checkPhaseIs3 = plugged1Phase.to(plugged3Phase)
    
    def on_doPlugVehicle(self):
        print('Plugged')

    def on_checkPhaseIs2(self):
        print('Activate 2 Phase calc')

    def on_checkPhaseIs3(self):
        print('Activate 3 Phase calc')
    
phaseDetection = PhaseDetectionMaschine()

print(phaseDetection.current_state)
print(phaseDetection.doPlugVehicle)
#traffic_light.slowdown()
#traffic_light.go()
"""