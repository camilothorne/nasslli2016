#==================#
#==================#
#                  #
#    Word          #  
#   Distributions  # 
#                  #
#==================#
#==================#


from __future__ import division
from nltk.corpus import PlaintextCorpusReader
from nltk.probability import FreqDist
import string, re, array
from string import append
from matplotlib import pylab
from numpy import *

# Class generating word frequency plots

class MyStats:
    
    # object constructor
    def __init__(self,corpus,patt,n):
        self.corpus = corpus
        self.patt = patt
        self.n = n
        self.my_bar(corpus, patt, n)
        
    # initializing the bar plot:
    def my_bar(self,corpus,patt,n):
        wordlists = PlaintextCorpusReader(corpus,patt)
        fileids = wordlists.fileids()
        k = len(fileids)
        fig1 = pylab.figure(1)
        fig2 = pylab.figure(2)
        fig3 = pylab.figure(3)
        fig4 = pylab.figure(4) 
        for id in fileids:
            i = fileids.index(id)+1
            words = wordlists.words(id)
            fre = FreqDist(word.lower() for word in words if word.isalpha())
            self.bar_per(fre,n,fig1,2*k,2*i,id)
            self.bar_count(fre,n,fig2,2*k,2*i,id)
            self.bar_freq(fre,n,fig3,2*k,2*i,id)
        fig4 = self.plot_cfreq(corpus,patt,n)
        pylab.show()
    
    # plotting word counts:
    def bar_count(self,fre,n,fig,k,i,id):
        words = fre.keys()[:n]
        freqs = [] # y axis (counts)
        # x axis given by words!
        for word in words:
            freqs.append(fre[word])
        ax = fig.add_subplot(k,1,i)
        ind = pylab.arange(len(freqs))
        width = 1
        ax.bar(ind,freqs,width,facecolor='blue')
        ax.set_ylabel('Freq\n',fontstyle='italic',fontsize='10')
        ax.set_xlabel('\nWord',fontstyle='italic',fontsize='10')
        ax.set_title('Word frequencies: '+ id +' (top ' + `n` + ' words)\n',fontstyle='italic',fontsize='12')
        max = fre[fre.max()]
        ax.axis([0,len(words),0,max])
        tags = []
        for c in range(len(words)):
            tags.append(width+c)
        ax.set_xticks(tags)
        ax.set_xticklabels(words,size='10')
        ax.grid(True)

    # plotting word frequencies:   
    def bar_freq(self,fre,n,fig,k,i,id):
        words = fre.keys()[:n]
        freqs = []
        for word in words:
            freqs.append(fre.freq(word))
        ax = fig.add_subplot(k,1,i)
        ind = pylab.arange(len(freqs))
        width = 1
        ax.bar(ind,freqs,width,facecolor='blue')
        ax.set_ylabel('Rel freq',fontstyle='italic',fontsize='10')
        ax.set_xlabel('Word',fontstyle='italic',fontsize='10')
        ax.set_title('Rel frequency: '+ id +' (top ' + `n` + ' words)',fontstyle='italic',fontsize='12')
        #max = fre.freq(fre.max())
        max = 0.2
        ax.axis([0,len(words),0,max])
        tags = []
        for c in range(len(words)):
            tags.append(width+c)
        ax.set_xticks(tags)
        ax.set_xticklabels(words,size='10')
        ax.grid(True)
    
    # plotting word precentages:   
    def bar_per(self,fre,n,fig,k,i,id):
        words = fre.keys()[:n]
        freqs = []
        for word in words:
            freqs.append(100*fre.freq(word))
        ax = fig.add_subplot(k,1,i)
        ind = pylab.arange(len(freqs))
        width = 1
        ax.bar(ind,freqs,width,facecolor='blue')
        ax.set_ylabel('Per',fontstyle='italic',fontsize='10')
        ax.set_xlabel('Word',fontstyle='italic',fontsize='10')
        ax.set_title('Percentages: '+ id +' (top ' + `n` + ' words)',fontstyle='italic',fontsize='12')
        #max = 100*fre.freq(fre.max())+1
        max = 15
        ax.axis([0,len(words),0,max])
        tags = []
        for c in range(len(words)):
            tags.append(width+c)
        ax.set_xticks(tags)
        ax.set_xticklabels(words,size='10')
        ax.grid(True)

    # plots the top n most common words
    def plot_freq(self,corpus,patt,n):
        wordlists = PlaintextCorpusReader(corpus,patt)
        fileids = wordlists.fileids()
        words = []
        for id in fileids:
            words = append(words,wordlists.words(id))
        fre = FreqDist(word.lower() for word in words if word.isalpha())
        fre.tabulate(n)
        return fre.plot(n)
    
    # plots the cumul freq of top n most common words
    def plot_cfreq(self,corpus,patt,n):
        wordlists = PlaintextCorpusReader(corpus,patt)
        fileids = wordlists.fileids()
        for id in fileids:
            words = wordlists.words(id)
            fre = FreqDist(word.lower() for word in words if word.isalpha()) 
        return fre.plot(n,cumulative=True)

    # saves some stats regarding top n words in a file
    def my_count(self,corpus,patt,n,filename):
        wordlists = PlaintextCorpusReader(corpus,patt)
        fileids = wordlists.fileids()
        res = []
        for id in fileids:    
            leng = len(wordlists.words(id))
            wordc = len(set(wordlists.words(id)))
            wor = "=> num corpus words: " + `leng`
            dis = "=> num distinct words: " + `wordc`
            ric = "=> ind lex richness: " + `leng / wordc`
            res.append(dis)
            res.append(ric)
            res.append(wor)
            for word in sorted(set(wordlists.words(id))):
                freq = (wordlists.words(id)).count(word)
                f = "(" + word.lower() + "," + `round(100 * (freq / leng),1)` + ")"
                t = "(" + word.lower() + "," + `freq` + "/" + `leng` + ")"
                res.append(f)
                res.append(t)
        out = open("/home/camilo/"+filename,"w")
        try:
            for t in res[:n]:
                out.write(t + "\n")
        finally:
            out.close()
