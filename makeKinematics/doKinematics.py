#!/usr/bin/python

import os,sys,time,math,datetime,fnmatch,pickle
from numpy import linspace
from weights import *
from analyze import *
from samples import *
import ROOT as R

R.gROOT.SetBatch(1)
start_time = time.time()

###########################################################
#################### CUTS & OUTPUT ########################
###########################################################

cutList = {'isPassTrig': 0, 
		   'isPassTrig_dilep': 1,
		   'isPassTrig_dilep_anth': 0,
		   'isPassTrig_trilep': 0, 
		   'isPassTrilepton': 1,
		   'lep1PtCut': 0, #40, #0, #
		   'leadJetPtCut':0,#150, #300, #0, #
		   'subLeadJetPtCut':0, #75, #150, #0, #
		   'thirdJetPtCut':0, #30, #100, #0, #
		   'metCut': 20,#60, #75, #0, #
		   'njetsCut': 2, 
		   'nbjetsCut':0, #1,
		   'drCut':0, #1.0, #
	   	   'stCut':0,
	   	   'mllOSCut':0,
		   }

doAllSys= True

cutString = 'isPassTrig_All'+str(int(cutList['isPassTrig']))+'_'+'dilep'+str(int(cutList['isPassTrig_dilep']))+'_'+'dilepAnth'+str(int(cutList['isPassTrig_dilep_anth']))+'_'+'trilep'+str(int(cutList['isPassTrig_trilep']))+'_'+'isPassTrilepton'+str(int(cutList['isPassTrilepton']))+'_lep1Pt'+str(int(cutList['lep1PtCut']))+'_NJets'+str(int(cutList['njetsCut']))+'_NBJets'+str(int(cutList['nbjetsCut']))+'_DR'+str(int(cutList['drCut']))+'_ST'+str(int(cutList['stCut']))+'_MllOS'+str(int(cutList['mllOSCut']))
# cutString = 'isPassTrig'+str(int(cutList['isPassTrig']))+'_'+'isPassTrig_dilep'+str(int(cutList['isPassTrig_dilep']))+'_'+'isPassTrig_dilepHT'+str(int(cutList['isPassTrig_dilepHT']))+'_'+'isPassTrig_trilep'+str(int(cutList['isPassTrig_trilep']))+'_'+'isPassTrilepton'+str(int(cutList['isPassTrilepton']))+'_'+'lep'+str(int(cutList['lepPtCut']))+'_NJets'+str(int(cutList['njetsCut']))+'_NBJets'+str(int(cutList['nbjetsCut']))+'_DR'+str(int(cutList['drCut']))+'_ST'+str(int(cutList['stCut']))
# cutString = 'lep'+str(int(cutList['lepPtCut']))+'_MET'+str(int(cutList['metCut']))+'_leadJet'+str(int(cutList['leadJetPtCut']))+'_subLeadJet'+str(int(cutList['subLeadJetPtCut']))+'_thirdJet'+str(int(cutList['thirdJetPtCut']))+'_NJets'+str(int(cutList['njetsCut']))+'_NBJets'+str(int(cutList['nbjetsCut']))+'_DR'+str(int(cutList['drCut']))+'_ST'+str(int(cutList['stCut']))

# pfix='kinematics_80x_Exactly3Lep_2016_9_8'
# pfix='kinematics_80x_condor_Exactly3Lep_no2Dcut_noMllOScut_2016_9_8'

#pfix='kinematics_80x_Exactly3Lep_2016_9_14'

pfix='kinematics_80x_Exactly3Lep_2016_9_19'


# outDir = os.getcwd()+'/'
outDir = '/user_data/rsyarif/'
# outDir+=pfix+'/'
outDir+=pfix+'/'+cutString


isEMlist = ['EEE','EEM','EMM','MMM','All']

###########################################################
#################### SAMPLE GROUPS ########################
###########################################################

whichSignal = 'TT' #TT, BB, or T53T53
signalMassRange = [800,1800]
signals = [whichSignal+'M'+str(mass) for mass in range(signalMassRange[0],signalMassRange[1]+100,100)]
if whichSignal=='T53T53': signals = [whichSignal+'M'+str(mass)+chiral for mass in range(signalMassRange[0],signalMassRange[1]+100,100) for chiral in ['left','right']]
if whichSignal=='TT': decays = ['BWBW','THTH','TZTZ','TZBW','THBW','TZTH'] #T' decays
if whichSignal=='BB': decays = ['TWTW','BHBH','BZBZ','BZTW','BHTW','BZBH'] #B' decays
if whichSignal=='T53T53': decays = [''] #decays to tWtW 100% of the time
sigList = {signal+decay:(signal+decay).lower() for signal in signals for decay in decays}

# bkgStackList = ['WJets','VV','TTV','TTJets','T','QCD','ddbkg']
# bkgStackList = ['VV','VVV','TTV','ddbkg']
bkgStackList = ['VV','WZ','ZZ','VVV','TTV','ddbkg']
# wjetList  = ['WJetsMG100','WJetsMG200','WJetsMG400','WJetsMG600','WJetsMG800','WJetsMG1200','WJetsMG2500']
# zjetList  = ['DY50']
# vvList    = ['WW','WZ','ZZ']
vvList    = ['WZ','ZZ']
wzList    = ['WZ']
zzList    = ['ZZ']
vvvList   = ['WWW','WWZ','WZZ','ZZZ']
# ttvList   = ['TTWl','TTWq','TTZl','TTZq']
ttvList   = ['TTWl','TTZl']
# ttjetList = ['TTJetsPH0to700inc','TTJetsPH700to1000inc','TTJetsPH1000toINFinc','TTJetsPH700mtt','TTJetsPH1000mtt']
# ttjetList = ['TTJetsPH']
tList     = ['Tt','Ts','TtW','TbtW']

dataList = ['DataEEPRD','DataEEPRC','DataEEPRB','DataMMPRD','DataMMPRC','DataMMPRB','DataMEPRD','DataMEPRC','DataMEPRD']
# dataList = ['DataEPRD','DataEPRC','DataEPRB','DataMPRD','DataMPRC','DataMPRD']
signalList = [signal+decay for signal in signals for decay in decays]
# topList = ['TTWl','TTZl','TTWq','TTZq'] #NoTTJets, No singleT
topList = ['TTWl','TTZl'] #NoTTJets, No singleT
# topList = ['TTJetsPH0to700inc','TTJetsPH700to1000inc','TTJetsPH1000toINFinc','TTJetsPH700mtt','TTJetsPH1000mtt','TTWl','TTZl','TTWq','TTZq','Tt','Ts','TtW','TbtW']
#topList = ['TTJetsPH','TTWl','TTZl','TTWq','TTZq','Tt','Ts','TtW','TbtW']
ewkList = ['WZ','ZZ','WWW','WWZ','WZZ','ZZZ'] #No DY, WJets, WW
# ewkList = ['DY50','WJetsMG100','WJetsMG200','WJetsMG400','WJetsMG600','WJetsMG800','WJetsMG1200','WJetsMG2500','WW','WZ','ZZ','WWZ','WZZ','ZZZ']
# qcdList = ['QCDht100','QCDht200','QCDht300','QCDht500','QCDht700','QCDht1000','QCDht1500','QCDht2000']
ddbkgList = ['DataDrivenBkgEEPRB','DataDrivenBkgEEPRC','DataDrivenBkgEEPRD','DataDrivenBkgMMPRB','DataDrivenBkgMMPRC','DataDrivenBkgMMPRD','DataDrivenBkgMEPRB','DataDrivenBkgMEPRC','DataDrivenBkgMEPRD']

ddbkgTTTList = ['DataDrivenBkgTTTEEPRB','DataDrivenBkgTTTEEPRC','DataDrivenBkgTTTEEPRD','DataDrivenBkgTTTMMPRB','DataDrivenBkgTTTMMPRC','DataDrivenBkgTTTMMPRD','DataDrivenBkgTTTMEPRB','DataDrivenBkgTTTMEPRC','DataDrivenBkgTTTMEPRD']

ddbkgTTLList = ['DataDrivenBkgTTLEEPRB','DataDrivenBkgTTLEEPRC','DataDrivenBkgTTLEEPRD','DataDrivenBkgTTLMMPRB','DataDrivenBkgTTLMMPRC','DataDrivenBkgTTLMMPRD','DataDrivenBkgTTLMEPRB','DataDrivenBkgTTLMEPRC','DataDrivenBkgTTLMEPRD']
ddbkgTLTList = ['DataDrivenBkgTLTEEPRB','DataDrivenBkgTLTEEPRC','DataDrivenBkgTLTEEPRD','DataDrivenBkgTLTMMPRB','DataDrivenBkgTLTMMPRC','DataDrivenBkgTLTMMPRD','DataDrivenBkgTLTMEPRB','DataDrivenBkgTLTMEPRC','DataDrivenBkgTLTMEPRD']
ddbkgLTTList = ['DataDrivenBkgLTTEEPRB','DataDrivenBkgLTTEEPRC','DataDrivenBkgLTTEEPRD','DataDrivenBkgLTTMMPRB','DataDrivenBkgLTTMMPRC','DataDrivenBkgLTTMMPRD','DataDrivenBkgLTTMEPRB','DataDrivenBkgLTTMEPRC','DataDrivenBkgLTTMEPRD']

