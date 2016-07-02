'''
Created on Jan 27, 2016
@author: camilo
'''


from __future__ import division
import json, os
#from valplots import ExpPlotD
#from statstests import STest
#from numpy import average as avg
from nltk.metrics import f_measure as f1_score
from nltk.metrics import recall as recall_score, precision as precision_score
from nltk.stem import PorterStemmer


class JSON(object):
    '''
    class to collect Precision, Recall, Accuracy and F-1 measures
    '''

    def __init__(self, filepath, name):
        '''
        constructor
        '''
  
        json_data=open(filepath).read().decode('utf-8').encode('utf-8', 'ignore')
        self.data = json.loads(json_data)
        self.name = name 
        
        # all senses
        self.corpus   = []
        self.mmap     = []
        self.wnet     = []
        self.bnet     = []
        self.tagm     = []                   
        
        # stemmer
        self.stemmer = PorterStemmer()
        
        # save stats
        self.csv    = None
        self.g_csv  = None
        self.tex    = None
        self.g_tex  = None
        
    
    def stemWords(self,word):
        '''
        stem words to allow for partial matches
        '''
     
        if " " in word:
            l = word.split(" ")
            r = [self.stemmer.stem(s) for s in l]
            return " ".join(r)
        else:
            return self.stemmer.stem(word)
 
        
    
    def json2file(self):
        '''
        save results to .tex and .csv    
        '''
              
        text_file = open(os.environ['TEX']+self.name+".csv", "w")
        text_file.write(self.g_csv)
        text_file2 = open(os.environ['TEX']+self.name+".tex", "w")
        text_file2.write(self.g_tex)        
        print self.g_csv, "\n"
        print self.g_tex, "\n"        
        text_file.close()
        text_file2.close()     
            

    def process(self,data):
        '''
        collect performance statistics
        '''
        
        for i in range(len(data)):
            
            print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++"
            print "sentence = ", i, str(data[str(i)][1]['Sentence'])
            print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++"
            
            corpus          = data[str(i)][3]['Corpus']
            senses_corpus   = [str(ann['dbid']).encode('utf-8') for ann in corpus] 
            phr_corpus      = [str(ann['phrase']) for ann in corpus]
 
            mmap            = data[str(i)][5]['MetaMap']
            senses_mmap     = [str(ann['dbid'].encode('utf-8')) for ann in mmap]
            phr_mmap        = [str(ann['phrase']) for ann in mmap]           

            wnet            = data[str(i)][4]['WordNet']
            senses_wnet     = [str(ann['dbid'].encode('utf-8')) for ann in wnet]
            phr_wnet        = [str(ann['phrase']) for ann in wnet]            

            bnet            = data[str(i)][2]['BabelFly']                         
            senses_bnet     = [str(ann['dbid'].encode('utf-8')) for ann in bnet]
            phr_bnet        = [str(ann['phrase']) for ann in bnet]
            
            tagm            = data[str(i)][0]['TagMe']             
            senses_tagm     = [str(ann['dbid'].encode('utf-8')) for ann in tagm]
            phr_tagm        = [str(ann['phrase']) for ann in tagm]                                       
            
            # corpus
            print "==============="
            print "corpus phrases\t", phr_corpus
            print "corpus senses\t",  senses_corpus
            print "==============="                   
            self.corpus = self.corpus + senses_corpus                                     
 
            # metamap                  
            sset = set([])
            pred = []    
            if len(senses_corpus)>0:
                for k in range(len(senses_mmap)):
                    for j in range(len(senses_corpus)):
                        if self.stemWords(phr_corpus[j]) == self.stemWords(phr_mmap[k]):
                            sset.add(senses_mmap[k])
            pred = list(sset)                  
            print "------------------------"
            print "MetaMap matches\t", pred              
            self.mmap = self.mmap + pred 
                                     
            # wordnet              
            sset = set([])
            pred = []          
            if len(senses_corpus)>0:
                for k in range(len(senses_wnet)):
                    for j in range(len(senses_corpus)):
                        if phr_corpus[j] == phr_wnet[k]:
                            sset.add(senses_wnet[k])                   
            pred = list(sset)           
            print "WordNet matches\t", pred               
            self.wnet = self.wnet + pred          
   
            # babelnet                
            sset = set([])
            pred = []
            if len(senses_corpus)>0:
                for k in range(len(senses_bnet)):
                    for j in range(len(senses_corpus)):
                        if phr_corpus[j] == phr_bnet[k]:
                            sset.add(senses_bnet[k])
            pred = list(sset)                         
            print "BabelFly matches", pred             
            self.bnet = self.bnet + pred
                  
            # tagme                 
            sset = set([])
            pred = []
            if len(senses_corpus)>0:
                for k in range(len(senses_tagm)):
                    for j in range(len(senses_corpus)):
                        if phr_corpus[j] == phr_tagm[k]:
                            sset.add(senses_tagm[k])       
            pred = list(sset)                                             
            print "TagMe matches\t", pred    
            print "------------------------"  
            self.tagm = self.tagm + pred
            
            
    def computeGlobalStats(self):
        '''
        save global performance statistics
        '''
        
        csv = "(avg.),MetaMap,BabelFly,TagMe,WordNet\n"

        r0 = self.corpus.count('NaN')        
        r1 = self.mmap.count('NaN')
        r2 = self.bnet.count('NaN')     
        r3 = self.tagm.count('NaN')       
        r4 = self.wnet.count('NaN')       
    
        print "\n===================================="
        print "# of CUIs in corpus            =", 428*2  
        print "------------------------------------"            
        print "# of DBpedia senses in corpus  =", len(self.corpus)
        print "# of non-null senses in corpus =", len(self.corpus) - r0       
        print "# of mmap senses               =", len(self.mmap)        
        print "# of mmap non-null senses      =", len(self.mmap) - r1
        print "# of bnet senses               =", len(self.bnet)
        print "# of bnet non-null senses      =", len(self.bnet) - r2
        print "# of tagm senses               =", len(self.tagm)
        print "# of tagm non-null senses      =", len(self.tagm) - r3
        print "# of wnet senses               =", len(self.wnet)  
        print "# of wnet non-null senses      =", len(self.wnet) - r4
        print "====================================\n"                        
 
        mmap_pre = precision_score(set(self.corpus),set(self.mmap))
        bnet_pre = precision_score(set(self.corpus),set(self.bnet))
        tagm_pre = precision_score(set(self.corpus),set(self.tagm))
        wnet_pre = precision_score(set(self.corpus),set(self.wnet)) 
 
        mmap_rec = recall_score(set(self.corpus),set(self.mmap))
        bnet_rec = recall_score(set(self.corpus),set(self.bnet))
        tagm_rec = recall_score(set(self.corpus),set(self.tagm))
        wnet_rec = recall_score(set(self.corpus),set(self.wnet)) 
        
        mmap_f1 = f1_score(set(self.corpus),set(self.mmap))
        bnet_f1 = f1_score(set(self.corpus),set(self.bnet))
        tagm_f1 = f1_score(set(self.corpus),set(self.tagm))
        wnet_f1 = f1_score(set(self.corpus),set(self.wnet))
        
        print "\n===================================="        
        print "# of red. senses in corpus  =", len(set(self.corpus)) 
        print "# of red. mmap senses       =", len(set(self.mmap))   
        print "# of red. bnet senses       =", len(set(self.bnet))        
        print "# of red. tagm senses       =", len(set(self.tagm))  
        print "# of red. wnet senses       =", len(set(self.wnet))                               
        print "====================================\n"          
         
        csv = csv + "Pre," + format(mmap_pre,'.2f')  + ","
        csv = csv + format(bnet_pre,'.2f') + ","
        csv = csv + format(tagm_pre,'.2f') + ","            
        csv = csv + format(wnet_pre,'.2f') + "\n"
         
        csv = csv + "Rec," + format(mmap_rec,'.2f')  + ","
        csv = csv + format(bnet_rec,'.2f') + ","
        csv = csv + format(tagm_rec,'.2f') + ","
        csv = csv + format(wnet_rec,'.2f') + "\n"        
         
        csv = csv + "F-1," + format(mmap_f1,'.2f')  + ","
        csv = csv + format(bnet_f1,'.2f')  + ","
        csv = csv + format(tagm_f1,'.2f') + ","
        csv = csv + format(wnet_f1,'.2f') + "\n" 
        
        self.g_csv = csv.replace("'","")

        # generate .tex table
        tex  = "\\begin{tabular}{ccccc}\n"
        tex  = tex + csv.replace("\n","\\\ \n")
        tex  = tex.replace(","," & ")
        tex  = tex + "\n\end{tabular}"
        self.g_tex = tex     
        
        
