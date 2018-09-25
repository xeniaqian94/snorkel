from snorkel.lf_helpers import *


from .util_common_default import create_LFs,candidate_pos_in_doc
from .util_background_default import background_regex_list,neg_proper_background_pos
from .util_mechanism_default import mechanism_regex_list,mechanism_LFs,neg_proper_mechanism_pos
from .util_method_default import method_regex_list,neg_proper_method_pos
from .util_finding_default import finding_regex_list,neg_proper_finding_pos


# Part 1: common regex 8 LFs, about contrast 
# common_regex_list are a list of tuples in the format of (regex, label_if_match_1_or_-1)
common_regex_list=[("((^|\s)however.*$)",1)]
common_regex_list+=[("((^|\s)nevertheless.*$)",1)]
common_regex_list+=[("((^|\s)despite.*$)",1)]
common_regex_list+=[("((^|\s)spite.*$)",1)]
common_regex_list+=[("((^|\s)yet.*$)",1)]
common_regex_list+=[("((^|\s)but.*$)",1)]
common_regex_list+=[("(^.*but sometimes.*$)",-1)]
common_regex_list+=[("(^.*but also.*$)",-1)]
common_LFs=[create_LFs(pair,"common") for pair in common_regex_list]


# Part 2: purpose-specific regex

# Part 2.1: existing 15 LFs
purpose_regex_list=[("(.*more [a-z ]* than.*$)",1)]
purpose_regex_list+=[("(.*er than.*$)",1)]
purpose_regex_list+=[("(.*in order to.*$)",1)]
purpose_regex_list+=[("(.* implication.*$)",1)]
purpose_regex_list+=[("(.*to solve.*$)",1)]
purpose_regex_list+=[("(.* hypothesis.*$)",1)]
purpose_regex_list+=[("(.*to enable.*$)",1)]
purpose_regex_list+=[("(.*to aid.*$)",1)]
purpose_regex_list+=[("(.*to produce.*$)",1)]
purpose_regex_list+=[("(.*to investigat.*$)",1)]
purpose_regex_list+=[("(.* give.*$)",1)]
purpose_regex_list+=[("(.* that can .*$)",1)]
purpose_regex_list+=[("(.* examine.*$)",1)]
purpose_regex_list+=[("(.* extend.*$)",1)]
purpose_regex_list+=[("(.* offer.*$)",1)]

