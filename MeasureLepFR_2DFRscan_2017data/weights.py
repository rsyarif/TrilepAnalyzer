#!/usr/bin/python

# Json lumi with normtag: BCDEF - https://twiki.cern.ch/twiki/bin/view/CMS/PdmV2017Analysis - Nov 11, 2018.
# 4.823 + 9.664 + 4.252 + 9.278 + 13.540
targetlumi = 41557. # 1/pb  

BR={}
BR['BW'] = 0.5
BR['TZ'] = 0.25
BR['TH'] = 0.25
BR['TTBWBW'] = BR['BW']*BR['BW']
BR['TTTHBW'] = 2*BR['TH']*BR['BW']
BR['TTTZBW'] = 2*BR['TZ']*BR['BW']
BR['TTTZTZ'] = BR['TZ']*BR['TZ']
BR['TTTZTH'] = 2*BR['TZ']*BR['TH']
BR['TTTHTH'] = BR['TH']*BR['TH']

BR['TW'] = 0.5
BR['BZ'] = 0.25
BR['BH'] = 0.25
BR['BBTWTW'] = BR['TW']*BR['TW']
BR['BBBHTW'] = 2*BR['BH']*BR['TW']
BR['BBBZTW'] = 2*BR['BZ']*BR['TW']
BR['BBBZBZ'] = BR['BZ']*BR['BZ']
BR['BBBZBH'] = 2*BR['BZ']*BR['BH']
BR['BBBHBH'] = BR['BH']*BR['BH']


# Number of processed MC events (before selections)
nRun={}

### updated Nov 13, 2018 - start
nRun['WW'] = 7791498. 
nRun['WZ'] = 965938. 
nRun['ZZ'] = 103995630. 
nRun['WWW'] = 203246.  
nRun['WWZ'] = 219964. 	
nRun['WZZ'] = 219660.   
nRun['ZZZ'] = 214318. 	
nRun['TTWl'] = 2678775.  
# nRun['TTWq'] = ??  
nRun['TTZl'] = 3570720.  
# nRun['TTZq'] = ??  
### updated Nov 13, 2018 - end

#### As requested by Cristina Botta (ARC B2G-17-011).
# nRun['TTGJets'] = 4870911* 0.325 #relim estimate: ran 1204482 events, adjusted count 391002. Could assume adjusted = 0.325 * total, from Julie Nov29-2017
# nRun['ZGTo2LG'] = 1579452 #ZG: int 2307158, adjusted count 1579452 , from Julie Nov29-2017
# nRun['TTZToLLM1to10'] = 246792 #DAS
 

nRun_ = {} #so this doesn enter the weights loop at the end. nRun_ != nRun.
nRun_['TTM1000'] = 812636
nRun_['TTM1100'] = 706170
nRun_['TTM1200'] = 767798
nRun_['TTM1300'] = 757036
nRun_['TTM1400'] = 693456
nRun_['TTM1500'] = 661276
nRun_['TTM1600'] = 622818
nRun_['TTM1700'] = 542558
nRun_['TTM1800'] = 455156


defaultBR = {}
defaultBR['BWBW'] = 0.333*0.333
defaultBR['THBW'] = 0.333*0.333*2
defaultBR['TZBW'] = 0.333*0.333*2
defaultBR['TZTZ'] = 0.333*0.333
defaultBR['TZTH'] = 0.333*0.333*2
defaultBR['THTH'] = 0.333*0.333


for decay in ['BWBW','THBW','TZBW','TZTZ','TZTH','THTH']:
	for mass in xrange(1000,1900,100):
		nRun['TTM'+str(mass)+decay] = nRun_['TTM'+str(mass)]*defaultBR[decay]


#BELOW NEEDS UPDATING!! Nov 13, 2018
nRun_['BBM1000'] = 812636
nRun_['BBM1100'] = 812636
nRun_['BBM1200'] = 812636
nRun_['BBM1300'] = 812636
nRun_['BBM1400'] = 812636
nRun_['BBM1500'] = 812636
nRun_['BBM1600'] = 812636
nRun_['BBM1700'] = 812636
nRun_['BBM1800'] = 812636


defaultBR['TWTW'] = 0.333*0.333
defaultBR['BHTW'] = 0.333*0.333*2
defaultBR['BZTW'] = 0.333*0.333*2
defaultBR['BZBZ'] = 0.333*0.333
defaultBR['BZBH'] = 0.333*0.333*2
defaultBR['BHBH'] = 0.333*0.333


for decay in ['TWTW','BHTW','BZTW','BZBZ','BZBH','BHBH']:
	for mass in xrange(1000,1900,100):
		nRun['BBM'+str(mass)+decay] = nRun_['BBM'+str(mass)]*defaultBR[decay]



# Cross sections for MC samples (in pb)
xsec={}
# xsec['DY10to50'] = 18610 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
# xsec['DY50'] = 6025.2 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
# xsec['DY50'] = 5765.4 #1921.8*3 +-0.6*3 (integration err) +- 33.2*3 pb (pdf+alpha_s err) : https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns#DY_Z 

# xsec['DYMG100'] = 147.4*1.23 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
# xsec['DYMG200'] = 40.99*1.23 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
# xsec['DYMG400'] = 5.678*1.23 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
# xsec['DYMG600'] = 1.367*1.23 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
# xsec['DYMG800'] = 0.6304*1.23 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
# xsec['DYMG1200'] = 0.1514*1.23 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
# xsec['DYMG2500'] = 0.003565*1.23 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns

