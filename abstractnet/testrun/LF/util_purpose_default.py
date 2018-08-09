from snorkel.lf_helpers import *

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





###  below are splitted LFs
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


