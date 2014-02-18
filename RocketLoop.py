#!/usr/bin/python
import RocketPacket
import OpenRocketInterface as API
import RocketPacket as ADIS
import time
import math
from MathematicalFunctions import Maths

def VelocityToAccel(oldV, newV, timestep):
    x = (newV[0] - oldV[0])/timestep
    y = (newV[1] - oldV[1])/timestep
    z = (newV[2] - oldV[2])/timestep
    return (x,y,z)
    
def RocketLoop(orkFile, sim_index=None, host=None, time_step='default'):
    adis = ADIS.RocketPacket(host)
    count = 0
    OpenRocket = API.OpenRocketInterface()
    OpenRocket.getDeploymentVelocity()
    if sim_index != None:
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
            v_tt  = OpenRocket.GetValue(flightDataStep,'TYPE_TIME')
            v_Aax = OpenRocket.GetValue(flightDataStep,'TYPE_ACCELERATION_ANGULAR_X')
            v_Aay = OpenRocket.GetValue(flightDataStep,'TYPE_ACCELERATION_ANGULAR_Y')
            v_Aaz = OpenRocket.GetValue(flightDataStep,'TYPE_ACCELERATION_ANGULAR_Z')
            
            #This may well be the right way to get accel, i just wanted
            #To play with the new stuff.                
            # oldvelocity = OpenRocket.GetVelocity()
            # velocity = OpenRocket.GetVelocity()
            # accel = Maths.VelocityToAccel(oldvelocity, velocity, timestep)
            
            p = [0]*12
            # Gyro
            p[1] = OpenRocket.GetValue(flightDataStep,'TYPE_POSITION_X')
            p[2] = OpenRocket.GetValue(flightDataStep,'TYPE_POSITION_Y')
            p[3] = OpenRocket.GetValue(flightDataStep,'TYPE_POSITION_Z')
            # acceleration x,y,z
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
            v_tt  = OpenRocket.GetValue(flightDataStep,'TYPE_TIME')
            v_Aax = OpenRocket.GetValue(flightDataStep,'TYPE_ACCELERATION_ANGULAR_X')
            v_Aay = OpenRocket.GetValue(flightDataStep,'TYPE_ACCELERATION_ANGULAR_Y')
            v_Aaz = OpenRocket.GetValue(flightDataStep,'TYPE_ACCELERATION_ANGULAR_Z')
            
            #This may well be the right way to get accel, i just wanted
            #To play with the new stuff.                
            # oldvelocity = OpenRocket.GetVelocity()
            # velocity = OpenRocket.GetVelocity()
            # accel = Maths.VelocityToAccel(oldvelocity, velocity, timestep)
            
            p = [0]*12
            # Gyro
            p[1] = OpenRocket.GetValue(flightDataStep,'TYPE_POSITION_X')
            p[2] = OpenRocket.GetValue(flightDataStep,'TYPE_POSITION_Y')
            p[3] = OpenRocket.GetValue(flightDataStep,'TYPE_POSITION_Z')
            # acceleration x,y,z
            p[4] = OpenRocket.GetValue(flightDataStep,'TYPE_ACCELERATION_LINEAR_X')
            p[5] = OpenRocket.GetValue(flightDataStep,'TYPE_ACCELERATION_LINEAR_Y')
            p[6] = OpenRocket.GetValue(flightDataStep,'TYPE_ACCELERATION_LINEAR_Z')
            
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

