## utility libraries
library(Rmisc)
library(infotheo)
library(MASS)
library(car)
library(leaps)
library(xlsx)
library(lme4)
library(optimx)
library(lmerTest)

## linguistic datasets & libraries
library(languageR)
library(zipfR)

## affix productivity data (English)
View(affixProductivity)
str(affixProductivity)

## the productivity prod(x) of affix x is defined as
##
## (*) prod(x) = V(1,x) / h
##
## V(1,affix) 	: |hapax legomena with affix x|
## h		: |hapax legomena|

## mean
mean(affixProductivity$ness)

## median
median(affixProductivity$ness)

## mode
hist(affixProductivity$ness))
plot(density(affixProductivity$ness))

## variance
var(affixProductivity$ness)

## std
std(affixProductivity$ness)

## confidence intervals for mean (c=0.95)
CI(affixProductivity$semi)

## confidence intervals for group means
group.CI(semi~Registers,affixProductivity)

## variance, covariance, correlation
var(affixProductivity$semi)
var(affixProductivity$ness,affixProductivity$en)
cor(affixProductivity$ness,affixProductivity$en)

## regression: linear model
lm(semi~anti+ee+ism+ful,data=affixProductivity)

## regression: explore model
summary(lm(semi~anti+ee+ism+ful,data=affixProductivity))

## regression: diagnostics plots
plot(lm(semi~anti+ee+ism+ful,data=affixProductivity))

## regression: Anova
Anova(lm(semi~anti+ee+ism+ful,data=affixProductivity))

## model selection: does semi depend on any of these?
regsubsets(semi~anti+ee+ism+ful,data=affixProductivity)
plot(regsubsets(semi~anti+ee+ism+ful,data=affixProductivity))

## model selection: does register depend on affixes?
regsubsets(Registers~semi+anti+ee+ism+ful+be+en+ation+ify,data=affixProductivity)
plot(regsubsets(Registers~semi+anti+ee+ism+ful+be+en+ation+ify,data=affixProductivity))

## linear mixed model
data(beginningReaders)
View(beginningReaders)
srt(beginningReaders)
beginningReaders.lmer = lmer(LogRT ~  PC1 + PC2 + PC3  + ReadingScore +OrthLength + I(OrthLength^2) + LogFrequency + LogFamilySize + 
			(1|Word) + (1|Subject) + (0+LogFrequency|Subject) + (0+OrthLength|Subject) + (0+PC1|Subject), 
			data = beginningReaders,control=lmerControl(optimizer="optimx",optCtrl=list(method="nlminb")))
summary(beginningReaders.lmer)

## Alice in Wonderland (array of strings)
alice

## growth statistics
alice.growth = growth.fnc(text = alice, size = 648, nchunks = 40)
plot(alice.growth)
alice.vgc = growth2vgc.fnc(alice.growth)
plot(alice.vgc)

## spectrum statistics
alice.spectrum = spectrum.fnc(alice)
plot(alice.spectrum)
plot(alice.spectrum,xlab="m",ylab="V(m)")

## more on spectra
data(ItaRi.spc)
plot(ItaRi.spc)
plot(ItaRi.spc, log="x")

## more on growth
data(ItaRi.emp.vgc)
N(ItaRi.emp.vgc)
V(ItaRi.emp.vgc)
plot(ItaRi.emp.vgc)
plot(ItaRi.emp.vgc, add.m=1)

## vocabulary growth w.r.t. expectation (0.95 confidence intervals)
data(ItaUltra.spc)
zm <- lnre("zm",ItaUltra.spc)
zm.vgc <- lnre.vgc(zm,(1:100)*70, variances=TRUE)
plt(zm.vgc)

## zipfR example (Baroni & Evert, 2006)
## load Dickens dataset and compute lnre models
data(Dickens.spc)
zm <- lnre("zm",Dickens.spc)
fzm <- lnre("fzm",Dickens.spc, exact=FALSE)
gigp <- lnre("gigp",Dickens.spc)## calculate the corresponding expected
## frequency spectra at the Dickens size
zm.spc <- lnre.spc(zm,N(Dickens.spc))
fzm.spc <- lnre.spc(fzm,N(Dickens.spc))
gigp.spc <- lnre.spc(gigp,N(Dickens.spc))
## comparative plot
plot(Dickens.spc,zm.spc,fzm.spc,gigp.spc,m.max=10)
## expected spectra at N=100e+8
## and comparative plot
zm.spc <- lnre.spc(zm,1e+8)
fzm.spc <- lnre.spc(fzm,1e+8)
gigp.spc <- lnre.spc(gigp,1e+8)
plot(zm.spc,fzm.spc,gigp.spc,m.max=10)
## with variances
zm.spc <- lnre.spc(zm,1e+8,variances=TRUE)
head(zm.spc)
## asking for more than 50 spectrum elements
## (increasing m.max will eventually lead
## to error, at different threshold for
## the different models)
zm.spc <- lnre.spc(zm,1e+8,m.max=1000)
fzm.spc <- lnre.spc(fzm,1e+8,m.max=1000)
gigp.spc <- lnre.spc(gigp,1e+8,m.max=100) ## gigp breaks first!