ddbkgTLLList = ['DataDrivenBkgTLLEEPRB','DataDrivenBkgTLLEEPRC','DataDrivenBkgTLLEEPRD','DataDrivenBkgTLLMMPRB','DataDrivenBkgTLLMMPRC','DataDrivenBkgTLLMMPRD','DataDrivenBkgTLLMEPRB','DataDrivenBkgTLLMEPRC','DataDrivenBkgTLLMEPRD']
ddbkgLTLList = ['DataDrivenBkgLTLEEPRB','DataDrivenBkgLTLEEPRC','DataDrivenBkgLTLEEPRD','DataDrivenBkgLTLMMPRB','DataDrivenBkgLTLMMPRC','DataDrivenBkgLTLMMPRD','DataDrivenBkgLTLMEPRB','DataDrivenBkgLTLMEPRC','DataDrivenBkgLTLMEPRD']
ddbkgLLTList = ['DataDrivenBkgLLTEEPRB','DataDrivenBkgLLTEEPRC','DataDrivenBkgLLTEEPRD','DataDrivenBkgLLTMMPRB','DataDrivenBkgLLTMMPRC','DataDrivenBkgLLTMMPRD','DataDrivenBkgLLTMEPRB','DataDrivenBkgLLTMEPRC','DataDrivenBkgLLTMEPRD']

ddbkgLLLList = ['DataDrivenBkgLLLEEPRB','DataDrivenBkgLLLEEPRC','DataDrivenBkgLLLEEPRD','DataDrivenBkgLLLMMPRB','DataDrivenBkgLLLMMPRC','DataDrivenBkgLLLMMPRD','DataDrivenBkgLLLMEPRB','DataDrivenBkgLLLMEPRC','DataDrivenBkgLLLMEPRD']


# systematicList = ['pileup','jec','jer','jsf','jmr','jms','btag','tau21','pdfNew','muR','muF',
# 				  'muRFcoPRC','toppt','muRFcorrdNew','muRFdecorrdNew','PR','FR']
# systematicList = ['pileup','jec','jer','jsf','btag','pdfNew','muR','muF',
# 				  'muRFcoPRC','muRFcorrdNew','muRFdecorrdNew','PR','FR']
systematicList = ['PR','FR']


###########################################################
#################### NORMALIZATIONS #######################
###########################################################

lumiSys = 0.062 #6.2% https://twiki.cern.ch/twiki/bin/view/CMS/TWikiLUM - 20Sep2016
trigSys = 0.03 #3% trigger uncertainty - AN 2016 229
lepIdSys = math.sqrt(3.*0.01**2) #1% lepton id uncertainty ## NEED to add in quadrature for 3 leptons! - ATTENTION! NEED UPDATING!
lepIsoSys = math.sqrt(3.*0.01**2) #1% lepton isolation uncertainty ## NEED to add in quadrature for 3 leptons! - ATTENTION! NEED UPDATING!
topXsecSys = 0.0 #55 #5.5% top x-sec uncertainty
ewkXsecSys = 0.0 #5 #5% ewk x-sec uncertainty
qcdXsecSys = 0.0 #50 #50% qcd x-sec uncertainty
corrdSys = math.sqrt(lumiSys**2+trigSys**2+lepIdSys**2+lepIsoSys**2)

def round_sig(x,sig=2):
	try:
		return round(x, sig-int(math.floor(math.log10(abs(x))))-1)
	except:
		return round(x,5)

###########################################################
######### GROUP SAMPLES AND PRINT YIELDS/UNCERTS ##########
###########################################################
def makeCats(datahists,sighists,bkghists,discriminant):
	## Input  histograms (datahists,sighists,bkghists) must have corresponding histograms returned from analyze.py##
	
	## INITIALIZE DICTIONARIES FOR YIELDS AND STATISTICAL UNCERTAINTIES ##
	yieldTable = {}
	yieldErrTable = {} #what is actually stored here is the square of the yield error
	for isEM in isEMlist:
		histoPrefix=discriminant+'_'+lumiStr+'fb_'+isEM
		yieldTable[histoPrefix]={}
		yieldErrTable[histoPrefix]={}
		if doAllSys:
			for systematic in systematicList:
				for ud in ['Up','Down']:
					yieldTable[histoPrefix+systematic+ud]={}
	
	## WRITING HISTOGRAMS IN ROOT FILE ##
	outputRfile = R.TFile(outDir+'/templates_'+discriminant+'_'+lumiStr+'fb.root','RECREATE')
	hsig,htop,hewk,hqcd,hdata={},{},{},{},{}
	hwjets,hzjets,httjets,ht,httv,hvv,hwz,hzz,hvvv={},{},{},{},{},{},{},{},{}
	hddbkg,hddbkgTTT,hddbkgTTL,hddbkgTLT,hddbkgLTT,hddbkgTLL,hddbkgLTL,hddbkgLLT,hddbkgLLL={},{},{},{},{},{},{},{},{}
	for isEM in isEMlist:
		histoPrefix=discriminant+'_'+lumiStr+'fb_'+isEM

		#Group processes
# 		hwjets[isEM] = bkghists[histoPrefix+'_'+wjetList[0]].Clone(histoPrefix+'_WJets')
# 		hzjets[isEM] = bkghists[histoPrefix+'_'+zjetList[0]].Clone(histoPrefix+'_ZJets')
# 		httjets[isEM] = bkghists[histoPrefix+'_'+ttjetList[0]].Clone(histoPrefix+'_TTJets')
# 		ht[isEM] = bkghists[histoPrefix+'_'+tList[0]].Clone(histoPrefix+'_T')
		httv[isEM] = bkghists[histoPrefix+'_'+ttvList[0]].Clone(histoPrefix+'_TTV')
		hvv[isEM] = bkghists[histoPrefix+'_'+vvList[0]].Clone(histoPrefix+'_VV')
		hwz[isEM] = bkghists[histoPrefix+'_'+wzList[0]].Clone(histoPrefix+'_WZ')
		hzz[isEM] = bkghists[histoPrefix+'_'+zzList[0]].Clone(histoPrefix+'_ZZ')
		hvvv[isEM] = bkghists[histoPrefix+'_'+vvvList[0]].Clone(histoPrefix+'_VVV')
		hddbkg[isEM] = bkghists[histoPrefix+'_'+ddbkgList[0]].Clone(histoPrefix+'_ddbkg')
		hddbkgTTT[isEM] = bkghists[histoPrefix+'_'+ddbkgTTTList[0]].Clone(histoPrefix+'_ddbkgTTT')

		hddbkgTTL[isEM] = bkghists[histoPrefix+'_'+ddbkgTTLList[0]].Clone(histoPrefix+'_ddbkgTTL')
		hddbkgTLT[isEM] = bkghists[histoPrefix+'_'+ddbkgTLTList[0]].Clone(histoPrefix+'_ddbkgTLT')
		hddbkgLTT[isEM] = bkghists[histoPrefix+'_'+ddbkgLTTList[0]].Clone(histoPrefix+'_ddbkgLTT')

		hddbkgTLL[isEM] = bkghists[histoPrefix+'_'+ddbkgTLLList[0]].Clone(histoPrefix+'_ddbkgTLL')
		hddbkgLTL[isEM] = bkghists[histoPrefix+'_'+ddbkgLTLList[0]].Clone(histoPrefix+'_ddbkgLTL')
		hddbkgLLT[isEM] = bkghists[histoPrefix+'_'+ddbkgLLTList[0]].Clone(histoPrefix+'_ddbkgLLT')

		hddbkgLLL[isEM] = bkghists[histoPrefix+'_'+ddbkgLLLList[0]].Clone(histoPrefix+'_ddbkgLLL')


# 		for bkg in ttjetList:
# 			if bkg!=ttjetList[0]: httjets[isEM].Add(bkghists[histoPrefix+'_'+bkg])
# 		for bkg in wjetList:
# 			if bkg!=wjetList[0]: hwjets[isEM].Add(bkghists[histoPrefix+'_'+bkg])
		for bkg in ttvList:
			if bkg!=ttvList[0]: httv[isEM].Add(bkghists[histoPrefix+'_'+bkg])
# 		for bkg in tList:
# 			if bkg!=tList[0]: ht[isEM].Add(bkghists[histoPrefix+'_'+bkg])
# 		for bkg in zjetList:
# 			if bkg!=zjetList[0]: hzjets[isEM].Add(bkghists[histoPrefix+'_'+bkg])
		for bkg in vvList:
			if bkg!=vvList[0]: hvv[isEM].Add(bkghists[histoPrefix+'_'+bkg])
		for bkg in wzList:
			if bkg!=wzList[0]: hwz[isEM].Add(bkghists[histoPrefix+'_'+bkg])
		for bkg in zzList:
			if bkg!=zzList[0]: hzz[isEM].Add(bkghists[histoPrefix+'_'+bkg])
		for bkg in vvvList:
			if bkg!=vvvList[0]: hvvv[isEM].Add(bkghists[histoPrefix+'_'+bkg])
		for bkg in ddbkgList:
			if bkg!=ddbkgList[0]: hddbkg[isEM].Add(bkghists[histoPrefix+'_'+bkg])

		for bkg in ddbkgTTTList:
			if bkg!=ddbkgTTTList[0]: hddbkgTTT[isEM].Add(bkghists[histoPrefix+'_'+bkg])

		for bkg in ddbkgTTLList:
			if bkg!=ddbkgTTLList[0]: hddbkgTTL[isEM].Add(bkghists[histoPrefix+'_'+bkg])
		for bkg in ddbkgTLTList:
			if bkg!=ddbkgTLTList[0]: hddbkgTLT[isEM].Add(bkghists[histoPrefix+'_'+bkg])
		for bkg in ddbkgLTTList:
			if bkg!=ddbkgLTTList[0]: hddbkgLTT[isEM].Add(bkghists[histoPrefix+'_'+bkg])

		for bkg in ddbkgTLLList:
			if bkg!=ddbkgTLLList[0]: hddbkgTLL[isEM].Add(bkghists[histoPrefix+'_'+bkg])
		for bkg in ddbkgLTLList:
			if bkg!=ddbkgLTLList[0]: hddbkgLTL[isEM].Add(bkghists[histoPrefix+'_'+bkg])
		for bkg in ddbkgLLTList:
			if bkg!=ddbkgLLTList[0]: hddbkgLLT[isEM].Add(bkghists[histoPrefix+'_'+bkg])

		for bkg in ddbkgLLLList:
			if bkg!=ddbkgLLLList[0]: hddbkgLLL[isEM].Add(bkghists[histoPrefix+'_'+bkg])

		
		#Group QCD processes
