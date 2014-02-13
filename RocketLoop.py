#!/usr/bin/python
import OpenRocketInterface as API
import RocketPacket as ADIS
import time


#Main simulation loop
def RocketLoop(orkFile, sim_index=None, host=None, time_step='default'):
    adis = ADIS.RocketPacket(host)
    OpenRocket = API.OpenRocketInterface()

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
        print "DONE!"

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

        actualTime = time.time() - actualTime
        print "DONE!"
        print "Simulation Time: ", simTime
        print "Actual Time: ", actualTime


#Gets simulation data and sets up packet for sending
def GetData(OpenRocket):
    iteration = OpenRocket.SimulationStep()

    # remove?
    #Just looking at some values here.
    # v_tt = OpenRocket.GetValue(flightDataStep, 'TYPE_TIME')
    # v_Aax = OpenRocket.GetValue(flightDataStep, 'TYPE_ACCELERATION_ANGULAR_X')
    # v_Aay = OpenRocket.GetValue(flightDataStep, 'TYPE_ACCELERATION_ANGULAR_Y')
    # v_Aaz = OpenRocket.GetValue(flightDataStep, 'TYPE_ACCELERATION_ANGULAR_Z')

    p = [0]*12
    # Gyro
    p[1] = OpenRocket.GetValue('TYPE_POSITION_X')
    p[2] = OpenRocket.GetValue('TYPE_POSITION_Y')
    p[3] = OpenRocket.GetValue('TYPE_POSITION_Z')
    # Acceleration x,y,z
    p[4] = OpenRocket.GetValue('TYPE_ACCELERATION_LINEAR_X')
    p[5] = OpenRocket.GetValue('TYPE_ACCELERATION_LINEAR_Y')
    p[6] = OpenRocket.GetValue('TYPE_ACCELERATION_LINEAR_Z')

    return p
