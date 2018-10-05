from snorkel.lf_helpers import *

from .util_common_default_categorical import * #create_LFs,create_POS_LFs,candidate_pos_in_doc,PURPOSE_LABEL,MECHANISM_LABEL,NULL_LABEL

# Part 1: common regex 8 LFs, about contrast 
# common_regex_list are a list of tuples in the format of (regex, label_if_match_1_or_-1)

common_regex_list=[]
# common_regex_list=[("((^|\s)however.*$)",PURPOSE_LABEL)]
# common_regex_list+=[("((^|\s)nevertheless.*$)",PURPOSE_LABEL)]
# common_regex_list+=[("((^|\s)despite.*$)",PURPOSE_LABEL)]
# common_regex_list+=[("((^|\s)spite.*$)",PURPOSE_LABEL)]
# common_regex_list+=[("((^|\s)yet.*$)",PURPOSE_LABEL)]
# common_regex_list+=[("((^|\s)but.*$)",PURPOSE_LABEL)]
# common_regex_list+=[("(^.*but sometimes.*$)",NULL_LABEL)]
# common_regex_list+=[("(^.*but also.*$)",NULL_LABEL)]

common_LFs=[create_LFs(pair,"common") for pair in common_regex_list]


# Part 2: purpose-specific regex
# Part 2.1: existing 15 LFs
purpose_regex_list=[]

# purpose_regex_list=[("(.*more [a-z ]* than.*$)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.*er than.*$)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.*in order to.*$)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.* implication.*$)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.* give.*$)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.* that can .*$)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.* examine.*$)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.* extend.*$)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.* offer.*$)",PURPOSE_LABEL)]

# Part 2.2: new 58 LFs added 090218
# purpose_regex_list+=[("(.*we consider.*)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.*how[ a-z]+can.*)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.*we study.*)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.*we are interested in .*)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.*we seek.*)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.*initiate.*)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.*for[ a-z]+ing.*)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.* do .*)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.* does .*)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.*which can.*)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.*to extract.*)",PURPOSE_LABEL)]
# purpose_regex_list+=[("((^|\s)what .*)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.*one can only.*)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.*in order for.*)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.*a[a-z ]+problem.*)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.*why.*)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.*current.*)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.*today.*)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.*recent .*)",PURPOSE_LABEL)]  # we don't want to have recently?? more like background?
# purpose_regex_list+=[("(.*we ask.*)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.*can we.*)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.*as a[n]* [a-z]*er.*)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.*as a more .*)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.*objective.*)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.*often.*)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.* problem.*)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.*challeng.*)",PURPOSE_LABEL)] # challenging or challenge
# purpose_regex_list+=[("(.*task.*)",PURPOSE_LABEL)] # challenging or challenge
# purpose_regex_list+=[("(.*especially if.*)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.*how [a-z ]* do[es]* .*)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.* no .*)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.* first.*)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.*fail to.*)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.*what is.*)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.*what are.*)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.*is needed.*)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.*necessary.*)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.*too [a-z ]* to.*)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.*prohibitive.*)",PURPOSE_LABEL)]  # negative sentiment towards past progress/approach
# purpose_regex_list+=[("(.* hypothesis.*$)",PURPOSE_LABEL)]

purpose_regex_list+=[("(.*way to.*)",PURPOSE_LABEL)]
purpose_regex_list+=[("(.*to address.*)",PURPOSE_LABEL)]
purpose_regex_list+=[("(.*for the .*)",PURPOSE_LABEL)]
purpose_regex_list+=[("(.*alternative to.*)",PURPOSE_LABEL)]
purpose_regex_list+=[("(.*solutions for.*)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.*an extension to.*)",PURPOSE_LABEL)]
purpose_regex_list+=[("(.*to further.*)",PURPOSE_LABEL)]
purpose_regex_list+=[("(.*to find.*)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.*focus.*)",PURPOSE_LABEL)]
purpose_regex_list+=[("(.*allow.*)",PURPOSE_LABEL)]
purpose_regex_list+=[("(.*explain.*)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.*answer.*)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.*discuss.*)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.*discover.*)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.*solve.*)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.*argue.*)",PURPOSE_LABEL)]
purpose_regex_list+=[("(.*enable.*)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.*to solve.*$)",PURPOSE_LABEL)]
purpose_regex_list+=[("(.*to enable.*$)",PURPOSE_LABEL)]
purpose_regex_list+=[("(.*to aid.*$)",PURPOSE_LABEL)]
purpose_regex_list+=[("(.*to produce.*$)",PURPOSE_LABEL)]
purpose_regex_list+=[("(.*to investigat.*$)",PURPOSE_LABEL)]
purpose_regex_list+=[("(.* goal.*)",PURPOSE_LABEL)]
# purpose_regex_list+=[("(.*the question of how.*)",PURPOSE_LABEL)]

purpose_pos_tag_list=[("NN IN DT",PURPOSE_LABEL)] # cue: task for the
# purpose_pos_tag_list+=[("NN TO DT",PURPOSE_LABEL)] # cue: solution to the
purpose_pos_tag_list+=[("NNS IN DT",PURPOSE_LABEL)] # cue: tasks for the 
# purpose_pos_tag_list+=[("NNS TO DT",PURPOSE_LABEL)] # cue: solutions for the 
purpose_pos_tag_list+=[("TO VB",PURPOSE_LABEL)] # cue: to solve
purpose_pos_tag_list+=[("DT NN IN",PURPOSE_LABEL)] # cue: the problem of 
purpose_pos_tag_list+=[("IN VBG",PURPOSE_LABEL)] # cue: for improving
purpose_pos_tag_list+=[("DT VBZ",PURPOSE_LABEL)] # cue: This enables
purpose_pos_tag_list+=[("DT NN IN",PURPOSE_LABEL)] # cue: The question of

def proper_purpose_pos(c):
	relative_pos=candidate_pos_in_doc(c)
	return PURPOSE_LABEL if (relative_pos<=0.4 or relative_pos>=0.8) else 0

purpose_LFs=[create_LFs(pair,"purpose") for pair in purpose_regex_list]+[create_POS_LFs(pair,"purpose") for pair in purpose_pos_tag_list]#+[proper_purpose_pos]
