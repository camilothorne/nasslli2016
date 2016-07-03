from subprocess import call, Popen


class SaveStats:


    # path         : path to report file
    # classstats   : class stats
    # stats        : filestats


    # constructor
    def __init__(self,classstats,stats,plotfile,path,report):
        
        self.classstats = classstats
        self.stats = stats
        
        # building the report, saving the tables
        resD = self.makeCSVB(self.classstats, self.stats)
        
        print "\n"+resD
        print path
        
        #self.fileSave(path + ".txt", resL)
        self.fileSave(path + "-B.csv", resD)                   


    # write down complexities and lengths (in number of words)
    def printRest(self,classtats):
        rows = ""
        if len(classtats) > 3:
            rows = rows + "len,2,2,1,4,4,2,4,4,1,2,1,1,1" + "\n"
            rows = rows + "comp,k-FA,k-FA,PDA,PDA,PDA,PDA,PDA,PDA,PDA,PDA,k-FA,2-FA,PDA" + "\n"            
            return rows
        else:
            rows = rows + "comp,PDA,k-FA,2-FA" + "\n"
            return rows
    
    
    # make full csv table (second method)
    def makeCSVB(self,classstats,stats):   

        # print class names
        table = "Num \t GQ \t Freq\n"
        
        num = 1
        for cla in classstats:
            #for idf in cla.classes:
            freq = cla.fre
            mytag =  cla.tag.split("|")[0][2:len(cla.tag.split("|")[0])]
            table = table + `num` + " \t " + mytag + " \t " + `freq` + "\n"
            num = num + 1

        # return table
        return table    


    # save the table in a file
    def fileSave(self,path,res):
        myfile = open(path,'w')
        myfile.write(res)
        myfile.close()
