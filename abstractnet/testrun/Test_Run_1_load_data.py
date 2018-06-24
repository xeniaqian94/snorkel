
# coding: utf-8

# ## Test Run 1: Load AbstractNet Dataset: 70K unlabeled (and 2K labeled) Abstracts into DB
# 
# This notebook loads the dataset and create labeled *candidates* through labeling function. Feel extra free to document/bring up any upcoming confusion throughout the test run, e.g. are the following two consistent, the **(segment, label) pair** that we want to have, and the **candidates** that we instruct snorkel to extract? 
# 
# Before everything, please ensure that you have followed project-level ``README.md`` and installed all python dependencies, e.g. ``tika``.  
# 
# We filtered out null abstracts from `ClydeDB.csv` ([AbstractSegmentationCrowdNLP Git repo](https://github.com/zhoujieli/AbstractSegmentationCrowdNLP.git)), resulting in 48,914 valid ones out of 56,851 total abstracts. The 48,914 abstracts are saved to `data/70kpaper.tsv`.
# 
# 

# In this section, we preprocess documents by parsing them into *contexts*. *Candidates* are extracted out of *contexts*, which are *instances* (one of the *background*, *mechanism*, *method*, and *findings*).

# In[2]:


# import os
# os.chdir("../../")

# get_ipython().magic('load_ext autoreload')
# get_ipython().magic('autoreload 2')
# get_ipython().magic('matplotlib inline')
import os

from snorkel import SnorkelSession
session = SnorkelSession()

# # Here, we just set how many documents we'll process for automatic testing- you can safely ignore this!
n_docs = 500 if 'CI' in os.environ else 1000 #  change the number 1000 to 60,000 for real dataset 

from snorkel.parser import TSVDocPreprocessor

doc_preprocessor = TSVDocPreprocessor('abstractnet/testrun/data/70kpaper_061418_cleaned.tsv', encoding="utf-8",max_docs=n_docs)


# Get statistics on the number of documents and sentences, as below. This could take 5-8 minutes to load ~60K papers (see progress bar, also might have exception). The following code parses docs into sentences by period, averaging 4.49 sentences per documents. Earlier I spent a few hours debugging some hidden formatting error that confuses Spacey. Need to ensure that we format raw data from .csv into .tsv *without* preceeding and appending quotes.  
# 

# In[3]:

from snorkel.parser.spacy_parser import Spacy
from snorkel.parser import CorpusParser


corpus_parser = CorpusParser(parser=Spacy())
corpus_parser.apply(doc_preprocessor, count=n_docs)


from snorkel.models import Document, Sentence

print("Documents:", session.query(Document).count())
print("Sentences:", session.query(Sentence).count())


# Next we extract `candidates` by defining the specific `CandidateExtractor` for abstract segmentation. We take *Background* as an example and come back with other segmentation parts, i.e., *mechanism*, *method*, *findings*, later. 
# 
# Some more explanation based on my understanding: 
#     
# 1. `Candidates` are defined as a class that contains 1+ `Span` objects within one `Sentence` context.  
#     
# 2. `Span(s)` correspond to conceptual categories in text like people or disease names. 
# 
# To visualize, here is the Context Hierarchy 
# <img src="../../tutorials/workshop/imgs/context-hierarchy.jpg" width="300px;">
# 
# All `Context(s)` are hierarchical in Snorkel. The default objects provided by Snorkel are show above. 
#     
# In the intro tutorial example, their `candidate` represents the possible `Spouse` mention `(Barrack Obama, Michelle Obama)`. As readers, we know this mention is true due to external knowledge and the keyword of `wedding` occuring later in the sentence. (Reference: (1) section `Writing a basic CandidateExtractor` in [Intro_tutorial_1](../intro/Intro_Tutorial_1.ipynb); (2) section `Candidate Member Functions and Variables` in [Workshop_1_Snorkel_API](../workshop/Workshop_1_Snorkel_API.ipynb)) 
# 
# 
# + Background: 
#   - "Recent research ... ", 
#   - "... have/has been widely ...", 
#   - "How ... ?" (and as the first sentence), 
#   - "Previous work...", 
#   - "Motivated by...", 
#   - "The success of ...", etc.
# + Mechanism:
#   - something
#   - some other pattern

# We define `CandidateExtractor` as a wrapper of `CandidateSpace` (e.g. `Ngrams` is one type of `CandidateSpace`) and `Matcher` (e.g. `DictionaryMatcher`, `PersonMatcher`). Please make sure that `longest_match_only=True`, since this gets us longest span that contains dictionary words. (Reference: source code [candidates.py](../../snorkel/candidates.py) and [matchers.py](../../snorkel/matchers.py)]

# Get the longest sentence length. This value is important, to be used soon.

# In[4]:


sents = session.query(Sentence).all()
n_max_corpus=0
for sent in sents:
    n_max_corpus=max(n_max_corpus,len(sent.words))

print("The longest sentence has "+str(n_max_corpus)+" tokens.")


# In[7]:


from snorkel.models import candidate_subclass
from snorkel.candidates import Ngrams, CandidateExtractor
from snorkel.matchers import PersonMatcher,DictionaryMatch

Background = candidate_subclass('Background', ['background_cue'])

ngrams = Ngrams(n_max=n_max_corpus) # we define the maximum n value as n_max_corpus
# Start simple: any ngram that matches the dictionary are *background* candidates! 
dict_matcher=DictionaryMatch(d=['previous','motivated','recent','widely'],longest_match_only=True) 
cand_extractor=CandidateExtractor(Background, [ngrams], [dict_matcher])


# Now we apply the defined `CandidateExtractor` to the all `Sentences` in the collection (splitted 90/10/10 for train/dev/test). 

