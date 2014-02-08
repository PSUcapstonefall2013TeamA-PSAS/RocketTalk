#!/usr/bin/env python
#rockettalk.py

import argparse
import socket
import RocketLoop

parser = argparse.ArgumentParser(description="The RocketTalk program")
parser.add_argument("filename", metavar="filename.ork",
                    help="input .ork simulation file")
parser.add_argument("-s", type=int, metavar='index', dest="sim_index",
                    help="specify index of specific simulation")
parser.add_argument("--fc", metavar='IP address',
                    default=None, dest="fc_IP",
                    help="Override configured IP address of fc")
parser.add_argument("--ts", metavar='Time Step',
                    default='default', dest='time_step',
                    help="Set time step for simulation.")
args = parser.parse_args()


#check for file existence
#explicitly setting mode r, change to r+ if we also need to write to the file
#this can easily be prepended with a path_to_file if necessary
#no file locking at the moment
try:
  fh = open(args.filename)
except IOError, ex:
  print "Caught the IOError:\n    ", ex
  print "Verify the path to the .ork file"
  quit()

# sanity check -s
if args.sim_index != None:
  if args.sim_index < 1:
    print "Invalid simulation index, enter index > 0 please."
    quit()

#sanity check -fc.
#this throws an error if it's not a valid hostname, otherwise converts to IP
if args.fc_IP:
  args.fc_IP = socket.gethostbyname(args.fc_IP)

if args.time_step:
    if args.time_step != 'default':
       if args.time_step != 'realtime':
           print 'Invalid time step, enter default or realtime'
           quit()

#Call Rocketloop
RocketLoop.RocketLoop(args.filename, args.sim_index, args.fc_IP, args.time_step)

