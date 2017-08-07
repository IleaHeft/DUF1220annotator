#! /usr/bin/env python

import sys
import pdb
from collections import Counter
from collections import defaultdict

pos_annotation = sys.argv[1]
neg_annotation = sys.argv[2]
domain_numbered_protein_fasta_file=sys.argv[3]
output_folder = sys.argv[4]

files = [pos_annotation, neg_annotation]


#out_flags = open(output_folder + "flags-clade-numbering.txt",mode= 'w')
out_new_fasta = open(output_folder + "fasta-for-protein-domains-clade-based-numbering.fa", mode = 'w')
domain_counter = Counter()
exon_counter = Counter()
domain_current = "placeholder"
old_new = defaultdict(str)


#Dictionary of gene names to change (e.g. LOC102724250 to NBPF1L)
gene_name_change = {"LOC102724250":"NBPF1L","LOC100996724":"PDE4DIPL1","RP11-744H18.1":"PDE4DIPL2","LOC105369199":"CON8C1","LOC105369140":"CON8C2","LINC00869":"CON8C3"} 

for strand_file in files:

    for line in open(strand_file):
    
        fields = line.strip().split("\t")
        chrom = fields[0]
        start = fields[1]
        end = fields[2]
        domain = fields[3]
        gene = fields[4]
        strand = fields[5]
        exon_length = fields[6]
       

        original_gene = gene
        original_domain = domain
        if original_gene in gene_name_change.keys():
            gene = gene_name_change[original_gene]
            domain = domain.replace(original_gene,gene)

        else:
            pass

        exon_counter[gene] += 1 #This keeps a count of all exons in a gen (regardless of their type - used for numbering, non-conserved, non-duf exons


        if "UCE" in domain: #No need to number UCE instances within a gene because they are not observed to repeat within a gen
            
            to_print = [chrom, start, end, domain, gene, strand, exon_length]
            print  "\t".join(to_print)

        elif "exon" in domain: #For exons that are neither conserved (CE or UCE) or DUF, number them according to their exon number in the gene
            
            exon = domain + "_" + str(exon_counter[gene])

            old_new[domain] = exon

            to_print = [chrom, start, end, exon, gene, strand, exon_length]
            print  "\t".join(to_print)

        elif "Non" in domain: # We might be able to remove this section
            domain_counter[domain] += 1
            domain_new = domain + "_" + str(domain_counter[domain])  

            old_new[domain] = domain_new
            to_print = [chrom, start, end, domain_new, gene, strand, exon_length]
            print  "\t".join(to_print)
        else:
            if domain != domain_current: #If the current domain you are looking at is different from the one in the line before, then add it to the counter
            
                domain_current = domain

                gene_clade = domain_current.split("_")[0] + "_" + domain_current.split("_")[1]
                
                domain_counter[gene_clade] += 1

                # this ifelse block is required to correctly number the CON4 domains in NBPF4 and NBPF6 - this is because their current annotation has a non-DUF exon between the short and long exons
                if "CON4" not in domain:
                    domain_new = gene_clade + "_" + str(domain_counter[gene_clade])
                else:
                    domain_new = gene_clade + "_" + "1"


                old_new[domain] = domain_new
                to_print = [chrom, start, end, domain_new, gene, strand, exon_length]
                print  "\t".join(to_print)
            else: # if the domain you are looking at is the same as the one the line before (e.g. you've just gone from the short to long peice of the domain, so domain hasn't changed) don't add to the count, give it the same count number as its mate
                
                domain_current = domain

                gene_clade = domain_current.split("_")[0] + "_" + domain_current.split("_")[1]

                domain_new = gene_clade + "_" + str(domain_counter[gene_clade])
                
                # Set up a dictionary that will be used to update the fasta file
                if original_gene in gene_name_change.keys(): #Need this bit so that the key in the dictionary matches what is in the input fasta file
                    old_new[original_domain] = domain_new
                else:
                    old_new[domain] = domain_new
                
                to_print = [chrom, start, end, domain_new, gene, strand, exon_length]
                print   "\t".join(to_print)


for line in open(domain_numbered_protein_fasta_file):

    if line.startswith(">"):
        header = line.strip()
        old_domain = header.replace(">","")

        new_domain = old_new[old_domain]
        new_header = ">" + new_domain
        
       
        print >> out_new_fasta, new_header
    else:
        seq = line.strip()
        
        print >> out_new_fasta, seq
