#!/usr/bin/python
try:
    import jpype
except:
    print 'Jpype is required to use the OpenRocketInterface class'
    print 'Install Jpype using the command:'
    print '  aptitude install python-jpype\n'

try:
    from config import JAR_PATH as classpath
    from config import JVM as jvm
except:
    print 'Not configured.\n'
    print 'Copy config.py_dist to config.py and fill in your settings\n'
    quit()
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
        # openrocket.simulation.FlightDataType depends on resources.I10n.messages.properties
        flightdatatype = jpype.JPackage('net.sf.openrocket.simulation').FlightDataType
        self.type_dic = {
            'TYPE_TIME': flightdatatype.TYPE_TIME,
            'TYPE_ALTITUDE': flightdatatype.TYPE_ALTITUDE,
            'TYPE_VELOCITY_Z': flightdatatype.TYPE_VELOCITY_Z,
            'TYPE_ACCELERATION_Z': flightdatatype.TYPE_ACCELERATION_Z,
            'TYPE_VELOCITY_TOTAL': flightdatatype.TYPE_VELOCITY_TOTAL,
            'TYPE_ACCELERATION_TOTAL': flightdatatype.TYPE_ACCELERATION_TOTAL,
            'TYPE_ACCELERATION_LINEAR_X': flightdatatype.TYPE_ACCELERATION_LINEAR_X,
            'TYPE_ACCELERATION_LINEAR_Y': flightdatatype.TYPE_ACCELERATION_LINEAR_Y,
            'TYPE_ACCELERATION_LINEAR_Z': flightdatatype.TYPE_ACCELERATION_LINEAR_Z,
            'TYPE_ACCELERATION_ANGULAR_X': flightdatatype.TYPE_ACCELERATION_ANGULAR_X,
            'TYPE_ACCELERATION_ANGULAR_Y': flightdatatype.TYPE_ACCELERATION_ANGULAR_Y,
            'TYPE_ACCELERATION_ANGULAR_Z': flightdatatype.TYPE_ACCELERATION_ANGULAR_Z,
            'TYPE_POSITION_Z': flightdatatype.TYPE_POSITION_Z,
            'TYPE_POSITION_X': flightdatatype.TYPE_POSITION_X,
            'TYPE_POSITION_Y': flightdatatype.TYPE_POSITION_Y,
            'TYPE_POSITION_XY': flightdatatype.TYPE_POSITION_XY,
            'TYPE_POSITION_DIRECTION': flightdatatype.TYPE_POSITION_DIRECTION,
            'TYPE_VELOCITY_X': flightdatatype.TYPE_VELOCITY_X,
            'TYPE_VELOCITY_Y': flightdatatype.TYPE_VELOCITY_Y,
            'TYPE_VELOCITY_XY': flightdatatype.TYPE_VELOCITY_XY,
            'TYPE_ACCELERATION_XY': flightdatatype.TYPE_ACCELERATION_XY,
            'TYPE_LATITUDE': flightdatatype.TYPE_LATITUDE,
            'TYPE_LONGITUDE': flightdatatype.TYPE_LONGITUDE,
            'TYPE_GRAVITY': flightdatatype.TYPE_GRAVITY,
            'TYPE_AOA': flightdatatype.TYPE_AOA,
            'TYPE_ROLL_RATE': flightdatatype.TYPE_ROLL_RATE,
            'TYPE_PITCH_RATE': flightdatatype.TYPE_PITCH_RATE,
            'TYPE_YAW_RATE': flightdatatype.TYPE_YAW_RATE,
            'TYPE_MASS': flightdatatype.TYPE_MASS,
            'TYPE_PROPELLANT_MASS': flightdatatype.TYPE_PROPELLANT_MASS,
            'TYPE_LONGITUDINAL_INERTIA': flightdatatype.TYPE_LONGITUDINAL_INERTIA,
            'TYPE_ROTATIONAL_INERTIA': flightdatatype.TYPE_ROTATIONAL_INERTIA,
            'TYPE_CP_LOCATION': flightdatatype.TYPE_CP_LOCATION,
            'TYPE_CG_LOCATION': flightdatatype.TYPE_CG_LOCATION,
            'TYPE_STABILITY': flightdatatype.TYPE_STABILITY,
            'TYPE_MACH_NUMBER': flightdatatype.TYPE_MACH_NUMBER,
            'TYPE_REYNOLDS_NUMBER': flightdatatype.TYPE_REYNOLDS_NUMBER,
            'TYPE_THRUST_FORCE': flightdatatype.TYPE_THRUST_FORCE,
            'TYPE_DRAG_FORCE': flightdatatype.TYPE_DRAG_FORCE,
            'TYPE_DRAG_COEFF': flightdatatype.TYPE_DRAG_COEFF,
            'TYPE_AXIAL_DRAG_COEFF': flightdatatype.TYPE_AXIAL_DRAG_COEFF,
            'TYPE_FRICTION_DRAG_COEFF': flightdatatype.TYPE_FRICTION_DRAG_COEFF,
            'TYPE_PRESSURE_DRAG_COEFF': flightdatatype.TYPE_PRESSURE_DRAG_COEFF,
            'TYPE_BASE_DRAG_COEFF': flightdatatype.TYPE_BASE_DRAG_COEFF,
            'TYPE_NORMAL_FORCE_COEFF': flightdatatype.TYPE_NORMAL_FORCE_COEFF,
            'TYPE_PITCH_MOMENT_COEFF': flightdatatype.TYPE_PITCH_MOMENT_COEFF,
            'TYPE_YAW_MOMENT_COEFF': flightdatatype.TYPE_YAW_MOMENT_COEFF,
            'TYPE_SIDE_FORCE_COEFF': flightdatatype.TYPE_SIDE_FORCE_COEFF,
            'TYPE_ROLL_MOMENT_COEFF': flightdatatype.TYPE_ROLL_MOMENT_COEFF,
            'TYPE_ROLL_FORCING_COEFF': flightdatatype.TYPE_ROLL_FORCING_COEFF,
            'TYPE_ROLL_DAMPING_COEFF': flightdatatype.TYPE_ROLL_DAMPING_COEFF,
            'TYPE_PITCH_DAMPING_MOMENT_COEFF': flightdatatype.TYPE_PITCH_DAMPING_MOMENT_COEFF,
            'TYPE_YAW_DAMPING_MOMENT_COEFF': flightdatatype.TYPE_YAW_DAMPING_MOMENT_COEFF,
            'TYPE_CORIOLIS_ACCELERATION': flightdatatype.TYPE_CORIOLIS_ACCELERATION,
            'TYPE_CORIOLIS_ACCELERATION_X': flightdatatype.TYPE_CORIOLIS_ACCELERATION_X,
            'TYPE_CORIOLIS_ACCELERATION_Y': flightdatatype.TYPE_CORIOLIS_ACCELERATION_Y,
            'TYPE_CORIOLIS_ACCELERATION_Z': flightdatatype.TYPE_CORIOLIS_ACCELERATION_Z,
            'TYPE_REFERENCE_LENGTH': flightdatatype.TYPE_REFERENCE_LENGTH,
            'TYPE_REFERENCE_AREA': flightdatatype.TYPE_REFERENCE_AREA,
            'TYPE_ORIENTATION_THETA': flightdatatype.TYPE_ORIENTATION_THETA,
            'TYPE_ORIENTATION_PHI': flightdatatype.TYPE_ORIENTATION_PHI,
            'TYPE_WIND_VELOCITY': flightdatatype.TYPE_WIND_VELOCITY,
            'TYPE_AIR_TEMPERATURE': flightdatatype.TYPE_AIR_TEMPERATURE,
            'TYPE_AIR_PRESSURE': flightdatatype.TYPE_AIR_PRESSURE,
            'TYPE_SPEED_OF_SOUND': flightdatatype.TYPE_SPEED_OF_SOUND,
            'TYPE_TIME_STEP': flightdatatype.TYPE_TIME_STEP,
            'TYPE_COMPUTATION_TIME': flightdatatype.TYPE_COMPUTATION_TIME
        }

    def cleanup(self):
        jpype.shutdownJVM()

    def setlogfile(self, filename):  # takes in string
        return self.apiInstance.setlogfile(filename)  # returns int

    def GetFlightData(self):
        flightDataBranch = self.apiInstance.GetFlightData()
        return flightDataBranch

    def GetFlightDataStep(self):
        flightDataStep = self.apiInstance.GetFlightDataStep()
        return flightDataStep

    def GetTimeStep(self):
        return self.apiInstance.GetTimeStep()

    def GetItteration(self):
        return self.apiInstance.GetItteration()

    def GetValue(self, d_type):
        '''
        These values correlated to the types found in
        openrocket.simulation.FlightDataType

        @param d_type           string matching a flightdatatype.
        '''

        TYPE = self.type_dic.get(d_type)
        value = self.apiInstance.GetValue(TYPE)
        return value

    def SetValue(self, d_type, value):
        '''
        These values correlated to the types found in
        openrocket.simulation.FlightDataType

        @param d_type           string matching a flightdatatype.
        @param value            the value to be assigned
        '''

        TYPE = self.type_dic.get(d_type)
        value = self.apiInstance.SetValue(TYPE, value)

    def SetMinTimeStep(self, timestep):
        self.apiInstance.SetMinTimeStep(timestep)

    def GetVelocity(self):
        return (self.GetVelocityX(), self.GetVelocityY(), self.GetVelocityZ())

    def GetVelocityX(self):
        return self.apiInstance.GetVelocityX()  # returns int

    def GetVelocityY(self):
        return self.apiInstance.GetVelocityY()  # returns int

    def GetVelocityZ(self):
        return self.apiInstance.GetVelocityZ()  # returns int

    def GetCordinateX(self):
        return self.apiInstance.GetCordinateX()  # returns int

    def GetCordinateY(self):
        return self.apiInstance.GetCordinateY()  # returns int

    def GetCordinateZ(self):
        return self.apiInstance.GetCordinateZ()  # returns int

    def GetVelocityRotationX(self):
        return self.apiInstance.GetVelocityRotationX()  # returns int

    def GetVelocityRotationY(self):
        return self.apiInstance.GetVelocityRotationY()  # returns int

    def GetVelocityRotationZ(self):
        return self.apiInstance.GetVelocityRotationZ()  # returns int

    def GetSimulationRunningTime(self):
        return self.apiInstance.Getsimulationrunningtime()  # returns double

    def GetBoolTumbling(self):
        return self.apiInstance.GetBoolTumbling()  # returns bool

    def GetBoolMotorIgnited(self):
        return self.apiInstance.GetBoolMotorIgnited()  # return bool

    def GetBoolApogeeReached(self):
        return self.apiInstance.GetBoolApogeeReached()  # return bool

    def GetBoolLaunchRodCleared(self):
        return self.apiInstance.GetBoolLaunchRodCleared()  # return bool

    def GetBoolLiftOff(self):
        return self.apiInstance.GetBoolLiftoff()  # return bool

    def IsSimulationRunning(self):
        return self.apiInstance.IsSimulationRunning()  # returns bool

    def StartSimulation(self):
        return self.apiInstance.StartSimulation()  # returns int

    def SimulationStep(self):
        return self.apiInstance.SimulationStep()  # returns int

    def LoadRocket(self, szFileName):  # takes in a string
        self.LoadRocketSpecific(szFileName, 1)

    def LoadRocketSpecific(self, szFileName, simtograb):  # takes in a string and int
        errorCode = self.apiInstance.LoadRocket(szFileName, simtograb)
        if (errorCode == -1):
            print "Oops! No simulations available in this file."
            quit()
        elif (errorCode == -2):
            print "Woops! You asked for a simulation not present in this file."
            quit()
        elif (errorCode == -3):
            print "Uh Oh! Simulation data is not present in this simulation."
            quit()
        elif (errorCode == -4):
            print "Oh No! Java RocketLoadException thrown"
            quit()
        else:
            print "Successfully loaded rocket simulation data!!!"

    def RunSimulation(self):
        self.apiInstance.RunSimulation()

    def getMaxAltitude(self):
        return self.apiInstance.getMaxAltitude()  # returns double

    def getMaxVelocity(self):
        return self.apiInstance.getMaxVelocity()  # returns double

    def getMaxAcceleration(self):
        return self.apiInstance.getMaxAcceleration()  # returns double

    def getMaxMachNumber(self):
        return self.apiInstance.getMaxMachNumber()  # returns double

    def getTimeToApogee(self):
        return self.apiInstance.getTimeToApogee()  # returns double

    def getFlightTime(self):
        return self.apiInstance.getFlightTime()  # returns double

    def getGroundHitVelocity(self):
        return self.apiInstance.getGroundHitVelocity()  # returns double

    def getLaunchRodVelocity(self):
        return self.apiInstance.getLaunchRodVelocity()  # returns double

    def getDeploymentVelocity(self):
        return self.apiInstance.getDeploymentVelocity()  # returns double

    def IsSimulationStagesRunning(self):
        return self.apiInstance.IsSimulationStagesRunning()  # returns bool

    def IsSimulationLoopRunning(self):
        return self.apiInstance.IsSimulationLoopRunning()  # returns int

    def StagesStep(self):
        return self.apiInstance.StagesStep()  # return int
