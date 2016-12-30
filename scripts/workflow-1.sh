#!/usr/bin/env bash

source scripts/config.sh

#Action: Using the starting proteome file, make a new file that contains only the logest isoforms of each protein

#Script: _get-longest-isoform.py_ (Credit to Zimmer & Montgomery, 2015) 

#Inputs:
##Path to folder that contains the original, unzipped, proteome files   
##The output location (in this case, the same as the original folder where the proteome files are  

echo "Getting longest isoforms from proteome"
python scripts/get-longest-isoform.py $proteome_dir $proteome_dir 

####################

# Action: Generate BED files of reference exon, gene, and coding sequence annotations (RefSeq and Ensembl)

# Script: _convert-gff3-or-gtf-to-bed-files.py_ 
# Actions: _convert-gff3-or-gtf-to-bed-files.py_ Extracts the coordinates and relevant annotation data from the GFF3 or GTF file and puts it in BED file format.

# Input:  
##  Path to the GFF3 or GTF file
## Species name, as you want it to be shown in output file names (e.g. "human")
## Refence name, either "refseq" or "ensembl"
## If using refseq, give the path to the assembly report, if ensembl, give the folder where you want the output to go
## If using refseq, give the folder where you want the output to go

# Output:
## $species-exons-$reference.bed  
## $species-genes-$reference.bed  
## $species-cds-$reference.bed  
## For Ensembl only: $species-utr-$reference.bed (The RefSeq file doesn't have this information in

# Run for RefSeq

echo "Converting RefSeq GFF3 to BED"

python scripts/convert-gff3-or-gtf-to-bed-files.py \
$refseq_gff3 \
human \
refseq \
$refseq_assembly_report \
$refseq_dir/

# Run for Ensembl

echo "Converting Ensembl GTF to BED"

python scripts/convert-gff3-or-gtf-to-bed-files.py $ensembl_gtf human ensembl $ensembl_dir/

####################

#Action: Sort and merge the BED files in preparation for future use

# Script: _sort-and-merge-reference-annotation-bed-files.sh_

# Actions:  
## Sorts and merges the BED files created with the python script above so that they are ready for use in future bedtools intersect operations.  

# Input:
## The folder that contains the output files from the previous step - with no "/" on the end  
## Species, as above (e.g. "human")  
## Reference annotation, as above - either "refseq" or "ensembl" 

# Output:  
## $species-genes-$reference-sorted.bed  
## $species-exons-$reference-sorted-merged.bed  
## $species-cds-$reference-sorted-merged.bed  
## For Ensembl Only: $species-utr-$reference-sorted-merged.bed  (The script will attempt to create this file for RefSeq, and you will get an error message from the bedtools merge step, because the input file for this step does not exist for RefSeq)  

# Run for Refseq  
echo "Sorting & merging RefSeq BED files"

bash scripts/sort-and-merge-reference-annotation-bed-files.sh $refseq_dir human refseq


#Run for Ensembl
echo "Sorting & merging Ensembl BED files"

bash scripts/sort-and-merge-reference-annotation-bed-files.sh $ensembl_dir human ensembl

####################

# Action: From the full set of DUF1220 seed domains, extract out only the seed domains annotated as being human by running the below code:  

# Script: _select-human-seed-domains.py_  
# Input:  
## original file of all PFAM seed domains  
## the output folder  

echo "Generating a file of human seed domains"

python scripts/select-human-seed-domains.py $pfam_seed_original $pfam_dir 

####################

#Prepatory steps are now complete, run workflow-par
