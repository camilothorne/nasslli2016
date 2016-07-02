'''
Created on Jan 12, 2016
@author: camilo
'''

from __future__ import division
from nltk.corpus import wordnet as wn
import json, os
from nltk.corpus import stopwords
from statstests import STest
from numpy import average
from gensim.models import Word2Vec
from unidecode import unidecode as stru


class WSD:
    '''
    measure similarity
    '''

    def word_similarity(self,w1, w2,sim=wn.path_similarity):
        '''
        WordNet similarity
        '''
        
        synsets1 = wn.synsets(w1,'n') #@UndefinedVariable
        synsets2 = wn.synsets(w2,'n') #@UndefinedVariable
        sim_scores = []
        for synset1 in synsets1:
            for synset2 in synsets2:
                sim_scores.append(sim(synset1, synset2))
        if len(sim_scores) == 0:
            return 0
        else:
            return max(sim_scores)


    def synonym(self,w1,w2,thrs):
        '''
        WordNet synonymy
        '''
        
        if (self.word_similarity(w1, w2) > thrs):
            return True
        else:
            return False          
    
    
    def word_dsimilarity(self, w1, w2, model):
        '''
        distributional similarity
        '''
        
        try:
            return model.similarity(w1, w2)
        except KeyError:
            return 0    


    def dsynonym(self, w1, w2, model, thrs):
        '''
        distributional synonymy
        '''
        
        if (self.word_dsimilarity(w1, w2, model) > thrs):
            return True
        else:
            return False


    def bag_esimilarity(self,w_list1, w_list2):
        '''
        loose WordNet similarity of two word lists/sets
        '''
        
        if (len(w_list2)==0 | len(w_list1)==0):
            return 0
        else:   
            cnt = 0
            siz = 0            
            for w1 in w_list1:
                for w2 in w_list2:
                    if self.synonym(w1, w2, 0):
                        cnt = cnt + self.word_similarity(w1, w2, wn.path_similarity)
                        siz = siz + 1 
            #sim = cnt/(len(w_list1) * len(w_list2))
            sim = cnt/(siz+1)       
            return sim 
            
            
    def bag_similarity(self,w_list1, w_list2):
        '''
        strict WordNet similarity of two word lists/sets
        '''        
      
        if (len(w_list2)==0 | len(w_list1)==0):
            return 0
        else:   
            cnt = 0
            siz = 0            
            for w1 in w_list1:
                for w2 in w_list2:
                    if self.synonym(w1, w2, 0.2):
                        cnt = cnt + self.word_similarity(w1, w2, wn.path_similarity)
                        siz = siz + 1 
            #sim = cnt/(len(w_list1) * len(w_list2))
            sim = cnt/(siz+1)            
            return sim   


    def bag_dsimilarity(self, w_list1, w_list2, model):
        '''
        strict distributional similarity of two word lists/sets
        '''
           
        if (len(w_list2)==0 | len(w_list1)==0):
            return 0
        else: 
            cnt = 0
            siz = 0            
            for w1 in w_list1:
                for w2 in w_list2:
                    if self.dsynonym(w1, w2, model, 0.2):
                        cnt = cnt + self.word_dsimilarity(w1, w2, model)
                        siz = siz + 1 
            #sim = cnt/(len(w_list1) * len(w_list2))
            sim = cnt/(siz+1)              
            return sim 


    def bag_edsimilarity(self, w_list1, w_list2, model):
        '''
        loose distributional similarity of two word lists/sets
        '''
           
        if (len(w_list2)==0 | len(w_list1)==0):
            return 0
        else: 
            cnt = 0
            siz = 0
            for w1 in w_list1:
                for w2 in w_list2:
                    if self.dsynonym(w1, w2, model, 0):
                        cnt = cnt + self.word_dsimilarity(w1, w2, model)
                        siz = siz + 1 
            #sim = cnt/(len(w_list1) * len(w_list2))
            sim = cnt/(siz+1)                     
            return sim    



