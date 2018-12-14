'''

Usage:
python apply_large_scale_onset_label.py [split_id] [start_batch]
e.g. python apply_large_scale_onset_label.py 2
'''

import os
import sys
import pandas as pd
train_bucket=int(sys.argv[1])
print(train_bucket,"train_bucket is <-")

os.environ['SNORKELDB'] = "postgresql:///abstractnet30konsetgz"+str(train_bucket)

print(os.environ['SNORKELDB'])
os.environ['SNORKELHOME']="../../"
from snorkel import SnorkelSession
from snorkel.parser import TSVDocPreprocessor
session = SnorkelSession()

## Here, we just set the upperbound for how many documents we'll process!
# wc -l ~/Desktop/snorkel/abstractnet/testrun/data/hard-drive-slim-top-tier-citation-10-39
#    21799 /Users/xinq/Desktop/snorkel/abstractnet/testrun/data/hard-drive-slim-top-tier-citation-10-39

n_docs = 40000
# doc_preprocessor = TSVDocPreprocessor('data/annotations_label-level_all-to-date-2018-4-25-WithTitle_full_abstract_punc_concatenated.csv', encoding="utf-8",max_docs=n_docs)
# doc_preprocessor = TSVDocPreprocessor('data/hard-drive-slim-top-tier-citation-10-39', encoding="utf-8",max_docs=n_docs)

filename=os.environ['SNORKELHOME']+"../semantic/hard-drive-slim-top-tier-citation-"+str(train_bucket)
docID=set()
newfile=os.environ['SNORKELHOME']+"../semantic/hard-drive-slim-top-tier-citation-"+str(train_bucket)+"-new"
with open(newfile,"w") as fout:
    for line in open(filename,"r", errors='ignore').readlines():
        if line.split("\t")[0] in docID or len(line.split("\t"))!=2:
            continue
        docID.add(line.split("\t")[0])
        fout.write(line.replace("\n"," ").strip()+"\n")

print("total docID count", len(docID))
doc_preprocessor = TSVDocPreprocessor(newfile, encoding="utf-8", max_docs=n_docs)

from snorkel.parser.spacy_parser import Spacy
from snorkel.parser import CorpusParser
from snorkel.models import Document, Sentence  # defined in context.py file

if session.query(Document).count()==0:
    corpus_parser = CorpusParser(parser=Spacy())
    corpus_parser.apply(doc_preprocessor, count=n_docs)# ,parallelism=5)

print("Documents:", session.query(Document).count())

from snorkel import SnorkelSession
from snorkel.parser.spacy_parser import Spacy
from snorkel.parser import CorpusParser
from snorkel.models import Document, Sentence
from collections import defaultdict
import numpy as np

session = SnorkelSession()
docs = session.query(Document).all()
sents = session.query(Sentence).all()  # get all sentences from snorkel.db

docs_per_bucket=150
sents_split=defaultdict(lambda:[])
for ind, doc in enumerate(docs):
    bucket=int(ind/docs_per_bucket)
    for s in doc.sentences:
        sents_split[bucket]+=[s]
print("Number of buckets: (should have around ~100 buckets??)", len(sents_split))

from snorkel.models import candidate_subclass
from snorkel.candidates import Ngrams, CandidateExtractor
from snorkel.matchers import *
import datetime

Unigram = candidate_subclass('Unigram', ['unigram_cue'],values=['PP','MN','NULL'])
ngrams = Ngrams(n_max=1)
ngram_matcher=NgramMatcher()
unigram_segment_extractor=CandidateExtractor(Unigram,[ngrams],[ngram_matcher])

# from snorkel.lf_helpers import *
from snorkel.annotations import LabelAnnotator

# from LF.util_common_default_categorical import purpose_LFs,mechanism_LFs,null_LFs
from LF.util_common_default_categorical_onset_1026 import *
# purpose_LFs,mechanism_LFs,null_LFs
print("total LF count", len(purpose_LFs+mechanism_LFs+null_LFs), "unique count",len(set(purpose_LFs+mechanism_LFs+null_LFs)),"purpose_LFs",len(purpose_LFs),"mechanism_LFs",len(mechanism_LFs))
print("\n\npurpose_LFs\n",[lf.__name__ for lf in purpose_LFs])
print("\n\nmechanism_LFs\n",[lf.__name__ for lf in mechanism_LFs])
print("\n\nnull_LFs\n",[lf.__name__ for lf in null_LFs])

