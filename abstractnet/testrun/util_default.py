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


# Compound Matcher for Background: 

def get_segment_class_and_matcher(name,ngrams=None,non_comma_matcher=DictionaryMatch(d=[','],longest_match_only=True,reverse=True)):

	transition_prev_work=DictionaryMatch(d=['previous','earlier','past'],longest_match_only=True)

	if name.lower()=="background":
		Background = candidate_subclass('Background', ['background_cue'])
		transition_word=DictionaryMatch(d=['while','unlike','despite'],longest_match_only=True) 
		dict_background_matcher=DictionaryMatch(d=['previous work','traditionally','researchers'],longest_match_only=True) 
		excluded_dict_background_matcher=DictionaryMatch(d=['we','unlike','our'],longest_match_only=True,reverse=True) 
		non_comma_dict_background_matcher=CandidateExtractor(Background, [ngrams], [Intersection(non_comma_matcher,Union(dict_background_matcher,Intersection(transition_word,transition_prev_work)),excluded_dict_background_matcher)])
		return Background,non_comma_dict_background_matcher

	elif name.lower()=="purpose":
		Purpose=candidate_subclass('Purpose',['purpose_cue'])

		transition_regex_matcher=RegexMatchSpan(rgx="((^|\s)however.*$)|((^|\s)but(?!(also))*$)",longest_match_only=True)  # Correction: purpose 
		excluded_dict_purpose_matcher=SentenceMatch(d=['but also','but without','but sometimes'],longest_match_only=True,reverse=True)  # the parent sentence shall not include "but also"
		transition_matcher=Intersection(transition_regex_matcher,excluded_dict_purpose_matcher)
		comparative_degree_matcher=Intersection(RegexMatchSpan(rgx="(.*more.*than.*$)|(.*er than.*$)",longest_match_only=True),transition_prev_work)  # Correction: purpose 
		other_regex_matcher=RegexMatchSpan(rgx="(.*extend.*$)|(.*offer.*$)",longest_match_only=True)
		dict_purpose_matcher=DictionaryMatch(d=['in this paper','in the paper',' that can ','in this study','to examine','we examine','to investigate','implications'],longest_match_only=True) 
		non_comma_dict_purpose_matcher=CandidateExtractor(Purpose, [ngrams], [Intersection(non_comma_matcher,Union(comparative_degree_matcher,other_regex_matcher,dict_purpose_matcher,transition_matcher))]) #,intersection(excluded_dict_purpose_matcher,transition_regex_matcher)])
		return Purpose, non_comma_dict_purpose_matcher

	elif name.lower()=="mechanism":
		Mechanism = candidate_subclass('Mechanism', ['mechanism_cue']) 
		dict_mechanism_matcher=DictionaryMatch(d=['introduce','introduces','propose','proposes','we propose','we develop','approach'],longest_match_only=True) 
		non_comma_dict_mechanism_matcher=CandidateExtractor(Mechanism, [ngrams], [Intersection(non_comma_matcher,dict_mechanism_matcher)])
		return Mechanism, non_comma_dict_mechanism_matcher

	elif name.lower()=="method":
		Method = candidate_subclass('Method', ['method_cue'])
		dict_method_matcher=DictionaryMatch(d=['dataset','benchmark','experiment ','experiments',"empirical","participant","survey"," conduct"," analyze"],longest_match_only=True) 
		non_comma_dict_method_matcher=CandidateExtractor(Method, [ngrams], [Intersection(non_comma_matcher,dict_method_matcher)])
		return Method, non_comma_dict_method_matcher

	elif name.lower()=="finding":
		Finding = candidate_subclass('Finding', ['finding_cue'])
		dict_finding_matcher=DictionaryMatch(d=['show that','shows that','found','indicate','results','performance','find'],longest_match_only=True) 
		non_comma_dict_finding_matcher=CandidateExtractor(Finding, [ngrams], [Intersection(non_comma_matcher,dict_finding_matcher)])
		return Finding, non_comma_dict_finding_matcher
		


		