# In[8]:


from snorkel.models import Document
from util import number_of_people

docs = session.query(Document).order_by(Document.name).all()

train_sents = set()
dev_sents   = set()
test_sents  = set()

for i, doc in enumerate(docs):
    for s in doc.sentences:
        # if number_of_people(s) <= 5:
        if i % 10 == 8:

            dev_sents.add(s)
        elif i % 10 == 9:
            test_sents.add(s)
        else:
            train_sents.add(s)
                
for i, sents in enumerate([train_sents, dev_sents, test_sents]):
    cand_extractor.apply(sents, split=i)
    print("Split "+str(i)+" - number of candidates extracted:", session.query(Background).filter(Background.split == i).count(),"\n\n")
            


# Let's take a look at a few of those extracted `Candidates`! Obviously, since we used `DictionaryMatcher`, all `Candidates` will contain at least one word from the set `['previous','motivated','recent','widely']`.

# In[18]:


# from IPython.display import Markdown, display
#
# def printmd(string):
#     display(Markdown(string))
    
cands = session.query(Background).filter(Background.split == 0).all()

document_list=list()
for i in range(len(cands)):

    print(str(i)+"/"+str(len(cands))+" Candidate/Span:\t"+str(cands[i].background_cue))
    print("Its parent Sentence's text:\t"+str(cands[i].get_parent().text))
    # printmd("**"+str(i)+"/"+str(len(cands))+" Candidate/Span:**\t`"+str(cands[i].background_cue)+"`")
    # printmd("**Its parent Sentence's text:**\t"+str(cands[i].get_parent().text))
    document_list+=[cands[i].background_cue.sentence]
    print()
    
print("Is there any of the extracted candidates come from the same sentence? "+str(len(set(document_list))!=len(document_list)))

# **(Solved) Question 1:** the `CandidateExtractor` extracts only spans with length 1. But Each sentence is only getting matched once with one span (try search "sentence=3993", for example). The sentence is good, but we still would want longer span, e.g. half part or the whole of a sentence. 
# 
# `Span("b'previous'", sentence=4705, chars=[20,27], words=[4,4])`
# 
# **Answer 1:** overwrite `DictionaryMatch._f()`.
# 
# =====================================================================================
# 
# **(Solved) Question 2:** Several `Span` corresponds to the same sentence, e,g, three `Span` corresponds to `sentence=490`. They wee all included even after we have set `longest_match_only=True`, as these spans all have the longest length.  
# 
# **Answer 2:** Perhaps try either (1) filtering by first appearance of document ID; (2) set max_length as the length of the longest sentence length.
# 
# 
# ### Stopped here as of Wed 06/19 9:39 pm. More to come ... ###

# ## TODO List
# 
# 1. Re-format 2K gold label papers. Load them as gold standard. Question: are there any recommended approaches to evaluate segmentation quality, e.g. word overlap? 
# 2. Our current segmentation strictly segments by sentence boundary, is that errorenous? 
# 
# 

# Thanks for reading! 
# 
# Some debugging note to memorize (could ignore). 
# 
# ```
# python -m spacy download en
# ```
# 
# Current issue: parser does not parse *by periods*. Sentence count is significantly fewer than expected! 
# Potential fix: https://github.com/explosion/spaCy/issues/93
# 
# ======= Some more debugging log here (not necessary, could skip reading) ======
# ~~~~
# Xins-MacBook-Pro:~ xin$ source activate snorkel
# (snorkel) Xins-MacBook-Pro:~ xin$ python
# Python 3.6.4 |Anaconda custom (64-bit)| (default, Jan 16 2018, 12:04:33) 
# [GCC 4.2.1 Compatible Clang 4.0.1 (tags/RELEASE_401/final)] on darwin
# Type "help", "copyright", "credits" or "license" for more information.
# >>> import spacey
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# ModuleNotFoundError: No module named 'spacey'
# >>> import spacy
# >>> spacy.load('en')
# <spacy.en.English object at 0x1080e1da0>
# >>> model=spacy.load('en')
# >>> docs=model.tokenizer('Hello, world. Here are two sentences.')
# >>> for sent in docs.sents:
# ...     pritn(sent.text)
# ... 
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
#   File "spacy/tokens/doc.pyx", line 439, in __get__ (spacy/tokens/doc.cpp:9808)
# ValueError: Sentence boundary detection requires the dependency parse, which requires data to be installed. For more info, see the documentation: 
# https://spacy.io/docs/usage
# 
# >>> for sent in docs.sents:
# ...     print(sent.text)
# ... 
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
#   File "spacy/tokens/doc.pyx", line 439, in __get__ (spacy/tokens/doc.cpp:9808)
# ValueError: Sentence boundary detection requires the dependency parse, which requires data to be installed. For more info, see the documentation: 
# https://spacy.io/docs/usage
# 
# >>> from spacy.en import English
# >>> nlp = English()
# >>> doc = nlp(raw_text)
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# NameError: name 'raw_text' is not defined
# >>> raw_text='Hello, world. Here are two sentences.'
# >>> doc = nlp(raw_text)
# >>> sentences = [sent.string.strip() for sent in doc.sents]
# >>> sentences
# ['Hello, world.', 'Here are two sentences.']
# >>> model(raw_text)
# Hello, world. Here are two sentences.
# >>> docs=model(raw_text)
# >>> docs.sents
# <generator object at 0x14ad31948>
# >>> docs=model(raw_text)
# >>> sentences = [sent.string.strip() for sent in docs.sents]
# >>> sentences
# ['Hello, world.', 'Here are two sentences.']
# >>> 
# ~~~~
# 
