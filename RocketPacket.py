import socket
import struct
import math
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

RAD2DEG = 180/math.pi
MSS2GEE = 1.0/9.81

ADIS_Message = struct.Struct('!12h')


def CLAMPR(value):
    return CLAMP(value, "Roll")


def CLAMPA(value):
    return CLAMP(value, "Acceleration")


def CLAMP(value, msg):
    return clamp(msg, value, -32768, 32767)


def clamp(msg, value, minV, maxV):
    if value < minV:
        print msg, value
        return minV
    if value > maxV:
        print msg, value
        return maxV
    return value


class RocketPacket(object):

    def __init__(self, ip):
        # Open socket and bind to address
        if ip is None:
            ip = config.FC_IP

        self.ADISsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ADISsocket.bind((ip, config.ADIS_TX_PORT))

    def send_message(self, p):

        for i in range(0, 11):
            if math.isnan(p[i]):
                p[i] = 0
        p[1] = CLAMPR(int(((p[0])*RAD2DEG)/.05))
        p[2] = CLAMPR(int(((p[1])*RAD2DEG)/.05))
        p[3] = CLAMPR(int(((p[2])*RAD2DEG)/.05))

        p[4] = CLAMPA(int((p[4]*MSS2GEE)/0.00333))
        p[5] = CLAMPA(int((p[5]*MSS2GEE)/0.00333))
        p[6] = CLAMPA(int((p[6]*MSS2GEE)/0.00333))

        packet = ADIS_Message.pack(*p)

        self.ADISsocket.sendto(packet, (config.FC_IP, config.FC_LISTEN_PORT))
