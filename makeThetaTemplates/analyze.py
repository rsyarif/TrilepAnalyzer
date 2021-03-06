#!/usr/bin/python

import ROOT as R
from array import array
from weights import *

"""
--This function will make theta templates for a given distribution and a category
--Check the cuts below to make sure those are the desired full set of cuts!
--The applied weights are defined in "weights.py". Also, the additional weights (SFs, 
negative MC weights, ets) applied below should be checked!
"""

lumiStr = str(targetlumi/1000).replace('.','p') # 1/fb

def analyze(tTree,process,cutList,doAllSys,discriminantName,discriminantDetails,category):
	print "*****"*20
	print "*****"*20
	print "DISTRIBUTION:", discriminantName
	print "            -name in ljmet trees:", discriminantDetails[0]
	print "            -x-axis label is set to:", discriminantDetails[2]
	print "            -using the binning as:", discriminantDetails[1]
	discriminantLJMETName=discriminantDetails[0]
	xbins=array('d', discriminantDetails[1])
	xAxisLabel=discriminantDetails[2]
	
	print "/////"*5
	print "PROCESSING: ", process, " CATEGORY: ", category
	print "/////"*5
	cut = '1'
	cut += ' && (AllLeptonPt_PtOrdered[0] >= '+str(cutList['lep1PtCut'])+')'
	cut += ' && (corr_met_singleLepCalc >= '+str(cutList['metCut'])+')'
# 	cut += ' && (theJetPt_JetSubCalc_PtOrdered[0] > '+str(cutList['leadJetPtCut'])+')'
# 	cut += ' && (theJetPt_JetSubCalc_PtOrdered[1] > '+str(cutList['subLeadJetPtCut'])+')'
# 	cut += ' && (theJetPt_JetSubCalc_PtOrdered[2] > '+str(cutList['thirdJetPtCut'])+')'
# 	cut += ' && (NJetsHtagged == 0)'
#	cut += ' && ('+wtagvar+' == 0)'
#  	cut += ' && minDR_lep3Jet > 0.05'
#  	cut += ' && (deltaR_lepClosestJet[0] > 0.4 || PtRelLepClosestJet[0] > 40)'
#  	cut += ' && (deltaR_lepClosestJet[1] > 0.4 || PtRelLepClosestJet[1] > 40)'
#  	cut += ' && (deltaR_lepClosestJet[2] > 0.4 || PtRelLepClosestJet[2] > 40)'
	cut += ' && (NJets_JetSubCalc >= '+str(cutList['njetsCut'])+')'
# 	cut += ' && (NJets_JetSubCalc == 1 || NJets_JetSubCalc == '+str(cutList['njetsCut'])+')'
#	cut += ' && (('+wtagvar+' > 0 && NJets_JetSubCalc >= '+str(cutList['njetsCut'])+') || ('+wtagvar+' == 0 && NJets_JetSubCalc >= '+str(cutList['njetsCut']+1)+'))'
	cut += ' && (NJetsCSVwithSF_JetSubCalc >= '+str(cutList['nbjetsCut'])+')'
# 	cut += ' && (NJetsCSVwithSF_JetSubCalc_noLepCorr >= '+str(cutList['nbjetsCut'])+')'
#	cut += ' && DataPastTrigger == 1 && MCPastTrigger == 1'
# 	if 'Data' in process: cut += ' && DataPastTrigger == 1'
# 	else: cut += ' && MCPastTrigger == 1'
	if ('Data' in process and 'Bkg' not in process): 
		if cutList['isPassTrig']==1:        cut += ' && DataPastTrigger == 1'
		if cutList['isPassTrig_dilep']==1:  cut += ' && DataPastTrigger_dilep == 1'
		if cutList['isPassTrig_dilep_anth']==1:cut += ' && DataPastTrigger_dilep_anth == 1'
		if cutList['isPassTrig_trilep']==1: cut += ' && DataPastTrigger_trilep == 1'
		if cutList['isPassTrilepton']==1 :  cut += ' && isPassTrilepton == 1'
	elif ('DataDrivenBkg' in process): 
		if cutList['isPassTrig']==1:        cut += ' && DataPastTrigger == 1'
		if cutList['isPassTrig_dilep']==1:  cut += ' && DataPastTrigger_dilep == 1'
		if cutList['isPassTrig_dilep_anth']==1:cut += ' && DataPastTrigger_dilep_anth == 1'
		if cutList['isPassTrig_trilep']==1: cut += ' && DataPastTrigger_trilep == 1'
	elif ('Data' not in process): 
		if cutList['isPassTrig']==1:        cut += ' && MCPastTrigger == 1'
		if cutList['isPassTrig_dilep']==1:  cut += ' && MCPastTrigger_dilep == 1'
		if cutList['isPassTrig_dilep_anth']==1:cut += ' && MCPastTrigger_dilep_anth == 1'
		if cutList['isPassTrig_trilep']==1: cut += ' && MCPastTrigger_trilep == 1'
		if cutList['isPassTrilepton']==1 :  cut += ' && isPassTrilepton == 1'	