# 		hqcd[isEM] = bkghists[histoPrefix+'_'+qcdList[0]].Clone(histoPrefix+'__qcd')
# 		for bkg in qcdList: 
# 			if bkg!=qcdList[0]: hqcd[isEM].Add(bkghists[histoPrefix+'_'+bkg])
		
		#Group EWK processes
		hewk[isEM] = bkghists[histoPrefix+'_'+ewkList[0]].Clone(histoPrefix+'__ewk')
		for bkg in ewkList:
			if bkg!=ewkList[0]: hewk[isEM].Add(bkghists[histoPrefix+'_'+bkg])
		
		#Group TOP processes
		htop[isEM] = bkghists[histoPrefix+'_'+topList[0]].Clone(histoPrefix+'__top')
		for bkg in topList:
			if bkg!=topList[0]: htop[isEM].Add(bkghists[histoPrefix+'_'+bkg])
		
		#get signal
		for signal in sigList.keys(): hsig[isEM+signal] = sighists[histoPrefix+'_'+signal].Clone(histoPrefix+'__'+sigList[signal])
		#get total signal
		for signal in signals: 
			hsig[isEM+signal] = sighists[histoPrefix+'_'+signal+decays[0]].Clone(histoPrefix+'__'+signal)
			for decay in decays: 
				if decay!=decays[0]: hsig[isEM+signal].Add(sighists[histoPrefix+'_'+signal+decay])

		#systematics
		if doAllSys:
			for systematic in systematicList:
				if systematic=='pdfNew' or systematic=='muRFcorrdNew' or systematic=='muRFdecorrdNew': continue
				for ud in ['Up','Down']:
					if systematic!='toppt' and systematic!='PR' and systematic!='FR':
# 						hqcd[isEM+systematic+ud] = bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+qcdList[0]].Clone(histoPrefix+'__qcd__'+systematic+'__'+ud.replace('Up','plus').replace('Down','minus'))
						hewk[isEM+systematic+ud] = bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+ewkList[0]].Clone(histoPrefix+'__ewk__'+systematic+'__'+ud.replace('Up','plus').replace('Down','minus'))
						htop[isEM+systematic+ud] = bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+topList[0]].Clone(histoPrefix+'__top__'+systematic+'__'+ud.replace('Up','plus').replace('Down','minus'))
						for signal in sigList.keys(): hsig[isEM+signal+systematic+ud] = sighists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+signal].Clone(histoPrefix+'__'+sigList[signal]+'__'+systematic+'__'+ud.replace('Up','plus').replace('Down','minus'))
						for signal in signals: 
							hsig[isEM+signal+systematic+ud] = sighists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+signal+decays[0]].Clone(histoPrefix+'__'+signal+'__'+systematic+'__'+ud.replace('Up','plus').replace('Down','minus'))
							for decay in decays: 
								if decay!=decays[0]: hsig[isEM+signal+systematic+ud].Add(sighists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+signal+decay])
# 						for bkg in qcdList: 
# 							if bkg!=qcdList[0]: hqcd[isEM+systematic+ud].Add(bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+bkg])
						for bkg in ewkList: 
							if bkg!=ewkList[0]: hewk[isEM+systematic+ud].Add(bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+bkg])
						for bkg in topList: 
							if bkg!=topList[0]: htop[isEM+systematic+ud].Add(bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+bkg])
					if systematic=='toppt': # top pt is only on the ttbar sample, so it needs special treatment!
						htop[isEM+systematic+ud] = bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+ttjetList[0]].Clone(histoPrefix+'__top__'+systematic+'__'+ud.replace('Up','plus').replace('Down','minus'))
						for bkg in ttjetList: 
							if bkg!=ttjetList[0]: htop[isEM+systematic+ud].Add(bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+bkg])
						for bkg in topList: 
							if bkg not in ttjetList: htop[isEM+systematic+ud].Add(bkghists[histoPrefix+'_'+bkg])
					if systematic=='PR' or systematic=='FR': # PR and FR is only on the ddbkg sample, so it needs special treatment!
						hddbkg[isEM+systematic+ud] = bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+ddbkgList[0]].Clone(histoPrefix+'__ddbkg__'+systematic+'__'+ud.replace('Up','plus').replace('Down','minus'))
						for bkg in ddbkgList: 
							if bkg!=ddbkgList[0]: hddbkg[isEM+systematic+ud].Add(bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+bkg])

