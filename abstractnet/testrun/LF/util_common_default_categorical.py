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
    return "LF_"+lf_prefix+"_"+re.sub('[^0-9a-zA-Z]+', '_', re.sub("-","neg",match_pattern)).strip("_")


def candidate_pos_in_doc(c):
    sent=c.get_parent()
    sents=sent.get_parent().sentences
    return sents.index(sent)*1.0/len(sents)

# TODO get_surrounding_words maybe group segments back to doc level from  Sentence has words in its __dict__ 

def get_surrounding_sequence(segment,window_size,including_itself=True,seq_type="pos_tags"):
    sequence_list=segment.get_parent().__dict__[seq_type]
    unigram_psn=segment.unigram_cue.get_word_start()
    if window_size==-1: # -1 means get all sequences till the end
        return sequence_list[unigram_psn+(0 if including_itself else 1):]
    elif window_size==-2: # -2 means get all preceeding sequences
        return sequence_list[0:min(unigram_psn+(1 if including_itself else 0),len(sequence_list))]
    elif window_size==0: # 0 means get all sequences in this sentence
        return sequence_list
    half_window_size=int((window_size-1)/2)
    return sequence_list[max(0,unigram_psn-half_window_size):min(len(sequence_list),unigram_psn+half_window_size+1)]

def get_surrounding_words(segment,window_size,including_itself=True):
    return get_surrounding_sequence(segment,window_size,including_itself=True,seq_type="words")

def get_surrounding_tags(segment,window_size,including_itself=True):
    return " ".join(get_surrounding_sequence(segment,window_size,including_itself=True,seq_type="pos_tags"))

def get_surrounding_dep_parents(segment,window_size,including_itself=True):
    return get_surrounding_sequence(segment,window_size,including_itself=True,seq_type="dep_parents",)

def create_POS_LFs_by_window(pair,lf_prefix,including_itself=True):
    
    # pair = (pattern, window_size, label)
    pattern, window_size, label = pair
    
    def func(c):
        window_tags=get_surrounding_tags(c,window_size,including_itself=including_itself)
        return label if pattern in window_tags else 0

    func.__name__=create_function_name(lf_prefix,pattern+str(window_size)+"_"+str(including_itself))
    return func

# initialization 
purpose_LFs=[]
mechanism_LFs=[]

# run 0

'''
purpose_pos_tag_list=[("NN IN DT",PURPOSE_LABEL)] # cue: task for the
# purpose_pos_tag_list+=[("NN TO DT",PURPOSE_LABEL)] # cue: solution to the
purpose_pos_tag_list+=[("NNS IN DT",PURPOSE_LABEL)] # cue: tasks for the 
# purpose_pos_tag_list+=[("NNS TO DT",PURPOSE_LABEL)] # cue: solutions for the 
purpose_pos_tag_list+=[("TO VB",PURPOSE_LABEL)] # cue: to solve
purpose_pos_tag_list+=[("DT NN IN",PURPOSE_LABEL)] # cue: the problem of 
purpose_pos_tag_list+=[("IN VBG",PURPOSE_LABEL)] # cue: for improving, but false positive as by applying... 
purpose_pos_tag_list+=[("DT VBZ",PURPOSE_LABEL)] # cue: This enables

purpose_LFs=[create_POS_LFs_by_window((pair[0],window_size,pair[1]),"purpose") for pair in purpose_pos_tag_list for window_size in [3,5,7,9]]

mechanism_pos_tag_list=[("PRP VBP",MECHANISM_LABEL)] # cue: we propose/present/...
mechanism_pos_tag_list+=[("PRP RB VBP",MECHANISM_LABEL)] # cue: we further/also propose/present/...
mechanism_pos_tag_list+=[("DT VBN NN",MECHANISM_LABEL)] # cue: the proposed method/methods
mechanism_pos_tag_list+=[("VBZ VBN",MECHANISM_LABEL)] # cue: is proposed
mechanism_pos_tag_list+=[("VBD VBN",MECHANISM_LABEL)] # cue: was proposed
mechanism_pos_tag_list+=[("VBP VBN",MECHANISM_LABEL)] # cue: are proposed
mechanism_pos_tag_list+=[("DT NN VBZ",MECHANISM_LABEL)] # cue: this/the paper proposes/presents/...
mechanism_pos_tag_list+=[("DT NN VBN",MECHANISM_LABEL)] # cue: the/this paper proposed/presented/...

mechanism_LFs=[create_POS_LFs_by_window((pair[0],window_size,pair[1]),"mechanism") for pair in mechanism_pos_tag_list for window_size in [3,5,7,9]]
'''


# below are *run 1* !