# 	cut += ' && (deltaR_lepJets[1] >= '+str(cutList['drCut'])+')'
 	cut += ' && (AK4HTpMETpLepPt >= '+str(cutList['stCut'])+')'

#  	cut += ' && AllLeptonCount_PtOrdered == 3' #require exactly 3 leptons

# 	cut += ' && Mll_sameFlavorOS > '+str(cutList['mllOSCut']) #to make sure the OS pair are same sign cut above 0. 

	cut += ' && MllOS_allComb_min > '+str(cutList['mllOSCut']) #to make sure the OS pair are same sign cut above 0. 

# 	cut += ' && ( (MllOS_allComb[0] > 80 && MllOS_allComb[0] < 100)' #on Z cut
# 	cut += ' || (MllOS_allComb[1] > 80 && MllOS_allComb[1] < 100)' #on Z cut
# 	cut += ' || (MllOS_allComb[2] > 80 && MllOS_allComb[2] < 100) )' #on Z cut

# 	cut += ' && !( (MllOS_allComb[0] > 80 && MllOS_allComb[0] < 100)' #off Z cut
# 	cut += ' || (MllOS_allComb[1] > 80 && MllOS_allComb[1] < 100)' #off Z cut
# 	cut += ' || (MllOS_allComb[2] > 80 && MllOS_allComb[2] < 100) )' #off Z cut

# 	cut += ' && ( (MllOS_allComb[0] <= 80 || MllOS_allComb[0] >= 100)' #off Z cut
# 	cut += ' || (MllOS_allComb[1] <= 80 || MllOS_allComb[1] >= 100)' #off Z cut
# 	cut += ' || (MllOS_allComb[2] <= 80 || MllOS_allComb[2] >= 100) )' #off Z cut

	isLepCut=''
	if category=='EEE': isLepCut+=' && isEEE==1'
	if category=='EEM': isLepCut+=' && isEEM==1'
	if category=='EMM': isLepCut+=' && isEMM==1'
	if category=='MMM': isLepCut+=' && isMMM==1'
	


