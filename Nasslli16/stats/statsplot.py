#===================#
#===================#
#                   #
#   Plot Builder    #
#                   #
#===================#
#===================#


from __future__ import division
import array
import matplotlib as mpl
#mpl.use('Agg') # uncomment to use in environments other than UNIX
from matplotlib import pylab, cm
from numpy import *
from numpy import log10
from operator import itemgetter, attrgetter
import scipy
from time import time
from matplotlib.ticker import FormatStrFormatter


# Class encoding the plot
class MyPlot:


    #stats      : corpus statistics
    #classstats : class statistics
    #name       : title
    #cl         : plot type
    #path       : directory
    #li         : list of corpora


    #constructor
    def __init__(self,stats,classstats,name,cl,path,li):
        self.stats = stats
        self.classstats = classstats
        self.name = name
        self.cl = cl
        self.path = path
        self.li = li
        if self.cl == "one":
            self.plotClass(stats,classstats,len(classstats),name,path,li)
        if self.cl == "two":
            self.plotClass2(classstats,name,path,li)
        if self.cl == "three":
            self.plotClassB(stats,classstats,len(classstats),name,path,li)


    #################################################
    # 1. Class plots:


    # plotter/container 1 (barplot + log-log)
    def plotClass(self,stats,classstats,c_num,name,path,li):
        fig = pylab.figure(figsize=(10,8), dpi=100)
        f_num = len(stats.keys())
        #c_num : # of classes
        #f_num : number of files
        self.plotPer(fig,stats,classstats,f_num,c_num,name,li)
        self.plotLog(fig,stats,classstats,f_num,c_num,name)
        pylab.ioff()
        #to use if needed
        #mytime = '%.2f' % time()
        mytime = ""
        fig.savefig(path+'/'+name.replace(' ', '-')+'-stats'+mytime+'.pdf')
        #pylab.show()


    # plotter/container 2 (barplot)
    def plotClassB(self,stats,classstats,c_num,name,path,li):
        fig = pylab.figure(figsize=(5,8), dpi=100)
        f_num = len(stats.keys())
        #c_num : # of classes
        #f_num : number of files
        self.plotPerB(fig,stats,classstats,f_num,c_num,name,li)
        pylab.ioff()
        #to use if needed
        #mytime = '%.2f' % time()
        mytime = ""
        fig.savefig(path+'/'+name.replace(' ', '-')+'-stats'+mytime+'.pdf')
        #pylab.show()
    

    #################################################
    # Power law curve-fitting:


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
        print "(sl,int) :", results['(sl,int)']
        print "r^2      :", results['R^2']
        return results


    #################################################
    # Computing (cum) mean (rel) frequencies:


    # computes list of rel freq averages
    def defineAvg(self,stats,f_num,c_num):
        means = []
        #print range(c_num)
        for j in range(c_num):
            meanj = 0
            for idf in stats.keys():
                meanj = meanj + stats[idf][j].freq
            meanj = (meanj/f_num)
            means.append(meanj)
        means.sort()
        return means


    # computes list of frequency averages
    def defineAvg2(self,stats,f_num,c_num):
        means = []
        for j in range(c_num):
            meanj = 0
            for idf in stats.keys():
                meanj = meanj + stats[idf][j].count
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


    #################################################
    # Plots:


    #power-law log-log plot
    def plotLog(self,figu,stats,classstats,f_num,c_num,name):
        ax2 = figu.add_subplot(1,2,2)
        myind = pylab.arange(c_num)
        ind = myind
        log = log10(ind+1)
        logind = log
        # avg means
        fmeans = self.defineAvg2(stats,f_num,c_num)
        fmax = fmeans[len(fmeans)-1]
        fmin = fmeans[0]
        print "###################################################"
        print fmax, "= max avg freq"
        print log10(fmax), "= max avg freq (log)"
        print fmin, "= min avg freq"
        print log10(fmin), "= min avg freq (log)"
        # avg cumul means
        fcumul = self.disCumul(fmeans)
        cumax = fcumul[len(fcumul)-1]
        print "###################################################"
        print cumax, "= max avg cumul freq"
        print log10(cumax), "= max avg cumul freq (log)"
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
        ax2.set_title(name+' (log-log best fit)\n\n',
                     fontstyle='normal',fontsize='12')
        # setting axis
        ax2.axis([log10(c_num)+0.5,-0.1,-0.1,log10(cumax)+3.0])
        ax2.grid(False)
        ax2.set_xlabel("log rank",fontsize='12')
        ax2.set_ylabel("log frequency",fontsize='12')
        
        # make the y, x-axis ticks formatted to 1 decimal places
        ax2.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))
        ax2.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
        
        # plot legend
        formc = self.powerLog(ind,fcumul)[0]
        formm = self.powerLog(ind,fmeans)[0]
        li = ('y=' +
              '%.2f' % formc['(sl,int)'][1] + "-" +
                    '%.2f' % formc['(sl,int)'][0] + 'x, R2=' +
                    '%.2f' % formc['R^2'],
              'y=' +
              '%.2f' % formm['(sl,int)'][1] + "-" +
                    '%.2f' % formm['(sl,int)'][0] + 'x, R2=' +
                    '%.2f' % formm['R^2']
              )
        self.plotLegend(ax2,li)


    # class distribution (rel frequency) plot
    def plotPer(self,figu,stats,classstats,f_num,c_num,name,li):
        ax = figu.add_subplot(1,2,1)
        ind = pylab.arange(c_num)
        width = 1
        i = 0
        maxi = 1
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
                color='k',label="relfreq") # change color
        # plot cumulative distribution
        ax.plot((ind+width/2),cumul,'o-', # change line type
                color='k',label="cumulative") # change color
        # plot labels
        ax.set_title(name+'\n\n',
                     fontstyle='normal',fontsize='12')
        # setting axis
        ax.axis([0,c_num,0,maxi])
        # plot class names
        for c in range(c_num):
            mytags.append(c+(width/2))
        ax.set_xticks(mytags)
        ax.set_xticklabels(ctags,rotation='75',fontsize='12')
        ax.grid(False)
        # set y axis label
        ax.set_ylabel("relative frequency",fontsize='12')
        self.plotLegend(ax,li)

    
    # class distribution (rel frequency) plot, no means
    def plotPerB(self,figu,stats,classstats,f_num,c_num,name,li):
        ax = figu.add_subplot(1,1,1)
        ind = pylab.arange(c_num)
        width = 1
        i = 0
        maxi = 1
        ctags = []
        mytags = []
        # means
        means = self.defineAvg(stats,f_num,c_num)
        # cumul means
        cumul = self.disCumul(means)
        # plot bars
        self.barPlot(ax,ind,width,f_num,ctags,stats,i)
        # plot labels
        ax.set_title(name+'\n\n',
                     fontstyle='normal',fontsize='12')
        # setting axis
        ax.axis([0,c_num,0,maxi])
        # plot class names
        for c in range(c_num):
            mytags.append(c+(width/2))
        ax.set_xticks(mytags)
        ax.set_xticklabels(ctags,rotation='75',fontsize='12')
        ax.grid(False)
        # set y axis label
        ax.set_ylabel("relative frequency",fontsize='12')
        self.plotLegend(ax,li)


    #################################################
    # Plotting components:


    # plotting the bars
    def barPlot(self,ax,ind,width,f_num,ctags,stats,i):
        for idf in stats.keys():
            #print idf
            #print stats.keys()
            classes = stats[idf]
            cstats = []
            for clas in classes:
                cstats.append(clas.freq)
            for clas in classes:
                ctags.append(clas.tag)
            flo = 0.75/(i+1)
            bars = ax.bar(ind,cstats,width/f_num,
                          #color=(cm.hsv(12*(i+1))),linewidth=1,
                          color=""+`flo`+"",linewidth=1,
                          edgecolor='k',label=idf)
            #print len(bars)
            for rect in bars:
                rect.set_x(rect.get_x()+(i*(width/f_num)))
            i = i+1


    #################################################
    # 2. Simple plots:


    # plotter/container 2 (simple barplot(s))
    def plotClass2(self,classstats,name,path,li):
        fig = pylab.figure(figsize=(5,8), dpi=100)
        self.plotPerSim(fig, classstats,name,li)
        pylab.ioff()
        #to use if needed
        #mytime = '%.2f' % time()
        mytime = ""
        fig.savefig(path+name+'-stats'+mytime+'.eps')
        fig.savefig(path+name+'-stats'+mytime+'.pdf')
        pylab.show()


    # simple barplot (no grouping into classes)
    def plotPerSim(self,figu,classstats,name,li):
        ax = figu.add_subplot(1,1,1)
        labels = []
        stats  = []
        for cls in classstats:
            for cl in cls.classes:
                stats.append(cl.freq)
                for i in range(len(cl.fileid)):
                    if cl.fileid[i]=="-":
                        labels.append(cl.fileid[:i])
                        break
        num_items = len(stats)
        ind = pylab.arange(num_items)
        width = 1
        maxi  = 1
        xdata = ind
        # plot labels
        ax.set_ylabel("frequency\n",fontsize='12')
        ax.set_title(name+'\n\n',
                     fontstyle='normal',fontsize='12')
        ax.set_xticks(ind+(width/2))
        ax.set_xticklabels(labels)
        ax.set_xticklabels(labels,rotation='45',fontsize='12')
        # setting axis
        ax.axis([0,num_items,0,maxi])
        # plotting bars
        for i in range(len(stats)):
            if i <= 1:
                flo = (i+1)/(i+2)
                gene_rects = ax.bar(xdata[i], stats[i], width,
                                    color=""+`flo`+"",
                                    edgecolor='k' )
            else:
                flo = (4+1)/(4+2)
                gene_rects = ax.bar(xdata[i], stats[i], width,
                                    color=""+`flo`+"",
                                    edgecolor='k' )

        # plot values
        ax.plot(ind+(width/2),stats,'o-',# change line type
             color='k') # change color
        ax.grid(False)
        self.plotLegend(ax,li)


    #################################################
    # 3. Common to all methods:


    # plotting the legend of plots
    def plotLegend(self,ax,li):
        leg = ax.legend(li,shadow=True,loc=0)
        frame  = leg.get_frame()
        #frame.set_facecolor('0.80')     # set the frame face color to light gray
        frame.set_facecolor('1.0')       # set the frame face color to white
        for t in leg.get_texts():
            #t.set_fontsize('medium')    # the legend text fontsize
            t.set_fontsize('12')         # the legend text fontsize
        for l in leg.get_lines():
            l.set_linewidth(1.5)         # the legend line width

