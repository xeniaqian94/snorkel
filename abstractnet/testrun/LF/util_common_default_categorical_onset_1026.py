from snorkel.lf_helpers import *
import re

from gensim.models.wrappers import FastText
import os
from tqdm import tqdm
import numpy as np

# from collections import Counter
# word_counter = Counter()
# with open(os.path.expanduser("~/Desktop/snorkel/abstractnet/testrun/data/annotations_label-level_all-to-date-2018-4-25-WithTitle_full_abstract_punc_concatenated.csv")) as f:
#     for i, l in enumerate(tqdm(f)):
#         line=l.split("\t")
#         word_counter.update(line[1].lower().split())

PURPOSE_LABEL="PP"
MECHANISM_LABEL="MN"
NULL_LABEL="NULL"

def get_candidate_text(segment):
    segment_cue=segment.get_contexts()[0]
    return segment.get_parent().text[segment_cue.char_start:segment_cue.char_end+1]

def get_candidate_idx(segment):
    return segment.get_contexts()[0].get_word_start()

# def create_LFs(pair,lf_prefix):
#     # (regex_str,label)=pair

#     def func(c):
#         # print("working on c")
#         return rule_regex_search_candidate_text(c,pair[0],pair[1]) 
        
#     # print(func.__name__)
#     func.__name__=create_function_name(lf_prefix,pair[0])

#     return func


# def create_POS_LFs(pair,lf_prefix):
#     def func(c):
#         # pair[0] as the pos tag pattern (space delimited), pair[1] is the corresponding label if matched
#         return rule_pos_tag_pattern_search(c,pair[0],pair[1])

#     func.__name__=create_function_name(lf_prefix,pair[0])

#     return func

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

def get_surrounding_words(segment,window_size,including_itself=True,lowercase=False):
    word_sequences=get_surrounding_sequence(segment,window_size,including_itself=True,seq_type="words")
    if lowercase:
        return [word.lower() for word in word_sequences]
    return word_sequences

def get_surrounding_lemmas(segment,window_size,including_itself=True):
    return get_surrounding_sequence(segment,window_size,including_itself=True,seq_type="lemmas")

def get_surrounding_tags(segment,window_size,including_itself=True,concatenated=True):
    if concatenated:
        return " ".join(get_surrounding_sequence(segment,window_size,including_itself=True,seq_type="pos_tags"))
    return get_surrounding_sequence(segment,window_size,including_itself=True,seq_type="pos_tags")

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

def create_words_LFs_by_window(pair,lf_prefix,including_itself=True,no_prep_in_btw=False):
    
    # pair = (pattern, window_size, label)
    pattern, window_size, label = pair
    
    def func(c):
        window_tags=" ".join(get_surrounding_words(c,window_size,including_itself=including_itself)).lower()

        return label if pattern in window_tags else 0

    func.__name__=create_function_name(lf_prefix,pattern+str(window_size)+"_"+str(including_itself))
    return func

def create_lemma_LFs_by_window(pair,lf_prefix,including_itself=True,no_prep_in_btw=False):
    
    # pair = (pattern, window_size, label)
    pattern, window_size, label = pair
    
    def func(c):

        c_idx=c.unigram_cue.get_word_start()

        text_window=get_surrounding_lemmas(c,window_size,including_itself=True)
        pos_window=get_surrounding_tags(c,window_size,including_itself=True)

        connection_word=pattern

        if connection_word not in text_window:
            return 0

        connection_psn=text_window.index(connection_word)
        if window_size==-1 and "IN" not in pos_window[:connection_psn]:
            return label
        elif window_size==-2 and "IN" not in pos_window[connection_psn:]:
            return label
        elif window_size==3 and "IN" not in pos_window:
            return label
        return 0

    func.__name__=create_function_name(lf_prefix,"lemma_"+pattern+str(window_size)+"_"+str(including_itself))
    return func

# initialization 
purpose_LFs=[]
mechanism_LFs=[]
null_LFs=[]


