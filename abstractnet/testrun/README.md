#### This is the README.md for snorkel testrun on Analogy Mining project

We are maintaining and building a list of ipython notebooks, about any experience/lessons that we have learned about Snorkel. 


Below are a few common Snorkel transational error to help unnecessary prevent/debug. 
1. If you want to overwrite a Snorkel session, please make sure to restart your current notebook kernel. Otherwise, you might experience mid-of-commit atomicity-related snorkel Exception, whose exception stack could also be hard to interpret.

2. The LabelAnnotator needs to get cleared before get re-applied. Or needs to be re-created.
e.g. 1
    from snorkel.annotations import LabelAnnotator
    np.random.seed(1702)
    labeler.clear(session,split=1)
    %time L_dev = labeler.apply(split=1)
e.g. 2

    np.random.seed(1701)

    # input(type(labeler))
    labeler = LabelAnnotator(lfs=purpose_LFs)
    # labeler.clear(session,split=1)
    %time L_dev = labeler.apply_existing(split=1)

3. Documentation that is related to start a new session or re-open an existing session is located at models/meta.py

4. Write your regex in lightweight. Snorkel could hiccup (0% halting ProgressBar) with heavy regex, e.g. 

mechanism_regex_list+=[("a[n]{0,1} (([a-z]+[ ]{0,1})*)algorithm",1)]
mechanism_regex_list+=[("a[n]{0,1} (([a-z]+[ ]{0,1})*)mechanism",1)]

compared to lightweight regex,

mechanism_regex_list+=[("we (also )*show",1)]