# Part 2.2: new 58 LFs added 090218
purpose_regex_list+=[("(.*we consider.*)",1)]
purpose_regex_list+=[("(.*how[ a-z]+can.*)",1)]
purpose_regex_list+=[("(.*we study.*)",1)]
purpose_regex_list+=[("(.*we are interested in .*)",1)]
purpose_regex_list+=[("(.*way to.*)",1)]
purpose_regex_list+=[("(.*we seek.*)",1)]
purpose_regex_list+=[("(.*initiate.*)",1)]
purpose_regex_list+=[("(.*the question of how.*)",1)]
purpose_regex_list+=[("(.*for[ a-z]+ing.*)",1)]
purpose_regex_list+=[("(.* do .*)",1)]
purpose_regex_list+=[("(.* does .*)",1)]
purpose_regex_list+=[("(.*to address.*)",1)]
purpose_regex_list+=[("(.*which can.*)",1)]
purpose_regex_list+=[("(.*to extract.*)",1)]
purpose_regex_list+=[("((^|\s)what .*)",1)]
purpose_regex_list+=[("(.*focus.*)",1)]
purpose_regex_list+=[("(.*allow.*)",1)]
purpose_regex_list+=[("(.*explain.*)",1)]
purpose_regex_list+=[("(.*answer.*)",1)]
purpose_regex_list+=[("(.*discuss.*)",1)]
purpose_regex_list+=[("(.*discover.*)",1)]
purpose_regex_list+=[("(.*solve.*)",1)]
purpose_regex_list+=[("(.*argue.*)",1)]
purpose_regex_list+=[("(.*enable.*)",1)]
purpose_regex_list+=[("(.*one can only.*)",1)]
purpose_regex_list+=[("(.*in order for.*)",1)]
purpose_regex_list+=[("(.*a[a-z ]+problem.*)",1)]
purpose_regex_list+=[("(.*to further.*)",1)]
purpose_regex_list+=[("(.*to find.*)",1)]
purpose_regex_list+=[("(.*why.*)",1)]
purpose_regex_list+=[("(.*current.*)",1)]
purpose_regex_list+=[("(.*today.*)",1)]
purpose_regex_list+=[("(.*recent .*)",1)]  # we don't want to have recently?? more like background?
purpose_regex_list+=[("(.*we ask.*)",1)]
purpose_regex_list+=[("(.*can we.*)",1)]
purpose_regex_list+=[("(.*for the .*)",1)]
purpose_regex_list+=[("(.*as a[n]* [a-z]*er.*)",1)]
purpose_regex_list+=[("(.*as a more .*)",1)]
purpose_regex_list+=[("(.*objective.*)",1)]
purpose_regex_list+=[("(.*often.*)",1)]
purpose_regex_list+=[("(.*an extension to.*)",1)]
purpose_regex_list+=[("(.* problem.*)",1)]
purpose_regex_list+=[("(.*challeng.*)",1)] # challenging or challenge
purpose_regex_list+=[("(.*task.*)",1)] # challenging or challenge
purpose_regex_list+=[("(.* goal.*)",1)]
purpose_regex_list+=[("(.*especially if.*)",1)]
purpose_regex_list+=[("(.*how [a-z ]* do[es]* .*)",1)]
purpose_regex_list+=[("(.* no .*)",1)]
purpose_regex_list+=[("(.* first.*)",1)]
purpose_regex_list+=[("(.*fail to.*)",1)]
purpose_regex_list+=[("(.*what is.*)",1)]
purpose_regex_list+=[("(.*what are.*)",1)]
purpose_regex_list+=[("(.*is needed.*)",1)]
purpose_regex_list+=[("(.*necessary.*)",1)]
purpose_regex_list+=[("(.*too [a-z ]* to.*)",1)]
purpose_regex_list+=[("(.*prohibitive.*)",1)]  # negative sentiment towards past progress/approach
purpose_regex_list+=[("(.*alternative to.*)",1)]
purpose_regex_list+=[("(.*solutions for.*)",1)]

def proper_purpose_pos(c):
	relative_pos=candidate_pos_in_doc(c)
	return 1 if (relative_pos<=0.4 or relative_pos>=0.8) else 0

def neg_proper_purpose_pos(c):
	return -1*proper_purpose_pos(c)

purpose_LFs=[create_LFs(pair,"purpose") for pair in purpose_regex_list]+[proper_purpose_pos]


## Below we declare a list of reverse LFs, -1 if match 
neg_for_purpose_LFs=[create_LFs((pair[0],-1*pair[1]),"neg_"+segment_name) for (regex_list,segment_name) in [(background_regex_list,"background"),(mechanism_regex_list,"mechanism"),(method_regex_list,"method"),(finding_regex_list,"finding")] for pair in regex_list ]+[neg_proper_finding_pos,neg_proper_method_pos,neg_proper_mechanism_pos,neg_proper_background_pos]

neg_for_mechanism_LFs=[create_LFs((pair[0],-1*pair[1]),"neg_"+segment_name) for (regex_list,segment_name) in [(background_regex_list,"background"),(purpose_regex_list+common_regex_list,"purpose"),(method_regex_list,"method"),(finding_regex_list,"finding")] for pair in regex_list ]+[neg_proper_finding_pos,neg_proper_method_pos,neg_proper_purpose_pos,neg_proper_background_pos]

neg_for_background_LFs=[create_LFs((pair[0],-1*pair[1]),"neg_"+segment_name) for (regex_list,segment_name) in [(purpose_regex_list+common_regex_list,"purpose"),(mechanism_regex_list,"mechanism"),(method_regex_list,"method"),(finding_regex_list,"finding")] for pair in regex_list ]+[neg_proper_finding_pos,neg_proper_method_pos,neg_proper_mechanism_pos,neg_proper_purpose_pos]

neg_for_method_LFs=[create_LFs((pair[0],-1*pair[1]),"neg_"+segment_name) for (regex_list,segment_name) in [(background_regex_list,"background"),(purpose_regex_list+common_regex_list,"purpose"),(mechanism_regex_list,"mechanism"),(finding_regex_list,"finding")] for pair in regex_list ]+[neg_proper_finding_pos,neg_proper_purpose_pos,neg_proper_mechanism_pos,neg_proper_background_pos]

