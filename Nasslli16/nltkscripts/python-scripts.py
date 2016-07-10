# main imports/settings
from nltk import *

# A. collocations
from nltk.collocations import *
bigram_measures = collocations.BigramAssocMeasures()

# Genesis
finder0 = BigramCollocationFinder.from_words(corpus.genesis.words('english-web.txt')) # corpus 0 (from Bible)
finder0.nbest(bigram_measures.pmi, 10)

# Brown corpus
finder1 = BigramCollocationFinder.from_words(corpus.brown.words()) # corpus 1 (multiple-domain texts, see: https://en.wikipedia.org/wiki/Brown_Corpus)
finder1.nbest(bigram_measures.pmi, 10)

# Switchboard corpus
finder2 = BigramCollocationFinder.from_words(corpus.switchboard.words()) # corpus 2 (dialog corpus)
finder2.nbest(bigram_measures.pmi, 10)

# B. frequency
from nltk.book import *

text1 # Moby Dick
text2 # Sense and Sensibility
text4 # inaugural US president speeches

text1.concordance("monstrous") # checks for sentences that contain "monstrous"
text1.similar("monstrous") # distributionally related words
text2.common_contexts(["monstrous", "very"]) # common contexts
text2.collocations() # collocations, again

# dispesion of keywords in text 4
text4.dispersion_plot(["citizens", "democracy", "freedom", "duties", "America"])

# freq distribution of words
fdist0 = FreqDist(text1[:300])
fdist0['whale']
fdist0.max()
fdist0.freq('whale') # rel freq
fdist0.tabulate()
fdist0.plot()
fdist0.plot(cumulative=True)
print(fdist0)
sorted(w for w in set(text1[:300]) if len(w) > 7 and fdist0[w] > 7)

# freq distribution wrt length
fdist1 = FreqDist(len(w) for w in text1[:300])
fdist1[3]
fdist1.max()
fdist1.freq(3) # rel freq
fdist1.tabulate()
fdist1.plot()
fdist1.plot(cumulative=True)
print(fdist1)
sorted(len(n) for n in set(text1[:300]) if len(n) > 3 and fdist0[len(n)] > 3)
