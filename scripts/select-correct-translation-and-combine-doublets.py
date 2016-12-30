#! /usr/bin/env python

import pdb
import sys
from collections import defaultdict
from operator import itemgetter
import time

# Manually identified from NBPF10-duf-short-9: EEDQDPPCP, from NBPF17P-duf-short-4: EEDQGPSCP, NBPF17P-duf-short-5: EEDQNPSCP
# PDE4DIP-duf-short-1 & LOC100996724-duf-short-1   :DHKSEKDQAGLEPLAL
# NBPF22P-duf-short-2: EEVEDQSPPCP
# NBPF1L-duf-short-1: EDVQVEEAEK
# NBPF4-duf-short-2, NBPF5P-duf-short-2, NBPF7-duf-short-2, NBPF6-poss-duf-short-lone: EEEGKAPVPP
# duf-short-1 of NBPF4, 5p, and 6
# duf-short-3 of NBPF4 and 6
# duf-short-4 of NBPF4 and 6
# nbpf15-duf-short-6: EGEDDNPPCP
# This motif is in both nbpf12-duf-short 2 and nbpf10-duf-short-1:EDVQVEE
# nbpf9-duf-short-7: EENQNPPCP
# nbpf17p-duf-short-1: EDKDVEVEE
# nbpf17p-duf-short-2: EEKGPVFP
# nbpf17p-duf-short-3: EDQEATDPR
# nbpf26-duf-short-4: EDHEATGP
# nbpf7-duf-short-1: DKVQESPAP
# nbpf20-duf-short-53: EDQTPPCP
# LOC101927520-duf-short-1:EDRQKPLAP
# nbpf21p-duf-short-1: EKVEKVQG
# nbpf21p-duf-short-2: EEDGKQPVSP
# nbpf13p-duf-short-1: ENDKDEE
# nbpf13p-duf-short-2: EEKGPASP
# nbpf13p-duf-short-3: DDREATCP
# nbpf13p-duf-short-4: EEDQGPPGP
# nbpf13p-duf-short-5: EEDQDPQCP


######## Notes on manual input of long exons:
# nbpf19-duf-long-5 (and a few others): LSRELVEVVE
# nbpf19-duf-long-43 (and others):LSRELLAEK
# nbpf12-duf-long-1 (and others):  EVQKAEESK
# nbpf1l-duf-long-7: SRELLEAVE
# LOC100996724-duf-long-1 :LSRELQEKEK
# nbpf14-duf-long-15: LSRELLHEK
# nbpf4-duf-1-long (and others): EVQKTEEKEV
# nbpf13p-duf-long-2: NLQETEEEE
# nbpf7-duf-long-2: KLQESEEK
# nbpf20-duf-long-1: EMQKAEEKEV
# nbpf7-duf-long-1: EEQKAEEKEV
# nbpf10-duf-long-40: NGVLMEVEER
# nbpf26-duf-long-13 (and others): LNSVLMEVEEP
# nbpf11-duf-long-7: LSSVLMEVEVPEV
# nbpf10-duf-long-lone: LSRELLDEKGP
# nbpf11-duf-long-7: LSSVLMEVEVP
# nbpf1-duf-long-7: LSGMLMEVEEPEV
# nbpf2p-duf-long-2: VLQDSLDRCYSTT
# nbpf17p-duf-long-4: LSRELLEGEEP
# nbpf1-duf-long-3: EMPKAEEKE
# nbpf17p-duf-long-3: LSRELLDKKEP
# nbpf6-duf-long-4 (and others): LSQELPEVKEQ
# nbpf12-duf-long-2: EMQKAEESKVP
# nbpf14-duf-long-31: LSRELLDEKDP
# nbpf10-duf-long-12: LSRELLEEKGP
# nbpf17p-duf-long-5: RSRELLEVVES
# nbpf21p-duf-long-1: VEVQEAEEKEVP
# nbpf16-duf-long-5: LSGELLDEKEP
# nbpf3-duf-long-4: LSRELPEVVEP
# nbpf15-duf-long-6: LYGVLMEVEEPEV
# nbpf26-duf-long-13: LNSMLMEVEEPEV
# nbpf13p-duf-long-5: LSPDLPEVEEQDVP
# nbpf13p-duf-long-4: LSSELLEGEG
# nbpf13p-duf-long-3: LSRELLEVEEPEV
# FAM91A3P: WLKREVQEEE
# nbpf6-duf-long-3 (and others: nbpf4-duf-long-3 and nbpf22p-duf-long-1): LSRGPLRVDK -- the sequence of these exons matches this seed domain: H2R5P0_PANTR/364-427
# duf-long-2 for nbpf4, 5p,and 6: HHDKSNSYRHRE - matches a portion of seed domain: H2R5P0_PANTR/271-337
# nbpf6-duf-short-2: NRQSLEPGEL --  matches a portion of the seed domain: H2R5P0_PANTR/271-337
# nbpf21p-duf-long-lone: DLCDCHQAYSK -- this motif from the middle of the sequence matches a region of this seed sequence: F6WNF5_MACMU/504-568 
# it is hard to figure out which is the correct translation for nbpf21p-duf-long-2 b/c none are obviously great matches.  Right now, this seems like the best choice, portions of its sequence
#    match some seed domain sequences:  YPSSLSWEVPQV
# NDEDVDD is for the short exon of NBPF18P - by nucleotide sequence it is definitely a CON1, but its amino acid sequence is a bit difference

