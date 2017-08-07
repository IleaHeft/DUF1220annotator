#!/usr/bin/env bash

# Set variables for HMMER annotation workflow
# Note all the variables for human are specified upfront, and then below that I've build in an option that uses a different set of variables if the species is non-human

# Set todays date
today=$(date +"%Y-%m-%d")

# For human, use human, for chimp, use panTrog
species=human



# Reference annotation directory
ref_anno_dir=~/LabProjects/hmmer-annotation/data/reference-annotations

# Hidden Markov Model
pfam_seed_original=~/LabProjects/DUF1220annotator/data/pfam-seed-domains/pfam-seed-all-20170710.txt
pfam_dir=~/LabProjects/DUF1220annotator/data/pfam-seed-domains/
seqs_for_hmm=$pfam_seed_original
hmm_name=duf1220_seed
hmm=hidden-markov-models/pfam_seed_20170710.hmm

# Filename settings
## directory to print annotation files to
annotation_dir=annotation/$species-$today

if [ ! -d $annotation_dir ];then
    mkdir $annotation_dir
fi


# file name of six-frame-translation-short-exons and six-frame-translation-long-exons, and the six-frame-all file
six_frame_short=six-frame-translation-short-exons.fa
six_frame_long=six-frame-translation-long-exons.fa
six_frame_all=six-frame-translation-all-exons.fa

# file names
fasta_transl_doublets_and_lone=fasta-for-translated-protein-doublets-and-lone-sequences.fa
fasta_all_non_duf=fasta-for-all-non-duf-exons.fa
combo_refseq_ensembl_bed=combined-refseq-ensembl-annotation.bed

#file with clades added
annotation_domain_numbering=annotation-domain-based-numbering.bed
fasta_protein_domains_with_clades=fasta-for-protein-domains-with-clades.fa

# settings for HUMAN
ref=hg38

# RefSeq directory and files

refseq_dir=~/LabProjects/hmmer-annotation/data/reference-annotations/refseq/human
refseq_gff3=$refseq_dir/GCF_000001405.35_GRCh38.p9_genomic.gff
refseq_assembly_report=$refseq_dir/GCF_000001405.35_GRCh38.p9_assembly_report.txt

# Ensembl dir and GTF file

ensembl_dir=~/LabProjects/hmmer-annotation/data/reference-annotations/ensembl/human
ensembl_gtf=$ensembl_dir/Homo_sapiens.GRCh38.86.gtf

# directory that holds proteome files
proteome_dir=~/LabProjects/hmmer-annotation/sequences/pep/human

# cdna directory
cdna_dir=~/LabProjects/hmmer-annotation/sequences/cdna/human

# dna directory (holds the reference fasta file, e.g. hg38.fa)
dna_dir=~/LabProjects/hmmer-annotation/sequences/dna/dna-ucsc/human

