#==================#
#==================#
#                  #
#    Lexical       #  
#   Statistics     # 
#                  #
#==================#
#==================#


from __future__ import division
from nltk.corpus import PlaintextCorpusReader
from nltk.probability import *
import string, re, array
from matplotlib import pylab
from numpy import *
from decimal import *


# Class generating word frequency plots


class MyStats:

    
    # object constructor
    def __init__(self,corpus,patt,n):
        self.corpus = corpus
        self.patt = patt
        self.n = n
        self.print_my_count(corpus, patt, n)
        self.my_bar(corpus, patt, n)

        
    # initializing the bar plot:
    def my_bar(self,corpus,patt,n):
        wordlists = PlaintextCorpusReader(corpus,patt)
        fileids = wordlists.fileids()
        k = len(fileids)
        figA = pylab.figure(1)
        figB = pylab.figure(2)
        li = ['Brown corpus']
        for id in fileids:
            if k > 1:
                i = fileids.index(id)+1
                words = wordlists.words(id)
                fre = FreqDist(word.lower() for word in words if word.isalpha())
                self.bar_count(fre,n,figA,2*k,2*i,id,li)
                self.bar_freq(fre,n,figB,2*k,2*i,id,li)
                figA.savefig('/home/camilo/Desktop/complex-freq.pdf')
                figB.savefig('/home/camilo/Desktop/complex-relfreq.pdf')
            else:
                words = wordlists.words(id)
                fre = FreqDist(word.lower() for word in words if word.isalpha())
                self.bar_count(fre,n,figA,k,1,id,li)
                self.bar_freq(fre,n,figB,k,1,id,li)
                figA.savefig('/home/camilo/Desktop/simple-freq.pdf')
                figB.savefig('/home/camilo/Desktop/simple-relfreq.pdf')             
        pylab.show()

    
    # plotting word counts:
    def bar_count(self,fre,n,fig,k,i,id,li):
        words = fre.keys()[:n]
        freqs = []
        for word in words:
            freqs.append(fre[word])
        ax = fig.add_subplot(k,1,i)
        ind = pylab.arange(len(freqs))
        width = 1
        ax.bar(ind,freqs,width,facecolor='gray')
        ax.set_title('Word frequencies (top ' + `n` + ' words)\n\n',
                     fontstyle='normal',fontsize='12')
        max = fre[fre.max()]
        ax.axis([0,len(words),0,max])
        tags = []
        for c in range(len(words)):
            tags.append(width+c)
        ax.set_xticks(tags)
        self.plotticks(ax,words)
        ax.grid(False)
        self.plotLegend(ax, li)


    # plotting word frequencies:   
    def bar_freq(self,fre,n,fig,k,i,id,li):
        words = fre.keys()[:n]
        freqs = []
        for word in words:
            freqs.append(fre.freq(word))
        ax = fig.add_subplot(k,1,i)
        ind = pylab.arange(len(freqs))
        width = 1
        ax.bar(ind,freqs,width,facecolor='gray')
        ax.set_title('Word relative frequencies (top ' + `n` + ' words)\n\n',
                     fontstyle='normal',fontsize='12')
        max = fre.freq(fre.max())
        ax.axis([0,len(words),0,max])
        tags = []
        for c in range(len(words)):
            tags.append(width+c)
        ax.set_xticks(tags)
        self.plotticks(ax,words)
        ax.grid(False)
        self.plotLegend(ax, li)

    
    # plotting word percentages:   
    def bar_per(self,fre,n,fig,k,i,id,li):
        words = fre.keys()[:n]
        freqs = []
        for word in words:
            freqs.append(100*fre.freq(word))
        ax = fig.add_subplot(k,1,i)
        ind = pylab.arange(len(freqs))
        width = 1
        ax.bar(ind,freqs,width,facecolor='gray')
        ax.set_title('Percentages (top ' + `n` + ' words)\n\n',
                     fontstyle='normal',fontsize='12')
        max = 100*(fre.freq(fre.max())) +1
        ax.axis([0,len(words),0,max])
        tags = []
        for c in range(len(words)):
            tags.append(width+c)
        ax.set_xticks(tags)
        self.plotticks(ax,words)
        ax.grid(False)
        self.plotLegend(ax, li)


    # plots the top n most common words
    def plot_freq(self,corpus,patt,n):
        wordlists = PlaintextCorpusReader(corpus,patt)
        fileids = wordlists.fileids()
        for id in fileids:
            words = wordlists.words(id)
            fre = FreqDist(word.lower() for word in words if word.isalpha())
        return fre.plot(n)

    
    # plots the cumul freq of top n most common words
    def plot_cfreq(self,corpus,patt,n):
        wordlists = PlaintextCorpusReader(corpus,patt)
        fileids = wordlists.fileids()
        for id in fileids:
            words = wordlists.words(id)
            fre = FreqDist(word.lower() for word in words if word.isalpha()) 
        return fre.plot(n,cumulative=True)


    # prints some stats regarding top n words in a file
    def print_my_count(self,corpus,patt,n):
        wordlists = PlaintextCorpusReader(corpus,patt)
        fileids = wordlists.fileids()
        for id in fileids:
            words = wordlists.words(id)   
            wordt = len(words)
            wordc = len(set(words))
            wor = "=> corpus tokens : " + `wordt`
            dis = "=> distinct token types : " + `wordc`
            ric = "=> ind lex richness : " + `wordt / wordc`
            print "********************************************"
            print "1. Corpus parameters", "(= "+id+")"
            print "********************************************"
            print dis
            print ric
            print wor
            print "********************************************"
            fre = FreqDist(word.lower() for word in words if word.isalpha())
            print "2. Top 100 words"
            print "********************************************"
            for word in fre.keys()[:n]:
                t = word, `fre[word]` + "/" + `wordt`
                print t


    # saves some stats regarding top n words in a file
    def save_my_count(self,corpus,patt,n,filename):
        wordlists = PlaintextCorpusReader(corpus,patt)
        fileids = wordlists.fileids()
        res = []
        for id in fileids:    
            leng = len(wordlists.words(id))
            wordc = len(set(wordlists.words(id)))
            wor = "=> corpus tokens: " + `leng` + "\n"
            dis = "=> corpus token types: " + `wordc` + "\n"
            ric = "=> ind lex richness: " + `leng / wordc` + "\n"
            res.append(dis)
            res.append(ric)
            res.append(wor)
            for word in sorted(set(wordlists.words(id))):
                freq = (wordlists.words(id)).count(word)
                f = "(" + word.lower() + "," + `round(100 * (freq / leng),1)` + ")\n"
                t = "(" + word.lower() + "," + `freq` + "/" + `leng` + ")"
                res.append(f)
                res.append(t)
        out = open("/home/camilo/"+filename,"w")
        try:
            for t in res[:n]:
                out.write(t + "\n")
        finally:
            out.close()


    # plotting the tags of the x/y axis (rel freqs)       
    def plotticksFloat(self,ax,words,freq):
        freq.append(0)
        freq.sort()
        myf = [float(Decimal("%.2f" % e)) for e in freq]
        ax.set_xticklabels(words,rotation='90')
        ax.set_yticklabels(myf)


    # plotting the tags of the x/y axis (freqs)       
    def plotticks(self,ax,words):
        ax.set_xticklabels(words,rotation='90')


    # plotting the legend            
    def plotLegend(self,ax,li):
        leg = ax.legend(li,shadow=True,loc='upper right')
        frame  = leg.get_frame()
        frame.set_facecolor('1.0')       # set the frame face color to white
        for t in leg.get_texts():
            t.set_fontsize('medium')      # the legend text fontsize
        for l in leg.get_lines():
            l.set_linewidth(1.5)  