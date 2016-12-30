#! /usr/bin/env bash

source scripts/config.sh


cat $annotation_dir/$six_frame_short $annotation_dir/$six_frame_long > $annotation_dir/$six_frame_all


python scripts/select-correct-translation-and-combine-doublets.py $annotation_dir/$six_frame_all $annotation_dir/

python scripts/give-aligned-seqs-clade-names-and-conserved-exon-groups.py $annotation_dir/$fasta_transl_doublets_and_lone $annotation_dir/$fasta_all_non_duf $annotation_dir/$combo_refseq_ensembl_bed $annotation_dir/

bash scripts/number-domains-according-to-clade.sh $annotation_dir/$annotation_domain_numbering  $annotation_dir/$fasta_protein_domains_with_clades $annotation_dir/
