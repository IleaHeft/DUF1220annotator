#!/usr/bin/env bash

# Set variables for HMMER annotation workflow

# RefSeq files

refseq_gff3=data/reference-annotations/refseq/GCF_000001405.35_GRCh38.p9_genomic.gff
refseq_assembly_report=data/reference-annotations/refseq/GCF_000001405.35_GRCh38.p9_assembly_report.txt


# Ensembl GTF file
ensembl_gtf=data/reference-annotations/ensembl/Homo_sapiens.GRCh38.86.gtf

# Hidden Markov Model

seqs_for_hmm=data/pfam-seed-domains/PF06758_seed_20151113_human.txt
hmm_name=duf1220_seed
hmm=hidden-markov-models/PF06758_seed_20151113_human.hmm
