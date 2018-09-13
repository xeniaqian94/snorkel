method_regex_list=[]

from snorkel.lf_helpers import *
from .util_common_default import create_LFs,candidate_pos_in_doc

method_regex_list=[("in theory",1)]  # theoretical analysis
method_regex_list+=[("real data",1)]
method_regex_list+=[("theoretical",1)]
method_regex_list+=[("empirical",1)]
method_regex_list+=[("experiment",1)] # which includes experimentation, experimentally, experiments
method_regex_list+=[("observation",1)]
method_regex_list+=[("analysis",1)]
method_regex_list+=[("dataset",1)]
method_regex_list+=[("by performing",1)]
method_regex_list+=[("evaluation",1)]
method_regex_list+=[("network",1)]

def proper_method_pos(c):
	relative_pos=candidate_pos_in_doc(c)
	return 1 if relative_pos>=0.4 else 0
	
def neg_proper_method_pos(c):
	return -1*proper_method_pos(c)

method_LFs=[create_LFs(pair,"method") for pair in method_regex_list]+[proper_method_pos]

