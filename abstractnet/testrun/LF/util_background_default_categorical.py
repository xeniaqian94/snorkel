from snorkel.lf_helpers import *
from .util_common_default_categorical import create_LFs,candidate_pos_in_doc,NULL_LABEL

background_regex_list=[]
background_regex_list+=[("a key challenge",NULL_LABEL)]
background_regex_list+=[("is a [a-z ]*task",NULL_LABEL)]
background_regex_list+=[("a central topic",NULL_LABEL)]
background_regex_list+=[("the development of",NULL_LABEL)]
background_regex_list+=[("modern",NULL_LABEL)]
background_regex_list+=[("has emerged",NULL_LABEL)]
background_regex_list+=[("emergence of",NULL_LABEL)]
background_regex_list+=[("the [a-z ]* community",NULL_LABEL)]
background_regex_list+=[("for decades",NULL_LABEL)]
background_regex_list+=[("classic",NULL_LABEL)]
background_regex_list+=[("a [a-z ]* problem in",NULL_LABEL)]
background_regex_list+=[("arises",NULL_LABEL)]
background_regex_list+=[("has been an issue",NULL_LABEL)]

# exclude potentially low precision background regex 
# background_regex_list=[("typically",NULL_LABEL)]
# background_regex_list+=[("motivated by",NULL_LABEL)]
# background_regex_list+=[("previous work",NULL_LABEL)]
# background_regex_list+=[("has been",NULL_LABEL)]
# background_regex_list+=[("if we",NULL_LABEL)]
# background_regex_list+=[("prior research",NULL_LABEL)]
# background_regex_list+=[("difficult problem",NULL_LABEL)]
# background_regex_list+=[("recent [a-z ]*work",NULL_LABEL)]
# background_regex_list+=[("variety",NULL_LABEL)]
# background_regex_list+=[("various",NULL_LABEL)]
# background_regex_list+=[("has led to",NULL_LABEL)]
# background_regex_list+=[("to the best of our knowledge",NULL_LABEL)]
# background_regex_list+=[("unsolved",NULL_LABEL)]
# background_regex_list+=[("how many",NULL_LABEL)]
# background_regex_list+=[("how about",NULL_LABEL)]
# background_regex_list+=[("implications for",NULL_LABEL)]
# background_regex_list+=[("rarely",NULL_LABEL)]
# background_regex_list+=[("could we",NULL_LABEL)]
# background_regex_list+=[("how often",NULL_LABEL)]
# background_regex_list+=[("has the potential",NULL_LABEL)]
# background_regex_list+=[("how can",NULL_LABEL)]

def proper_background_pos(c):
	return NULL_LABEL if candidate_pos_in_doc(c)<=0.2 else 0

def neg_proper_background_pos(c):
	return -1*proper_background_pos(c)
	
background_LFs=[create_LFs(pair,"background") for pair in background_regex_list]# +[proper_background_pos]


