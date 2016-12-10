#! /usr/bin/env bash

##########################################
# Purpose: Intersect the HMMER domain coordinates with RefSeq gene and exon coordinates (the program first sorts the list of domains and make sure that all start positions are before end positions
# Inputs:
#   (1) the domain table out results of the nhmmer search
#   (2) the output foler for all of the operations on the domains (e.g. cleaning them up, figuring out their exons, etc)
#   (3) the file of exon annotations
#   (4) the file of gene annotations
#   (5) the type of reference being used, RefSeq or Ensemble
#   (6) the fasta file to use to get sequence information



domains=$1
output_folder=$2
exons=$3
cds=$4
genes=$5
reference=$6
#domain_bed=$3
#fasta=$6

#Conver the HMMER outbput to BED file format
python scripts/convert-dtable-to-bed.py $domains $output_folder 

# Sort and format the bed file produced from the python script
sort -k 1,1 -k 2,2n $output_folder/domain-alignment-cords-all.bed | \
awk 'BEGIN {OFS="\t"} {if ($2 > $3) print $1,$3,$2,"name","score",$4; else print $1,$2,$3,"name","score",$4}' > $output_folder/domain_cords_clean.bed

####################
# Exons that are intersected by a domain

bedtools intersect -b  $output_folder/domain_cords_clean.bed -a $exons -wa  |  \
bedtools merge -i stdin -c 4,6 -o distinct | \
awk 'BEGIN {OFS = "\t"} {print $1,$2,$3,$4,$3-$2,$5,"hit"}' > $output_folder/exons-intersected-by-domain-$reference.bed 



###################
# Identify domains found by HMMER that don't overlap any annotated exon and then annotate the gene within which that domain is found.  
#bedtools intersect -v -a $output_folder/domain_cords_clean.bed -b $exons -wa -wb > $output_folder/domains-not-intersecting-exons-$reference.bed

bedtools intersect -v -a $output_folder/domain_cords_clean.bed -b $exons -wa -wb | bedtools intersect -a stdin -b $genes -wa -wb |\
awk 'BEGIN {OFS = "\t"} {print $1,$2,$3,$10,$3-$2,$6,"hit-ena"}' > $output_folder/domains-not-intersecting-exons-$reference.bed

# {print $1,$2,$3,$8,$10,"hit-ena", $3-$2}

#Identify domains fround by HMMER that don't overlap any annotated exon OR any annotated gene (which happens with refseq), and add those to list of hits


bedtools intersect -v -a $output_folder/domain_cords_clean.bed -b $genes -wa -wb | \
awk 'BEGIN {OFS = "\t"} {print $1,$2,$3,"gna",$3-$2,$6,"hit-ena"}' > $output_folder/domains-not-intersecting-any-gene-$reference.bed


cat $output_folder/exons-intersected-by-domain-$reference.bed $output_folder/domains-not-intersecting-exons-$reference.bed $output_folder/domains-not-intersecting-any-gene-$reference.bed | \
cut -f 4 | cut -f 1 -d "," | sort | uniq > $output_folder/genes-with-hits-$reference.bed



# Print exons of all genes with "hits" that are not intersected by a HMMER hit 
bedtools intersect -v -a $exons -b $output_folder/domain_cords_clean.bed | \
awk 'BEGIN {OFS = "\t"} {print $1,$2,$3,$4,$3-$2,$6,"not-hit"}' > $output_folder/exons-not-hit-by-domain-$reference.bed


rm $output_folder/not-hit-exons-from-relevant-genes-$reference.bed
touch $output_folder/not-hit-exons-from-relevant-genes-$reference.bed

for i in $(cut -f 1 $output_folder/genes-with-hits-$reference.bed);
    do
        echo $i
        grep -w $i $output_folder/exons-not-hit-by-domain-$reference.bed >> $output_folder/not-hit-exons-from-relevant-genes-$reference.bed
    
    done



# Combine all of the exons with a hmmer hit, all of the non-hit exons from genes that have a hit, all of the hits that don't overlap an annotated exon, and all of the hits that don't overlap any gene
# Also manually include all exons from NBPF18P - there is a CON1 short exon in this gene (but no long exon)

grep "NBPF18P" $exons | awk 'BEGIN{OFS="\t"} {print $1,$2,$3,$4,$3-$2,$6,"not-hit"}' > nbpf18p-exons-$reference.bed

cat $output_folder/exons-intersected-by-domain-$reference.bed $output_folder/not-hit-exons-from-relevant-genes-$reference.bed \
$output_folder/domains-not-intersecting-exons-$reference.bed $output_folder/domains-not-intersecting-any-gene-$reference.bed nbpf18p-exons-$reference.bed|\
sort -k 1,1 -k 2,2n > $output_folder/all-relevant-exons-$reference.bed

# Perform these steps to create an annotation file with information on coding status (according to the reference annotation being used)

bedtools intersect -u -a $output_folder/all-relevant-exons-$reference.bed -b $cds | awk '{print $0,"\t","C"}' > $output_folder/all-relevant-exons-coding-$reference.bed
bedtools intersect -v -a $output_folder/all-relevant-exons-$reference.bed -b $cds | awk '{print $0,"\t","NC"}' > $output_folder/all-relevant-exons-non-coding-$reference.bed
cat $output_folder/all-relevant-exons-coding-$reference.bed $output_folder/all-relevant-exons-non-coding-$reference.bed |\
sort -k 1,1 -k 2,2n | uniq  > $output_folder/all-relevant-exons-with-coding-annotated-$reference.bed

#Run this script to clean up gene names where there is more than one gene listed (an artefact of the bedtools merge steps that create the reference annotation bed files
python scripts/clean-gene-names.py $output_folder/all-relevant-exons-with-coding-annotated-$reference.bed > $output_folder/all-relevant-exons-clean-$reference.bed

# Generates a handy file of the number of hits per gene
grep -v "not-hit" $output_folder/all-relevant-exons-hit-nohit-$reference.bed | bedtools groupby -i stdin -g 4 -c 1 -o count > $output_folder/domains-per-gene-stats-$reference.bed

