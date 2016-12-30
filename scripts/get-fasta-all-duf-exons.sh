#! /usr/bin/env bash
todays_date=$(date +"%Y-%m-%d")

annotated_exons=$1
fasta_file=$2
output_folder=$3

# Get fast for all duf exons
grep -v "Non" $annotated_exons |\
bedtools getfasta -s -name -fi $fasta_file -bed stdin > $output_folder/fasta-for-all-duf-exons-nuc.fa 

#Make these files for just short & just long exons

grep -v "Non" $annotated_exons |\
awk 'BEGIN{OFS="\t"} {if ($5 < 120 || $2 == "148109284") print $1,$2,$3,$4,$5,$6,$7}' |\
bedtools getfasta -name -s -fi $fasta_file -bed stdin > $output_folder/fasta-for-all-short-exons-nuc.fa



grep -v "Non" $annotated_exons |\
awk 'BEGIN{OFS="\t"} {if ($5 > 120) print $1,$2,$3,$4,$5,$6,$7}' |\
bedtools getfasta -name -s -fi $fasta_file -bed stdin > $output_folder/fasta-for-all-long-exons-nuc.fa


#Make this file of all non-DUF1220 exons
grep "Non" $annotated_exons |\
bedtools getfasta -name -s -fi $fasta_file -bed stdin > $output_folder/fasta-for-all-non-duf-exons.fa

#Make this file of coding, non-DUF1220 exons
#grep "Non" $annotated_exons | grep -w "C" |\
#bedtools getfasta -name -s -fi $fasta_file -bed stdin -fo $output_folder/fasta-for-coding-non-duf-exons.fa




# Repeat the previous commands but with the output being tab delimited rather than fasta

# Get fast for all duf exons
grep -v "Non" $annotated_exons |\
bedtools getfasta -tab -s -name -fi $fasta_file -bed stdin > $output_folder/fasta-for-all-duf-exons-nuc.tab 

#Make these files for just short & just long exons

grep -v "Non" $annotated_exons |\
awk 'BEGIN{OFS="\t"} {if ($5 < 120) print $1,$2,$3,$4,$5,$6,$7}' |\
bedtools getfasta -tab -name -s -fi $fasta_file -bed stdin > $output_folder/fasta-for-all-short-exons-nuc.tab


grep -v "Non" $annotated_exons |\
awk 'BEGIN{OFS="\t"} {if ($5 > 120) print $1,$2,$3,$4,$5,$6,$7}' |\
bedtools getfasta -tab -name -s -fi $fasta_file -bed stdin > $output_folder/fasta-for-all-long-exons-nuc.tab


#Make this file of all non-DUF1220 exons
grep "Non" $annotated_exons |\
bedtools getfasta -tab -name -s -fi $fasta_file -bed stdin > $output_folder/fasta-for-all-non-duf-exons.tab

