# DUF1220annotator

DUF1220annotator is a toolkit for locating the coordinates of DUF1220 domains in a reference genome and assigning them to the appropriate DUF1220 subytpe/clade. 

This code was used to generate the DUF1220 annotations utilized in the forthcoming paper:

> Astling, DP, Heft IE, Jones, KL, Sikela, JM. "High resolution measurement of DUF1220 domain copy number from whole genome sequence data"

# Dependancies

DUF1220annotator currently requires the below software to run

- [Python 2.7.10](https://www.python.org/downloads/)  
- [HMMER 3.1b2](http://hmmer.org/)   
- [Go 1.7.3 darwin/amd64](https://golang.org/dl/)  
- [MAFFT 7.245](http://mafft.cbrc.jp/alignment/software/macstandard.html)   

Required files include:
- The fasta file for your reference genome (e.g. hg38)  
- A proteome file for your species  
- A cdna file for your species  
- RefSeq GFF file  
- Ensembl GTF file  

# Getting Started 
All of the underlying scripts have been packaged into three workflow scripts, with a supporting config.sh script to specify file paths and directories.  You should modify the config.sh script as necessary to match your directory set-up. Detailed information on each of the underlying scripts can be found in docs/DUF1220annotator-detailed-doc.md  

- workflow-1.sh  
- workflow-2.sh  
- workflow-3.sh  

## Step 1:  
```
bash scripts/workflow-1.sh
```
## Step 2:
```
bash scripts/workflow-2.sh
```
## Step 3:  

Run the *fasta-for-all-short-exons-nuc.fa* and *fasta-for-all-long-exons-nuc.fa* files through [Transeq](http://www.ebi.ac.uk/Tools/st/emboss_transeq/) for all 6 frames, download the files, and save them as *six-frame-translation-short-exons.fa* and *six-frame-translation-long-exons*.fa

## Step 4: 
```
bash scripts/workflow-3.sh
```

## Step 5:
Visually confirm the validity of the clade assignments by aligning the file *fasta-for-protein-domains-clade-based-numbering.fa* with [Clustal Omega](http://www.ebi.ac.uk/Tools/msa/clustalo/) and save as *aligned-pro-domain-w-clades.aln*. Generate a phylogenetic tree is helpful (if desired).  

Might also want to perform the above steps with the fasta file that inludes "lone" protein sequences: *fasta-for-protein-domains-and-lone-with-clades.fa* and save as *aligned-protein-doublets-and-lone-with-clades.aln*

