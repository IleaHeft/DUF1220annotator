#! /usr/bin/env bash

today=$(date +%Y-%m-%d)

annotation_domain_order_numbering=$1
fasta_protein_file_domain_numbering=$2
output_folder=$3

pos_strand=$output_folder/annotation-domain-order-numbering-pos-strand-$today.bed
grep "+" $annotation_domain_order_numbering | sort -k 1,1 -k 2,2n  > $pos_strand

neg_strand=$output_folder/annotation-domain-order-numbering-neg-strand-$today.bed
grep -v "+" $annotation_domain_order_numbering | sort -k 1,1 -k 2,2nr > $neg_strand

indiv_domain_annotation=$output_folder/annotation-clade-based-numbering-$today.bed
python scripts/number-domains-according-to-clade.py $pos_strand $neg_strand $fasta_protein_file_domain_numbering  $output_folder | sort -k 1,1 -k 2,2n > $indiv_domain_annotation

full_domain_annotation=$output_folder/annotation-clade-based-numbering-full-domains-$today.bed
sort -k 4,4 $indiv_domain_annotation |\
bedtools groupby -i stdin -g 4 -c 1,2,3,5,6 -o distinct,min,max,distinct,distinct |\
awk 'BEGIN{OFS = "\t"} {print $2,$3,$4,$1,$5,$6,$4-$3}'| sort -k 1,1 -k 2,2n > $full_domain_annotation
