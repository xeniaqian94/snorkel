from snorkel.lf_helpers import *

def LF_expressing_contrast(c):
    return 1 if rule_regex_search_candidate_text(c,"((^|\s)(however|nevertheless|despite|spite|yet).*$)|((^|\s)but(?!(also))*$)",1) else 0

def LF_excluded_pseudo_contrast(c):
    return -1 if rule_regex_search_candidate_text(c,"(^.*but sometimes.*$)|(^.*but also.*$)",1) else 0

def negate(f):
    return lambda x: -f(x)
