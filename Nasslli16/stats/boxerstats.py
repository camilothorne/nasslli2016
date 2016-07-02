#===================#
#===================#
#                   #
# Class Statistics  #
#                   #
#===================#
#===================#


from __future__ import division
from nltk.corpus import PlaintextCorpusReader
import string, re, array
from matplotlib import pylab, cm
from numpy import *
from subprocess import call
from operator import itemgetter, attrgetter
import scipy

from statsplot import MyPlot
from classes import MyClass, MyPatts, MyClassStats
from statstests import STest


# (Global) Patterns/features
# notice that we disregard non-FO semantics


#####################################  
s0 = ".*"                                     # anything!
#####################################
s1 = "some\(.*\)"                             # exists
#####################################
s2 = "and\(.*\)"                              # intersection
#####################################
s3 = "or\(.*\)"                               # union
#####################################
s4 = "all\(.*\)"                              # for all
#####################################
s5 = "not\(.*\)"                              # complement
#####################################


# Class encoding the plot
class BoxerStats:
    
    
    # corpus       : path to corpora
    # format       : format of corpora (e.g. .txt files)
    # stats        : hash table with the class stats of each corpus
    # classstats   : list with the global class stats (with mean frequency) 
    
    
    # object constructor
    def __init__(self,path,format):
        self.stats = {}
        self.classstats = []
        self.path = path
        self.format = format
        self.occStats(path,format)
        self.statTest(self.classstats)
     
            
    # collecting statistics
    def occStats(self,path,format):
        wordlists = PlaintextCorpusReader(path,format)
        fileids = wordlists.fileids()
        k = len(fileids)
        # parsing the corpora
        self.parseCorpora(path,fileids)
        # computing relative frequencies
        self.fileStats(path,fileids)
        # plotting
        MyPlot(self.stats,self.classstats,"Boxer","one") 
    
           
    # computes the FO MRs of the corpus sentences
    # (this function is quite ...slow!)
    def parseCorpora(self,path,fileids):
        fileids2 = []
        words1 = PlaintextCorpusReader(path,".*ccg")
        words2 = PlaintextCorpusReader(path,".*fol")
        for file in words1.fileids():
            fileids2.append(file)
        for file in words2.fileids():
            fileids2.append(file)
        for id in fileids:
            if id+".ccg" not in fileids2:
                # parsing the corpora
                call(["/usr/local/candc/bin/candc","--models","/home/camilo/models-boxer/boxer",
                  "--input",path+"/"+id,"--output",path+"/"+id+".ccg"])
            """
            if id+".fol" not in fileids2:
                # generating the meaning representations         
                call(["/usr/local/candc/bin/boxer","--input",path+"/"+id+".ccg",
                  "--semantics","fol","--output",path+"/"+id+".fol"])
            """

    # creating the classes
    def fileStats(self,path,fileids):
        # stat classes
        C1 = MyClassStats("some+\nand",[],0)
        C2 = MyClassStats("some+\nand+\nor",[],0)
        C3 = MyClassStats("some+\nand+\nall",[],0)
        C5 = MyClassStats("some+\nand+\nnot",[],0)
        C6 = MyClassStats("some+\nand+\nor+all",[],0)   
        C7 = MyClassStats("not+\nall",[],0)        
        C8 = MyClassStats("some+\nand+\nnot+all",[],0)
        C10 = MyClassStats("some+\nand+\nnot+or+all",[],0)
        self.classstats = [C1,C2,C3,C5,C6,C7,C8,C10]
        print "###################################################"
        print "==================================================="
        print ""
        print "1. BOXER STATS"
        print ""
        print "==================================================="
        print "###################################################" 
        # computing the stats
        for id in fileids:
            filestats = []
            id = id+".fol"
            ####################################################################
            #corpus
            PC = MyPatts([s0]).P
            corpus = MyClass(PC,[],id,0,0,"corpus")
            corpus.openFile(path+"/"+id,corpus.pats,corpus.patts)
            ####################################################################         
            print id + " is of size : " + `corpus.count` + " sentences"
            print "###################################################"
            ####################################################################
            # class 1 (exists+intersection)
            P1 = MyPatts([s1,s2]).P
            N1 = MyPatts([s3,s4,s5]).P
            c1 = MyClass(P1,N1,id,0,0,"some+\nand")
            c1.openFile(path+"/"+id,c1.pats,c1.patts)
            ####################################################################
            # class 2 (exists+intersection+union)
            P2 = MyPatts([s1,s2,s3]).P
            N2 = MyPatts([s4,s5]).P       
            c2 = MyClass(P2,N2,id,0,0,"some+\nand+\nor")
            c2.openFile(path+"/"+id,c2.pats,c2.patts)
            ####################################################################
            # class 3 (exists+intersection+every)
            P3 = MyPatts([s1,s2,s4]).P
            N3 = MyPatts([s3,s5]).P
            c3 = MyClass(P3,N3,id,0,0,"some+\nand+\nall")
            c3.openFile(path+"/"+id,c3.pats,c3.patts)
            ####################################################################
            # class 5 (exists+intersection+complement)
            P5 = MyPatts([s1,s2,s5]).P
            N5 = MyPatts([s3,s4]).P
            c5 = MyClass(P5,N5,id,0,0,"some+\nand+\nnot")
            c5.openFile(path+"/"+id,c5.pats,c5.patts)
            ####################################################################
            # class 6 (exists+intersection+union+every)
            P6 = MyPatts([s1,s2,s3,s4]).P
            N6 = MyPatts([s5]).P
            c6 = MyClass(P6,N6,id,0,0,"some+\nand+\nor+all")
            c6.openFile(path+"/"+id,c6.pats,c6.patts)
            ####################################################################
            # class 7 (every+complement)
            P7 = MyPatts([s5,s4]).P
            N7 = MyPatts([s1,s2,s3]).P
            c7 = MyClass(P7,N7,id,0,0,"not+\nall")
            c7.openFile(path+"/"+id,c7.pats,c7.patts)
            ####################################################################           
            # class 8 (exists+intersection+complement+every)
            P8 = MyPatts([s1,s2,s5,s4]).P
            N8 = MyPatts([s3]).P
            c8 = MyClass(P8,N8,id,0,0,"some+\nand+\nnot+all")
            c8.openFile(path+"/"+id,c8.pats,c8.patts)
            ####################################################################            
            # class 10 (exists+intersection+every+complement+union)
            P10 = MyPatts([s1,s2,s5,s3,s4]).P
            N10 = MyPatts([]).P
            c10 = MyClass(P10,N10,id,0,0,"some+\nand+\nnot+or+all")
            c10.openFile(path+"/"+id,c10.pats,c10.patts)
            ####################################################################                  
            c1.freq = (c1.count/corpus.count)
            c2.freq = (c2.count/corpus.count)
            c3.freq = (c3.count/corpus.count)
            c5.freq = (c5.count/corpus.count)        
            c6.freq = (c6.count/corpus.count)
            c7.freq = (c7.count/corpus.count)
            c8.freq = (c8.count/corpus.count)
            c10.freq = (c10.count/corpus.count)
            ####################################################################  
            filestats = [c1,c2,c3,c5,c6,c7,c8,c10]
            self.stats[id] = filestats
            for aclass in self.classstats:
                for thiscls in filestats:
                    if (thiscls.tag == aclass.tag):
                        aclass.classes.append(thiscls)
        self.classAvg(self.classstats)
        self.classAvg2(self.classstats)
        sort = self.sortClass(self.classstats)
        self.classstats = sort
        self.printClasses(self.classstats)
        
                
    # sorts stats classes
    def sortClass(self,classlist):
        sort = sorted(classlist,key=attrgetter('avg'))
        return sort
    
    
    # computes list of averages    
    def classAvg(self,classstats):
        for cla in classstats:
            meanj = 0
            for id in cla.classes:
                meanj = meanj + id.freq
            meanj = (meanj/len(cla.classes))
            cla.avg = meanj
    
    
    # computes list of frequencies    
    def classAvg2(self,classstats):
        for cla in classstats:
            meanf = 0
            for id in cla.classes:
                meanf = meanf + id.count
            meanf = (meanf/len(cla.classes))
            cla.fre = meanf
 
        
    # prints the stats
    def printClasses(self,classstats):
        for cla in classstats:
            print cla.tag
            print "---------------------------------------------------"            
            print `cla.avg` + ": avg rel. freq"
            print "---------------------------------------------------"
            for id in cla.classes:
                print `id.freq` + ": rel. freq "+ id.fileid
                print `id.count` + ": freq "+ id.fileid              
            print "###################################################"
            
    
    # statistical tests
    def statTest(self,classstats):
        samplef = []
        for cla in classstats:
            samplef.append(cla.fre)
        sampler = []
        for cla in classstats:
            sampler.append(cla.avg)
        STest(sampler,samplef)