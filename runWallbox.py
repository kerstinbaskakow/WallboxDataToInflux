#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 20:24:30 2021

@author: kerstin
"""

import setWallboxChargeMode
import readWallboxValues
import time

def runWallboxSchedule():
    readWallboxValues.readWallboxValuesMain()
    print("read value")
    time.sleep(1)
    setWallboxChargeMode.setWallboxChargeModeMain()
    print("set value")

if __name__ == "__main__":
    runWallboxSchedule()