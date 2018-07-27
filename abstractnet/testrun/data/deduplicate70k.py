import sys
file=open(sys.argv[1])
lines=file.readlines()
doc_set=dict()
file_w=open(sys.argv[1].replace(".tsv","_deduplicated.tsv"),"w")
for line in lines:
	docid=line.split("\t")[0]
	if docid in doc_set:
		# print("Duplicate!")
		doc_set[docid]+=1
	else:
		doc_set[docid]=1
		
		file_w.write(line)


count=0
for key in doc_set:
	if doc_set[key]==2:
		print(key)
		count+=1

print(count)

