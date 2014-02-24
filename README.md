RocketTalk
==========
RocketTalk is a python wrapper to OpenRocket using JPype for the PSAS flight computer. 


RocketTalk will run a simulation in a given .ork file and send packets to the flight computer.
This data can be then viewed with Telemetry. 


PSAS Flight Computer:  http://github.com/psas/av3-fc
Telemetry: http://github.com/psas/telemetry

##Installing:
Install JPype using your package manager:  
`$ sudo apt-get install python-jpype`

Rename config.py_dist to config.py
Modify the paths in config.py to point to your OpenRocket.jar and libjvm.so

Example path to OpenRocket jar file:         
JAR_PATH = "/home/username/openrocket.git/swing/build/jar/OpenRocket.jar"

Example path to libjvm.so  
JVM = "/usr/lib/jvm/jdk-7-oracle-x64/jre/lib/amd64/server/libjvm.so"

##Running:
Start RocketTalk with default settings.
        
`$ ./rockettalk.py /path/to/rocket.ork`

###Flags:

####-s simnum
Selects simulation number simnum from the simulation list in the .ork, default 1.

####-fc addr
Sets the flight computer IP address to addr, default is FC_IP in config.py.

####-rt
Sets the simulation to be stepped in real time.
The sleep threshold amount can be adjusted in config.py. Using higher or lower values may yield more accurate results. 

####-ns
Disables stepping and runs the entire simulation.

####-d seed
Sets the random seed to seed. A non-zero seed used on repeated simulations will give deterministic results.