# Reference: https://4syllables.com.au/resources/verbs-nouns-cheat-sheet/
nominalization_dict=['achievement', 'action', 'agreement', 'appearance', 'application', 'approval', 'arrival', 'assessment', 'beginning', 'transition', 'commitment', 'communication', 'conclusion', 'confirmation', 'consideration', 'consultation', 'continuation', 'contribution', 'decision', 'definition', 'demonstration', 'description', 'determination', 'development', 'discussion', 'donation', 'editing', 'employment', 'enhancement', 'enrolment, re-enrolment', 'evaluation', 'examination', 'expectation', 'explanation', 'implementation', 'implication', 'indication', 'inspection', 'instruction', 'intention', 'introduction', 'investigation', 'leadership', 'mentoring', 'notification', 'objection', 'observation', 'ownership', 'payment', 'performance', 'prioritisation', 'progression', 'reaction', 'recommendation', 'reduction', 'referral', 'reformation', 'refusal', 'rejection', 'relocation', 'replacement', 'requirement', 'resistance', 'resolution', 'review (as a noun)', 'revision', 'ruling', 'solution', 'statement', 'submission', 'suggestion', 'training', 'transformation', 'translation', 'undertaking']

def purpose_for_clause(c): 

# Criteria: 
# (1) current word is "for"; 
# (2) anything after for (excluding period) has a dep_parent number smaller than for
# (3) the direct child of "for" is a verb or is a nominalization (verb-as-noun) 

# Question/TODO: should we also say, anything after for should be longer than a window_size?

    onset_word="for"

    candidate_word=get_candidate_text(c).lower()

    if candidate_word!=onset_word:
        return 0

    for_idx=get_candidate_idx(c)
    for_psn=for_idx+1

    dep_parents_whole_sent=get_surrounding_dep_parents(c,0,including_itself=True)
    pos_tags_whole_sent=get_surrounding_tags(c,0,including_itself=True,concatenated=False)
    words_whole_sent=get_surrounding_words(c,0,including_itself=True)

    clause=dep_parents_whole_sent[for_psn:-1]

    return PURPOSE_LABEL if all([(dep_parent>=for_psn and (("VB" in pos_tags_whole_sent[for_psn+ind] or words_whole_sent[for_psn+ind].lower() in nominalization_dict) if dep_parent==for_psn else True)) for ind,dep_parent in enumerate(clause)]) else 0


purpose_LFs+=[purpose_for_clause] # this one is very accurate 

def purpose_to_verb(c,min_window_size=7):

# Criteria: 
# (1) current word is "to"; 
# (2) anything after for (excluding period) has a dep_parent number smaller than to
# (3) the direct child of "to" is a verb or is a nominalization (verb-as-noun) 

# Question/TODO: should we also say, anything before a punctuation and after to should be longer than a window_size?

    onset_word="to"

    candidate_word=get_candidate_text(c).lower()

    if candidate_word!=onset_word:
        return 0

    to_idx=get_candidate_idx(c)
    to_psn=to_idx+1

    dep_parents_whole_sent=get_surrounding_dep_parents(c,0,including_itself=True)
    pos_tags_whole_sent=get_surrounding_tags(c,0,including_itself=True,concatenated=False)
    words_whole_sent=get_surrounding_words(c,0,including_itself=True)


    sub_tags=pos_tags_whole_sent[to_psn:]

    if pos_tags_whole_sent[to_idx]!="TO":
        return 0
    if "," in sub_tags and sub_tags.index(",")<min_window_size:
        return 0
    if "." in sub_tags and sub_tags.index(".")<min_window_size:
        return 0

    sentence=c.get_parent()
    doc_sentences=sentence.get_parent().sentences
    sent_idx=doc_sentences.index(sentence)
    if sent_idx==0:
        return 0

    clause=dep_parents_whole_sent[to_psn: (sub_tags.index(",") if "," in sub_tags else sub_tags.index(".") if "." in sub_tags else -1)]

    if len(clause)==0:
        return 0

    to_dep=dep_parents_whole_sent[to_idx]

    # print(sub_tags)
    if all([((dep_parent>=to_dep or ((ind+to_psn+1)==to_dep)) and ((words_whole_sent[to_psn+ind] not in ["be","solve"]) if dep_parent<to_dep or "VB" in pos_tags_whole_sent[to_psn+ind] else True)) for ind,dep_parent in enumerate(clause)]):
        return PURPOSE_LABEL 
    
    return 0

purpose_LFs+=[purpose_to_verb]


