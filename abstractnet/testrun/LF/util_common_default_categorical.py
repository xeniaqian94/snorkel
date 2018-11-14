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

def create_words_LFs_by_window(pair,lf_prefix,including_itself=True):
    
    # pair = (pattern, window_size, label)
    pattern, window_size, label = pair
    
    def func(c):
        window_tags=" ".join(get_surrounding_words(c,window_size,including_itself=including_itself)).lower()
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

# purpose_pos_tag_list=[("NN IN DT",PURPOSE_LABEL)] # cue: task for the
# purpose_pos_tag_list+=[("NNS IN DT",PURPOSE_LABEL)] # cue: tasks for the 
# purpose_pos_tag_list+=[("DT NN IN",PURPOSE_LABEL)] # cue: the problem of 
# # purpose_pos_tag_list+=[("IN VBG",PURPOSE_LABEL)] # cue: for improving, but false positive as by applying... 
# purpose_pos_tag_list+=[("DT VBZ",PURPOSE_LABEL)] # cue: This enables

# purpose_LFs=[create_POS_LFs_by_window((pair[0],window_size,pair[1]),"purpose") for pair in purpose_pos_tag_list for window_size in [3,5,7,9]]

# # a "for" is before this word and this word's dep_ is larger than "for"'s position
 

# def purpose_for_doing(c):

#     text_before_c=get_surrounding_words(c,-2,including_itself=True)
    
#     connection_word="for"

#     if connection_word not in text_before_c:
#         return 0

#     for_psn=text_before_c.index(connection_word)+1

#     dep_parents_whole_sent=get_surrounding_dep_parents(c,0,including_itself=True)

#     return PURPOSE_LABEL if all([dep_parent>=for_psn for dep_parent in dep_parents_whole_sent[for_psn:-1]]) else 0

# # anything after to has dep_parent no smaller than to.head.i
# def purpose_to_verb(c):

#     text_before_c=get_surrounding_words(c,-2,including_itself=True)

#     connection_word="to"
#     if connection_word not in text_before_c:
#         return 0

#     to_psn=text_before_c.index(connection_word)
#     dep_parents_whole_sent=get_surrounding_dep_parents(c,0,including_itself=True)
#     verb_psn=dep_parents_whole_sent[to_psn]-1

#     return PURPOSE_LABEL if all([dep_parent>=verb_psn+1 or idx==(verb_psn-to_psn) for idx, dep_parent in enumerate(dep_parents_whole_sent[to_psn:-1])]) else 0

# purpose_LFs+=[purpose_for_doing,purpose_to_verb]


# mechanism_pos_tag_list=[("PRP VBP",MECHANISM_LABEL)] # cue: we propose/present/...
# mechanism_pos_tag_list+=[("PRP RB VBP",MECHANISM_LABEL)] # cue: we further/also propose/present/...
# mechanism_pos_tag_list+=[("DT VBN NN",MECHANISM_LABEL)] # cue: the proposed method/methods
# mechanism_pos_tag_list+=[("VBZ VBN",MECHANISM_LABEL)] # cue: is proposed
# mechanism_pos_tag_list+=[("VBD VBN",MECHANISM_LABEL)] # cue: was proposed
# mechanism_pos_tag_list+=[("VBP VBN",MECHANISM_LABEL)] # cue: are proposed
# mechanism_pos_tag_list+=[("DT NN VBZ",MECHANISM_LABEL)] # cue: this/the paper proposes/presents/...
# mechanism_pos_tag_list+=[("DT NN VBN",MECHANISM_LABEL)] # cue: the/this paper proposed/presented/...

# mechanism_LFs=[create_POS_LFs_by_window((pair[0],window_size,pair[1]),"mechanism") for pair in mechanism_pos_tag_list for window_size in [3,5,7,9]]

# # We show that the global minimum of this criterion can be reached by first solving a linear system then calculating the roots of some polynomial of order K .
# def mechanism_by_adv_doing(c):

#     candidate_idx_in_sent=c.get_contexts()[0].get_word_start()
#     # print("candidate_idx_in_sent",candidate_idx_in_sent)
#     text_whole_sent=get_surrounding_words(c,0,including_itself=True)
#     connection_word="by"
#     if connection_word not in text_whole_sent:
#         return 0
#     connection_psn=text_whole_sent.index(connection_word)+1
#     # print("connection_psn",connection_psn)
#     if connection_psn-1>candidate_idx_in_sent:
#         return 0
#     dep_parents_whole_sent=get_surrounding_dep_parents(c,0,including_itself=True)
#     modifier_index=dep_parents_whole_sent.index(connection_psn) if connection_psn in dep_parents_whole_sent else -1
#     # print("modifier_index",modifier_index)
#     if modifier_index==-1:
#         return 0
#     # print("text_whole_sent[modifier_index][-3:]",text_whole_sent.split(" ")[modifier_index][-3:])
#     if text_whole_sent[modifier_index][-3:]=="ing":
#         return MECHANISM_LABEL
#     return 0   

