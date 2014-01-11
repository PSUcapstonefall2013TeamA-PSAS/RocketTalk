#!/usr/bin/env python
# -*- coding: UTF-8 -*-
### Send data to test RocketPacket ###

import RocketPacket as ADIS
import time
import subprocess
from random import gauss 

adis = ADIS.RocketPacket()

p = [0]*12

# Power
p[0] = int(gauss(5.0,0.1)/0.002418)
# Gryo
p[1] = int(gauss(0,0.1)/0.05)
p[2] = int(gauss(0,0.1)/0.05)
p[3] = int(gauss(0,0.1)/0.05)
# accel
p[4] = int(gauss(0.98,0.03)/0.00333)
p[5] = int(gauss(0,0.03)/0.00333)
p[6] = int(gauss(0,0.03)/0.00333)
# mag
p[7] = 0
p[8] = 0
p[9] = 0
# temp
p[10] = 0
# spare ADC
p[11] = 0

av3fc = subprocess.Popen({"./../av3-fc/fc"})
telemetry = subprocess.Popen({"./../telemetry/telemetry.py"})

while True:
    try:
        p[10] += 1000
        adis.send_message(p)
        time.sleep(2)
    except KeyboardInterrupt:
        print "\nKilling Processes..."
        av3fc.terminate();
        telemetry.terminate();
        
        while av3fc.poll() == None or telemetry.poll() == None:
            time.sleep(1)
        
        exit();

