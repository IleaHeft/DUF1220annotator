# DUF1220annotator

DUF1220annotator is a toolkit for locating the coordinates of DUF1220 domains in a reference genome and assigning them to the appropriate DUF1220 subytpe/clade. 

This code was used to generate the DUF1220 annotations utilized in:

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
All of the underlying scripts have been packaged into three workflow scripts, with a supporting config.sh script to specify file paths, and directories.  You should modify the config.sh script as necessary to match your directory set-up.  

- workflow-1.sh  
- workflow-2.sh  
- workflow-3.sh  

Step 1:  
```
bash workflow-1.sh
```
Step 2:
```
bash workflow-2.sh
```
Use 
