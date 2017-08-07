#! /usr/bin/env/ bash

#Calls MakeBEDfiles.py
#Cleans up the gene name and transcript name columns
#Sorts the bed file
#Collapse redudnant exons from multiple transcripts into a single set of exons

# Inputs
#   (1) the original gff file to operate on

#gff3_or_gtf=$1
#species=$2
#reference=$3 #Either "refseq" or "ensembl"
#assembly_report=$4
#output_folder=$5


source scripts/config.sh

output_folder=$1 #The folder where the results of the code are stored
reference=$2

#Create variable names for the exon, gene, and coding sequence files that will be output from MakeBEDfiles.py
exon_file=$output_folder/$species-exons-$reference.bed
gene_file=$output_folder/$species-genes-$reference.bed
cds_file=$output_folder/$species-cds-$reference.bed
#utr_file=$output_folder/$species-utr-$reference.bed

echo $output_folder
echo $exon_file

#sort the gene file
sort -k 1,1 -k 2,2n $gene_file > $output_folder/$species-genes-$reference-sorted.bed

#sort and merge the exon file

sort -k 1,1 -k 2,2n $exon_file | bedtools merge -i stdin -s -c 4,5,6 -o distinct | cut -f 1-3,5-7 > $output_folder/$species-exons-$reference-sorted-merged.bed

#sort and merge the CDS file


sort -k 1,1 -k 2,2n $cds_file | bedtools merge -i stdin -s -c 4,5,6 -o distinct | cut -f 1-3,5-7 > $output_folder/$species-cds-$reference-sorted-merged.bed

