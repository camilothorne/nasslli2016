'''
Created on May 23, 2016

@author: camilo
'''


#===================#
#===================#
#
# Pattern likelihoods
#
#===================#
#===================#


# python
from __future__ import division
from operator import attrgetter
#from math import ceil


# my plotting + test classes
from statsplot import MyPlot
from statstests import STest


# nltk
from nltk.corpus import PlaintextCorpusReader


# my classes
from proporclasses import MyClass2, MyPatts2, MyClassStats2
from savestats import SaveStats
from buildsen import *


####################################################################
#################################################################### 

s0 = ".*"        # anything!

####################################################################
# ARISTOTELIAN
####################################################################

# 1. exists

s16     = "( some/dt|some/dt )"

some5 = [s16]

####################################################################

# 4. all

s40     = "( every/dt |every/dt )"
s42     = "( all/dt |all/dt)"
s42a    = "( all/pdt |all/pdt )"
s4c     = "( each/dt [a-z]{1,12}/nn |each/dt [a-z]{1,12}/nn )"
s4e     = "( no/dt |no\dt )"

all1 = [s40]
all2 = [s42]
all3 = [s42a]
all7 = [s4c]
all8 = [s4e]

####################################################################
# COUNTING
####################################################################

# 6. at most k, less than k (k integer)

s60     = "( at/in most/jjs [a-z]{1,12}/cd |at/in most/jjs [a-z]{1,12}/cd )"
s60a    = "( at/in most/rbs [a-z]{1,12}/cd |at/in most/rbs [a-z]{1,12}/cd )"

s20b    = "( less/rbr than/in [a-z]{1,12}/cd |less/rbr than/in [a-z]{1,12}/cd )"
s20bb   = "( less/jjr than/in [a-z]{1,12}/cd |less/jjr than/in [a-z]{1,12}/cd )"

s20c    = "( fewer/jjr than/in [a-z]{1,12}/cd |fewer/jjr than/in [a-z]{1,12}/cd )"

lessk1 = [s20b]
lessk2 = [s20c]
lessk3 = [s60]
lessk4 = [s20bb]
lessk5 = [s20c]

####################################################################

# 7. at least k, more than k (k integer)

s60b     = "( at/in least/jjs [a-z]{1,12}/cd |at/in least/jjs [a-z]{1,12}/cd )"

s20      = "( more/rbr than/in [a-z]{1,12}/cd | more/rbr than/in [a-z]{1,12}/cd )"
s20a     = "( more/jjr than/in [a-z]{1,12}/cd |more/jjr than/in [a-z]{1,12}/cd )"

morek1 = [s20]
morek2 = [s20a]
morek3 = [s60b]

####################################################################
# PROPORTIONAL
####################################################################

# 9. more than p/k (p, k integers)

s80aa   = "( at/in least/jj half/nn |at/in least/jj half/nn )"
s80     = "( more/rbr than/in half/nn |more/rbr than/in half/nn )"
s80a    = "( more/jjr than/in half/nn |more/jjr than/in half/nn )"

s82c    = "( at/in least/jjs [a-z]{1,12}/cd [a-z]{1,12}/nns of/in |at/in least/jjs [a-z]{1,12}/cd [a-z]{1,12}/nns of/in )"

s82     = "( more/rbr than/in [a-z]{1,12}/cd [a-z]{1,12}/nns of/in |more/rbr than/in [a-z]{1,12}/cd [a-z]{1,12}/nns of/in )"
s82a    = "( more/jjr than/in [a-z]{1,12}/cd [a-z]{1,12}/nns of/in |more/jjr than/in [a-z]{1,12}/cd [a-z]{1,12}/nns of/in )"

morethanpro1 = [s80aa]
morethanpro2 = [s80]
morethanpro3 = [s80a]
morethanpro4 = [s82c]
morethanpro5 = [s82]
morethanpro6 = [s82a]

####################################################################

# 9.1 less than p/k (p, k integers)

s80b    = "( less/rbr than/in half/nn |less/rbr than/in half/nn )"
s80bb   = "( fewer/jjr than/in half/nn |fewer/jjr than/in half/nn )"
s80c    = "( at/in most/jjs half/nn |at/in most/jjs half/nn )"