# 			htop[isEM+'muRFcorrdNewUp'] = htop[isEM+'muRFcorrdUp'].Clone(histoPrefix+'__top__muRFcorrdNew__plus')
# 			htop[isEM+'muRFcorrdNewDown'] = htop[isEM+'muRFcorrdUp'].Clone(histoPrefix+'__top__muRFcorrdNew__minus')
# 			hewk[isEM+'muRFcorrdNewUp'] = hewk[isEM+'muRFcorrdUp'].Clone(histoPrefix+'__ewk__muRFcorrdNew__plus')
# 			hewk[isEM+'muRFcorrdNewDown'] = hewk[isEM+'muRFcorrdUp'].Clone(histoPrefix+'__ewk__muRFcorrdNew__minus')
# # 			hqcd[isEM+'muRFcorrdNewUp'] = hqcd[isEM+'muRFcorrdUp'].Clone(histoPrefix+'__qcd__muRFcorrdNew__plus')
# # 			hqcd[isEM+'muRFcorrdNewDown'] = hqcd[isEM+'muRFcorrdUp'].Clone(histoPrefix+'__qcd__muRFcorrdNew__minus')
# 			for signal in sigList.keys(): hsig[isEM+signal+'muRFcorrdNewUp'] = hsig[isEM+signal+'muRFcorrdUp'].Clone(histoPrefix+'__'+sigList[signal]+'__muRFcorrdNew__plus')
# 			for signal in sigList.keys(): hsig[isEM+signal+'muRFcorrdNewDown'] = hsig[isEM+signal+'muRFcorrdUp'].Clone(histoPrefix+'__'+sigList[signal]+'__muRFcorrdNew__minus')
# 			for signal in signals: 
# 				hsig[isEM+signal+'muRFcorrdNewUp'] = hsig[isEM+signal+decays[0]+'muRFcorrdUp'].Clone(histoPrefix+'__'+signal+'__muRFcorrdNew__plus')
# 				hsig[isEM+signal+'muRFcorrdNewDown'] = hsig[isEM+signal+decays[0]+'muRFcorrdUp'].Clone(histoPrefix+'__'+signal+'__muRFcorrdNew__minus')
# 
# 			htop[isEM+'muRFdecorrdNewUp'] = htop[isEM+'muRFcorrdUp'].Clone(histoPrefix+'__top__muRFdecorrdNew__plus')
# 			htop[isEM+'muRFdecorrdNewDown'] = htop[isEM+'muRFcorrdUp'].Clone(histoPrefix+'__top__muRFdecorrdNew__minus')
# 			hewk[isEM+'muRFdecorrdNewUp'] = hewk[isEM+'muRFcorrdUp'].Clone(histoPrefix+'__ewk__muRFdecorrdNew__plus')
# 			hewk[isEM+'muRFdecorrdNewDown'] = hewk[isEM+'muRFcorrdUp'].Clone(histoPrefix+'__ewk__muRFdecorrdNew__minus')
# # 			hqcd[isEM+'muRFdecorrdNewUp'] = hqcd[isEM+'muRFcorrdUp'].Clone(histoPrefix+'__qcd__muRFdecorrdNew__plus')
# # 			hqcd[isEM+'muRFdecorrdNewDown'] = hqcd[isEM+'muRFcorrdUp'].Clone(histoPrefix+'__qcd__muRFdecorrdNew__minus')
# 			for signal in sigList.keys(): hsig[isEM+signal+'muRFdecorrdNewUp'] = hsig[isEM+signal+'muRFcorrdUp'].Clone(histoPrefix+'__'+sigList[signal]+'__muRFdecorrdNew__plus')
# 			for signal in sigList.keys(): hsig[isEM+signal+'muRFdecorrdNewDown'] = hsig[isEM+signal+'muRFcorrdUp'].Clone(histoPrefix+'__'+sigList[signal]+'__muRFdecorrdNew__minus')
# 			for signal in signals: 
# 				hsig[isEM+signal+'muRFdecorrdNewUp'] = hsig[isEM+signal+decays[0]+'muRFcorrdUp'].Clone(histoPrefix+'__'+signal+'__muRFdecorrdNew__plus')
# 				hsig[isEM+signal+'muRFdecorrdNewDown'] = hsig[isEM+signal+decays[0]+'muRFcorrdUp'].Clone(histoPrefix+'__'+signal+'__muRFdecorrdNew__minus')
# 
# 			# nominal,renormWeights[4],renormWeights[2],renormWeights[1],renormWeights[0],renormWeights[5],renormWeights[3]
# 			histPrefixList = ['','muRUp','muRDown','muFUp','muFDown','muRFcorrdUp','muRFcorrdDown']
# 			for ibin in range(1,htop[isEM].GetNbinsX()+1):
# 				weightListTop = [htop[isEM+item].GetBinContent(ibin) for item in histPrefixList]	
# 				weightListEwk = [hewk[isEM+item].GetBinContent(ibin) for item in histPrefixList]	
# # 				weightListQcd = [hqcd[isEM+item].GetBinContent(ibin) for item in histPrefixList]	
# 				weightListSig = {}
# 				for signal in sigList.keys()+signals: weightListSig[signal] = [hsig[isEM+signal+item].GetBinContent(ibin) for item in histPrefixList]
# 				indTopRFcorrdUp = weightListTop.index(max(weightListTop))
# 				indTopRFcorrdDn = weightListTop.index(min(weightListTop))
# 				indEwkRFcorrdUp = weightListEwk.index(max(weightListEwk))
# 				indEwkRFcorrdDn = weightListEwk.index(min(weightListEwk))
# 				indQcdRFcorrdUp = weightListQcd.index(max(weightListQcd))
# 				indQcdRFcorrdDn = weightListQcd.index(min(weightListQcd))
# 				indSigRFcorrdUp = {}
# 				indSigRFcorrdDn = {}
# 				for signal in sigList.keys()+signals: 
# 					indSigRFcorrdUp[signal] = weightListSig[signal].index(max(weightListSig[signal]))
# 					indSigRFcorrdDn[signal] = weightListSig[signal].index(min(weightListSig[signal]))
# 
# 				indTopRFdecorrdUp = weightListTop.index(max(weightListTop[:-2]))
# 				indTopRFdecorrdDn = weightListTop.index(min(weightListTop[:-2]))
# 				indEwkRFdecorrdUp = weightListEwk.index(max(weightListEwk[:-2]))
# 				indEwkRFdecorrdDn = weightListEwk.index(min(weightListEwk[:-2]))
# 				indQcdRFdecorrdUp = weightListQcd.index(max(weightListQcd[:-2]))
# 				indQcdRFdecorrdDn = weightListQcd.index(min(weightListQcd[:-2]))
# 				indSigRFdecorrdUp = {}
# 				indSigRFdecorrdDn = {}
# 				for signal in sigList.keys()+signals: 
# 					indSigRFdecorrdUp[signal] = weightListSig[signal].index(max(weightListSig[signal][:-2]))
# 					indSigRFdecorrdDn[signal] = weightListSig[signal].index(min(weightListSig[signal][:-2]))
# 				
# 				htop[isEM+'muRFcorrdNewUp'].SetBinContent(ibin,htop[isEM+histPrefixList[indTopRFcorrdUp]].GetBinContent(ibin))
# 				htop[isEM+'muRFcorrdNewDown'].SetBinContent(ibin,htop[isEM+histPrefixList[indTopRFcorrdDn]].GetBinContent(ibin))
# 				hewk[isEM+'muRFcorrdNewUp'].SetBinContent(ibin,hewk[isEM+histPrefixList[indEwkRFcorrdUp]].GetBinContent(ibin))
# 				hewk[isEM+'muRFcorrdNewDown'].SetBinContent(ibin,hewk[isEM+histPrefixList[indEwkRFcorrdDn]].GetBinContent(ibin))
# # 				hqcd[isEM+'muRFcorrdNewUp'].SetBinContent(ibin,hqcd[isEM+histPrefixList[indQcdRFcorrdUp]].GetBinContent(ibin))
# # 				hqcd[isEM+'muRFcorrdNewDown'].SetBinContent(ibin,hqcd[isEM+histPrefixList[indQcdRFcorrdDn]].GetBinContent(ibin))
# 				for signal in sigList.keys()+signals: 
# 					hsig[isEM+signal+'muRFcorrdNewUp'].SetBinContent(ibin,hsig[isEM+signal+histPrefixList[indSigRFcorrdUp[signal]]].GetBinContent(ibin))
# 					hsig[isEM+signal+'muRFcorrdNewDown'].SetBinContent(ibin,hsig[isEM+signal+histPrefixList[indSigRFcorrdDn[signal]]].GetBinContent(ibin))
# 				htop[isEM+'muRFdecorrdNewUp'].SetBinContent(ibin,htop[isEM+histPrefixList[indTopRFdecorrdUp]].GetBinContent(ibin))
# 				htop[isEM+'muRFdecorrdNewDown'].SetBinContent(ibin,htop[isEM+histPrefixList[indTopRFdecorrdDn]].GetBinContent(ibin))
# 				hewk[isEM+'muRFdecorrdNewUp'].SetBinContent(ibin,hewk[isEM+histPrefixList[indEwkRFdecorrdUp]].GetBinContent(ibin))
# 				hewk[isEM+'muRFdecorrdNewDown'].SetBinContent(ibin,hewk[isEM+histPrefixList[indEwkRFdecorrdDn]].GetBinContent(ibin))
# # 				hqcd[isEM+'muRFdecorrdNewUp'].SetBinContent(ibin,hqcd[isEM+histPrefixList[indQcdRFdecorrdUp]].GetBinContent(ibin))
# # 				hqcd[isEM+'muRFdecorrdNewDown'].SetBinContent(ibin,hqcd[isEM+histPrefixList[indQcdRFdecorrdDn]].GetBinContent(ibin))
# 				for signal in sigList.keys()+signals: 
# 					hsig[isEM+signal+'muRFdecorrdNewUp'].SetBinContent(ibin,hsig[isEM+signal+histPrefixList[indSigRFdecorrdUp[signal]]].GetBinContent(ibin))
# 					hsig[isEM+signal+'muRFdecorrdNewDown'].SetBinContent(ibin,hsig[isEM+signal+histPrefixList[indSigRFdecorrdDn[signal]]].GetBinContent(ibin))
# 
# 				htop[isEM+'muRFcorrdNewUp'].SetBinError(ibin,htop[isEM+histPrefixList[indTopRFcorrdUp]].GetBinError(ibin))
# 				htop[isEM+'muRFcorrdNewDown'].SetBinError(ibin,htop[isEM+histPrefixList[indTopRFcorrdDn]].GetBinError(ibin))
# 				hewk[isEM+'muRFcorrdNewUp'].SetBinError(ibin,hewk[isEM+histPrefixList[indEwkRFcorrdUp]].GetBinError(ibin))
# 				hewk[isEM+'muRFcorrdNewDown'].SetBinError(ibin,hewk[isEM+histPrefixList[indEwkRFcorrdDn]].GetBinError(ibin))
# # 				hqcd[isEM+'muRFcorrdNewUp'].SetBinError(ibin,hqcd[isEM+histPrefixList[indQcdRFcorrdUp]].GetBinError(ibin))
# # 				hqcd[isEM+'muRFcorrdNewDown'].SetBinError(ibin,hqcd[isEM+histPrefixList[indQcdRFcorrdDn]].GetBinError(ibin))
# 				for signal in sigList.keys()+signals: 
# 					hsig[isEM+signal+'muRFcorrdNewUp'].SetBinError(ibin,hsig[isEM+signal+histPrefixList[indSigRFcorrdUp[signal]]].GetBinError(ibin))
# 					hsig[isEM+signal+'muRFcorrdNewDown'].SetBinError(ibin,hsig[isEM+signal+histPrefixList[indSigRFcorrdDn[signal]]].GetBinError(ibin))
# 				htop[isEM+'muRFdecorrdNewUp'].SetBinError(ibin,htop[isEM+histPrefixList[indTopRFdecorrdUp]].GetBinError(ibin))
# 				htop[isEM+'muRFdecorrdNewDown'].SetBinError(ibin,htop[isEM+histPrefixList[indTopRFdecorrdDn]].GetBinError(ibin))
# 				hewk[isEM+'muRFdecorrdNewUp'].SetBinError(ibin,hewk[isEM+histPrefixList[indEwkRFdecorrdUp]].GetBinError(ibin))
# 				hewk[isEM+'muRFdecorrdNewDown'].SetBinError(ibin,hewk[isEM+histPrefixList[indEwkRFdecorrdDn]].GetBinError(ibin))
# # 				hqcd[isEM+'muRFdecorrdNewUp'].SetBinError(ibin,hqcd[isEM+histPrefixList[indQcdRFdecorrdUp]].GetBinError(ibin))
# # 				hqcd[isEM+'muRFdecorrdNewDown'].SetBinError(ibin,hqcd[isEM+histPrefixList[indQcdRFdecorrdDn]].GetBinError(ibin))
# 				for signal in sigList.keys()+signals: 
# 					hsig[isEM+signal+'muRFdecorrdNewUp'].SetBinError(ibin,hsig[isEM+signal+histPrefixList[indSigRFdecorrdUp[signal]]].GetBinError(ibin))
# 					hsig[isEM+signal+'muRFdecorrdNewDown'].SetBinError(ibin,hsig[isEM+signal+histPrefixList[indSigRFdecorrdDn[signal]]].GetBinError(ibin))
# 
# 			for pdfInd in range(100):
# # 				hqcd[isEM+'pdf'+str(pdfInd)] = bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+qcdList[0]].Clone(histoPrefix+'__qcd__pdf'+str(pdfInd))
# 				hewk[isEM+'pdf'+str(pdfInd)] = bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+ewkList[0]].Clone(histoPrefix+'__ewk__pdf'+str(pdfInd))
# 				htop[isEM+'pdf'+str(pdfInd)] = bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+topList[0]].Clone(histoPrefix+'__top__pdf'+str(pdfInd))
# 				for signal in sigList.keys(): hsig[isEM+signal+'pdf'+str(pdfInd)] = sighists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+signal].Clone(histoPrefix+'__'+signal+'__pdf'+str(pdfInd))
# 				for signal in signals: 
# 					hsig[isEM+signal+'pdf'+str(pdfInd)] = sighists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+signal+decays[0]].Clone(histoPrefix+'__'+signal+'__pdf'+str(pdfInd))
# 					for decay in decays: 
# 						if decay!=decays[0]: hsig[isEM+signal+'pdf'+str(pdfInd)].Add(sighists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+signal+decay])
# 				for bkg in qcdList: 
# 					if bkg!=qcdList[0]: hqcd[isEM+'pdf'+str(pdfInd)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+bkg])
# 				for bkg in ewkList: 
# 					if bkg!=ewkList[0]: hewk[isEM+'pdf'+str(pdfInd)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+bkg])
# 				for bkg in topList: 
# 					if bkg!=topList[0]: htop[isEM+'pdf'+str(pdfInd)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+bkg])
# 			htop[isEM+'pdfNewUp'] = htop[isEM+'pdf0'].Clone(histoPrefix+'__top__pdfNew__plus')
# 			htop[isEM+'pdfNewDown'] = htop[isEM+'pdf0'].Clone(histoPrefix+'__top__pdfNew__minus')
# 			hewk[isEM+'pdfNewUp'] = hewk[isEM+'pdf0'].Clone(histoPrefix+'__ewk__pdfNew__plus')
# 			hewk[isEM+'pdfNewDown'] = hewk[isEM+'pdf0'].Clone(histoPrefix+'__ewk__pdfNew__minus')
# 			hqcd[isEM+'pdfNewUp'] = hqcd[isEM+'pdf0'].Clone(histoPrefix+'__qcd__pdfNew__plus')
# 			hqcd[isEM+'pdfNewDown'] = hqcd[isEM+'pdf0'].Clone(histoPrefix+'__qcd__pdfNew__minus')
# 			for signal in sigList.keys(): hsig[isEM+signal+'pdfNewUp'] = hsig[isEM+signal+'pdf0'].Clone(histoPrefix+'__'+sigList[signal]+'__pdfNew__plus')
# 			for signal in sigList.keys(): hsig[isEM+signal+'pdfNewDown'] = hsig[isEM+signal+'pdf0'].Clone(histoPrefix+'__'+sigList[signal]+'__pdfNew__minus')
# 			for signal in signals: 
# 				hsig[isEM+signal+'pdfNewUp'] = hsig[isEM+signal+decays[0]+'pdf0'].Clone(histoPrefix+'__'+signal+'__pdfNew__plus')
# 				hsig[isEM+signal+'pdfNewDown'] = hsig[isEM+signal+decays[0]+'pdf0'].Clone(histoPrefix+'__'+signal+'__pdfNew__minus')
# 			for ibin in range(1,htop[isEM+'pdfNewUp'].GetNbinsX()+1):
# 				weightListTop = [htop[isEM+'pdf'+str(pdfInd)].GetBinContent(ibin) for pdfInd in range(100)]
# 				weightListEwk = [hewk[isEM+'pdf'+str(pdfInd)].GetBinContent(ibin) for pdfInd in range(100)]
# 				weightListQcd = [hqcd[isEM+'pdf'+str(pdfInd)].GetBinContent(ibin) for pdfInd in range(100)]
# 				weightListSig = {}
# 				for signal in sigList.keys()+signals: weightListSig[signal] = [hsig[isEM+signal+'pdf'+str(pdfInd)].GetBinContent(ibin) for pdfInd in range(100)]
# 				indTopPDFUp = sorted(range(len(weightListTop)), key=lambda k: weightListTop[k])[83]
# 				indTopPDFDn = sorted(range(len(weightListTop)), key=lambda k: weightListTop[k])[15]
# 				indEwkPDFUp = sorted(range(len(weightListEwk)), key=lambda k: weightListEwk[k])[83]
# 				indEwkPDFDn = sorted(range(len(weightListEwk)), key=lambda k: weightListEwk[k])[15]
# 				indQcdPDFUp = sorted(range(len(weightListQcd)), key=lambda k: weightListQcd[k])[83]
# 				indQcdPDFDn = sorted(range(len(weightListQcd)), key=lambda k: weightListQcd[k])[15]
# 				indSigPDFUp = {}
# 				indSigPDFDn = {}
# 				for signal in sigList.keys()+signals: 
# 					indSigPDFUp[signal] = sorted(range(len(weightListSig[signal])), key=lambda k: weightListSig[signal][k])[83]
# 					indSigPDFDn[signal] = sorted(range(len(weightListSig[signal])), key=lambda k: weightListSig[signal][k])[15]
# 				
# 				htop[isEM+'pdfNewUp'].SetBinContent(ibin,htop[isEM+'pdf'+str(indTopPDFUp)].GetBinContent(ibin))
# 				htop[isEM+'pdfNewDown'].SetBinContent(ibin,htop[isEM+'pdf'+str(indTopPDFDn)].GetBinContent(ibin))
# 				hewk[isEM+'pdfNewUp'].SetBinContent(ibin,hewk[isEM+'pdf'+str(indEwkPDFUp)].GetBinContent(ibin))
# 				hewk[isEM+'pdfNewDown'].SetBinContent(ibin,hewk[isEM+'pdf'+str(indEwkPDFDn)].GetBinContent(ibin))
# # 				hqcd[isEM+'pdfNewUp'].SetBinContent(ibin,hqcd[isEM+'pdf'+str(indQcdPDFUp)].GetBinContent(ibin))
# # 				hqcd[isEM+'pdfNewDown'].SetBinContent(ibin,hqcd[isEM+'pdf'+str(indQcdPDFDn)].GetBinContent(ibin))
# 				for signal in sigList.keys()+signals: 
# 					hsig[isEM+signal+'pdfNewUp'].SetBinContent(ibin,hsig[isEM+signal+'pdf'+str(indSigPDFUp[signal])].GetBinContent(ibin))
# 					hsig[isEM+signal+'pdfNewDown'].SetBinContent(ibin,hsig[isEM+signal+'pdf'+str(indSigPDFDn[signal])].GetBinContent(ibin))
# 
# 				htop[isEM+'pdfNewUp'].SetBinError(ibin,htop[isEM+'pdf'+str(indTopPDFUp)].GetBinError(ibin))
# 				htop[isEM+'pdfNewDown'].SetBinError(ibin,htop[isEM+'pdf'+str(indTopPDFDn)].GetBinError(ibin))
# 				hewk[isEM+'pdfNewUp'].SetBinError(ibin,hewk[isEM+'pdf'+str(indEwkPDFUp)].GetBinError(ibin))
# 				hewk[isEM+'pdfNewDown'].SetBinError(ibin,hewk[isEM+'pdf'+str(indEwkPDFDn)].GetBinError(ibin))
# # 				hqcd[isEM+'pdfNewUp'].SetBinError(ibin,hqcd[isEM+'pdf'+str(indQcdPDFUp)].GetBinError(ibin))
# # 				hqcd[isEM+'pdfNewDown'].SetBinError(ibin,hqcd[isEM+'pdf'+str(indQcdPDFDn)].GetBinError(ibin))
# 				for signal in sigList.keys()+signals: 
# 					hsig[isEM+signal+'pdfNewUp'].SetBinError(ibin,hsig[isEM+signal+'pdf'+str(indSigPDFUp[signal])].GetBinError(ibin))
# 					hsig[isEM+signal+'pdfNewDown'].SetBinError(ibin,hsig[isEM+signal+'pdf'+str(indSigPDFDn[signal])].GetBinError(ibin))
		
		#Group data processes
		hdata[isEM] = datahists[histoPrefix+'_'+dataList[0]].Clone(histoPrefix+'__DATA')
		for dat in dataList:
			if dat!=dataList[0]: hdata[isEM].Add(datahists[histoPrefix+'_'+dat])

		#prepare yield table

		yieldTable[histoPrefix]['top']    = htop[isEM].Integral()
		yieldTable[histoPrefix]['ewk']    = hewk[isEM].Integral()
