import csv
import sys
import ast
import re

# Usage: python segment_label_2K_paper_comma_asOriginal.py annotations_label-level_all-to-date-2018-4-25-WithTitle.csv 
# Output: the file is named as annotations_label-level_all-to-date-2018-4-25-WithTitle.labelled_comma_original.csv 
# in each line, [segment]\t[label]\t[docid]

f_write=open(sys.argv[1].replace(".csv",".labelled_comma_original.csv"),"w")
with open(sys.argv[1]) as csvfile:
	spamreader = csv.reader(csvfile)
	n=0
	for row in spamreader:
		if n==0:
			n+=1
			continue
		row_segment=[s.replace("\t"," ") for s in row]

		# background=" ".join([str(s) for s in row[2]])
		# print(str(row[2]))

		for pair in [(2,"background"),(3,"finding"),(4,"mechanism"),(5,"method"),(7,"purpose")]:
			try:
				value=ast.literal_eval(row[pair[0]])
				
				text=" ".join([str(v) for v in value])
				for sentence in re.split("\\.",text):
					segments=re.split(",",sentence)
					for i in range(len(segments)):
						if len(segments[i].strip())>5:
							f_write.write(segments[i].strip()+"\t"+pair[1]+"\t2K_dev_"+str(row[0])+"\n")
			except:
				continue