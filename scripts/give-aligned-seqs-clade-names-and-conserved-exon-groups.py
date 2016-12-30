#! /usr/bin/env python

import sys
import re
import pdb
import time

from collections import defaultdict


#Inputs
# alignment file of protein doublets
# the annotation file (with coordinates, etc)
# the output folder

fasta_file_of_protein_doublets_and_lone_seqs = sys.argv[1]
fasta_file_of_non_duf_exons = sys.argv[2]
my_annotation = sys.argv[3]
output_folder = sys.argv[4]

todaysdate=time.strftime("%Y-%m-%d")

#out = open(output_folder + "/combined-refseq-ensembl-annotation-with-clades.bed", mode = 'w')
out_csv = open(output_folder + "/annotation-domain-based-numbering.csv",mode = 'w')
out_bed_file = open(output_folder + "/annotation-domain-based-numbering.bed", mode = 'w')
out_protein_doublets_with_clades = open(output_folder + "/fasta-for-protein-domains-with-clades.fa", mode = 'w')
out_protein_doublets_and_lone_with_clades = open(output_folder + "/fasta-for-protein-domains-and-lone-with-clades.fa", mode = 'w')
out_domain_clade_list = open(output_folder + "/duf-domain-numbers-to-clades.txt", mode = 'w')

domain_seq = defaultdict(str)
domain_clade = defaultdict(str)


exon_seq = defaultdict(str)
exon_group = defaultdict(str)

# First, work on assigning DUF protein doublets to a clade

## This bit goes through the fasta file of protein doublets and makes a dictionary of domain names and protein sequences
for line in open(fasta_file_of_protein_doublets_and_lone_seqs):

    if line.startswith(">"):
        domain = line.strip().split("(")[0]
        
    else:
        sequence = line.strip()

        domain_seq[domain] = sequence    

