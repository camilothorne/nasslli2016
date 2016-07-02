#=======================#
#=======================#
#                       #
#  Statistical  tests   #
#                       #
#=======================#
#=======================#


from __future__ import division


import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)  # remove warnings  
warnings.filterwarnings("ignore", category=RuntimeWarning)      # remove warnings


from numpy import array
from numpy import std       #@UnusedImport
from scipy.stats import *   #@UnusedWildImport
from math import log


# stat tests class
class STest:
        
    
    ###############################################################3
    # 1. Tests   


    # X^2 test - control contains the fitted model/null hypothesis   
    def myChiTest(self,sample,control):
        res = chisquare(array(sample),control*sum(control))
        print "==================================================="
        print "X^2 test:"
        print "===================================================" 
        print `res`
        print "(chi^2, p-value)"
        print "(*) if p-value < 0.05 ==> reject null"
        
    
    # t test
    def myTTest(self,sample,mean):
        res = ttest_1samp(sample, mean)    
        print "==================================================="
        print "One-sample/way t test:"
        print "===================================================" 
        print `res`
        print "(t, p-value)"
        print "(*) if p-value < 0.05 ==> reject null"


    # skewness   
    def mySkew(self,sample):
        sk1 = skew(sample)
        print "==================================================="
        print "Skewness:"
        print "===================================================" 
        print `sk1` 
        print "(skewness)"

     
    # one-way ANOVA 
    def myANOVA(self,samples):
        # samples is an array of samples of equal size
        # the test checks if the distribution of variable/factor X
        # differs throughout samples
        res = f_oneway(array(samples))
        print "==================================================="
        print "One-way ANOVA:"
        print "===================================================" 
        print `res` 
        print "(F, p-value)"
        print "(*) if p-value > 0.05 ==> accept null"
        
        
    # X^2 for independence 
    def myChiInd(self,samples):
        # samples is an array of samples of equal size
        # the test checks if the distribution of variable/factor X
        # differs throughout samples
        chi, p, d, exp = chi2_contingency(array(samples)) #@UnusedVariable
        print "==================================================="
        print "X^2 test for independence:"
        print "===================================================" 
        print "(" + `chi` + ", " + `p` +  ")"
        print "(chi^2, p-value),"
        print "(*) if p-value > 0.05 ==> accept null"
     
       
    # Friedman X^2 for variation 
    def myFChi(self,samples):
        # samples is an array of samples of equal size
        # the test checks if the distribution of variable/factor X
        # differs throughout samples
        res = friedmanchisquare(array(samples))
        print "==================================================="
        print "Friedman X^2 test for variation:"
        print "===================================================" 
        print `res` 
        print "(chi^2, p-value)"
        print "(*) if p-value > 0.05 ==> accept null"
        
                
    # entropy and relative entropy of class distribution    
    def myEntropy(self,sample):
        res = 0
        for val in sample:
            if val == 0.0:
                res = res # 0 * log_2 0 = 0
            else:
                res = res + (val * log(val,2))
        #  entropy:
        #  H(X) = - Sum_i (p(x_i) * log_2(p(x_i))
        ent = - res
        #  relative entropy:
        #  H_rel(X) = H(X) / log_2(|X|)
        rent = ent / log(len(sample),2)
        print "==================================================="
        print "Entropy and relative entropy:"
        print "===================================================" 
        print `ent`
        print "(entropy)"
        print "---------------------------------------------------"
        print `log(len(sample),2)`
        print "(entropy max val)"
        print "---------------------------------------------------"
        print `rent`
        print "(relative entropy)"
     
     
    ###############################################################3
    # 2. Tests for arbitrarily large samples
    
 
    # Mann-Whitney:
    def myWhitney(self,sample1,sample2):
        # the test checks if the distributions described by
        # two samples differs
        res = mannwhitneyu(sample1, sample2, use_continuity=True)
        print "==================================================="
        print "Mann-Whitney test:"
        print "===================================================" 
        print `res`
        print "(value, p-value)"
        print "(*) if p-value > 0.05 ==> accept null"  
        
        
    # t test (large)
    def myTTestL(self,sample,mean):
        res = ttest_1samp(sample, mean)    
        print "==================================================="
        print "One-sample/way t test (> 20 observations):"
        print "===================================================" 
        print `res`
        print "(t, p-value)"
        print "(*) if p-value < 0.05 ==> reject null"   
        
        
    # t test (large)
    def myTTestP(self,sample1,sample2):
        res = ttest_1samp(sample1, sample2)    
        print "==================================================="
        print "Two-sample t test (> 20 observations):"
        print "===================================================" 
        print `res`
        print "(t, p-value)"
        print "(*) if p-value < 0.05 ==> reject null"                 
    
        
    # Wilcox:
    def myWilcox(self,sample1,sample2):
        # the test checks if the distributions described by
        # two samples differs
        res = wilcoxon(sample1, sample2)
        print "==================================================="
        print "Wilcox test:"
        print "===================================================" 
        print `res`
        print "(value, p-value)"
        print "(*) if p-value > 0.05 ==> accept null"        
        
        
    # Wilcox:
    def myWilcoxon(self,sample,mean):
        # the test checks if the distributions described by
        # two samples differs
        res = wilcoxon(sample - mean)
        print "==================================================="
        print "Wilcox test w.r.t. mean:"
        print "===================================================" 
        print `res`
        print "(value, p-value)"
        print "(*) if p-value > 0.05 ==> accept null"              
    

    # Kolmogorov-Smirnoff:
    def myKolmogorov(self,sample1,sample2):
        # the test checks if the distributions described by
        # two samples differs
        res = ks_2samp(sample1, sample2)
        print "==================================================="
        print "Kolmogorov-Smirnoff test:"
        print "===================================================" 
        print `res`
        print "(value, p-value)"
        print "(*) if p-value > 0.05 ==> accept null"  


    # Kruskal-Wallis:
    def myKruskal(self,*args):
        # the test checks if the distributions described by more than
        # two samples differs
        res = kruskal(*args)
        print "==================================================="
        print "Kruskal-Wallis test:"
        print "===================================================" 
        print `res`
        print "(value, p-value)"
        print "(*) if p-value > 0.05 ==> accept null"  
        
        
    # friedman
    def myFriedman(self,*args):
        # the test checks if different measurements on one same
        # samples differ
        res = friedmanchisquare(*args)
        print "==================================================="
        print "Friedman X^2 test:"
        print "===================================================" 
        print `res`
        print "(value, p-value)"
        print "(*) if p-value > 0.05 ==> accept null"          
           
    
    ###############################################################3
    # 3. Control distributions
        
        
    # building uniform distribution
    def uniFor(self,sample):
        res = []
        for i in range(len(sample)): #@UnusedVariable
            freq = 1/len(sample)
            res.append(freq)
        return array(res)*sum(array(sample))


    # building uniform distribution
    def uniForm(self,sample):
        res = []
        for i in range(len(sample)): #@UnusedVariable
            freq = 1/len(sample)
            res.append(freq)
        return array(res)
    
    
    #building constant distribution
    def conFor(self,sample,n):
        res = []
        for i in range(len(sample)): #@UnusedVariable
            res.append(n)
        return array(res)