def purpose_but_followed_next_sentence_we(onset_word="but",min_window_size=5):

    def func(c):
        candidate_word=get_candidate_text(c).lower()

        if candidate_word!=onset_word:
            return 0

        text_whole=get_surrounding_words(c,0,including_itself=True,lowercase=True)
        
        if "we" in text_whole or "our" in text_whole or "this" in text_whole or "results" in text_whole or "experiments" in text_whole:
            return 0

        to_idx=get_candidate_idx(c)
        to_psn=to_idx+1
        pos_tags_whole_sent=get_surrounding_tags(c,0,including_itself=True,concatenated=False)
        sub_tags=pos_tags_whole_sent[to_psn:]

        if onset_word=="but":
    
            if "," in sub_tags and sub_tags.index(",")<min_window_size:
                return 0
            if "." in sub_tags and sub_tags.index(".")<min_window_size:
                return 0
            if to_idx==0 or pos_tags_whole_sent[to_idx-1] not in [",","."]:
                return 0

        c_idx=c.unigram_cue.get_word_start()

        sentence=c.get_parent()
        doc_sentences=sentence.get_parent().sentences
        sent_idx=doc_sentences.index(sentence)
        if sent_idx==len(doc_sentences)-1:
            return 0
        next_sent_token=doc_sentences[sent_idx+1].__dict__['text'].lower()
        if "we" in next_sent_token or "our" in next_sent_token or "this" in next_sent_token:
            return PURPOSE_LABEL
        return 0

    func.__name__="purpose_but_followed_next_sentence_we".replace("but",onset_word)
    return func
    

purpose_LFs+=[purpose_but_followed_next_sentence_we(onset_word=ow) for ow in ["but"]]


def purpose_followed_by_goal(onset_word="our"):

    def func(c):
        candidate_word=get_candidate_text(c).lower()

        if candidate_word!=onset_word:
            return 0

        to_idx=get_candidate_idx(c)
        to_psn=to_idx+1
        text_whole=get_surrounding_words(c,0,including_itself=True,lowercase=True)
        
        # print(text_whole,to_psn)
        if to_psn<len(text_whole) and "goal" in text_whole[to_psn]:
            return PURPOSE_LABEL
        return 0

    func.__name__="purpose_our_followed_by_goal".replace("our",onset_word)
    return func
    
purpose_LFs+=[purpose_followed_by_goal(onset_word=ow) for ow in ["our","the"]]

def purpose_we_study(c):
    onset_word="we"

    candidate_word=get_candidate_text(c).lower()

    if candidate_word!=onset_word:
        return 0

    to_idx=get_candidate_idx(c)
    to_psn=to_idx+1
    text_whole=get_surrounding_words(c,0,including_itself=True,lowercase=True)
    
    if "study" in text_whole[to_psn] or "studied" in text_whole[to_psn]:
        return PURPOSE_LABEL
    return 0
purpose_LFs+=[purpose_we_study]


def purpose_A_follow_by_B(onset_word,next_word):

    def func(c):

        candidate_word=get_candidate_text(c).lower()

        if candidate_word!=onset_word:
            return 0

        to_idx=get_candidate_idx(c)
        to_psn=to_idx+1
        text_whole=get_surrounding_words(c,0,including_itself=True,lowercase=True)
        
        if to_psn<len(text_whole) and next_word in text_whole[to_psn]:
            return PURPOSE_LABEL
        return 0

    func.__name__="purpose_"+onset_word+"_follow_by_"+next_word.replace(",","comma")
    return func


purpose_LFs+=[purpose_A_follow_by_B(onset_word="however",next_word=","),purpose_A_follow_by_B("we","consider"),purpose_A_follow_by_B("we","examine"),purpose_A_follow_by_B("will","allow"),purpose_A_follow_by_B("that","allows"),purpose_A_follow_by_B("will","enable")]  

def purpose_starting_what(onset_word="what"):

    def func(c):
        candidate_word=get_candidate_text(c).lower()

        if candidate_word!=onset_word:
            return 0

        to_idx=get_candidate_idx(c)
        if to_idx==0:
            return PURPOSE_LABEL
        return 0 
    func.__name__="purpose_starting_what".replace("what",onset_word)
    return func

purpose_LFs+=[purpose_starting_what(onset_word=ow) for ow in ["what","how","although","yet"]]

def purpose_this_paper_investigates(c):

    onset_word="this"
    next_word="paper"
    candidate_word=get_candidate_text(c).lower()

    if candidate_word!=onset_word:
        return 0

    to_idx=get_candidate_idx(c)
    if to_idx!=0:
        return 0
    to_psn=to_idx+1
    text_whole=get_surrounding_words(c,0,including_itself=True,lowercase=True)
    
    if next_word in text_whole[to_psn] and "investigates" in text_whole[to_psn+1]:
        return PURPOSE_LABEL
    return 0
    
purpose_LFs+=[purpose_this_paper_investigates]

def purpose_we_investigate(c):

    onset_word="we"
    next_word="investigate"
    candidate_word=get_candidate_text(c).lower()

    if candidate_word!=onset_word:
        return 0

    to_idx=get_candidate_idx(c)
    if to_idx!=0:
        return 0
    to_psn=to_idx+1
    text_whole=get_surrounding_words(c,0,including_itself=True,lowercase=True)
    
    if next_word in text_whole[to_psn]:
        return PURPOSE_LABEL
    return 0
    
