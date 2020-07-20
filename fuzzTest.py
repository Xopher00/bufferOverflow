#!/usr/bin/python
import os, sys, socket, argparse

parser = argparse.ArgumentParser()
parser.add_argument("--h", help="this is the target IP Address")
parser.add_argument("--p", type=int, help="This is the target Port Number")
parser.add_argument("--cmd", type=str, help="This is the command to be eexcuted")
args = parser.parse_args()

RHOST = args.h
RPORT = args.p
cmd = args.cmd

# Create an array of buffers, from 10 to 2000, with increments of 20.
counter = 100
fuzz_strings = ["A"]
while len(fuzz_strings) <= 30:
    fuzz_strings.append("A" * counter)
    counter = counter + 100
for fuzz in fuzz_strings:
    print "Fuzzing with %s bytes" % len(fuzz)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connect = s.connect((RHOST, RPORT))
    s.send((cmd + fuzz + '\n' ))
    print s.recv(1024)
    s.close()