neg_for_finding_LFs=[create_LFs((pair[0],-1*pair[1]),"neg_"+segment_name) for (regex_list,segment_name) in [(background_regex_list,"background"),(purpose_regex_list+common_regex_list,"purpose"),(method_regex_list,"method"),(mechanism_regex_list,"mechanism")] for pair in regex_list ]+[neg_proper_purpose_pos,neg_proper_method_pos,neg_proper_mechanism_pos,neg_proper_background_pos]



### below are *Deprecated(old)* LFs who are no longer being used. 

def LF_comparative_degree(c):
    return 1 if rule_regex_search_candidate_text(c,"(.*more.*than.*$)|(.*er than.*$)",1) else 0

def LF_purpose_verb(c):
    return 1 if rule_regex_search_candidate_text(c,"(.*in order to.*$)|(.* implication.*$)|(.* to solve.*$)|(.* hypothesis.*$)|(.*to enable.*$)|(.*to aid.*$)|(.*to produce.*$)|(.*to investigat.*$)|(.* give.*$)|(.* that can .*$)|(.* examine.*$)|(.* extend.*$)|(.* offer.*$)",1) else 0

def LF_purpose_delimiter(c):
    return 1 if rule_regex_search_candidate_text(c,"(.*in this paper.*$)|(.*in the paper.*$)|(.*in this study.*$)",1) else 0

def LF_purpose_adj_problem(c):
    return 1 if rule_regex_search_candidate_text(c,"(.* challenging.*$)|(.* captivating.*$)|(.* engaging.*$)|(.* interesting.*$)",1) else 0

def LF_purpose_leading_question_word(c):
    return 1 if rule_regex_search_candidate_text(c,"(.*how to.*$)|(.*what .*$)|(.*why .*$)",1) else 0



###  below are *Deprecated(old)*, splitted LFs
def LF_comparative_degree_morethan(c):
	return 1 if rule_regex_search_candidate_text(c,"(.*more.*than.*$)",1) else 0 

def LF_comparative_degree_fooerthan(c):
	return 1 if rule_regex_search_candidate_text(c,"(.*er than.*$)",1) else 0

def LF_purpose_verb_inorderto(c):
	return 1 if rule_regex_search_candidate_text(c,"(.*in order to.*$)",1) else 0

def LF_purpose_verb_implication(c):
	return 1 if rule_regex_search_candidate_text(c,"(.* implication.*$)",1) else 0

def LF_purpose_verb_solve(c):
	return 1 if rule_regex_search_candidate_text(c,"(.*to solve.*$)",1) else 0

def LF_purpose_verb_hypothesis(c):
	return 1 if rule_regex_search_candidate_text(c,"(.* hypothesis.*$)",1) else 0

def LF_purpose_verb_toenable(c):
	return 1 if rule_regex_search_candidate_text(c,"(.*to enable.*$)",1) else 0

def LF_purpose_verb_toaid(c):
	return 1 if rule_regex_search_candidate_text(c,"(.*to aid.*$)",1) else 0

def LF_purpose_verb_toproduce(c):
	return 1 if rule_regex_search_candidate_text(c,"(.*to produce.*$)",1) else 0

def LF_purpose_verb_toinvestigate(c):
	return 1 if rule_regex_search_candidate_text(c,"(.*to investigat.*$)",1) else 0

def LF_purpose_verb_togive(c):
	return 1 if rule_regex_search_candidate_text(c,"(.* give.*$)",1) else 0

def LF_purpose_verb_thatcan(c):
	return 1 if rule_regex_search_candidate_text(c,"(.* that can .*$)",1) else 0

def LF_purpose_verb_examine(c):
	return 1 if rule_regex_search_candidate_text(c,"(.* examine.*$)",1) else 0

def LF_purpose_verb_extend(c):
	return 1 if rule_regex_search_candidate_text(c,"(.* extend.*$)",1) else 0

def LF_purpose_verb_offer(c):
	return 1 if rule_regex_search_candidate_text(c,"(.* offer.*$)",1) else 0

