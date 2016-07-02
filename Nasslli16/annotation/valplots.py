'''
Created on 2016
@author: camilothorne
'''


from __future__ import division
import array                        #@UnusedImport
from matplotlib import pylab, rc
from numpy import *                 #@UnusedWildImport
import scipy                        #@UnusedImport
import csv, os
#from time import time

# statistical test(s)
from statstests import STest

# saving the experiments
from savestat import SaveStat


class ExpPlotD:
    '''
    chart plotter
    '''
    
    def __init__(self,stats):
        '''
        constructor
        '''
        
        statsA = stats.expOne        
        uni = stats.titOne
        
        rc('xtick', labelsize=12) 
        rc('ytick', labelsize=12) 
        fig1 = pylab.figure(figsize=(8,5), dpi=100)   
        self.plotCurve(fig1,statsA,len(statsA[0]),"Performance" ,1)     
        pylab.ioff()
        #to use if needed
        #mytime = '%.2f' % time()
        mytime = ""
        fig1.savefig(os.environ['TEX']+uni+mytime+'.pdf')        
        # display plot if required
        #pylab.show()
        # save
        SaveStat(os.environ['TEX']+uni+mytime+'.tex',
                  os.environ['TEX']+uni+mytime+'.pdf',
                  uni)           
        
                                     
    def plotCurve(self,figu,stats,c_num,name,pos):
        '''
        curve chart plotter
        
        feature x precision, recall, f-measure          
        '''
        
        ax      = figu.add_subplot(1,1,pos)
        ind     = pylab.arange(c_num)
        width   = 1         # 1cm per unit of length
        maxi    = 1         # y-axis ranges from 0 to 0.6
        
        # methods, annotators
        ctags   = stats[0]
        pre     = stats[1]
        rec     = stats[2]
        fme     = stats[3]
        acc     = stats[4]
        
#         print "pre ", pre
#         print "rec ", rec
#         print "fme ", fme
#         print "acc ", acc 
        
        # line identifiers
        li = ("MetaMap","BabelFly","TagMe","WordNet")    
                              
        # plot 1
        ax.plot((ind+width/2),pre,'o--',# change line type
                color='r',linewidth=3,label="MetaMap") # change color

        # plot 1
        ax.plot((ind+width/2),rec,'x--',# change line type
                color='k',linewidth=3,label="BabelFly") # change color        
        
        # plot 2
        ax.plot((ind+width/2),fme,'x-',# change line type
                color='b',linewidth=1,label="TagMe")    # change color
        # plot 3
        ax.plot((ind+width/2),acc,'o-',# change line type
                color='g',linewidth=3,label="WordNet")  # change color
            
        ax.axis([0,c_num,0,maxi])
            
        # set name of y-axis
#        ax.set_ylabel(name+" (avg.)",fontsize='12')        
        ax.set_ylabel(name+" ",fontsize='12')
        
        # plot feature names
        mytags = []
        for c in range(c_num):
            mytags.append(c+(width/2))
        ax.set_xticks(mytags)
        ax.set_xticklabels(ctags,rotation='45',fontsize='12')
        ax.grid(False)
     
        # plot legend
        self.plotLegend(ax,li)
    
                
    def plotLegend(self,ax,li):
        '''
        plotting the legend on top of figure
        '''
        
        leg = ax.legend(li,bbox_to_anchor=(0., 1.005, 1., .102), loc=3,
                        ncol=4, mode="expand", borderaxespad=0.)
        frame  = leg.get_frame()
        frame.set_facecolor('1.0')       # set the frame face color to white
        for t in leg.get_texts():
            t.set_fontsize('large')      # the legend text fontsize
        for l in leg.get_lines():
            l.set_linewidth(1.5)         # the legend line width
     
    