## This goes through every domain and its protein sequence and assigns it to a clade
for domain, seq in domain_seq.items(): #The long exons of the different clades vary pretty clearly from one another in their last few amino acids and that "clade-specific sequence" is pretty well conserved across all members of a clade

   
    #account for the domains that have short exons from one domain and long exons from another
    # This first one accoutns for the HLS1(short)/HLS2(long) hybrids in NBPF3 and NBPF17P
    if "LGLALD" in seq and "KEDQ" in seq:
        clade = "HLS1/HLS2"

    # This one accounts for the HLS2(short)/HLS1(long) hybrids in NBPF26
    elif "IEKYQEVEEDQDPSCP" in seq and "AVDM" in seq:
        clade = "HLS2/HLS1"

    # This one accounts for the seemingly HLS3(short)/HLS2(long) hybrid in NBPF17P
    elif "IKKDQEEEEDQGPSCP" in seq and "LALDV" in seq:
        clade = "HLS3/HLS2"

    # This accounts for the HLS1(short)/HLS2(long) hybrid in NBPF13P
    elif "DQVKK" in seq and "YLELPD" in seq:
        clade = "HLS1/HLS2"


    #"This accounts for the the HLS1-G4 short exon with HLS2 long hybrids:
    elif "IEKKGKGKKRRGRRSKK" in seq and "LGLALDVD" in seq:
        clade = "HLS1/HLS2"

    elif "EDSLEE" in seq or "EDSQEE" in seq or "QDSLEE" in seq or "AEEK" in seq: #The AEEK is necessary to capture a diverged sequence from 21P
        clade = "CON1"


    # Most of the CON2 seqs are caputred by "VCMAVDIG" -- the other two are included to captured the slightly different sequences of NBPF17P, NBPF13P, and NBPF3
    elif "VCMAVDIG" in seq or "VGLALDIG" in seq or "VGLALVIG" in seq: 
        clade = "CON2"

    elif "VIFP" in seq:
        clade = "CON3"


    
    # Most HLS1 sequences are caputred by the AVDMD at the end of their sequence
    elif "AVDM" in seq or "AFDMD" in seq or "AIDMD" in seq or "ALDMD" in seq:
        clade ="HLS1"

    # Most HLS2 sequences have the "LGLALDVD" run at their end, "LGLALDLD" caputures an NBPF9 domain
    elif "LGLALDVD" in seq or "LGLALDL" in seq:
       # clade = "2"
        clade = "HLS2"
    
    
    # The LSRELLEVVE part is added here to caputure NBPF11-duf-6, which has a very diverged end, so doesn't match the DVG---, but is clearly most related to this clade if you
    # futher upstream in the sequence.  NBPF13-duf-4 is heavily diverged, but is most similar to this group -- same for NBPF13P-duf-3
   
    elif "HVGFSLD" in seq or  "LSRELLEVVE" in seq or domain == "NBPF13P-duf-4" or domain == "NBPF13P-duf-3":
       # clade = "3"
        clade = "HLS3"

    # This "manually" accounts for one of the NBPF13P domains that appears to have a frameshift and so isn't caught by the other sequences I'm using for HLS
    elif "SSELLEGEGP" in seq:
        clade = "HLS3"

    ### Here is one of the 4/5/6/22p specific clades
    # NBPF4-DUF-2
    # NBPF5P-DUF-2
    # NBPF6-DUF-2
    # NBPF7-DUF2

    elif "LGFL" in seq  or "LGFP" in seq:
        clade = "CON4"

    ### Here is one of the 4/5/6/22p specific clades
    # NBPF22P-DUF-1
    # NBPF6-DUF-3
    # NBPF4-DUF-3

    elif "SFEDKQVSLALVD" in seq:
        clade = "CON5"

    ### Here is another 4/5/6/22p clade
    # NBPF22P-DUF-2
    # NBPF4-DUF-4
    # NBPF6-DUF-4
    # NBPF13P-DUF-5

    elif "ALDVA" in seq or "ESYLTPS" in seq: #Almost all are captured by "ALDVA", the "ESYLTPS" graps a diverged sequence from NBPF21P
        clade = "CON6"
    

    # This is the clade I have established for PDE4DIP, the gna seq, and its similar sequences:

    elif "EACSDMDI" in seq:
        clade = "CON7"

    # This is the other clade, for FAM91A3P and related sequences:

    elif "LFDAQEGP" in seq:
        clade = "CON8"

    else:
        clade = "NO SEQUENCE MATCH"

    domain_clade[domain] = clade

    ### This prints the aligned protein doublet file with the clade names, as a fasta file

    gene = domain.split("_")[0]
    exon_type = domain.split("_")[1]
    num = domain.split("_")[2]

    # This handles the lone sequence - the short exons only need some different criteria for assigning them to a clades, but the amino acid motifs used above are generally for the long exon
    if "long-lone" in exon_type:
        clade = clade + "(long-lone)" #The lone long ones were already correctly assigned to a clade above, we just want to add an annotation that they are a "long-lone" domain
    elif "short-lone" in exon_type:
        if "EEEK" in seq:
            clade = "CON2(short-lone)"
        elif "NDND" in seq or "NDED" in seq or "NDDD" in seq or "NDTD" in seq or "NDEG" in seq or "EDED" in seq:
            clade = "CON1(short-lone)"
        elif "IEKY" in seq:
            clade = "HLS2(short-lone)"
        elif "RRRGR" in seq:
            clade = "HLS1.108(short-lone)"
        elif "HRWD" in seq or "YRWD" in seq:
            clade = "HLS1.51(short-lone)"
        elif "TKKD" in seq or "IKKD" in seq:
            clade = "HLS3(short-lone)"

    else:
        pass

    domain_clade[gene + "_" + exon_type + "_" + num] = clade


    if "lone" in domain or "lone" in exon_type:
        
        print >> out_protein_doublets_and_lone_with_clades, gene + "_" + clade + "_" + num
        print >> out_protein_doublets_and_lone_with_clades, seq 

    else:
        
        print >> out_protein_doublets_with_clades, gene + "_" + clade + "_" + num
        print >> out_protein_doublets_with_clades, seq 
    
        print >> out_protein_doublets_and_lone_with_clades, gene + "_" + clade + "_" + num
        print >> out_protein_doublets_and_lone_with_clades, seq 
    domain_clean = domain.replace(">","")
    print >> out_domain_clade_list, domain_clean, "\t", clade


# Assign non-DUF1220 exons to "conserved exon" groups where appropriate:

## As we did for the protein doublets, first make a dictionary of the current exon names and their sequences
for line in open(fasta_file_of_non_duf_exons):

    if line.startswith(">"):
        exon = line.strip().split("(")[0] 

        
    else:
        sequence = line.strip()
        
       
        exon_seq[exon] = sequence

