# How to run the analysis for Chimpanzee

## Nucleotide sequence based approach

At present, the exon annotations for chimpanzee are poor and most short exons are not annotated, so some changes to the normal flow are necessary. 

1. Modify the scripts/config.sh file to reflect the parameters for chimpanzee rather than human
2. Run ```bash scripts/workflow-1.sh```
3. Run ```bash scripts/workflow-2.sh```
4. Run ```bash scripts/get-fasta-non-human-long-exons.sh```
5. Combine the *fasta-for-chimp-long-duf-exons.fa* file with a fasta file of human exons with clade annotation, and modify the sequence names of the human ones so that Clustal Omega works 
```
grep -v "exon\|CE\|short" annotation-clade-based-numbering-2017-07-11.bed | awk 'BEGIN{OFS="\t"} {if ($7 > 130) print $0}' | bedtools getfasta -s -name -bed stdin -fi ~/LabProjects/hmmer-annotation/sequences/dna/dna-ucsc/human/hg38.fa -fo fasta-for-human-long-duf-exons-with-clade-names-nuc.fa

cat annotation/human/fasta-for-human-long-duf-exons-with-clade-names-nuc.fa annotation/panTrog-2017-09-22/fasta-for-chimp-long-duf-exons.fa > annotation/panTrog-2017-09-22/fasta-combined-human-chimp-long-exons-nuc.fa

sed 's/>[A-Z]/>chr1:N/g' annotation/panTrog-2017-09-22/fasta-combined-human-chimp-long-exons-nuc.fa > annotation/panTrog-2017-09-22/fasta-combined-human-chimp-long-exons-nuc-with-name-mod.fa
```

6. Align the fasta file of human and chimp long exons with Clustal Omega
7. Generate a distance matrix with Geneious, and export the distance matrix (this produces a csv file)
8. Use the python code I wrote to find the best human match for each chimp sequence

```
python scripts/find-best-human-match-to-non-human-sequence.py annotation/panTrog-2017-09-22/distance-matrix-human-chimp-long-exons-nuc.csv > annotation/panTrog-2017-09-22/chimp-to-human-best-matches.txt
```

9. Update the chimp bed file with the information on the best clade match

```
python scripts/update-non-human-bed-file-with-clades.py annotation/panTrog-2017-09-22/domain_cords_clean.bed annotation/panTrog-2017-09-22/chimp-to-human-best-matches.txt > annotation/panTrog-2017-09-22/chimp-long-exon-coords-with-clades.bed
```

10. Find the G4 sequences

10.1 Make nucleotide hmm of the G4 108bp exon using an alignment of the 108bp exon sequences from human
```
bash scripts/make-nucleotide-hmm-of-human-G4-108bp-exon.sh 
```

10.2 Search the non-human reference using this nucleotide hidden markov model
```
bash scripts/nhmmer-search-of-non-human-reference-for-G4108bpexon.sh

```
10.3 Clean up the G4 results

```
python scripts/convert-dtable-to-bed.py annotation/gorGor4-2017-09-22/G4108bp-search-of-gorGor4.dfamtblout .

sort -k 1,1 -k 2,2n domain-alignment-cords-all.bed | awk 'BEGIN {OFS="\t"} {if ($2 > $3) print $1,$3,$2,"G4","score",$4; else print $1,$2,$3,"G4","score",$4}' > annotation/panTrog-2017-09-22/g4-108bp-domain_cords_clean.bed
```

**NOTE** - This search return no hits matching the search criteria for panTro5, but does return 8 hits for panTro4

11. Integrate the coordinates of the G4 108bp matches with the BED file of DUF1220 long exons and see where they fall

```
cat  annotation/panTrog-2017-09-22/g4-108bp-domain_cords_clean.bed annotation/panTrog-2017-09-22/chimp-long-exon-coords-with-clades.bed | sort -k 1,1 -k 2,2n > annotation/panTrog-2017-09-22/combined-duf-long-and-g4-108-annotation.bed
```


## Nucleotide sequence based approach -  old

1. Make nucleotide HMM from alignment of full-domain (short exon, intron, long exon) sequences located and classified into clades for humans (This is taking a super long time to run)
2. Used that nucleotide HMM to do a nhmmer search of the chimpanzee reference genome
3. Locate G4s either by eye, or by doing a separate nhmmer analysis of just 108bp G4 exons and see where they show up

## Protein sequence based approach (probably not going to work that well because of failure to select correct translation
At present, the exon annotations for chimpanzee are poor and most short exons are not annotated, so some changes to the normal flow are necessary. 

1. Modify the scripts/config.sh file to reflect the parameters for chimpanzee rather than human
2. Run ```bash scripts/workflow-1.sh```
3. Run ```bash scripts/workflow-2.sh```
4. Run ```bash scripts/get-fasta-chimpanzee-long-exons.sh```
5. Make a blank file for short exons so that the follow-on script runs: ``` touch six-frame-translation-short-exons.fa ```
6. Run ```bash scripts/workflow-3.sh```
- Right now, this assigns clades for several, but not all domains - also the "select correct translation" script is failing for ~40 of the domains.  

- Approaches: 
-- After assigning clades where possible, make a phylogenetic tree of the remaining ones and assigned the un-assigned ones to the clade to which cluster - this works fairly well, but some don't cluster that well - might need to put in tree with human domains for confirmation - also, this doesn't work for the domains for which it is difficult to select a correct translation 
-- Align the nucleotide sequences with human sequences and see where things group

Note to self: might be able to make nucleotide hmm with DUF1220 short exons sequences just to locate all of the short exons - not necessarily to classify them, since I tried that and its ability to classify into clades isn't great.  But it could at least find the sequences.  
