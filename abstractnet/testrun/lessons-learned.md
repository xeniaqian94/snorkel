## Automated abstract segmentation

### Task definition 

This task examines effective weak-supervision approach to segment abstracts (into sections of *background*, *problem*, *mechanism*, *finding*, etc.). It serve as the pre-processing technique to support analogical thinking for scientific researchers to generate new ideas.

We illustrate the segmentation (red as problem section, blue as mechanism section) below, compared with ground-truth segmentation from human annotators, and supervised segmentation from a labeled dataset in [SOLVENT paper](http://joelchan.me/assets/pdf/2018-cscw-schema-highlighter.pdf).

![Segmentation by weakly-supervised, supervised models and groud-truth](visualization.png)

### Lessons learned

1. Q: Can weak supervision support segmentation of abstracts (i.e., purpose/mechanism)?
A: To some extent. First, one requirement is to segment by word (as the unit), not clause or sentence. We design labeling functions wit the word as candidate, and its surroundin context. 

we seem to have some success with purpose, less so with mechanism (supervised models still seem to be substantially better)


A: Especially if we do expansions
A: Hybrid model (Snorkel-purpose, supervised-mechanism) partially replicates CSCW50 findings: approaches crowd-level matching, but only up to K=2%; also finding different matches than all-words baseline
Q: Why is there such a weak relationship between word-level label accuracy (agreement with “gold standard”) and matching accuracy? In other words, how can we get reasonable matching performance with sub-.50 label accuracy?
H: Types of errors matter - might be ok to have overall bad-ish label accuracy as long as we capture the most important/informative bits, or ok to capture things that are purpose but were ignored by gold standard because they were repeats at the end.
Q: Why weak-onset > supervised for purpose, and weak-onset < supervised for mechanism?
H: good cues + reasonable expansion strategies for purpose, not so much for mechanism (especially expansion strategies)
A: Cue-density seems like a poor fit for Snorkel’s advantages: many cues are sparse, so denoising of LFs doesn’t really seem to add much value
BIG TAKEAWAYS (edit: 4/30/19):
Weak supervision is promising; but does not have to be within Snorkel
Snorkel has significant costs (computational efficiency, transparency) that significantly outweigh any benefits for our application (esp. since cue density is so low)
If we had to do it again, we would probably have better spent our time by validating this key assumption first, and if it turned out to false, explore weak supervision outside of the Snorkel framework
Q: What are some useful ways to help people judge the quality of potential analogical matches?
Q: Might entity-matching and verb-matching be a useful way to filter down important bits of discourse segments?
Not for matching, but possible for sensemaking
Q: What signals might be useful to capture for “lit-review profiling” and make available to others?
?

