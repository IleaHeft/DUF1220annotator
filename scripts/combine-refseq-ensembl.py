#! /usr/bin/env python

import sys
import pdb
from collections import defaultdict

refseq_annotation = sys.argv[1]
ensembl_annotation = sys.argv[2]
reference_selection_file = sys.argv[3]
output_folder = sys.argv[4]

refseq_genes = []
ensembl_genes = []

for line in open(reference_selection_file): 
    fields = line.strip().split(",")
    gene = fields[0]
    ref_selec = fields[1]
    
    if ref_selec == "refseq":

        refseq_genes.append(gene)
    else:
        ensembl_genes.append(gene)


for line in open(ensembl_annotation):

    fields = line.strip().split("\t")
    
    chrom = fields[0]
    start = fields[1]
    end = fields[2]
    prelim_notation = fields[3]
    
    gene = prelim_notation.split("_")[0]

    
    if gene in ensembl_genes:

        print "\t".join(fields)

    else:
        continue

for line in open(refseq_annotation):

    fields = line.strip().split("\t")

    prelim_notation = fields[3]
    
    gene = prelim_notation.split("_")[0]
    
    if gene in refseq_genes:
        
        print  "\t".join(fields)
