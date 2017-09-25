# How to run the analysis for non-human primates

## Nucleotide sequence based approach

At present, the exon annotations for non-human priamtes are poor and most short exons are not annotated, so some changes to the normal flow are necessary. 

1. Modify the scripts/config.sh file to reflect the parameters for the non-human species you are analyzing - notably, make sure to change both the "species" and the "ref" parameters as desired
2. Run ```bash scripts/workflow-1.sh```
3. Run ```bash scripts/workflow-2.sh```
4. Run ```bash scripts/get-fasta-non-human-long-exons.sh```
5. Combine the non-human long exon fasta file with a fasta file of human exons with clade annotation, and modify the sequence names of the human ones so that Clustal Omega works 

*If you need to make a fasta file of the human long exons, run this first, otherwise, skip to the code below*
```
grep -v "exon\|CE\|short" annotation-clade-based-numbering-2017-07-11.bed | awk 'BEGIN{OFS="\t"} {if ($7 > 130) print $0}' | bedtools getfasta -s -name -bed stdin -fi ~/LabProjects/hmmer-annotation/sequences/dna/dna-ucsc/human/hg38.fa -fo fasta-for-human-long-duf-exons-with-clade-names-nuc.fa
```

```
bash scripts/combine-human-and-non-human-fasta-files.sh 
```

6. Align the fasta file of human and chimp long exons with Clustal Omega

7. Generate a distance matrix with Geneious, and export the distance matrix (this produces a csv file)

8. Use the python code I wrote to find the best human match for each chimp sequence and update the non-human bed file with the information on the best match 

```
bash scripts/find-best-clade-match-for-non-human-and-update-bed.sh 
```

10. Find the G4 sequences

10.1 Make nucleotide hmm of the G4 108bp exon using an alignment of the 108bp exon sequences from human
```
bash scripts/make-nucleotide-hmm-of-human-G4-108bp-exon.sh 
```

10.2 Search the non-human reference using this nucleotide hidden markov model and make a file that merges the G4 coordinates with the long exon coordinates
```
bash scripts/nhmmer-search-of-non-human-reference-for-G4108bpexon.sh

```