purpose_LFs+=[purpose_we_investigate]


def mechanism_we_propose(next_word="propose"):

    def func(c):

        onset_word="we"

        candidate_word=get_candidate_text(c).lower()

        if candidate_word!=onset_word:
            return 0

        to_idx=get_candidate_idx(c)
        to_psn=to_idx+1
        text_whole=get_surrounding_words(c,0,including_itself=True,lowercase=True)
        
        if next_word in text_whole[to_psn]:
            return MECHANISM_LABEL
        return 0

    func.__name__="mechanism_we_propose".replace("propose",next_word)
    return func
    
mechanism_LFs+=[mechanism_we_propose(next_word) for next_word in ["propose","develop","design","model","modeled","introduce","introduced"]]

def mechanism_we_present(c):

    onset_word="we"
    next_word="present"
    candidate_word=get_candidate_text(c).lower()

    if candidate_word!=onset_word:
        return 0

    to_idx=get_candidate_idx(c)
    to_psn=to_idx+1
    text_whole=get_surrounding_words(c,0,including_itself=True,lowercase=True)
    
    if next_word in text_whole[to_psn] and "a" in text_whole[to_psn+1][0]:
        return MECHANISM_LABEL
    return 0
    
mechanism_LFs+=[mechanism_we_present]


def mechanism_our_followed_by(next_word="work",onset_word="our",sentence_beginning=True):

    def func(c):
        candidate_word=get_candidate_text(c).lower()

        if candidate_word!=onset_word:
            return 0

        to_idx=get_candidate_idx(c)
        if sentence_beginning:
            if to_idx!=0:
                return 0
        to_psn=to_idx+1
        text_whole=get_surrounding_words(c,0,including_itself=True,lowercase=True)
        
        if next_word in text_whole[to_psn]:
            return MECHANISM_LABEL
        return 0

    func.__name__="mechanism_"+onset_word+"_followed_by_"+next_word
    return func


mechanism_LFs+=[mechanism_our_followed_by(next_word=nw) for nw in ["work","approach"]]+[mechanism_our_followed_by(onset_word="we",next_word="extend")]+[mechanism_our_followed_by(onset_word="our",next_word="system")]

def mechanism_by_adv_doing(c):
    onset_word="by"

    candidate_word=get_candidate_text(c).lower()

    if candidate_word!=onset_word:
        return 0

    to_idx=get_candidate_idx(c)

    dep_parents_whole_sent=get_surrounding_dep_parents(c,0,including_itself=True)
    pos_tags_whole_sent=get_surrounding_tags(c,0,including_itself=True,concatenated=False)

    for idx in range(to_idx+1,len(dep_parents_whole_sent)):
        if dep_parents_whole_sent[idx]==(to_idx+1):
            if pos_tags_whole_sent[idx]=="VBG":
                return MECHANISM_LABEL
            return 0
    return 0
mechanism_LFs+=[mechanism_by_adv_doing]

def mechanism_this_paper(c):

    onset_word="this"
    next_word="paper"
    candidate_word=get_candidate_text(c).lower()

    if candidate_word!=onset_word:
        return 0

    to_idx=get_candidate_idx(c)
    if to_idx!=0:
        return 0
    to_psn=to_idx+1
    text_whole=get_surrounding_words(c,0,including_itself=True,lowercase=True)
    
    if next_word in text_whole[to_psn] and text_whole[to_psn+1] in ["introduces","presents","proposes"]:
        return MECHANISM_LABEL
    return 0
    
mechanism_LFs+=[mechanism_this_paper]


def mechanism_in_this_paper(c):

    onset_word="in"
    next_word="this"
    candidate_word=get_candidate_text(c).lower()

    if candidate_word!=onset_word:
        return 0

    to_idx=get_candidate_idx(c)
    if to_idx!=0:
        return 0
    to_psn=to_idx+1
    text_whole=get_surrounding_words(c,0,including_itself=True,lowercase=True)
    
    if next_word in text_whole[to_psn] and "paper" in text_whole[to_psn+1] and ("we" in text_whole[to_psn+3] or "we" in text_whole[to_psn+2]):
        return MECHANISM_LABEL
    return 0
    
mechanism_LFs+=[mechanism_in_this_paper]




# # purpose_LFs+=[create_POS_LFs_by_window((pair[0],-2,pair[1]),"purpose") for pair in [("TO VB ",PURPOSE_LABEL)] ]
# purpose_word_tag_list=[]

