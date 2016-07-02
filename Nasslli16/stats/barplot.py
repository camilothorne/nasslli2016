'''
Created on Nov 30, 2012

@author: camilothorne
'''

#===================#
#===================#
#                                                   #
#   Plot Builder                        #
#                                                   #
#===================#
#===================#


from __future__ import division
import array
from matplotlib import pylab, cm
from numpy import *
from operator import itemgetter, attrgetter
import scipy
from time import time


# Class encoding the plot
class MyBarPlot:


    #stats      : corpus statistics
    #classstats : class statistics 
    
    
    #constructor
    def __init__(self,stats,classstats,name):
        self.stats = stats
        self.classstats = classstats
        self.name = name
        self.plotClass(stats,classstats,len(classstats),name)
        
        
    # plotter/container
    def plotClass(self,stats,classstats,c_num,name):
        fig = pylab.figure()
        f_num = len(stats.keys())
        self.plotPer(fig,stats,classstats,f_num,c_num,name)
        self.plotLog(fig,stats,classstats,f_num,c_num,name)
        pylab.ioff()
        #to use if needed
        #mytime = '%.2f' % time()
        mytime = ""
        fig.savefig('/home/camilo/Desktop/'+name+'-stats'+mytime+'.eps') 
        pylab.show()
       
            
    # r-squared correlation coefficient
    def rSquare(self,x, y, coeffs):
        results = {}
        # coefficients
        results['(sl,int)'] = coeffs.tolist()
        # r-squared
        p = scipy.poly1d(coeffs)
        # fit values, and mean
        yhat = [p(z) for z in x]
        ybar = sum(y)/len(y)
        ssreg = sum([ (yihat - ybar)**2 for yihat in yhat])
        sstot = sum([ (yi - ybar)**2 for yi in y])
        results['R^2'] = ssreg / sstot
        print "###################################################"
        print "(sl,int):", results['(sl,int)']
        print "r^2:", results['R^2']
        return results   


    #power-law log-log regression
    def powerLog(self,xdata,ydata):
        logx = log10(xdata+1)
        logy = log10((scipy.array(ydata)+0.01)*100)
        # implements least squares interpolation
        polycoeffs = scipy.polyfit(logx, logy, 1)
        mycoeff = polycoeffs[1]#intercept
        myexp   = polycoeffs[0]#slope
        ploglaw = lambda x, coeff, exp: (exp*x) + coeff
        rqd = self.rSquare(logx, logy, polycoeffs)
        return [rqd,ploglaw(logx,mycoeff,myexp)]
    
    
    #power-law regression
    def powerLaw(self,xdata,ydata):
        # to infer a powerlaw model y = ax^b
        # run a linear regression on log(y) = log(a) + b*log(x)
        logx = log10(xdata+1)
        logy = log10((scipy.array(ydata)+0.01)*100)
        # implements least squares interpolation
        polycoeffs = scipy.polyfit(logx, logy, 1)
        mycoeff = 10.0**polycoeffs[1]   #intercept to slope
        myexp   = polycoeffs[0]         #slope to exponent 
        powerlaw = lambda x, coeff, exp: coeff * (x**exp)
        return powerlaw(xdata,mycoeff,myexp)    
     
     
    #power-law log-log plot   
    def plotLog(self,figu,stats,classstats,f_num,c_num,name):
        ax2 = figu.add_subplot(1,2,2)
        myind = pylab.arange(c_num)
        ind = myind
        log = log10(ind+1)
        logind = log
        width = 0.1
        i = 0
        ctags = []
        mytags = []
        # means
        fmeans = self.defineAvg2(stats,f_num,c_num)
        fmax = fmeans[len(fmeans)-1]
        print fmax, "is max freq"
        # cumul means
        fcumul = self.disCumul(fmeans)
        cumax = log10(fcumul[len(fcumul)-1])
        print "###################################################"
        print cumax, "is max cumul freq"
        # plot log powerlaw (cumul)
        ax2.plot(logind,self.powerLog(ind,fcumul)[1],'-', 
                 color='k')
        ax2.plot(logind,self.powerLog(ind,fmeans)[1],'--', 
                 color='k')        
        ax2.plot(logind,log10((scipy.array(fcumul)+0.01)*100),'o', 
                 color='k')
        ax2.plot(logind,log10((scipy.array(fmeans)+0.01)*100),'x', 
                 color='k')
        # title
        ax2.set_title('log-log best fit ('+name+')\n\n',
                     fontstyle='normal',fontsize='12')
        # setting axis
        ax2.axis([1.05,-0.1,0,7])
        ax2.grid(False)
        # plot legend
        formc = self.powerLog(ind,fcumul)[0]
        formm = self.powerLog(ind,fmeans)[0]
        li = ('best fit (cum.), y = ' + 
              '%.2f' % formc['(sl,int)'][1] + " - " + 
                    '%.2f' % formc['(sl,int)'][0] + 'x, r^2 = ' +
                    '%.2f' % formc['R^2'],
              'best fit (incr.), y = ' + 
              '%.2f' % formm['(sl,int)'][1] + " - " + 
                    '%.2f' % formm['(sl,int)'][0] + 'x, r^2 = ' +
                    '%.2f' % formm['R^2'],
              #'averages (cum.)',
              #'averages (inc..)'
              )
        self.plotLegend(ax2,li)
     
                
    # bar chart + plotter component    
    def plotPer(self,figu,stats,classstats,f_num,c_num,name):
        ax = figu.add_subplot(1,2,1)
        ind = pylab.arange(c_num)
        width = 1
        i = 0
        max = 1
        ctags = []
        mytags = []
        # means
        means = self.defineAvg(stats,f_num,c_num)
        # cumul means
        cumul = self.disCumul(means)
        # plot bars
        self.barPlot(ax,ind,width,f_num,ctags,stats,i)
        # plot means
        ax.plot((ind+width/2),means,'x--',# change line type
                color='k',label="averages (inc.)") # change color
        # plot cumulative distribution
        ax.plot((ind+width/2),cumul,'o-', # change line type
                color='k',label="averages (cum.)") # change color
        # plot labels        
        ax.set_title('Distribution of FO fragments ('+name+')\n\n',
                     fontstyle='normal',fontsize='12')
        # setting axis
        ax.axis([0,c_num,0,max])
        # plot class names
        for c in range(c_num):
            mytags.append(c+(width/2))
        ax.set_xticks(mytags)
        ax.set_xticklabels(ctags,rotation='90')
        ax.grid(False)
        # plot legend
        li = ('averages (inc.)','averages (cum.)',
              'TREC', 'Clinical', 'Geoquery', 'Brown')
        self.plotLegend(ax,li)
     
        
    # plotting the bars in the chart
    def barPlot(self,ax,ind,width,f_num,ctags,stats,i):
        for id in stats.keys():
            classes = stats[id]
            cstats = []
            for clas in classes:
                cstats.append(clas.freq)
            for clas in classes:
                ctags.append(clas.tag)
            flo = 0.75/(i+1)      
            bars = ax.bar(ind,cstats,width/f_num,
                          #color=(cm.hsv(12*(i+1))),linewidth=1,
                          color=""+`flo`+"",linewidth=1,
                          edgecolor='k',label=id)
            for rect in bars:
                rect.set_x(rect.get_x()+(i*(width/f_num)))
            i = i+1
    
            
    # plotting the legend
    def plotLegend(self,ax,li):
        leg = ax.legend(li,shadow=True,loc=0)
        frame  = leg.get_frame()
        #frame.set_facecolor('0.80')     # set the frame face color to light gray
        frame.set_facecolor('1.0')       # set the frame face color to white
        for t in leg.get_texts():
            t.set_fontsize('medium')      # the legend text fontsize
        for l in leg.get_lines():
            l.set_linewidth(1.5)         # the legend line width
            
    
    # computes list of rel freq averages    
    def defineAvg(self,stats,f_num,c_num):
        means = []
        for j in range(c_num):
            meanj = 0
            for id in stats.keys():
                meanj = meanj + stats[id][j].freq
            meanj = (meanj/f_num)
            means.append(meanj)
        means.sort()
        return means
    
    
    # computes list of frequency averages    
    def defineAvg2(self,stats,f_num,c_num):
        means = []
        for j in range(c_num):
            meanj = 0
            for id in stats.keys():
                meanj = meanj + stats[id][j].count
            meanj = ((meanj+1)/f_num)
            #print log10(meanj)
            means.append(meanj)
        means.sort()
        return means
    
    
    # computes list of averages    
    def disCumul(self,means):
        cumul = []
        j = 0
        for mean in means:
            j = mean + j
            cumul.append(j)
        return cumul