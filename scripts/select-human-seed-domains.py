#! /usr/bin/env python

import sys
import pdb

filename = sys.argv[1]
output_folder = sys.argv[2]

file_parts = filename.split("/")

new_file_name = file_parts[len(file_parts)-1].split(".")[0] + "_human.txt"

out = open(output_folder + new_file_name, mode = 'w')


for line in open(filename):
    
    line = line.strip()

    if "STOCKHOLM" in line:
        print >> out, line

    elif "HUMAN" in line:
        print >> out, line

#    elif "#=GC" in line:
        #print >> out, line

    else:
        continue

print >> out, "//"