short_exon_seed_seqs = ["EDQGPPC","EDQGPPC","EDQNPPC","EDQKPPC", "EDQEATG","EDQEATS","EDQDPSC","KVQELYA","KVQKSSA","EEKGPVS"]
short_exon_manual = ["EEDQDPPCP","EEDQGPSCP","EEDQNPSCP","DHKSEKDQAGLEP","EEVEDQSPPCP","EDVQVEEAEK","EEEGKAPVPP","EEVEKVQ",
"EEVKGQETVA","EEIEDQSPPCP", "EGEDDNPPCP","EDVQVE","EENQNPPCP","EDKDVEVEE","EEKGPVFP","EDQEATDPR","EDHEATGP","DKVQESPAP","EDQTPPCP",
"EDRQKPLAP","EKVEKVQG","EEDGKQPVSP","ENDKDEE","EEKGPASP","EEDQGPPGP","EEDQDPQCP","DDREATCP","NRQSLEPGEL","NDEDVDD"]
short_exon_seqs = short_exon_seed_seqs + short_exon_manual

long_exon_seed_seqs = ["SRELLEVVEP","SRELLEVVEP","NGVLMEVEEP","NEVLMEAEEP","SRELLDEKGP","SRELLDEKEP","SRELLDEKEP","EVQKAEEK","EVQKTEES","NLQESEEE"]
long_exon_manual = ["LSRELVEVVE","LSRELLAEK","EVQKAEESK","SRELLEAVE","LSRELQEKEK","LSRELLHEK","EVQKTEEKEV","NLQETEEEE","KLQESEEK","EMQKAEEKEV",
"EEQKAEEKEV","NGVLMEVEER","LNSVLMEVEEP","LSRELLDEKGP","LSSVLMEVEVP","LSGMLMEVEEPEV","VLQDSLDRCYSTT","LSRELLEGEEP","EMPKAEEKE","LSRELLDKKEP",
"LSQELPEVKEQ","EMQKAEESKVP","LSRELLDEKDP","LSRELLEEKGP","RSRELLEVVES","VEVQEAEEKEVP","LSGELLDEKEP","LSRELPEVVEP","LYGVLMEVEEPEV","LNSMLMEVEEPEV","LSPDLPEVEEQDVP",
"LSSELLEGEG","LSRELLEVEEPEV","WLKREVQEEE","LSRGPLRVDK","HHDKSNSYRHRE","DLCDCHQAYSK","YPSSLSWEVPQV"]

