#!/usr/bin/env bash

# Set variables for HMMER annotation workflow

# Set todays date
today=$(date +"%Y-%m-%d")

# Reference annotation directory
ref_anno_dir=~/LabProjects/hmmer-annotation/data/reference-annotations


# RefSeq directory and files

refseq_dir=~/LabProjects/hmmer-annotation/data/reference-annotations/refseq/human
refseq_gff3=$refseq_dir/GCF_000001405.35_GRCh38.p9_genomic.gff
refseq_assembly_report=$refseq_dir/GCF_000001405.35_GRCh38.p9_assembly_report.txt


# Ensembl dir and GTF file
ensembl_dir=~/LabProjects/hmmer-annotation/data/reference-annotations/ensembl/human
ensembl_gtf=$ensembl_dir/Homo_sapiens.GRCh38.86.gtf

# Hidden Markov Model
pfam_seed_original=~/LabProjects/DUF1220annotator/data/pfam-seed-domains/PF06758_seed_20151113.txt
pfam_dir=~/LabProjects/DUF1220annotator/data/pfam-seed-domains/
seqs_for_hmm=data/pfam-seed-domains/PF06758_seed_20151113_human.txt
hmm_name=duf1220_seed
hmm=hidden-markov-models/PF06758_seed_20151113_human.hmm

# directory that holds proteome files
proteome_dir=~/LabProjects/hmmer-annotation/sequences/pep/human

# cdna directory
cdna_dir=~/LabProjects/hmmer-annotation/sequences/cdna/human

# dna directory (holds hg38.fa)
dna_dir=~/LabProjects/hmmer-annotation/sequences/dna/dna-ucsc

# directory to print annotation files to
annotation_dir=annotation

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

