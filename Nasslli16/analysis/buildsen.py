'''
Created on Jul 29, 2014
@author: camilothorne
'''


# class to open big files
class OpenFile:
    
    
    # file : name of file
    # lines : file buffered reader
    # bigfile : file
    

    # constructor
    def __init__(self,filename):

        self.file = filename
        self.lines = None
        self.bigfile = open(filename,'r')

            
    # close file
    def myclose(self):  
        
            self.bigfile.close()
            self.destroy()
    

    # buffered reading of file
    def myread(self):    
        
            lines = []
            try:
                lines = self.bigfile.readlines(100000000)
            except:
                print 'error'
            return lines
            
            
    # free memory buffer
    def destroy(self):
        
        self.lines = None
        
        
####################################################################


# class to generate sentences
class MySen:
    
    
        # begin : begin of sentence?
        # end    : end of sentence?
        # sen     : current sentence
        # len     : length of current sentence
        
        
        # init to false, empty sentence      
        def __init__(self):
            
            self.sen      = " "
            self.begin  = False
            self.end     = False
            self.len      = 0
            
            
        # build a sentence
        def buildSen(self,i,lines,my_max):
        
                tokens = lines[i].split()
                if tokens[0] == '<s>':
                    self.begin = True
                    posi = i+1
                    if posi+1 < my_max:          
                        while not(lines[posi+1].split()[0] == '</s>' ):
                            posi = posi + 1
                            tokens = lines[posi].split()
                            self.sen = self.sen + tokens[1]+ '/' + tokens[2] + ' '
                            if posi+1 == my_max:                 
                                break            
                        self.len = posi - (i+1)
                        self.end = True                  
                self.sen = self.sen.lower()
        
        
        # reset object
        def reset(self):
            
            self.sen      = ""
            self.end     = False
            self.begin  = False
            self.len       = 0   