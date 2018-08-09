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



# below are splitted LFs

def LF_mechanism_verb_introduce(c):
	return 1 if rule_regex_search_candidate_text(c,"((^|\s)introduce.*$)",1) else 0

def LF_mechanism_verb_propose(c):
	return 1 if rule_regex_search_candidate_text(c,"((^|\s)propose.*$)",1) else 0

def LF_mechanism_verb_develop(c):
	return 1 if rule_regex_search_candidate_text(c,"((^|\s)develop.*$)",1) else 0

def LF_mechanism_verb_approach(c):
	return 1 if rule_regex_search_candidate_text(c,"((^|\s)approach.*$)",1) else 0

def LF_mechanism_verb_applied(c):
	return 1 if rule_regex_search_candidate_text(c,"((^|\s)applied.*$)",1) else 0

def LF_mechanism_verb_apply(c):
	return 1 if rule_regex_search_candidate_text(c,"((^|\s)apply.*$)",1) else 0

def LF_mechanism_verb_develop(c):
	return 1 if rule_regex_search_candidate_text(c,"((^|\s)develop.*$)",1) else 0

def LF_mechanism_verb_using(c):
	return 1 if rule_regex_search_candidate_text(c,"((^|\s)using.*$)",1) else 0

def LF_mechanism_verb_present(c):
	return 1 if rule_regex_search_candidate_text(c,"((^|\s)present.*$)",1) else 0

def LF_mechanism_verb_contribute(c):
	return 1 if rule_regex_search_candidate_text(c,"((^|\s)contribute.*$)",1) else 0

def LF_mechanism_verb_build(c):
	return 1 if rule_regex_search_candidate_text(c,"((^|\s)build.*$)",1) else 0

def LF_mechanism_verb_built(c):
	return 1 if rule_regex_search_candidate_text(c,"((^|\s)built.*$)",1) else 0


