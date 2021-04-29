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

from chargeApp import influxclient
from chargeApp.utils import writeDataToInflux

#generate dummy values
resultTarget = []
for phase in range(1,4,1):
    values= np.random.randint(2, size=1)
    meas = "L{}_Current_A".format(phase)
    for value in values:
        resultTarget.append(value)
        writeDataToInflux(int(value*230),meas)

from chargeApp.phaseDetection import findActivePhases


class TestPhaseDetection(unittest.TestCase):
    
    def test_findActivePhases(self):        
        for i in range(100):
            result = findActivePhases()
            self.assertEqual(result,resultTarget)
        for phase in range(1,4,1):      
            meas = "L{}_Current_A".format(phase)
            influxclient.query("DELETE from {}".format(meas))
        
