#!/usr/bin/python
import OpenRocketInterface as API
import RocketPacket as ADIS
import time
try:
    from config import sensor_matrix
except:
    print 'Not configured.\n'
    print 'Copy config.py_dist to config.py and fill in your settings\n'
    print 'Set sensor_matrix to a 3x3 rotation matrix for'
    print 'Rocket coordinates to sensor coordinates'
    print 'defaulting to identity matrix'
    sensor_matrix = [[1,0,0],[0,1,0],[0,0,1]]

#Main simulation loop
def RocketLoop(orkFile, sim_index=None, host=None, time_step='default', random_seed=0):

    adis = ADIS.RocketPacket(host)
    OpenRocket = API.OpenRocketInterface()
    OpenRocket.SetRandomSeed(random_seed)
    if sim_index is not None:
        OpenRocket.LoadRocketSpecific(orkFile, sim_index)
    else:
        OpenRocket.LoadRocket(orkFile)
    OpenRocket.StartSimulation()

    print "Starting simulation"

    if time_step == 'default':  # Step through simulation as fast as possible
        while OpenRocket.IsSimulationStagesRunning():
            while OpenRocket.IsSimulationLoopRunning():
                p = GetData(OpenRocket)

            adis.send_message(p)
            OpenRocket.StagesStep()
        
        OpenRocket.apiInstance.printExtras()
        print "Instant stepping RocketLoop DONE!"

    elif time_step == 'realtime':  # Step through simulation in realtime
        actualTime = time.time()
        simTime = 0
        sleepTime = 0

        while OpenRocket.IsSimulationStagesRunning():
            while OpenRocket.IsSimulationLoopRunning():
                stepTimer = OpenRocket.GetValue('TYPE_TIME_STEP') + time.time()
                simTime = OpenRocket.GetSimulationRunningTime()

                p = GetData(OpenRocket)

                sleepTime = sleepTime + stepTimer - time.time()
                if sleepTime > 0.25:  # Sleep when we get ahead more than 0.25 seconds
                    time.sleep(sleepTime)
                    sleepTime = 0

                adis.send_message(p)

            OpenRocket.StagesStep()
        OpenRocket.apiInstance.printExtras()
        actualTime = time.time() - actualTime
        print "Realtime RocketLoop DONE!"
        print "Simulation Time: ", simTime
        print "Actual Time: ", actualTime


#Gets simulation data and sets up packet for sending
def GetData(OpenRocket):
    iteration = OpenRocket.SimulationStep()

    p = [0]*12
    # Gyro
    p[0] = OpenRocket.GetValue('TYPE_PITCH_RATE')
    p[1] = OpenRocket.GetValue('TYPE_YAW_RATE')
    p[2] = OpenRocket.GetValue('TYPE_ROLL_RATE')
    # Acceleration x,y,z
    x = OpenRocket.GetValue('TYPE_ACCELERATION_LINEAR_X')
    y = OpenRocket.GetValue('TYPE_ACCELERATION_LINEAR_Y')
    z = OpenRocket.GetValue('TYPE_ACCELERATION_LINEAR_Z') + OpenRocket.GetValue('TYPE_GRAVITY')
    vec = [x,y,z]
    
    newX = vec[0] * sensor_matrix[0][0] + vec[1] * sensor_matrix[0][1] + vec[2] * sensor_matrix[0][2]
    newY = vec[0] * sensor_matrix[1][0] + vec[1] * sensor_matrix[1][1] + vec[2] * sensor_matrix[1][2]
    newZ = vec[0] * sensor_matrix[2][0] + vec[1] * sensor_matrix[2][1] + vec[2] * sensor_matrix[2][2]            
    
    p[4] = newX
    p[5] = newY
    p[6] = newZ
    

    return p
