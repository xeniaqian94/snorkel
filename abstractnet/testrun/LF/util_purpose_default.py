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