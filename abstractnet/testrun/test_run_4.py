import os
import sys
from snorkel import SnorkelSession
from snorkel.parser.spacy_parser import Spacy
from snorkel.parser import CorpusParser
from snorkel.models import Document, Sentence
from snorkel.models.meta import create_session_with_conn
import argparse
from snorkel.models import candidate_subclass
from snorkel.candidates import Ngrams, CandidateExtractor
from snorkel.matchers import *
import imp

def extract_and_display(train_sents,dev_sents,test_sents, session, matcher,candidate_class,candidate_class_name,train_doc_breakdown_map=None,test_doc_breakdown_map=None,selected_split=0,is_print=True):  
	# split over train/dev/test but returns only train set
	print(type(matcher))
	for (i, sents) in ([(0,train_sents), (1,dev_sents), (2,test_sents)] if selected_split==0 else ([(2,test_sents)] if selected_split==2 else [(1,dev_sents)])):
		matcher.apply(sents, split=i)
		print("Split "+str(i)+" - number of candidates extracted: "+str(session.query(candidate_class).filter(candidate_class.split == i).count())+"\n\n")
	cands = session.query(candidate_class).filter(candidate_class.split == selected_split).all()
	if is_print:
		for i in range(min(4,len(cands))): # to print all cands, range(len(cands))
			print(str(i)+"/"+str(len(cands))+" Candidate/Span:\t"+str(cands[i]))
			print("Its parent Sentence's text:\t"+str(cands[i].get_parent().text))
			print("Its parent Document's text:\t"+str(cands[i].get_parent().get_parent().__dict__))
			print() 
		

	# add candidates into train_doc_breakdown_map
	if train_doc_breakdown_map is not None:
		for cand in cands:
			doc_name=cand.get_parent().get_parent().name
			if doc_name not in train_doc_breakdown_map:
				train_doc_breakdown_map[doc_name]=dict()
			if candidate_class_name not in train_doc_breakdown_map[doc_name]:
				train_doc_breakdown_map[doc_name][candidate_class_name]=[]
			train_doc_breakdown_map[doc_name][candidate_class_name]+=[cand]  
		
	if test_doc_breakdown_map is not None:
		cands = session.query(candidate_class).filter(candidate_class.split == 2).all()
		for cand in cands:
			doc_name=cand.get_parent().get_parent().name
			if doc_name not in test_doc_breakdown_map:
				test_doc_breakdown_map[doc_name]=dict()
			if candidate_class_name not in test_doc_breakdown_map[doc_name]:
				test_doc_breakdown_map[doc_name][candidate_class_name]=[]
			test_doc_breakdown_map[doc_name][candidate_class_name]+=[cand]
	
	return cands


def main(argv):
	parser = argparse.ArgumentParser(description='Process some arguments.')
	parser.add_argument('--dbPath', type=str, default=os.getcwd() + os.sep + 'snorkel.db',
					   help='the path of snorkel database')
	parser.add_argument('--lfPath', type=str,default=os.getcwd() + os.sep + 'util_default.py',
					   help='the path of util.py file where labelling functions were defined')

	args = parser.parse_args()
	
	# Connect to db, and get session

	util_module=imp.load_source("module.name",args.lfPath)
	train_doc_breakdown_map=dict() # maps doc_id into a dict of ["Background", "Purpose", "Mechanism", "Method", "Finding"]
	test_doc_breakdown_map=dict()

	SnorkelSession=create_session_with_conn("sqlite:///"+args.dbPath)
	session=SnorkelSession()

	print("Documents:", session.query(Document).count())
	print("Sentences:", session.query(Sentence).count())

	sents = session.query(Sentence).all()
	n_max_corpus=0
	for sent in sents:
		n_max_corpus=max(n_max_corpus,len(sent.words))

	print("The longest sentence has "+str(n_max_corpus)+" tokens.")

	ngrams = Ngrams(n_max=n_max_corpus)

	# from util import number_of_people

	docs = session.query(Document).all()

	train_sents = set()
	dev_sents   = set()
	test_sents  = set()

	for i, doc in enumerate(docs):
		for s in doc.sentences:
			if i % 10 == 8 and "cscw18"!=doc.name[:6]:
				dev_sents.add(s)
			elif "cscw18"==doc.name[:6]:  # replace the earlier 10% test documents as cscw'18 annotation guideline 10 examples
				test_sents.add(s)
			elif "cscw18"!=doc.name[:6]:
				train_sents.add(s)


	# load segment_candidate_class and corresponding_matcher, e.g. (Background, non_comma_dict_background_matcher)
	# Background,background_matcher=util_module.get_segment_class_and_matcher("Background",ngrams)
	# background_cands=extract_and_display(train_sents,dev_sents,test_sents, session, background_matcher,Background,"Background",train_doc_breakdown_map=train_doc_breakdown_map,test_doc_breakdown_map=test_doc_breakdown_map)

	# Purpose,purpose_matcher=util_module.get_segment_class_and_matcher("Purpose",ngrams)
	# purpose_cands=extract_and_display(train_sents,dev_sents,test_sents, session, purpose_matcher,Purpose,"Purpose",train_doc_breakdown_map=train_doc_breakdown_map,test_doc_breakdown_map=test_doc_breakdown_map)

	Mechanism,mechanism_matcher=util_module.get_segment_class_and_matcher("Mechanism",ngrams)
	mechanism_cands=extract_and_display(train_sents,dev_sents,test_sents, session, mechanism_matcher,Mechanism,"Mechanism",train_doc_breakdown_map=train_doc_breakdown_map,test_doc_breakdown_map=test_doc_breakdown_map)

	Method,method_matcher=util_module.get_segment_class_and_matcher("Method",ngrams)
	method_cands=extract_and_display(train_sents,dev_sents,test_sents, session, method_matcher,Method,"Method",train_doc_breakdown_map=train_doc_breakdown_map,test_doc_breakdown_map=test_doc_breakdown_map)

	Finding,finding_matcher=util_module.get_segment_class_and_matcher("Finding",ngrams)
	finding_cands=extract_and_display(train_sents,dev_sents,test_sents, session, finding_matcher,Finding,"Finding",train_doc_breakdown_map=train_doc_breakdown_map,test_doc_breakdown_map=test_doc_breakdown_map)



if __name__ == "__main__":
   main(sys.argv[1:])


