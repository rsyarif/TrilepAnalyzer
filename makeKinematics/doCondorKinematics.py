import os,sys,datetime

thisDir = os.getcwd()
# outputDir = thisDir+'/'
relbase = '/home/rsyarif/LJMet/TprimeAnalysis/CMSSW_7_6_3/src/'
outputDir = '/user_data/rsyarif/'


cTime=datetime.datetime.now()
date='%i_%i_%i'%(cTime.year,cTime.month,cTime.day)
time='%i_%i_%i'%(cTime.hour,cTime.minute,cTime.second)

# pfix='kinematics_80x_condor_Exactly3Lep_no2Dcut_noMllOScut_dilepTrigReady_fixedSF'

# pfix='kinematics_80x_condor_Exactly3Lep_no2Dcut_noMllOScut_dilepTrigReady_noDDBKG'

# pfix='kinematics_80x_condor_Exactly3Lep_no2Dcut_noMllOScut_dilepTrigReady_noDDBKG_fixedSF'

# pfix='kinematics_80x_condor_Exactly3Lep_no2Dcut_noMllOScut_dilepTrigReady_fixedSF_1bjet'

# pfix='kinematics_80x_condor_Exactly3Lep_no2Dcut_noMllOScut_dilepTrigReady_fixedSF_1bjet_mllOSmin20'

# pfix='kinematics_80x_condor_Exactly3Lep_no2Dcut_dilepTrigReady_fixedSF_mllOSmin0'

# pfix='kinematics_80x_condor_Exactly3Lep_no2Dcut_dilepTrigReady_fixedSF_1bjet_mllOSmin20'

# pfix='kinematics_80x_condor_Exactly3Lep_no2Dcut_dilepTrigReady_fixedSF_1bjet_mllOSmin20_st600'

# pfix='kinematics_80x_condor_Exactly3Lep_no2Dcut_dilepTrigReady_fixedSF_mllOSmin20_FRv2'

# pfix='kinematics_80x_condor_Exactly3Lep_no2Dcut_dilepTrigReady_fixedSF_mllOSmin20_FRv2_step2'

# pfix='kinematics_80x_condor_Exactly3Lep_no2Dcut_dilepTrigReady_fixedSF_mllOSmin20_1bjet_FRv2_step2'

# pfix='kinematics_80x_condor_Exactly3Lep_no2Dcut_dilepTrigReady_fixedSF_mllOSmin0_step2'

# pfix='kinematics_80x_condor_Exactly3Lep_no2Dcut_dilepTrigReady_fixedSF_mllOSmin20_step2'

# pfix='kinematics_80x_condor_Exactly3Lep_no2Dcut_dilepTrigReady_fixedSF_mllOSmin20_FRv3_step2'

# pfix='kinematics_80x_condor_Exactly3Lep_no2Dcut_dilepTrigReady_fixedSF_mllOSmin20_FRv3_step2_noDDBKG'

# pfix='kinematics_80x_condor_Exactly3Lep_no2Dcut_dilepTrigReady_fixedSF_mllOSmin20_FRv3_step2_noDDBKG_MoreThan2Jets'

# pfix='kinematics_80x_condor_Exactly3Lep_no2Dcut_dilepTrigReady_fixedSF_mllOSmin20_FRv3_step2_noDDBKG_exactly2Jets'

# pfix='kinematics_80x_condor_Exactly3Lep_no2Dcut_dilepTrigReady_fixedSF_mllOSmin20_FRv3_step2_1bjet'

# pfix='kinematics_80x_condor_Exactly3Lep_no2Dcut_dilepTrigReady_fixedSF_mllOSmin20_FRv3_step2_v2'

#pfix='kinematics_80x_condor_Exactly3Lep_no2Dcut_dilepTrigReady_fixedSF_mllOSmin20_FRv3_step2_noDDBKG_v2'

# pfix='kinematics_80x_condor_Exactly3Lep_no2Dcut_dilepTrigReady_fixedSF_mllOSmin20_FRv3_step2_noDDBKG_v2_noNjetCut'

