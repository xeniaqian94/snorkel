from snorkel.lf_helpers import *
from .util_common_default import create_LFs,candidate_pos_in_doc

finding_regex_list=[("we [a-z ]*show",1)]
finding_regex_list+=[("^results",1)]
finding_regex_list+=[("we [a-z ]*prove",1)]
finding_regex_list+=[("this uncovers",1)]
finding_regex_list+=[("observe(s)* that",1)]
finding_regex_list+=[("we [a-z ]*report",1)]
finding_regex_list+=[("our findings",1)]
finding_regex_list+=[("spots",1)]
finding_regex_list+=[("our results",1)]
finding_regex_list+=[("result(s)* on",1)]
finding_regex_list+=[("we [a-z ]*demonstrate",1)]
finding_regex_list+=[("we [a-z ]*find",1)]
finding_regex_list+=[("finally",1)]
finding_regex_list+=[("our experiments",1)]
finding_regex_list+=[("show(s)* that",1)]
finding_regex_list+=[("our [a-z ]* result",1)]
finding_regex_list+=[("indicate(s)* that",1)]
finding_regex_list+=[("yield",1)]
finding_regex_list+=[("showcase",1)]
finding_regex_list+=[("reveal(s)* that",1)]
finding_regex_list+=[("produce(s)*",1)]
finding_regex_list+=[("we [a-z ]*provide",1)]
finding_regex_list+=[("can also",1)]
finding_regex_list+=[("we [a-z ]*discover",1)]

def proper_finding_pos(c):
	relative_pos=candidate_pos_in_doc(c)
	return 1 if relative_pos>=0.6 else 0

def neg_proper_finding_pos(c):
	return -1*proper_finding_pos(c)
	

finding_LFs=[create_LFs(pair,"finding") for pair in finding_regex_list]+[proper_finding_pos]