# # any mechanism that has NN TO VB pattern, anything before TO VB will be mechanism 
# mechanism_LFs+=[create_POS_LFs_by_window((pair[0],-1,pair[1]),"mechanism",including_itself=False) for pair in [("TO VB",MECHANISM_LABEL)] ]
# mechanism_LFs+=[create_POS_LFs_by_window((pair[0],-1,pair[1]),"mechanism",including_itself=False) for pair in [("IN VBG",MECHANISM_LABEL)] ]
# mechanism_LFs+=[mechanism_by_adv_doing]



# # below are *run 2* !

# purpose_LFs=[]
# mechanism_LFs=[]

# purpose_pos_tag_list=[("NN IN DT",PURPOSE_LABEL)] # cue: task for the
# purpose_pos_tag_list+=[("NNS IN DT",PURPOSE_LABEL)] # cue: tasks for the 
# purpose_pos_tag_list+=[("DT NN IN",PURPOSE_LABEL)] # cue: the problem of 
# # purpose_pos_tag_list+=[("IN VBG",PURPOSE_LABEL)] # cue: for improving, but false positive as by applying... 
# # purpose_pos_tag_list+=[("DT VBZ",PURPOSE_LABEL)] # cue: This enables

# # purpose_LFs=[create_POS_LFs_by_window((pair[0],window_size,pair[1]),"purpose") for pair in purpose_pos_tag_list for window_size in [3,-2]]

# # a "for" is before this word and this word's dep_ is larger than "for"'s position
# def purpose_for_doing(c):

#     text_before_c=get_surrounding_words(c,-2,including_itself=True)
    
#     connection_word="for"

#     if connection_word not in text_before_c:
#         return 0

#     for_psn=text_before_c.index(connection_word)+1

#     dep_parents_whole_sent=get_surrounding_dep_parents(c,0,including_itself=True)

#     return PURPOSE_LABEL if all([dep_parent>=for_psn for dep_parent in dep_parents_whole_sent[for_psn:-1]]) else 0

# # anything after to has dep_parent no smaller than to.head.i
# def purpose_to_verb(c):

#     text_before_c=get_surrounding_words(c,-2,including_itself=True)

#     connection_word="to"
#     if connection_word not in text_before_c:
#         return 0

#     to_psn=text_before_c.index(connection_word)
#     dep_parents_whole_sent=get_surrounding_dep_parents(c,0,including_itself=True)
#     verb_psn=dep_parents_whole_sent[to_psn]-1

#     return PURPOSE_LABEL if all([dep_parent>=verb_psn+1 or idx==(verb_psn-to_psn) for idx, dep_parent in enumerate(dep_parents_whole_sent[to_psn:-1])]) else 0

# purpose_LFs+=[create_POS_LFs_by_window((pair[0],-2,pair[1]),"purpose") for pair in [("TO VB ",PURPOSE_LABEL)] ]

# purpose_word_tag_list=[("that can",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("for the",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("for",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("goal",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("problem",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("challenging",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("fundamental",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("issue",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("task",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("investigate",PURPOSE_LABEL)]
# purpose_LFs+=[create_words_LFs_by_window((pair[0],window_size,pair[1]),"purpose") for pair in purpose_word_tag_list for window_size in [3,-2]]

# purpose_word_tag_list2=[("bottleneck",PURPOSE_LABEL)]
# purpose_word_tag_list2+=[("problem",PURPOSE_LABEL)]
# purpose_word_tag_list2+=[("challenging",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("fundamental",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("issue",PURPOSE_LABEL)]
# purpose_word_tag_list2+=[("task",PURPOSE_LABEL)]
# purpose_LFs+=[create_words_LFs_by_window((pair[0],window_size,pair[1]),"purpose") for pair in purpose_word_tag_list2 for window_size in [3,-1]]
# purpose_LFs+=[purpose_for_doing,purpose_to_verb]




# mechanism_pos_tag_list=[("PRP VBP",MECHANISM_LABEL)] # cue: we propose/present/...
# mechanism_pos_tag_list+=[("PRP RB VBP",MECHANISM_LABEL)] # cue: we further/also propose/present/...
# # mechanism_pos_tag_list+=[("DT VBN NN",MECHANISM_LABEL)] # cue: the proposed method/methods
# # mechanism_pos_tag_list+=[("DT NN VBZ",MECHANISM_LABEL)] # cue: this/the paper proposes/presents/...
# # mechanism_pos_tag_list+=[("DT NN VBN",MECHANISM_LABEL)] # cue: the/this paper proposed/presented/...
# mechanism_LFs=[create_POS_LFs_by_window((pair[0],window_size,pair[1]),"mechanism") for pair in mechanism_pos_tag_list for window_size in [3,-2]]

