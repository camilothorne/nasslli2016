'''
Created on May 17, 2016

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
####################################################################
# A. simple classes
####################################################################
####################################################################

####################################################################
# ARISTOTELIAN
####################################################################

# 1. exists

s10     = " someone/nn"
s12     = " somebody/nn"
s12a    = " anybody/nn"
s14     = " something/nn"
s16     = " some/dt"
s20     = " many/jj "

some1 = [s10]
some2 = [s12]
some3 = [s12a]
some4 = [s14]
some5 = [s16]
some6 = [s20]

####################################################################

# 4. all

s40     = " every/dt "
s42     = " all/dt "
s42a    = " all/pdt "
s46     = " everything/nn "
s48     = " everyone/nn " 
s4a     = " everybody/nn " 
s4c     = " each/dt "
s4e     = " no/dt "

all1 = [s40]
all2 = [s42]
all3 = [s42a]
all4 = [s46]
all5 = [s48]
all6 = [s4a]
all7 = [s4c]
all8 = [s4e]

####################################################################
# COUNTING
####################################################################

# 6. at most k, less than k (k integer)

s60     = " at/in most/jjs .*/cd "

s20b    = " less/rbr than/in .*/cd "
s20bb   = " less/jjr than/in .*/cd "

s20c    = " fewer/jjr than/in .*/cd "

lessk1 = [s20b]
lessk2 = [s20c]
lessk3 = [s60]

####################################################################

# 7. at least k, more than k (k integer)

s60b     = " at/in least/jjs .*/cd "

s20      = " more/rbr than/in .*/cd "
s20a     = " more/jjr than/in .*/cd "

morek1 = [s20]
morek2 = [s20a]
morek3 = [s60b]

####################################################################

# 8. exactly k (k integer)

s70    = " .*/cd [a-z]{1,12}/nns "
s70a   = " .*/cd [a-z]{1,12}/jj [a-z]{1,12}/nns "
s70b   = " .*/cd [a-z]{1,12}/nn [a-z]{1,12}/nns "
s71    = " exactly/rb .*/cd "

exactlyk1 = [s70]
exactlyk2 = [s70a]
exactlyk3 = [s70b]
exactlyk4 = [s71]

####################################################################
# PROPORTIONAL
####################################################################

# 9. more than p/k (p, k integers)

s80  = " more/rbr than/in half/nn "
s80a = " more/jjr than/in half/nn "

s82  = " more/rbr than/in .*/cd .*/nns of/in "
s82a = " more/jjr than/in .*/cd .*/nns of/in "

morethanpro1 = [s80]
morethanpro2 = [s82]
morethanpro3 = [s80a]
morethanpro4 = [s82a]

####################################################################

# 9.1 less than p/k (p, k integers)

s80b    = " less/rbr than/in half/nn "
s80bb   = " fewer/jjr than/in half/nn "

s82b    = " less/rbr than/in .*/cd .*/nns of/in "
s82bb   = " fewer/jjr than/in .*/cd .*/nn of/in "

lessthanpro1 = [s80b]
lessthanpro2 = [s80bb]
lessthanpro3 = [s82b]
lessthanpro4 = [s82bb]

####################################################################

# 9.2 p/k (p, k integers)                                       TODO

s80c    = " half/dt "
s80d    = " half/pdt "
s80e    = " half/nn of/in"

s81c    = " .*/cd [a-z]{1,12}/nns of/in "
s81d    = " .*/cd [a-z]{1,12}/nn of/in "

pro1 = [s80c]
pro2 = [s80d]
pro3 = [s80e]
pro4 = [s81c]
pro5 = [s81d]

####################################################################

# 3. more than k% (k a percentage)

s30     = " more/rbr than/in .*/cd percent/nn "
s30a    = " more/rbr than/in .*/cd %/nn "

s30aa   = " more/jjr than/in .*/cd percent/nn "
s30aaa  = " more/jjr than/in .*/cd %/nn "

morekper1 = [s30]
morekper2 = [s30a]
morekper3 = [s30aa]
morekper4 = [s30aaa]

####################################################################

# 3.1 less than k% (k a percentage)

s30b     = " less/rbr than/in .*/cd percent/nn "
s30bb    = " less/rbr than/in .*/cd %/nn "

s30bx    = " less/jjr than/in .*/cd percent/nn "
s30bbx   = " less/jjr than/in .*/cd %/nn "

s30bc    = " fewer/jjr than/in .*/cd percent/nn "
s30bcx   = " fewer/jjr than/in .*/cd %/nn "

lesskper1 = [s30b]
lesskper2 = [s30bb]
lesskper3 = [s30bbx]
lesskper4 = [s30bc]
lesskper5 = [s30bcx]

####################################################################

# 3.2 k% (k a percentage)

s30c    = " .*/cd percent/nn "
s30d    = " .*/cd %/NN"

kper1 = [s30c]
kper2 = [s30d]

####################################################################

# 5. most, more than half

s52     = " most/rbs "
s51     = " most/jjs "
s51a    = " most/dt "

s53     = " more/rbr than/in half/nn "
s53a    = " more/jjr than/in half/nn "

most1 = [s51a]
most2 = [s53]
most3 = [s51]
most4 = [s52]
most5 = [s53a]

####################################################################

# 5.1 few, less than half, fewer than half

ss51b   = " few/jj "
s51bb   = " few/dt "

s53b    = " less/rbr than/in half/nn "
s53bb   = " fewer/jjr than/in half/nn "

few1 = [s51bb]
few2 = [s53b]
few3 = [s53bb]
few4 = [ss51b]


####################################################################
####################################################################


# Class encoding the plot(s) + test(s)


class ProporStatsP:
   
    
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
        statsname = "Base GQs (patterns)"
        savpath = plotting +'/'+ statsname.replace(' ', '-')
        
        # generating report
        SaveStats(self.classstats,self.stats,"",savpath,plotting) # all
        
        
    #############################################################
    #############################################################        
 
            
    # creating the classes
    def fileStats(self,path,fileids):
                
        # starting the title
        tit = "Base GQs (patterns)"
        
        # all
        C11  =   MyClassStats2(all1[0].strip(),[],0,tit)
        C12  =   MyClassStats2(all2[0].strip(),[],0,tit)
        C13  =   MyClassStats2(all3[0].strip(),[],0,tit)
        C14  =   MyClassStats2(all4[0].strip(),[],0,tit)
        C15  =   MyClassStats2(all5[0].strip(),[],0,tit)
        C16  =   MyClassStats2(all6[0].strip(),[],0,tit)
        C17  =   MyClassStats2(all7[0].strip(),[],0,tit)
        C18  =   MyClassStats2(all8[0].strip(),[],0,tit)                              
        
        # some
        C21  =   MyClassStats2(some1[0].strip(),[],0,tit)
        C22  =   MyClassStats2(some2[0].strip(),[],0,tit)        
        C23  =   MyClassStats2(some3[0].strip(),[],0,tit)
        C24  =   MyClassStats2(some4[0].strip(),[],0,tit)
        C25  =   MyClassStats2(some5[0].strip(),[],0,tit)
        C26  =   MyClassStats2(some6[0].strip(),[],0,tit)        
        
        # > k
        C41 =    MyClassStats2(morek1[0].strip(),[],0,tit)
        C42 =    MyClassStats2(morek2[0].strip(),[],0,tit)
        C43 =    MyClassStats2(morek3[0].strip(),[],0,tit)        
        
        # < k
        C51 =    MyClassStats2(lessk1[0].strip(),[],0,tit)
        C52 =    MyClassStats2(lessk2[0].strip(),[],0,tit)
        C53 =    MyClassStats2(lessk3[0].strip(),[],0,tit)
        
        # k
        C61 =    MyClassStats2(exactlyk1[0].strip(),[],0,tit)
        C62 =    MyClassStats2(exactlyk2[0].strip(),[],0,tit)
        C63 =    MyClassStats2(exactlyk3[0].strip(),[],0,tit)
        C64 =    MyClassStats2(exactlyk4[0].strip(),[],0,tit)        
        
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
        
        # < p/k
        C101 =   MyClassStats2(lessthanpro1[0].strip(),[],0,tit)
        C102 =   MyClassStats2(lessthanpro2[0].strip(),[],0,tit)
        C103 =   MyClassStats2(lessthanpro3[0].strip(),[],0,tit)
        C104 =   MyClassStats2(lessthanpro4[0].strip(),[],0,tit)
        
        # p/k
        C131 =   MyClassStats2(pro1[0].strip(),[],0,tit)
        C132 =   MyClassStats2(pro2[0].strip(),[],0,tit)
        C133 =   MyClassStats2(pro3[0].strip(),[],0,tit)
        C134 =   MyClassStats2(pro4[0].strip(),[],0,tit)
        C135 =   MyClassStats2(pro5[0].strip(),[],0,tit)        
        
        # > p%
        C111 =   MyClassStats2(morekper1[0].strip(),[],0,tit)
        C112 =   MyClassStats2(morekper2[0].strip(),[],0,tit)
        C113 =   MyClassStats2(morekper3[0].strip(),[],0,tit)
        C114 =   MyClassStats2(morekper4[0].strip(),[],0,tit)
        
        # < p%
        C121 =   MyClassStats2(lesskper1[0].strip(),[],0,tit)
        C122 =   MyClassStats2(lesskper2[0].strip(),[],0,tit)
        C123 =   MyClassStats2(lesskper3[0].strip(),[],0,tit)
        C124 =   MyClassStats2(lesskper4[0].strip(),[],0,tit)
        C125 =   MyClassStats2(lesskper5[0].strip(),[],0,tit)
        
        # p%
        C141 =   MyClassStats2(kper1[0].strip(),[],0,tit)
        C142 =   MyClassStats2(kper2[0].strip(),[],0,tit)
        
        self.classstats = [C11,C12,C13,C14,C15,C16,C17,C18,
                           C21,C22,C23,C24,C25,C26,
                           C41,C42,C43,
                           C51,C52,C53,
                           C61,C62,C63,C64,
                           C71,C72,C73,C74,C75,
                           C81,C82,C83,C84,
                           C91,C92,C93,C94,
                           C101,C102,C103,C104,
                           C131,C132,C133,C134,C135,
                           C111,C112,C113,C114,
                           C121,C122,C123,C124,C125,
                           C141,C142]        
        
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
            rest = []  
            
            # corpus
            corpus = MyClass2([".*"],[],idf,0,0,"corpus")
            
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
            
            P14 = MyPatts2(all4).P
            N14 = MyPatts2(rest).P
            c14 = MyClass2(P14,N14,idf,0,0,all4[0].strip())
            
            P15 = MyPatts2(all5).P
            N15 = MyPatts2(rest).P
            c15 = MyClass2(P15,N15,idf,0,0,all5[0].strip())       
            
            P16 = MyPatts2(all6).P
            N16 = MyPatts2(rest).P
            c16 = MyClass2(P16,N16,idf,0,0,all6[0].strip()) 
            
            P17 = MyPatts2(all7).P
            N17 = MyPatts2(rest).P
            c17 = MyClass2(P17,N17,idf,0,0,all7[0].strip()) 
            
            P18 = MyPatts2(all8).P
            N18 = MyPatts2(rest).P
            c18 = MyClass2(P18,N18,idf,0,0,all8[0].strip())                                                                  
            
            # some
            P21 = MyPatts2(some1).P
            N21 = MyPatts2(rest).P           
            c21 = MyClass2(P21,N21,idf,0,0,some1[0].strip())   
                    
            P22 = MyPatts2(some2).P
            N22 = MyPatts2(rest).P           
            c22 = MyClass2(P22,N22,idf,0,0,some2[0].strip())  
            
            P23 = MyPatts2(some3).P
            N23 = MyPatts2(rest).P           
            c23 = MyClass2(P23,N23,idf,0,0,some3[0].strip())   
                    
            P24 = MyPatts2(some4).P
            N24 = MyPatts2(rest).P           
            c24 = MyClass2(P24,N24,idf,0,0,some4[0].strip())
            
            P25 = MyPatts2(some5).P
            N25 = MyPatts2(rest).P           
            c25 = MyClass2(P25,N25,idf,0,0,some5[0].strip())    
            
            P26 = MyPatts2(some6).P
            N26 = MyPatts2(rest).P           
            c26 = MyClass2(P26,N26,idf,0,0,some6[0].strip())                           
            
            ####################################################################                
            
            # >k
            P41 = MyPatts2(morek1).P
            N41 = MyPatts2(rest).P
            c41 = MyClass2(P41,N41,idf,0,0,morek1[0].strip())                      

            P42 = MyPatts2(morek2).P
            N42 = MyPatts2(rest).P
            c42 = MyClass2(P42,N42,idf,0,0,morek2[0].strip())  
            
            P43 = MyPatts2(morek3).P
            N43 = MyPatts2(rest).P
            c43 = MyClass2(P43,N43,idf,0,0,morek3[0].strip())                         
            
            # <k
            P51 = MyPatts2(lessk1).P
            N51 = MyPatts2(rest).P
            c51 = MyClass2(P51,N51,idf,0,0,lessk2[0].strip())

            P52 = MyPatts2(lessk2).P
            N52 = MyPatts2(rest).P
            c52 = MyClass2(P52,N52,idf,0,0,lessk2[0].strip())

            P53 = MyPatts2(lessk3).P
            N53 = MyPatts2(rest).P
            c53 = MyClass2(P53,N53,idf,0,0,lessk3[0].strip())
            
            # k
            P61 = MyPatts2(exactlyk1).P
            N61 = MyPatts2(rest).P
            c61 = MyClass2(P61,N61,idf,0,0,exactlyk1[0].strip())

            P62 = MyPatts2(exactlyk2).P
            N62 = MyPatts2(rest).P
            c62 = MyClass2(P62,N62,idf,0,0,exactlyk2[0].strip())
            
            P63 = MyPatts2(exactlyk3).P
            N63 = MyPatts2(rest).P
            c63 = MyClass2(P63,N63,idf,0,0,exactlyk3[0].strip())
            
            P64 = MyPatts2(exactlyk4).P
            N64 = MyPatts2(rest).P
            c64 = MyClass2(P64,N64,idf,0,0,exactlyk4[0].strip())                        
            
            ####################################################################
            
            # most
            P71 = MyPatts2(most1).P
            N71 = MyPatts2(rest).P
            c71 = MyClass2(P71,N71,idf,0,0,most1[0].strip())
            
            P72 = MyPatts2(most2).P
            N72 = MyPatts2(rest).P
            c72 = MyClass2(P72,N72,idf,0,0,most2[0].strip())
                        
            P73 = MyPatts2(most3).P
            N73 = MyPatts2(rest).P
            c73 = MyClass2(P73,N73,idf,0,0,most3[0].strip())
            
            P74 = MyPatts2(most4).P
            N74 = MyPatts2(rest).P
            c74 = MyClass2(P74,N74,idf,0,0,most4[0].strip())
            
            P75 = MyPatts2(most5).P
            N75 = MyPatts2(rest).P
            c75 = MyClass2(P75,N75,idf,0,0,most5[0].strip())            
                             
            # few
            P81 = MyPatts2(few1).P
            N81 = MyPatts2(rest).P
            c81 = MyClass2(P81,N81,idf,0,0,few1[0].strip())

            P82 = MyPatts2(few2).P
            N82 = MyPatts2(rest).P
            c82 = MyClass2(P82,N82,idf,0,0,few2[0].strip())

            P83 = MyPatts2(few3).P
            N83 = MyPatts2(rest).P
            c83 = MyClass2(P83,N83,idf,0,0,few3[0].strip())

            P84 = MyPatts2(few4).P
            N84 = MyPatts2(rest).P
            c84 = MyClass2(P84,N84,idf,0,0,few4[0].strip())
                
            # >k/100
            P91 = MyPatts2(morekper1).P
            N91 = MyPatts2(rest).P
            c91 = MyClass2(P91,N91,idf,0,0,morekper1[0].strip())
            
            P92 = MyPatts2(morekper2).P
            N92 = MyPatts2(rest).P
            c92 = MyClass2(P92,N92,idf,0,0,morekper2[0].strip())
            
            P93 = MyPatts2(morekper3).P
            N93 = MyPatts2(rest).P
            c93 = MyClass2(P93,N93,idf,0,0,morekper3[0].strip())
            
            P94 = MyPatts2(morekper4).P
            N94 = MyPatts2(rest).P
            c94 = MyClass2(P94,N94,idf,0,0,morekper4[0].strip())
    
            # <k/100
            P101 = MyPatts2(lesskper1).P
            N101 = MyPatts2(rest).P
            c101 = MyClass2(P101,N101,idf,0,0,lesskper1[0].strip())

            P102 = MyPatts2(lesskper2).P
            N102 = MyPatts2(rest).P
            c102 = MyClass2(P102,N102,idf,0,0,lesskper2[0].strip())

            P103 = MyPatts2(lesskper3).P
            N103 = MyPatts2(rest).P
            c103 = MyClass2(P103,N103,idf,0,0,lesskper3[0].strip())

            P104 = MyPatts2(lesskper4).P
            N104 = MyPatts2(rest).P
            c104 = MyClass2(P104,N104,idf,0,0,lesskper4[0].strip())

            P105 = MyPatts2(lesskper5).P
            N105 = MyPatts2(rest).P
            c105 = MyClass2(P105,N105,idf,0,0,lesskper5[0].strip())
                
            # k/100
            P131 = MyPatts2(kper1).P
            N131 = MyPatts2(rest).P
            c131 = MyClass2(P131,N131,idf,0,0,kper1[0].strip())

            P132 = MyPatts2(kper2).P
            N132 = MyPatts2(rest).P
            c132 = MyClass2(P132,N132,idf,0,0,kper2[0].strip())
                
            # >p/k
            P111 = MyPatts2(morethanpro1).P
            N111 = MyPatts2(rest).P
            c111 = MyClass2(P111,N111,idf,0,0,morethanpro1[0].strip())                    
 
            P112 = MyPatts2(morethanpro2).P
            N112 = MyPatts2(rest).P
            c112 = MyClass2(P112,N112,idf,0,0,morethanpro2[0].strip())   
 
            P113 = MyPatts2(morethanpro3).P
            N113 = MyPatts2(rest).P
            c113 = MyClass2(P113,N113,idf,0,0,morethanpro3[0].strip())   
 
            P114 = MyPatts2(morethanpro4).P
            N114 = MyPatts2(rest).P
            c114 = MyClass2(P114,N114,idf,0,0,morethanpro4[0].strip())   
            
            # <p/k

            P121 = MyPatts2(lessthanpro1).P
            N121 = MyPatts2(rest).P
            c121 = MyClass2(P121,N121,idf,0,0,lessthanpro1[0].strip())

            P122 = MyPatts2(lessthanpro2).P
            N122 = MyPatts2(rest).P
            c122 = MyClass2(P122,N122,idf,0,0,lessthanpro2[0].strip())

            P123 = MyPatts2(lessthanpro3).P
            N123 = MyPatts2(rest).P
            c123 = MyClass2(P123,N123,idf,0,0,lessthanpro3[0].strip())
            
            P124 = MyPatts2(lessthanpro4).P
            N124 = MyPatts2(rest).P
            c124 = MyClass2(P124,N124,idf,0,0,lessthanpro4[0].strip())
            
            # p/k

            P141 = MyPatts2(pro1).P
            N141 = MyPatts2(rest).P
            c141 = MyClass2(P141,N141,idf,0,0,pro1[0].strip())   

            P142 = MyPatts2(pro2).P
            N142 = MyPatts2(rest).P
            c142 = MyClass2(P142,N142,idf,0,0,pro2[0].strip())   

            P143 = MyPatts2(pro3).P
            N143 = MyPatts2(rest).P
            c143 = MyClass2(P143,N143,idf,0,0,pro3[0].strip())   

            P144 = MyPatts2(pro4).P
            N144 = MyPatts2(rest).P
            c144 = MyClass2(P144,N144,idf,0,0,pro4[0].strip())   
            
            P145 = MyPatts2(pro5).P
            N145 = MyPatts2(rest).P
            c145 = MyClass2(P145,N145,idf,0,0,pro5[0].strip())                      
            
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
                        c11.openSen(myline,c11.pats,c11.patts)  
                        c12.openSen(myline,c12.pats,c12.patts)
                        c13.openSen(myline,c13.pats,c13.patts)
                        c14.openSen(myline,c14.pats,c14.patts)
                        c15.openSen(myline,c15.pats,c16.patts)
                        c16.openSen(myline,c16.pats,c16.patts) 
                        c17.openSen(myline,c17.pats,c17.patts)
                        c18.openSen(myline,c18.pats,c18.patts)   
                        
                        # some
                        c21.openSen(myline,c21.pats,c21.patts)
                        c22.openSen(myline,c22.pats,c22.patts)
                        c23.openSen(myline,c23.pats,c23.patts)
                        c24.openSen(myline,c24.pats,c24.patts)
                        c25.openSen(myline,c25.pats,c25.patts)
                        c26.openSen(myline,c26.pats,c26.patts)
                        
                        # > k
                        c41.openSen(myline,c41.pats,c41.patts)
                        c42.openSen(myline,c42.pats,c42.patts)
                        c43.openSen(myline,c43.pats,c43.patts)
                        
                        # < k
                        c51.openSen(myline,c51.pats,c51.patts)
                        c52.openSen(myline,c52.pats,c52.patts)
                        c53.openSen(myline,c53.pats,c53.patts)
                        
                        # k
                        c61.openSen(myline,c61.pats,c61.patts)
                        c62.openSen(myline,c62.pats,c62.patts)
                        c63.openSen(myline,c63.pats,c63.patts)
                        c64.openSen(myline,c64.pats,c64.patts)
                        
                        # most
                        c71.openSen(myline,c71.pats,c71.patts)
                        c72.openSen(myline,c72.pats,c72.patts)
                        c73.openSen(myline,c73.pats,c73.patts)
                        c74.openSen(myline,c74.pats,c74.patts)
                        c75.openSen(myline,c75.pats,c75.patts)
                        
                        # few
                        c81.openSen(myline,c81.pats,c81.patts)
                        c82.openSen(myline,c82.pats,c82.patts)
                        c83.openSen(myline,c83.pats,c83.patts)
                        c84.openSen(myline,c84.pats,c84.patts)
                        
                        # >k/100
                        c91.openSen(myline,c91.pats,c91.patts)
                        c92.openSen(myline,c92.pats,c92.patts)
                        c93.openSen(myline,c93.pats,c93.patts)
                        c94.openSen(myline,c94.pats,c94.patts)
                        
                        # <k/100
                        c101.openSen(myline,c101.pats,c101.patts)
                        c102.openSen(myline,c102.pats,c102.patts)
                        c103.openSen(myline,c103.pats,c103.patts)
                        c104.openSen(myline,c104.pats,c104.patts)
                        c105.openSen(myline,c105.pats,c105.patts)
                        
                        # k/100
                        c131.openSen(myline,c131.pats,c131.patts)
                        c132.openSen(myline,c132.pats,c132.patts)
                        
                        # > p/k
                        c111.openSen(myline,c111.pats,c111.patts)
                        c112.openSen(myline,c112.pats,c112.patts)
                        c113.openSen(myline,c113.pats,c113.patts)
                        c114.openSen(myline,c114.pats,c114.patts)
                        
                        # < p/k
                        c121.openSen(myline,c121.pats,c121.patts)
                        c122.openSen(myline,c122.pats,c122.patts)
                        c123.openSen(myline,c123.pats,c123.patts)
                        c124.openSen(myline,c124.pats,c124.patts)
                        
                        # p/k
                        c141.openSen(myline,c141.pats,c141.patts)
                        c142.openSen(myline,c142.pats,c142.patts)
                        c143.openSen(myline,c143.pats,c143.patts)
                        c144.openSen(myline,c144.pats,c144.patts)
                        c145.openSen(myline,c145.pats,c145.patts)
                
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
                   c11.count + c12.count + c13.count + c14.count + c15.count + c16.count + c17.count + c18.count + 
                   c21.count + c22.count + c23.count + c24.count + c25.count + c26.count + 
                   c41.count + c42.count + c43.count + 
                   c51.count + c52.count + c53.count +
                   c61.count + c62.count + c63.count + c64.count +                 
                   c71.count + c72.count + c73.count + c74.count + c75.count +                   
                   c81.count + c82.count + c83.count + c84.count +  
                   c91.count + c92.count + c93.count + c94.count + 
                   c101.count + c102.count + c103.count + c104.count + c105.count +
                   c111.count + c112.count + c113.count + c114.count +
                   c121.count + c122.count + c123.count + c124.count + 
                   c131.count + c132.count + 
                   c141.count + c142.count + c143.count + c144.count + c145.count 
                   ) + 1
    
            print "corpus size : " + `corpus.count` + " sentences"        
            print "==================================================="
            print "total matches: " + `tot` + " GQs"
            
            ####################################################################            
            
            filestats = [
                         c11,c12,c13,c14,c15,c16,c17,c18,
                         c21,c22,c23,c24,c25,c26,
                         c41,c42,c43,
                         c51,c52,c53,
                         c61,c62,c63,c64,
                         c71,c72,c73,c74,c75,
                         c81,c82,c83,c84,
                         c91,c92,c93,c94,
                         c101,c102,c103,c104,c105,
                         c131,c132,
                         c111,c112,c113,c114,
                         c121,c122,c123,c124,
                         c141,c142,c143,c144,c145
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
        num = 1
        for cla in classstats:
            print cla.tag, "(class " + `num` + ")"
            num = num + 1
            print "---------------------------------------------------"
            for idf in cla.classes:
                print `idf.count` + ": freq "+ idf.fileid              
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

