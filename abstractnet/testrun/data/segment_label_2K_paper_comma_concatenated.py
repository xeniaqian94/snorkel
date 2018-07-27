import csv
import sys
import ast
import re

f_write=open(sys.argv[1].replace(".csv",".labelled.csv"),"w")
f_write.write("segment\tlabel\n")
with open(sys.argv[1]) as csvfile:
	spamreader = csv.reader(csvfile)
	n=0
	for row in spamreader:
		if n==0:
			n+=1
			continue
		row_segment=[s.replace("\t"," ") for s in row]

		for pair in [(2,"background"),(3,"finding"),(4,"mechanism"),(5,"method")]:
			try:
				value=ast.literal_eval(row[pair[0]])
				
				text=" ".join(value)
				for sentence in re.split("\\.",text):
					segments=re.split(",",sentence)
					current_segment=""

					for i in range(len(segments)):
						# print(segments[i])
						current_segment+=" "+segments[i].strip()
						if len(current_segment.strip().split(" "))>2:
							f_write.write(current_segment.strip()+"\t"+pair[1]+"\n")
							current_segment=""
					if current_segment.strip()!="":
						f_write.write(current_segment.strip()+"\t"+pair[1]+"\n")
			except:
				continue