# mechanism_word_tag_list=[("we propose", MECHANISM_LABEL)]
# mechanism_word_tag_list+=[("we develop", MECHANISM_LABEL)]
# mechanism_word_tag_list+=[("we provide", MECHANISM_LABEL)]
# mechanism_word_tag_list+=[("we have developed", MECHANISM_LABEL)]
# mechanism_word_tag_list+=[("we also propose", MECHANISM_LABEL)]
# mechanism_word_tag_list+=[("presents ", MECHANISM_LABEL)]
# mechanism_word_tag_list+=[("present ", MECHANISM_LABEL)]
# mechanism_word_tag_list+=[("we use ", MECHANISM_LABEL)]
# mechanism_word_tag_list+=[("uses ", MECHANISM_LABEL)]
# mechanism_word_tag_list+=[("using a ", MECHANISM_LABEL)]
# mechanism_word_tag_list+=[("by using", MECHANISM_LABEL)]
# mechanism_word_tag_list+=[("by ", MECHANISM_LABEL)]
# mechanism_word_tag_list+=[("method", MECHANISM_LABEL)]
# mechanism_word_tag_list+=[("approach", MECHANISM_LABEL)]
# mechanism_word_tag_list+=[("algorithm", MECHANISM_LABEL)]
# mechanism_word_tag_list+=[("we also developed", MECHANISM_LABEL)]
# mechanism_LFs+=[create_words_LFs_by_window((pair[0],window_size,pair[1]),"mechanism") for pair in mechanism_word_tag_list for window_size in [3,-2]]

# # mechanism_word_tag_list2=[("is proposed", MECHANISM_LABEL)]
# # mechanism_word_tag_list+=[("are proposed", MECHANISM_LABEL)]
# # mechanism_word_tag_list+=[("was proposed", MECHANISM_LABEL)]
# # mechanism_LFs+=[create_words_LFs_by_window((pair[0],window_size,pair[1]),"mechanism") for pair in mechanism_word_tag_list for window_size in [3,-1]]

# # should we ignore this??
# mechanism_pos_tag_list2=[("VBZ VBN",MECHANISM_LABEL)] # cue: is proposed
# mechanism_pos_tag_list2+=[("VBD VBN",MECHANISM_LABEL)] # cue: was proposed
# mechanism_pos_tag_list2+=[("VBP VBN",MECHANISM_LABEL)] # cue: are proposed
# # mechanism_LFs+=[create_POS_LFs_by_window((pair[0],window_size,pair[1]),"mechanism") for pair in mechanism_pos_tag_list2 for window_size in [3,-1]]


# # We show that the global minimum of this criterion can be reached by first solving a linear system then calculating the roots of some polynomial of order K .
# def mechanism_by_adv_doing(c):

#     candidate_idx_in_sent=c.get_contexts()[0].get_word_start()
#     # print("candidate_idx_in_sent",candidate_idx_in_sent)
#     text_whole_sent=get_surrounding_words(c,0,including_itself=True)
#     connection_word="by"
#     if connection_word not in text_whole_sent:
#         return 0
#     connection_psn=text_whole_sent.index(connection_word)+1
#     # print("connection_psn",connection_psn)
#     if connection_psn-1>candidate_idx_in_sent:
#         return 0
#     dep_parents_whole_sent=get_surrounding_dep_parents(c,0,including_itself=True)
#     modifier_index=dep_parents_whole_sent.index(connection_psn) if connection_psn in dep_parents_whole_sent else -1
#     # print("modifier_index",modifier_index)
#     if modifier_index==-1:
#         return 0
#     # print("text_whole_sent[modifier_index][-3:]",text_whole_sent.split(" ")[modifier_index][-3:])
#     if text_whole_sent[modifier_index][-3:]=="ing":
#         return MECHANISM_LABEL
#     return 0   

# # any mechanism that has NN TO VB pattern, anything before TO VB will be mechanism 
# # mechanism_LFs+=[create_POS_LFs_by_window((pair[0],-1,pair[1]),"mechanism",including_itself=False) for pair in [("TO VB",MECHANISM_LABEL)] ]
# # mechanism_LFs+=[create_POS_LFs_by_window((pair[0],-1,pair[1]),"mechanism",including_itself=False) for pair in [("IN VBG",MECHANISM_LABEL)] ]
# mechanism_LFs+=[mechanism_by_adv_doing]

# null_LFs=[]
# null_word_tag_list=[]
# null_word_tag_list+=[("test", NULL_LABEL)]
# null_word_tag_list+=[("dataset", NULL_LABEL)]
# null_word_tag_list+=[("experiment", NULL_LABEL)]
# null_word_tag_list+=[("results", NULL_LABEL)]
# null_word_tag_list+=[("show", NULL_LABEL)]
# null_word_tag_list+=[("indicate that", NULL_LABEL)]
# null_word_tag_list+=[("indicates that", NULL_LABEL)]
# null_LFs+=[create_words_LFs_by_window((pair[0],window_size,pair[1]),"null") for pair in null_word_tag_list for window_size in [3,-2]]


# # below are *run 3*  first run for week 8 !

# purpose_LFs=[]
# mechanism_LFs=[]

# purpose_pos_tag_list=[("NN IN DT",PURPOSE_LABEL)] # cue: task for the
# purpose_pos_tag_list+=[("NNS IN DT",PURPOSE_LABEL)] # cue: tasks for the 

