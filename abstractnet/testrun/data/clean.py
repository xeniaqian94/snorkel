import csv
with open("ClydeDB.csv") as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        row_segment=[s.replace("\t"," ") for s in row]
        if row[4]!="null":
            print(row[0]+"\t"+row[4].strip("\n"))