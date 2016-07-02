'''
Created on Mar 3, 2016
@author: camilo
'''

from SPARQLWrapper import SPARQLWrapper
from SPARQLWrapper import JSON
import time


class Spar(object):
    '''
    class to query DBpedia for URI identity;
    URIs are identical when connected by 
    page redirects
    '''


    def __init__(self):
        '''
        constructor
        '''
        
        self.sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        self.sparql.addDefaultGraph("http://dbpedia.org")
        
        
    def isEqualTest(self,uri1, uri2):
        '''
        check for identity of URIs (test)
        '''   
           
        spar = ("ASK {<" + uri1 + "> " 
                "(<http://dbpedia.org/ontology/wikiPageRedirects>|"
                "^<http://dbpedia.org/ontology/wikiPageRedirects>)* "
                "<" + uri2 + ">}")
        
        #print spar
        
        return self.evalQuery(spar)


    def isEqual(self,uri1, uri2):
        '''
        check for identity of URIs
        '''   
           
        spar = ("ASK {<" + uri1 + "> " 
                "(<http://dbpedia.org/ontology/wikiPageRedirects>|"
                "^<http://dbpedia.org/ontology/wikiPageRedirects>)* "
                "<" + uri2 + ">}")
        #print self.evalRes(self.evalQuery(spar))
        return True and self.evalRes(self.evalQuery(spar))
        
        
    def evalQuery(self,query):
        '''
        evaluate query remotely
        '''
        
        time.sleep(1) # run one query per second
        try:
            self.sparql.setReturnFormat(JSON)
            self.sparql.setQuery(query)
            print "running", query
            return self.sparql.query().convert()
        except:
            return False
        
        
    def evalRes(self,results):
        '''
        check for value of ask query
        '''
        
        if results == False:
            return results
        else:
            return results['boolean']        
        

    def printRes(self, results):
        '''
        print raw JSON results (tests)
        '''
        
        print results
      
        
    def test(self):
        '''
        test if it works
        '''
        
        uri1 = "http://dbpedia.org/resource/NaN"
        uri2 = "NaN"
        for i in range(20):
            print "query", i, self.isEqual(uri1, uri2)
        
    
# # execute    
# if __name__ == '__main__':
#     sp = Spar()
#     sp.test()   