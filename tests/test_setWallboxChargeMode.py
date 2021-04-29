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
from chargeApp.utils import writeDataToInflux,queryDataFromInflux

meas = "TestValues"
value= np.random.randint(0,10000)
query= 'SELECT * FROM "{}" ORDER BY time DESC LIMIT 1'.format(meas)


class TestSetWallboxChargeMode(unittest.TestCase):
    
    def test_writeDataToInflux(self):        
        result = writeDataToInflux(value,meas)
        self.assertTrue(result)
        
    def test_queryDataFromInflux(self):
        result = queryDataFromInflux(query,meas)
        self.assertEqual(result,value)
