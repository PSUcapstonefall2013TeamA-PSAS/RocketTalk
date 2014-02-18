#!/usr/bin/python
import OpenRocketInterface as API
import RocketPacket as ADIS
import time


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
            x = OpenRocket.GetValue(flightDataStep,'TYPE_ACCELERATION_LINEAR_X')
            y = OpenRocket.GetValue(flightDataStep,'TYPE_ACCELERATION_LINEAR_Y')
            z = OpenRocket.GetValue(flightDataStep,'TYPE_ACCELERATION_LINEAR_Z')
            vec = [x,y,z]
            #transform with the identity matrix.
            idMatrix = [[0,0,1],[0,1,0],[1,0,0]]
            newX = vec[0] * idMatrix[0][0] + vec[1] * idMatrix[0][1] + vec[2] * idMatrix[0][2]
            newY = vec[0] * idMatrix[1][0] + vec[1] * idMatrix[1][1] + vec[2] * idMatrix[1][2]
            newZ = vec[0] * idMatrix[2][0] + vec[1] * idMatrix[2][1] + vec[2] * idMatrix[2][2]            
            
            p[4] = newX
            p[5] = newY
            p[6] = newZ
            
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
    p[4] = OpenRocket.GetValue('TYPE_ACCELERATION_LINEAR_X')
    p[5] = OpenRocket.GetValue('TYPE_ACCELERATION_LINEAR_Y')
    p[6] = OpenRocket.GetValue('TYPE_ACCELERATION_LINEAR_Z') + OpenRocket.GetValue('TYPE_GRAVITY')
    

    return p
