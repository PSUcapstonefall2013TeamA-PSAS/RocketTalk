#!/usr/bin/python
import OpenRocketInterface as API
import RocketPacket as ADIS
import time
import numpy as np
import math
from config import SLEEP_THRESHOLD
try:
    from config import sensor_matrix
    from config import csv_output
    from config import log_file
except:
    print 'Not configured.\n'
    print 'Copy config.py_dist to config.py and fill in your settings\n'
    print 'Set sensor_matrix to a 3x3 rotation matrix for'
    print 'Rocket coordinates to sensor coordinates'
    print 'defaulting to identity matrix'
    sensor_matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]


#Main simulation loop
def RocketLoop(orkFile, sim_index=1, host=None, time_step='default',
               random_seed=0.0, csv=False):

    adis = ADIS.RocketPacket(host)
    OpenRocket = API.OpenRocketInterface()
    OpenRocket.SetLogFile(log_file)
    OpenRocket.SimulationSetup(orkFile, sim_index, random_seed)

    print "Starting simulation"

    if time_step == 'none':
        OpenRocket.SimulationRun()
        print "Stepless RocketLoop DONE!"

    elif time_step == 'default':  # Step through simulation as fast as possible
        OpenRocket.SimulationStep(1)
        while OpenRocket.SimulationIsRunning():
            p = GetData(OpenRocket)

            adis.send_message(p)

            OpenRocket.SimulationStep(1)
        print "Instant stepping RocketLoop DONE!"

    elif time_step == 'realtime':  # Step through simulation in realtime
        actualTime = time.time()
        simTime = 0
        sleepTime = 0

        OpenRocket.SimulationStep(1)
        while OpenRocket.SimulationIsRunning():
            stepTimer = OpenRocket.GetValue('TYPE_TIME_STEP') + time.time()
            simTime = OpenRocket.GetSimulationRunningTime()
            p = GetData(OpenRocket)

            sleepTime = sleepTime + stepTimer - time.time()
            # Sleep when we get ahead more than SLEEP_THRESHOLD seconds
            if sleepTime > SLEEP_THRESHOLD:
                time.sleep(sleepTime)
                sleepTime = 0

            adis.send_message(p)
            OpenRocket.SimulationStep(1)

        actualTime = time.time() - actualTime
        print "Realtime RocketLoop DONE!"
        print "Simulation Time: ", simTime
        print "Actual Time: ", actualTime

    if csv:
        OpenRocket.FullCSVOut(csv_output)


#Gets simulation data and sets up packet for sending
def GetData(OpenRocket):

    p = [0]*12

    try:
        # Gyro
        p[1] = OpenRocket.GetValue('TYPE_PITCH_RATE')
        p[2] = OpenRocket.GetValue('TYPE_YAW_RATE')
        p[3] = OpenRocket.GetValue('TYPE_ROLL_RATE')
    except:
        pass

    # Acceleration x,y,z
    try:
        x = OpenRocket.GetValue('TYPE_ACCELERATION_X')
        y = OpenRocket.GetValue('TYPE_ACCELERATION_Y')
        z = OpenRocket.GetValue('TYPE_ACCELERATION_Z') + OpenRocket.GetValue('TYPE_GRAVITY')
    except:
        x = y = z = 0
    accel = np.array([x, y, z])

    try:
        #sine of zenith offset
        sphi = math.sin(OpenRocket.GetValue('TYPE_ORIENTATION_PHI'))
        #sine of azimuth
        sthe = math.sin(OpenRocket.GetValue('TYPE_ORIENTATION_THETA'))
        #sine of roll
        spsi = math.sin(0)

        #cosine of zenith offset
        cphi = math.cos(OpenRocket.GetValue('TYPE_ORIENTATION_PHI'))
        #cosine of azimuth
        cthe = math.cos(OpenRocket.GetValue('TYPE_ORIENTATION_THETA'))
        #cosine of roll
        cpsi = math.cos(0)

        #the Eulerian transformation matrix for world to body coordinate systems
        rotWorldtoBody = np.array([[cpsi*cphi-cthe*sphi*spsi, cpsi*sphi+cthe*cphi*spsi, spsi*sthe],
                                   [-spsi*cphi-cthe*sphi*cpsi, -spsi*sphi+cthe*cphi*cpsi, cpsi*sthe],
                                   [sthe*sphi, -sthe*cphi, cthe]])

        body_accel = np.dot(accel, rotWorldtoBody)
    except:
        body_accel = accel
    offset_body_accel = np.dot(body_accel, np.array(sensor_matrix))

    p[4] = offset_body_accel[0]
    p[5] = offset_body_accel[1]
    p[6] = offset_body_accel[2]

    return p