# 		yieldTable[histoPrefix]['qcd']    = hqcd[isEM].Integral()
# 		yieldTable[histoPrefix]['totBkg'] = htop[isEM].Integral()+hewk[isEM].Integral()+hqcd[isEM].Integral()+hddbkg[isEM].Integral()
		yieldTable[histoPrefix]['totBkg'] = htop[isEM].Integral()+hewk[isEM].Integral()+hddbkg[isEM].Integral()
		yieldTable[histoPrefix]['data']   = hdata[isEM].Integral()
		if yieldTable[histoPrefix]['totBkg']!=0:
			yieldTable[histoPrefix]['dataOverBkg']= yieldTable[histoPrefix]['data']/yieldTable[histoPrefix]['totBkg']
		else:
			yieldTable[histoPrefix]['dataOverBkg']= 0.
# 		yieldTable[histoPrefix]['WJets']  = hwjets[isEM].Integral()
# 		yieldTable[histoPrefix]['ZJets']  = hzjets[isEM].Integral()
		yieldTable[histoPrefix]['VV']     = hvv[isEM].Integral()
		yieldTable[histoPrefix]['WZ']     = hwz[isEM].Integral()
		yieldTable[histoPrefix]['ZZ']     = hzz[isEM].Integral()
		yieldTable[histoPrefix]['VVV']    = hvvv[isEM].Integral()
		yieldTable[histoPrefix]['TTV']    = httv[isEM].Integral()
