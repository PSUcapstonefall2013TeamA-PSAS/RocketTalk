#!/usr/bin/python
import jpype

class OpenRocketInterface(object):
    def __init__(self):
        classpath = "home/annajoel/openrocket.git/core/bin"
        jvm = "/usr/lib/jvm/jdk-7-oracle-x64/jre/lib/amd64/server/libjvm.so"
        jpype.startJVM(jvm)#, "-Djava.class.path=%s" % classpath)
        
        testOpenRock = jpype.JPackage('org').rocket.testexe
        OpenRocketAPI = testOpenRock.OpenRocketAPI
        self.apiInstance = OpenRocketAPI()
    def cleanup(self):
        jpype.shutdownJVM()

    def getDeploymentVelocity(self):
        print self.apiInstance.getDeploymentVelocity()
