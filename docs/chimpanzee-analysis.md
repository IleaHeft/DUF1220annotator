# How to run the analysis for Chimpanzee

## Nucleotide sequence based approach

At present, the exon annotations for chimpanzee are poor and most short exons are not annotated, so some changes to the normal flow are necessary. 

1. Modify the scripts/config.sh file to reflect the parameters for chimpanzee rather than human
2. Run ```bash scripts/workflow-1.sh```
3. Run ```bash scripts/workflow-2.sh```
4. Run ```bash scripts/get-fasta-chimpanzee-long-exons.sh```
5. Combine the *fasta-for-chimp-long-duf-exons.fa* file with a fasta file of human exons with clade annotation, and modify the sequence names of the human ones so that Clustal Omega works 
```
grep -v "exon\|CE\|short" annotation-clade-based-numbering-2017-07-11.bed | awk 'BEGIN{OFS="\t"} {if ($7 > 130) print $0}' | bedtools getfasta -s -name -bed stdin -fi ~/LabProjects/hmmer-annotation/sequences/dna/dna-ucsc/human/hg38.fa -fo fasta-for-human-long-duf-exons-with-clade-names-nuc.fa

cat ../human/fasta-for-human-long-duf-exons-with-clade-names-nuc.fa fasta-for-chimp-long-duf-exons.fa > fasta-combined-human-chimp-long-exons-nuc.fa

sed 's/>[A-Z]/>chr1:N/g' fasta-combined-human-chimp-long-exons-nuc.fa > fasta-combined-human-chimp-long-exons-nuc-with-name-mod.fa
```

5. Make a blank file for short exons so that the follow-on script runs: ``` touch six-frame-translation-short-exons.fa ```
6. Run ```bash scripts/workflow-3.sh```

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
