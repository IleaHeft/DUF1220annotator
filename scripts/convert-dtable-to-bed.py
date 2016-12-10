#! /usr/bin/env python

###################################################################
# Purpose: Convert HMMERs "domain table out" to a bed format 
# Inputs:
#   (1) The name of the file to operate (the "domain table out")


import sys
import pdb
import re

filename = sys.argv[1]
output_folder=sys.argv[2]

output_all = open(output_folder+"/domain-alignment-cords-all.bed",mode='w')
#output = open(output_folder+"domain-alignment-cords-mapped.bed", mode = 'w')
#output_contig = open(output_folder+"domain-alignment-cords-unmapped.bed", mode = 'w')

for line in open(filename):

    if line.startswith("#"):
        continue
    else:
        
        line = re.sub("\s+","\t",line)

        fields = line.strip().split("\t")
        
        chrom = fields[0]
        start_align = fields[9]
        end_align = fields[10]
        start_env = fields[11]
        end_env = fields[12]
        strand = fields[8]
        gene = "TBD"
        score = "1"

        #toprint = [chrom, start_align, end_align,gene,score, strand]
        toprint = [chrom, start_align, end_align, strand]

        print >> output_all, "\t".join(toprint)

       # if "chr1_K" in chrom:

           # print >> output_contig, "\t".join(toprint)
       # else:    
           # print >> output, "\t".join(toprint)

        
