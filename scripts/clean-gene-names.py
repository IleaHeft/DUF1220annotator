#! /usr/bin/env python

import sys
import pdb

bed_file=sys.argv[1]

for line in open(bed_file):

    fields = line.strip().split("\t")
    
    chrom=fields[0]
    start = fields[1]
    end = fields[2]
    gene = fields[3]
    region = fields[4]
    strand = fields[5]
    hit_status=fields[6]
    coding_status=fields[7]
    
    hit_status = hit_status.strip()
    coding_status = coding_status.strip()

    if "," in gene:
        genes = gene.split(",")
       
        if gene == "NBPF5P,NBPF6": # I know from troubleshooting stetps that this occurance should be coded as NBPF5 - it needs to have its own code, because it enters the below loop, extra lines get created
            gene_selected = "NBPF5P"

            to_print=[chrom,start,end,gene_selected,region,strand,hit_status,coding_status]
            print "\t".join(to_print)
        
        elif "NBPF" in gene or "PDE4DIP" in gene or "LINC00869" in gene or "LINC00623" in gene: # If one of the genes in the list is an NBPF gene

            for index,gene in enumerate(genes): # Go through the list of genes, and when you find the NBPF one, set that one to the selected gene
                if "NBPF" in gene or "PDE4DIP" in gene or "LINC00869" in gene or "LINC00623" in gene:

                    gene_selected = gene
                    
                    to_print=[chrom,start,end,gene_selected,region,strand,hit_status,coding_status]

                    print "\t".join(to_print)

                else:
                    continue

        else: 
            print "\t".join(fields), "FLAG: two-genes, non-NBPF"
                
    else: #If there was only one gene in the list to begin with, just print the original line from the BED file
        if gene != "LOC105371303": # This gene has a partial overlap with the 5' end of NBPF20, but it doesn't have any DUF domains in it, so it is not necessary to print its other exons
            print "\t".join(fields)
