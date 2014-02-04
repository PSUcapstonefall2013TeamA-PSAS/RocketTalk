#!/usr/bin/python
import RocketPacket
import OpenRocketInterface as API
from MathematicalFunctions import Maths
import RocketPacket as ADIS
 
def RocketLoop(orkFile, sim_index=None, host=None):
    adis = ADIS.RocketPacket(host)
    OpenRocket = API.OpenRocketInterface()
    OpenRocket.getDeploymentVelocity()
    if sim_index != None:
        OpenRocket.LoadRocketSpecific(orkFile, sim_index)
    else:
        OpenRocket.LoadRocket(orkFile)
    OpenRocket.RunSimulation()
    OpenRocket.StartSimulation()
    while OpenRocket.IsSimulationStagesRunning():
        while OpenRocket.IsSimulationLoopRunning():
            iteration = OpenRocket.SimulationStep()
            timestep = OpenRocket.GetTimeStep()
            flightDataStep = OpenRocket.GetFlightDataStep()
            #Just looking at some values here.
            v_tt  = OpenRocket.GetValue(flightDataStep,'TYPE_TIME')
            v_Aax = OpenRocket.GetValue(flightDataStep,'TYPE_ACCELERATION_ANGULAR_X')
            v_Aay = OpenRocket.GetValue(flightDataStep,'TYPE_ACCELERATION_ANGULAR_Y')
            v_Aaz = OpenRocket.GetValue(flightDataStep,'TYPE_ACCELERATION_ANGULAR_Z')

            #This may well be the right way to get accel, i just wanted
            #To play with the new stuff.                
            oldvelocity = OpenRocket.GetVelocity()
            velocity = OpenRocket.GetVelocity()
            accel = Maths.VelocityToAccel(oldvelocity, velocity, timestep)
            p = [0]*12
            # Gyro
            p[1] = OpenRocket.GetValue(flightDataStep,'TYPE_POSITION_X')
            p[2] = OpenRocket.GetValue(flightDataStep,'TYPE_POSITION_Y')
            p[3] = OpenRocket.GetValue(flightDataStep,'TYPE_POSITION_Z')
            # acceleration x,y,z
            p[4] = OpenRocket.GetValue(flightDataStep,'TYPE_ACCELERATION_LINEAR_X')
            p[5] = OpenRocket.GetValue(flightDataStep,'TYPE_ACCELERATION_LINEAR_Y')
            p[6] = OpenRocket.GetValue(flightDataStep,'TYPE_ACCELERATION_LINEAR_Z')
            adis.send_message(p)
        OpenRocket.StagesStep()
    print "DONE!"   