################################################################################
    
    
class MMStats:
    '''
    class with the stats
    '''
        
        
    def __init__(self):
        '''
        void constructor
        '''

        self.expOne     = None
        self.titOne     = None
  
    
    def set(self,resname):
        '''
        set data for plots
        '''
        
        self.expOne     = self.readAVG(resname)
        self.titOne     = resname        
  

    def readAVG(self,name):
        '''
        open data file (metrics per method)
        '''
        
        readerA = open(os.environ['TEX']+name+'.csv', 'rb')
        feats   = self.csv_extract_col(readerA, '(avg.)')
        readerE = open(os.environ['TEX']+name+'.csv', 'rb')
        a       = [float(i) for i in self.csv_extract_col(readerE, 'MetaMap')]        
        readerB = open(os.environ['TEX']+name+'.csv', 'rb')
        b       = [float(i) for i in self.csv_extract_col(readerB, 'BabelFly')]
        readerC = open(os.environ['TEX']+name+'.csv', 'rb')
        c       = [float(i) for i in self.csv_extract_col(readerC, 'TagMe')]
        readerD = open(os.environ['TEX']+name+'.csv', 'rb')
        d       = [float(i) for i in self.csv_extract_col(readerD, 'WordNet')]
        print feats, a, b, c, d
        res     = [feats,a,b,c,d]
        return res
    
      
    def csv_extract_col(self,csvinput,colname):
        '''
        extract columns from .csv file
        '''
        
        col = []
        for row in csv.DictReader(csvinput,delimiter = ",", quotechar = "'"):
            col.append(row[colname])
        return col
    
    
    def readF(self,name):
        '''
        open .csv file
        '''
        
        csvinput = open(os.environ['DATA']+name+'.csv', 'rb')
        rows = []
        data = []
        for row in csv.reader(csvinput):
            data.append(row)
        for d in data[1:]:
            vals = [float(i) for i in d[1:]]
            rows.append(vals)
        return rows
 

    def chi2Tests(self):
        '''
        chi-2 tests (1) 
        '''
        
        stats = STest()
        
        # results
        avgOne =    []
        for i in range(1,len(self.expOne)):
            avgOne.append(self.expOne[i][0])            
        avgTwo =    []
        for i in range(1,len(self.expOne)):
            avgTwo.append(self.expOne[i][1])          
        avgThree =    []
        for i in range(1,len(self.expOne)):
            avgThree.append(self.expOne[i][2])         
                          
        # tests
        print "###################################################"        
        print "TESTS:\t", "by measure (random?)", "(pre, rec, F1)\n",
        print "###################################################"
        # null hypothesis: uniform distribution
        # we want to know if it is random     
        stats.myChiTest(avgOne,stats.uniFor(avgOne))
        stats.myChiTest(avgTwo,stats.uniFor(avgTwo))
        stats.myChiTest(avgThree,stats.uniFor(avgThree))     
        print "===================================================\n"
    
        
    def otherTests(self):
        '''
        other tests (2) - Kruskal, Friedman
        '''
        
        stats = STest()
        
        # results
        avgOne      =   self.expOne[1]        
        avgTwo      =   self.expOne[2] 
        avgThree    =   self.expOne[3]
        avgFour    =    self.expOne[4:quit]             
                          
        # test
        print "###################################################"        
        print "TESTS:\t", "by method (equal?)", "(MetaMap,BabelFly,WordNet,TagMe)\n",
        print "###################################################"
        # null hypothesis: equally distributed
        # we want to know if they are different        
        stats.myKruskal(avgOne,avgTwo,avgThree,avgFour)
        print "===================================================\n"
        
        # test
        print "###################################################"        
        print "TESTS:\t", "by method (equal?)", "(MetaMap, BabelFly,WordNet,TagMe)\n",
        print "###################################################"
        # null hypothesis: equally distributed
        # we want to know if they are different        
        stats.myFriedman(array(avgOne),array(avgTwo),array(avgThree),array(avgFour))
        print "===================================================\n"        
 
        # results
        avgOne =    []
        for i in range(1,len(self.expOne)):
            avgOne.append(self.expOne[i][0])            
        avgTwo =    []
        for i in range(1,len(self.expOne)):
            avgTwo.append(self.expOne[i][1])          
        avgThree =    []
        for i in range(1,len(self.expOne)):
            avgThree.append(self.expOne[i][2])
        
        # test
        print "###################################################"        
        print "TESTS:\t", "by measure (equal?)", "(pre, rec, F1)\n",
        print "###################################################"
        # null hypothesis: equally distributed
        # we want to know if they are different        
        stats.myKruskal(avgOne,avgTwo,avgThree)
        print "===================================================\n"                  

