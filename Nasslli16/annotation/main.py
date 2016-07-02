'''
Created on Jan 18, 2016
@author: camilo
'''


from glossim import JSON as SIM                                 #@UnusedImport
from evaluation import JSON as LOOSE                            #@UnusedImport
from strictevaluation import JSON as EVAL                       #@UnusedImport
from strictevaluation import JSON as STRICT                     #@UnusedImport
from simplots import MMStats as SIMStats, ExpPlotC as SPlot     #@UnusedImport
from valplots import MMStats as VALStats, ExpPlotD as VPlot     #@UnusedImport
import os, sys 


def main():
    
    
    '''
    0.1 set the experiments' directories
    '''
  
  
    os.environ['DATA']  = "/home/camilo/mmap-wsd/"                  # directory with input dataset
    os.environ['TEX']   = "/home/camilo/mmap-wsd/tex/"              # directory with .tex and .csv files
    os.environ['W2V']   = "/home/camilo/mmap-wsd/Word2Vec/"         # directory with word embeddings                 
    
    
    '''
    0.2 redirect stdout to log file
    '''    
    
    
    old_stdout          = sys.stdout                                        # redirect stdout             
    log_file            = open(os.environ['DATA']+"word2vec-full-b.log","w")  # log file
    sys.stdout          = log_file                                          # redirect to log
    
    
    '''
    1. process data / collect stats
    '''

    
    # 1.1 process data (similarity)
    jsons =  SIM(os.environ['DATA']+'annotations-wsd.json','word2vec-full') 
    #datas =  jsons.data 
    #jsons.process(datas,len(datas)) 	           # similarity, consider only 1st k sentences, save results
    mys = SIMStats()
    mys.set('word2vec-full')	                   # stats
    SPlot(mys) 					                   # generate plot (averages)


#     # 1.2. process data (strict evaluation)
#     jsone =  EVAL(os.environ['DATA']+'annotations-wsd.json', 'dbpedia-strict-100')
#     myt = VALStats() 
#     datae =  jsone.data
#     jsone.process(datae,100) 			    # evaluation (consider only the 1st k sentences)
#     jsone.computeGlobalStats()      		# compute stats and plots
#     jsone.json2file()               		# save files  
#     myt.set('dbpedia-strict-100')		    # stats
#     VPlot(myt)                      		# generate plot, prepare report    


#     # 1.3. process data (strict evaluation, resolved)
#     jsonf =  STRICT(os.environ['DATA']+'annotations-wsd.json','dbpedia-strict-resolved')
#     myw = VALStats()  
#     dataf =  jsonf.data
#     jsonf.process(dataf,len(dataf))     	    # evaluation (consider only the 1st k sentences)
#     #jsonf.computeResStats()                	# compute stats and plots
#     jsonf.json2file()                       	# save files    
#     myw.set('dbpedia-strict-resolved:')     	# stats
#     VPlot(myw)                              	#generate plot, prepare report  

 
#     # 1.4. process data (loose evaluation)
#     jsong =  LOOSE(os.environ['DATA']+'annotations-wsd.json', 'dbpedia-loose')    
#     myx = VALStats()
#     datag =  jsong.data
#     jsong.process(datag) 			    # evaluation     
#     jsong.computeGlobalStats() 		# compute stats and plots
#     jsong.json2file() 			    # save files, prepare report 
#     myx.set('dbpedia-loose')
#     VPlot(myx) 				        # generate plot   
    
    
#    '''
#    2.1 statistical tests
#    '''
    
#     # 1. test summary stats
#     myt.chi2Tests()         
#     myw.chi2Tests()
#     myx.chi2Tests()

    
    '''
    2.2 test metrics
    '''

    
    mys.otherTests()
#     myt.otherTests()    
#     myw.otherTests() 
#     myx.otherTests()                  


    '''
    2.3 redirect stdout, close log
    '''

    
    sys.stdout = old_stdout
    log_file.close()

   
if __name__ == '__main__':
      
      
    '''
    top-level execution
    '''
         
    main()