purpose_pos_tag_list=[("NN IN DT",PURPOSE_LABEL)] # cue: task for the
purpose_pos_tag_list+=[("NNS IN DT",PURPOSE_LABEL)] # cue: tasks for the 
purpose_pos_tag_list+=[("DT NN IN",PURPOSE_LABEL)] # cue: the problem of 
purpose_pos_tag_list+=[("IN VBG",PURPOSE_LABEL)] # cue: for improving, but false positive as by applying... 
purpose_pos_tag_list+=[("DT VBZ",PURPOSE_LABEL)] # cue: This enables

purpose_LFs=[create_POS_LFs_by_window((pair[0],window_size,pair[1]),"purpose") for pair in purpose_pos_tag_list for window_size in [3,5,7,9,-2]]

# a "for" is before this word and this word's dep_ is larger than "for"'s position
 

def purpose_for_doing(c):

    text_before_c=get_surrounding_words(c,-2,including_itself=True)
    
    connection_word="for"

    if connection_word not in text_before_c:
        return NULL_LABEL

    for_psn=text_before_c.index(connection_word)+1

    dep_parents_whole_sent=get_surrounding_dep_parents(c,0,including_itself=True)

    return PURPOSE_LABEL if all([dep_parent>=for_psn for dep_parent in dep_parents_whole_sent[for_psn:-1]]) else NULL_LABEL

# anything after to has dep_parent no smaller than to.head.i
def purpose_to_verb(c):

    text_before_c=get_surrounding_words(c,-2,including_itself=True)

    connection_word="to"
    if connection_word not in text_before_c:
        return NULL_LABEL

    to_psn=text_before_c.index(connection_word)
    dep_parents_whole_sent=get_surrounding_dep_parents(c,0,including_itself=True)
    verb_psn=dep_parents_whole_sent[to_psn]-1

    return PURPOSE_LABEL if all([dep_parent>=verb_psn+1 or idx==(verb_psn-to_psn) for idx, dep_parent in enumerate(dep_parents_whole_sent[to_psn:-1])]) else NULL_LABEL

purpose_LFs+=[purpose_for_doing,purpose_to_verb]


mechanism_pos_tag_list=[("PRP VBP",MECHANISM_LABEL)] # cue: we propose/present/...
mechanism_pos_tag_list+=[("PRP RB VBP",MECHANISM_LABEL)] # cue: we further/also propose/present/...
mechanism_pos_tag_list+=[("DT VBN NN",MECHANISM_LABEL)] # cue: the proposed method/methods
mechanism_pos_tag_list+=[("VBZ VBN",MECHANISM_LABEL)] # cue: is proposed
mechanism_pos_tag_list+=[("VBD VBN",MECHANISM_LABEL)] # cue: was proposed
mechanism_pos_tag_list+=[("VBP VBN",MECHANISM_LABEL)] # cue: are proposed
mechanism_pos_tag_list+=[("DT NN VBZ",MECHANISM_LABEL)] # cue: this/the paper proposes/presents/...
mechanism_pos_tag_list+=[("DT NN VBN",MECHANISM_LABEL)] # cue: the/this paper proposed/presented/...

mechanism_LFs=[create_POS_LFs_by_window((pair[0],window_size,pair[1]),"mechanism") for pair in mechanism_pos_tag_list for window_size in [3,5,7,9,-2]]

# We show that the global minimum of this criterion can be reached by first solving a linear system then calculating the roots of some polynomial of order K .
def mechanism_by_adv_doing(c):

    candidate_idx_in_sent=c.get_contexts()[0].get_word_start()
    # print("candidate_idx_in_sent",candidate_idx_in_sent)
    text_whole_sent=get_surrounding_words(c,0,including_itself=True)
    connection_word="by"
    if connection_word not in text_whole_sent:
        return NULL_LABEL
    connection_psn=text_whole_sent.index(connection_word)+1
    # print("connection_psn",connection_psn)
    if connection_psn-1>candidate_idx_in_sent:
        return NULL_LABEL
    dep_parents_whole_sent=get_surrounding_dep_parents(c,0,including_itself=True)
    modifier_index=dep_parents_whole_sent.index(connection_psn) if connection_psn in dep_parents_whole_sent else -1
    # print("modifier_index",modifier_index)
    if modifier_index==-1:
        return NULL_LABEL
    # print("text_whole_sent[modifier_index][-3:]",text_whole_sent.split(" ")[modifier_index][-3:])
    if text_whole_sent[modifier_index][-3:]=="ing":
        return MECHANISM_LABEL
    return NULL_LABEL   

# any mechanism that has NN TO VB pattern, anything before TO VB will be mechanism 
mechanism_LFs+=[create_POS_LFs_by_window((pair[0],-1,pair[1]),"mechanism",including_itself=False) for pair in [("TO VB",MECHANISM_LABEL)] ]
mechanism_LFs+=[create_POS_LFs_by_window((pair[0],-1,pair[1]),"mechanism",including_itself=False) for pair in [("IN VBG",MECHANISM_LABEL)] ]
mechanism_LFs+=[mechanism_by_adv_doing]


