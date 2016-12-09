## DUF1220 Annotation Pipeline from Astling, 2016/2017

Software versions used:  
- [Python 2.7.10](https://www.python.org/downloads/)  
- [HMMER 3.1b2](http://hmmer.org/)   
- [Go 1.7.3 darwin/amd64](https://golang.org/dl/)  
- [MAFFT 7.245](http://mafft.cbrc.jp/alignment/software/macstandard.html)   

Background/reference data used:  
- Proteome
- Reference genome, GRCh38,`wget http://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/hg38.fa.gz`
- cDNA data: 
- RefSeq gene/exon annotation data:  
-- \*genomic.gff.gz
```
wget ftp://ftp.ncbi.nlm.nih.gov/genomes/refseq/vertebrate_mammalian/Homo_sapiens/latest_assembly_versions/GCF_000001405.35_GRCh38.p9/GCF_000001405.35_GRCh38.p9_genomic.gff.gz
```
-- \*assembly_report.txt 
```
wget ftp://ftp.ncbi.nlm.nih.gov/genomes/refseq/vertebrate_mammalian/Homo_sapiens/latest_assembly_versions/GCF_000001405.35_GRCh38.p9/GCF_000001405.35_GRCh38.p9_assembly_report.txt
```
- Ensembl gene/exon annotation data:
```
 wget ftp://ftp.ensembl.org/pub/release-86/gtf/homo_sapiens/Homo_sapiens.GRCh38.86.gtf.gz
```
- PFAM seed domains

#### Steps
1. Clone repository  
2. Run _human-hmmer-annotation-prep.sh_  
3. Run _human-hmmer-annotation-workflow-part1.sh_
4. 
5. Run _human-hmmer-annotation-workflow-part2.sh_


Note: Code from Montgomery & Zimmer, 2015 (https://github.com/qfma/duf1220)
The exon and gene annotation files from Ensembl and RefSeq, processed into sorted, merged files using my code

**Script:** _convert-gff3-or-gtf-to-bed-files.py_ 
**Actions:**  
- _convert-gff3-or-gtf-to-bed-files.py_ Extracts the coordinates and relevant annotation data from the GFF3 or GTF file and puts it in BED file format.  Will need to run once for RefSeq and once for Ensembl  

**Input:**  
1. Path to the GFF3 or GTF file
2. Species name, as you want it to be shown in output file names (e.g. "human")
3. Refence name, either "refseq" or "ensembl"
4. If using refseq, give the path to the assembly report, if ensembl, give the folder where you want the output to go
5. If using refseq, give the folder where you want the output to go

**Output:**  
- $species-exons-$reference.bed  
- $species-genes-$reference.bed  
- $species-cds-$reference.bed  
- For Ensembl only: $species-utr-$reference.bed (The RefSeq file doesn't have this information in it)  

**Example Usage for RefSeq:**
```
python scripts/convert-gff3-or-gtf-to-bed-files.py data/reference-annotations/refseq/human/GCF_000001405.35_GRCh38.p9_genomic.gff human refseq data/reference-annotations/refseq/human/GCF_000001405.35_GRCh38.p9_assembly_report.txt data/reference-annotations/refseq/human/
```

**Example Usage for Ensembl:**
```
python scripts/convert-gff3-or-gtf-to-bed-files.py data/reference-annotations/ensembl/human/Homo_sapiens.GRCh38.86.gtf human ensembl data/reference-annotations/ensembl/human/
```
##### Sort and merge the BED files in preparation for future use
**Script:** _sort-and-merge-reference-annotation-bed-files.sh_
**Actions:**  
- _sort-and-merge-reference-annotation-bed-files.sh_ Sorts and merges the BED files created with the python script above so that they are ready for use in future bedtools intersect operations. Will need to run once for RefSeq and once for Ensembl  
**Input:**
1. The folder that contains the output files from the previous step - with no "/" on the end  
2. Species, as above (e.g. "human")  
3. Reference annotation, as above - either "refseq" or "ensembl" 
**Output:**  
- $species-genes-$reference-sorted.bed  
- $species-exons-$reference-sorted-merged.bed  
- $species-cds-$reference-sorted-merged.bed  
- For Ensembl Only: $species-utr-$reference-sorted-merged.bed  (The script will attempt to create this file for RefSeq, and you will get an error message from the bedtools merge step, because the input file for this step does not exist for RefSeq)  

**Example Usage RefSeq:**  
```
bash scripts/sort-and-merge-reference-annotation-bed-files.sh data/reference-annotations/refseq/human human refseq
```
**Example Usage Ensembl:**
```
bash scripts/sort-and-merge-reference-annotation-bed-files.sh data/reference-annotations/ensembl/human human ensembl
```


### Download the PFAM seed domains and select out only the human seed domains
Download the DUF1220 seed domains from the [PFAM website](http://pfam.xfam.org/family/DUF1220#tabview=tab3)

I renamed the seed domain file to: PF06758_seed_20151113.txt

From the full set of DUF1220 seed domains, extract out only the seed domains annotated as being human by running the below code:  
**Script:** _select-human-seed-domains.py_  
**Input:**  
1) original file of all PFAM seed domains  
2) the output folder  

**Example usage:**  
```
python scripts/select-human-seed-domains.py data/seed-alignments/PF06758_seed_20151113.txt data/seed-alignments/ 
```

## Locate DUF1220 domains in the reference genomes provided using HMMER:

### Build a hidden markov model of DUF1220 using hmmbuild:
**Command:** hmmbuild  
**Input:**  
-n: The name you want to give to your hidden markov model  
1) The output path and file name that you want your hidden markov model to have  
2) The PFAM seed domain file  

**Example Usage:**
```
hmmbuild -n duf1220_seed hidden-markov-models/PF06758_seed_20151113_human.hmm data/seed-alignments/PF06758_seed_20151113_human.txt
```
**Example Usage for generating hidden markov model based on ALL PFAM domains, not just the human ones:**  

```
hmmbuild -n duf1220_seed hidden-markov-models/PF06758_seed_20151113_all.hmm data/seed-alignments/PF06758_seed_20151113.txt
```
### Locate DUF1220 domains in the proteome files
**Script:** _hmmsearch-vs-pep-all-longest.sh_ (Montgomery & Zimmer, 2015)  
**Actions:** searches all proteomes in the folder that you provide for matches to the hidden markov model with E less than 1e-10  
**Input:**  
1) The hidden markov model you previously generated   
2) "human" or "non-human" (I have the human files in their own folder and the non-human files in a separate folder)    

**Output:**  
- Folder: "Today's Date"-hmmsearch-vs-pep-all-longest/    
- Files: For each proteome searched, a "domtblout" and "tblout" file that reportes the DUF1220 "hits"  

**Example Usage:**    
``` 
bash scripts/hmmsearch-vs-pep-all-longest.sh hidden-markov-models/PF06758_seed_20151113_human.hmm human
```
**Example Usage - using hidden markov model generated with ALL PFAM seed domains, not just human ones:**
```
bash scripts/hmmsearch-vs-pep-all-longest.sh hidden-markov-models/PF06758_seed_20151113_all.hmm non-human
```
### Make nucleotide hidden markov model using proteome hit data and cDNA data
**Script:** _get-all-positions.sh_ (Montgomery & Zimmer, 2015)  

**Actions:** Using the proteome hit coordinates, this script obtains the corresponding cDNA coordinates in the cDNA file, and from the cDNA file, it extracts the nucleotide sequences coding for the proteim domain hits, and then using those nucleotide sequences to produce a nucleotide hidden markov model that will subsequently be used to search the genome  

**Input:**  
1. "human" or "non-human" (I have the human files in their own folder and the non-human files in a separate folder)    

**Output:**  
Folder: "Today's Date"-duf1220-all-ensembl-nucl/  
Files:  
- A nucleotide hidden markov model for the DUF1220 domains  
**Example Usage:**  
```
bash scripts/get-all-positions.sh human
```
### Locate DUF1220 domains in the reference genome
**Script:** _nhmmer-vs-dna-ucsc.sh_ (Montgomery & Zimmer, 2015)  - _nhmmer-vs-dna-ucsc.sh_ searches the fasta file downloaded from UCSC Genome Browser, as an alternative, I've coded _nhmmer-vs-dna.sh_ to search the Ensemble fasta file    
**Actions:**: Using the nucleotide hidden markov model generated with _get-all-positions.sh_ above, this script searches for hits 
in the reference genome (hg38.fa). 
**Input:**
- None, the script automatically looks for the appropriate files in certain folders (if you file set-up follows the convention in the script, there is nothing else you need to provide)   
**Output:**
Folder: "Today's Date"-nhmmer-vs-dna  
Files: The nucleotide positions of all "hits" in the genome (duf1220-vs-hg38.dfamtblout, duf1220-vs-hg38.tblout)

**Example Usage:**  
```
bash scripts/nhmmer-vs-dna-ucsc.sh
```
**Example Usage for searching in non-human DNA -- I've coded this version to search in a specific folder of non-human genomes**  
```
bash scripts/nhmmer-vs-dna-ucsc-non-human.sh 
```
### Annotate the DUF1220 hits identified by HMMER

#### Convert HMMER results to exon coordinate BED files

Make a directory for the annotations
Example: annotations/"Todays Date-domain-annotation"

**Script:** _intersect-with-reference-annotations.sh_  You will run this command once against the RefSeq annotations and once against the Ensemble annotations

**Actions:**  
- Calls _convert-dtable-to-bed-10-19-15.py_ to convert the HMMER output format to a BED file format  
- Performs different bedtools interesect operations to conver HMMER coordinates to exon coordinates and identify the genes that contain hits as well as the "not-hit" exons within those genes  


**Inputs:**

1. the dfamtblout file produced by HMMER  
2. the location of the output folder  
3. the reference exon annotation file to use  
4. the reference gene annotation file to use  
5. the name of the annotation being used (e.g. refseq, ensembl)  

**Outputs:**  

Intermediate Files:  

- domain_cords_clean.bed: presents HMMER coordinates in bed file format  
- exons-intersected-by-domain-$reference.bed: gives coordinates of all exons in the reference you searched (RefSeq or Ensemble) that are overlapped by the HMMER hit coordinates  
- domains-not-intersecting-exons-$reference.bed: coordinates of HMMER hits that don't overlap annotated exons, but do overlap an annotated gene 
- domains-not-intersecting-any-gene-$reference.bed: coordinates of HMMER hits that don't overlap any annotated exon OR any annotated gene
- genes-with-hits-$reference.bed: list of all genes having a hit  
- exons-not-hit-by-domain-$reference.bed: all exons (in the exon reference used) that aren't overlapped by a HMMER hit
- not-hit-exons-from-relevant-genes-$reference.bed: all exons, from genes WITH a HMMER hit, that aren't overlapped by a HMMER hit
- domains-intersecting-genes-$reference.bed:
- domains-not-intersecting-genes-$reference.bed:

Files for futher analysis/use:
- all-relevant-exons-hit-nohit-$reference.bed: Has the coordinates of all exons that were overlapped by a HMMER hit, all non-hit exons from the genes that contain hits, and the full HMMER coordiantes for any hits that don't overlap an exon or a gene  

Handy reference information:
- duf1220-containing-gene-cords-$reference.bed: full gene-lengths coordinates for any gene that contains a HMMER hit
- domains-per-gene-stats-$reference.bed: a file giving the number of HMMER hits within each gene


**Example command for running against the refseq annotations:**  
```
bash scripts/intersect-with-reference-annotations.sh 2016-11-12-nhmmer-vs-dna/duf1220-vs-hg38.dfamtblout annotations/2016-11-12-human-domain-annotation/ data/reference-annotations/refseq/human/human-exons-refseq-sorted-merged.bed data/reference-annotations/refseq/human/human-cds-refseq-sorted-merged.bed data/reference-annotations/refseq/human/human-genes-refseq-sorted.bed refseq
```

**Example command for running against the ensemble annotations:**  
```
bash scripts/intersect-with-reference-annotations.sh 2016-11-12-nhmmer-vs-dna/duf1220-vs-hg38.dfamtblout annotations/2016-11-12-human-domain-annotation/ data/reference-annotations/ensembl/human/human-exons-ensembl-sorted-merged.bed data/reference-annotations/ensembl/human/human-cds-ensembl-sorted-merged.bed data/reference-annotations/ensembl/human/human-genes-ensembl-sorted.bed ensembl
```




#### Group short/long exons into domains and perform initital annotation:  

**Script:** _exon-annotation-wrapper.sh_ You will run this command once against the RefSeq annotations and once against the Ensemble annotations  

**Actions:**
- Calls _group-exon-doublets.py_ which groups short and long exons as appropriate into domains and adds initital annotations
- Generates files for positive and negative strand exons, and sorts them appropriately so that the code to number domain occurance in gene numbers them in the correct order depending upon which strand they are on
- Calls _add-counts-to-doublets.py_ which assigns "order in gene" numbers to each DUF1220 domain exon doublet

**Inputs:**  
1. Path to the "all-relevant-exons-hit-nohit-"refseq or ensembl".bed file  
2. Output folder  
3. Name of the exon reference annotation being used  

**Outputs:**
Intermediate files:
- annotated-nbpf-exons-neg-strand-$reference.bed: output of _group-exon-doublets-v4.py_  
- annotated-nbpf-exons-pos-strand-$reference.bed: output of _group-exon-doublets-v4.py_  
- annotated-nbpf-exons-neg-strand-sorted-$reference.bed: sorted version of the above file  
- annotated-nbpf-exons-pos-strand-sorted-$reference.bed: sorted version of the above file  
- annotated-nbpf-exons-neg-doublets-$reference.bed  
- annotated-nbpf-exons-pos-doublets-$reference.bed

File going forward for future use:  
- annotated-nbpf-exons-all-doublets-$reference.bed  

**Example usage for refseq annotation:**    
```
bash scripts/exon-annotation-wrapper.sh annotations/2016-11-12-human-domain-annotation/all-relevant-exons-clean-refseq.bed annotations/2016-11-12-human-domain-annotation/ refseq
```

** Example usage for ensembl annotation:**  
```
bash scripts/exon-annotation-wrapper.sh annotations/2016-11-12-human-domain-annotation/all-relevant-exons-clean-ensembl.bed annotations/2016-11-12-human-domain-annotation/ ensembl
```

#### Combine the results of the refseq and ensemble annotations to get the most complete exon annotations:
**Scripts:** _combine-refseq-ensembl-wrapper.sh_

**Actions:**  
- Calls _combine-refseq-ensembl.py_ which prints RefSeq exons in cases where that annotation is the most complete and prints Ensembl exons where the Ensembl annotation is more complete  
- Sorts the resulting file  

**Inputs:**  
1. Path to refseq file generated from previous step, "annotated-nbpf-exons-all-doublets-refseq.bed"  
2. Path to ensembl file generated from previous step, "annotated-nbpf-exons-all-doublets-ensembl.bed"  
3. Path to a comma separated file that holds gene names in the first column, and the selected reference annotation to use for that gene in the second column (either refseq or ensembl).  Optionally, the third column can hold notes as to why a particular reference was selected for each gene. To make these selections, manually inspect the all-relevant-exons-clean-$reference.bed files for both reference annotations.  For each gene, determine if the two reference annotations give the same exon structure, or if one does a better job annotating DUF1220 domains (e.g. RefSeq doesn't have any exon annotation for NBPF17P, while Ensembl does). 
3. Output folder  

**Outputs:**  
- combined-refseq-ensembl-annotation-$date.bed: The most complete form of the annotation prior to beginning work on assigning clades  

**Example Usage:**  
```
bash scripts/combine-refseq-ensembl-wrapper.sh annotations/2016-11-12-human-domain-annotation/annotated-nbpf-exons-all-doublets-refseq.bed annotations/2016-11-12-human-domain-annotation/annotated-nbpf-exons-all-doublets-ensembl.bed data/reference-annotations/reference-selection-by-gene.csv annotations/2016-11-12-human-domain-annotation/
```


#### Determine which clade each DUF1220 domain belongs to

##### Get the fasta sequences for all DUF1220 exons
**Script:** _get-fasta-all-duf-exons.sh_  
**Actions:**  
Runs bedtools getfasta to obtain the fasta sequences for all duf exons in one file, as well as seperate files for short exons and long exons
**Input:**  
1. Path to file generated from previous step, "combined-refseq-ensembl-annotation.bed"
2. Path to genome reference fasta file (e.g. hg38.fa)  
3. Output folder  

**Output:**  
- fasta-for-all-duf-exons-nuc.fa  
- fasta-for-all-short-exons-nuc.fa  
- fasta-for-all-long-exons-nuc.fa  
```
bash scripts/get-fasta-all-duf-exons.sh annotations/2016-11-12-human-domain-annotation/combined-refseq-ensembl-annotation-2016-11-29.bed sequences/dna/dna-ucsc/hg38.fa annotations/2016-11-12-human-domain-annotation/
```

##### Combine the nucleotide sequences from adjacent short & long exons**
It would seem to make sense to combine the short and long exon nucleotide sequences and then do the translation, but that seems to be troublesome, because the short and long exons don't appear to be translated in the same frame.  This would be useful if you wanted to do nucleotide level analysis of full domains, but it isn't necessary for the steps that follow. 

**Output:**  
- combined-short-long-nuc-seqs.fa: The nucleotide fasta sequences for the short and long exons combined (when there is proper doublet)  
- fasta-for-lone-dufs.fa: The nucleotide fasta sequences for lone short and long DUF exons  
```
python scripts/combine-short-long-nucleotide-seq.py results/2015-11-13-domain-ops/fasta-for-all-duf-exons.txt results/2015-11-13-domain-ops/
```

#### Determine protein sequence for DUF1220 domains (exon doublets)

##### Translate each exon (short & long) individually**  
Translating them individually is important for two reasons (1) Transeq can not handle all of the short and long exons at once, (2) the short and long exons appear to be in different frames  

1. Run the fasta-for-all-short-exons-nuc-$date.fa and fasta-for-all-long-exons-nuc-$date.fa files through [Transeq](http://www.ebi.ac.uk/Tools/st/emboss_transeq/) for all 6 frames, download the files, and save them as *six-frame-translation-short-exons-$date.fa* and *six-frame-translation-long-exons-$date*.fa
2. Combine the files with the code below  
```
cat annotations/2016-11-12-human-domain-annotation/six-frame-translation-short-exons-2016-11-29.txt annotations/2016-11-12-human-domain-annotation/six-frame-translation-long-exons-2016-11-29.txt > annotations/2016-11-12-human-domain-annotation/six-frame-translation-all-exons-2016-11-29.fa
```
##### Select the appropriate translated sequence for each exon, and combine adjacent short & long exons together**
**Script:** _select-correct-translation-and-combine-doublets.py_  

**Actions:**  
1. For each duf exon, it picks the appropriate translation based on matches to the PFAM seed domain sequences and the lack of stop codons  
2. It combines the appropriate translated short and long exons for each doublet  

**Input:**  
1. The file that has the six-frame translations for all exons  
2. The output folder  

**Output:**  
- selected-translation-all-long-$date.fa  
- selected-translation-all-short-$date.fa  
- fasta-for-protein-doublets-$date.fa
- fasta-for-translated-protein-doublets-and-lone-sequences-$date.fa

**Example Usage:**
```
python scripts/select-correct-translation-and-combine-doublets.py annotations/2016-11-12-human-domain-annotation/six-frame-translation-all-exons-2016-11-29.fa annotations/2016-11-12-human-domain-annotation/
```

#### Visualize aligned protein sequences to identify motifs characteristic of each clade
1. Align protein doublet sequences by taking the fasta file of the exon doublet protein sequences (fasta-for-translated-protein-doublets.fa) and run it through [Clustal Omega](http://www.ebi.ac.uk/Tools/msa/clustalo/)  
2.  Identify characteristic sequence motifs -- The changes in amino acid motifs are striking and clearly suggest sub-groups  (**I have identified motifs and coded them into the next step that assigns each domain to a clade**).  Which subgroup should be which clade (e.g. HLS1 vs HLS2) was established by using the previously published information on the characteristic ordering of DUF1220 clades within each gene.  Domains of each subgroup take on the characteristic pattern previously described, and so were named accordingly (e.g. the subgroup with its domains always at the 5' end of the gene was named CON1).

#### Assign each DUF1220 doublet to a clade
**Script:** _give-aligned-seqs-clade-names.py_  
**Actions:**  
- Assigns each protein sequence to a DUF1220 clade based on the presence of the characteristic sequence motif  
- Creates a new annotation BED file with the new clade names replacing the old "duf" placeholder  

**Input:**  
1. The fasta file of the translated protein domains (and translated lone short and long exons) "fasta-for-translated-protein-doublets-and-lone-sequences.fa" (generated by the script in the previous step, _select-correct-translation-and-combine-doublets.py_)  
2. The current annotation file up to this point, "combined-refseq-ensembl-annotation.bed" (generated in a previous step by _combine-refseq-ensembl-wrapper.sh_)  
3. Output folder  

**Output:**  
- annotation-domain-based-numbering-" + todaysdate + ".bed": The BED file of DUF1220 coordinates with the clades annotated
- annotation-domain-based-numbering-" + todaysdate +".csv": The same as the BED file, but as a comma separated file, for use in other applicaions that handle .csv files better than .bed files  

- fasta-for-protein-seqs-with-clades-" + todaysdate + ".fa": The fasta file of protein doublets updated with the clades annotated in the headers

```
python scripts/give-aligned-seqs-clade-names-and-conserved-exon-groups.py annotations/2016-11-12-human-domain-annotation/fasta-for-translated-protein-doublets-and-lone-sequences-2016-11-29.fa annotations/2016-11-12-human-domain-annotation/fasta-for-all-non-duf-exons-2016-11-29.fa annotations/2016-11-12-human-domain-annotation/combined-refseq-ensembl-annotation-2016-11-29.bed annotations/2016-11-12-human-domain-annotation/
```
#### Number domains according to clade and generate a file of "full-domain" (rather than individual exon) coordinates
**Script:** _number-domains-according-to-clade.sh_  
**Actions:**
Converts the annotation file generated by _give-aligned-seqs-clade-names.py_, which has a domain-based number, that is, domains are numbered within genes according to the order in which they appear in the gene without reference to the clade (e.g. CON1_1, CON2_2, HLS1_3, HLS2_4) rather than (CON1_1, CON2_1, HLS1_1, HLS2_1,HLS3_1,HLS1_2, etc).   This script also produces a file of the annotations collapsed to "full domains"

**Inputs:**  
1. The BED file with "domain numbering" format produced by _scripts/give-aligned-seqs-clade-names.py_  
2. The fasta file with domain numbering produced by _scripts/give-aligned-seqs-clade-names.py_ 
2. The output folder (without the "/" on the end)  

**Output:**  
Intermediate Files:  
- annotation-domain-order-numbering-neg-strand-$today.bed  
- annotation-domain-order-numbering-pos-strand-$today.bed  

Final files:  
- annotation-clade-based-numbering-$today.bed  
- annotation-clade-based-numbering-full-domains-$today.bed  

**Example usage:**  
```
bash scripts/number-domains-according-to-clade.sh annotations/2016-11-12-human-domain-annotation/annotation-domain-based-numbering-2016-11-29.bed  annotations/2016-11-12-human-domain-annotation/fasta-for-protein-domains-with-clades-2016-11-29.fa annotations/2016-11-12-human-domain-annotation/
```

#### Visually confirm validity of clade assignments by phylogenetic tree and visualization of aligned protein sequences
1. Take fasta file of clade-labeled protein sequences generated with previous script, "fasta-for-protein-seqs-with-clades-2016-11-13.fa", and align the sequences with Clustal Omega.  Download the alignment file (name with .aln extension)
2. Generate phylogenetic tree (Jukes-Cantor, neighbor-joining, no outgroup)



