from snorkel.lf_helpers import *
import re

def create_LFs(pair,lf_prefix):
    # (regex_str,label)=pair

    def func(c):
        return rule_regex_search_candidate_text(c,pair[0],pair[1]) 

    # print(func.__name__)
    func.__name__="LF_"+lf_prefix+"_"+re.sub('[^0-9a-zA-Z]+', '_', pair[0]).strip("_")
    # print(func.__name__)

    return func


def LF_expressing_contrast(c):
    return 1 if rule_regex_search_candidate_text(c,"((^|\s)(however|nevertheless|despite|spite|yet).*$)|((^|\s)but(?!(also))*$)",1) else 0

def LF_excluded_pseudo_contrast(c):
    return -1 if rule_regex_search_candidate_text(c,"(^.*but sometimes.*$)|(^.*but also.*$)",1) else 0

def negate(f):
    return lambda x: -f(x)


### below are splitted LF, since all are about purpose, on 9/2/18, we merged them into util_purpose_default.py

def LF_expressing_contrast_however(c):
    return 1 if rule_regex_search_candidate_text(c,"((^|\s)however.*$)",1) else 0

def LF_expressing_contrast_nevertheless(c):
    return 1 if rule_regex_search_candidate_text(c,"((^|\s)nevertheless.*$)",1) else 0

def LF_expressing_contrast_despite(c):
    return 1 if rule_regex_search_candidate_text(c,"((^|\s)despite.*$)",1) else 0

def LF_expressing_contrast_spite(c):
    return 1 if rule_regex_search_candidate_text(c,"((^|\s)spite.*$)",1) else 0

def LF_expressing_contrast_yet(c):
    return 1 if rule_regex_search_candidate_text(c,"((^|\s)yet.*$)",1) else 0

def LF_expressing_contrast_but(c):
    return 1 if rule_regex_search_candidate_text(c,"((^|\s)but.*$)",1) else 0

def LF_excluded_pseudo_contrast_butsometimes(c):
    return -1 if rule_regex_search_candidate_text(c,"(^.*but sometimes.*$)",1) else 0

def LF_excluded_pseudo_contrast_butalso(c):
    return -1 if rule_regex_search_candidate_text(c,"(^.*but also.*$)",1) else 0