s82b    = "( less/rbr than/in [a-z]{1,12}/cd [a-z]{1,12}/nns of/in |less/rbr than/in [a-z]{1,12}/cd [a-z]{1,12}/nns of/in )"
s82bb   = "( fewer/jjr than/in [a-z]{1,12}/cd [a-z]{1,12}/nns of/in |fewer/jjr than/in [a-z]{1,12}/cd [a-z]{1,12}/nns of/in )"

s80d    = "( at/in most/jjs [a-z]{1,12}/cd [a-z]{1,12}/nns of/in |at/in most/jjs [a-z]{1,12}/cd [a-z]{1,12}/nns of/in )"
s80e    = "( at/in most/rbs [a-z]{1,12}/cd [a-z]{1,12}/nns of/in |at/in most/rbs [a-z]{1,12}/cd [a-z]{1,12}/nns of/in )"

lessthanpro1 = [s80b]
lessthanpro2 = [s80bb]
lessthanpro3 = [s80c]
lessthanpro4 = [s82b]
lessthanpro5 = [s82bb]
lessthanpro6 = [s80d]
lessthanpro7 = [s80e]

####################################################################

# 5. most, more than half

s52     = "( most/rbs [a-z]{1,12}/nns |most/rbs [a-z]{1,12}/nns )"
s51     = "( most/jjs [a-z]{1,12}/nns |most/jjs [a-z]{1,12}/nns )"
s51a    = "( most/dt |most/dt )"

s53     = "( more/rbr than/in half/nn |more/rbr than/in half/nn )"
s53a    = "( more/jjr than/in half/nn |more/jjr than/in half/nn )"

most1 = [s51a]
most2 = [s53]
most3 = [s51]
most4 = [s52]
most5 = [s53a]

nomost = ["( the/dt most/rbs |the/dt most/rbs )", 
          "( the/dt most/jjs |the/dt most/jjs )", 
          "( at/in most/jjs |at/in most/jjs )", 
          "( at/in most/rbs |at/in most/rbs )"]

####################################################################

# 5.1 few, less than half, fewer than half

ss51b   = "( few/jj [a-z]{1,12}/nns |few/jj [a-z]{1,12}/nns )"
s51bb   = "( few/dt |few/dt )"

s53b    = "( less/rbr than/in half/nn |less/rbr than/in half/nn )"
s53bb   = "( fewer/jjr than/in half/nn |fewer/jjr than/in half/nn )"

few1 = [s51bb]
few2 = [s53b]
few3 = [s53bb]
few4 = [ss51b]

nofew = ["( a/dt few/jj |a/dt few/jj )", 
         "( the/dt few/jj |the/dt few/jj )"]


####################################################################
####################################################################


# Class encoding the plot(s) + test(s)