long_exon_seqs = long_exon_seed_seqs + long_exon_manual

filename = sys.argv[1]
output_folder = sys.argv[2]

date=time.strftime("%Y-%m-%d")

out_combined_doublets = open(output_folder + "/fasta-for-protein-doublets.fa", mode = 'w')
out_con3_full = open(output_folder + "/full-con3-seqs.fa", mode = 'w')
out_flags = open(output_folder + "/flags-combining-short-long-pro-seq.txt",mode = 'w')
out_all_shorts = open(output_folder + "/selected-translation-all-short.fa", mode = 'w')
out_all_longs = open(output_folder + "/selected-translation-all-long.fa", mode = 'w')
out_doublets_plus_lone = open(output_folder + "/fasta-for-translated-protein-doublets-and-lone-sequences.fa", mode = 'w')

header_seq = defaultdict(list)
selected_seqs = defaultdict(list)
selected_seqs_wo_tags = defaultdict(list)
short_selects = defaultdict(list)
long_selects = defaultdict(list)
exon_all_frames = defaultdict(list)
list_of_exon_names = []

#This block takes the fasta file of all six frames translations, and does some formatting to get sequences that fall across multiple lines into
# a dictionary so that in the next step we can combine the sequence fragments togetner (not the exons, just fragments of the same sequence that are on multiple lines)

for line in open(filename):

    if line.startswith(">"):
        header = line.strip()


        exon_name = header.split("_")[0:3]
        exon_name = "_".join(exon_name)
        list_of_exon_names.append(exon_name)
    else:
        seq = line.strip()
        header_seq[header].append(seq)

    
for header, seq_components in header_seq.items():
    
    full_seq = "".join(seq_components)


    exon_name = header.split("_")[0:3]
    exon_name = "_".join(exon_name)
    
    exon_all_frames[exon_name].append(full_seq)
     

    if "short" in header or len(full_seq) < 120:
        
        for item in short_exon_seqs: #Look in the list of "known" short exon sequences
            if item in full_seq: # If you find a match between the particular sequenc you're looking at the the known short exon sequences, then make that sequence the selected sequence

                
                if full_seq.endswith("X"): # Drop "X"s if they appear in the translated sequence 
                    full_seq = full_seq[0:len(full_seq)-1]
                
                else:
                    full_seq = full_seq 

                tag = 1 # The tage is necessary to later sort short and long exons in the correct order so we can append them in the correct order)
                short_selects[exon_name].append(full_seq) #For this particular exon, we have selected this sequence as the correct translation of the short exon because it matches known sequences

                if "SHORT" in exon_name and "LONG" not in exon_name: #The capitalized LONG represents lone long domains, the capitalized SHORT represents lone short domains
                    continue

                elif "lone" in exon_name: #This extra condition accounts for the first pass through without clades yet
                    continue

                elif "duf-long" in exon_name or "duf-short" in exon_name: # This accounts for the first time using this script, in which clades aren't assigned yet
                    exon_name_parts = exon_name.split("_")
                    domain = exon_name_parts[0] + "_duf_" + exon_name_parts[2]
                
                    if full_seq not in selected_seqs_wo_tags[domain]: #If this sequence not already in the list, then add it to list
                        selected_seqs_wo_tags[domain].append(full_seq)
                        selected_seqs[domain].append((full_seq,tag))
                else:
                    domain = exon_name

                    if full_seq not in selected_seqs_wo_tags[domain]: #If this sequence not already in the list, then add it to list
                        selected_seqs_wo_tags[domain].append(full_seq)
                        selected_seqs[domain].append((full_seq,tag))

    if "long" in header or len(full_seq) >= 120:
        for item in long_exon_seqs: #Look in the list of "known" long exon sequences
            if item in full_seq: # If you find a mtach between the particular sequence you're looking at and the known long exon sequences, then make that sequence the selected translation

                if full_seq.endswith("X"): #Drop "X"s if they appear at the end of the translated sequence
                    full_seq = full_seq[0:len(full_seq)-1]
                
                else:
                    full_seq = full_seq

                tag = 2 #The tag is necessary to later sort short and long exons in the correct order so we can append them in the correct order)
                long_selects[exon_name].append(full_seq) #For this exon, set this sequence as the selected translation
                
                if "LONG" in exon_name and "SHORT" not in exon_name:
                    continue

                elif "lone" in exon_name:
                    continue

                elif "duf-long" in exon_name or "duf-short" in exon_name: # This accounts for the first time using this script, in which clades aren't assigned yet
                    exon_name_parts = exon_name.split("_")
                    domain = exon_name_parts[0] + "_duf_" + exon_name_parts[2]

                    if full_seq not in selected_seqs_wo_tags[domain]: #If this sequence not already in the list, then add it to list
                        selected_seqs_wo_tags[domain].append(full_seq)
                        selected_seqs[domain].append((full_seq,tag))
                else:
                    domain = exon_name

                    if full_seq not in selected_seqs_wo_tags[domain]:

                        selected_seqs_wo_tags[domain].append(full_seq)
                        selected_seqs[domain].append((full_seq,tag))
                    

    else:
        continue

