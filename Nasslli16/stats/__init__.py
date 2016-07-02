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
from boxerstats import *
from pattstats import *


# 0. Corpora root files and format


# N.B. 1. Some corpora are stored in /usr/lib/nltk_lite/
# while custom corpora are stored elsewhere


# A. FOL distribution


#path = "/home/camilo/unison/corpora/aggregations/fol"
#format = ".*test"


# B. Word distributions


#path = "/Users/camilothorne/unison/corpora/aggregations"
#format = "brown-no-tags.txt"


# 1. Word distributions:


#MyStats(path,format,80)


# 2. Fragment distributions:


# 2.1 boxer


#BoxerStats(path, format)


# 2.2 patterns


#PattStats(path, format)


# N.B. 2. Instantiating (1) prevents (2.1) or (2.2) from generating
# a plot object and reciprocally; they should be called
# separately rather than sequentially! 
# They also expect files in different formats (.fol vs.
# .txt)
