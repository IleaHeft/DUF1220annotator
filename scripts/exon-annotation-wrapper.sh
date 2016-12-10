#! /usr/bin/env bash

################
# Inputs:
#   (1) Provide the file with all nbpf exons annoated as "hit" or "not-hit" by hmmer
#   (2) Provide the output folder (with not slash at the end)
#   (3) The reference being utilized (refseq or ensembl)

# Output:
# All of the exons annotated as being one of the following (duf-short, duf-long, coiled-coil, or tbd) AND
# Adjancent short and long exons grouped together and numbered within each gene

starting_exon_file=$1
output_folder=$2
reference=$3

python scripts/group-exon-doublets.py $starting_exon_file $output_folder $reference

input_neg=$output_folder/annotated-nbpf-exons-neg-strand-$reference.bed
input_pos=$output_folder/annotated-nbpf-exons-pos-strand-$reference.bed

sorted_neg=$output_folder/annotated-nbpf-exons-neg-strand-sorted-$reference.bed
sorted_pos=$output_folder/annotated-nbpf-exons-pos-strand-sorted-$reference.bed

sort -k 1,1 -k 2,2nr  $input_neg > $sorted_neg
sort -k 1,1 -k 2,2n   $input_pos > $sorted_pos

python scripts/add-counts-to-doublets.py $sorted_neg > $output_folder/annotated-nbpf-exons-neg-doublets-$reference.bed

python scripts/add-counts-to-doublets.py $sorted_pos > $output_folder/annotated-nbpf-exons-pos-doublets-$reference.bed

cat $output_folder/annotated-nbpf-exons-neg-doublets-$reference.bed  $output_folder/annotated-nbpf-exons-pos-doublets-$reference.bed |\
sort -k 1,1 -k 2,2n > $output_folder/annotated-nbpf-exons-all-doublets-$reference.bed
