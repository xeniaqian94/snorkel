method_regex_list=[]

from snorkel.lf_helpers import *
from .util_common_default_categorical import create_LFs,candidate_pos_in_doc,NULL_LABEL


method_regex_list+=[("real data",NULL_LABEL)]
# method_regex_list+=[("theoretical",NULL_LABEL)]
method_regex_list+=[("empirical",NULL_LABEL)]
# method_regex_list+=[("observation",NULL_LABEL)]
method_regex_list+=[("dataset",NULL_LABEL)]
# method_regex_list+=[("by performing",NULL_LABEL)]

# # we filtered low precision regex when we change to categorical 
# method_regex_list=[("in theory",NULL_LABEL)]  # theoretical analysis
# method_regex_list+=[("experiment",NULL_LABEL)] # which includes experimentation, experimentally, experiments
# method_regex_list+=[("analysis",NULL_LABEL)]
# method_regex_list+=[("evaluation",NULL_LABEL)]
# method_regex_list+=[("network",NULL_LABEL)]

def proper_method_pos(c):
	relative_pos=candidate_pos_in_doc(c)
	return NULL_LABEL if relative_pos>=0.4 else 0
	
def neg_proper_method_pos(c):
	return -1*proper_method_pos(c)

method_LFs=[create_LFs(pair,"method") for pair in method_regex_list]#+[proper_method_pos]

