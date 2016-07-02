#=======================#
#=======================#
#                       #
#  Statistical  tests   #
#                       #
#=======================#
#=======================#


from __future__ import division
from numpy import *
from numpy import array
from scipy.stats import *
from math import log


# stat tests class
class STest:

    
#    #samplestat : statistics


#    # constructor    
#    def __init__(self):
#        self.samplestat = samplestat
#        self.sampler = sampler
#        self.samplef = samplef
#        # distribution to fit (X^2)
#        control = self.uniFor(samplef) # distribution to fit
#        # tests
#        self.myEntropy(sampler) # entropy
#        self.myTest(samplef,control) # X^2 test
        
    
    ###############################################################3
    # 1. Tests   


    # X^2 test - control contains the fitted model/null hypothesis   
    def myChiTest(self,sample,control):
        res = chisquare(array(sample),control*sum(control))
        print "==================================================="
        print "X^2 test:"
        print "===================================================" 
        print `res`
        print "(chi^2, p-value), df="+`len(sample)-1`
        print "(*) if p-value < 0.05 ==> reject null"
        
    
    # t test
    def myTTest(self,sample,mean):
        res = ttest_1samp(sample, mean)    
        print "==================================================="
        print "One-sample/way t test:"
        print "===================================================" 
        print `res`
        print "(t, p-value), df="+`len(sample)-1`
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
        print "(F, p-value), df="+`(len(samples)-1)*(len(samples[0])-1)`
        print "(*) if p-value > 0.05 ==> accept null"
        
        
    # X^2 for independence 
    def myChiInd(self,samples):
        # samples is an array of samples of equal size
        # the test checks if the distribution of variable/factor X
        # differs throughout samples
        chi, p, d, exp = chi2_contingency(array(samples))
        print "==================================================="
        print "X^2 test for independence:"
        print "===================================================" 
        print "(" + `chi` + ", " + `p` +  ")"
        print "(chi^2, p-value), df=" + `(len(samples)-1)*(len(samples[0])-1)`
        print "(*) if p-value > 0.05 ==> accept null"
     
       
    # Friedman X^2 for variation 
    def myFChi(self,samples):
        # samples is an array of samples of equal size
        # the test checks if the distribution of variable/factor X
        # differs throughout samples
        res = friedmanchisquare(array(samples))
        print "==================================================="
        print "X^2 test for independence:"
        print "===================================================" 
        print `res` 
        print "(chi^2, p-value), df="+`(len(samples)-1)*(len(samples[0])-1)`
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
    # 2. Control distributions
        
        
    # building uniform distribution
    def uniFor(self,sample):
        res = []
        for i in range(len(sample)):
            freq = 1/len(sample)
            res.append(freq)
        return array(res)*sum(array(sample))
    
    
    #building constant distribution
    def conFor(self,sample,n):
        res = []
        for i in range(len(sample)):
            res.append(n)
        return array(res)


#    # building power law distribution
#    def uniFor(self,sample):
#       res = []
#       for i in range(len(sample)):
#           freq = 1/len(sample)
#           res.append(freq)
#       return array(res)


#    # building normal distribution
#    def uniFor(self,sample):
#       res = []
#       for i in range(len(sample)):
#           freq = 1/len(sample)
#           res.append(freq)
#       return array(res)