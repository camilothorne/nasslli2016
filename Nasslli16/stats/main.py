#!/usr/bin/python


'''
Created on July 1, 2016
@author: Camilo Thorne
'''


# test
from lexstatistics import MyStats
from pattstats import PattStats


def main():


    # B. Data
    path = "../data/"
    formats = "cli-ques.test"

    # 1. Word distributions:
    # top 80 words
    MyStats(path,formats,80)

    # 2 Patterns
    PattStats(path, formats)


if __name__ == '__main__':
      
      
    '''
    top-level execution
    '''
    
    main()

