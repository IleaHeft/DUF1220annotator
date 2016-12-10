#! /usr/bin/env python

import sys
import pdb
from collections import Counter


filename = sys.argv[1]
output_folder = sys.argv[2]
reference = sys.argv[3]

list_of_status_length = []
list_of_lengths = []
domain_counter = Counter()

#out_all = open(output_folder + "annotated-nbpf-exons.bed", mode = 'w')
out_neg = open(output_folder + "/annotated-nbpf-exons-neg-strand-" + reference + ".bed" , mode = 'w')
out_pos = open(output_folder + "/annotated-nbpf-exons-pos-strand-" + reference + ".bed", mode = 'w')

for index, line in enumerate(open(filename)):


    fields = line.strip().split("\t")
    
    chrom = fields[0]
    start = fields[1]
    end = fields[2]
    gene = fields[3]
    length = int(fields[4])
    strand = fields[5]
    status = fields[6]
    coding_status = fields[7]
    
    status = status.strip()
    coding_status = coding_status.strip()

    list_of_status_length.append((status, length))


for index,line in enumerate(open(filename)):

    fields = line.strip().split("\t")

    chrom = fields[0]
    start = fields[1]
    end = fields[2]
    gene = fields[3]
    length = int(fields[4])
    strand = fields[5]
    status = fields[6]
    coding_status = fields[7]

    status = status.strip()
    coding_status = coding_status.strip()

    try:
        

        #Manually annotate the two lone short exons in NBPF26 as duf-short-lone.  See fasta sequences for supporting evidence.

        if start ==  "120827946" or start == "120835517":
            notation = "duf-short-lone"

        # Manually annotate this exon in NBPF18P as being a duf-short-lone -- the sequence matches CON1 short sequences, but it has no long exon and so won't get picked up
        if start == "152022437":
            notation = "duf-short-lone"


        #Manually annotate this exon in NBPF11 as being a DUF-short exon. 
        # It doesn't get picked up in the standard script because the lenght of the exon is 127bp, but sequence analysis clearly shows its 3' end aligning with duf-short sequences (specifically, the HLS1 51bp short exons)
        # We have to manually annotate the long exon as well because the standard script annotates it as a lone long exon 

        elif end == "148109411": #using the end coordinate instead of the start, because it is likely to be more stable if if later reference annotations, the exon length is shortened
            notation = "duf-short"

        elif start == "148108482":
            notation = "duf-long"
        
        # Manually annotate this short exon in the NBPF10 ensemble annotation as being a duf-short - it definietly is one by sequence, it only isn't getting automatically roped into
        # its long exon pair, because the ensemble annotation includes an odd non-duf exon between this short one and the long one with the HMMER hit:

        # annotate the short one
        elif start == "146075046":
            notation = "duf-short"

        # manually annotate the long one as well so that it doesn't get flagged as a "lone" exon:

        elif start == "146074271":

            notation = "duf-long"
        
        #manually annotated this exon as being a duf-short exon, its length is longer than normal AND it has a potentially spurious 12bp exon between it and the long exon hit, so it doesn't get correctly picked up by the standard code
        elif start == "145393861":
            notation = "duf-short"
            
            # must also manually annoted the long exon that is hit so that it doesn't get flagged as being a lone hit

        elif start == "145393074":
            notation = "duf-long"

        # manually annotated this one as a non-duf exon -- it is 108bp in length, so the normal code annotates it as possible duf short, but it is in the UTR
        elif start == "149090753":
            notation = "Non-DUF1220"

        # In both NBPF4 and NBPF6, there is an 86bp exon lying between what appears to the actual short exon and the long exon that is "hit" by the HMMER search
        # The two elif statements below annotate the 86bp exon as a Non-DUF and the 51bp exon as a duf-short exon

        elif start == "108457248" or start == "108237011": #Start coord of 108237011 is in NBPF4, start coord of 108457248 is in NBPF6
            notation = "Non-DUF1220"

        elif start == "108457007" or start == "108237287": #Start coord of 108237287 is in NBPF4, start coord of 108457007 is in NBPF6
            notation = "duf-short"

        # If the exon was was "hit" by a HMMER located domain, then do these steps
        elif status == "hit"  and length > 120:
            notation = "duf-long"
            if strand == "-" and list_of_status_length[index + 1][1] > 120:
                notation = "duf-long-lone"

            elif strand == "-" and list_of_status_length[index + 1][1] < 45:
                notation = "duf-long-lone"

            elif strand == "+" and list_of_status_length[index - 1][1] > 120: 
                notation = "duf-long-lone"

            elif strand == "+" and list_of_status_length[index - 1][1] < 45: 
                notation = "duf-long-lone"

        elif status == "hit"  and length == 51:
            notation = "duf-short"

        elif status == "hit-ena"  and length > 120:
            notation = "duf-long"
            if strand == "-" and list_of_status_length[index + 1][1] > 120:
                notation = "duf-long-lone"
            elif strand == "+" and list_of_status_length[index - 1][1] > 120: 
                notation = "duf-long-lone"
        

        elif status == "hit-ena" and length == 51:
            notation = "duf-short"

        
        #If the exon was not hit by a HMMER domain, then see if the exon upstream or downstream of it was in order to determine if it should be annotated as a DUF short exon

        elif status == "not-hit" and strand == "-" and list_of_status_length[index - 1][0] == "hit" and length < 120 and length > 45:

            notation = "duf-short"

        
        elif status == "not-hit" and strand == "-" and list_of_status_length[index - 1][0] == "hit-ena" and length < 120 and length > 45:

            notation = "duf-short"
        
        elif status == "not-hit" and strand == "+" and list_of_status_length[index + 1][0] == "hit" and length < 120 and length > 45:

            notation = "duf-short"

        elif status == "not-hit" and strand == "+" and list_of_status_length[index + 1][0] == "hit-ena" and length < 120 and length > 45:

            notation = "duf-short"

        ##### These next four conditions deal with the annotation of my "not-hit-ena" sequences which are short sequences whose annotation I had to input manually

        elif status == "not-hit-ena" and strand == "-" and list_of_status_length[index - 1][0] == "hit" and length < 120 and length > 45:

            notation = "duf-short"

        
        elif status == "not-hit-ena" and strand == "-" and list_of_status_length[index - 1][0] == "hit-ena" and length < 120 and length > 45:

            notation = "duf-short"
        
        elif status == "not-hit-ena" and strand == "+" and list_of_status_length[index + 1][0] == "hit" and length < 120 and length > 45:

            notation = "duf-short"

        elif status == "not-hit-ena" and strand == "+" and list_of_status_length[index + 1][0] == "hit-ena" and length < 120 and length > 45:

            notation = "duf-short"



        elif length == 51 or length == 108:
            notation = "poss-duf-short-lone"
        else:
            notation = "Non-DUF1220"


    except:
         notation = "Non-DUF1220"


    if notation == "Non-DUF1220":
        notation = "Non-DUF1220" + "-" + str(length) 
    
    to_print =  [chrom,start,end,gene + "_" + notation,length,strand,status,coding_status]
    to_print = map(str, to_print)
    
    
    # Do not print the exons from this gene, this gene overlaps a non-duf region at the extreme 5' end of NBPF9 -- but there are no dufs in this gene, so don't print it
    if gene == "LOC101060398":
        continue
    
    elif strand == "-":
        print >> out_neg, "\t".join(to_print)

    else:
        print >> out_pos, "\t".join(to_print)