# # this part can be augmented with embedding

# purpose_word_tag_list+=[("the problem of",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("the task of",PURPOSE_LABEL)]
# # purpose_word_tag_list+=[("challenging",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("challenge",PURPOSE_LABEL)]
# # purpose_word_tag_list+=[("fundamental",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("to understand",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("to answer",PURPOSE_LABEL)]
# # purpose_word_tag_list+=[("crucial",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("issue",PURPOSE_LABEL)]
# # purpose_word_tag_list+=[("allow ",PURPOSE_LABEL)]
# # purpose_word_tag_list+=[("allows ",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("useful to",PURPOSE_LABEL)]
# # purpose_word_tag_list+=[("task",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("investigate",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("we explore",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("although",PURPOSE_LABEL)]
# # purpose_word_tag_list+=[("however",PURPOSE_LABEL)]
# ## purpose_word_tag_list+=[("yet ",PURPOSE_LABEL)]
# # purpose_word_tag_list+=[("but ",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("know little ",PURPOSE_LABEL)]



# # purpose_word_tag_list+=[("a study of ",PURPOSE_LABEL)]
# # purpose_word_tag_list+=[("existing ",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("deals with ",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("we explore", PURPOSE_LABEL)]
# purpose_word_tag_list+=[("investigate", PURPOSE_LABEL)]
# purpose_word_tag_list+=[("examine",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("whether",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("that allows",PURPOSE_LABEL)]
# # purpose_word_tag_list+=[("in order to",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("ways to",PURPOSE_LABEL)]
# purpose_word_tag_list+=[("our goal is",PURPOSE_LABEL)]
# purpose_LFs+=[create_words_LFs_by_window((pair[0],window_size,pair[1]),"purpose",no_prep_in_btw=True) for pair in purpose_word_tag_list for window_size in [3,-2]]


# purpose_word_tag_list4=[("little is known",PURPOSE_LABEL)]
# purpose_word_tag_list4+=[("limited knowledge",PURPOSE_LABEL)]
# purpose_word_tag_list4+=[("do n't know",PURPOSE_LABEL)]
# purpose_LFs+=[create_words_LFs_by_window((pair[0],window_size,pair[1]),"purpose",no_prep_in_btw=True) for pair in purpose_word_tag_list4 for window_size in [4]]


# purpose_word_tag_list2=[("bottleneck",PURPOSE_LABEL)]
# # purpose_word_tag_list2+=[("problem",PURPOSE_LABEL)]
# purpose_word_tag_list2+=[("challenging",PURPOSE_LABEL)]
# purpose_word_tag_list2+=[("fundamental",PURPOSE_LABEL)]
# purpose_word_tag_list2+=[("issue",PURPOSE_LABEL)]
# purpose_word_tag_list2+=[("task",PURPOSE_LABEL)]
# purpose_word_tag_list2+=[("challenge",PURPOSE_LABEL)]
# purpose_LFs+=[create_words_LFs_by_window((pair[0],window_size,pair[1]),"purpose",no_prep_in_btw=True) for pair in purpose_word_tag_list2 for window_size in [3,-1]]
# purpose_LFs+=[purpose_for_clause, purpose_to_verb] # purpose_for_doing,

# purpose_lemma_tag_list=[("understand",PURPOSE_LABEL)]
# purpose_lemma_tag_list+=[("answer",PURPOSE_LABEL)]
# # purpose_lemma_tag_list+=[("crucial",PURPOSE_LABEL)]
# # purpose_lemma_tag_list+=[("issue",PURPOSE_LABEL)]
# # purpose_lemma_tag_list+=[("allow",PURPOSE_LABEL)]
# purpose_lemma_tag_list+=[("investigate",PURPOSE_LABEL)]
# purpose_lemma_tag_list+=[("study",PURPOSE_LABEL)]
# purpose_lemma_tag_list+=[("explore",PURPOSE_LABEL)]
# purpose_lemma_tag_list+=[("although",PURPOSE_LABEL)]
# purpose_lemma_tag_list+=[("however",PURPOSE_LABEL)]
# purpose_lemma_tag_list+=[("examine",PURPOSE_LABEL)]
# purpose_LFs+=[create_lemma_LFs_by_window((pair[0],window_size,pair[1]),"purpose",no_prep_in_btw=True) for pair in purpose_lemma_tag_list for window_size in [3,-2]]

# def purpose_end_question_mark(c):
#     text_whole_sent=get_surrounding_words(c,0,including_itself=True)