for exon_name in set(list_of_exon_names):
    
    if "short" in exon_name and exon_name not in short_selects.keys():
        print >> out_flags, exon_name,"\t", "nss", "\t",exon_all_frames[exon_name]


    elif "long" in exon_name and exon_name not in long_selects.keys():
        print >> out_flags, exon_name,"\t", "nls","\t",exon_all_frames[exon_name]

    else:
        continue

for exon_name, seq in short_selects.items():

    if len(set(seq)) > 1:
        print >> out_flags, exon_name, "\t", "moss", "\t", seq #moss = more than one short sequence

    else:
        print >> out_all_shorts, exon_name
        print >> out_all_shorts, seq[0]

    if "lone" in exon_name:
        print >> out_doublets_plus_lone, exon_name
        print >> out_doublets_plus_lone, seq[0]
        

for exon_name, seq in long_selects.items():

    if len(set(seq)) >1:
        print >> out_flags, exon_name,"\t", "mols","\t",seq #mols = more than one long sequence
    else:
        print >> out_all_longs, exon_name
        print >> out_all_longs, seq[0]

    if "lone" in exon_name:
        
        print >> out_doublets_plus_lone, exon_name
        print >> out_doublets_plus_lone, seq[0]

for domain, seqs in selected_seqs.items():


    if len(seqs) == 2:

        
        sorted_seqs = sorted(seqs, key = itemgetter(1))
        sorted_seq_list = sorted_seqs[0][0] + sorted_seqs[1][0]
        combined_short_long_seq = "".join(sorted_seq_list)

        
        print >> out_combined_doublets, domain
        
        #truncate the CON3 domains at the first stop codon

        if "VIFPQ*" in combined_short_long_seq or "FQMGVIFPH*" in combined_short_long_seq:


        # print the full length CON3s, with the UTR sequence
            print >> out_con3_full, domain
            print >> out_con3_full, combined_short_long_seq

            
            # Set "combined_short_long_seq" to the truncated version to be printed with all of the others"

            combined_short_long_seq = combined_short_long_seq.split("*")[0]
        else:
            pass
        
        print >> out_combined_doublets, combined_short_long_seq

        


        print >> out_doublets_plus_lone, domain
        print >> out_doublets_plus_lone, combined_short_long_seq


    elif "gna" in domain: #Make a special case to print the domain that lands outside of any gene annotation "GNA" = Gene Note Annotated, fixing the original annotation to reflect a lone long would also work
        
        print >> out_combined_doublets, domain
        print >> out_combined_doublets, seqs[0][0]


    else:
        print >> out_flags, "FLAG","\t",domain,"\t", seqs
