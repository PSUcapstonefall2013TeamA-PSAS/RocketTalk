#!/usr/bin/python
import jpype
from config import JAR_PATH as classpath
from config import JVM as jvm
class OpenRocketInterface(object):
    def __init__(self):
        jpype.startJVM(jvm, "-Djava.class.path=%s" % classpath)
        package = jpype.JPackage('net').sf.openrocket.startup
        OpenRocketAPI = package.OpenRocketAPI
        self.apiInstance = OpenRocketAPI()
    def cleanup(self):
        jpype.shutdownJVM()

    def getDeploymentVelocity(self):
	self.apiInstance.LoadRocket('/home/annajoel/foo.ork')
	self.apiInstance.RunSimulation()
	print self.apiInstance.getDeploymentVelocity()