# 		yieldTable[histoPrefix]['TTJets'] = httjets[isEM].Integral()
# 		yieldTable[histoPrefix]['T']      = ht[isEM].Integral()
# 		yieldTable[histoPrefix]['QCD']    = hqcd[isEM].Integral()
		yieldTable[histoPrefix]['ddbkg']  = hddbkg[isEM].Integral()

		print ''
		print '----------', isEM,'----------'

		yieldTable[histoPrefix]['ddbkgTTT']  = hddbkgTTT[isEM].Integral()
		print 'hddbkgTTT[isEM].Integral() = ', hddbkgTTT[isEM].Integral()
		print ''

		yieldTable[histoPrefix]['ddbkgTTL']  = hddbkgTTL[isEM].Integral()
		print 'hddbkgTTL[isEM].Integral() = ', hddbkgTTL[isEM].Integral()
		yieldTable[histoPrefix]['ddbkgTLT']  = hddbkgTLT[isEM].Integral()
		print 'hddbkgTLT[isEM].Integral() = ', hddbkgTLT[isEM].Integral()
		yieldTable[histoPrefix]['ddbkgLTT']  = hddbkgLTT[isEM].Integral()
		print 'hddbkgLTT[isEM].Integral() = ', hddbkgLTT[isEM].Integral()
		print ''

		yieldTable[histoPrefix]['ddbkgTLL']  = hddbkgTLL[isEM].Integral()
		print 'hddbkgTLL[isEM].Integral() = ', hddbkgTLL[isEM].Integral()
		yieldTable[histoPrefix]['ddbkgLTL']  = hddbkgLTL[isEM].Integral()
		print 'hddbkgLTL[isEM].Integral() = ', hddbkgLTL[isEM].Integral()
		yieldTable[histoPrefix]['ddbkgLLT']  = hddbkgLLT[isEM].Integral()
		print 'hddbkgLLT[isEM].Integral() = ', hddbkgLLT[isEM].Integral()
		print ''

		yieldTable[histoPrefix]['ddbkgLLL']  = hddbkgLLL[isEM].Integral()
		print 'hddbkgLLL[isEM].Integral() = ', hddbkgLLL[isEM].Integral()

		for signal in sigList.keys(): yieldTable[histoPrefix][signal] = hsig[isEM+signal].Integral()
		for signal in signals: yieldTable[histoPrefix][signal] = hsig[isEM+signal].Integral()
		
		#+/- 1sigma variations of shape systematics
		if doAllSys:
			for systematic in systematicList:
				for ud in ['Up','Down']:
					if systematic!='PR' and systematic!='FR':
						yieldTable[histoPrefix+systematic+ud]['top'] = htop[isEM+systematic+ud].Integral()
						if systematic!='toppt':
							yieldTable[histoPrefix+systematic+ud]['ewk'] = hewk[isEM+systematic+ud].Integral()
							yieldTable[histoPrefix+systematic+ud]['qcd'] = hqcd[isEM+systematic+ud].Integral()
							for signal in sigList.keys(): yieldTable[histoPrefix+systematic+ud][signal] = hsig[isEM+signal+systematic+ud].Integral()
							for signal in signals: yieldTable[histoPrefix+systematic+ud][signal] = hsig[isEM+signal+systematic+ud].Integral()
					if systematic=='PR' or systematic=='FR':
						yieldTable[histoPrefix+systematic+ud]['ddbkg'] = hddbkg[isEM+systematic+ud].Integral()

		#prepare MC yield error table
		yieldErrTable[histoPrefix]['top']    = 0.
		yieldErrTable[histoPrefix]['ewk']    = 0.
# 		yieldErrTable[histoPrefix]['qcd']    = 0.
		yieldErrTable[histoPrefix]['totBkg'] = 0.
		yieldErrTable[histoPrefix]['data']   = 0.
		yieldErrTable[histoPrefix]['dataOverBkg']= 0.
# 		yieldErrTable[histoPrefix]['WJets']  = 0.
# 		yieldErrTable[histoPrefix]['ZJets']  = 0.
		yieldErrTable[histoPrefix]['VV']     = 0.
		yieldErrTable[histoPrefix]['WZ']     = 0.
		yieldErrTable[histoPrefix]['ZZ']     = 0.
		yieldErrTable[histoPrefix]['VVV']    = 0.
		yieldErrTable[histoPrefix]['TTV']    = 0.
# 		yieldErrTable[histoPrefix]['TTJets'] = 0.
# 		yieldErrTable[histoPrefix]['T']      = 0.
# 		yieldErrTable[histoPrefix]['QCD']    = 0.
		yieldErrTable[histoPrefix]['ddbkg']  = 0.
		yieldErrTable[histoPrefix]['ddbkgTTT']  = 0.

		yieldErrTable[histoPrefix]['ddbkgTTL']  = 0.
		yieldErrTable[histoPrefix]['ddbkgTLT']  = 0.
		yieldErrTable[histoPrefix]['ddbkgLTT']  = 0.

		yieldErrTable[histoPrefix]['ddbkgTLL']  = 0.
		yieldErrTable[histoPrefix]['ddbkgLTL']  = 0.
		yieldErrTable[histoPrefix]['ddbkgLLT']  = 0.

		yieldErrTable[histoPrefix]['ddbkgLLL']  = 0.
		for signal in sigList.keys(): yieldErrTable[histoPrefix][signal] = 0.
		for signal in signals: yieldErrTable[histoPrefix][signal] = 0.

		for ibin in range(1,hsig[isEM+signal].GetXaxis().GetNbins()+1):
			yieldErrTable[histoPrefix]['top']    += htop[isEM].GetBinError(ibin)**2
			yieldErrTable[histoPrefix]['ewk']    += hewk[isEM].GetBinError(ibin)**2
# 			yieldErrTable[histoPrefix]['qcd']    += hqcd[isEM].GetBinError(ibin)**2
# 			yieldErrTable[histoPrefix]['totBkg'] += htop[isEM].GetBinError(ibin)**2+hewk[isEM].GetBinError(ibin)**2+hqcd[isEM].GetBinError(ibin)**2+hddbkg[isEM].GetBinError(ibin)**2
			yieldErrTable[histoPrefix]['totBkg'] += htop[isEM].GetBinError(ibin)**2+hewk[isEM].GetBinError(ibin)**2+hddbkg[isEM].GetBinError(ibin)**2
			yieldErrTable[histoPrefix]['data']   += hdata[isEM].GetBinError(ibin)**2
# 			print "hdata[isEM].GetBinError(ibin) = ", hdata[isEM].GetBinError(ibin)
# 			print "hdata[isEM].GetBinError(ibin)*hdata[isEM].GetBinError(ibin) = ", hdata[isEM].GetBinError(ibin)*hdata[isEM].GetBinError(ibin)
# 			print "yieldErrTable[histoPrefix]['data'] = ", yieldErrTable[histoPrefix]['data']
# 			yieldErrTable[histoPrefix]['WJets']  += hwjets[isEM].GetBinError(ibin)**2
# 			yieldErrTable[histoPrefix]['ZJets']  += hzjets[isEM].GetBinError(ibin)**2
			yieldErrTable[histoPrefix]['VV']     += hvv[isEM].GetBinError(ibin)**2
			yieldErrTable[histoPrefix]['WZ']     += hwz[isEM].GetBinError(ibin)**2
			yieldErrTable[histoPrefix]['ZZ']     += hzz[isEM].GetBinError(ibin)**2
			yieldErrTable[histoPrefix]['VVV']    += hvvv[isEM].GetBinError(ibin)**2
			yieldErrTable[histoPrefix]['TTV']    += httv[isEM].GetBinError(ibin)**2
# 			yieldErrTable[histoPrefix]['TTJets'] += httjets[isEM].GetBinError(ibin)**2
# 			yieldErrTable[histoPrefix]['T']      += ht[isEM].GetBinError(ibin)**2
# 			yieldErrTable[histoPrefix]['QCD']    += hqcd[isEM].GetBinError(ibin)**2
			yieldErrTable[histoPrefix]['ddbkg']  += hddbkg[isEM].GetBinError(ibin)**2
			yieldErrTable[histoPrefix]['ddbkgTTT']  += hddbkgTTT[isEM].GetBinError(ibin)**2

			yieldErrTable[histoPrefix]['ddbkgTTL']  += hddbkgTTL[isEM].GetBinError(ibin)**2
			yieldErrTable[histoPrefix]['ddbkgTLT']  += hddbkgTLT[isEM].GetBinError(ibin)**2
			yieldErrTable[histoPrefix]['ddbkgLTT']  += hddbkgLTT[isEM].GetBinError(ibin)**2

			yieldErrTable[histoPrefix]['ddbkgTLL']  += hddbkgTLL[isEM].GetBinError(ibin)**2
			yieldErrTable[histoPrefix]['ddbkgLTL']  += hddbkgLTL[isEM].GetBinError(ibin)**2
			yieldErrTable[histoPrefix]['ddbkgLLT']  += hddbkgLLT[isEM].GetBinError(ibin)**2

			yieldErrTable[histoPrefix]['ddbkgLLL']  += hddbkgLLL[isEM].GetBinError(ibin)**2
			for signal in sigList.keys(): yieldErrTable[histoPrefix][signal] += hsig[isEM+signal].GetBinError(ibin)**2
			for signal in signals: yieldErrTable[histoPrefix][signal] += hsig[isEM+signal].GetBinError(ibin)**2
			
		yieldErrTable[histoPrefix]['top']    += (corrdSys*yieldTable[histoPrefix]['top'])**2+(topXsecSys*yieldTable[histoPrefix]['top'])**2
		yieldErrTable[histoPrefix]['ewk']    += (corrdSys*yieldTable[histoPrefix]['ewk'])**2+(ewkXsecSys*yieldTable[histoPrefix]['ewk'])**2