#Start -- Method if isTTT doesnt exist
# 	'''
	if 'DataDrivenBkgTTT' in process: 
		cut+=' && (AllLeptonIsTight_PtOrdered[0]==1 && AllLeptonIsTight_PtOrdered[1]==1 && AllLeptonIsTight_PtOrdered[2]==1)'

	if 'DataDrivenBkgTTL' in process: 
		cut+=' && (AllLeptonIsTight_PtOrdered[0]==1 && AllLeptonIsTight_PtOrdered[1]==1 && AllLeptonIsTight_PtOrdered[2]==0)'
		if category=='EEE':
			cut+=' && (AllLeptonFlavor_PtOrdered[0]==0 && AllLeptonFlavor_PtOrdered[1]==0 && AllLeptonFlavor_PtOrdered[2]==0)'
		if category=='EEM':
			cut+=' && (AllLeptonFlavor_PtOrdered[0]==0 && AllLeptonFlavor_PtOrdered[1]==0 && AllLeptonFlavor_PtOrdered[2]==1)'
		if category=='EMM':
			cut+=' &&  ( (AllLeptonFlavor_PtOrdered[0]==0 && AllLeptonFlavor_PtOrdered[1]==1 && AllLeptonFlavor_PtOrdered[2]==1)'
			cut+=' ||    (AllLeptonFlavor_PtOrdered[0]==1 && AllLeptonFlavor_PtOrdered[1]==0 && AllLeptonFlavor_PtOrdered[2]==1) )'
		if category=='MMM':
			cut+=' && (AllLeptonFlavor_PtOrdered[0]==1 && AllLeptonFlavor_PtOrdered[1]==1 && AllLeptonFlavor_PtOrdered[2]==1)'
	if 'DataDrivenBkgTLT' in process: 
		cut+=' && (AllLeptonIsTight_PtOrdered[0]==1 && AllLeptonIsTight_PtOrdered[1]==1 && AllLeptonIsTight_PtOrdered[2]==0)'
		if category=='EEE':
			cut+=' && (AllLeptonFlavor_PtOrdered[0]==0 && AllLeptonFlavor_PtOrdered[1]==0 && AllLeptonFlavor_PtOrdered[2]==0)'
		if category=='EEM':
			cut+=' &&  ( (AllLeptonFlavor_PtOrdered[0]==0 && AllLeptonFlavor_PtOrdered[1]==1 && AllLeptonFlavor_PtOrdered[2]==0)'
			cut+=' ||    (AllLeptonFlavor_PtOrdered[0]==1 && AllLeptonFlavor_PtOrdered[1]==0 && AllLeptonFlavor_PtOrdered[2]==0) )'
		if category=='EMM':
			cut+=' &&  ( (AllLeptonFlavor_PtOrdered[0]==0 && AllLeptonFlavor_PtOrdered[1]==1 && AllLeptonFlavor_PtOrdered[2]==1)'
			cut+=' ||    (AllLeptonFlavor_PtOrdered[0]==1 && AllLeptonFlavor_PtOrdered[1]==0 && AllLeptonFlavor_PtOrdered[2]==1) )'
		if category=='MMM':
			cut+=' && (AllLeptonFlavor_PtOrdered[0]==1 && AllLeptonFlavor_PtOrdered[1]==1 && AllLeptonFlavor_PtOrdered[2]==1)'
	if 'DataDrivenBkgLTT' in process: 
		cut+=' && (AllLeptonIsTight_PtOrdered[0]==1 && AllLeptonIsTight_PtOrdered[1]==1 && AllLeptonIsTight_PtOrdered[2]==0)'
		if category=='EEE':
			cut+=' && (AllLeptonFlavor_PtOrdered[0]==0 && AllLeptonFlavor_PtOrdered[1]==0 && AllLeptonFlavor_PtOrdered[2]==0)'
		if category=='EEM':
			cut+=' &&  ( (AllLeptonFlavor_PtOrdered[0]==0 && AllLeptonFlavor_PtOrdered[1]==1 && AllLeptonFlavor_PtOrdered[2]==0)'
			cut+=' ||    (AllLeptonFlavor_PtOrdered[0]==1 && AllLeptonFlavor_PtOrdered[1]==0 && AllLeptonFlavor_PtOrdered[2]==0) )'
		if category=='EMM':
			cut+=' && (AllLeptonFlavor_PtOrdered[0]==1 && AllLeptonFlavor_PtOrdered[1]==1 && AllLeptonFlavor_PtOrdered[2]==0)'
		if category=='MMM':
			cut+=' && (AllLeptonFlavor_PtOrdered[0]==1 && AllLeptonFlavor_PtOrdered[1]==1 && AllLeptonFlavor_PtOrdered[2]==1)'

	if 'DataDrivenBkgTLL' in process: 
		cut+=' && (AllLeptonIsTight_PtOrdered[0]==1 && AllLeptonIsTight_PtOrdered[1]==0 && AllLeptonIsTight_PtOrdered[2]==0)'
		if category=='EEE':
			cut+=' && (AllLeptonFlavor_PtOrdered[0]==0 && AllLeptonFlavor_PtOrdered[1]==0 && AllLeptonFlavor_PtOrdered[2]==0)'
		if category=='EEM':
			cut+=' &&  ( (AllLeptonFlavor_PtOrdered[0]==0 && AllLeptonFlavor_PtOrdered[1]==0 && AllLeptonFlavor_PtOrdered[2]==1)'
			cut+=' ||    (AllLeptonFlavor_PtOrdered[0]==0 && AllLeptonFlavor_PtOrdered[1]==1 && AllLeptonFlavor_PtOrdered[2]==0) )'
		if category=='EMM':
			cut+=' && (AllLeptonFlavor_PtOrdered[0]==0 && AllLeptonFlavor_PtOrdered[1]==1 && AllLeptonFlavor_PtOrdered[2]==1)'
		if category=='MMM':
			cut+=' && (AllLeptonFlavor_PtOrdered[0]==1 && AllLeptonFlavor_PtOrdered[1]==1 && AllLeptonFlavor_PtOrdered[2]==1)'
	if 'DataDrivenBkgLTL' in process: 
		cut+=' && (AllLeptonIsTight_PtOrdered[0]==1 && AllLeptonIsTight_PtOrdered[1]==0 && AllLeptonIsTight_PtOrdered[2]==0)'
		if category=='EEE':
			cut+=' && (AllLeptonFlavor_PtOrdered[0]==0 && AllLeptonFlavor_PtOrdered[1]==0 && AllLeptonFlavor_PtOrdered[2]==0)'
		if category=='EEM':
			cut+=' &&  ( (AllLeptonFlavor_PtOrdered[0]==0 && AllLeptonFlavor_PtOrdered[1]==0 && AllLeptonFlavor_PtOrdered[2]==1)'
			cut+=' ||    (AllLeptonFlavor_PtOrdered[0]==0 && AllLeptonFlavor_PtOrdered[1]==1 && AllLeptonFlavor_PtOrdered[2]==0) )'
		if category=='EMM':
			cut+=' &&  ( (AllLeptonFlavor_PtOrdered[0]==1 && AllLeptonFlavor_PtOrdered[1]==0 && AllLeptonFlavor_PtOrdered[2]==1)'
			cut+=' ||    (AllLeptonFlavor_PtOrdered[0]==1 && AllLeptonFlavor_PtOrdered[1]==1 && AllLeptonFlavor_PtOrdered[2]==0) )'
		if category=='MMM':
			cut+=' && (AllLeptonFlavor_PtOrdered[0]==1 && AllLeptonFlavor_PtOrdered[1]==1 && AllLeptonFlavor_PtOrdered[2]==1)'
	if 'DataDrivenBkgLLT' in process: 
		cut+=' && (AllLeptonIsTight_PtOrdered[0]==1 && AllLeptonIsTight_PtOrdered[1]==0 && AllLeptonIsTight_PtOrdered[2]==0)'
		if category=='EEE':
			cut+=' && (AllLeptonFlavor_PtOrdered[0]==0 && AllLeptonFlavor_PtOrdered[1]==0 && AllLeptonFlavor_PtOrdered[2]==0)'
		if category=='EEM':
			cut+=' && (AllLeptonFlavor_PtOrdered[0]==1 && AllLeptonFlavor_PtOrdered[1]==0 && AllLeptonFlavor_PtOrdered[2]==0)'
		if category=='EMM':
			cut+=' &&  ( (AllLeptonFlavor_PtOrdered[0]==1 && AllLeptonFlavor_PtOrdered[1]==0 && AllLeptonFlavor_PtOrdered[2]==1)'
			cut+=' ||    (AllLeptonFlavor_PtOrdered[0]==1 && AllLeptonFlavor_PtOrdered[1]==1 && AllLeptonFlavor_PtOrdered[2]==0) )'
		if category=='MMM':
			cut+=' && (AllLeptonFlavor_PtOrdered[0]==1 && AllLeptonFlavor_PtOrdered[1]==1 && AllLeptonFlavor_PtOrdered[2]==1)'

	if 'DataDrivenBkgLLL' in process: 
		cut+=' && (AllLeptonIsTight_PtOrdered[0]==0 && AllLeptonIsTight_PtOrdered[1]==0 && AllLeptonIsTight_PtOrdered[2]==0)'
