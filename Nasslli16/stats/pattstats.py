#===================#
#===================#
#                   #
# Class likelihoods #
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


#################################################################### 

s0 = ".*"        # anything!

####################################################################

s10 = "( some | Some | some/| Some/)"

s11 = " some "    # exists
s12 = " Some "    # exists
s13 = " some/"    # exists
s14 = " Some/"    # exists

s15 = " a "       # exists
s16 = " A "       # exists
s17 = " a/"       # exists
s18 = " A/"       # exists

####################################################################

s20 = "( and | And | and/| And/| that | That | that/| That/| which | Which | which/| Which/|)"

s21 = " and "     # intersection
s22 = " And "     # intersection
s23 = " and/"     # intersection
s24 = " And/"     # intersection

s25 = " that "    # intersection
s26 = " That "    # intersection
s27 = " that/"    # intersection
s28 = " That/"    # intersection

s2a = " which "   # intersection
s2b = " Which "   # intersection
s2c = " which/"   # intersection
s2d = " Which/"   # intersection

####################################################################

s30 = "( or | Or | or/| Or/)"

s31 = " or "     # union
s32 = " Or "     # union
s33 = " or/"     # union
s34 = " Or/"     # union

####################################################################

s40 = "( every | Every | every/| Every/| the | The | the/| The/| all | All | all/| All/)"

s41 = " every "      # for all
s42 = " Every "      # for all
s43 = " every/"      # for all
s44 = " Every/"      # for all

s45 = " the "        # for all
s46 = " The "        # for all
s47 = " the/"        # for all
s48 = " The/"        # for all

s4a = " all "       # for all
s4b = " All "       # for all
s4c = " all/"       # for all
s4d = " All/"       # for all

####################################################################

s50 = "( not | Not | not/| Not/)"

s51 = " not "       # complement
s52 = " Not "       # complement
s53 = " not/"       # complement
s54 = " Not/"       # complement

####################################################################


# Class encoding the plot


class PattStats:
   
    
    # corpus       : path to corpora
    # format       : format of corpora (e.g. .txt files)
    # stats        : hash table with class stats of each corpus
    # classstats   : list with global stats (mean frequency) 
    
    
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
        # computing relative frequencies
        self.fileStats(path,fileids)
        # plotting
        MyPlot(self.stats,self.classstats,"patterns","one") 
            
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
        print "2. PATTERN STATS"
        print ""
        print "==================================================="
        print "###################################################" 
        # computing the stats
        for id in fileids:
            filestats = []
            #id = id+".test"
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
            exists = [s0,s20]
            rest1 = [s31,s32,s33,s34,
                     s41,s42,s43,s44,s45,s46,s47,s48,s4a,s4b,s4c,s4d,
                     s51,s52,s53,s54]
            P1 = MyPatts(exists).P
            N1 = MyPatts(rest1).P
            c1 = MyClass(P1,N1,id,0,0,"some+\nand")
            c1.openFile(path+"/"+id,c1.pats,c1.patts)
            ####################################################################
            # class 2 (exists+intersection+union)
            existsor = [s0,s20,s30]
            rest2 = [s41,s42,s43,s44,s45,s46,s47,s48,s4a,s4b,s4c,s4d,
                     s51,s52,s53,s54]
            P2 = MyPatts(existsor).P
            N2 = MyPatts(rest2).P       
            c2 = MyClass(P2,N2,id,0,0,"some+\nand+\nor")
            c2.openFile(path+"/"+id,c2.pats,c2.patts)
            ####################################################################
            # class 3 (exists+intersection+every)
            existsall = [s0,s20,s40]
            rest3 = [s31,s32,s33,s34,
                     s51,s52,s53,s54]
            P3 = MyPatts(existsall).P
            N3 = MyPatts(rest3).P
            c3 = MyClass(P3,N3,id,0,0,"some+\nand+\nall")
            c3.openFile(path+"/"+id,c3.pats,c3.patts)
            ####################################################################
            # class 5 (exists+intersection+complement)
            existsnot = [s0,s20,s50]
            rest4 = [s31,s32,s33,s34,
                     s41,s42,s43,s44,s45,s46,s47,s48,s4a,s4b,s4c,s4d]
            P5 = MyPatts(existsnot).P
            N5 = MyPatts(rest4).P
            c5 = MyClass(P5,N5,id,0,0,"some+\nand+\nnot")
            c5.openFile(path+"/"+id,c5.pats,c5.patts)
            ####################################################################
            # class 6 (exists+intersection+union+every)
            existsallor = [s0,s20,s30,s40]
            rest5 = [s51,s52,s53,s54]
            P6 = MyPatts(existsallor).P
            N6 = MyPatts(rest5).P
            c6 = MyClass(P6,N6,id,0,0,"some+\nand+\nor+all")
            c6.openFile(path+"/"+id,c6.pats,c6.patts)
            ####################################################################
            # class 7 (every+complement)
            allnot = [s40,s50]
            rest6 = [s11,s12,s13,s14,s15,s16,s17,s18,
                     s31,s32,s33,s34,
                     s21,s22,s23,s24,s25,s26,s27,s28,s2a,s2b,s2c,s2d]
            P7 = MyPatts(allnot).P
            N7 = MyPatts(rest6).P
            c7 = MyClass(P7,N7,id,0,0,"not+\nall")
            c7.openFile(path+"/"+id,c7.pats,c7.patts)
            ####################################################################           
            # class 8 (exists+intersection+complement+every)
            existsnotall = [s0,s20,s40,s50]
            rest7 = [s31,s32,s33,s34]
            P8 = MyPatts(existsnotall).P
            N8 = MyPatts(rest7).P
            c8 = MyClass(P8,N8,id,0,0,"some+\nand+\nnot+all")
            c8.openFile(path+"/"+id,c8.pats,c8.patts)
            ####################################################################            
            # class 10 (exists+intersection+every+complement+union)
            allpats = [s0,s20,s30,s40,s50]
            P10 = MyPatts(allpats).P
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
        
           
