import string, re

# nltk imports:

from nltk.corpus import brown
from nltk import tokenize
from nltk import tag
from itertools import islice
import xml.dom.minidom as minidom

# This class and methods
# open inputs file,
# process them, and write a "clean"
# file with no annotations.

#.Global path of file 

# filename (can be changed)
file   = "clinical3"
# file directory
infile = "/home/camilo/unison/corpora/aggregations/"+file

# Dataformat class

class MyDFormat:
    
    # path:     filepath 
    def __init__(self,infile):
        self.infile = infile
        # method(s) to call 
        self.processXml(infile)
        #self.process2(infile)
        #self.process(infile)
        #self.pos_tag(infile)

    #1. We clean the trec/geo data
    def process(self,infile):
        file = open(infile + ".txt","r")
        out = open(infile + "-clean.txt","w")
        try:
            text = file.read()
            lines = string.split(text, "\n")
            for line in lines:
                line1 = re.sub(".*:"," ",line)
                line1 = re.sub("\[answer\]"," ",line1)
                #line1 = re.sub("\n"," ",line1)
                out.write(line1 + "\n")
                print line1
        except IOError:
                raise IOError()
        file.close()
        out.close()
    
    #2. We clean the gutenberg data:
    def process2(self,infile):
        file = open(infile + ".txt","r")
        out = open(infile + "-clean.txt","w")
        try:
            text = file.read()
            #text = re.sub("\n\n","",text)
            text = re.sub("^[ \t\r\n]+|[ \t\r\n]+"," ",text)
            text = re.sub("('|' )", "",text)
            text = re.sub("--", "",text)
            text = re.sub('\*', "",text)
            text = re.sub('("|" )', "",text)
            #print text + "\n\n"
            lines = string.split(text, "\.")
            for line in lines:
                line1 = re.sub("\. ",".\n\n",line)
                line1 = re.sub("(\! |\!  |\!   )","!\n\n",line1)
                line1 = re.sub("(\? |\?  |\?   )","?\n\n",line1)
                line1 = re.sub("(Dr.|Mr.|No.)+\n\n"," ",line1)
                #line1 = re.sub("( |  )[A-Z]+","[A-Z]+",line1)
                line1 = re.sub("CHAPTER.*", "",line1)
                line1 = re.sub("\[.*", "",line1)
                out.write(line1)
                print line1
        except IOError:
                raise IOError()
        file.close()
        out.close()
    
    #3. POS tagging of the data
    def pos_tag(self,infile):
        train_sents = list(islice(brown.tagged(),1000000))
        trigram_tagger = tag.Trigram()
        trigram_tagger.train(train_sents)
        file = open(infile + ".txt","r")
        out = open(infile + "-tag.txt","w")
        try:
            text = file.read()
            lines = string.split(text, '\n')
            for line in lines:
                tokens = list(tokenize.whitespace(line))
                tagged = list(trigram_tagger.tag(tokens))
                for tags in tagged:
                    print tags
                    if tags[1] == None:
                        out.write(tags[0] + "/" + "NA")
                    else:
                        out.write(tags[0] + "/" + tags[1])
                    out.write(" ")
                out.write("\n")
        except IOError:
                raise IOError()
        file.close()
        out.close()
            
    #4. We extract clinical questions
    def processXml(self,xmlinfile):
        doc = minidom.parse(xmlinfile + ".xml")
        node = doc.documentElement
        out = open(xmlinfile + ".test", "w")
        # lists recovering questions
        questions = doc.getElementsByTagName("original_question")
        gquestions = doc.getElementsByTagName("general_question")
        squestions = doc.getElementsByTagName("short_question")
        # recover questions
        c = 0
        try:
            for ques in questions:
                nodes = ques.childNodes
                for node in nodes:
                    if node.nodeType == node.TEXT_NODE:
                        out.write(node.data)
                        c = c + 1
            print "#########################"
            print `c` + " : orig question"
            for ques in gquestions:
                nodes = ques.childNodes
                for node in nodes:
                    if node.nodeType == node.TEXT_NODE:
                        out.write(node.data)
                        c = c + 1
            print "#########################"
            print `c` + " : gen question"
            for ques in squestions:
                nodes = ques.childNodes
                for node in nodes:
                    if node.nodeType == node.TEXT_NODE:
                        out.write(node.data)
                        c = c + 1
            print "#########################"
            print `c` + " : short question"
        except IOError:
                raise IOError()
        out.close()

# Initialization

MyDFormat(infile)
