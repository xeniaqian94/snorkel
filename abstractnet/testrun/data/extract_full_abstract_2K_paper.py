import csv
import sys
import ast
import re

# Usage: python extract_full_abstract_2K_paper.py annotations_label-level_all-to-date-2018-4-25-WithTitle.csv

f_write=open(sys.argv[1].replace(".csv",".full_abstract.csv"),"w")
abstract_col_index=1

with open(sys.argv[1]) as csvfile:
	spamreader = csv.reader(csvfile)
	n=0
	for row in spamreader:
		try:
			if n==0:
				n+=1
				continue
			row_segment=[s.replace("\t"," ") for s in row]

			value=ast.literal_eval(row[abstract_col_index])  # 1 is the abstract_row_index
			text=" ".join([str(v) for v in value]).replace("\n"," ")

			f_write.write('2K_dev_'+str(row[0])+"\t"+text+"\n")
		except:
			print(row[abstract_col_index])
			print

