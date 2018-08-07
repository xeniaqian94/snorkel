import csv
import sys
import ast
import re


# Usage: python segment_label_2K_paper_comma_concatenated.py annotations_label-level_all-to-date-2018-4-25-WithTitle.csv 1 Filtered_MLD_RI_HCI_CSD_LTI_ISR.csv
# Output: the file is named as annotations_label-level_all-to-date-2018-4-25-WithTitle.labelled_comma_original.csv 
# in each line, [segment]\t[label]\t[docid]

docid_prefix="2K_test_"
level=int(sys.argv[2])  # level = 1 if we want only LTI, CSD, MLD, RI, HCII, ISR papers, level = 2 for all papers 
if level==1:
	with open(sys.argv[3]) as csvfile:
		reader=csv.reader(csvfile)
		next(reader)

		title_set=set([r[14].lower().strip() for r in reader])
	docid_prefix="2K_dev_"


f_write=open(sys.argv[1].replace(".csv",".labelled_level_"+str(level)+".csv"),"w")

# f_write.write("segment\tlabel\n")
with open(sys.argv[1]) as csvfile:
	spamreader = csv.reader(csvfile)
	n=0
	valid_title_count=0
	for row in spamreader:
		if n==0:
			n+=1
			continue
		row_segment=[s.replace("\t"," ") for s in row]
		title=row[8].lower().strip()
		if level==1 and title not in title_set:
			continue
		else:
			valid_title_count+=1;

		for pair in [(2,"background"),(3,"finding"),(4,"mechanism"),(5,"method"),(7,"purpose")]:
			try:
				value=ast.literal_eval(row[pair[0]])
				
				text=" ".join(value)
				for sentence in re.split("\\.",text):
					segments=re.split(",",sentence)
					current_segment=""

					for i in range(len(segments)):
						# print(segments[i])
						current_segment+=" "+segments[i].strip()
						if len(current_segment.strip().split(" "))>3:
							f_write.write(current_segment.strip()+"\t"+pair[1]+"\t"+docid_prefix+str(row[0])+"\n")
							current_segment=""
					if len(current_segment.strip().split(" "))>3:
						f_write.write(current_segment.strip()+"\t"+pair[1]+"\t"+docid_prefix+str(row[0])+"\n")
			except:
				continue
	print("valid_title_count ",valid_title_count)