# xsec['TTJets'] = 831.76
# xsec['WJets'] = 61526.7
# xsec['TTJetsPH'] = 831.76 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
# xsec['TTJetsPH0to700inc'] = 831.76
# xsec['TTJetsPH700to1000inc'] = 831.76*0.0921 #(xsec*filtering coeff.)
# xsec['TTJetsPH1000toINFinc'] = 831.76*0.02474 #(xsec*filtering coeff.)
# xsec['TTJetsPH700mtt'] = 831.76*0.0921 #(xsec*filtering coeff.)
# xsec['TTJetsPH1000mtt'] = 831.76*0.02474 #(xsec*filtering coeff.)
# xsec['WJetsMG100'] = 1345.*1.21 # (1.21 = k-factor )# https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
# xsec['WJetsMG200'] = 359.7*1.21 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
# xsec['WJetsMG400'] = 48.91*1.21 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
# xsec['WJetsMG600'] = 12.05*1.21 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
# xsec['WJetsMG800'] = 5.501*1.21 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
# xsec['WJetsMG1200'] = 1.329*1.21 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
# xsec['WJetsMG2500'] = 0.03216*1.21 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns 
xsec['WW'] = 118.7 # https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeVInclusive
# xsec['WZinc'] = 47.13 # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#Diboson
xsec['WZ'] = 4.4297 # WZTo3LNu_13TeV https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#Diboson
# xsec['ZZinc'] = 16.523 # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#Diboson
xsec['ZZ'] = 1.256 # ZZTo4: https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#Diboson
xsec['WWW'] = 0.2086 # from McM Generator Parameters - WWW_4F_TuneCUETP8M1_13TeV-amcatnlo-pythia8 but also https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#Triboson
xsec['WWZ'] = 0.1651 #cs = 0.1651 pb at NLO, frac_negW = 0.0571 (from CMS AN-2015/148) but also https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#Triboson
xsec['WZZ'] = 0.05565 #cs = 0.05565 pb at NLO, frac_negW = 0.0617 (from CMS AN-2015/148) but also https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#Triboson
xsec['ZZZ'] = 0.01398 #cs = 0.01398 pb at NLO, frac_negW = 0.0723 (from CMS AN-2015/148) but also https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#Triboson
xsec['TTZl'] = 0.2529 # from McM but also https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#TT_X
# xsec['TTZq'] = 0.5297 # from McM but also https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#TT_X
xsec['TTWl'] = 0.2043 # from McM but also https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#TT_X
# xsec['TTWq'] = 0.4062 # from McM but also https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#TT_X
# xsec['Tt'] = 216.99/3 #(1/3 was suggested by Thomas Peiffer to account for the leptonic branching ratio)# https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma
# xsec['Ts'] = 11.36/3 #(1/3 was suggested by Thomas Peiffer to account for the leptonic branching ratio)# https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma
# xsec['TtW'] = 35.6 # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma
# xsec['TbtW'] = 35.6 # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma

#### As requested by Cristina Botta (ARC B2G-17-011).
# xsec['TTGJets'] = 3.697 #AN2016_386_v9
# xsec['ZGTo2LG'] = 123.9 #AN2016_386_v9
# xsec['TTZToLLM1to10'] = 0.0493 #AN2016_386_v9

# xsec['TTM700']   = 0.455 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
# xsec['TTM800']  = 0.196 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
# xsec['TTM900']   = 0.0903 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['TTM1000']  = 0.0440 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['TTM1100']  = 0.0224 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['TTM1200'] = 0.0118 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['TTM1300']  = 0.00639 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['TTM1400'] = 0.00354 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['TTM1500']  = 0.00200 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['TTM1600'] = 0.001148 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['TTM1700']  = 0.000666 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['TTM1800'] = 0.000391 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo


# xsec['BBM700']   = 0.455 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
# xsec['BBM800']  = 0.196 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
# xsec['BBM900']   = 0.0903 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['BBM1000']  = 0.0440 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['BBM1100']  = 0.0224 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['BBM1200'] = 0.0118 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['BBM1300']  = 0.00639 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['BBM1400'] = 0.00354 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['BBM1500']  = 0.00200 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['BBM1600'] = 0.001148 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['BBM1700']  = 0.000666 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['BBM1800'] = 0.000391 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo


# xsec['QCDht100'] = 27990000. # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#QCD
# xsec['QCDht200'] = 1712000. # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#QCD 
# xsec['QCDht300'] = 347700. # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#QCD 
# xsec['QCDht500'] = 32100. # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#QCD
# xsec['QCDht700'] = 6831. # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#QCD 
# xsec['QCDht1000'] = 1207. # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#QCD
# xsec['QCDht1500'] = 119.9 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#QCD 
# xsec['QCDht2000'] = 25.24 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#QCD

#energy scale samples (Q^2)
# xsec['TTJetsPHQ2U'] = xsec['TTJetsPH']
# xsec['TTJetsPHQ2D'] = xsec['TTJetsPH']
# xsec['TtWQ2U'] = xsec['TtW']
# xsec['TtWQ2D'] = xsec['TtW']
# xsec['TbtWQ2U'] = xsec['TbtW']
# xsec['TbtWQ2D'] = xsec['TbtW']

# Calculate lumi normalization weights
weight = {}
for sample in sorted(nRun.keys()): 
        if 'BBM' not in sample and 'TTM' not in sample: 
                weight[sample] = (targetlumi*xsec[sample]) / (nRun[sample])
                #print sample, (xsec[sample]) / (nRun[sample])
        else: 
        	#print sample, sample[:2],sample[-4:]
        	weight[sample] = (targetlumi*BR[sample[:2]+sample[-4:]]*xsec[sample[:-4]]) / (nRun[sample])