################################################################################
        
  
class JSON:
    '''
    post-process annotations/glosses
    '''
    

    def __init__(self,filepath,expname):
        '''
        constructor
        '''
        
        json_data=open(filepath).read().decode('utf-8').encode('utf-8', 'ignore')
        self.data = json.loads(json_data)
        
        # annotations per method
        self.mmap   = {}
        self.wnet   = {}
        self.bnet   = {}
        self.tagm   = {}
        self.corpus = {}
        
        # to save results
        self.csv    = None
        self.tex    = None 
        self.model  = None
        
        # name of experiment
        self.name = expname
        
        # remove stop words
        self.stop_words = set(stopwords.words('english'))
        self.stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}']) # remove it if you need punctuation
        
    
    def json2file(self,expname):
        '''
        save to .csv and .tex
        '''
        
        text_file = open(os.environ['TEX']+expname+".csv", "w")
        text_file.write(self.csv)
        text_file2 = open(os.environ['TEX']+expname+".tex", "w")
        text_file2.write(self.tex)        
        print self.csv, "\n"
        print self.tex, "\n"        
        text_file.close()
        text_file2.close()
        
        
    def process(self,data,bound):
        '''
        compute similarity scores, generate plot,
        run statistical tests
        '''
        
        for i in range(bound):

            # metamap
            corpus          = data[str(i)][3]['Corpus']
            senses_corp     = [stru(ann['gloss']).lower().split(" ") for ann in corpus]           
            if (len(senses_corp)==0):
                self.corpus[i] = senses_corp
            else:
                self.corpus[i] = [word for word in reduce(lambda x,y: x+y, senses_corp) 
                                            if word not in self.stop_words] 
            
            # metamap
            mmap            = data[str(i)][5]['MetaMap']
            senses_mmap     = [stru(ann['gloss']).lower().split(" ") for ann in mmap]           
            if (len(senses_mmap)==0):
                self.mmap[i] = senses_mmap
            else:
                self.mmap[i] = [word for word in reduce(lambda x,y: x+y, senses_mmap) 
                                            if word not in self.stop_words]   
            
            # wordnet
            wnet            = data[str(i)][4]['WordNet']
            senses_wnet     = [stru(ann['gloss']).lower().split(" ") for ann in wnet]          
            if (len(senses_wnet)==0):
                self.wnet[i] = senses_wnet
            else:
                self.wnet[i] = [word for word in reduce(lambda x,y: x+y, senses_wnet) 
                                            if word not in self.stop_words]          
                
            # babelnet
            bnet            = data[str(i)][2]['BabelFly']
            senses_bnet     = [stru(ann['gloss']).lower().split(" ") for ann in bnet]  
            if (len(senses_bnet)==0):
                self.bnet[i] = senses_bnet
            else:           
                self.bnet[i] = [word for word in reduce(lambda x,y: x+y, senses_bnet) 
                                            if word not in self.stop_words] 
            
            # tagme
            tagm            = data[str(i)][0]['TagMe'] 
            senses_tagm     = [stru(ann['gloss']).encode('utf-8').lower().split(" ") for ann in tagm]
            if (len(senses_tagm)==0):
                self.tagm[i] = senses_tagm
            else:
                self.tagm[i]    = [word for word in reduce(lambda x,y: x+y, senses_tagm) 
                                            if word not in self.stop_words]
                                    
        csv = "(avg.),MetaMap,BabelFly,TagMe,WordNet\n"
    
        wsd  =  WSD()

        tot_mmap_syn = []    
        tot_bnet_syn = []
        tot_wnet_syn = []
        tot_tagm_syn = []

        tot_mmap_esyn = []
        tot_bnet_esyn = []
        tot_wnet_esyn = []
        tot_tagm_esyn = []

        tot_mmap_dsyn = []
        tot_bnet_dsyn = []
        tot_wnet_dsyn = []
        tot_tagm_dsyn = []    
        
        tot_mmap_edsyn = []
        tot_bnet_edsyn = []
        tot_wnet_edsyn = []
        tot_tagm_edsyn = []

        # print annotation statistics
        
        corp     = len(set(self.corpus))
        corpus   = average([len(set(self.corpus[i])) for i in range(len(set(self.corpus)))])         
        babelfly = average([len(set(self.bnet[i])) for i in range(len(set(self.bnet)))]) 
        tagme    = average([len(set(self.tagm[i])) for i in range(len(set(self.tagm)))])
        metamap  = average([len(set(self.mmap[i])) for i in range(len(set(self.mmap)))])
        wordnet  = average([len(set(self.wnet[i])) for i in range(len(set(self.wnet)))])

        print "\n------------------------------------------------------"        
        print "corpus size (sentences)                    \t",   corp
        print "------------------------------------------------------"
        print "avg. len. of Corpus gloss (per sentence)   \t",   format(corpus, '.2f')        
        print "avg. len. of BabelFly gloss (per sentence) \t",   format(babelfly, '.2f')
        print "avg. len. of TagMe gloss (per sentence)    \t",   format(tagme, '.2f')
        print "avg. len. of MetaMap gloss (per sentence)  \t",   format(metamap, '.2f')
        print "avg. len. of WordNet gloss (per sentence)  \t",   format(wordnet, '.2f')   
        print "------------------------------------------------------\n"
        
        # initalize word embedding:
        print "loading word space...\n"
        self.model = Word2Vec.load_word2vec_format(os.environ['W2V']+"GoogleNews-vectors-negative300.bin",binary=True)                       
        print "computing similarities...\n"        

        # measures per sentence and method 
        for i in range(len(self.corpus)):
        
            w_list0 = set(self.corpus[i])
            w_list1 = set(self.mmap[i])
            w_list2 = set(self.bnet[i])
            w_list3 = set(self.wnet[i])
            w_list4 = set(self.tagm[i])

            tot_mmap_syn.append(wsd.bag_similarity(w_list0, w_list1))      
            tot_bnet_syn.append(wsd.bag_similarity(w_list0, w_list2))
            tot_wnet_syn.append(wsd.bag_similarity(w_list0, w_list3))
            tot_tagm_syn.append(wsd.bag_similarity(w_list0, w_list4))           
  
            tot_mmap_esyn.append(wsd.bag_esimilarity(w_list0, w_list1))      
            tot_bnet_esyn.append(wsd.bag_esimilarity(w_list0, w_list2))        
            tot_wnet_esyn.append(wsd.bag_esimilarity(w_list0, w_list3))           
            tot_tagm_esyn.append(wsd.bag_esimilarity(w_list0, w_list4))
            
            tot_mmap_dsyn.append(wsd.bag_dsimilarity(w_list0, w_list1, self.model))          
            tot_bnet_dsyn.append(wsd.bag_dsimilarity(w_list0, w_list2, self.model))        
            tot_wnet_dsyn.append(wsd.bag_dsimilarity(w_list0, w_list3, self.model))       
            tot_tagm_dsyn.append(wsd.bag_dsimilarity(w_list0, w_list4, self.model))            

            tot_mmap_edsyn.append(wsd.bag_edsimilarity(w_list0, w_list1, self.model))          
            tot_bnet_edsyn.append(wsd.bag_edsimilarity(w_list0, w_list2, self.model))        
            tot_wnet_edsyn.append(wsd.bag_edsimilarity(w_list0, w_list3, self.model))                           
            tot_tagm_edsyn.append(wsd.bag_edsimilarity(w_list0, w_list4, self.model))        
            
        csv = csv + "sy," + format(average(tot_mmap_syn),'.5f') + ","
        csv = csv + format(average(tot_bnet_syn),'.5f') + ","
        csv = csv + format(average(tot_tagm_syn),'.5f') + ","
        csv = csv + format(average(tot_wnet_syn),'.5f') + "\n"
        
        csv = csv + "sy+," + format(average(tot_mmap_esyn),'.5f')  + ","
        csv = csv + format(average(tot_bnet_esyn),'.5f') + ","
        csv = csv + format(average(tot_tagm_esyn),'.5f') + ","
        csv = csv + format(average(tot_wnet_esyn),'.5f') + "\n"
        
        csv = csv + "dsy," + format(average(tot_mmap_dsyn),'.5f')  + ","
        csv = csv + format(average(tot_bnet_dsyn),'.5f') + ","
        csv = csv + format(average(tot_tagm_dsyn),'.5f') + ","
        csv = csv + format(average(tot_wnet_dsyn),'.5f') + "\n"     

        csv = csv + "dsy+," + format(average(tot_mmap_edsyn),'.5f')  + ","
        csv = csv + format(average(tot_bnet_edsyn),'.5f') + ","
        csv = csv + format(average(tot_tagm_edsyn),'.5f') + ","
        csv = csv + format(average(tot_wnet_edsyn),'.5f') + "\n"    
        
        self.csv = csv.replace("'","")

        # generate .tex table
        tex  = "\\begin{tabular}{ccccc}\n"
        tex  = tex + self.csv.replace("\n","\\\ \n")
        tex  = tex.replace(","," & ")
        tex  = tex + "\n\end{tabular}"
        self.tex = tex
        
        self.json2file(self.name)
        
        # check for statistically significant differences
        mys = STest()
             
        print "###################################################"        
        print "TESTS: \tsyn", "(BabelFly vs. WordNet vs. TagMe vs. MetaMap)"
        print "###################################################"
        
        # Kruskal
        mys.myKruskal(tot_bnet_syn,tot_wnet_syn,tot_tagm_syn,tot_mmap_syn)
        
        print "###################################################"        
        print "TESTS: \tsyn+", "(BabelFly vs. WordNet vs. TagMe vs. MetaMap)"
        print "###################################################"        
        
        # Kruskal
        mys.myKruskal(tot_bnet_esyn,tot_wnet_esyn,tot_tagm_esyn,tot_mmap_esyn)
        
        print "###################################################"        
        print "TESTS: \tdsyn", "(BabelFly vs. WordNet vs. TagMe vs. MetaMap)"
        print "###################################################"
        
        # pairwise Kruskal
        mys.myKruskal(tot_bnet_dsyn,tot_wnet_dsyn,tot_tagm_dsyn,tot_mmap_dsyn)

        print "###################################################"        
        print "TESTS: \tdsyn+", "(BabelFly vs. WordNet vs. TagMe vs. MetaMap)"
        print "###################################################"
        
        # pairwise Kruskal
        mys.myKruskal(tot_bnet_edsyn,tot_wnet_edsyn,tot_tagm_edsyn,tot_mmap_edsyn)

