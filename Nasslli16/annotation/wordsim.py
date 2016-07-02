'''
Created on Jan 12, 2016
@author: camilo
'''

from __future__ import division
from nltk.corpus import wordnet as wn
import json, os
from nltk.metrics import distance as met
import difflib as mydiff
from simplots import ExpPlotC
from statstests import STest
from numpy import average
from gensim.models import Word2Vec


# measure similarity 
class WSD:


    # compute similarity of two words
    def word_similarity(self,w1, w2,sim=wn.path_similarity):
        
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


    # synonymy w.r.t. threshold
    def synonym(self,w1,w2,thrs):
        
        if (self.word_similarity(w1, w2) > thrs):
            return True
        else:
            return False
        

    # compute similarity of two word lists
    def bag_similarity(self,w_list1, w_list2):
        
        set1 = set(w_list1)
        if len(w_list2)==0:
            return 0
        else: 
            set2 = set(w_list2)
            cnt = 0
            for w1 in set1:
                for w2 in set2:
                    if self.synonym(w1,w2,0):
                        cnt = cnt + self.word_similarity(w1, w2, wn.path_similarity)
                    else:
                        if ("_" in w1) & ("_" in w2):
                            l1 = w1.split("_")
                            l2 = w2.split("_")
                            cc = 0
                            for w in l1:
                                for ww in l2:
                                    cc = cc + self.word_similarity(w, ww, wn.path_similarity)
                            cnt = cnt + cc
                        if ("_" in w1) & ("_" not in w2):
                            l1 = w1.split("_")
                            cc = 0
                            for w in l1:
                                cc = cc + self.word_similarity(w, w2, wn.path_similarity)
                            cnt = cnt + cc                           
                        if ("_" not in w1) & ("_" in w2):
                            l2 = w2.split("_")
                            cc = 0
                            for w in l2:
                                cc = cc + self.word_similarity(w1, w, wn.path_similarity)
                            cnt = cnt + cc    
            sim = cnt/(len(set1)+len(set2))          
            return sim 
            
            
    # compute similarity of two word lists
    def synonym_bag(self,w_list1, w_list2):
        
        set1 = set(w_list1)
        if len(w_list2)==0:
            return 0
        else:
            set2 = set(w_list2)
            cnt = 0
            for w1 in set1:
                for w2 in set2:
                    if self.synonym(w1,w2,0.8):
                        cnt = cnt + 1
            sim = cnt/(len(set1)+len(set2))          
            return sim             
    

    # distributional similarity
    def word_dsimilarity(self,word1,word2,model):
        
        try:
            return model.similarity(word1,word2)
        except KeyError:
            return 0    


    # distrib synonymy w.r.t. threshold
    def dsynonym(self, w1, w2, model, thrs):
        
        if (self.word_dsimilarity(w1, w2, model) > thrs):
            return True
        else:
            return False


    # compute distrib similarity of two word lists
    def bag_dsimilarity(self, w_list1, w_list2, model):
        
        set1 = set(w_list1)
        if len(w_list2)==0:
            return 0
        else: 
            set2 = set(w_list2)
            cnt = 0
            for w1 in set1:
                for w2 in set2:
                    if self.dsynonym(w1, w2, model, 0):
                        cnt = cnt + self.word_dsimilarity(w1, w2, model)
                    else:
                        if ("_" in w1) & ("_" in w2):
                            l1 = w1.split("_")
                            l2 = w2.split("_")
                            cc = 0
                            for w in l1:
                                for ww in l2:
                                    cc = cc + self.word_dsimilarity(w, ww, model)
                            cnt = cnt + cc
                        if ("_" in w1) & ("_" not in w2):
                            l1 = w1.split("_")
                            cc = 0
                            for w in l1:
                                cc = cc + self.word_dsimilarity(w, w2, model)
                            cnt = cnt + cc                           
                        if ("_" not in w1) & ("_" in w2):
                            l2 = w2.split("_")
                            cc = 0
                            for w in l2:
                                cc = cc + self.word_dsimilarity(w1, w, model)
                            cnt = cnt + cc    
            sim = cnt/(len(set1)+len(set2))          
            return sim    
    
    
    # compare two bags of words (normalized Levensthein edit distance)    
    def edit_bag(self,w_list1,w_list2):
        
        w1 = " ".join(w_list1)
        w2 = " ".join(w_list2)
        return (met.edit_distance(w1, w2)/max(len(w1),len(w2)))
        
        
    # compare two bags of words (diff distance, normalized)    
    def sequence_bag(self,w_list1,w_list2):
        
        w1 = " ".join(w_list1)
        w2 = " ".join(w_list2)
        return  mydiff.SequenceMatcher(None,w1.lower(),w2.lower()).ratio()
        
        
    # compare two bags of words (jaccard distance, normalized)    
    def jaccard_bag(self,w_list1,w_list2):
        if len(w_list2)==0:
            return 0
        else:     
            return met.jaccard_distance(set(w_list1), set(w_list2))


