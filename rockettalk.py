#!/usr/bin/env python
""" The RocketTalk program runs a rocket simulation in OpenRocket
and sends the acceleration and orientation data to a flight computer"""
import argparse
import socket
import RocketLoop
#import RunRocket

parser = argparse.ArgumentParser(description="The RocketTalk program")
parser.add_argument("filename", metavar="filename.ork",
                    help="Input .ork simulation file")
parser.add_argument("-s", type=int, metavar='index', dest="sim_index",
                    help="Specify index of specific simulation")
parser.add_argument("-fc", metavar='IP address',
                    default=None, dest="fc_IP",
                    help="Override configured IP address of fc")
parser.add_argument("-rt", default='default', const='realtime', dest='time_step',
                    action='store_const', help="Sets time step interval to realtime")
parser.add_argument("-ns", default='default', const='none', dest='time_step',
                    action='store_const', help="Disable stepping")
parser.add_argument("-d", type=int, default=0, metavar='Random Seed', dest='rand_seed',
                    help="Use a non zero constant random seed for deterministic results")

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
if args.sim_index is not None:
    if args.sim_index < 1:
        print "Invalid simulation index, enter index > 0 please."
        quit()
else:
    args.sim_index = 1

#sanity check -fc.
#this throws an error if it's not a valid hostname, otherwise converts to IP
if args.fc_IP:
    args.fc_IP = socket.gethostbyname(args.fc_IP)
#if args.c is not None:
#    RunRocket.RunRocket(args.filename, args.sim_index, args.fc_IP, args.time_step, args.rand_seed)
#else:
    #Call Rocketloop
RocketLoop.RocketLoop(args.filename, args.sim_index, args.fc_IP, args.time_step, args.rand_seed,args.log_string)
