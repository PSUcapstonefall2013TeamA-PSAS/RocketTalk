#!/usr/bin/python
import jpype
from config import JAR_PATH as classpath
from config import JVM as jvm
try:
   fh = open(classpath)
except IOError, ex:
   print "Caught the IOError:\n    ", ex
   print "Verify the path to openrocket.jar in config.py"
   quit()
try:
   fh = open(jvm)
except IOError, ex:
   print "Caught the IOError:\n    ", ex
   print "Verify the path to the jvm in config.py"
   quit()

class OpenRocketInterface(object):
    def __init__(self):
        jpype.startJVM(jvm, "-Djava.class.path=%s" % classpath)
        SwingStartup = jpype.JClass('net.sf.openrocket.startup.SwingStartup') 
        SwingStartup.initializeLogging()

#        package = jpype.JPackage('net').sf.openrocket.startup
#        OpenRocketAPI = package.OpenRocketAPI
        openRocketAPIClass = 'net.sf.openrocket.startup.OpenRocketAPI'
        try:
            OpenRocketAPI = jpype.JClass(openRocketAPIClass)
        except jpype.JavaException, ex:
            if ex.message() == "Class " + openRocketAPIClass + " not found":
                print "Caught the runtime exception:\n     ", ex.message()
                print "Ensure that you are using a version of OpenRocket with this class"
            else:
                print "Caught the runtime exception:\n     ", ex.message()
            quit()
        self.apiInstance = OpenRocketAPI()
    def GetTimeStep(self):
        return self.apiInstance.GetTimeStep()
    def cleanup(self):
        jpype.shutdownJVM()
        
    def GetVelocityX(self):
        return self.apiInstance.GetVelocityX()	#returns int

    def GetVelocityY(self):
        return self.apiInstance.GetVelocityY() #returns int

    def GetVelocityZ(self):
        return self.apiInstance.GetVelocityZ() #returns int

    def IsSimulationRunning(self):
        return self.apiInstance.IsSimulationRunning() #returns bool

    def StartSimulation(self):
        return self.apiInstance.StartSimulation() #returns int

    def SimulationStep(self):
        return self.apiInstance.SimulationStep() #returns int

    def SimulationStep(self, timestep): #takes in a double
        return self.apiInstance.SimulationStep(timestep) #returns int

    def LoadRocket(self, szFileName): #takes in a string
        return self.apiInstance.LoadRocket(szFileName) #returns int

    def RunSimulation(self):
        self.apiInstance.RunSimulation()

    def getMaxAltitude(self):
        return self.apiInstance.getMaxAltitude() #returns double

    def getMaxVelocity(self):
        return self.apiInstance.getMaxVelocity() #returns double

    def getMaxAcceleration(self):
        return self.apiInstance.getMaxAcceleration() #returns double

    def getMaxMachNumber(self):
        return self.apiInstance.getMaxMachNumber() #returns double

    def getTimeToApogee(self):
        return self.apiInstance.getTimeToApogee() #returns double

    def getFlightTime(self):
        return self.apiInstance.getFlightTime() #returns double

    def getGroundHitVelocity(self):
        return self.apiInstance.getGroundHitVelocity() #returns double

    def getLaunchRodVelocity(self):
        return self.apiInstance.getLaunchRodVelocity() #returns double

    def getDeploymentVelocity(self):
        return self.apiInstance.getDeploymentVelocity() #returns double
