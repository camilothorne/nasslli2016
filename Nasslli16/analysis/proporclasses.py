'''
Created on Jul 29, 2014
@author: camilothorne
'''


import re


# from nltk.corpus import PlaintextCorpusReader
# from nltk.corpus import brown
# from nltk.tag.util import str2tuple
# from nltk.tag import pos_tag
# from nltk import word_tokenize, sent_tokenize
# from nltk.tag import DefaultTagger, UnigramTagger, BigramTagger
# from nltk.tag.sequential import NgramTagger


# Class collecting stats
class MyClass2:


    #fileid:   filename
    #count :   feature occ frequency
    #freq  :   feature occ rel frequency
    #pats  :   set of regexps whose occ we want to check
    #patts :   set of regexps whose occ we want to rule out
    #tag   :   class name tag
    #typ   :   corpus type


    # object constructor
    def __init__(self,pats,patts,fileid,count,freq,tag):


        self.pats = pats
        self.patts = patts
        self.fileid = fileid
        self.count = count
        self.freq = freq
        self.tag = tag


    # check sentence method (no co-occurence)
    def openSen(self,sent,pats,patts):

        pos = 0
        for pa in pats:
            m = re.search(pa, sent)
            if (m != None):
                pos = pos + 1
        self.count = self.count + pos
            

    # check sentence method (co-occurrence)
    def openSen3(self,sent,pats,patts):

            pos = 0
            for pa in pats:
                m = re.search(pa, sent)
                if (m != None):
                    for paa in patts:
                        mm = re.search(paa, sent)
                        if (mm != None):
                            pos = pos + 1
            self.count = self.count + pos


    # check sentence method (exclusion, to ensure dijointeness)
    def openSen2(self,sent,pats,patts):

            pos = 0
            for pa in pats:
                m = re.search(pa, sent)
                if (m != None):
                    if len(patts)==0:
                        pos = pos + 1
                    else:
                        for paa in patts:
                            mm = re.search(paa, sent)
                            if (mm == None):
                                pos = pos + 1
            self.count = self.count + pos


    # check sent method-analysis (all patterns)
    def openFileAll(self,sent,pats,patts):
 
                pos = 0
                for pa in pats:
                    m = re.search(pa, sent)
                    if m:
                        for paa in patts:
                            mm = re.search(paa, sent)
                            if mm:
                                pos = pos + 1
                self.count = self.count + pos
                
                
####################################################################   


# Class encapsulating lists of patterns
class MyPatts2:


        #P : list of regular expressions
        P = []


        # constructor
        def __init__(self,S):
            B = []
            for s in S:
                B.append(s)
            self.P = B


####################################################################


# Class encapsulating all the class stats
class MyClassStats2:


    #classes:    list of classes
    #avg:        average
    #tag:        class tag
    #typ:        corpus subset


    # constructor
    def __init__(self,tag,classes,avg,tit):
        self.tag = tag
        self.classes = classes
        self.avg = avg
        self.fre = 0
        self.tit = tit