# purpose_LFs=[create_POS_LFs_by_window((pair[0],window_size,pair[1]),"purpose") for pair in purpose_pos_tag_list for window_size in [3,-2]]

# # a "for" is before this word and this word's dep_ is larger than "for"'s position
# def purpose_for_doing(c):

#     text_before_c=get_surrounding_words(c,-2,including_itself=True)
    
#     connection_word="for"

#     if connection_word not in text_before_c:
#         return 0

#     for_psn=text_before_c.index(connection_word)+1

#     dep_parents_whole_sent=get_surrounding_dep_parents(c,0,including_itself=True)

#     return PURPOSE_LABEL if all([dep_parent>=for_psn for dep_parent in dep_parents_whole_sent[for_psn:-1]]) else 0

# # anything after to has dep_parent no smaller than to.head.i
# def purpose_to_verb(c):

#     c_idx=c.unigram_cue.get_word_start()

#     text_whole_sent=get_surrounding_words(c,0,including_itself=True)

#     connection_word="to"
#     if (connection_word not in text_whole_sent[:c_idx+1]) or connection_word+" be" in " ".join(text_whole_sent):
#         return 0

#     to_psn=text_whole_sent.index(connection_word)
#     dep_parents_whole_sent=get_surrounding_dep_parents(c,0,including_itself=True)
#     dep_labels_whole_sent=get_surrounding_tags(c,0,including_itself=True).split(" ")

#     if "VB" in dep_labels_whole_sent[to_psn-1]:
#         return 0

#     verb_psn=dep_parents_whole_sent[to_psn]-1
#     if dep_labels_whole_sent[verb_psn]=="NN" or dep_labels_whole_sent[verb_psn]=="NNS":
#         return 0

#     return PURPOSE_LABEL if all([dep_parent>=verb_psn+1 or idx==(verb_psn-to_psn) for idx, dep_parent in enumerate(dep_parents_whole_sent[to_psn:-1])]) else 0

# purpose_LFs+=[create_POS_LFs_by_window((pair[0],-2,pair[1]),"purpose") for pair in [("TO VB ",PURPOSE_LABEL)] ]

# purpose_word_tag_list=[("that can",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("for the",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("for",PURPOSE_LABEL)]


# purpose_word_tag_list+=[("goal",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("problem",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("the problem of",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("the task of",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("challenging",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("challenge",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("fundamental",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("issue",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("allow ",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("allows ",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("useful to",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("task",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("investigate",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("we study",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("although",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("however",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("yet ",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("but ",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("existing ",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("gaps ",PURPOSE_LABEL)]
# purpose_LFs+=[create_words_LFs_by_window((pair[0],window_size,pair[1]),"purpose") for pair in purpose_word_tag_list for window_size in [3,-2]]

# purpose_word_tag_list2=[("bottleneck",PURPOSE_LABEL)]
# purpose_word_tag_list2+=[("problem",PURPOSE_LABEL)]
# purpose_word_tag_list2+=[("challenging",PURPOSE_LABEL)]
# purpose_word_tag_list2+=[("fundamental",PURPOSE_LABEL)]
# purpose_word_tag_list2+=[("issue",PURPOSE_LABEL)]
# purpose_word_tag_list2+=[("task",PURPOSE_LABEL)]
# purpose_word_tag_list2+=[("challenge",PURPOSE_LABEL)]
# purpose_LFs+=[create_words_LFs_by_window((pair[0],window_size,pair[1]),"purpose") for pair in purpose_word_tag_list2 for window_size in [3,-1]]
# purpose_LFs+=[purpose_for_doing,purpose_to_verb]




# mechanism_pos_tag_list=[("PRP VBP",MECHANISM_LABEL)] # cue: we propose/present/...
# mechanism_pos_tag_list+=[("PRP RB VBP",MECHANISM_LABEL)] # cue: we further/also propose/present/...
# # mechanism_pos_tag_list+=[("DT VBN NN",MECHANISM_LABEL)] # cue: the proposed method/methods
# # mechanism_pos_tag_list+=[("DT NN VBZ",MECHANISM_LABEL)] # cue: this/the paper proposes/presents/...
# # mechanism_pos_tag_list+=[("DT NN VBN",MECHANISM_LABEL)] # cue: the/this paper proposed/presented/...
# mechanism_LFs=[create_POS_LFs_by_window((pair[0],window_size,pair[1]),"mechanism") for pair in mechanism_pos_tag_list for window_size in [3,-2]]

