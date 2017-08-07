#! /usr/bin/env bash

source scripts/config.sh

# Generate hidden markov model
hmmbuild -n $hmm_name $hmm $seqs_for_hmm

# Locate DUF1220 domains in the proteome file
bash scripts/hmmsearch-vs-pep-all-longest.sh $hmm

# Make nucleotide hidden markov model based on the results of the proteome search
bash scripts/get-all-positions.sh

# Locate DUF1220 domains in the reference genome
bash scripts/nhmmer-vs-dna-ucsc.sh

# Intersect HMMER hit coordinates with reference annotations
## Intersect with RefSeq annotation
bash scripts/intersect-with-reference-annotations.sh results/nhmmer-vs-dna/duf1220-vs-$ref.dfamtblout $annotation_dir/ $refseq_dir/$species-exons-refseq-sorted-merged.bed $refseq_dir/$species-cds-refseq-sorted-merged.bed $refseq_dir/$species-genes-refseq-sorted.bed refseq

## Intersect with Ensembl annotation
bash scripts/intersect-with-reference-annotations.sh results/nhmmer-vs-dna/duf1220-vs-$ref.dfamtblout $annotation_dir/ $ensembl_dir/$species-exons-ensembl-sorted-merged.bed $ensembl_dir/$species-cds-ensembl-sorted-merged.bed $ensembl_dir/$species-genes-ensembl-sorted.bed ensembl

# Group short and long exons and perform initial annotation

## initial annotation for refseq
bash scripts/exon-annotation-wrapper.sh $annotation_dir/all-relevant-exons-clean-refseq.bed $annotation_dir/ refseq

## initial annotation for ensembl
bash scripts/exon-annotation-wrapper.sh $annotation_dir/all-relevant-exons-clean-ensembl.bed $annotation_dir/ ensembl

# Combine the RefSeq and Ensembl annotations in a way that gives the best annotations for each gene
bash scripts/combine-refseq-ensembl-wrapper.sh $annotation_dir/annotated-nbpf-exons-all-doublets-refseq.bed $annotation_dir/annotated-nbpf-exons-all-doublets-ensembl.bed $ref_anno_dir/reference-selection-by-gene.csv $annotation_dir/

# Using the combined BED filed, get the FASTA sequences for DUF exons

bash scripts/get-fasta-all-duf-exons.sh $annotation_dir/combined-refseq-ensembl-annotation.bed $dna_dir/$ref.fa $annotation_dir/
