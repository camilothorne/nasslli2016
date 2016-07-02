'''
Created on 2016
@author: camilothorne
'''

#import re, string, array
from subprocess import call
import os


class SaveStat:
    
    
    # path         : path to report file
    # plotfile     : path to the plots
    # tables       : path to the table
    
    
    # constructor
    def __init__(self,table,plotfile1,name):
#         self.path       = "/home/camilo/mmap-wsd/tex/"+name+".tex"
        self.path       = os.environ['TEX']+name+"-report.tex"        
        self.plotfile1  = plotfile1
        self.table      = table
        #print self.table
        # building the report
        res = self.makeRes(self.table, self.plotfile1, name)
        # saving the report
        print "###################################################"
        print "\n\npreparing report...\n\n"
        self.compileFile(self.path, res)
        self.fileSave(self.path, res)
    
        
    # make contingency table   
    def makeRes(self,table,plotfile1,name):
                        
        # plugin table
        title = r'\begin{center}\textbf{\Large '+name+'}\end{center}\n'
        ntable  = title + r'\begin{center}\begin{table}[p]\centering' + "\n"
        #print table
        myfile  = open(table,'r')
        myfiler = myfile.read()
        ntable  = ntable + myfiler
        ntable  = ntable + "\caption{Results.}\end{table}\end{center}\n\n"
        myfile.close()     
        # complete and return table 
        fig1 = r'\begin{center}' + "\n\includegraphics[scale=0.8]{" + plotfile1 + "}\n\end{center}\n"
        res = ntable + "\n\n" + r'\vspace{0.2cm}' + "\n\n" + fig1 + "\\newpage\n" #+ fig2
        return res    
        
    
    # save the table in a .tex file    
    def fileSave(self,path,res):
        myfile = open(path,'w')
        myfile.write(res)
        myfile.close()
    
        
    # compile with pdflatex
    def compileFile(self,path,res):
        myfile = open(path,'w')
        myfile.write("\documentclass[a4paper,12pt]{article}")
        myfile.write("\n\n")
        myfile.write("\usepackage{graphicx}\n")
        myfile.write("\usepackage{epstopdf}\n")
        myfile.write("\usepackage{rotating}\n")
        myfile.write("\usepackage{times}\n")
        myfile.write("\n\n")
        myfile.write(r'\begin{document}')
        myfile.write("\n\n")
        myfile.write(res)
        myfile.write("\n\n")
        myfile.write("\end{document}")
        myfile.close()
        call(['/usr/bin/pdflatex',
#               '-output-directory='+'/home/camilo/workspace-git/RestWSD/results/'+'tex/',
              '-output-directory='+os.environ['TEX'],
              path],
             shell=False)      