#     def computeStats(self): 
#         '''
#         save performance statistics
#         and test for statistical 
#         significance
#         '''                                                                 
#  
#         csv = "(avg.),MetaMap,BabelFly,TagMe,WordNet\n"
#  
#         bnet_acc = avg(self.bnet_a)
#         wnet_acc = avg(self.wnet_a)
#         tagm_acc = avg(self.tagm_a)
#         mmap_acc = avg(self.mmap_a)
# 
#         bnet_rec = avg(self.bnet_r)
#         wnet_rec = avg(self.wnet_r)
#         tagm_rec = avg(self.tagm_r)
#         mmap_rec = avg(self.mmap_r)
# 
#         bnet_pre = avg(self.bnet_p)
#         wnet_pre = avg(self.wnet_p)
#         tagm_pre = avg(self.tagm_p)
#         mmap_pre = avg(self.mmap_p)
#     
#         bnet_f1  = avg(self.bnet_f)
#         wnet_f1  = avg(self.wnet_f)
#         tagm_f1  = avg(self.tagm_f)
#         mmap_f1  = avg(self.mmap_f)
#                        
#         csv = csv + "Acc," + `format(mmap_acc,'.2f')` + ","
#         csv = csv + `format(bnet_acc,'.2f')` + ","
#         csv = csv + `format(tagm_acc,'.2f')` + ","        
#         csv = csv + `format(wnet_acc,'.2f')` + "\n"
#          
#         csv = csv + "Pre," + `format(mmap_pre,'.2f')`  + ","
#         csv = csv + `format(bnet_pre,'.2f')` + ","
#         csv = csv + `format(tagm_pre,'.2f')` + ","            
#         csv = csv + `format(wnet_pre,'.2f')` + "\n"
#          
#         csv = csv + "Rec," + `format(mmap_rec,'.2f')`  + ","
#         csv = csv + `format(bnet_rec,'.2f')` + ","
#         csv = csv + `format(tagm_rec,'.2f')` + ","
#         csv = csv + `format(wnet_rec,'.2f')` + "\n"        
#          
#         csv = csv + "F-1," + `format(mmap_f1,'.2f')`  + ","
#         csv = csv + `format(bnet_f1,'.2f')`  + ","
#         csv = csv + `format(tagm_f1,'.2f')` + ","
#         csv = csv + `format(wnet_f1,'.2f')` + "\n" 
#         
#         self.csv = csv.replace("'","")
# 
#         # generate .tex table
#         tex  = "\\begin{tabular}{ccccc}\n"
#         tex  = tex + self.csv.replace("\n","\\\ \n")
#         tex  = tex.replace(","," & ")
#         tex  = tex + "\n\end{tabular}"
#         self.tex = tex
#         
#         # save files
#         self.json2file("avg")
#         
#         # check for statistically significant differences
#         mys = STest()
#               
#         print "###################################################"        
#         print "TESTS: \taccuracy"
#         print "###################################################"
#         # Kruskal
#         mys.myKruskal(self.mmap_a,self.bnet_a,self.wnet_a,self.tagm_a)
#          
#         print "###################################################"        
#         print "TESTS: \tprecision"
#         print "###################################################"        
#         # Kruskal
#         mys.myKruskal(self.mmap_p,self.bnet_p,self.wnet_p,self.tagm_p)
#        
#         print "###################################################"        
#         print "TESTS: \trecall"
#         print "###################################################"
#         # pairwise Kruskal
#         mys.myKruskal(self.mmap_r,self.bnet_r,self.wnet_r,self.tagm_r)                       
#          
#         print "###################################################"        
#         print "TESTS: \tF-1 measure"
#         print "###################################################"        
#         mys.myKruskal(self.mmap_f,self.bnet_f,self.wnet_f,self.tagm_f)         
# 
#         # generate plot (averages)        
#         ExpPlotD()        