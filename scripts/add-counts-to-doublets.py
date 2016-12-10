#! /usr/bin/env python

import pdb
import sys
from collections import Counter

filename = sys.argv[1]

domain_counter = Counter()
long_lone_counter = Counter()

for line in open(filename):

    fields = line.strip().split("\t")
    

    chrom = fields[0]
    start = fields[1]
    end = fields[2]
    prelim_annotation = fields[3]
    length = fields[4]
    strand = fields[5]
    status = fields[6]
    
    try:
        coding_status = fields[7]
    except:
        coding_status = "unk"

    domain_counter[prelim_annotation] += 1

    numbered_prelim_annotation = prelim_annotation + "_" + str(domain_counter[prelim_annotation])
    
    
    toprint = [chrom,start,end,numbered_prelim_annotation,length,strand,status,coding_status]
    print "\t".join(toprint) 
    #print "\t".join(fields), "\t", name
