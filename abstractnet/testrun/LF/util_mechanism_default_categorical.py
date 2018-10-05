from snorkel.lf_helpers import *

from .util_common_default_categorical import * # create_LFs,create_POS_LFs,candidate_pos_in_doc,PURPOSE_LABEL,MECHANISM_LABEL

# Part 1.1: existing 11 LFs
# mechanism_regex_list=[("((^|\s)introduce.*$)",MECHANISM_LABEL)]
# mechanism_regex_list+=[("((^|\s)propos.*$)",MECHANISM_LABEL)]  # propose or proposing
# mechanism_regex_list+=[("((^|\s)develop.*$)",MECHANISM_LABEL)]
# mechanism_regex_list+=[("((^|\s)approach.*$)",MECHANISM_LABEL)]
# mechanism_regex_list+=[("((^|\s)applied.*$)",MECHANISM_LABEL)]
# mechanism_regex_list+=[("((^|\s)apply.*$)",MECHANISM_LABEL)]
# mechanism_regex_list+=[("((^|\s)using.*$)",MECHANISM_LABEL)]
# mechanism_regex_list+=[("((^|\s)present.*$)",MECHANISM_LABEL)]
# mechanism_regex_list+=[("((^|\s)contribute.*$)",MECHANISM_LABEL)]
# mechanism_regex_list+=[("((^|\s)build.*$)",MECHANISM_LABEL)]
# mechanism_regex_list+=[("((^|\s)built.*$)",MECHANISM_LABEL)]

mechanism_regex_list=[("(introduce.*$)",MECHANISM_LABEL)]
mechanism_regex_list=[("(describe.*$)",MECHANISM_LABEL)]
mechanism_regex_list+=[("(the proposed)",MECHANISM_LABEL)]  # propose or proposing 1
mechanism_regex_list+=[("(we propose)",MECHANISM_LABEL)]  # propose or proposing 2 
mechanism_regex_list+=[("(is proposed)",MECHANISM_LABEL)]  # propose or proposing 3
mechanism_regex_list+=[("(are proposed)",MECHANISM_LABEL)]  # propose or proposing 4


mechanism_regex_list+=[("((^|\s)develop.*$)",MECHANISM_LABEL)]
mechanism_regex_list+=[("((^|\s)approach.*$)",MECHANISM_LABEL)]
mechanism_regex_list+=[("((^|\s)applied.*$)",MECHANISM_LABEL)]
mechanism_regex_list+=[("((^|\s)apply.*$)",MECHANISM_LABEL)]
mechanism_regex_list+=[("((^|\s)using.*$)",MECHANISM_LABEL)]

mechanism_regex_list+=[("(we present)",MECHANISM_LABEL)]
mechanism_regex_list+=[("(this paper presents)",MECHANISM_LABEL)]
mechanism_regex_list+=[("(the paper presents)",MECHANISM_LABEL)]

mechanism_regex_list+=[("(present)",MECHANISM_LABEL)]

mechanism_regex_list+=[("((^|\s)contribute.*$)",MECHANISM_LABEL)]
mechanism_regex_list+=[("((^|\s)build.*$)",MECHANISM_LABEL)]
mechanism_regex_list+=[("((^|\s)built.*$)",MECHANISM_LABEL)]


# Part 1.2: new 27 LFs added 090518, should it be a "we+verb" thing
# mechanism_regex_list+=[("((^|\s)design.*$)",MECHANISM_LABEL)]
mechanism_regex_list+=[("we (also )*give",MECHANISM_LABEL)]
mechanism_regex_list+=[("we (also )*formalize",MECHANISM_LABEL)]
mechanism_regex_list+=[("we (also )*establish",MECHANISM_LABEL)]
# mechanism_regex_list+=[("we (also )*reason",MECHANISM_LABEL)]
# mechanism_regex_list+=[("we (also )*show",MECHANISM_LABEL)]
# mechanism_regex_list+=[("we (also )*identify",MECHANISM_LABEL)]
# mechanism_regex_list+=[("we (also )*characterize",MECHANISM_LABEL)]
# mechanism_regex_list+=[("we (also )*proceed to",MECHANISM_LABEL)]
# mechanism_regex_list+=[("our algorithm",MECHANISM_LABEL)]
# mechanism_regex_list+=[("the method",MECHANISM_LABEL)]
# mechanism_regex_list+=[("the algorithm",MECHANISM_LABEL)]
# mechanism_regex_list+=[("in our",MECHANISM_LABEL)]
# mechanism_regex_list+=[("^our",MECHANISM_LABEL)]
mechanism_regex_list+=[("we (also )*provide",MECHANISM_LABEL)]
mechanism_regex_list+=[("we (also )*derive",MECHANISM_LABEL)]
# mechanism_regex_list+=[("we (also )*illustrate",MECHANISM_LABEL)]
# mechanism_regex_list+=[("than existing algorithms",MECHANISM_LABEL)]
mechanism_regex_list+=[("we (also )*extend",MECHANISM_LABEL)]
# mechanism_regex_list+=[("using (([a-z]+[ ]{0,1})*)",MECHANISM_LABEL)]
# mechanism_regex_list+=[("we (also )*adopt",MECHANISM_LABEL)]
# mechanism_regex_list+=[("we (also )*argue",MECHANISM_LABEL)]
mechanism_regex_list+=[("we (also )*generalize",MECHANISM_LABEL)]
# mechanism_regex_list+=[("novelty is",MECHANISM_LABEL)]
mechanism_regex_list+=[("a[a-z ]+algorithm",MECHANISM_LABEL)]
mechanism_regex_list+=[("a[a-z ]+mechanism",MECHANISM_LABEL)]
# mechanism_regex_list+=[("we (also )*demonstrate",MECHANISM_LABEL)]


mechanism_pos_tag_list=[("PRP VBP",MECHANISM_LABEL)] # cue: we propose/present/...
mechanism_pos_tag_list+=[("PRP RB VBP",MECHANISM_LABEL)] # cue: we further/also propose/present/...
mechanism_pos_tag_list+=[("DT VBN NN",MECHANISM_LABEL)] # cue: the proposed method/methods
mechanism_pos_tag_list+=[("VBZ VBN",MECHANISM_LABEL)] # cue: is proposed
mechanism_pos_tag_list+=[("VBD VBN",MECHANISM_LABEL)] # cue: was proposed
mechanism_pos_tag_list+=[("VBP VBN",MECHANISM_LABEL)] # cue: are proposed
mechanism_pos_tag_list+=[("DT NN VBZ",MECHANISM_LABEL)] # cue: this/the paper proposes/presents/...
mechanism_pos_tag_list+=[("DT NN VBN",MECHANISM_LABEL)] # cue: the/this paper proposed/presented/...



def proper_mechanism_pos(c):
	return MECHANISM_LABEL if candidate_pos_in_doc(c)>=0.4 else 0

mechanism_LFs=[create_LFs(pair,"mechanism") for pair in mechanism_regex_list]+[create_POS_LFs(pair,"mechanism") for pair in mechanism_pos_tag_list]# +[proper_mechanism_pos]
