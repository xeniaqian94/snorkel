from snorkel.lf_helpers import *
import re


PURPOSE_LABEL="PP"
MECHANISM_LABEL="MN"
NULL_LABEL="NULL"

def create_LFs(pair,lf_prefix):
    # (regex_str,label)=pair

    def func(c):
        # print("working on c")
        return rule_regex_search_candidate_text(c,pair[0],pair[1]) 
        
    # print(func.__name__)
    func.__name__=create_function_name(lf_prefix,pair[0])

    # "LF_"+lf_prefix+"_"+re.sub('[^0-9a-zA-Z]+', '_', pair[0]).strip("_")
    # print(func.__name__)

    return func


def create_POS_LFs(pair,lf_prefix):
    def func(c):
        # pair[0] as the pos tag pattern (space delimited), pair[1] is the corresponding label if matched
        return rule_pos_tag_pattern_search(c,pair[0],pair[1])

    func.__name__=create_function_name(lf_prefix,pair[0])

    return func

def create_function_name(lf_prefix,match_pattern):
    return "LF_"+lf_prefix+"_"+re.sub('[^0-9a-zA-Z]+', '_', match_pattern).strip("_")


def candidate_pos_in_doc(c):
    sent=c.get_parent()
    sents=sent.get_parent().sentences
    return sents.index(sent)*1.0/len(sents)
