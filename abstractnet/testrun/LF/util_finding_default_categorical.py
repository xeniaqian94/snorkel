from snorkel.lf_helpers import *
from .util_common_default_categorical import create_LFs,candidate_pos_in_doc,NULL_LABEL

finding_regex_list=[("we [a-z ]*show",NULL_LABEL)]
finding_regex_list+=[("^results",NULL_LABEL)]
finding_regex_list+=[("this uncovers",NULL_LABEL)]
finding_regex_list+=[("observe(s)* that",NULL_LABEL)]
finding_regex_list+=[("[a-z ]*report",NULL_LABEL)]
finding_regex_list+=[("findings",NULL_LABEL)]
finding_regex_list+=[("spots",NULL_LABEL)]
finding_regex_list+=[("our results",NULL_LABEL)]
finding_regex_list+=[("result(s)* on",NULL_LABEL)]
finding_regex_list+=[("we [a-z ]*find",NULL_LABEL)]
finding_regex_list+=[("finally",NULL_LABEL)]
finding_regex_list+=[("our experiments",NULL_LABEL)]
finding_regex_list+=[("show(s)*",NULL_LABEL)]
finding_regex_list+=[("our [a-z ]* result",NULL_LABEL)]
finding_regex_list+=[("indicate(s)* that",NULL_LABEL)]
finding_regex_list+=[("yield",NULL_LABEL)]
finding_regex_list+=[("showcase",NULL_LABEL)]
finding_regex_list+=[("reveal(s)* that",NULL_LABEL)]
finding_regex_list+=[("produce(s)*",NULL_LABEL)]
# finding_regex_list+=[("can also",NULL_LABEL)]
# finding_regex_list+=[("[a-z ]*discover",NULL_LABEL)]

# potentially low-precision finding regex
# finding_regex_list+=[("we [a-z ]*prove",NULL_LABEL)]
# finding_regex_list+=[("we [a-z ]*demonstrate",NULL_LABEL)]
# finding_regex_list+=[("we [a-z ]*provide",NULL_LABEL)]

def proper_finding_pos(c):
	relative_pos=candidate_pos_in_doc(c)
	return NULL_LABEL if relative_pos>=0.6 else 0

def neg_proper_finding_pos(c):
	return -1*proper_finding_pos(c)
	

finding_LFs=[create_LFs(pair,"finding") for pair in finding_regex_list]# +[proper_finding_pos]