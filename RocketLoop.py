#!/usr/bin/python
import RocketPacket
import OpenRocketInterface as API
import RocketPacket as ADIS


def VelocityToAccel(oldV, newV, timestep):
    x = (newV[0] - oldV[0]) / timestep
    y = (newV[1] - oldV[1]) / timestep
    z = (newV[2] - oldV[2]) / timestep
    return (x, y, z)
    
def RocketLoop(orkFile, sim_index=None, host=None):
    adis = ADIS.RocketPacket()
    OpenRocket = API.OpenRocketInterface()
    OpenRocket.getDeploymentVelocity()
    if sim_index != None:
        OpenRocket.LoadRocket(orkFile, sim_index)
    else:
        OpenRocket.LoadRocket(orkFile)
    OpenRocket.RunSimulation()
    OpenRocket.StartSimulation()
    while OpenRocket.IsSimulationStagesRunning():
        while OpenRocket.IsSimulationLoopRunning():
            iteration = OpenRocket.SimulationStep()
            timestep = OpenRocket.GetTimeStep()
            flightDataStep = OpenRocket.GetFlightDataStep()
            value00 = OpenRocket.GetValue(flightDataStep,'TYPE_TIME')
            value01 = OpenRocket.GetValue(flightDataStep,'TYPE_ORIENTATION_THETA')
            value02 = OpenRocket.GetValue(flightDataStep,'TYPE_ORIENTATION_PHI')
            value03 = OpenRocket.GetValue(flightDataStep,'TYPE_YAW_RATE')
            value04 = OpenRocket.GetValue(flightDataStep,'TYPE_PITCH_RATE')
            value05 = OpenRocket.GetValue(flightDataStep,'TYPE_ROLL_RATE')
            value06 = OpenRocket.GetValue(flightDataStep,'TYPE_AOA')
            value07 = OpenRocket.GetValue(flightDataStep,'TYPE_ACCELERATION_XY')
            value08 = OpenRocket.GetValue(flightDataStep,'TYPE_ACCELERATION_Z')
            value09 = OpenRocket.GetValue(flightDataStep,'TYPE_VELOCITY_Z')
            value10 = OpenRocket.GetValue(flightDataStep,'TYPE_VELOCITY_XY')
            i =0
            i = i + 1
            #types = flightDataStep.getTypes()
            #value = OpenRocket.getTotalAcceleration(flightDataStep)
            
            
#           oldvelocity = OpenRocket.GetVelocity()
#           velocity = OpenRocket.GetVelocity()
            #This may well be the right way to get accel, i just wanted
            #To play with the new stuff.
#           accel = VelocityToAccel(oldvelocity, velocity, timestep)
#           p = [0]*12
#           p[4] = accel[0]
#           p[5] = accel[1]
#           p[6] = accel[2]
#           adis.send_message(p)
        OpenRocket.StagesStep()
    print "DONE!"   
