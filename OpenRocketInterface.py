#!/usr/bin/python
try:
    import jpype
except:
    print 'Jpype is required to use the OpenRocketInterface class'
    print 'Install Jpype using the command:'
    print '  aptitude install python-jpype\n'
    quit()
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

        # openrocket.simulation.FlightDataType
        # depends on resources.I10n.messages.properties
        fdt = jpype.JPackage('net.sf.openrocket.simulation').FlightDataType
        self.type_dic = {
            'TYPE_TIME': fdt.TYPE_TIME,
            'TYPE_TIME_STEP': fdt.TYPE_TIME_STEP,
            'TYPE_ALTITUDE': fdt.TYPE_ALTITUDE,
            'TYPE_VELOCITY_Z': fdt.TYPE_VELOCITY_Z,
            'TYPE_ACCELERATION_Z': fdt.TYPE_ACCELERATION_Z,
            'TYPE_VELOCITY_TOTAL': fdt.TYPE_VELOCITY_TOTAL,
            'TYPE_ACCELERATION_TOTAL': fdt.TYPE_ACCELERATION_TOTAL,
            'TYPE_POSITION_X': fdt.TYPE_POSITION_X,
            'TYPE_POSITION_Y': fdt.TYPE_POSITION_Y,
            'TYPE_POSITION_XY': fdt.TYPE_POSITION_XY,
            'TYPE_POSITION_DIRECTION': fdt.TYPE_POSITION_DIRECTION,
            'TYPE_VELOCITY_XY': fdt.TYPE_VELOCITY_XY,
            'TYPE_ACCELERATION_XY': fdt.TYPE_ACCELERATION_XY,
            'TYPE_ACCELERATION_X': fdt.TYPE_ACCELERATION_X,
            'TYPE_ACCELERATION_Y': fdt.TYPE_ACCELERATION_Y,
            'TYPE_LATITUDE': fdt.TYPE_LATITUDE,
            'TYPE_LONGITUDE': fdt.TYPE_LONGITUDE,
            'TYPE_GRAVITY': fdt.TYPE_GRAVITY,
            'TYPE_AOA': fdt.TYPE_AOA,
            'TYPE_ROLL_RATE': fdt.TYPE_ROLL_RATE,
            'TYPE_PITCH_RATE': fdt.TYPE_PITCH_RATE,
            'TYPE_YAW_RATE': fdt.TYPE_YAW_RATE,
            'TYPE_MASS': fdt.TYPE_MASS,
            'TYPE_PROPELLANT_MASS': fdt.TYPE_PROPELLANT_MASS,
            'TYPE_LONGITUDINAL_INERTIA': fdt.TYPE_LONGITUDINAL_INERTIA,
            'TYPE_ROTATIONAL_INERTIA': fdt.TYPE_ROTATIONAL_INERTIA,
            'TYPE_CP_LOCATION': fdt.TYPE_CP_LOCATION,
            'TYPE_CG_LOCATION': fdt.TYPE_CG_LOCATION,
            'TYPE_STABILITY': fdt.TYPE_STABILITY,
            'TYPE_MACH_NUMBER': fdt.TYPE_MACH_NUMBER,
            'TYPE_REYNOLDS_NUMBER': fdt.TYPE_REYNOLDS_NUMBER,
            'TYPE_THRUST_FORCE': fdt.TYPE_THRUST_FORCE,
            'TYPE_DRAG_FORCE': fdt.TYPE_DRAG_FORCE,
            'TYPE_DRAG_COEFF': fdt.TYPE_DRAG_COEFF,
            'TYPE_AXIAL_DRAG_COEFF': fdt.TYPE_AXIAL_DRAG_COEFF,
            'TYPE_FRICTION_DRAG_COEFF': fdt.TYPE_FRICTION_DRAG_COEFF,
            'TYPE_PRESSURE_DRAG_COEFF': fdt.TYPE_PRESSURE_DRAG_COEFF,
            'TYPE_BASE_DRAG_COEFF': fdt.TYPE_BASE_DRAG_COEFF,
            'TYPE_NORMAL_FORCE_COEFF': fdt.TYPE_NORMAL_FORCE_COEFF,
            'TYPE_PITCH_MOMENT_COEFF': fdt.TYPE_PITCH_MOMENT_COEFF,
            'TYPE_YAW_MOMENT_COEFF': fdt.TYPE_YAW_MOMENT_COEFF,
            'TYPE_SIDE_FORCE_COEFF': fdt.TYPE_SIDE_FORCE_COEFF,
            'TYPE_ROLL_MOMENT_COEFF': fdt.TYPE_ROLL_MOMENT_COEFF,
            'TYPE_ROLL_FORCING_COEFF': fdt.TYPE_ROLL_FORCING_COEFF,
            'TYPE_ROLL_DAMPING_COEFF': fdt.TYPE_ROLL_DAMPING_COEFF,
            'TYPE_PITCH_DAMPING_MOMENT_COEFF': fdt.TYPE_PITCH_DAMPING_MOMENT_COEFF,
            'TYPE_YAW_DAMPING_MOMENT_COEFF': fdt.TYPE_YAW_DAMPING_MOMENT_COEFF,
            'TYPE_CORIOLIS_ACCELERATION': fdt.TYPE_CORIOLIS_ACCELERATION,
            'TYPE_REFERENCE_LENGTH': fdt.TYPE_REFERENCE_LENGTH,
            'TYPE_REFERENCE_AREA': fdt.TYPE_REFERENCE_AREA,
            'TYPE_ORIENTATION_THETA': fdt.TYPE_ORIENTATION_THETA,
            'TYPE_ORIENTATION_PHI': fdt.TYPE_ORIENTATION_PHI,
            'TYPE_WIND_VELOCITY': fdt.TYPE_WIND_VELOCITY,
            'TYPE_AIR_TEMPERATURE': fdt.TYPE_AIR_TEMPERATURE,
            'TYPE_AIR_PRESSURE': fdt.TYPE_AIR_PRESSURE,
            'TYPE_SPEED_OF_SOUND': fdt.TYPE_SPEED_OF_SOUND,
            'TYPE_COMPUTATION_TIME': fdt.TYPE_COMPUTATION_TIME
        }

    def SetLogFile(self, filename):  # takes in string
        return self.apiInstance.setlogfile(filename)  # returns int

    #Start OpenRocketAPI functions dependant on FlightDataType

    def GetValue(self, d_type):
        '''
        These values correlated to the types found in
        openrocket.simulation.FlightDataType

        @param d_type           string matching a flightdatatype.
        '''

        TYPE = self.type_dic.get(d_type)
        value = self.apiInstance.GetValue(TYPE)
        return value

    def GetSimulationRunningTime(self):
        return self.apiInstance.GetTime()  # returns double

    #End OpenRocketAPI functions dependant on FlightDataType

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

    def GetCordinate(self):
        coordinate = self.apiInstance.getOrientation()
        if coordinate is None:
            return (0, 0, 0)
        return (coordinate.x, coordinate.y, coordinate.z)  # returns int

    def GetCordinateY(self):
        return self.apiInstance.GetCordinateY()  # returns int

    def GetCordinateZ(self):
        return self.apiInstance.GetCordinateZ()  # returns int

    def SimulationIsRunning(self):
        return self.apiInstance.SimulationIsRunning()  # returns bool

    #takes at least a string and int
    def SimulationSetup(self, szFileName, simtograb=1, randSeed=0, timeStep=0.0):
        errorCode = self.apiInstance.SimulationSetup(szFileName, simtograb,
                                                     randSeed, timeStep)
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

    def SimulationStep(self, steps=1):
        return self.apiInstance.SimulationStep(steps)  # returns int

    def SimulationRun(self):
        return self.apiInstance.SimulationRun()

    def FullCSVOut(self, fileName):
        return self.apiInstance.FullCSVOut(fileName)
