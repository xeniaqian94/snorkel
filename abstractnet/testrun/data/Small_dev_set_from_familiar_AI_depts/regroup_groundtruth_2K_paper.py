import csv
import sys
import ast
import re
from collections import defaultdict

# Usage: python regroup_groundtruth_2K_paper.py annotations_label-level_all-to-date-2018-4-25-WithTitle.labelled.csv 
# Input: line format [segment]\t[segment_name]\t[docid]， e.g. authority and types of behaviors	background	2K_dev_0
# Output: file format [docid]\t[regrouped_doc]

regrouped_docs=defaultdict(lambda:defaultdict(lambda:list()))

f_write=open(sys.argv[1].replace(".labelled",".labelled_regrouped"),"w")
with open(sys.argv[1]) as csvfile:
	# span_reader = csv.reader(csvfile)
	for line in csvfile.readlines():
		entries=line.split("\t")

		regrouped_docs[entries[2].strip()][entries[1].strip()]+=[entries[0].strip()]

segment_order=[(2,"background"),(7,"purpose"),(3,"finding"),(4,"mechanism"),(5,"method")]
for docid in regrouped_docs.keys():
	for (segment_id,segment_name) in segment_order:
		if segment_name in regrouped_docs[docid]:
			regrouped_docs[docid][segment_name]=", ".join(regrouped_docs[docid][segment_name])
	regrouped_docs[docid]=". ".join([regrouped_docs[docid][segment_name][0].upper()+regrouped_docs[docid][segment_name][1:] for (segment_id, segment_name) in segment_order if len(regrouped_docs[docid][segment_name])!=0])
	f_write.write(str(docid)+"\t"+str(regrouped_docs[docid])+".\n")
