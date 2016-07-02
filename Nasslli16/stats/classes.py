#===================#
#===================#
#                   #
#     Classes       #
#                   #
#===================#
#===================#


import string, re


# 1. Class encoding pattern stats        
class MyClass:

    #fileid:   filename
    #count :   feature occ frequency
    #freq  :   feature occ rel frequency
    #pats  :   set of regexps whose occ we want to check
    #patts :   set of regexps whose occ we want to rule out
    #tag   :   class name tag

    # object constructor
    def __init__(self,pats,patts,fileid,count,freq,tag):
        
        self.pats = pats
        self.patts = patts
        self.fileid = fileid
        self.count = count
        self.freq = freq
        self.tag = tag
        
    # open file method   
    def openFile(self,fileid,pats,patts):
        lcount = 0
        myfile = open(fileid,'r')
        try:
            text = myfile.read()
            lines = set(string.split(text,"\n"))
            #lcount = 0
            for line in lines:
                pos = 0
                neg = 0
                for pa in pats:
                    m = re.search(pa, line)
                    if m:
                        pos = pos + 1
                for paa in patts:
                    mm = re.search(paa, line)
                    if (mm == None):
                        neg = neg + 1
                if ((pos == len(pats)) & (neg == len(patts))):
                    lcount = lcount + 1
        finally:
            self.count = lcount
            myfile.close()

            
# 2. Class encapsulating lists of patterns        
class MyPatts:
    
        #P : list of regular expressions
        P = []
        
        # constructor
        def __init__(self,S):
            B = []
            for s in S:
                B.append(s)
            self.P = B


# 3. Class encapsulating all the class stats
class MyClassStats:
    
    #classes:    list of classes
    #avg:        average
    #tag:        class tag

    
    # constructor
    def __init__(self,tag,classes,avg):
        self.tag = tag
        self.classes = classes
        self.avg = avg
        self.fre = 0

        
#    # average frequency
#    def avgFre(self,classes):
#        print len(classes)
#        freq = 0
#        for cla in classes:
#            freq = freq + cla.count
#        freq = freq / len(classes)
#        return freq