#     if "?"==text_whole_sent[-1]:
#         return PURPOSE_LABEL
#     return 0 

# from scipy.spatial.distance import cosine
# purpose_LFs+=[purpose_but_followed_next_sentence_we]

# # for pair in [("develops","developed"),("propose","studied"),("method","methods"),("rapid","fast"),("propose","proposed"),("propose","introduce"),("method","approach"),("model","approach"),("algorithm","model"),("models","model"),("models","modeling"),("modeling","model"),("dataset","corpus"),("growth","development"),("emerging","arising"),("emerging","emerged")]:
# #     if pair[0] in glove_words and pair[1] in glove_words:
# #         print(pair,1-cosine(glove_words[pair[0]],glove_words[pair[1]]))
# #     else:
# #         print("at lease one not in glove_words",pair)

# def create_LFs_by_embedding_similarity(pair,lf_prefix,including_itself=True,threshold=0.8):
    
#     lemma, window_size, label = pair
#     def func(c):
#         window_words=get_surrounding_words(c,window_size,including_itself=including_itself)
        
#         if lemma not in glove_words:
#             return 0
#         lemma_array=glove_words[lemma]
#         for word in window_words:
#             if word in glove_words and 1-cosine(glove_words[word],lemma_array)>threshold:
#                 # print("there are this word ",word, "similar to lemma",lemma)
#                 return label
#         return 0

#     func.__name__=create_function_name(lf_prefix,"we_similar_"+lemma+"_"+str(window_size)+"_"+str(including_itself))
#     return func

# # purpose_LFs+=[create_LFs_by_embedding_similarity((pair[0],window_size,pair[1]),"purpose") for pair in purpose_word_tag_list2 for window_size in [-2]]
# # purpose_LFs+=[create_LFs_by_embedding_similarity((lemma,window_size,PURPOSE_LABEL),"purpose") for lemma in ["allow"] for window_size in [-2]]


# mechanism_pos_tag_list=[]
# mechanism_LFs=[create_POS_LFs_by_window((pair[0],window_size,pair[1]),"mechanism") for pair in mechanism_pos_tag_list for window_size in [3,-2]]

# mechanism_word_tag_list=[]
# mechanism_word_tag_list=[("propose", MECHANISM_LABEL)]
# mechanism_word_tag_list+=[("include", MECHANISM_LABEL)]
# mechanism_word_tag_list+=[("includes", MECHANISM_LABEL)]
# mechanism_word_tag_list+=[("develop ", MECHANISM_LABEL)]
# mechanism_word_tag_list+=[("develops ", MECHANISM_LABEL)]
# mechanism_word_tag_list+=[("developed ", MECHANISM_LABEL)]
# mechanism_word_tag_list+=[("provide", MECHANISM_LABEL)]
# # mechanism_word_tag_list+=[("presents ", MECHANISM_LABEL)]
# # mechanism_word_tag_list+=[("present ", MECHANISM_LABEL)]
# mechanism_word_tag_list+=[("by ", MECHANISM_LABEL)] 
# mechanism_word_tag_list+=[("method ", MECHANISM_LABEL)] # propsed a method, vs. most existing methods
# # mechanism_word_tag_list+=[("approach ", MECHANISM_LABEL)]
# # mechanism_word_tag_list+=[("via ", MECHANISM_LABEL)]
# ## mechanism_word_tag_list+=[("a function that", MECHANISM_LABEL)]
# # mechanism_word_tag_list+=[("contribution", MECHANISM_LABEL)]
# mechanism_LFs+=[create_words_LFs_by_window((pair[0],window_size,pair[1]),"mechanism") for pair in mechanism_word_tag_list for window_size in [3,-2]]

# # mechanism_LFs+=[create_LFs_by_embedding_similarity((lemma,window_size,MECHANISM_LABEL),"mechanism") for lemma in ["propose","develop","provide","present","method","employ"] for window_size in [-1,-2]]

# mechanism_word_tag_list2=[("is proposed", MECHANISM_LABEL)]
# mechanism_word_tag_list+=[("are proposed", MECHANISM_LABEL)]
# mechanism_word_tag_list+=[("was proposed", MECHANISM_LABEL)]
# mechanism_LFs+=[create_words_LFs_by_window((pair[0],window_size,pair[1]),"mechanism") for pair in mechanism_word_tag_list for window_size in [3,-1]]

