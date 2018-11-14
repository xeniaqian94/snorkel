from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import *

import re
import sys
import csv
import numpy as np
import scipy.sparse as sparse
import pandas as pd
from snorkel.models import StableLabel
from snorkel.db_helpers import reload_annotator_labels

FPATH="data/annotations_label-level_all-to-date-2018-4-25-WithTitle.labelled.csv"

def load_external_labels(session, candidate_class, annotator_name='gold',file_path=None,isPrint=True):
    # inherited from tutorial/intro/util.py
    gold_labels = pd.read_csv(file_path, sep="\t")
    for index, row in gold_labels.iterrows(): 

        # if row['label'].strip()==annotator_name: 
            # We check if the label already exists, in case this cell was already executed
        # print(row['segment'],row['label'])
        context_stable_ids = row['segment']
        if isPrint:
            print(context_stable_ids)
        query = session.query(StableLabel).filter(StableLabel.context_stable_ids == context_stable_ids)
        query = query.filter(StableLabel.annotator_name == annotator_name)
        if query.count() == 0:
            session.add(StableLabel(
                context_stable_ids=context_stable_ids,
                annotator_name=annotator_name,
                value=row['label']))

    # Commit session
    session.commit()

    # Reload annotator labels
    reload_annotator_labels(session, candidate_class, annotator_name, split=1, filter_label_split=False)
    reload_annotator_labels(session, candidate_class, annotator_name, split=2, filter_label_split=False)

def get_candidate_text(candidate):
    return candidate.get_contexts()[0].sentence.text[candidate.segment_cue.char_start:candidate.segment_cue.char_end+1]

from collections import defaultdict
def load_groundtruth_as_external_dict(groundtruth_path,delimiter=""):
    groundtruth_dict=defaultdict(lambda: defaultdict(lambda: list()))
    with open(groundtruth_path) as f:
        if delimiter==",":
            csv_reader=csv.reader(f,delimiter=",")
            for row in csv_reader:
                groundtruth_dict[row[2].strip()][row[1].strip()]+=[row[0].strip("., \n").strip()]
        else:
            for line in f.readlines():
                if len(line.strip())==0:
                    continue
                text=line.split("\t")[0].strip("., \n").strip()
                label=line.split("\t")[1].strip()
                name=line.split("\t")[2].strip()
                groundtruth_dict[name][label]+=[text]
    return groundtruth_dict

def write_segment_name(cands,fpath,groundtruth_dict,segment_name):
    with open(fpath,"w") as f_write:
        f_write.write("segment\tlabel\n")
        unmatched_count=0
        for segment in cands:
            labeled=False
            striped_query_text=get_candidate_text(segment).strip("., \n").strip() # strip by . , or space
            stable_label_id=segment.segment_cue.stable_id
            docid=segment.get_parent().document.name
            
            for sname in groundtruth_dict[docid].keys():
                if sname==segment_name:
                    label=1

                else:
                    label=-1
                for gold_sentence in groundtruth_dict[docid][sname]:
                    if striped_query_text.lower() in gold_sentence.lower() and labeled==False:
                        # if striped_query_text.lower()!=gold_sentence.lower():
                        #     print("Partially matched - striped_query_text: ",striped_query_text, "\nbut gold_sentence ",gold_sentence,"\n=============\n")
                        f_write.write(str(stable_label_id)+"\t"+str(label)+"\n")
                        labeled=True
                        # if label==1:
                        #     print(segment.__dict__)
                        #     print(stable_label_id)
                        #     input()


            if labeled==False:
                unmatched_count+=1
                print("Unmatched - striped_query_text: ",striped_query_text)
                # print(segment.__dict__)
                # print(groundtruth_dict[docid])
        print("\n\nOut of "+str(len(cands))+", "+str(unmatched_count)+" are unmatched"+(", great job!" if unmatched_count==0 else ", please double check"))