new_LFs=[]

from snorkel.learning import GenerativeModel
from util import get_candidate_text
import matplotlib.pyplot as plt
import datetime

def get_L_train(LFs,parallelism=2,split=0):
    L_train=None
    labeler=None
    np.random.seed(1701)
    labeler = LabelAnnotator(lfs=LFs)
    print(datetime.datetime.now())
    L_train = labeler.apply(split=split)# ,cids_query=session.query(Candidate.id).filter(Candidate.get_parent().id %10==1))
    print(datetime.datetime.now())
    print(type(L_train))
    print(L_train.shape)
    # print("**Total non_overlapping_coverage on L_train (percentage of labelled over all)**  "+str(L_train.non_overlapping_coverage()))
    return L_train


import numpy as np


def get_candidate_text(segment):
    return segment.get_parent().text[segment.get_contexts()[0].char_start:segment.get_contexts()[0].char_end + 1]


def write_csv_from_L_train(L_train, csv_path, session):
    try:
        aggregated_doc = defaultdict(lambda: [])
        aggregated_sent = defaultdict(lambda: [])
        # LF_list = purpose_LFs + mechanism_LFs + null_LFs

        non_zero_array = L_train.nonzero()

        train_marginals_tmp = np.zeros([L_train.shape[0]])
        # train_marginals_tmp[:, 2] = 1
        unigram_segments_tmp = []

        for idx in range(L_train.shape[0]):
            unigram_segments_tmp += [L_train.get_candidate(session, idx)]

        print("len(unigram_segments_tmp)==train_marginals.shape[0]?", len(unigram_segments_tmp),
              train_marginals_tmp.shape)

        for idx in range(len(non_zero_array[0])):
            row_idx = non_zero_array[0][idx]
            label = L_train[row_idx, non_zero_array[1][idx]]
            train_marginals_tmp[row_idx] = label

        for idx, train_segment in enumerate(unigram_segments_tmp):

            sent_id = train_segment.get_parent().id
            winningHighlight = int(train_marginals_tmp[idx])
            cue = train_segment.get_contexts()[0]
            aggregated_sent[sent_id] += [
                (cue.char_start, cue.char_end, get_candidate_text(train_segment), winningHighlight)]

            doc_id = train_segment.get_parent().get_parent().name
            if doc_id not in aggregated_doc:
                aggregated_doc[doc_id] = train_segment.get_parent().get_parent().sentences

        df_list = []
        print("csv paperID [start, end] as ", list(aggregated_doc.keys())[0], list(aggregated_doc.keys())[-1])

        for doc_id in aggregated_doc:
            globalPsn = 1
            for sent in aggregated_doc[doc_id]:
                sent_id = sent.id
                if sent_id not in aggregated_sent:
                    raise ValueError('we have no info about this sent' + str(sent))
                    break
                aggregated_sent[sent_id] = sorted(aggregated_sent[sent_id], key=lambda x: x[0])
                for idx, pair in enumerate(aggregated_sent[sent_id]):
                    text = pair[2]
                    df_list += [[pair[3], doc_id, globalPsn, text]]
                    globalPsn += 1

        df = pd.DataFrame(df_list, columns=['winningHighlight', 'paperID', 'globalPsn', 'content'])
        df.to_csv(open(csv_path, "w"))  # in the spreadsheet, punctuations are splitted
    except Exception as e:
        print(traceback.format_exc())


import sys
import _thread
smooth_window=0

def multi_thread_train_label(split):
    print("running train_bucket", split)
    # if len(session.query(Unigram).filter(Unigram.split == split).all())<docs_per_bucket*100:
    unigram_segment_extractor.apply(sents_split[split], split=split)
    session.commit()
    print("session commited")
    unigram_segments_tmp = session.query(Unigram).filter(Unigram.split == split).all()
    print("len(train_segments)", len(unigram_segments_tmp))
    print("applying L_train_tmp")
    L_train_tmp = get_L_train(purpose_LFs + mechanism_LFs + null_LFs, split=split)
    write_csv_from_L_train(L_train_tmp, "data/annotations_2k/largest-s2/onset_split_gz_" + str(train_bucket)+"_"+str(split)+ "_window" + str(smooth_window) + ".csv", session)
    print("write_csv_from_L_train finished")


for i in range((0 if len(sys.argv)==2 else int(sys.argv[-1])),len(sents_split)):
    try:
        multi_thread_train_label(i)
    except Exception as e:
        print(e)
        continue