# 	'''
#End -- Method if isTTT doesnt exist

#Start -- Method if isTTT  exist
	'''
	if 'DataDrivenBkgTTT' in process: cut+=' && isTTT==1'
	if 'DataDrivenBkgTTL' in process: cut+=' && isTTL==1'
	if 'DataDrivenBkgTLT' in process: cut+=' && isTLT==1'
	if 'DataDrivenBkgLTT' in process: cut+=' && isLTT==1'
	if 'DataDrivenBkgTLL' in process: cut+=' && isTLL==1'
	if 'DataDrivenBkgLTL' in process: cut+=' && isLTL==1'
	if 'DataDrivenBkgLLT' in process: cut+=' && isLLT==1'
	if 'DataDrivenBkgLLL' in process: cut+=' && isLLL==1'
	'''
#End -- Method if isTTT exist


# 	if 'DataDrivenBkg' in process:
# 		cut+=' && (AllLeptonIsTight_PtOrdered[0]==0 || AllLeptonIsTight_PtOrdered[1]==0 || AllLeptonIsTight_PtOrdered[2]==0)'
# 	if 'DataDrivenBkg' not in process:
# 		cut+=' && (AllLeptonIsTight_PtOrdered[0]==1 && AllLeptonIsTight_PtOrdered[1]==1 && AllLeptonIsTight_PtOrdered[2]==1)'

	if 'PrunedSmearedNm1' in discriminantName: cut += ' && (theJetAK8NjettinessTau2_JetSubCalc_PtOrdered/theJetAK8NjettinessTau1_JetSubCalc_PtOrdered < 0.6)'

	massvar = 'theJetAK8PrunedMassJMRSmeared_JetSubCalc'
	if 'Data' in process: massvar = 'theJetAK8PrunedMass_JetSubCalc_PtOrdered'

	if 'Tau21Nm1' in discriminantName:  cut += ' && ('+massvar+' > 65 && '+massvar+' < 105)'

	TrigEff = 'TrigEffWeight'
		
	print "Applying Cuts: ", cut
	
	doDDBKGsys = True

	hists = {}
	hists[discriminantName+'_'+lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'_'+lumiStr+'fb_'+category+'_' +process,xAxisLabel,len(xbins)-1,xbins)
	if doAllSys or doDDBKGsys:
		if doDDBKGsys and 'DataDrivenBkg' in process: 	
			hists[discriminantName+'PRUp_'     +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'PRUp_'     +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			hists[discriminantName+'PRDown_'   +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'PRDown_'   +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			hists[discriminantName+'FRUp_'     +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'FRUp_'     +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			hists[discriminantName+'FRDown_'   +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'FRDown_'   +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		elif doAllSys:			
			hists[discriminantName+'pileupUp_'  +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'pileupUp_'  +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			hists[discriminantName+'pileupDown_'+lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'pileupDown_'+lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			hists[discriminantName+'muRFcorrdUp_'  +lumiStr+'fb_'+category+'_'+process]=R.TH1D(discriminantName+'muRFcorrdUp_'  +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			hists[discriminantName+'muRFcorrdDown_'+lumiStr+'fb_'+category+'_'+process]=R.TH1D(discriminantName+'muRFcorrdDown_'+lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			hists[discriminantName+'muRUp_'     +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'muRUp_'     +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			hists[discriminantName+'muRDown_'   +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'muRDown_'   +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			hists[discriminantName+'muFUp_'     +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'muFUp_'     +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			hists[discriminantName+'muFDown_'   +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'muFDown_'   +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
# 			hists[discriminantName+'topptUp_'   +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'topptUp_'   +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
# 			hists[discriminantName+'topptDown_' +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'topptDown_' +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
# 			hists[discriminantName+'jmrUp_'     +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'jmrUp_'     +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
# 			hists[discriminantName+'jmrDown_'   +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'jmrDown_'   +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
# 			hists[discriminantName+'jmsUp_'     +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'jmsUp_'     +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
# 			hists[discriminantName+'jmsDown_'   +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'jmsDown_'   +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
# 			hists[discriminantName+'tau21Up_'   +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'tau21Up_'   +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
# 			hists[discriminantName+'tau21Down_' +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'tau21Down_' +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
# 			hists[discriminantName+'jsfUp_'     +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'jsfUp_'     +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
# 			hists[discriminantName+'jsfDown_'   +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'jsfDown_'   +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)

			hists[discriminantName+'btagUp_'    +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'btagUp_'    +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			hists[discriminantName+'btagDown_'  +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'btagDown_'  +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			hists[discriminantName+'bmistagUp_'    +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'bmistagUp_'    +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			hists[discriminantName+'bmistagDown_'  +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'bmistagDown_'  +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)


# 			if tTree[process+'jecUp']:		
# 				hists[discriminantName+'jecUp_'   +lumiStr+'fb_'+category+'_'+process]  = R.TH1D(discriminantName+'jecUp_'   +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
# 				hists[discriminantName+'jecDown_' +lumiStr+'fb_'+category+'_'+process]  = R.TH1D(discriminantName+'jecDown_' +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
# 			if tTree[process+'jerUp']:		
# 				hists[discriminantName+'jerUp_'   +lumiStr+'fb_'+category+'_'+process]  = R.TH1D(discriminantName+'jerUp_'   +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
# 				hists[discriminantName+'jerDown_' +lumiStr+'fb_'+category+'_'+process]  = R.TH1D(discriminantName+'jerDown_' +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
# 			if tTree[process+'btagUp']:		
# 				hists[discriminantName+'btagUp_'  +lumiStr+'fb_'+category+'_'+process]  = R.TH1D(discriminantName+'btagUp_'  +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
# 				hists[discriminantName+'btagDown_'+lumiStr+'fb_'+category+'_'+process]  = R.TH1D(discriminantName+'btagDown_'+lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			for i in range(100): hists[discriminantName+'pdf'+str(i)+'_'+lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'pdf'+str(i)+'_'+lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
	for key in hists.keys(): hists[key].Sumw2()
		
	if 'Data' in process: 
		if ('DataDrivenBkg' in process):
			if ('TTT' in process or 'TTL' in process or 'TLT' in process or 'LTT' in process or 'TLL' in process or 'LTL' in process or 'LLT' in process or 'LLL' in process):  
				weightStr         ='1'
				weightPRUpStr     ='1'
				weightPRDownStr   ='1'
				weightFRUpStr     ='1'
				weightFRDownStr   ='1'
				print 'weightStr-------------------------------------------------------->', weightStr
			else: 
				print 'process----------------------------------------------------------> ', process
				weightStr         ='ddBkgWeights[0]'
				weightPRUpStr     ='ddBkgWeights[3]'
				weightPRDownStr   ='ddBkgWeights[4]'
				weightFRUpStr     ='ddBkgWeights[1]'
				weightFRDownStr   ='ddBkgWeights[2]'
		else: 
			weightStr         ='1'
			weightPRUpStr     ='1'
			weightPRDownStr   ='1'
			weightFRUpStr     ='1'
			weightFRDownStr   ='1'

		weightPileupUpStr   = '1'
		weightPileupDownStr = '1'
		weightmuRFcorrdUpStr   = '1'
		weightmuRFcorrdDownStr = '1'
		weightmuRUpStr   = '1'
		weightmuRDownStr = '1'
		weightmuFUpStr   = '1'
		weightmuFDownStr = '1'
		weighttopptUpStr    = '1'
		weighttopptDownStr  = '1'
		weightjsfUpStr    = '1'
		weightjsfDownStr  = '1'		

	else: 
		weightStr           = TrigEff+' * pileupWeight * 1 * isoSF * lepIdSF * EGammaGsfSF * MuTrkSF * MCWeight_singleLepCalc/abs(MCWeight_singleLepCalc) * '+str(weight[process])
# 		weightStr           = TrigEff+' * pileupWeight * 1 * isoSF * lepIdSF * MCWeight_singleLepCalc/abs(MCWeight_singleLepCalc) * '+str(weight[process])
# 		weightStr           = TrigEff+' * pileupWeight * JetSF_pTNbwflat * isoSF * lepIdSF * MCWeight_singleLepCalc/abs(MCWeight_singleLepCalc) * '+str(weight[process])
		weightPileupUpStr   = weightStr.replace('pileupWeight','pileupWeightUp')
		weightPileupDownStr = weightStr.replace('pileupWeight','pileupWeightDown')
		weightmuRFcorrdUpStr   = 'renormWeights[5] * '+weightStr
		weightmuRFcorrdDownStr = 'renormWeights[3] * '+weightStr
		weightmuRUpStr      = 'renormWeights[4] * '+weightStr
		weightmuRDownStr    = 'renormWeights[2] * '+weightStr
		weightmuFUpStr      = 'renormWeights[1] * '+weightStr
		weightmuFDownStr    = 'renormWeights[0] * '+weightStr
		weighttopptUpStr    = weightStr
		weighttopptDownStr  = 'topPtWeight * '+weightStr
		weightjsfUpStr      = weightStr.replace('JetSF','JetSFupwide')
		weightjsfDownStr    = weightStr.replace('JetSF','JetSFdnwide')

	if 'Data' in process:
		origname = discriminantLJMETName
		if discriminantName == 'NWJetsSmeared':
			discriminantLJMETName = 'NJetsWtagged_0p6'
		if '0p55' in discriminantName:
			discriminantLJMETName = 'NJetsWtagged_0p55'
		if discriminantName == 'PrunedSmeared':
			discriminantLJMETName = 'theJetAK8PrunedMass_JetSubCalc_PtOrdered'
			#discriminantLJMETName = 'theJetAK8PrunedMass_JetSubCalc_new'
		if origname != discriminantLJMETName:
			print 'NEW LJMET NAME:',discriminantLJMETName

	if 'Bjet1' in discriminantName or 'Mlb' in discriminantName or 'b1' in discriminantName:
		cut += ' && (NJetsCSVwithSF_JetSubCalc > 0)'
	if 'b2' in discriminantName:
		cut += ' && (NJetsCSVwithSF_JetSubCalc > 1)'

	if 'Mlj' in discriminantName: cut += ' && (NJetsCSVwithSF_JetSubCalc == 0)'
	
	#print discriminantLJMETName+' >> '+discriminantName+''+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isLepCut+')', 'GOFF'

	try:
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+''+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isLepCut+')', 'GOFF')
		print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> DRAW SUCCESSFULL!!!!!'
	except:
		print '--------------------------------------------------------------------------------------------------------------------------------------------------->>>>>>>>>>>>>>>>>>>>>>>>>Skip DRAW'

	if doAllSys or doDDBKGsys:
		if doDDBKGsys and 'DataDrivenBkg' in process: 
			print 'Processing ddbkg sys !'
			tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'PRUp_'     +lumiStr+'fb_'+category+'_'+process, weightPRUpStr+'*('+cut+isLepCut+')', 'GOFF')
			tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'PRDown_'   +lumiStr+'fb_'+category+'_'+process, weightPRDownStr+'*('+cut+isLepCut+')', 'GOFF')
			tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'FRUp_'     +lumiStr+'fb_'+category+'_'+process, weightFRUpStr+'*('+cut+isLepCut+')', 'GOFF')
			tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'FRDown_'   +lumiStr+'fb_'+category+'_'+process, weightFRDownStr+'*('+cut+isLepCut+')', 'GOFF')
		if doAllSys:
			print 'Processing ALL other sys !'
			tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'pileupUp_'  +lumiStr+'fb_'+category+'_'+process, weightPileupUpStr+'*('+cut+isLepCut+')', 'GOFF')
			tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'pileupDown_'+lumiStr+'fb_'+category+'_'+process, weightPileupDownStr+'*('+cut+isLepCut+')', 'GOFF')
			tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'muRFcorrdUp_'  +lumiStr+'fb_'+category+'_'+process, weightmuRFcorrdUpStr  +'*('+cut+isLepCut+')', 'GOFF')
			tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'muRFcorrdDown_'+lumiStr+'fb_'+category+'_'+process, weightmuRFcorrdDownStr+'*('+cut+isLepCut+')', 'GOFF')
			tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'muRUp_'     +lumiStr+'fb_'+category+'_'+process, weightmuRUpStr+'*('+cut+isLepCut+')', 'GOFF')
			tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'muRDown_'   +lumiStr+'fb_'+category+'_'+process, weightmuRDownStr+'*('+cut+isLepCut+')', 'GOFF')
			tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'muFUp_'     +lumiStr+'fb_'+category+'_'+process, weightmuFUpStr+'*('+cut+isLepCut+')', 'GOFF')
			tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'muFDown_'   +lumiStr+'fb_'+category+'_'+process, weightmuFDownStr+'*('+cut+isLepCut+')', 'GOFF')
# 			tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'topptUp_'   +lumiStr+'fb_'+category+'_'+process, weighttopptUpStr+'*('+cut+isLepCut+')', 'GOFF')
# 			tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'topptDown_' +lumiStr+'fb_'+category+'_'+process, weighttopptDownStr+'*('+cut+isLepCut+')', 'GOFF')
# 			tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'jsfUp_'     +lumiStr+'fb_'+category+'_'+process, weightjsfUpStr+'*('+cut+isLepCut+')', 'GOFF')
# 			tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'jsfDown_'   +lumiStr+'fb_'+category+'_'+process, weightjsfDownStr+'*('+cut+isLepCut+')', 'GOFF')
			
			bTagSFshiftName = discriminantLJMETName
			if 'NJetsCSV' in discriminantLJMETName: 
				bTagSFshiftName = discriminantLJMETName+'_shifts[0]'
			print 'BTAGup LJMET NAME',bTagSFshiftName.replace('_shifts[0]','_shifts[0]')
			tTree[process].Draw(bTagSFshiftName.replace('_shifts[0]','_shifts[0]')+' >> '+discriminantName+'btagUp'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isLepCut+')', 'GOFF')
			print 'BTAGdn LJMET NAME',bTagSFshiftName.replace('_shifts[0]','_shifts[1]')
			tTree[process].Draw(bTagSFshiftName.replace('_shifts[0]','_shifts[1]')+' >> '+discriminantName+'btagDown'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isLepCut+')', 'GOFF')
			print 'MISTAGup LJMET NAME',bTagSFshiftName.replace('_shifts[0]','_shifts[2]')
			tTree[process].Draw(bTagSFshiftName.replace('_shifts[0]','_shifts[2]')+' >> '+discriminantName+'mistagUp'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isLepCut+')', 'GOFF')
			print 'MISTAGdn LJMET NAME',bTagSFshiftName.replace('_shifts[0]','_shifts[3]')
			tTree[process].Draw(bTagSFshiftName.replace('_shifts[0]','_shifts[3]')+' >> '+discriminantName+'mistagDown'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isLepCut+')', 'GOFF')


# 			JMRName = discriminantLJMETName
# 			if discriminantLJMETName == 'theJetAK8PrunedMassJMRSmeared_JetSubCalc': JMRName = 'theJetAK8PrunedMassJMRSmearedUp_JetSubCalc'
# 			if discriminantLJMETName == 'NJetsWtagged_JMR': JMRName = 'NJetsWtagged_shifts[0]'
# 			if 'NJetsWtagged_0p' in discriminantLJMETName: JMRName = discriminantLJMETName+'_shifts[0]'
# 			if 'Wjet' in discriminantLJMETName: JMRName = discriminantLJMETName+'_shifts[0]'
# 			if 'WJetLeadPt' in discriminantLJMETName: JMRName = discriminantLJMETName+'_shifts[0]'
# 			if 'taggedW' in discriminantLJMETName: JMRName = discriminantLJMETName+'_shifts[0]'
# 			if 'WJetTaggedPt' in discriminantLJMETName: JMRName = discriminantLJMETName.replace('WJetTaggedPt','WJetTaggedPtJMRup')
# 			print 'JMRup LJMET NAME',JMRName
# 			tTree[process].Draw(JMRName+' >> '+discriminantName+'jmrUp'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isLepCut+')', 'GOFF')
# 
# 			JMRName = discriminantLJMETName
# 			if discriminantLJMETName == 'theJetAK8PrunedMassJMRSmeared_JetSubCalc': JMRName = 'theJetAK8PrunedMassJMRSmearedDn_JetSubCalc'
# 			if discriminantLJMETName == 'NJetsWtagged_JMR': JMRName = 'NJetsWtagged_shifts[1]'
# 			if 'NJetsWtagged_0p' in discriminantLJMETName: JMRName = discriminantLJMETName+'_shifts[1]'
# 			if 'Wjet' in discriminantLJMETName: JMRName = discriminantLJMETName+'_shifts[1]'
# 			if 'WJetLeadPt' in discriminantLJMETName: JMRName = discriminantLJMETName+'_shifts[1]'
# 			if 'taggedW' in discriminantLJMETName: JMRName = discriminantLJMETName+'_shifts[1]'
# 			if 'WJetTaggedPt' in discriminantLJMETName: JMRName = discriminantLJMETName.replace('WJetTaggedPt','WJetTaggedPtJMRdn')
# 			print 'JMRdn LJMET NAME',JMRName
# 			tTree[process].Draw(JMRName+' >> '+discriminantName+'jmrDown'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isLepCut+')', 'GOFF')
# 
# 			JMSName = discriminantLJMETName
# 			if discriminantLJMETName == 'NJetsWtagged_JMR': JMRName = 'NJetsWtagged_shifts[2]'
# 			if 'NJetsWtagged_0p' in discriminantLJMETName: JMRName = discriminantLJMETName+'_shifts[2]'
# 			if 'Wjet' in discriminantLJMETName: JMRName = discriminantLJMETName+'_shifts[2]'
# 			if 'WJetLeadPt' in discriminantLJMETName: JMRName = discriminantLJMETName+'_shifts[2]'
# 			if 'taggedW' in discriminantLJMETName: JMRName = discriminantLJMETName+'_shifts[2]'
# 			if 'WJetTaggedPt' in discriminantLJMETName: JMSName = discriminantLJMETName.replace('WJetTaggedPt','WJetTaggedPtJMSup')
# 			print 'JMSup LJMET NAME',JMSName
# 			tTree[process].Draw(JMSName+' >> '+discriminantName+'jmsUp'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isLepCut+')', 'GOFF')
# 
# 			JMSName = discriminantLJMETName
# 			if discriminantLJMETName == 'NJetsWtagged_JMR': JMRName = 'NJetsWtagged_shifts[3]'
# 			if 'NJetsWtagged_0p' in discriminantLJMETName: JMRName = discriminantLJMETName+'_shifts[3]'
# 			if 'Wjet' in discriminantLJMETName: JMSName = discriminantLJMETName+'_shifts[3]'
# 			if 'WJetLeadPt' in discriminantLJMETName: JMRName = discriminantLJMETName+'_shifts[3]'
# 			if 'taggedW' in discriminantLJMETName: JMSName = discriminantLJMETName+'_shifts[3]'
# 			if 'WJetTaggedPt' in discriminantLJMETName: JMSName = discriminantLJMETName.replace('WJetTaggedPt','WJetTaggedPtJMSdn')
# 			print 'JMSdn LJMET NAME',JMSName
# 			tTree[process].Draw(JMSName+' >> '+discriminantName+'jmsDown'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isLepCut+')', 'GOFF')
# 
# 			TAUName = discriminantLJMETName
# 			if discriminantLJMETName == 'NJetsWtagged_JMR': JMRName = 'NJetsWtagged_shifts[4]'
# 			if 'NJetsWtagged_0p' in discriminantLJMETName: JMRName = discriminantLJMETName+'_shifts[4]'
# 			if 'Wjet' in discriminantLJMETName: TAUName = discriminantLJMETName+'_shifts[4]'
# 			if 'WJetLeadPt' in discriminantLJMETName: JMRName = discriminantLJMETName+'_shifts[4]'
# 			if 'taggedW' in discriminantLJMETName: TAUName = discriminantLJMETName+'_shifts[4]'
# 			if 'WJetTaggedPt' in discriminantLJMETName: TAUName = discriminantLJMETName.replace('WJetTaggedPt','WJetTaggedPtTAUup')
# 			print 'TAUup LJMET NAME',TAUName
# 			tTree[process].Draw(TAUName+' >> '+discriminantName+'tau21Up'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isLepCut+')', 'GOFF')
# 
# 			TAUName = discriminantLJMETName
# 			if discriminantLJMETName == 'NJetsWtagged_JMR': JMRName = 'NJetsWtagged_shifts[5]'
# 			if 'NJetsWtagged_0p' in discriminantLJMETName: JMRName = discriminantLJMETName+'_shifts[5]'
# 			if 'Wjet' in discriminantLJMETName: TAUName = discriminantLJMETName+'_shifts[5]'
# 			if 'WJetLeadPt' in discriminantLJMETName: JMRName = discriminantLJMETName+'_shifts[5]'
# 			if 'taggedW' in discriminantLJMETName: TAUName = discriminantLJMETName+'_shifts[5]'
# 			if 'WJetTaggedPt' in discriminantLJMETName: TAUName = discriminantLJMETName.replace('WJetTaggedPt','WJetTaggedPtTAUdn')
# 			print 'TAUdn LJMET NAME',TAUName
# 			tTree[process].Draw(TAUName+' >> '+discriminantName+'tau21Down'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isLepCut+')', 'GOFF')		

# 			if tTree[process+'jecUp']:
# 				tTree[process+'jecUp'].Draw(discriminantLJMETName   +' >> '+discriminantName+'jecUp'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isLepCut+')', 'GOFF')
# 				tTree[process+'jecDown'].Draw(discriminantLJMETName +' >> '+discriminantName+'jecDown'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isLepCut+')', 'GOFF')
# 			if tTree[process+'jerUp']:
# 				tTree[process+'jerUp'].Draw(discriminantLJMETName   +' >> '+discriminantName+'jerUp'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isLepCut+')', 'GOFF')
# 				tTree[process+'jerDown'].Draw(discriminantLJMETName +' >> '+discriminantName+'jerDown'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isLepCut+')', 'GOFF')

# # 			if tTree[process+'btagUp']:
# # 				tTree[process+'btagUp'].Draw(discriminantLJMETName  +' >> '+discriminantName+'btagUp'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isLepCut+')', 'GOFF')
# # 				tTree[process+'btagDown'].Draw(discriminantLJMETName+' >> '+discriminantName+'btagDown'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isLepCut+')', 'GOFF')

			for i in range(100): tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'pdf'+str(i)+'_'+lumiStr+'fb_'+category+'_'+process, 'pdfWeights['+str(i)+'] * '+weightStr+'*('+cut+isLepCut+')', 'GOFF')
	
	for key in hists.keys(): 
		#print key
		hists[key].SetDirectory(0)	

	#print hists
	
	return hists
