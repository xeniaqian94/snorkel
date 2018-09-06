from snorkel.lf_helpers import *


from .util_common_default import create_LFs
# from .util_background_default import background_regex_list
# from .util_purpose_default import purpose_regex_list
# from .util_method_default import method_regex_list
# from .util_finding_default import finding_regex_list

# Part 1.1: existing 11 LFs
mechanism_regex_list=[("((^|\s)introduce.*$)",1)]
mechanism_regex_list+=[("((^|\s)propos.*$)",1)]  # propose or proposing
mechanism_regex_list+=[("((^|\s)develop.*$)",1)]
mechanism_regex_list+=[("((^|\s)approach.*$)",1)]
mechanism_regex_list+=[("((^|\s)applied.*$)",1)]
mechanism_regex_list+=[("((^|\s)apply.*$)",1)]
mechanism_regex_list+=[("((^|\s)using.*$)",1)]
mechanism_regex_list+=[("((^|\s)present.*$)",1)]
mechanism_regex_list+=[("((^|\s)contribute.*$)",1)]
mechanism_regex_list+=[("((^|\s)build.*$)",1)]
mechanism_regex_list+=[("((^|\s)built.*$)",1)]

# Part 1.2: new 28 LFs added 090518, should it be a "we+verb" thing
mechanism_regex_list+=[("((^|\s)design.*$)",1)]
mechanism_regex_list+=[("we (also )*give",1)]
mechanism_regex_list+=[("we (also )*formalize",1)]
mechanism_regex_list+=[("we (also )*establish",1)]
mechanism_regex_list+=[("we (also )*reason",1)]
mechanism_regex_list+=[("we (also )*show",1)]
mechanism_regex_list+=[("we (also )*identify",1)]
mechanism_regex_list+=[("we (also )*characterize",1)]
mechanism_regex_list+=[("we (also )*proceed to",1)]
mechanism_regex_list+=[("our algorithm",1)]
mechanism_regex_list+=[("the method",1)]
mechanism_regex_list+=[("the algorithm",1)]
mechanism_regex_list+=[("in our",1)]
mechanism_regex_list+=[("^our",1)]
mechanism_regex_list+=[("we (also )*provide",1)]
mechanism_regex_list+=[("we (also )*derive",1)]
mechanism_regex_list+=[("we (also )*illustrate",1)]
mechanism_regex_list+=[("than existing algorithms",1)]
mechanism_regex_list+=[("we (also )*extend",1)]
mechanism_regex_list+=[("using (([a-z]+[ ]{0,1})*)",1)]
mechanism_regex_list+=[("we (also )*adopt",1)]
mechanism_regex_list+=[("we (also )*argue",1)]
mechanism_regex_list+=[("we (also )*generalize",1)]
mechanism_regex_list+=[("novelty is",1)]
mechanism_regex_list+=[("a[n]{0,1} (([a-z]+[ ]{0,1})*)algorithm",1)]
mechanism_regex_list+=[("a[n]{0,1} (([a-z]+[ ]{0,1})*)mechanism",1)]
mechanism_regex_list+=[("we (also )*demonstrate",1)]


mechanism_LFs=[create_LFs(pair,"mechanism") for pair in mechanism_regex_list]


## Below we declare a list of reverse LFs, -1 if match 
# neg_for_mechanism_LFs=[create_LFs((pair[0],-1*pair[1]),"neg_"+segment_name) for (regex_list,segment_name) in [(background_regex_list,"background"),(purpose_regex_list,"purpose"),(method_regex_list,"method"),(finding_regex_list,"finding")] for pair in regex_list ]




## Deprecated as of 090518

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