# mechanism_word_tag_list=[("we propose", MECHANISM_LABEL)]
# mechanism_word_tag_list+=[("we develop", MECHANISM_LABEL)]
# mechanism_word_tag_list+=[("we provide", MECHANISM_LABEL)]
# mechanism_word_tag_list+=[("we have developed", MECHANISM_LABEL)]
# mechanism_word_tag_list+=[("we also propose", MECHANISM_LABEL)]
# mechanism_word_tag_list+=[("presents ", MECHANISM_LABEL)]
# mechanism_word_tag_list+=[("present ", MECHANISM_LABEL)]
# mechanism_word_tag_list+=[("we use ", MECHANISM_LABEL)]
# mechanism_word_tag_list+=[("uses ", MECHANISM_LABEL)]
# mechanism_word_tag_list+=[("using a ", MECHANISM_LABEL)]
# mechanism_word_tag_list+=[("using the ", MECHANISM_LABEL)]
# mechanism_word_tag_list+=[("by using", MECHANISM_LABEL)]
# mechanism_word_tag_list+=[("by ", MECHANISM_LABEL)] 
# mechanism_word_tag_list+=[("method ", MECHANISM_LABEL)] # propsed a method, vs. most existing methods
# mechanism_word_tag_list+=[("approach ", MECHANISM_LABEL)]
# mechanism_word_tag_list+=[("we also developed", MECHANISM_LABEL)]
# mechanism_word_tag_list+=[("via ", MECHANISM_LABEL)]
# # mechanism_word_tag_list+=[("contribution", MECHANISM_LABEL)]
# mechanism_LFs+=[create_words_LFs_by_window((pair[0],window_size,pair[1]),"mechanism") for pair in mechanism_word_tag_list for window_size in [3,-2]]

# # mechanism_word_tag_list2=[("is proposed", MECHANISM_LABEL)]
# # mechanism_word_tag_list+=[("are proposed", MECHANISM_LABEL)]
# # mechanism_word_tag_list+=[("was proposed", MECHANISM_LABEL)]
# # mechanism_LFs+=[create_words_LFs_by_window((pair[0],window_size,pair[1]),"mechanism") for pair in mechanism_word_tag_list for window_size in [3,-1]]

# # should we ignore this??
# mechanism_pos_tag_list2=[("VBZ VBN",MECHANISM_LABEL)] # cue: is proposed
# mechanism_pos_tag_list2+=[("VBD VBN",MECHANISM_LABEL)] # cue: was proposed
# mechanism_pos_tag_list2+=[("VBP VBN",MECHANISM_LABEL)] # cue: are proposed
# # mechanism_LFs+=[create_POS_LFs_by_window((pair[0],window_size,pair[1]),"mechanism") for pair in mechanism_pos_tag_list2 for window_size in [3,-1]]


# # We show that the global minimum of this criterion can be reached by first solving a linear system then calculating the roots of some polynomial of order K .
# def mechanism_by_adv_doing(c):

#     candidate_idx_in_sent=c.get_contexts()[0].get_word_start()
#     # print("candidate_idx_in_sent",candidate_idx_in_sent)
#     text_whole_sent=get_surrounding_words(c,0,including_itself=True)
#     connection_word="by"
#     if connection_word not in text_whole_sent:
#         return 0
#     connection_psn=text_whole_sent.index(connection_word)+1
#     # print("connection_psn",connection_psn)
#     if connection_psn-1>candidate_idx_in_sent:
#         return 0
#     dep_parents_whole_sent=get_surrounding_dep_parents(c,0,including_itself=True)
#     modifier_index=dep_parents_whole_sent.index(connection_psn) if connection_psn in dep_parents_whole_sent else -1
#     # print("modifier_index",modifier_index)
#     if modifier_index==-1:
#         return 0
#     # print("text_whole_sent[modifier_index][-3:]",text_whole_sent.split(" ")[modifier_index][-3:])
#     if text_whole_sent[modifier_index][-3:]=="ing":
#         return MECHANISM_LABEL
#     return 0   

# def mechanism_an_algorithm(c):

#     text_before_c=get_surrounding_words(c,-2,including_itself=True)

#     connection_word="algorithm"
#     if connection_word not in text_before_c:
#         return 0

#     c_idx=c.unigram_cue.get_word_start()

#     window_array=text_before_c[c_idx-4:c_idx]

#     if "an" in window_array or "a" in window_array:
#         return MECHANISM_LABEL
#     return 0

# # any mechanism that has NN TO VB pattern, anything before TO VB will be mechanism 
# # mechanism_LFs+=[create_POS_LFs_by_window((pair[0],-1,pair[1]),"mechanism",including_itself=False) for pair in [("TO VB",MECHANISM_LABEL)] ]
# # mechanism_LFs+=[create_POS_LFs_by_window((pair[0],-1,pair[1]),"mechanism",including_itself=False) for pair in [("IN VBG",MECHANISM_LABEL)] ]
# mechanism_LFs+=[mechanism_by_adv_doing,mechanism_an_algorithm]