# pfix='kinematics_80x_condor_Exactly3Lep_no2Dcut_dilepTrigReady_fixedSF_mllOSmin20_FRv3_step2_noDDBKG_v2_moreThan2Jets'

# pfix='kinematics_80x_condor_Exactly3Lep_no2Dcut_dilepTrigReady_fixedSF_mllOSmin20_FRv3_step2_noDDBKG_v2_exactly2Jets'

# pfix='kinematics_80x_condor_Exactly3Lep_no2Dcut_dilepTrigReady_fixedSF_mllOSmin20_FRv3_step2_noDDBKG_v2_exactly1Jet'

# pfix='kinematics_80x_condor_Exactly3Lep_no2Dcut_dilepTrigReady_fixedSF_mllOSmin20_FRv3_step2_noDDBKG_v2_exactly0Jet'

# pfix='kinematics_80x_condor_Exactly3Lep_no2Dcut_dilepTrigReady_fixedSF_mllOSmin20_FRv3_step2_noDDBKG_v2_lessThan3Jets'

# pfix='kinematics_80x_condor_Exactly3Lep_no2Dcut_dilepTrigReady_fixedSF_mllOSmin20_FRv3_step2_noDDBKG_v2_1or2Jets'

# pfix='kinematics_80x_condor_Exactly3Lep_no2Dcut_dilepTrigReady_fixedSF_mllOSmin20_FRv3_step2_v2_noNjetCut'

# pfix='kinematics_80x_condor_Exactly3Lep_no2Dcut_dilepTrigReady_fixedSF_mllOSmin20_FRv3_step2_v2_moreThan2Jets'

# pfix='kinematics_80x_condor_Exactly3Lep_no2Dcut_dilepTrigReady_fixedSF_mllOSmin20_FRv3_step2_v2_exactly2Jets'

# pfix='kinematics_80x_condor_Exactly3Lep_no2Dcut_dilepTrigReady_fixedSF_mllOSmin20_FRv3_step2_v2_exactly1Jet'

# pfix='kinematics_80x_condor_Exactly3Lep_no2Dcut_dilepTrigReady_fixedSF_mllOSmin20_FRv3_step2_v2_exactly0Jet'

# pfix='kinematics_80x_condor_Exactly3Lep_no2Dcut_dilepTrigReady_fixedSF_mllOSmin20_FRv3_step2_v2_lessThan3Jets'

# pfix='kinematics_80x_condor_Exactly3Lep_no2Dcut_dilepTrigReady_fixedSF_mllOSmin20_FRv3_step2_v2_1or2Jets'

# pfix='kinematics_80x_condor_Exactly3Lep_no2Dcut_dilepTrigReady_fixedSF_mllOSmin20_FRv3_step2_v2_minDRlep3Jet0p05'

# pfix='kinematics_80x_condor_Exactly3Lep_SUSYID_nJets2'

# pfix='kinematics_80x_condor_Exactly3Lep_SUSYID'

# pfix='kinematics_80x_condor_MultiLep_FRv4_step2_moreThan2Jets'

# pfix='kinematics_80x_condor_Exactly3Lep_FRv4_step2_moreThan2Jets'

# pfix='kinematics_80x_condor_Exactly3Lep_FRv5_step2_moreThan2Jets'

# pfix='kinematics_80x_condor_MultiLep_FRv5_step2_moreThan2Jets'

# pfix='kinematics_80x_condor_MultiLep_FRv4_step2_moreThan2Jets_DOUBLECHECK'

# pfix='kinematics_80x_condor_MultiLep_FRv5_step2_moreThan2Jets_DOUBLECHECK'

# pfix='kinematics_80x_condor_MultiLep_FRv4_step2_moreThan2Jets_DOUBLECHECK_withSYS'

# pfix='kinematics_80x_condor_MultiLep_FRv5_step2_moreThan2Jets_DOUBLECHECK_withSYS'

# pfix='kinematics_80x_condor_MultiLep_FRv5_step2_moreThan2Jets_withALLSYS'

# pfix='kinematics_80x_condor_MultiLep_FRv5_step2_moreThan2Jets_withALLSYS_ST600'