class ProporStatsPD:
   
    
    # corpus            : path to corpora
    # format            : format of corpora (e.g. .txt files)
    # stats             : hash table with class stats of each corpus
    # classstats        : list with global stats (mean frequency) 
    # list              : list of legends in figure
    # plotting          : directory of compiled report

    
    # object constructor
    def __init__(self,path,myformat,mylist,plotting):
        self.stats = {} # stats
        self.classstats = [] # classes
        self.path = path # path of corpus
        self.format = myformat # format of file(s)
        self.list = mylist        
        self.occStats(path,myformat,self.list,plotting) # collects stats + plots them
        self.statTestB(self.classstats) # runs the stat tests
        self.plotting = plotting    

    
    #############################################################
    #############################################################
        
    
    # collecting statistics
    def occStats(self,path,format,list,plotting):
        wordlists = PlaintextCorpusReader(path,format)
        fileids = wordlists.fileids()
        k = len(fileids)
        
        # computing frequencies
        self.fileStats(path,fileids)
        
        # save stats
        statsname = "Base GQs (disjoint patterns)"
        savpath = plotting +'/'+ statsname.replace(' ', '-')
        
        # generating report
        SaveStats(self.classstats,self.stats,"",savpath,plotting) # all
        
        
    #############################################################
    #############################################################        
 
            
    # creating the classes
    def fileStats(self,path,fileids):
                
        # starting the title
        tit = "Base GQs (disjoint patterns)"
        
        # all
        C11  =   MyClassStats2(all1[0].strip(),[],0,tit)
        C12  =   MyClassStats2(all2[0].strip(),[],0,tit)
        C13  =   MyClassStats2(all3[0].strip(),[],0,tit)
        C17  =   MyClassStats2(all7[0].strip(),[],0,tit)
        C18  =   MyClassStats2(all8[0].strip(),[],0,tit)                              
        
        # some
        C25  =   MyClassStats2(some5[0].strip(),[],0,tit)     
        
        # > k
        C41 =    MyClassStats2(morek1[0].strip(),[],0,tit)
        C42 =    MyClassStats2(morek2[0].strip(),[],0,tit)
        C43 =    MyClassStats2(morek3[0].strip(),[],0,tit)        
        
        # < k
        C51 =    MyClassStats2(lessk1[0].strip(),[],0,tit)
        C52 =    MyClassStats2(lessk2[0].strip(),[],0,tit)
        C53 =    MyClassStats2(lessk3[0].strip(),[],0,tit)      
        C54 =    MyClassStats2(lessk4[0].strip(),[],0,tit)
        C55 =    MyClassStats2(lessk5[0].strip(),[],0,tit) 
        
        # most
        C71 =    MyClassStats2(most1[0].strip(),[],0,tit)
        C72 =    MyClassStats2(most2[0].strip(),[],0,tit)
        C73 =    MyClassStats2(most3[0].strip(),[],0,tit)
        C74 =    MyClassStats2(most4[0].strip(),[],0,tit)
        C75 =    MyClassStats2(most5[0].strip(),[],0,tit)
        
        # few
        C81 =    MyClassStats2(few1[0].strip(),[],0,tit)
        C82 =    MyClassStats2(few2[0].strip(),[],0,tit)
        C83 =    MyClassStats2(few3[0].strip(),[],0,tit)
        C84 =    MyClassStats2(few4[0].strip(),[],0,tit)
        
        # > p/k
        C91 =    MyClassStats2(morethanpro1[0].strip(),[],0,tit)    
        C92 =    MyClassStats2(morethanpro2[0].strip(),[],0,tit)    
        C93 =    MyClassStats2(morethanpro3[0].strip(),[],0,tit)    
        C94 =    MyClassStats2(morethanpro4[0].strip(),[],0,tit)                 
        C95 =    MyClassStats2(morethanpro5[0].strip(),[],0,tit)  
        C96 =    MyClassStats2(morethanpro6[0].strip(),[],0,tit)          
        
        # < p/k
        C101 =   MyClassStats2(lessthanpro1[0].strip(),[],0,tit)
        C102 =   MyClassStats2(lessthanpro2[0].strip(),[],0,tit)
        C103 =   MyClassStats2(lessthanpro3[0].strip(),[],0,tit)
        C104 =   MyClassStats2(lessthanpro4[0].strip(),[],0,tit)      
        C105 =   MyClassStats2(lessthanpro5[0].strip(),[],0,tit)
        C106 =   MyClassStats2(lessthanpro6[0].strip(),[],0,tit)
        C107 =   MyClassStats2(lessthanpro7[0].strip(),[],0,tit) 
        
        self.classstats = [
                           C11,C12,C13,C17,C18,
                           C25,
                           C41,C42,C43,
                           C51,C52,C53,C54,C55,                         
                           C71,C72,C73,C74,C75,
                           C81,C82,C83,C84,
                           C91,C92,C93,C94,C95,C96,
                           C101,C102,C103,C104,C105,C106,C107
                           ]        
        
        print "###################################################"
        print "GQ STATS"
        print "###################################################"
        
        # computing the stats
        for idf in fileids:
                        
            ####################################################################
            
            filestats = []
            mydata = OpenFile(path+'/'+idf)
            mydata.lines = mydata.myread()
            
            ####################################################################
            
            #print "==================================================="
            print idf
            print "==================================================="
            
            ####################################################################
 
            # patterns
            rest    = []
            
            # digits
            digit   = [" @card@/cd "]
            
            # corpus
            corpus  = MyClass2([".*"],[],idf,0,0,"corpus")
            
            ####################################################################  
            
            # all
            P11 = MyPatts2(all1).P
            N11 = MyPatts2(rest).P
            c11 = MyClass2(P11,N11,idf,0,0,all1[0].strip())
            
            P12 = MyPatts2(all2).P
            N12 = MyPatts2(rest).P
            c12 = MyClass2(P12,N12,idf,0,0,all2[0].strip())

            P13 = MyPatts2(all3).P
            N13 = MyPatts2(rest).P
            c13 = MyClass2(P13,N13,idf,0,0,all3[0].strip())
            
            P17 = MyPatts2(all7).P
            N17 = MyPatts2(rest).P
            c17 = MyClass2(P17,N17,idf,0,0,all7[0].strip()) 
            
            P18 = MyPatts2(all8).P
            N18 = MyPatts2(rest).P
            c18 = MyClass2(P18,N18,idf,0,0,all8[0].strip())                                                                  
            
            # some         
            P25 = MyPatts2(some5).P
            N25 = MyPatts2(rest).P           
            c25 = MyClass2(P25,N25,idf,0,0,some5[0].strip())                            
            
            ####################################################################                
            
            # >k
            P41 = MyPatts2(morek1).P
            N41 = MyPatts2(digit).P
            c41 = MyClass2(P41,N41,idf,0,0,morek1[0].strip())                      

            P42 = MyPatts2(morek2).P
            N42 = MyPatts2(digit).P
            c42 = MyClass2(P42,N42,idf,0,0,morek2[0].strip())  
            
            P43 = MyPatts2(morek3).P
            N43 = MyPatts2(digit).P
            c43 = MyClass2(P43,N43,idf,0,0,morek3[0].strip())                         
            
            # <k
            P51 = MyPatts2(lessk1).P
            N51 = MyPatts2(digit).P
            c51 = MyClass2(P51,N51,idf,0,0,lessk2[0].strip())

            P52 = MyPatts2(lessk2).P
            N52 = MyPatts2(digit).P
            c52 = MyClass2(P52,N52,idf,0,0,lessk2[0].strip())

            P53 = MyPatts2(lessk3).P
            N53 = MyPatts2(digit).P
            c53 = MyClass2(P53,N53,idf,0,0,lessk3[0].strip())                      

            P54 = MyPatts2(lessk4).P
            N54 = MyPatts2(digit).P
            c54 = MyClass2(P54,N54,idf,0,0,lessk4[0].strip())

            P55 = MyPatts2(lessk5).P
            N55 = MyPatts2(digit).P
            c55 = MyClass2(P55,N55,idf,0,0,lessk5[0].strip())  
            
            ####################################################################
            
            # most
            P71 = MyPatts2(most1).P
            N71 = MyPatts2(nomost+lessthanpro6+lessthanpro7+lessthanpro3+lessk1+lessk2).P
            c71 = MyClass2(P71,N71,idf,0,0,most1[0].strip())
            
            P72 = MyPatts2(most2).P
            N72 = MyPatts2(nomost+lessthanpro6+lessthanpro7+lessthanpro3+lessk1+lessk2).P
            c72 = MyClass2(P72,N72,idf,0,0,most2[0].strip())
                        
            P73 = MyPatts2(most3).P
            N73 = MyPatts2(nomost+lessthanpro6+lessthanpro7+lessthanpro3+lessk1+lessk2).P
            c73 = MyClass2(P73,N73,idf,0,0,most3[0].strip())
            
            P74 = MyPatts2(most4).P
            N74 = MyPatts2(nomost+lessthanpro6+lessthanpro7+lessthanpro3+lessk1+lessk2).P
            c74 = MyClass2(P74,N74,idf,0,0,most4[0].strip())
            
            P75 = MyPatts2(most5).P
            N75 = MyPatts2(nomost+lessthanpro6+lessthanpro7+lessthanpro3+lessk1+lessk2).P
            c75 = MyClass2(P75,N75,idf,0,0,most5[0].strip())            
                             
            # few
            P81 = MyPatts2(few1).P
            N81 = MyPatts2(nofew).P
            c81 = MyClass2(P81,N81,idf,0,0,few1[0].strip())

            P82 = MyPatts2(few2).P
            N82 = MyPatts2(nofew).P
            c82 = MyClass2(P82,N82,idf,0,0,few2[0].strip())

            P83 = MyPatts2(few3).P
            N83 = MyPatts2(nofew).P
            c83 = MyClass2(P83,N83,idf,0,0,few3[0].strip())

            P84 = MyPatts2(few4).P
            N84 = MyPatts2(nofew).P
            c84 = MyClass2(P84,N84,idf,0,0,few4[0].strip())
                
            # >p/k
            P91 = MyPatts2(morethanpro1).P
            N91 = MyPatts2(digit).P
            c91 = MyClass2(P91,N91,idf,0,0,morethanpro1[0].strip())                    
 
            P92 = MyPatts2(morethanpro2).P
            N92 = MyPatts2(digit).P
            c92 = MyClass2(P92,N92,idf,0,0,morethanpro2[0].strip())   
 
            P93 = MyPatts2(morethanpro3).P
            N93 = MyPatts2(digit).P
            c93 = MyClass2(P93,N93,idf,0,0,morethanpro3[0].strip())   
 
            P94 = MyPatts2(morethanpro4).P
            N94 = MyPatts2(digit).P
            c94 = MyClass2(P94,N94,idf,0,0,morethanpro4[0].strip())   

            P95 = MyPatts2(morethanpro5).P
            N95 = MyPatts2(digit).P
            c95 = MyClass2(P95,N95,idf,0,0,morethanpro5[0].strip())   
 
            P96 = MyPatts2(morethanpro6).P
            N96 = MyPatts2(digit).P
            c96 = MyClass2(P96,N96,idf,0,0,morethanpro6[0].strip())   
            
            # <p/k

            P121 = MyPatts2(lessthanpro1).P
            N121 = MyPatts2(digit).P
            c121 = MyClass2(P121,N121,idf,0,0,lessthanpro1[0].strip())

            P122 = MyPatts2(lessthanpro2).P
            N122 = MyPatts2(digit).P
            c122 = MyClass2(P122,N122,idf,0,0,lessthanpro2[0].strip())

            P123 = MyPatts2(lessthanpro3).P
            N123 = MyPatts2(digit).P
            c123 = MyClass2(P123,N123,idf,0,0,lessthanpro3[0].strip())
            
            P124 = MyPatts2(lessthanpro4).P
            N124 = MyPatts2(digit).P
            c124 = MyClass2(P124,N124,idf,0,0,lessthanpro4[0].strip())    
            
            P125 = MyPatts2(lessthanpro5).P
            N125 = MyPatts2(digit).P
            c125 = MyClass2(P125,N125,idf,0,0,lessthanpro5[0].strip())

            P126 = MyPatts2(lessthanpro6).P
            N126 = MyPatts2(digit).P
            c126 = MyClass2(P126,N126,idf,0,0,lessthanpro6[0].strip())
            
            P127 = MyPatts2(lessthanpro7).P
            N127 = MyPatts2(digit).P
            c127 = MyClass2(P127,N127,idf,0,0,lessthanpro7[0].strip())                                
            
            ####################################################################  
            ####################################################################            
            
            # examine only k chunks of the big file at a time
            while mydata.lines:
                
                i = 0
                my_max = len(mydata.lines)
                
                # loop over chunk
                while i  <  my_max:
            
                    # parse the chunk
                    lines = mydata.lines
                    line = mydata.lines[i]
                    
                    # build sentence            
                    sen = MySen()
                    sen.buildSen(i,lines,my_max)
                
                    # if sentence built, apply patterns       
                    if sen.end == True:
                        
                        # retrieve POS tagged sentence
                        myline = sen.sen
            
                        ####################################################################           
                    
                        # corpus
                        corpus.openSen(myline,corpus.pats,corpus.patts)        
                    
                        ####################################################################
                        ####################################################################            
                        
                        # all
                        c11.openSen2(myline,c11.pats,c11.patts)  
                        c12.openSen2(myline,c12.pats,c12.patts)
                        c13.openSen2(myline,c13.pats,c13.patts)
                        c17.openSen2(myline,c17.pats,c17.patts)
                        c18.openSen2(myline,c18.pats,c18.patts)   
                        
                        # some
                        c25.openSen2(myline,c25.pats,c25.patts)
                        
                        # > k
                        c41.openSen2(myline,c41.pats,c41.patts)
                        c42.openSen2(myline,c42.pats,c42.patts)
                        c43.openSen2(myline,c43.pats,c43.patts)
                        
                        # < k
                        c51.openSen2(myline,c51.pats,c51.patts)
                        c52.openSen2(myline,c52.pats,c52.patts)
                        c53.openSen2(myline,c53.pats,c53.patts)
                        c54.openSen2(myline,c54.pats,c54.patts)
                        c55.openSen2(myline,c55.pats,c55.patts)
                        
                        # most
                        c71.openSen2(myline,c71.pats,c71.patts)
                        c72.openSen2(myline,c72.pats,c72.patts)
                        c73.openSen2(myline,c73.pats,c73.patts)
                        c74.openSen2(myline,c74.pats,c74.patts)
                        c75.openSen2(myline,c75.pats,c75.patts)
                        
                        # few
                        c81.openSen2(myline,c81.pats,c81.patts)
                        c82.openSen2(myline,c82.pats,c82.patts)
                        c83.openSen2(myline,c83.pats,c83.patts)
                        c84.openSen2(myline,c84.pats,c84.patts)
                        
                        # > p/k
                        c91.openSen2(myline,c91.pats,c91.patts)
                        c92.openSen2(myline,c92.pats,c92.patts)
                        c93.openSen2(myline,c93.pats,c93.patts)
                        c94.openSen2(myline,c94.pats,c94.patts)
                        c95.openSen2(myline,c95.pats,c95.patts)
                        c96.openSen2(myline,c96.pats,c96.patts)
                        
                        # < p/k
                        c121.openSen2(myline,c121.pats,c121.patts)
                        c122.openSen2(myline,c122.pats,c122.patts)
                        c123.openSen2(myline,c123.pats,c123.patts)
                        c124.openSen2(myline,c124.pats,c124.patts)
                        c125.openSen2(myline,c125.pats,c125.patts)
                        c126.openSen2(myline,c126.pats,c126.patts)
                        c127.openSen2(myline,c127.pats,c127.patts)
                
                        ####################################################################
                    
                    # if a sentence is found, skip the lines it
                    # covers in the loop, otherwise move to the
                    # next line
                    if sen.len > 0:
                        i = i + sen.len
                        # print 'senlen=', sen.len, '\n'
                        # print 'sen= ', sen.sen, '\n'
                    else:    
                        i = i + 1
                    # print 'explore at line= ', i, '\n'
                
                # move to new chunk
                mydata.lines = mydata.myread()
            
            ####################################################################
            ####################################################################
                       
            # total cum count
            tot = (
                   c11.count + c12.count + c13.count + 
                   c17.count + c18.count + 
                   c25.count + 
                   c41.count + c42.count + c43.count + 
                   c51.count + c52.count + c53.count + c54.count + c55.count +              
                   c71.count + c72.count + c73.count + c74.count + c75.count +                   
                   c81.count + c82.count + c83.count + c84.count +  
                   c91.count + c92.count + c93.count + c94.count + c96.count + c95.count +
                   c121.count + c122.count + c123.count + c124.count + c125.count + c126.count + c127.count
                   ) + 1
    
            print "corpus size : " + `corpus.count` + " sentences"        
            print "==================================================="
            print "total matches: " + `tot` + " GQs"
            
            ####################################################################            
            
            filestats = [
                         c11,c12,c13,c17,c18,
                         c25,
                         c41,c42,c43,
                         c51,c52,c53,c54,c55,
                         c71,c72,c73,c74,c75,
                         c81,c82,c83,c84,
                         c91,c92,c93,c94,c95,c96,
                         c121,c122,c123,c124,c125,c126,c127
                         ]
            
            ####################################################################  
            
            self.stats[idf] = filestats
            
            ####################################################################  
            
            for cla in self.classstats:
                for thiscls in filestats:
                    if (thiscls.tag == cla.tag):
                        cla.classes.append(thiscls)

            ####################################################################  
                                
        # updating the distribution 
        #self.classAvg(self.classstats)
        self.classAvg2(self.classstats)
        #sort = self.sortClass(self.classstats)
        #self.classstats = sort
        print "###################################################"
        #self.printClasses(self.classstats)
    

    ############################################################# 
    #############################################################     
        
                
    # sorts stats classes
    def sortClass(self,classlist):
        sort = sorted(classlist,key=attrgetter('fre'))
        return sort
            
            
    # computes list of frequencies    
    def classAvg2(self,classstats):
        for cla in classstats:
            for idf in cla.classes:
                cla.fre = idf.count
    
    
    #############################################################
    #############################################################
    
        
    # prints the stats
    def printClasses(self,classstats):
        for cla in classstats:
            print cla.tag
            print "---------------------------------------------------"
            for idf in cla.classes:
                print `idf.count` + ": freq " + "(" + idf.fileid + ")"             
            print "###################################################"

    #############################################################
    #############################################################

        
    # statistical tests
    def statTestB(self,classstats):
        
        s = STest()
           
        # simple samples:   
             
        # freqs (cross corpus, per corpus)     
        sample1 = [] 
        for cla in classstats:
            sample1.append(sum([cl.count for cl in cla.classes]))             
            
        # simple stats methods
        print "\n###################################################"        
        print "Simple statistical tests: (patterns)"
        ##########################################################
        s.mySkew(sample1)                       # skewness     
        s.myChiTest(sample1,s.uniFor(sample1))  # X^2 test   

