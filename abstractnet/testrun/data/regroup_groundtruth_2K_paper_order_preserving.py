import csv
import sys
import ast
import re
from collections import defaultdict

# Usage: python regroup_groundtruth_2K_paper_order_preserving.py annotations_label-level_all-to-date-2018-4-25-WithTitle.labelled.csv 
# Input: line format [segment]\t[segment_name]\t[docid]， e.g. authority and types of behaviors	background	2K_dev_0
# Output: file format [docid]\t[regrouped_doc]

regrouped_docs=defaultdict(lambda:list())

f_write=open(sys.argv[1].replace(".labelled",".labelled_regrouped"),"w")
with open(sys.argv[1]) as csvfile:
	csv_reader=csv.reader(csvfile,delimiter=",")
	for row in csv_reader:
		regrouped_docs[row[2].strip()]+=[row[0].strip().replace("~"," ")]
		

for docid in sorted(regrouped_docs.keys()):
	regrouped_docs[docid]="~".join(regrouped_docs[docid])
	f_write.write(str(docid)+"\t"+str(regrouped_docs[docid])+".\n")  # finally enclosed with a period
