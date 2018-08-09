from snorkel.lf_helpers import *

def LF_expressing_contrast(c):
    return 1 if rule_regex_search_candidate_text(c,"((^|\s)(however|nevertheless|despite|spite|yet).*$)|((^|\s)but(?!(also))*$)",1) else 0

def LF_excluded_pseudo_contrast(c):
    return -1 if rule_regex_search_candidate_text(c,"(^.*but sometimes.*$)|(^.*but also.*$)",1) else 0

def negate(f):
    return lambda x: -f(x)


### below are splitted LF
def LF_expressing_contrast_however(c):
    return 1 if rule_regex_search_candidate_text(c,"(^|\s)however.*$)",1) else 0

def LF_expressing_contrast_nevertheless(c):
    return 1 if rule_regex_search_candidate_text(c,"(^|\s)nevertheless.*$)",1) else 0

def LF_expressing_contrast_despite(c):
    return 1 if rule_regex_search_candidate_text(c,"(^|\s)despite.*$)",1) else 0

def LF_expressing_contrast_spite(c):
    return 1 if rule_regex_search_candidate_text(c,"(^|\s)spite.*$)",1) else 0

def LF_expressing_contrast_yet(c):
    return 1 if rule_regex_search_candidate_text(c,"(^|\s)yet.*$)",1) else 0

def LF_expressing_contrast_but(c):
    return 1 if rule_regex_search_candidate_text(c,"(^|\s)but.*$)",1) else 0

def LF_excluded_pseudo_contrast_butsometimes(c):
    return -1 if rule_regex_search_candidate_text(c,"(^.*but sometimes.*$)",1) else 0

def LF_excluded_pseudo_contrast_butalso(c):
    return -1 if rule_regex_search_candidate_text(c,"(^.*but also.*$)",1) else 0