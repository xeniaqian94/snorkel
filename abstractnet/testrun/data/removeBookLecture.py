import sys
file=open(sys.argv[1])
lines=file.readlines()
doc_set=dict()
file_w=open(sys.argv[1].replace(".tsv","_noBookLecture.tsv"),"w")
count=0
for line in lines:
	content=line.split("\t")[1].lower()
	if ("this document " in content) or ("this note " in content) or (" i " in content) or ("this course" in content) or ("book " in content) or ("lecture" in content) or ("chapter" in content) or (content.strip()[-1]!="."):
		print("Removed: "+line+"\n")
		count+=1
	else:	
		file_w.write(line.split("\t")[0]+"\t"+line.split("\t")[1].strip().split("Description ")[-1].split("Abstract ")[-1].split("Abstract: ")[-1].split("ABSTRACT ")[-1].split("Abstract. ")[-1].strip()+"\n")
print(count)

