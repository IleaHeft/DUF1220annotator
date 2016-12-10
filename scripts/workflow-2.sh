#! /usr/bin/env bash

source scripts/config.sh

# Generate hidden markov model
hmmbuild -n $hmm_name $hmm $seqs_for_hmm

# Locate DUF1220 domains in the proteome file
bash scripts/hmmsearch-vs-pep-all-longest.sh $hmm human

# Make nucleotide hidden markov model based on the results of the proteome search
#bash scripts/get-all-positions.sh human

# Locate DUF1220 domains in the reference genome
#bash scripts/nhmmer-vs-dna-ucsc.sh

# Intersect HMMER hit coordinates with reference annotations
## Intersect with RefSeq annotation
#bash scripts/intersect-with-reference-annotations.sh 2016-11-12-nhmmer-vs-dna/duf1220-vs-hg38.dfamtblout annotations/2016-11-12-human-domain-annotation/ data/reference-annotations/refseq/human/human-exons-refseq-sorted-merged.bed data/reference-annotations/refseq/human/human-cds-refseq-sorted-merged.bed data/reference-annotations/refseq/human/human-genes-refseq-sorted.bed refseq

## Intersect with Ensembl annotation
#bash scripts/intersect-with-reference-annotations.sh 2016-11-12-nhmmer-vs-dna/duf1220-vs-hg38.dfamtblout annotations/2016-11-12-human-domain-annotation/ data/reference-annotations/ensembl/human/human-exons-ensembl-sorted-merged.bed data/reference-annotations/ensembl/human/human-cds-ensembl-sorted-merged.bed data/reference-annotations/ensembl/human/human-genes-ensembl-sorted.bed ensembl

# Group short and long exons and perform initial annotation

## initial annotation for refseq
#bash scripts/exon-annotation-wrapper.sh annotations/2016-11-12-human-domain-annotation/all-relevant-exons-clean-refseq.bed annotations/2016-11-12-human-domain-annotation/ refseq

## initial annotation for ensembl
#bash scripts/exon-annotation-wrapper.sh annotations/2016-11-12-human-domain-annotation/all-relevant-exons-clean-ensembl.bed annotations/2016-11-12-human-domain-annotation/ ensembl

# Combine the RefSeq and Ensembl annotations in a way that gives the best annotations for each gene
#bash scripts/combine-refseq-ensembl-wrapper.sh annotations/2016-11-12-human-domain-annotation/annotated-nbpf-exons-all-doublets-refseq.bed annotations/2016-11-12-human-domain-annotation/annotated-nbpf-exons-all-doublets-ensembl.bed data/reference-annotations/reference-selection-by-gene.csv annotations/2016-11-12-human-domain-annotation/

# Using the combined BED filed, get the FASTA sequences for DUF exons

#bash scripts/get-fasta-all-duf-exons.sh annotations/2016-11-12-human-domain-annotation/combined-refseq-ensembl-annotation-2016-11-29.bed sequences/dna/dna-ucsc/hg38.fa annotations/2016-11-12-human-domain-annotation/
