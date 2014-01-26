#!/usr/bin/python
import RocketPacket
import OpenRocketInterface as API
import RocketPacket as ADIS


def VelocityToAccel(oldV, newV, timestep):
    x = (newV[0] - oldV[0])/timestep
    y = (newV[1] - oldV[1])/timestep
    z = (newV[2] - oldV[2])/timestep
    return (x,y,z)
    
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
    timestep = OpenRocket.GetTimeStep()
    count = 1
    while OpenRocket.IsSimulationStagesRunning():
        while OpenRocket.IsSimulationLoopRunning():
            
            count  = count +1
            oldvelocity = OpenRocket.GetVelocity()
            OpenRocket.SimulationStep()
            velocity = OpenRocket.GetVelocity()
            
            accel = VelocityToAccel(oldvelocity, velocity, timestep)
            p = [0]*12
            p[4] = accel[0]
            p[5] = accel[1]
            p[6] = accel[2]
            adis.send_message(p)
        OpenRocket.StagesStep()
    print "DONE!"   
