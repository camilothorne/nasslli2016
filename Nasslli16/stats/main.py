#================#
#================#
#                  
#  Stats script     
# (init file)         
#              
#================#
#================#


# test


from lexstatistics import *
from pattstats import *


# B. Data


path = "../data/"
format = "cli-ques.test"


# 1. Word distributions:


MyStats(path,format,80)


# 2 Patterns


PattStats(path, format)

