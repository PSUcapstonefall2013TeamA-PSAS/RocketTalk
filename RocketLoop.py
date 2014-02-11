#!/usr/bin/python
import OpenRocketInterface as API
import RocketPacket as ADIS
import time


def RocketLoop(orkFile, sim_index=None, host=None, time_step='default'):
    adis = ADIS.RocketPacket(host)
    OpenRocket = API.OpenRocketInterface()
    OpenRocket.getDeploymentVelocity()
    if sim_index is not None:
        OpenRocket.LoadRocketSpecific(orkFile, sim_index)
    else:
        OpenRocket.LoadRocket(orkFile)
    OpenRocket.RunSimulation()
    OpenRocket.StartSimulation()

    print "Starting Simulation"
    if time_step == 'default':
        while OpenRocket.IsSimulationStagesRunning():
            while OpenRocket.IsSimulationLoopRunning():
                flightDataStep = OpenRocket.GetFlightDataStep()
                iteration = OpenRocket.SimulationStep()

                #Just looking at some values here.
                v_tt = OpenRocket.GetValue(flightDataStep, 'TYPE_TIME')
                v_Aax = OpenRocket.GetValue(flightDataStep, 'TYPE_ACCELERATION_ANGULAR_X')
                v_Aay = OpenRocket.GetValue(flightDataStep, 'TYPE_ACCELERATION_ANGULAR_Y')
                v_Aaz = OpenRocket.GetValue(flightDataStep, 'TYPE_ACCELERATION_ANGULAR_Z')

                #This may well be the right way to get accel, i just wanted
                #To play with the new stuff.
                # oldvelocity = OpenRocket.GetVelocity()
                # velocity = OpenRocket.GetVelocity()
                # accel = Maths.VelocityToAccel(oldvelocity, velocity, timestep)

                p = [0]*12
                # Gyro
                p[1] = OpenRocket.GetValue(flightDataStep, 'TYPE_POSITION_X')
                p[2] = OpenRocket.GetValue(flightDataStep, 'TYPE_POSITION_Y')
                p[3] = OpenRocket.GetValue(flightDataStep, 'TYPE_POSITION_Z')
                # acceleration x,y,z
                p[4] = OpenRocket.GetValue(flightDataStep, 'TYPE_ACCELERATION_LINEAR_X')
                p[5] = OpenRocket.GetValue(flightDataStep, 'TYPE_ACCELERATION_LINEAR_Y')
                p[6] = OpenRocket.GetValue(flightDataStep, 'TYPE_ACCELERATION_LINEAR_Z')
                adis.send_message(p)
            OpenRocket.StagesStep()
        print "DONE!"

    elif time_step == 'realtime':
        actualTime = time.time()
        simTime = 0
        sleepTime = 0

        OpenRocket.SetMinTimeStep(0.05)

        while OpenRocket.IsSimulationStagesRunning():
            while OpenRocket.IsSimulationLoopRunning():
                stepTimer = OpenRocket.GetTimeStep() + time.time()
                simTime = OpenRocket.GetSimulationRunningTime()

                flightDataStep = OpenRocket.GetFlightDataStep()
                iteration = OpenRocket.SimulationStep()
                #Just looking at some values here.
                v_tt = OpenRocket.GetValue(flightDataStep, 'TYPE_TIME')
                v_Aax = OpenRocket.GetValue(flightDataStep, 'TYPE_ACCELERATION_ANGULAR_X')
                v_Aay = OpenRocket.GetValue(flightDataStep, 'TYPE_ACCELERATION_ANGULAR_Y')
                v_Aaz = OpenRocket.GetValue(flightDataStep, 'TYPE_ACCELERATION_ANGULAR_Z')

                #This may well be the right way to get accel, i just wanted
                #To play with the new stuff.
                # oldvelocity = OpenRocket.GetVelocity()
                # velocity = OpenRocket.GetVelocity()
                # accel = Maths.VelocityToAccel(oldvelocity, velocity, timestep)

                p = [0]*12
                # Gyro
                p[1] = OpenRocket.GetValue(flightDataStep, 'TYPE_POSITION_X')
                p[2] = OpenRocket.GetValue(flightDataStep, 'TYPE_POSITION_Y')
                p[3] = OpenRocket.GetValue(flightDataStep, 'TYPE_POSITION_Z')
               # acceleration x,y,z
                p[4] = OpenRocket.GetValue(flightDataStep, 'TYPE_ACCELERATION_LINEAR_X')
                p[5] = OpenRocket.GetValue(flightDataStep, 'TYPE_ACCELERATION_LINEAR_Y')
                p[6] = OpenRocket.GetValue(flightDataStep, 'TYPE_ACCELERATION_LINEAR_Z')

                sleepTime = sleepTime + stepTimer - time.time()
                if sleepTime > 0.25:
                    time.sleep(sleepTime)
                    sleepTime = 0

                adis.send_message(p)

            OpenRocket.StagesStep()

        actualTime = time.time() - actualTime
        print "DONE!"
        print "Simulation Time: ", simTime
        print "Actual Time: ", actualTime
