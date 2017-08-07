#! /usr/bin/env python

##This program:
#Replaces chromosome accession numbers with the chr format
#Extracts the gene and transcript names from the long ugly line of text 
#Output is three files: species name - genes - reference.bed, species name - exons - reference.bed, and species name - cds - reference.bed - these files have all
#of the genes or exons (as appropriate) from the original gff file 
#with the newly formated chromosomes, and the extracted gene and transcript names


# Inputs
#   (1) The filename of the orignal gff file
#   (2) The species
#   (3) The assembly report for the species that gives the relationship between the accession numbers and standard chromosome notation (e.g. chr1)
#   (4) The output folder

import re
import sys
import pdb
from collections import defaultdict


gff3_or_gtf = sys.argv[1]
species = sys.argv[2]
reference = sys.argv[3]

if reference == "refseq":
    assembly_report = sys.argv[4]
    output_folder = sys.argv[5]

else:
    output_folder=sys.argv[4]

outputGene=open(output_folder + "/" + species + "-genes-" + reference + ".bed",mode='w')
outputExon=open(output_folder + "/" + species + "-exons-" + reference + ".bed",mode='w') 
outputCDS=open(output_folder + "/" + species + "-cds-" + reference + ".bed",mode='w')
outputUTR=open(output_folder + "/" + species + "-utr-" + reference + ".bed",mode='w')

print species
print output_folder + "/" + species + "-genes-" + reference + ".bed"

regions_to_keep=["exon","gene", "CDS","five_prime_utr", "three_prime_utr","start_codon","stop_codon"]

accession_chr_dict=defaultdict(str)


# Using the information in the assembly report file, make a dictionary that links acession IDs with chromosome notation (e.g. chr1), this is only necessary for refseq
if reference == "refseq":

    for line in open(assembly_report):

        if "#" not in line:
            
            fields = line.strip().split("\t")
            accession = fields[6]
            associated_chrom = fields[9]
            accession_chr_dict[accession] = associated_chrom
        

# Go through the GFF3 file (or GTF file for Ensembl), and extract out the necessary information to create clean bed files

for line in open(gff3_or_gtf):

    if line.startswith("#"):
        continue
    

    fields=line.strip().split("\t")
    chrom=fields[0]
    region=fields[2]
    start=fields[3]
    end=fields[4]
    strand=fields[6]
   
    # This code skips any lines that aren't describing an exon, gene, or coding sequence entry
    if region not in regions_to_keep:
        continue

    if reference == "refseq":
        chrom = accession_chr_dict.get(chrom) # This line sets the chromosome to the "chr" annotation based on the assembly report file
    else:
        chrom = "chr" + chrom # If the reference is Ensembl, you just need to put "chr" in front of the number that is provided in the GFF3 files
    

    # Extract the gene name for each feature from the messy line that contains the gene name
    
    if reference == "refseq":

        try:
            gene=re.search(r'gene=[^;\n]+',line).group()

        except:
            gene="NotFound"

        gene = gene.replace("gene=","") # gets rid of the "gene=" notation that was part of the original line
    
        if re.findall(r'transcript_id=[^\s]+',line):
            transcript = re.findall(r'transcript_id=[^\s]+',line)[0]
            transcript = transcript.replace("transcript_id=","")

        else:
            transcript = "NotFound"

    else: #For the ensembl gtf file, the search needs to be slightly different 
        
        try:
            gene= re.search(r'gene_name [^;\n]+',line).group()
            gene = gene.strip().split('"')[1]
        
        except:
            gene = "NotFound"

        if re.search(r'transcript_name [^;\n]+',line):
            transcript = re.search(r'transcript_name [^;\n]+',line).group()
            transcript = transcript.strip().split('"')[1]
        else:
            transcript = "NotFound"

    if chrom == "na":
        continue

    else:
        if region == "gene":
            to_print=[chrom,start,end,gene,"NA",strand]
            print >> outputGene, "\t".join(to_print)

        elif region == "exon":
            to_print=[chrom,start,end,gene,"exon",strand,transcript]
            print >> outputExon, "\t".join(to_print)

        elif region == "CDS":
            to_print=[chrom,start,end,gene,"CDS",strand,transcript]
            print >> outputCDS, "\t".join(to_print)

        elif region == "five_prime_utr" or region == "three_prime_utr" or region == "start_codon" or region == "stop_codon":
            
            if reference == "ensembl": #The UTR and start/stop codon notations don't exist in the RefSeq file, so no reason to print an empy file
                to_print=[chrom,start,end,gene,region,strand,transcript]
                print >> outputUTR, "\t".join(to_print)
            
        


    

    