# As for the protein doublets, look at each sequence and assign it to a "conserved exon group" based on certain nucleotide motifs (as opposed to protein motifs)
for exon, seq in exon_seq.items():

    exon = exon.split(":")[0]
    # The nucleotide sequences being used here were manually identifed from alignments of the exons, as the most conserved regions of clearly conserved group
    
    if "ACCTCTTCTGCCACAAAC" in seq or "TGAACATCCTAGAAATC" in seq: #Most sequences are caught by the first sequence, the second one, from a different part of the exon, is only necessary to pick up a couple of odd ones (NBPF21P,NBPF13P)
        ce_group = "CE1" #This is the gorup that is generally about 209bp long and is the first exon in the CON1-associated exon triplet

    elif "CAAGCTGAGGAGCT" in seq or "CAAGCTGGAAAGCTCA" in seq: #All but one are capture by the first sequence, the second sequence picks up one from NBPF13P
        ce_group = "CE2" # This is the group that is generally about 102bp long and is the second exon in the CON1- associated exon triplet
    
    elif "GGAAGGGAGAGATGCCT" in seq:
        ce_group = "CE3" #This is the group that is generally about 214bp long and is in the CON1-associated exon triplet

    elif "AACCGACAATCACTTGA" in seq:
        ce_group = "CE4" #These are the 86bp exons withing the DUF region of NBPF4 and NBPF6

    elif "CTGATTCTGGGAACCAATGGCCCTT" in seq: #These are in NBPF4 and NBPF6
        ce_group = "CE5"

    elif "AGACTGGCATTCAGATT" in seq or "AGACTGGCATGCAGATT" in seq: #These are in NBPF4, 6, and 7
        ce_group = "CE6"
   
    elif "TACCAAATACTGCTG" in seq or "attctgaagttgtctgaaaa" in seq: #The second sequence is only necessary to pick up the 588bp exon from NBPF25P
        ce_group = "CE7"
   
   #These are annotated as "UCE" for untranslated conserved exon

    elif "TCCACCCAGCGTT" in seq:
        ce_group = "UCE1" #For some of the genes, this is the most 5' UTR exon


    elif "CTGGTGATGGGCAAGCC" in seq:
        ce_group = "UCE2"
    

    elif "ccccaagtagctgggacctac" in seq: #Needs to be lowercase to match what is in the fasta file
        ce_group = "UCE3"


    elif "ACTCCCACTGTCCAGGG" in seq:
        ce_group = "UCE4"


    elif "TCCTGGGGGAGTAGGAGCCAGT" in seq:
        ce_group = "UCE5"


    elif "AATGTGATTGATAACAGTAAAG" in seq:
        ce_group = "UCE6"

   
    elif "TTGGGATCAAATGTGAGCCTATGGATCA" in seq:
        ce_group = "UCE7"
   

    elif "cattcgaatcattgtgagg" in seq: #Needs to be lowercase to match fasta file
        ce_group = "UCE8"


    elif "GGCGGCCCAGATGGA" in seq:
        ce_group = "UCE9"
  
 
    elif "CAGTGCATGGAGATGG" in seq:
        ce_group = "UCE10"
 

    elif "gtgtgacctcaagtaagcca" in seq:
        ce_group = "UCE11"


    elif "GATCCCCATTGGT" in seq:
        ce_group = "UCE12"

    elif "CCTCACTCTT" in seq:
        ce_group = "UCE13" # This group is the final UTR exon before the coding sequence (in most genes) 


    elif "CCCCCGCGCAT" in seq:
        ce_group = "UCE14"


    elif "TGTCGAGATGGCTATGAA" in seq:
        ce_group = "UCE15"


    elif "TGTCCAGAAGGCTTCTTGGGG" in seq:
        ce_group = "UCE16"


    elif "TAAGGAGTGCCAATGGACC" in seq:
        ce_group = "UCE17"


    elif "GAGGAACAGAGCTCTGGGAAAGAGACA" in seq: 
        ce_group = "UCE18"


    elif "TACTGCTAAGAATTCAAAC" in seq:
        ce_group = "UCE19"


    elif "tcagagccagaggaacatttgga" in seq:
        ce_group = "UCE20"


    else:
        ce_group = "exon"
    
    exon_group[exon] = ce_group
# This writes a new annotation file that replaces the old premiliary/generic "duf" annotation with clade names
for line in open(my_annotation):

    fields = line.strip().split("\t")

    chrom = fields[0]
    start = fields[1]
    end = fields[2]
    current_annotation = fields[3]
    
    # to get the annotation into the necessary form to match the fasta file
    current_annotation_parts = fields[3].split("_")
    gene = current_annotation_parts[0]
    exon_type = current_annotation_parts[1]
    number_in_gene = current_annotation_parts[2]

    
    if "lone" in current_annotation or "Non" in current_annotation:
        annotation = current_annotation
    
    else:
        annotation = gene + "_" + exon_type.split("-")[0] + "_" + number_in_gene
    
    length = int(fields[4])
    strand = fields[5]

    if "Non" not in annotation:    
        
        if current_annotation == "NBPF21P_duf-short_2":
            clade = "CON4(short)"

        elif current_annotation == "NBPF21P_duf-long_2":
            clade = "DIV(long)" #The long exon sequence is too diverged to confidently assign it to any one clade

        elif current_annotation == "NBPF18P_CON1-SHORT_1":
            clade = "CON1-SHORT"

        else:
            annotation = ">"+annotation
            clade = domain_clade[annotation]
   
                
        to_print = [chrom, start, end, gene + "_" + clade + "_" + number_in_gene, gene, strand, str(length)] 
        print >> out_csv, ",".join(to_print)
        print >> out_bed_file, "\t".join(to_print)
    else: 
        
        annotation = ">"+annotation
        
        if exon_group[annotation]:

            ce_group = exon_group[annotation]
        
        else:
            print line, "NO CE GROUP ASSIGNED"

        to_print_non_duf = [chrom,start,end,gene + "_" + ce_group,gene,strand,str(length)]
        print >> out_csv, ",".join(to_print_non_duf)
        print >> out_bed_file, "\t".join(to_print_non_duf)