################################################################################
        

# post-process annotations        
class JSON:
    
        
    # constructor
    def __init__(self,filepath):
        
        json_data=open(filepath).read().decode('utf-8').encode('ascii', 'ignore')
        self.data = json.loads(json_data)
        
        # annotations per method
        self.mmap   = {}
        self.wnet   = {}
        self.bnet   = {}
        self.tagm   = {}
        self.corpus = {}
        
        self.csv    = None
        self.tex    = None 
        self.model  = None
        
    
    # save to csv + tex
    def json2file(self):
        
        text_file = open(os.environ['TEX']+"mmap-eval.csv", "w")
        text_file.write(self.csv)
        text_file2 = open(os.environ['TEX']+"mmap-eval.tex", "w")
        text_file2.write(self.tex)        
        print self.csv, "\n"
        print self.tex, "\n"        
        text_file.close()
        text_file2.close()
        
        
    # batch process (similarity measures)
    def process(self,data):
        
        for i in range(len(data)):

#             # metamap
#             corpus          = data[str(i)][2]['Corpus']
#             senses_corp     = [str(ann['sense']) for ann in corpus]
#             self.corpus[i]  = senses_corp  
            
            # metamap
            mmap            = data[str(i)][2]['MetaMap']
            senses_mmap     = [str(ann['sense']) for ann in mmap]
            self.mmap[i]    = senses_mmap         
            
            # wordnet
            wnet            = data[str(i)][0]['WordNet']
            senses_wnet     = [str(ann['sense']) for ann in wnet]
            self.wnet[i]    = senses_wnet           
                
            # babelnet
            bnet            = data[str(i)][4]['BabelFly']
            senses_bnet     = [str(ann['sense']) for ann in bnet]
            self.bnet[i]    = senses_bnet
                
            # tagme
            tagm            = data[str(i)][0]['TagMe'] 
            senses_tagm     = [str(ann['sense']) for ann in tagm] 
            self.tagm[i]    = senses_tagm 
                            
        csv = "(avg.),BabelFly,TagMe,WordNet\n"
    
        wsd  =  WSD()
    
        tot_bnet_syn = []
        tot_wnet_syn = []
        tot_tagm_syn = []

        tot_bnet_esyn = []
        tot_wnet_esyn = []
        tot_tagm_esyn = []

        tot_bnet_dsyn = []
        tot_wnet_dsyn = []
        tot_tagm_dsyn = []
    
        tot_bnet_jacc = []
        tot_wnet_jacc = []
        tot_tagm_jacc = []
        
        tot_bnet_diff = []
        tot_wnet_diff = []
        tot_tagm_diff = []
        
        tot_bnet_edit = []
        tot_wnet_edit = []
        tot_tagm_edit = []  
        
        
        # print annotation statistics
        
        corpus   = len(self.mmap)
        babelfly = average([len(self.bnet[i]) for i in range(len(self.bnet))]) 
        tagme    = average([len(self.tagm[i]) for i in range(len(self.tagm))])
        metamap  = average([len(self.mmap[i]) for i in range(len(self.mmap))])
        wordnet  = average([len(self.wnet[i]) for i in range(len(self.wnet))])

        print "--------------------------------"        
        print "corpus size (sentences) \t",                           `format(corpus, '.2f')`
        print "--------------------------------"
        print "avg. num. of BabelFly annotations (per sentence) \t",  `format(babelfly, '.2f')`
        print "avg. num. of TagMe annotations (per sentence) \t",     `format(tagme, '.2f')`
        print "avg. num. of MetaMap annotations (per sentence) \t",   `format(metamap, '.2f')`
        print "avg. num. of WordNet annotations (per sentence) \t",   `format(wordnet, '.2f')`   
        
        # initalize word embedding:
        self.model = Word2Vec.load_word2vec_format(os.environ['W2V']+"GoogleNews-vectors-negative300.bin",binary=True)                       
        
        # measures per sentence and method             
    
        for i in range(len(self.mmap)):
        
            w_list1 = self.mmap[i]
            w_list2 = self.bnet[i]
            w_list3 = self.wnet[i]
            w_list4 = self.tagm[i]   
    
            tot_bnet_syn.append(wsd.synonym_bag(w_list1, w_list2))        
            tot_tagm_syn.append(wsd.synonym_bag(w_list1, w_list4))
            tot_wnet_syn.append(wsd.synonym_bag(w_list1, w_list3))
        
            tot_bnet_esyn.append(wsd.bag_similarity(w_list1, w_list2))        
            tot_tagm_esyn.append(wsd.bag_similarity(w_list1, w_list4))
            tot_wnet_esyn.append(wsd.bag_similarity(w_list1, w_list3))           
        
            tot_bnet_dsyn.append(wsd.bag_dsimilarity(w_list1, w_list2, self.model))        
            tot_tagm_dsyn.append(wsd.bag_dsimilarity(w_list1, w_list4, self.model))
            tot_wnet_dsyn.append(wsd.bag_dsimilarity(w_list1, w_list3, self.model))                   
            
            tot_bnet_jacc.append(wsd.jaccard_bag(w_list1, w_list2))        
            tot_tagm_jacc.append(wsd.jaccard_bag(w_list1, w_list4))
            tot_wnet_jacc.append(wsd.jaccard_bag(w_list1, w_list3)) 
            
            tot_bnet_diff.append(wsd.sequence_bag(w_list1, w_list2))        
            tot_tagm_diff.append(wsd.sequence_bag(w_list1, w_list4))
            tot_wnet_diff.append(wsd.sequence_bag(w_list1, w_list3))            
        
            tot_bnet_edit.append(wsd.edit_bag(w_list1, w_list2))        
            tot_tagm_edit.append(wsd.edit_bag(w_list1, w_list4))
            tot_wnet_edit.append(wsd.edit_bag(w_list1, w_list3))                 
        
        csv = csv + "syn," + `format(sum(tot_bnet_syn)/float(len(tot_bnet_syn)),'.2f')` + ","
        csv = csv + `format(sum(tot_tagm_syn)/float(len(tot_tagm_syn)),'.2f')` + ","
        csv = csv + `format(sum(tot_wnet_syn)/float(len(tot_wnet_syn)),'.2f')` + "\n"
        
        csv = csv + "syn+," + `format(sum(tot_bnet_esyn)/float(len(tot_bnet_esyn)),'.2f')`  + ","
        csv = csv + `format(sum(tot_tagm_esyn)/float(len(tot_tagm_esyn)),'.2f')` + ","
        csv = csv + `format(sum(tot_wnet_esyn)/float(len(tot_wnet_esyn)),'.2f')` + "\n"
        
        csv = csv + "dsyn," + `format(sum(tot_bnet_dsyn)/float(len(tot_bnet_dsyn)),'.2f')`  + ","
        csv = csv + `format(sum(tot_tagm_dsyn)/float(len(tot_tagm_dsyn)),'.2f')` + ","
        csv = csv + `format(sum(tot_wnet_dsyn)/float(len(tot_wnet_dsyn)),'.2f')` + "\n"        
        
        csv = csv + "jacc," + `format(sum(tot_bnet_jacc)/float(len(tot_bnet_jacc)),'.2f')`  + ","
        csv = csv + `format(sum(tot_tagm_jacc)/float(len(tot_tagm_jacc)),'.2f')`  + ","
        csv = csv + `format(sum(tot_wnet_jacc)/float(len(tot_wnet_jacc)),'.2f')` + "\n" 
        
        csv = csv + "seq," + `format(sum(tot_bnet_diff)/float(len(tot_bnet_diff)),'.2f')`  + ","
        csv = csv + `format(sum(tot_tagm_diff)/float(len(tot_tagm_diff)),'.2f')`  + ","
        csv = csv + `format(sum(tot_wnet_diff)/float(len(tot_wnet_diff)),'.2f')` + "\n" 
        
        csv = csv + "edit+," + `format(sum(tot_bnet_edit)/float(len(tot_bnet_edit)),'.2f')`  + ","
        csv = csv + `format(sum(tot_tagm_edit)/float(len(tot_tagm_edit)),'.2f')`  + ","
        csv = csv + `format(sum(tot_wnet_edit)/float(len(tot_wnet_edit)),'.2f')`
        
        self.csv = csv.replace("'","")

        # generate .tex table
        tex  = "\\begin{tabular}{cccc}\n"
        tex  = tex + self.csv.replace("\n","\\\ \n")
        tex  = tex.replace(","," & ")
        tex  = tex + "\n\end{tabular}"
        self.tex = tex
        
        self.json2file()
        
        # check for statistically significant differences
        mys = STest()
             
        print "###################################################"        
        print "TESTS: \tsyn+", "(BabelFly vs. WordNet,TagMe)"
        print "###################################################"
        # Kruskal
        mys.myKruskal(tot_bnet_esyn,tot_wnet_esyn,tot_tagm_esyn)
        # pairwise Wilcoxon
        mys.myWilcoxon(tot_wnet_esyn,average(tot_bnet_esyn))
        mys.myWilcoxon(tot_tagm_esyn,average(tot_bnet_esyn)) 
        
        print "###################################################"        
        print "TESTS: \tsyn", "(BabelFly vs. WordNet,TagMe)"
        print "###################################################"        
        # Kruskal
        mys.myKruskal(tot_bnet_syn,tot_wnet_syn,tot_tagm_syn)
        # pairwise Wilcoxon
        mys.myWilcoxon(tot_wnet_syn,average(tot_bnet_syn))
        mys.myWilcoxon(tot_tagm_syn,average(tot_bnet_syn))   
        
        print "###################################################"        
        print "TESTS: \tdsyn", "(BabelFly vs. WordNet,TagMe)"
        print "###################################################"
        # pairwise Kruskal
        mys.myKruskal(tot_bnet_dsyn,tot_wnet_dsyn,tot_tagm_dsyn)
        # pairwise Wilcoxon
        mys.myWilcoxon(tot_wnet_dsyn,average(tot_bnet_dsyn))
        mys.myWilcoxon(tot_tagm_dsyn,average(tot_bnet_dsyn))                           
        
        print "###################################################"        
        print "TESTS: \tjacc", "(BabelFly vs. WordNet,TagMe)"
        print "###################################################"        
        mys.myKruskal(tot_bnet_jacc,tot_wnet_jacc,tot_tagm_jacc)
        
        print "###################################################"        
        print "TESTS: \tseq", "(BabelFly vs. WordNet,TagMe)"
        print "###################################################"        
        mys.myKruskal(tot_bnet_diff,tot_wnet_diff,tot_tagm_diff)
        
        print "###################################################"        
        print "TESTS: \tedit+", "(BabelFly vs. WordNet,TagMe)"
        print "###################################################"        
        mys.myKruskal(tot_bnet_edit,tot_wnet_edit,tot_tagm_edit)            

        # generate plot (averages)        
        ExpPlotC()
