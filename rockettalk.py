#rockettalk.py

import argparse

parser = argparse.ArgumentParser(description="The RocketTalk program")
parser.add_argument("filename", metavar="filename.ork",
                    help="input .ork simulation file")
parser.add_argument("-s", type=int, metavar='index', dest="sim_index",
                    help="specify index of specific simulation")
parser.add_argument("--fc", metavar='IP address',
                    default="127.0.0.1", dest="fc_IP",
                    help="IP address of fc (default 127.0.0.1)")
args = parser.parse_args()


#check for file existence
#explicitly setting mode r, change to r+ if we also need to write to the file
#this can easily be prepended with a path_to_file if necessary
#no file locking at the moment

try:
   fh = open(args.filename)
except IOError:
   print "file open error, sure it exists?"
   raise

print args.filename + " successfully opened."

#todo: sanity check -s
#todo: sanity check -fc, then convert to IP address

