from snorkel.lf_helpers import *
from .util_common_default import create_LFs,candidate_pos_in_doc

background_regex_list=[("typically",1)]
background_regex_list+=[("motivated by",1)]
background_regex_list+=[("previous work",1)]
background_regex_list+=[("a [a-z ]* problem in",1)]
background_regex_list+=[("classic",1)]
background_regex_list+=[("has been",1)]
background_regex_list+=[("for decades",1)]
background_regex_list+=[("a key challenge",1)]
background_regex_list+=[("if we",1)]
background_regex_list+=[("is a [a-z ]*task",1)]
background_regex_list+=[("prior research",1)]
background_regex_list+=[("how can",1)]
background_regex_list+=[("difficult problem",1)]
background_regex_list+=[("recent [a-z ]*work",1)]
background_regex_list+=[("variety",1)]
background_regex_list+=[("various",1)]
background_regex_list+=[("previous work",1)]
background_regex_list+=[("the [a-z ]* community",1)]
background_regex_list+=[("has led to",1)]
background_regex_list+=[("emergence of",1)]
background_regex_list+=[("to the best of our knowledge",1)]
background_regex_list+=[("a central topic",1)]
background_regex_list+=[("unsolved",1)]
background_regex_list+=[("how many",1)]
background_regex_list+=[("how about",1)]
background_regex_list+=[("implications for",1)]
background_regex_list+=[("has been an issue",1)]
background_regex_list+=[("has emerged",1)]
background_regex_list+=[("rarely",1)]
background_regex_list+=[("arises",1)]
background_regex_list+=[("could we",1)]
background_regex_list+=[("how often",1)]
background_regex_list+=[("the development of",1)]
background_regex_list+=[("has the potential",1)]
background_regex_list+=[("modern",1)]

def proper_background_pos(c):
	return 1 if candidate_pos_in_doc(c)<=0.2 else 0

def neg_proper_background_pos(c):
	return -1*proper_background_pos(c)
	
background_LFs=[create_LFs(pair,"background") for pair in background_regex_list]+[proper_background_pos]


