#!/usr/bin/python


'''
Created on July 1, 2016
@author: Camilo Thorne
'''


# custom libraries
import sys
sys.path.append(u'../stats/')


#================#
#================#
#
#  Stats script
#  (init file)   
#
#================#
#================#


# analysis functions
from dpatterns import ProporStatsPD


def main():
    '''
    main
    '''

    # corpora root files and format
    plotting      = '/home/camilo/wacky-corpus/wackypedia/plotting/'
    path          = "/home/camilo/wacky-corpus/wackypedia/"

    #fformat        = ".*test"      # test 1
    fformat        = ".*testa"     # test 2

    # listA          = ('mean','cumul','wacky','stut')
    # listB          = ('wacky','stut')

    listA          = ('mean','cumul','wackypedia')
    listB          = ('wackypedia','')

    # by disjoint pattern
    ProporStatsPD(path, fformat, listB, plotting)


if __name__ == '__main__':     
      
    '''
    top-level execution
    '''
         
    main()
