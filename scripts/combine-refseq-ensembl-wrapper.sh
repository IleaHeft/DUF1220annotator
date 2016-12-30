#! /usr/bin/env bash
todays_date=$(date +"%Y-%m-%d")

refseq_annotation=$1
ensembl_annotation=$2
reference_selection_file=$3
output_folder=$4

python scripts/combine-refseq-ensembl.py $refseq_annotation $ensembl_annotation $reference_selection_file $output_folder | \
sort -k 1,1 -k 2,2n  > $output_folder/combined-refseq-ensembl-annotation.bed

