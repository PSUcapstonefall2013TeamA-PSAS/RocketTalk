import socket
import struct
import time
import json
import config
from random import gauss

'''
Packet Structure: 
    # Power
    p[0] = int(gauss(5.0,0.1)/0.002418)
    # Gryo
    p[1] = int(gauss(0,0.1)/0.05)
    p[2] = int(gauss(0,0.1)/0.05)
    p[3] = int(gauss(0,0.1)/0.05)
    # accel x,y,z 
    p[4] = int(gauss(0.98,0.03)/0.00333)
    p[5] = int(gauss(0,0.03)/0.00333)
    p[6] = int(gauss(0,0.03)/0.00333)
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

    def __init__(self):
        # Open socket and bind to address
        self.ADISsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ADISsocket.bind(('0.0.0.0', config.ADIS_TX_PORT))

    def ADISify_acc(self, acc):
        acc = json.loads(acc)
        x = acc['acc']['x']
        y = acc['acc']['y']
        z = acc['acc']['z']

        x = int((x*MSS2GEE)/0.00333)
        y = int((y*MSS2GEE)/0.00333)
        z = int((z*MSS2GEE)/0.00333)

        return x,y,z

    def send_message(self, p, data=None):
        if data != None:
            p[4], p[5], p[6] = self.ADISify_acc(data)

        packet = ADIS_Message.pack(*p)

        self.ADISsocket.sendto(packet, (config.FC_IP, config.FC_LISTEN_PORT))
             