# pfix='kinematics_80x_condor_MultiLep_FRv5_step2_moreThan2Jets_withALLSYS_ST700'
# 
# pfix='kinematics_80x_condor_MultiLep_FRv5_step2_moreThan2Jets_withALLSYS_ST800'
# 
# pfix='kinematics_80x_condor_MultiLep_FRv5_step2_moreThan2Jets_withALLSYS_ST900'
# 
# pfix='kinematics_80x_condor_MultiLep_FRv5_step2_moreThan2Jets_withALLSYS_ST1000'

# pfix='kinematics_80x_condor_Exactly3Lep_FRv5_step2_exactly2Jets_noSYS'

# pfix='kinematics_80x_condor_MultiLep_FRv6_step2_moreThan2Jets_1bjet_withALLSYS'

# pfix='kinematics_80x_condor_MultiLep_FRv7_PRv2_step2_moreThan2Jets_withALLSYS'

# pfix='kinematics_80x_condor_Exactly3Lep_FRv7_PRv2_step2_exactly2Jets_noSYS'

pfix='kinematics_80x_condor_MultiLep_FRv7_PRv2_step2_exactly2Jets_withALLSYS'


pfix+='_'+date
#pfix+='_'+date+'_'+time
# pfix+='_no_jsf'

plotList = [#distribution name as defined in "doHists.py"
	'NPV',
	'lepPt',
	'ElPt',
	'MuPt',
# 	'lep1Pt',
# 	'lep2Pt',
# 	'lep3Pt',
	'lepEta',
	'ElEta',
	'MuEta',
# 	'lep1Eta',
# 	'lep2Eta',
# 	'lep3Eta',
 	'JetEta',
#  	'Jet1Eta',
#  	'Jet2Eta',
	'JetPt' ,
# 	'Jet1Pt',
# 	'Jet2Pt',
	'HT',
	'HTrebinned',
	'ST',
	'STrebinned',
	'MET',
	'METrebinned',
	'NJets' ,
	'NBJets',
	'NBJetsCorr',
# 	'mindeltaRlepJets',
# 	'mindeltaRlep1Jets',
# 	'mindeltaRlep2Jets',
# 	'mindeltaRlep3Jets',
# 	'mindeltaRB',
# 	'mindeltaR1',
# 	'mindeltaR2',
# 	'mindeltaR3',
# 	'lepCharge',
# 	'lepIso',
# 	'ElIso',
# 	'MuIso',
# 	'PtRel1',
# 	'PtRel2',
# 	'PtRel3',
	'MllsameFlavorOS',
	'MllOSall',
	'MllOSallmin',
	'Mlll',
	]

catList = ['EEE','EEM','EMM','MMM','All']

outDir = outputDir+pfix
if not os.path.exists(outDir): os.system('mkdir '+outDir)
os.chdir(outDir)

count = 0
for distribution in plotList:
	for cat in catList:
		print cat
		if not os.path.exists(outDir+'/'+cat): os.system('mkdir '+cat)
		os.chdir(cat)
		
# 		dict={'dir':outputDir,'dist':distribution,'cat':cat}
# 		dict={'dir':thisDir,'dist':distribution,'cat':cat}
# 		dict={'CMSSWBASE':relbase,'dir':outputDir,'dist':distribution,'cat':cat}
		dict={'CMSSWBASE':relbase,'thisDir':thisDir,'dist':distribution,'cat':cat}


		jdf=open('condor_'+distribution+'.job','w')
		jdf.write(
"""universe = vanilla
Executable = %(thisDir)s/doCondorKinematics.sh
Should_Transfer_Files = YES
transfer_input_files = %(thisDir)s/doHists.py,%(thisDir)s/samples.py,%(thisDir)s/weights.py,%(thisDir)s/analyze.py
WhenToTransferOutput = ON_EXIT

arguments      = ""

Output = condor_%(dist)s.out
Error = condor_%(dist)s.err
Log = condor_%(dist)s.log
Notification = Error
Arguments = %(CMSSWBASE)s %(dist)s %(cat)s

Queue 1"""%dict)
		jdf.close()

		os.system('condor_submit condor_'+distribution+'.job')
		os.chdir('..')
		count+=1
									
print "Total jobs submitted:", count



                  
