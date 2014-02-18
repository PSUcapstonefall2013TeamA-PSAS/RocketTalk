import socket
import struct
import time
import json
import math
from random import gauss
try:
    import config
except:
    print 'Not configured.\n'
    print 'Copy config.py_dist to config.py and fill in your settings\n'
    quit()
'''
Packet Structure:
    # Power
    p[0] = int
    # Gryo
    p[1] = int
    p[2] = int
    p[3] = int
    # accel x,y,z
    p[4] = int
    p[5] = int
    p[6] = int
    # mag
    p[7] = 0
    p[8] = 0
    p[9] = 0
    # temp
    p[10] = int(24/0.14)
    # spare ADC
    p[11] = 0
'''

RAD2DEG = 57.2957795
MSS2GEE = 1.0/9.81
ADIS_Message = struct.Struct('!12h')


class RocketPacket(object):

    def __init__(self, ip):
        # Open socket and bind to address

        if ip is None:
            ip = config.FC_IP

        self.ADISsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ADISsocket.bind((ip, config.ADIS_TX_PORT))

    def send_message(self, p, data=None):

        for i in range(0, 11):
            if math.isnan(p[i]):
                p[i] = 0
        
        p[4] = int((p[4]*MSS2GEE)/0.00333)
        p[5] = int((p[5]*MSS2GEE)/0.00333)
        p[6] = int((p[6]*MSS2GEE)/0.00333)

        p[4] = int((p[4]*MSS2GEE)/0.00333)
        p[5] = int((p[5]*MSS2GEE)/0.00333)
        p[6] = int((p[6]*MSS2GEE)/0.00333)

        packet = ADIS_Message.pack(*p)

        self.ADISsocket.sendto(packet, (config.FC_IP, config.FC_LISTEN_PORT))
