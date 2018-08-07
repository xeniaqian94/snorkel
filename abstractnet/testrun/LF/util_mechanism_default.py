from snorkel.lf_helpers import *


def LF_mechanism_verb(c):
    return 1 if rule_regex_search_candidate_text(c,"((^|\s)(introduce|propose|develop|approach|applied|apply|using|present|contribute|build|built).*$)",1) else 0

# def LF_not_purpose_but_mechanism_verb(c):
#     return 0 if rule_regex_search_candidate_text(c,"((^|\s)(introduce|propose|develop|approach|applied|apply|using|present|contribute|build|built).*$)",1) else 1

def LF_mechanism_adv(c):
    return 1 if rule_regex_search_candidate_text(c,"((^|\s)(specifically|particularly|particular).*$)",1) else 0

def LF_mechanism_noun(c):
    return 1 if rule_regex_search_candidate_text(c,"((^|\s)(framework|algorithm|model|module|mechanism).*$)",1) else 0

def LF_mechanism_adj(c):
    return 1 if rule_regex_search_candidate_text(c,"((^|\s)(simple|general|effective|efficient).*$)",1) else 0