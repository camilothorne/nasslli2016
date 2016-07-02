'''
Created on Jan Feb 26, 2016
@author: camilo
'''


from __future__ import division
import json
#from valplots import ExpPlotD
from nltk.metrics import f_measure as f1_score
from nltk.metrics import recall as recall_score, precision as precision_score
from nltk.stem import PorterStemmer
from sparql import Spar
import time, os


class JSON(object):
    '''
    class to collect Precision, Recall and F-1 measures
    over *effectively DBpedia-linked* (via CUI2DBpedia mappings) phrases
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
 
        # Sparql
        self.spar = Spar()

 
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
        text_file.write(str(self.g_csv))
        text_file2 = open(os.environ['TEX']+self.name+".tex", "w")
        text_file2.write(str(self.g_tex))        
        print self.g_csv, "\n"
        print self.g_tex, "\n"        
        text_file.close()
        text_file2.close()     
            

    def process(self,data,bound):
        '''
        collect performance statistics
        
        (bound should be <= len(data))
        '''
        
        for i in range(bound):
            
            print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++"
            print "sentence = ", `i`, str(data[str(i)][1]['Sentence'])
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
            
            # corpus (filter out phrases with null/empty URIs)
            if senses_corpus[1] == "NaN":
                senses_corpus   = senses_corpus[:1]
                phr_corpus      = phr_corpus[:1]
            if senses_corpus[0] == "NaN":
                senses_corpus   = senses_corpus[1:]
                phr_corpus      = phr_corpus[1:]           
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
            
    
    def uri(self,uri):
        '''
        for monitoring progress
        '''
        
        print uri
        return uri   


    def computeResStats(self):
        '''
        save global performance statistics (resolved)
        '''
        
        csv = "(avg.),MetaMap,BabelFly,TagMe,WordNet\n"
        
        r1 = self.mmap.count('NaN')
        r2 = self.bnet.count('NaN')     
        r3 = self.tagm.count('NaN')       
        r4 = self.wnet.count('NaN')       
    
        print "\n===================================="
        print "# of CUIs in corpus           =", 428*2  
        print "------------------------------------"            
        print "# of DBpedia senses in corpus =", len(self.corpus)
        print "# of mmap senses              =", len(self.mmap)        
        print "# of mmap non-null senses     =", len(self.mmap) - r1
        print "# of bnet senses              =", len(self.bnet)
        print "# of bnet non-null senses     =", len(self.bnet) - r2
        print "# of tagm senses              =", len(self.tagm)
        print "# of tagm non-null senses     =", len(self.tagm) - r3
        print "# of wnet senses              =", len(self.wnet)  
        print "# of wnet non-null senses     =", len(self.wnet) - r4
        print "====================================\n"
        
        print "\n===================================="        
        print "# of red. senses in corpus  =", len(set(self.corpus))
        print "# of red. mmap senses       =", len(set(self.mmap))   
        print "# of red. bnet senses       =", len(set(self.bnet))        
        print "# of red. tagm senses       =", len(set(self.tagm))  
        print "# of red. wnet senses       =", len(set(self.wnet))                               
        print "====================================\n"          
        
        # collapse repetitions
        
        bnet = list(set(self.bnet))
        tagm = list(set(self.tagm))
        wnet = list(set(self.wnet)) 
        
#         mmap = list(set(self.mmap))       
        
        # resolve/normalize URI variants 

        print "resolving annotations...\n"
        count = 0
        for uri1 in set(self.corpus):
            print "resolving URI #", count
            time.sleep(1)
            bnet = [uri1 if self.spar.isEqual(uri1, uri2)==True else uri2 for uri2 in bnet]
            print "bnet updated"
            time.sleep(1)
            tagm = [uri1 if self.spar.isEqual(uri1, uri2)==True else uri2 for uri2 in tagm]
            print "tagm updated"
            time.sleep(1)
            wnet = [uri1 if self.spar.isEqual(uri1, uri2)==True else uri2 for uri2 in wnet]
            print "wnet updated"
            count = count + 1
            
#             mmap = [uri1 if self.spar.isEqual(uri1, uri2)==True else uri2 for uri2 in mmap]
            
        print "annotations resolved!\n"                            
 
        mmap_pre = precision_score(set(self.corpus),set(self.mmap))
#         mmap_pre = precision_score(set(self.corpus),set(mmap))
        bnet_pre = precision_score(set(self.corpus),set(bnet))
        tagm_pre = precision_score(set(self.corpus),set(tagm))
        wnet_pre = precision_score(set(self.corpus),set(wnet)) 
 
        mmap_rec = recall_score(set(self.corpus),set(self.mmap))
#         mmap_rec = recall_score(set(self.corpus),set(mmap))
        bnet_rec = recall_score(set(self.corpus),set(bnet))
        tagm_rec = recall_score(set(self.corpus),set(tagm))
        wnet_rec = recall_score(set(self.corpus),set(wnet)) 
        
        mmap_f1 = f1_score(set(self.corpus),set(self.mmap))
#         mmap_f1 = f1_score(set(self.corpus),set(mmap))        
        bnet_f1 = f1_score(set(self.corpus),set(bnet))
        tagm_f1 = f1_score(set(self.corpus),set(tagm))
        wnet_f1 = f1_score(set(self.corpus),set(wnet))
        
        print set(self.corpus)
        print set(self.mmap)
        print bnet
        print wnet
        print tagm
         
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
        csv = csv + format(wnet_f1,'.2f')
        
        self.g_csv = csv.replace("'","")

        # generate .tex table
        tex  = "\\begin{tabular}{ccccc}\n"
        tex  = tex + csv.replace("\n","\\\ \n")
        tex  = tex.replace(","," & ")
        tex  = tex + "\n\end{tabular}"
        self.g_tex = tex  
          
            
    def computeGlobalStats(self):
        '''
        save global performance statistics
        '''
        
        csv = "(avg.),MetaMap,BabelFly,TagMe,WordNet\n"
        
        r1 = self.mmap.count('NaN')
        r2 = self.bnet.count('NaN')     
        r3 = self.tagm.count('NaN')       
        r4 = self.wnet.count('NaN')       
    
        print "\n===================================="
        print "# of CUIs in corpus           =", 428*2  
        print "------------------------------------"            
        print "# of DBpedia senses in corpus =", len(self.corpus)
        print "# of mmap senses              =", len(self.mmap)        
        print "# of mmap non-null senses     =", len(self.mmap) - r1
        print "# of bnet senses              =", len(self.bnet)
        print "# of bnet non-null senses     =", len(self.bnet) - r2
        print "# of tagm senses              =", len(self.tagm)
        print "# of tagm non-null senses     =", len(self.tagm) - r3
        print "# of wnet senses              =", len(self.wnet)  
        print "# of wnet non-null senses     =", len(self.wnet) - r4
        print "====================================\n" 
        
        print "\n===================================="        
        print "# of red. senses in corpus  =", len(set(self.corpus))
        print "# of red. mmap senses       =", len(set(self.mmap))   
        print "# of red. bnet senses       =", len(set(self.bnet))        
        print "# of red. tagm senses       =", len(set(self.tagm))  
        print "# of red. wnet senses       =", len(set(self.wnet))                               
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
        csv = csv + format(wnet_f1,'.2f')
        
        self.g_csv = csv.replace("'","")

        # generate .tex table
        tex  = "\\begin{tabular}{ccccc}\n"
        tex  = tex + csv.replace("\n","\\\ \n")
        tex  = tex.replace(","," & ")
        tex  = tex + "\n\end{tabular}"
        self.g_tex = tex      