# # should we ignore this??
# # mechanism_pos_tag_list2=[("VBZ VBN",MECHANISM_LABEL)] # cue: is proposed
# # mechanism_pos_tag_list2+=[("VBD VBN",MECHANISM_LABEL)] # cue: was proposed
# # mechanism_pos_tag_list2+=[("VBP VBN",MECHANISM_LABEL)] # cue: are proposed
# # mechanism_LFs+=[create_POS_LFs_by_window((pair[0],window_size,pair[1]),"mechanism") for pair in mechanism_pos_tag_list2 for window_size in [3,-1]]


# mechanism_word_tag_list3=[("we use ", MECHANISM_LABEL)]
# mechanism_word_tag_list3+=[("uses ", MECHANISM_LABEL)]
# # mechanism_word_tag_list3+=[("using a ", MECHANISM_LABEL)]
# mechanism_word_tag_list3+=[("using the ", MECHANISM_LABEL)]
# mechanism_word_tag_list3+=[("by using", MECHANISM_LABEL)]
# mechanism_LFs+=[create_words_LFs_by_window((pair[0],window_size,pair[1]),"mechanism") for pair in mechanism_word_tag_list3 for window_size in [5]]


# mechanism_lemma_tag_list=[("propose",MECHANISM_LABEL)]
# mechanism_lemma_tag_list+=[("develop",MECHANISM_LABEL)]
# mechanism_lemma_tag_list+=[("provide",MECHANISM_LABEL)]
# mechanism_lemma_tag_list+=[("present",MECHANISM_LABEL)]
# mechanism_lemma_tag_list+=[("employ",MECHANISM_LABEL)]
# # mechanism_lemma_tag_list+=[("approach",MECHANISM_LABEL)]
# mechanism_lemma_tag_list+=[("via",MECHANISM_LABEL)]
# mechanism_LFs+=[create_lemma_LFs_by_window((pair[0],window_size,pair[1]),"mechanism",no_prep_in_btw=True) for pair in mechanism_lemma_tag_list for window_size in [3,-2]]




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

# def mechanism_then_VB(c):

#     candidate_idx_in_sent=c.get_contexts()[0].get_word_start()
#     # print("candidate_idx_in_sent",candidate_idx_in_sent)
#     text_whole_sent=get_surrounding_words(c,0,including_itself=True)
#     connection_word="then"

#     if connection_word not in text_whole_sent:
#         return 0

#     connection_idx=text_whole_sent.index(connection_word)
#     pos_whole_sent=get_surrounding_tags(c,0,including_itself=True,concatenated=False)

#     if connection_idx<len(text_whole_sent)-1 and "VB" in pos_whole_sent[connection_idx+1]:
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

# def mechanism_NN_for(c):

    
#     c_idx=c.unigram_cue.get_word_start()

#     text_whole=get_surrounding_words(c,0,including_itself=True)
    
#     connection_word="for"


#     if connection_word not in text_whole:
#         return 0

#     connection_idx=text_whole.index(connection_word)

#     dep_parents=get_surrounding_dep_parents(c,0,including_itself=True)
#     pos_tags=get_surrounding_tags(c,0,including_itself=True)
#     # print(c_idx)
#     # print(dep_parents[connection_idx])
#     # print(dep_parents[connection_idx]-1)
#     # print(pos_tags)
#     # print(pos_tags[dep_parents[connection_idx]-1])
#     # print(dep_parents[dep_parents[connection_idx]-1]-1)
#     # print(pos_tags[dep_parents[dep_parents[connection_idx]-1]-1])
#     if "NN" in pos_tags[dep_parents[connection_idx]-1] and "VB" in pos_tags[dep_parents[dep_parents[connection_idx]-1]-1] and c_idx<connection_idx:
#         return MECHANISM_LABEL
#     return 0


# # any mechanism that has NN TO VB pattern, anything before TO VB will be mechanism 
# # mechanism_LFs+=[create_POS_LFs_by_window((pair[0],-1,pair[1]),"mechanism",including_itself=False) for pair in [("TO VB",MECHANISM_LABEL)] ]
# # mechanism_LFs+=[create_POS_LFs_by_window((pair[0],-1,pair[1]),"mechanism",including_itself=False) for pair in [("IN VBG",MECHANISM_LABEL)] ]
# mechanism_LFs+=[mechanism_by_adv_doing,mechanism_then_VB]#,mechanism_NN_for] #mechanism_an_algorithm,mechanism_then_VB]