# null_LFs=[]
# null_word_tag_list=[]
# null_word_tag_list+=[("test", NULL_LABEL)]
# null_word_tag_list+=[("dataset", NULL_LABEL)]
# null_word_tag_list+=[("experiment", NULL_LABEL)]
# null_word_tag_list+=[("results", NULL_LABEL)]
# null_word_tag_list+=[("show", NULL_LABEL)]
# null_word_tag_list+=[("observe", NULL_LABEL)]
# null_word_tag_list+=[("we prove", NULL_LABEL)]
# null_word_tag_list+=[("evaluates ", NULL_LABEL)]
# null_word_tag_list+=[("evaluated ", NULL_LABEL)]
# null_word_tag_list+=[("evaluate ", NULL_LABEL)]
# null_word_tag_list+=[("demonstrate", NULL_LABEL)]
# null_word_tag_list+=[("indicate that", NULL_LABEL)]
# null_word_tag_list+=[("indicates that", NULL_LABEL)]
# null_word_tag_list+=[("are performed", NULL_LABEL)]
# null_word_tag_list+=[("were performed", NULL_LABEL)]
# null_word_tag_list+=[("have been", NULL_LABEL)] # background
# null_word_tag_list+=[("has been", NULL_LABEL)] # background
# null_word_tag_list+=[("popular ", NULL_LABEL)] # background
# null_word_tag_list+=[("popularity ", NULL_LABEL)] # background
# null_word_tag_list+=[("increasing", NULL_LABEL)] # background
# null_word_tag_list+=[("general", NULL_LABEL)] # background
# null_word_tag_list+=[("compared to", NULL_LABEL)] # background
# null_word_tag_list+=[("compare ", NULL_LABEL)] # background
# null_LFs+=[create_words_LFs_by_window((pair[0],window_size,pair[1]),"null") for pair in null_word_tag_list for window_size in [3,-2]]



# null_word_tag_list2=[("settings", NULL_LABEL)]
# null_word_tag_list2+=[("general", NULL_LABEL)] # background
# null_LFs+=[create_words_LFs_by_window((pair[0],window_size,pair[1]),"null") for pair in null_word_tag_list2 for window_size in [3,-1]]


## below are *run 4* 

# below are *run 3*  first run for week 8 !

purpose_LFs=[]
mechanism_LFs=[]

purpose_pos_tag_list=[]
# purpose_pos_tag_list=[("NN IN DT",PURPOSE_LABEL)] # cue: task for the
# purpose_pos_tag_list+=[("NNS IN DT",PURPOSE_LABEL)] # cue: tasks for the 

purpose_LFs=[create_POS_LFs_by_window((pair[0],window_size,pair[1]),"purpose") for pair in purpose_pos_tag_list for window_size in [3,-2]]

# a "for" is before this word and this word's dep_ is larger than "for"'s position
def purpose_for_doing(c):

    text_before_c=get_surrounding_words(c,-2,including_itself=True)
    
    connection_word="for"

    if connection_word not in text_before_c:
        return 0

    for_psn=text_before_c.index(connection_word)+1

    dep_parents_whole_sent=get_surrounding_dep_parents(c,0,including_itself=True)

    return PURPOSE_LABEL if all([dep_parent>=for_psn for dep_parent in dep_parents_whole_sent[for_psn:-1]]) else 0

# anything after to has dep_parent no smaller than to.head.i
def purpose_to_verb(c):

    c_idx=c.unigram_cue.get_word_start()

    text_whole_sent=get_surrounding_words(c,0,including_itself=True)

    connection_word="to"
    if (connection_word not in text_whole_sent[:c_idx+1]) or connection_word+" be" in " ".join(text_whole_sent):
        return 0

    to_psn=text_whole_sent.index(connection_word)
    dep_parents_whole_sent=get_surrounding_dep_parents(c,0,including_itself=True)
    dep_labels_whole_sent=get_surrounding_tags(c,0,including_itself=True).split(" ")

    if "VB" in dep_labels_whole_sent[to_psn-1]:
        return 0

    verb_psn=dep_parents_whole_sent[to_psn]-1
    if dep_labels_whole_sent[verb_psn]=="NN" or dep_labels_whole_sent[verb_psn]=="NNS":
        return 0

    return PURPOSE_LABEL if all([dep_parent>=verb_psn+1 or idx==(verb_psn-to_psn) for idx, dep_parent in enumerate(dep_parents_whole_sent[to_psn:-1])]) else 0

purpose_LFs+=[create_POS_LFs_by_window((pair[0],-2,pair[1]),"purpose") for pair in [("TO VB ",PURPOSE_LABEL)] ]
purpose_word_tag_list=[]
# purpose_word_tag_list=[("that can",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("for the",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("for",PURPOSE_LABEL)]