# 		yieldErrTable[histoPrefix]['qcd']    += (corrdSys*yieldTable[histoPrefix]['qcd'])**2+(qcdXsecSys*yieldTable[histoPrefix]['qcd'])**2
# 		yieldErrTable[histoPrefix]['totBkg'] += (corrdSys*yieldTable[histoPrefix]['totBkg'])**2+(topXsecSys*yieldTable[histoPrefix]['top'])**2+(ewkXsecSys*yieldTable[histoPrefix]['ewk'])**2+(qcdXsecSys*yieldTable[histoPrefix]['qcd'])**2
		yieldErrTable[histoPrefix]['totBkg'] += (corrdSys*yieldTable[histoPrefix]['totBkg'])**2+(topXsecSys*yieldTable[histoPrefix]['top'])**2+(ewkXsecSys*yieldTable[histoPrefix]['ewk'])**2
# 		yieldErrTable[histoPrefix]['WJets']  += (corrdSys*yieldTable[histoPrefix]['WJets'])**2+(ewkXsecSys*yieldTable[histoPrefix]['WJets'])**2
# 		yieldErrTable[histoPrefix]['ZJets']  += (corrdSys*yieldTable[histoPrefix]['ZJets'])**2+(ewkXsecSys*yieldTable[histoPrefix]['ZJets'])**2
		yieldErrTable[histoPrefix]['VV']     += (corrdSys*yieldTable[histoPrefix]['VV'])**2+(ewkXsecSys*yieldTable[histoPrefix]['VV'])**2 #ATTENTION! CHECK IF CORRECT CALCULATION!
		yieldErrTable[histoPrefix]['WZ']     += (corrdSys*yieldTable[histoPrefix]['WZ'])**2+(ewkXsecSys*yieldTable[histoPrefix]['WZ'])**2 #ATTENTION! CHECK IF CORRECT CALCULATION!
		yieldErrTable[histoPrefix]['ZZ']     += (corrdSys*yieldTable[histoPrefix]['ZZ'])**2+(ewkXsecSys*yieldTable[histoPrefix]['ZZ'])**2 #ATTENTION! CHECK IF CORRECT CALCULATION!
		yieldErrTable[histoPrefix]['VVV']    += (corrdSys*yieldTable[histoPrefix]['VVV'])**2+(ewkXsecSys*yieldTable[histoPrefix]['VVV'])**2	#ATTENTION! CHECK IF CORRECT CALCULATION!
		yieldErrTable[histoPrefix]['TTV']    += (corrdSys*yieldTable[histoPrefix]['TTV'])**2+(topXsecSys*yieldTable[histoPrefix]['TTV'])**2 #ATTENTION! CHECK IF CORRECT CALCULATION!
# 		yieldErrTable[histoPrefix]['TTJets'] += (corrdSys*yieldTable[histoPrefix]['TTJets'])**2+(topXsecSys*yieldTable[histoPrefix]['TTJets'])**2
# 		yieldErrTable[histoPrefix]['T']      += (corrdSys*yieldTable[histoPrefix]['T'])**2+(topXsecSys*yieldTable[histoPrefix]['T'])**2
# 		yieldErrTable[histoPrefix]['QCD']    += (corrdSys*yieldTable[histoPrefix]['QCD'])**2+(qcdXsecSys*yieldTable[histoPrefix]['qcd'])**2
		for signal in sigList.keys(): yieldErrTable[histoPrefix][signal] += (corrdSys*yieldTable[histoPrefix][signal])**2
		for signal in signals: yieldErrTable[histoPrefix][signal] += (corrdSys*yieldTable[histoPrefix][signal])**2

		if yieldTable[histoPrefix]['totBkg']!=0: 
			Ratio = yieldTable[histoPrefix]['data']/yieldTable[histoPrefix]['totBkg']
		else:
			Ratio = 0.0			
# 		yieldErrTable[histoPrefix]['dataOverBkg'] = (Ratio**2) * ((yieldErrTable[histoPrefix]['data']/(yieldTable[histoPrefix]['data']+1e-20))**2 + (yieldErrTable[histoPrefix]['totBkg']/(yieldTable[histoPrefix]['totBkg']+1e-20))**2)
		yieldErrTable[histoPrefix]['dataOverBkg'] = (Ratio**2) * (        (math.sqrt(yieldErrTable[histoPrefix]['data'])      /(yieldTable[histoPrefix]['data']+1e-20))**2 + (math.sqrt(yieldErrTable[histoPrefix]['totBkg'])/(yieldTable[histoPrefix]['totBkg']+1e-20))**2)
# 		print 'Ratio**2 = ', (Ratio**2)
# 		print '(yieldErrTable[histoPrefix]["data"]) = ', (yieldErrTable[histoPrefix]['data'])
# 		print '(yieldTable[histoPrefix]["data"]+1e-20) = ', (yieldTable[histoPrefix]['data']+1e-20)
# 		print '(yieldErrTable[histoPrefix]["data"]/(yieldTable[histoPrefix]["data"]+1e-20))**2 = ', (yieldErrTable[histoPrefix]['data']/(yieldTable[histoPrefix]['data']+1e-20))**2
# 		print '(yieldErrTable[histoPrefix]["totBkg"]/(yieldTable[histoPrefix]["totBkg"]+1e-20))**2 = ', (yieldErrTable[histoPrefix]['totBkg']/(yieldTable[histoPrefix]['totBkg']+1e-20))**2

		hdata[isEM].Write()
		#write theta histograms in root file, avoid having processes with no event yield (to make theta happy) 
		for signal in sigList.keys()+signals: 
			#if hsig[isEM+signal].Integral() > 0:  
				hsig[isEM+signal].Write()
				if doAllSys:
					for systematic in systematicList:
						if systematic=='toppt' or systematic=='PR' or systematic=='FR': continue
						hsig[isEM+signal+systematic+'Up'].Write()
						hsig[isEM+signal+systematic+'Down'].Write()
		if htop[isEM].Integral() > 0:  
			htop[isEM].Write()
			if doAllSys:
				for systematic in systematicList:
					if systematic=='PR' or systematic=='FR': continue
					htop[isEM+systematic+'Up'].Write()
					htop[isEM+systematic+'Down'].Write()
		if hewk[isEM].Integral() > 0:  
			hewk[isEM].Write()
			if doAllSys:
				for systematic in systematicList:
					if systematic=='toppt' or systematic=='PR' or systematic=='FR': continue
					hewk[isEM+systematic+'Up'].Write()
					hewk[isEM+systematic+'Down'].Write()
# 		if hqcd[isEM].Integral() > 0:  
# 			hqcd[isEM].Write()
# 			if doAllSys:
# 				for systematic in systematicList:
# 					if systematic=='toppt' or systematic=='PR' or systematic=='FR': continue
# 					hqcd[isEM+systematic+'Up'].Write()
# 					hqcd[isEM+systematic+'Down'].Write()
# 		if hwjets[isEM].Integral() > 0: hwjets[isEM].Write()
# 		if hzjets[isEM].Integral() > 0: hzjets[isEM].Write()
# 		if httjets[isEM].Integral()> 0: httjets[isEM].Write()
# 		if ht[isEM].Integral() > 0    : ht[isEM].Write()
		if httv[isEM].Integral() > 0  : httv[isEM].Write()
		if hvv[isEM].Integral() > 0   : hvv[isEM].Write()
		if hwz[isEM].Integral() > 0   : hwz[isEM].Write()
		if hzz[isEM].Integral() > 0   : hzz[isEM].Write()
		if hvvv[isEM].Integral() > 0  : hvvv[isEM].Write()
		if hddbkg[isEM].Integral() > 0: 
			hddbkg[isEM].Write()
			if doAllSys:
				for systematic in systematicList:
					if systematic!='PR' and systematic!='FR': continue
					hddbkg[isEM+systematic+'Up'].Write()
					hddbkg[isEM+systematic+'Down'].Write()
		hddbkgTTT[isEM].Write()

		hddbkgTTL[isEM].Write()
		hddbkgTLT[isEM].Write()
		hddbkgLTT[isEM].Write()

		hddbkgTLL[isEM].Write()
		hddbkgLTL[isEM].Write()
		hddbkgLLT[isEM].Write()

		hddbkgLLL[isEM].Write()

	outputRfile.Close()

	stdout_old = sys.stdout
	logFile = open(outDir+'/yields_'+discriminant+'_'+lumiStr.replace('.','p')+'fb.txt','a')
	sys.stdout = logFile

	## PRINTING YIELD TABLE WITH UNCERTAINTIES ##
	#first print table without background grouping
	ljust_i = 1
	print 'CUTS:',cutString
	print
	print 'YIELDS'.ljust(20*ljust_i), 
	for bkg in bkgStackList: print bkg.ljust(ljust_i),
	print 'data'.ljust(ljust_i),
	print
	for isEM in isEMlist:
		histoPrefix=discriminant+'_'+lumiStr+'fb_'+isEM
		print (isEM).ljust(ljust_i),
		for bkg in bkgStackList:
			print str(yieldTable[histoPrefix][bkg])+'\t',
		print str(yieldTable[histoPrefix]['data']),
		print

	print 'YIELDS STATISTICAL + NORM. SYS. ERRORS'
	for isEM in isEMlist:
		histoPrefix=discriminant+'_'+lumiStr+'fb_'+isEM
		print (isEM).ljust(ljust_i),
		for bkg in bkgStackList:
			print str(math.sqrt(yieldErrTable[histoPrefix][bkg])).ljust(ljust_i),
		print str(math.sqrt(yieldErrTable[histoPrefix]['data'])).ljust(ljust_i),
		print

	#now print with top,ewk,qcd grouping
	print
	print 'YIELDS'.ljust(20*ljust_i), 
	print 'ewk'.ljust(ljust_i),
	print 'top'.ljust(ljust_i),