# null_LFs=[]
# null_word_tag_list=[]
# null_word_tag_list+=[("test", NULL_LABEL)]
# # null_word_tag_list+=[("dataset", NULL_LABEL)]
# null_word_tag_list+=[("experiment", NULL_LABEL)]
# null_word_tag_list+=[("results", NULL_LABEL)]
# null_word_tag_list+=[("show", NULL_LABEL)]
# null_word_tag_list+=[("shows that", NULL_LABEL)]
# null_word_tag_list+=[("show that", NULL_LABEL)]
# null_word_tag_list+=[("find that", NULL_LABEL)]
# null_word_tag_list+=[("finds that", NULL_LABEL)]
# null_word_tag_list+=[("found that", NULL_LABEL)]
# null_word_tag_list+=[("this result", NULL_LABEL)]
# null_word_tag_list+=[("observe", NULL_LABEL)]
# null_word_tag_list+=[("prove", NULL_LABEL)]
# # null_word_tag_list+=[("evaluates ", NULL_LABEL)]
# # null_word_tag_list+=[("evaluated ", NULL_LABEL)]
# # null_word_tag_list+=[("evaluate ", NULL_LABEL)]
# null_word_tag_list+=[("validate ", NULL_LABEL)]
# # null_word_tag_list+=[("qualitative ", NULL_LABEL)]
# # null_word_tag_list+=[("quantitative ", NULL_LABEL)]
# ## null_word_tag_list+=[("validating ", NULL_LABEL)]
# # null_word_tag_list+=[("demonstrate", NULL_LABEL)]
# # null_word_tag_list+=[("indicate that", NULL_LABEL)]
# # null_word_tag_list+=[("indicates that", NULL_LABEL)]
# null_word_tag_list+=[("are performed", NULL_LABEL)]
# null_word_tag_list+=[("were performed", NULL_LABEL)]
# null_word_tag_list+=[("indicate that", NULL_LABEL)]
# # null_word_tag_list+=[("have been", NULL_LABEL)] # background
# # null_word_tag_list+=[("the success of", NULL_LABEL)] # background
# ## null_word_tag_list+=[("recently", NULL_LABEL)] # background
# ## null_word_tag_list+=[("recent research", NULL_LABEL)] # background
# null_word_tag_list+=[("increasingly", NULL_LABEL)] # background
# null_word_tag_list+=[("has been", NULL_LABEL)] # background
# null_word_tag_list+=[("has shown", NULL_LABEL)] # background
# # null_word_tag_list+=[("popular ", NULL_LABEL)] # background
# null_word_tag_list+=[("popularity ", NULL_LABEL)] # background
# null_word_tag_list+=[("increasing", NULL_LABEL)] # background
# # null_word_tag_list+=[("previously", NULL_LABEL)] # background
# # null_word_tag_list+=[("general", NULL_LABEL)] # background
# null_word_tag_list+=[("compared to", NULL_LABEL)] # background
# null_word_tag_list+=[("compare ", NULL_LABEL)] # background
# null_LFs+=[create_words_LFs_by_window((pair[0],window_size,pair[1]),"null") for pair in null_word_tag_list for window_size in [3,-2]]

# # null_word_tag_list2=[("settings", NULL_LABEL)]
# # null_word_tag_list2+=[("general", NULL_LABEL)] # background
# # null_LFs+=[create_words_LFs_by_window((pair[0],window_size,pair[1]),"null") for pair in null_word_tag_list2 for window_size in [3,-1]]
# # null_LFs+=[create_LFs_by_embedding_similarity((lemma,window_size,NULL_LABEL),"null") for lemma in ["indicate","interview","benchmark","experiment","empirical","shows"] for window_size in [-2]]


# null_lemma_tag_list=[("prototype",NULL_LABEL)]
# null_lemma_tag_list+=[("quantitative",NULL_LABEL)]
# null_lemma_tag_list+=[("qualitative",NULL_LABEL)]
# null_lemma_tag_list+=[("report",NULL_LABEL)]
# null_lemma_tag_list+=[("evaluate",NULL_LABEL)]
# null_lemma_tag_list+=[("demonstrate",NULL_LABEL)] 
# null_lemma_tag_list+=[("indicate",NULL_LABEL)] 
# null_lemma_tag_list+=[("suggest",NULL_LABEL)] 
# null_lemma_tag_list+=[("interview",NULL_LABEL)] 
# null_lemma_tag_list+=[("benchmark",NULL_LABEL)] 
# null_lemma_tag_list+=[("experiment",NULL_LABEL)] 
# null_lemma_tag_list+=[("empirical",NULL_LABEL)] 
# null_LFs+=[create_lemma_LFs_by_window((pair[0],window_size,pair[1]),"null",no_prep_in_btw=True) for pair in null_lemma_tag_list for window_size in [3,-2]]