purpose_word_tag_list+=[("goal",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("problem",PURPOSE_LABEL)]
purpose_word_tag_list+=[("the problem of",PURPOSE_LABEL)]
purpose_word_tag_list+=[("the task of",PURPOSE_LABEL)]
purpose_word_tag_list+=[("challenging",PURPOSE_LABEL)]
purpose_word_tag_list+=[("challenge",PURPOSE_LABEL)]
purpose_word_tag_list+=[("fundamental",PURPOSE_LABEL)]
purpose_word_tag_list+=[("issue",PURPOSE_LABEL)]
purpose_word_tag_list+=[("allow ",PURPOSE_LABEL)]
purpose_word_tag_list+=[("allows ",PURPOSE_LABEL)]
purpose_word_tag_list+=[("useful to",PURPOSE_LABEL)]
purpose_word_tag_list+=[("task",PURPOSE_LABEL)]
purpose_word_tag_list+=[("investigate",PURPOSE_LABEL)]
purpose_word_tag_list+=[("we study",PURPOSE_LABEL)]
purpose_word_tag_list+=[("although",PURPOSE_LABEL)]
purpose_word_tag_list+=[("however",PURPOSE_LABEL)]
purpose_word_tag_list+=[("yet ",PURPOSE_LABEL)]
purpose_word_tag_list+=[("but ",PURPOSE_LABEL)]
purpose_word_tag_list+=[("existing ",PURPOSE_LABEL)]
purpose_word_tag_list+=[("deals with ",PURPOSE_LABEL)]
purpose_word_tag_list+=[("we explore", PURPOSE_LABEL)]
purpose_word_tag_list+=[("investigate", PURPOSE_LABEL)]
purpose_word_tag_list+=[("examine",PURPOSE_LABEL)]
purpose_LFs+=[create_words_LFs_by_window((pair[0],window_size,pair[1]),"purpose") for pair in purpose_word_tag_list for window_size in [3,-2]]

purpose_word_tag_list2=[("bottleneck",PURPOSE_LABEL)]
purpose_word_tag_list2+=[("problem",PURPOSE_LABEL)]
purpose_word_tag_list2+=[("challenging",PURPOSE_LABEL)]
purpose_word_tag_list2+=[("fundamental",PURPOSE_LABEL)]
purpose_word_tag_list2+=[("issue",PURPOSE_LABEL)]
purpose_word_tag_list2+=[("task",PURPOSE_LABEL)]
purpose_word_tag_list2+=[("challenge",PURPOSE_LABEL)]
purpose_LFs+=[create_words_LFs_by_window((pair[0],window_size,pair[1]),"purpose") for pair in purpose_word_tag_list2 for window_size in [3,-1]]
purpose_LFs+=[purpose_for_doing,purpose_to_verb]



mechanism_pos_tag_list=[]
# mechanism_pos_tag_list=[("PRP VBP",MECHANISM_LABEL)] # cue: we propose/present/...
# mechanism_pos_tag_list+=[("PRP RB VBP",MECHANISM_LABEL)] # cue: we further/also propose/present/...
# mechanism_pos_tag_list+=[("DT VBN NN",MECHANISM_LABEL)] # cue: the proposed method/methods
# mechanism_pos_tag_list+=[("DT NN VBZ",MECHANISM_LABEL)] # cue: this/the paper proposes/presents/...
# mechanism_pos_tag_list+=[("DT NN VBN",MECHANISM_LABEL)] # cue: the/this paper proposed/presented/...
mechanism_LFs=[create_POS_LFs_by_window((pair[0],window_size,pair[1]),"mechanism") for pair in mechanism_pos_tag_list for window_size in [3,-2]]

mechanism_word_tag_list=[("propose", MECHANISM_LABEL)]
mechanism_word_tag_list+=[("develop ", MECHANISM_LABEL)]
mechanism_word_tag_list+=[("develops ", MECHANISM_LABEL)]
mechanism_word_tag_list+=[("developed ", MECHANISM_LABEL)]
mechanism_word_tag_list+=[("provide", MECHANISM_LABEL)]
# mechanism_word_tag_list+=[("we have developed", MECHANISM_LABEL)]
# mechanism_word_tag_list+=[("we also propose", MECHANISM_LABEL)]
mechanism_word_tag_list+=[("presents ", MECHANISM_LABEL)]
mechanism_word_tag_list+=[("present ", MECHANISM_LABEL)]
mechanism_word_tag_list+=[("we use ", MECHANISM_LABEL)]
mechanism_word_tag_list+=[("uses ", MECHANISM_LABEL)]
mechanism_word_tag_list+=[("using a ", MECHANISM_LABEL)]
mechanism_word_tag_list+=[("using the ", MECHANISM_LABEL)]
mechanism_word_tag_list+=[("by using", MECHANISM_LABEL)]
mechanism_word_tag_list+=[("by ", MECHANISM_LABEL)] 
mechanism_word_tag_list+=[("method ", MECHANISM_LABEL)] # propsed a method, vs. most existing methods
mechanism_word_tag_list+=[("approach ", MECHANISM_LABEL)]
mechanism_word_tag_list+=[("via ", MECHANISM_LABEL)]
mechanism_word_tag_list+=[("to solve ", MECHANISM_LABEL)]
# mechanism_word_tag_list+=[("contribution", MECHANISM_LABEL)]
mechanism_LFs+=[create_words_LFs_by_window((pair[0],window_size,pair[1]),"mechanism") for pair in mechanism_word_tag_list for window_size in [3,-2]]

# mechanism_word_tag_list2=[("is proposed", MECHANISM_LABEL)]
# mechanism_word_tag_list+=[("are proposed", MECHANISM_LABEL)]
# mechanism_word_tag_list+=[("was proposed", MECHANISM_LABEL)]
# mechanism_LFs+=[create_words_LFs_by_window((pair[0],window_size,pair[1]),"mechanism") for pair in mechanism_word_tag_list for window_size in [3,-1]]

# should we ignore this??
mechanism_pos_tag_list2=[("VBZ VBN",MECHANISM_LABEL)] # cue: is proposed
mechanism_pos_tag_list2+=[("VBD VBN",MECHANISM_LABEL)] # cue: was proposed
mechanism_pos_tag_list2+=[("VBP VBN",MECHANISM_LABEL)] # cue: are proposed
# mechanism_LFs+=[create_POS_LFs_by_window((pair[0],window_size,pair[1]),"mechanism") for pair in mechanism_pos_tag_list2 for window_size in [3,-1]]


# We show that the global minimum of this criterion can be reached by first solving a linear system then calculating the roots of some polynomial of order K .
def mechanism_by_adv_doing(c):

    candidate_idx_in_sent=c.get_contexts()[0].get_word_start()
    # print("candidate_idx_in_sent",candidate_idx_in_sent)
    text_whole_sent=get_surrounding_words(c,0,including_itself=True)
    connection_word="by"
    if connection_word not in text_whole_sent:
        return 0
    connection_psn=text_whole_sent.index(connection_word)+1
    # print("connection_psn",connection_psn)
    if connection_psn-1>candidate_idx_in_sent:
        return 0
    dep_parents_whole_sent=get_surrounding_dep_parents(c,0,including_itself=True)
    modifier_index=dep_parents_whole_sent.index(connection_psn) if connection_psn in dep_parents_whole_sent else -1
    # print("modifier_index",modifier_index)
    if modifier_index==-1:
        return 0
    # print("text_whole_sent[modifier_index][-3:]",text_whole_sent.split(" ")[modifier_index][-3:])
    if text_whole_sent[modifier_index][-3:]=="ing":
        return MECHANISM_LABEL
    return 0   

def mechanism_an_algorithm(c):

    text_before_c=get_surrounding_words(c,-2,including_itself=True)

    connection_word="algorithm"
    if connection_word not in text_before_c:
        return 0

    c_idx=c.unigram_cue.get_word_start()

    window_array=text_before_c[c_idx-4:c_idx]

    if "an" in window_array or "a" in window_array:
        return MECHANISM_LABEL
    return 0

# any mechanism that has NN TO VB pattern, anything before TO VB will be mechanism 
# mechanism_LFs+=[create_POS_LFs_by_window((pair[0],-1,pair[1]),"mechanism",including_itself=False) for pair in [("TO VB",MECHANISM_LABEL)] ]
# mechanism_LFs+=[create_POS_LFs_by_window((pair[0],-1,pair[1]),"mechanism",including_itself=False) for pair in [("IN VBG",MECHANISM_LABEL)] ]
mechanism_LFs+=[mechanism_by_adv_doing,mechanism_an_algorithm]

null_LFs=[]
null_word_tag_list=[]
null_word_tag_list+=[("test", NULL_LABEL)]
null_word_tag_list+=[("dataset", NULL_LABEL)]
null_word_tag_list+=[("experiment", NULL_LABEL)]
null_word_tag_list+=[("results", NULL_LABEL)]
null_word_tag_list+=[("show", NULL_LABEL)]
null_word_tag_list+=[("observe", NULL_LABEL)]
null_word_tag_list+=[("we prove", NULL_LABEL)]
null_word_tag_list+=[("evaluates ", NULL_LABEL)]
null_word_tag_list+=[("evaluated ", NULL_LABEL)]
null_word_tag_list+=[("evaluate ", NULL_LABEL)]
null_word_tag_list+=[("demonstrate", NULL_LABEL)]
null_word_tag_list+=[("indicate that", NULL_LABEL)]
null_word_tag_list+=[("indicates that", NULL_LABEL)]
null_word_tag_list+=[("are performed", NULL_LABEL)]
null_word_tag_list+=[("were performed", NULL_LABEL)]
null_word_tag_list+=[("have been", NULL_LABEL)] # background
null_word_tag_list+=[("has been", NULL_LABEL)] # background
null_word_tag_list+=[("popular ", NULL_LABEL)] # background
null_word_tag_list+=[("popularity ", NULL_LABEL)] # background
null_word_tag_list+=[("increasing", NULL_LABEL)] # background
null_word_tag_list+=[("general", NULL_LABEL)] # background
null_word_tag_list+=[("compared to", NULL_LABEL)] # background
null_word_tag_list+=[("compare ", NULL_LABEL)] # background
null_LFs+=[create_words_LFs_by_window((pair[0],window_size,pair[1]),"null") for pair in null_word_tag_list for window_size in [3,-2]]

null_word_tag_list2=[("settings", NULL_LABEL)]
null_word_tag_list2+=[("general", NULL_LABEL)] # background
null_LFs+=[create_words_LFs_by_window((pair[0],window_size,pair[1]),"null") for pair in null_word_tag_list2 for window_size in [3,-1]]


# below are embedding-based LFs