# 	print 'qcd'.ljust(ljust_i),
	print 'ddbkg'.ljust(ljust_i),
	print 'ddbkgTTT'.ljust(ljust_i),

	print 'ddbkgTTL'.ljust(ljust_i),
	print 'ddbkgTLT'.ljust(ljust_i),
	print 'ddbkgLTT'.ljust(ljust_i),

	print 'ddbkgTLL'.ljust(ljust_i),
	print 'ddbkgLTL'.ljust(ljust_i),
	print 'ddbkgLLT'.ljust(ljust_i),

	print 'ddbkgLLL'.ljust(ljust_i),
	print 'data'.ljust(ljust_i),
	print
	for isEM in isEMlist:
		histoPrefix=discriminant+'_'+lumiStr+'fb_'+isEM
		print (isEM).ljust(ljust_i),
		print str(yieldTable[histoPrefix]['ewk']).ljust(ljust_i),
		print str(yieldTable[histoPrefix]['top']).ljust(ljust_i),
# 		print str(yieldTable[histoPrefix]['qcd']).ljust(ljust_i),
		print str(yieldTable[histoPrefix]['ddbkg']).ljust(ljust_i),
		print str(yieldTable[histoPrefix]['ddbkgTTT']).ljust(ljust_i),

		print str(yieldTable[histoPrefix]['ddbkgTTL']).ljust(ljust_i),
		print str(yieldTable[histoPrefix]['ddbkgTLT']).ljust(ljust_i),
		print str(yieldTable[histoPrefix]['ddbkgLTT']).ljust(ljust_i),

		print str(yieldTable[histoPrefix]['ddbkgTLL']).ljust(ljust_i),
		print str(yieldTable[histoPrefix]['ddbkgLTL']).ljust(ljust_i),
		print str(yieldTable[histoPrefix]['ddbkgLLT']).ljust(ljust_i),

		print str(yieldTable[histoPrefix]['ddbkgLLL']).ljust(ljust_i),
		print str(yieldTable[histoPrefix]['data']).ljust(ljust_i),
		print

	print 'YIELDS STATISTICAL + NORM. SYS. ERRORS'
	for isEM in isEMlist:
		histoPrefix=discriminant+'_'+lumiStr+'fb_'+isEM
		print (isEM).ljust(ljust_i),
		print str(math.sqrt(yieldErrTable[histoPrefix]['ewk'])).ljust(ljust_i),
		print str(math.sqrt(yieldErrTable[histoPrefix]['top'])).ljust(ljust_i),
# 		print str(math.sqrt(yieldErrTable[histoPrefix]['qcd'])).ljust(ljust_i),
		print str(math.sqrt(yieldErrTable[histoPrefix]['ddbkg'])).ljust(ljust_i),
		print str(math.sqrt(yieldErrTable[histoPrefix]['ddbkgTTT'])).ljust(ljust_i),

		print str(math.sqrt(yieldErrTable[histoPrefix]['ddbkgTTL'])).ljust(ljust_i),
		print str(math.sqrt(yieldErrTable[histoPrefix]['ddbkgTLT'])).ljust(ljust_i),
		print str(math.sqrt(yieldErrTable[histoPrefix]['ddbkgLTT'])).ljust(ljust_i),

		print str(math.sqrt(yieldErrTable[histoPrefix]['ddbkgTLL'])).ljust(ljust_i),
		print str(math.sqrt(yieldErrTable[histoPrefix]['ddbkgLTL'])).ljust(ljust_i),
		print str(math.sqrt(yieldErrTable[histoPrefix]['ddbkgLLT'])).ljust(ljust_i),

		print str(math.sqrt(yieldErrTable[histoPrefix]['ddbkgLLL'])).ljust(ljust_i),
		print str(math.sqrt(yieldErrTable[histoPrefix]['data'])).ljust(ljust_i),
		print

	#print yields for signals
	print
	print 'YIELDS'.ljust(20*ljust_i), 
	for sig in signalList: print sig.ljust(ljust_i),
	print
	for isEM in isEMlist:
		histoPrefix=discriminant+'_'+lumiStr+'fb_'+isEM
		print (isEM).ljust(ljust_i),
		for sig in signalList:
			print str(yieldTable[histoPrefix][sig]).ljust(ljust_i),
		print

	print 'YIELDS STATISTICAL + NORM. SYS. ERRORS'
	for isEM in isEMlist:
		histoPrefix=discriminant+'_'+lumiStr+'fb_'+isEM
		print (isEM).ljust(ljust_i),
		for sig in signalList:
			print str(math.sqrt(yieldErrTable[histoPrefix][sig])).ljust(ljust_i),
		print

	#print yields for total signals
	print
	print 'YIELDS'.ljust(20*ljust_i), 
	for sig in signals: print sig.ljust(ljust_i),
	print
	for isEM in isEMlist:
		histoPrefix=discriminant+'_'+lumiStr+'fb_'+isEM
		print (isEM).ljust(ljust_i),
		for sig in signals:
			print str(yieldTable[histoPrefix][sig]).ljust(ljust_i),
		print

	print 'YIELDS STATISTICAL + NORM. SYS. ERRORS'
	for isEM in isEMlist:
		histoPrefix=discriminant+'_'+lumiStr+'fb_'+isEM
		print (isEM).ljust(ljust_i),
		for sig in signals:
			print str(math.sqrt(yieldErrTable[histoPrefix][sig])).ljust(ljust_i),
		print
				
	#print for AN tables
	print
	print 'YIELDS'.ljust(20*ljust_i), 
	for isEM in isEMlist:
		histoPrefix=discriminant+'_'+lumiStr+'fb_'+isEM
		print histoPrefix.ljust(ljust_i),
	print
# 	for process in bkgStackList+['ewk','top','qcd','ddbkg','totBkg','data','dataOverBkg']+signals+signalList:
# 	for process in bkgStackList+['ewk','top','qcd','ddbkg','ddbkgTTT','ddbkgTTL','ddbkgTLL','ddbkgLLL','totBkg','data','dataOverBkg']+signals+signalList:
# 	for process in bkgStackList+['ewk','top','ddbkg','ddbkgTTT','ddbkgTTL','ddbkgTLL','ddbkgLLL','totBkg','data','dataOverBkg']+signals+signalList:
	for process in bkgStackList+['ewk','top','ddbkg','ddbkgTTT','ddbkgTTL','ddbkgTLT','ddbkgLTT','ddbkgTLL','ddbkgLTL','ddbkgLLT','ddbkgLLL','totBkg','data','dataOverBkg']+signals+signalList:
		print process.ljust(ljust_i),
		for isEM in isEMlist:
			histoPrefix=discriminant+'_'+lumiStr+'fb_'+isEM
			print ' & '+str(round_sig(yieldTable[histoPrefix][process],4))+' $\pm$ '+str(round_sig(math.sqrt(yieldErrTable[histoPrefix][process]),2)),
		print '\\\\',
		print
				
	sys.stdout = stdout_old
	logFile.close()

###########################################################
###################### LOAD HISTS #########################
###########################################################

def findfiles(path, filtre):
    for root, dirs, files in os.walk(path):
        for f in fnmatch.filter(files, filtre):
            yield os.path.join(root, f)

distList = []
print outDir
for file in findfiles(outDir+'/'+isEMlist[0]+'/', '*.p'):
    if 'bkghists' not in file: continue
    distList.append(file.split('_')[-1][:-2])
print distList
for dist in distList:
	print "DISTRIBUTION: ",dist
	datahists = {}
	bkghists  = {}
	sighists  = {}
	#if dist!='minMlb' and dist!='HT':continue
	for isEM in isEMlist:
		print "LOADING: ",isEM
		datahists.update(pickle.load(open(outDir+'/'+isEM+'/datahists_'+dist+'.p','rb')))
		bkghists.update(pickle.load(open(outDir+'/'+isEM+'/bkghists_'+dist+'.p','rb')))
		sighists.update(pickle.load(open(outDir+'/'+isEM+'/sighists_'+dist+'.p','rb')))
	makeCats(datahists,sighists,bkghists,dist)

print 'AFTER YOU CHECK THE OUTPUT FILES, DELETE THE PICKLE FILES !!!!!!!'
print("--- %s minutes ---" % (round((time.time() - start_time)/60,2)))
