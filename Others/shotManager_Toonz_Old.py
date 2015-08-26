'''
    Author:	Jojan
    Descrptn:	Manages shot's workflow: staging -> animation -> shotfinal -> lighting.
		Referencing assets is NOT included in this code.
'''

import re, os, shutil
import maya.cmds as mc
import maya.mel as mel

import Utils; reload(Utils)
import createReference; reload(createReference)

util = None


def getEpiAndShotFromUI():
	'''Get episod and shot from Shot Manager window'''
	
	episod = str(mc.optionMenu('optEpi', q=True, v=True)).zfill(3)
	if not mc.optionMenu('optShot', q=True, v=True):
		mc.confirmDialog(t='Error', m='No shot selected!', b='SORRY')
		return episod, None
	
	tmp = mc.optionMenu('optShot', q=True, v=True)
	shot = tmp.zfill(3 + (len(tmp) == 4))
	return episod, shot


def openScene(flag):
	'''Open specified shot/version from workspace/{staging|animation|shotfinal}'''
	
	episod, shot = getEpiAndShotFromUI()
	if not shot:	return
	
	shotId = '%s%ssh%s' % (util.epOrSeq, episod, shot)
	
	if flag:	# Open the selected version
		vers = mc.optionMenu('optVers', q=True, v=True).zfill(2)
		if vers == '00':
			mc.confirmDialog(t='Warning', m='         No version', b='OK')
			return
		
		shotFldr = '%s/%s/%s%s/sh%s/versions' % (util.path, util.deptDic['wkspcFldr'], util.epOrSeq, episod, shot)
		scene = '%s/%s_%s_%s_v%s' % (shotFldr, util.projShort, shotId, util.deptDic['short'], vers)
		
		rtk = mc.text('txtRtk', q=True, l=True).zfill(2)
		if os.path.exists('%s_rtk%s.ma' % (scene, rtk)):
			scene += '_rtk%s' % rtk
		scene += '.ma'
	
	
	else:	# Open final shot, i.e; ..._v00
		shotFldr = '%s/%s/%s%s/sh%s' % (util.path, util.deptDic['wkspcFldr'], util.epOrSeq, episod, shot)
		scene = '%s/%s_%s%ssh%s_%s_v00.ma' % (shotFldr, util.projShort, util.epOrSeq, episod, shot, util.deptDic['short'])
	
	
	if mc.file(scene, q=True, ex=True):
		try:
			mc.loadPlugin( 'studioImport.mll' )
		except:
			pass
		
		loadNoRef = mc.checkBox('chkRef', q=True, v=True)
		if loadNoRef:	# Load no references, and show Reference Editor
			#Suneeth FEB07
			cancel = mel.eval('saveChanges("file -f -new")')
			if not cancel:
				return
			#Suneeth FEB07
			mc.file(scene, o=True, lrd='none', f=True)
			mel.eval('tearOffPanel "Reference Editor" referenceEditor true;')
		
		else:		# Load all references
			#Suneeth FEB07
			cancel = mel.eval('saveChanges("file -f -new")')
			if not cancel:
				return
			#Suneeth FEB07
			mc.file(scene, o=True, f=True)
		
		util.prepareForPlayblast(shotId, False)
		mel.eval('addRecentFile("%s", "mayaAscii");' % scene)	# Add to File -> Recent Files
	
	else:
		mc.confirmDialog(t='Error', m='No such shot:\n%s' % scene.replace('/', '\\'), b='SORRY')


def displayRetake(filename='', changeDisplay=True):
	
	if not filename:
		episod, shot = getEpiAndShotFromUI()
		if not shot:	return
		dept = mc.optionMenu('optDept', q=True, v=True).lower()
		vers = mc.optionMenu('optVers', q=True, v=True).zfill(2)
				
		versFldr = '%s/%s/%s%s/sh%s/versions' % (util.path, util.deptDic['wkspcFldr'], util.epOrSeq, episod, shot)
		shotName = '%s_%s%ssh%s_%s_v%s_rtk' % (util.projShort, util.epOrSeq, episod, shot, util.deptDic['short'], vers)
		for i in xrange(100):
			if os.path.exists('%s/%s%s.ma' % (versFldr, shotName, str(i).zfill(2))):
				filename = '%s%s' % (shotName, str(i).zfill(2))
				break
	
	if '_rtk' in filename:
		indx = filename.find('_rtk')
		rtk = filename[indx+4: indx+6]
	else:
		rtk = 0
	
	if changeDisplay:
		mc.text('txtRtk', e=True, l=int(rtk))
	return rtk


def displayLastVersion(dept=None, showErr=True):
	
	def clearVersMenu():
		'''Clear versions menuItems'''
		
		versOld = mc.optionMenu('optVers', q=True, ils=True)
		if versOld:
			for x in versOld:
				mc.deleteUI(x, mi=1)
		mc.text('txtRtk', e=True, l='00')
	
	
	episod, shot = getEpiAndShotFromUI()
	if not shot:	return
	
	if not dept:
		dept = mc.optionMenu('optDept', q=True, v=True)
	
	shotFldr = '%s/%s/%s%s/sh%s/versions' % (util.path, util.deptDic['wkspcFldr'], util.epOrSeq, episod, shot)
	versionsSaved = []
	
	if not os.path.exists(shotFldr):	# No version
		lastVers = '00'; lastRetake = '00'
	
	else:
		expr = '%s_%s[0-9]{3}sh[0-9]{3}[a-z]?_[a-z]{2}_v[0-9]{2}.*[.]ma$' % (util.projShort, util.epOrSeq)
		versions = [ x for x in sorted(os.listdir(shotFldr)) if re.search(expr, x) ]
		if versions:
			try:
				for fil in versions:		# e.g; jjg_ep001sh001_st_v03_rtk01.ma
					indx = fil.find('_v')
					vers = fil[indx+2: indx+4]
					try:
						versionsSaved.append( vers )
					except:
						pass
				lastVersFile = fil
				lastVers = vers
				lastRetake = displayRetake(lastVersFile, False)
			
			except:
				lastVers = '00'; lastRetake = '00'
		else:
			lastVers = '00'; lastRetake = '00'	# No version
	
	
	clearVersMenu()
	if versionsSaved:	# Add new list
		for x in versionsSaved:
			try:
				mc.menuItem('vers'+x, l=x, p='optVers')
			except:
				pass
	else:
		try:
			mc.menuItem('vers0', l='00', p='optVers')
		except:	pass
	
	# Set last version and it's retake as default
	mc.optionMenu('optVers', e=True, v=lastVers)
	mc.text('txtRtk', e=True, l=lastRetake)


def doPlayblast(fldr, movieName):
	'''Take playblast and save movie ONLY IF the option is checked'''
	
	plyBlst = mc.checkBox('chkPly', q=True, v=True)
	if plyBlst:
		addRtk = mc.checkBox('chkRtk', q=True, v=True)
		nextVers, nextRtkVers = Utils.getNextVersionAndRtk(fldr, addRtk)
		return util.takePlayblast( fldr, movieName, movieName.replace('_v00.', '_v%s_rtk%s.' % (nextVers, nextRtkVers)) )
	else:
		return


def importAssets(assets, typ, loadNoRef=False):
	'''Add refereces to assets, to create shot'''
	
	fldr = '%s/' % util.path
	if typ == 'char':
		fldr += util.charPath
		parent = 'CHARACTERS'
	elif typ == 'prop':
		fldr += util.propPath
		parent = 'PROPS'
	elif typ == 'sets':
		fldr += util.bgPath
		parent = 'SETS'
	else:
		return
	
	if not mc.objExists(parent):
		mc.group(em=True, n=parent)
	
	rslt = ''
	if assets:
		for asst in assets:
			if asst:	# Will be '' even if no asset in excel column!
				try:
					namesplit = asst.split("_")
					namesplit.pop(0)
					namespace = "_".join(namesplit)
					assetPath = '%s/%s/%s_pb000.ma' % (fldr, asst, asst)
					if os.path.exists(assetPath):
						
						if loadNoRef:
							fileret = mc.file(assetPath, r=True, type= 'mayaAscii', ns=namespace, lrd='none')
						else:
							fileret = mc.file(assetPath, r=True, type= 'mayaAscii', ns=namespace)
						refnode = mc.referenceQuery(fileret, rfn=True)
						nodes = mc.referenceQuery(refnode, n=True)
						mc.parent(nodes[0], parent)
					
					else:
						rslt += '\n'+assetPath
				except:
					pass
			else:
				pass
	return rslt


def filenamesMatch(episod=None, shot=None):
	
	nameOfOpenedScene = mc.file(q=True, sn=True, shn=True)
	if not nameOfOpenedScene:
		return True
	
	if not episod:
		episod = mc.optionMenu('optEpi', q=True, v=True).zfill(3)
	if not shot:
		if not mc.optionMenu('optShot', q=True, v=True):
			mc.confirmDialog(t='Error', m='No shot selected!', b='SORRY')
			return
		shot = mc.optionMenu('optShot', q=True, v=True).zfill(3)
	
	nameFromUI = '%s_%s%ssh%s_%s_' % (util.projShort, util.epOrSeq, episod, shot, util.deptDic['short'])
	
	if re.search(nameFromUI, nameOfOpenedScene):
		return True
	else:
		return False


def openPlayblast():
	
	episod = str(mc.optionMenu('optEpi', q=True, v=True)).zfill(3)
	if not mc.optionMenu('optShot', q=True, v=True):
		mc.confirmDialog(t='Error', m='No shot selected!', b='SORRY')
		return
	
	tmp = mc.optionMenu('optShot', q=True, v=True)
	shot = tmp.zfill(3 + (len(tmp) == 4))
	playblastPath = util.getPlayblastPath(episod, shot, util.deptDic['name'])
	
	if os.path.exists(playblastPath):
		os.startfile(playblastPath)
	else:
		mc.confirmDialog(t='Warning', m='No playblast: %s' % playblastPath.replace('/', '\\'), b='OK')


def saveToLocal(showWarning=True):
	
	episod, shot = getEpiAndShotFromUI()
	if not shot:	return
	
	if showWarning:
		warnMsg = 'SceneName from window doesnt match with opened scene\'s name.\nSceneName will be taken from window by default.\nDo you want to continue?'
		if not filenamesMatch(episod, shot):
			rslt = mc.confirmDialog(t='Warning', m=warnMsg, b=['Continue', 'Cancel'], db='Continue', cb='Cancel', ds='Cancel')
			if rslt == 'Cancel':
				return
	
	expr = '^%s_%s%ssh%s_%s_.*[.]ma' % (util.projShort, util.epOrSeq, episod, shot, util.deptDic['short'])
	dfltName = '%sv00.ma' % expr[1:-7]
	pathToSave = mc.fileDialog(m=1, dm='*.ma', dfn=dfltName)
	
	if pathToSave:
		filename = pathToSave.split('/')[-1]
		if re.search(expr, filename):	# Check if filename matches the required format
			util.correctFrames(episod, shot)
			
			#joj - March 9
			Utils.switchToProxy()
			
			mc.file(rn=pathToSave)
			mc.file(s=True, typ='mayaAscii')
			mc.confirmDialog(t='Success', m='Saved as:\n%s' % pathToSave, b='THANX')
		else:
			mc.confirmDialog(t='Error', m='SceneName format is incorrect', b='SORRY')
			saveToLocal(False)


def saveScene(flag):
	'''Save the opened scene as specified episode and shot, in workspace'''
	
	episod = str(mc.optionMenu('optEpi', q=True, v=True)).zfill(3)
	if not mc.optionMenu('optShot', q=True, v=True):
		mc.confirmDialog(t='Error', m='No shot selected!', b='SORRY')
		return
	
	tmp = mc.optionMenu('optShot', q=True, v=True)
	shot = tmp.zfill(3 + (len(tmp) == 4))
	
	shotChange = False
	warnMsg = 'SceneName from window doesnt match with opened scene\'s name.\nSceneName will be taken from window by default.\nDo you want to continue?'
	if flag and (not filenamesMatch(episod, shot)):
		shotChange = True
		rslt = mc.confirmDialog(t='Warning', m=warnMsg, b=['Continue', 'Cancel'], db='Continue', cb='Cancel', ds='Cancel')
		if rslt == 'Cancel':
			return
	
	rslt, shotFldr, sceneName = util.checkShotExist(episod, shot, True)
	if rslt:
		rslt = mc.confirmDialog(t='Warning', m='%s\\%s already exists. Do you really want to replace?' % (shotFldr.replace('/', '\\'), sceneName), \
						b=['Replace', 'Cancel'])
		if rslt == 'Cancel':
			return
	
	noOfFms = 100		# Default value for No of Frames	-- ???
	
	rslt, path = util.createFolders(episod, shot, True)	# create episod/shot/versions folders
	if rslt:
		mc.confirmDialog(t='Error', m='No permission to Save:\n%s' % path.replace('/', '\\'), b='SORRY')
		return
	
	copyThis = None		# This variable is useful ONLY when copy from scenes/staging to wrkspc/animtn
	hasBrkdnList = False
	
	if flag == 0:	# Create shot from scratch (in staging), OR by copying from scenes..
		#Suneeth FEB07
		cancel = mel.eval('saveChanges("file -f -new")')
		if not cancel:
			return
		#Suneeth FEB07
		if util.deptDic['name'] == 'staging':
			
			mc.file(new=True, f=True)	# Open blank scene
			
			chars, props, bg, noOfFms2 = util.getShotDetailsFromSheet(episod, shot)
			if (chars or props or bg or noOfFms2):		# import assets as per Breakdown list
				
				hasBrkdnList = True
				rslt = ''
				frameErr = False
				loadNoRef = mc.checkBox('chkRef', q=True, v=True)
				
				if chars:
					rslt = importAssets(chars, 'char', loadNoRef)
				if props:
					rslt1 = importAssets(props, 'prop', loadNoRef)
					if rslt1:
						rslt += rslt1
				if bg:
					rslt1 = importAssets(bg, 'sets', loadNoRef)
					if rslt1:
						rslt += rslt1
				if noOfFms2:
					noOfFms = noOfFms2
				else:
					frameErr = True

				if rslt or frameErr:
					errMsg = ''
					if frameErr:
						errMsg += 'Frame count is missing in Breakdown list.\n'
					if rslt:
						errMsg += 'Some shots in Breakdown list are missing:%s' % rslt
					mc.confirmDialog(t='Error', m=errMsg, b='OK')
			
			
			# Create camera groups and import audio..
			endFrame = 100 + int(noOfFms)
			camType=0
			if util.camera == 'stereo':
				camType=1
			util.doCameraAndRenderSettings(endFrame, sceneName,camType)
			util.importAudio(sceneName, False)
		
		
		else:	# Copy shot from scenes/[staging/animation/shotfinal] ---> workspace/[animation/shotfinal/lighting]
			
			if util.deptDic['name'] == 'animation':
				copyFrom = util.stagFinal
				sceneToCopy = sceneName.replace('_an_', '_st_')
			elif util.deptDic['name'] == 'shotfinal':
				copyFrom = util.animFinal
				sceneToCopy = sceneName.replace('_sf_', '_an_')
			elif util.deptDic['name'] == 'lighting':
				copyFrom = util.shotfinalFinal
				sceneToCopy = sceneName.replace('_li_', '_sf_')
			
			scenesPath = '%s/%s/%s%s/sh%s' % (util.path, copyFrom, util.epOrSeq, episod, shot)
			shotPath = '%s/%s' % (scenesPath, sceneToCopy)
			
			if mc.file(shotPath, q=True, ex=True):
				copyThis = shotPath
				wkspcFldr = '%s/%s/%s%s/sh%s' % (util.path, util.deptDic['wkspcFldr'], util.epOrSeq, episod, shot)
				path = ('%s/%s' % (wkspcFldr, sceneName), wkspcFldr)
			else:
				mc.confirmDialog(t='Error', m='No such shot:\n%s' % shotPath.replace('/', '\\'), b='SORRY')
				return
	
	
	elif flag == 1:
		
		if shotChange:	# Correct No of frames and audio if shot is created by saving an existing one..
			
			noOfFms = util.getShotDetailsFromSheet(episod, shot, True)
			if noOfFms and (noOfFms != 'None'):
				endFrame = 100 + int(noOfFms)	# First 100 frames are for simulation
				mc.playbackOptions(min=101, max=endFrame, ast=101, aet=endFrame)
		
		util.cleanupShot(sceneName, False)	# Cleanup before Save
		
		# Save playBlast (optional)
		if doPlayblast(shotFldr, sceneName.replace('.ma', '.avi')):
			return		# Playblast error!
	
	
	#joj - March 9
	Utils.switchToProxy()
	
	# SAVE...
	addRtk = mc.checkBox('chkRtk', q=True, v=True)
	rslt = Utils.saveShot(path[1], sceneName, copyThis, False, addRtk)
	shotPath = path[0]
	
	if rslt == 1:
		Utils.deleteInitialVersions(path[1], 'ma', 10)
		displayLastVersion()	# Update last version in UI
		mc.confirmDialog(t='Success', m='Saved shot:\n%s' % shotPath.replace('/', '\\'), b='OK')
		
		if flag == 0:	# 'Create shot' option ==> Show Asset Importer OR Reference Editor
			loadNoRef = mc.checkBox('chkRef', q=True, v=True)
			
			if util.deptDic['name'] == 'staging':
				if not hasBrkdnList:	# Show Asset Importer
					createReference.createref()
				elif loadNoRef:		# Show Reference Editor
					mel.eval('tearOffPanel "Reference Editor" referenceEditor true;')
			
			else:	# Open the copied shot..
				if loadNoRef:
					mc.file(shotPath, o=True, lrd='none', f=True)
					mel.eval('tearOffPanel "Reference Editor" referenceEditor true;')
				else:
					mc.file(shotPath, o=True, f=True)
	
	elif rslt == 0:
		return		# Cancelled
	else:
		mc.confirmDialog(t='Error', m='No permission to Save:\n%s' % shotPath.replace('/', '\\'), b='SORRY')


def copyToServer():
	'''Copy the specified shot from workspace to scenes'''
	'''Note: NO need to open the shot in Maya'''
	
	episod, shot = getEpiAndShotFromUI()
	if not shot:	return
	
	rslt, shotFldr, sceneName = util.checkShotExist(episod, shot, False)
	if rslt:
		rslt = mc.confirmDialog( t='Warning', m='%s\\%s already exists. Do you really want to replace?' % (shotFldr.replace('/', '\\'), \
								sceneName), b=['Replace', 'Cancel'] )
		if rslt == 'Cancel':
			return
	
	versionfileName = Utils.findLastVersionfileName( '%s' % shotFldr.replace('scenes', 'workspace') )
	
	rslt, path = util.createFolders(episod, shot, False)
	if rslt:
		mc.confirmDialog(t='Error', m='No permission to Save:\n%s' % path.replace('/', '\\'), b='SORRY')
		return
	
	# Copy to server i.e; from workspace to scenes..
	
	copyThis = '%s/%s' % (path[1].replace(util.deptDic['scenesFldr'], util.deptDic['wkspcFldr']), sceneName)
	
	addRtk = mc.checkBox('chkRtk', q=True, v=True)
	rslt = Utils.saveShot(path[1], sceneName, copyThis, False, addRtk, versionfileName=versionfileName)
	Utils.deleteInitialVersions(path[1], 'ma', 10)
	
	if rslt == 1:
		mc.confirmDialog(t='Success', m='Saved shot:\n%s\\%s' % (path[1].replace('/', '\\'), sceneName), b='OK')
		
		# Copy playblast
		movieName = sceneName.replace('.ma', '.avi')
		copyThis = '%s/%s' % (path[1].replace(util.deptDic['scenesFldr'], util.deptDic['wkspcFldr']), movieName)
		
		if versionfileName:	# Save new version as the same version as .ma's
			versionfileName = versionfileName.replace('.ma', '.avi')
		rslt = Utils.saveShot(path[1], movieName, copyThis, False, False, versionfileName=versionfileName)
		if rslt == 2:
			mc.confirmDialog(t='Error', m='No source file to Copy:\n%s' % copyThis.replace('/', '\\'), b='SORRY')
		else:
			Utils.deleteInitialVersions(path[1], 'avi', 3)
	
	elif rslt == 0:
		return		# Cancelled
	elif rslt == 2:
		mc.confirmDialog(t='Error', m='No source file to Copy:\n%s' % copyThis.replace('/', '\\'), b='SORRY')
	else:
		mc.confirmDialog(t='Error', m='No permission to Save:\n%s\\%s' % rslt.replace('/', '\\'), b='SORRY')


def copyToMuster():
	'''Copy the specified shot from lighting workspace to scenes in Muster'''
	'''Note: NO need to open the shot in Maya'''
	
	episod, shot = getEpiAndShotFromUI()
	if not shot:	return
	
	srcFldr = '%s/%s/%s%s/sh%s' % (util.path, util.lightFldr, util.epOrSeq, episod, shot)
	shotId = '^%s_%s[0-9]{3}sh[0-9]{3}[a-z]?_[bl|cl].*[.]ma$' % (util.projShort, util.epOrSeq)
	shotFiles = None
	try:
		shotFiles = [ x for x in os.listdir(srcFldr) if re.search(shotId, x) ]
	except:
		mc.confirmDialog(t='Error', m='No read permission:\n' + srcFldr.replace('/', '\\'), b='OK')
		return
	if not shotFiles:
		mc.confirmDialog(t='Error', m='No shots to copy from:\n' + srcFldr.replace('/', '\\'), b='OK')
		return
	
	rslt, destFldr = util.checkShotsExistInMuster(episod, shot)
	if rslt:
		rslt = mc.confirmDialog( t='Warning', m='Some shots already exists in %s. Do you really want to replace?' \
						% destFldr.replace('/', '\\'), b=['Replace', 'Cancel'] )
		if rslt == 'Cancel':
			return
	
	rslt, path = util.createFoldersInMuster(episod, shot)
	if rslt:
		mc.confirmDialog(t='Error', m='No permission to Save:\n' + path.replace('/', '\\'), b='SORRY')
		return
	
	# Copy shots to server i.e; from lighting workspace to Muster scenes..
	for fil in shotFiles:
		shutil.copyfile('%s/%s' % (srcFldr, fil), '%s/%s' % (destFldr, fil))
	
	mc.confirmDialog(t='Success', m='Copied to:\n' + destFldr.replace('/', '\\'), b='THANX')


def showSummary():
	path = os.path.dirname(Utils.__file__)
	shotSummary = '\\\\192.168.3.250\\scripts$\\Applications\\shot_summary\\shot_summaryUI.exe'
	os.startfile(shotSummary)


def checkPermission():
	try:
		usr = os.environ['USERNAME']
		return True  if (usr in util.deptDic['leads']) else  False
	except:
		return False


def loadShots(shot=None, showErr=False):
	'''Load shots from the sheet for selected episod, and select shot after load if necessary.
	If no sheet, read shots from episod directory.'''
	
	episod = mc.optionMenu('optEpi', q=True, v=True).zfill(3)
	shots = util.getShotsInSheet(episod)
	#shots = None  if ((episod == '002') or (episod == '003')) else  util.getShotsInSheet(episod)
	
	# Clear shots menuItems..
	shotsOld = mc.optionMenu('optShot', q=True, ils=True)
	if shotsOld:
		for x in shotsOld:
			mc.deleteUI(x, mi=1)
	
	if not shots:		# Find shots from episod directory and load
		epiPath = '%s/%s/%s%s' % (util.path, util.deptDic['wkspcFldr'], util.epOrSeq, episod)
		expr = '^sh[0-9]{3}[a-z]?'
		if os.path.exists(epiPath):
			shots = [ x[2:] for x in sorted(os.listdir(epiPath)) if re.search(expr, x) ]
	
	if shots:		# Add new list
		for x in sorted(shots):
			try:
				mc.menuItem('shot'+x, l=x, p='optShot')
			except:
				pass
	if shot:
		try:
			mc.optionMenu('optShot', e=True, v=shot)
		except:
			pass
	
	displayLastVersion(showErr=showErr)


def doDeptChanges():
	
	dept = mc.optionMenu('optDept', q=True, v=True)
	
	util.setDeptVars( dept )
	
	if dept == 'ANIMATION':
		mc.text('txtDept', e=True, h=20, l=dept, bgc=(1,1,0))
		mc.button('btnCreate', e=True, l='COPY FROM STAGING SCENES')
		mc.text('lblRtk', e=True, vis=True)
		mc.text('txtRtk', e=True, vis=True)
		mc.checkBox('chkRtk', e=True, vis=True)
		mc.checkBox('chkPly', e=True, v=True, en=True)
	
	elif dept == 'SHOTFINAL':
		mc.text('txtDept', e=True, h=20, l=dept, bgc=(1,0,1))
		mc.button('btnCreate', e=True, l='COPY FROM ANIMATION SCENES')
		mc.text('lblRtk', e=True, vis=False)
		mc.text('txtRtk', e=True, vis=False)
		mc.checkBox('chkRtk', e=True, vis=False)
		mc.checkBox('chkPly', e=True, v=True, en=True)
	
	elif dept == 'LIGHTING':
		mc.text('txtDept', e=True, h=20, l=dept, bgc=(1,1,1))
		mc.button('btnCreate', e=True, l='COPY FROM SHOTFINAL SCENES')
		mc.text('lblRtk', e=True, vis=False)
		mc.text('txtRtk', e=True, vis=False)
		mc.checkBox('chkRtk', e=True, vis=False)
		mc.checkBox('chkPly', e=True, v=False, en=False)
	
	else:
		mc.text('txtDept', e=True, h=20, l=dept, bgc=(0,1,1))
		mc.button('btnCreate', e=True, l='CREATE IN STAGING WORKSPACE')
		mc.text('lblRtk', e=True, vis=True)
		mc.text('txtRtk', e=True, vis=True)
		mc.checkBox('chkRtk', e=True, vis=True)
		mc.checkBox('chkPly', e=True, v=True, en=True)
	
	mc.button('btnOpen', e=True, l='OPEN FROM %s WORKSPACE' % dept)
	mc.button('btnWrkspc', e=True, l='SAVE TO %s WORKSPACE' % dept)
	mc.button('btnSmry', e=True, en=checkPermission())
	displayLastVersion(dept)
	
	if dept == 'LIGHTING':
		mc.button('btnSvr', e=True, l='COPY TO MUSTER', c=lambda event:copyToMuster())
		mc.button('btnSvr', e=True, en=True)
		mc.window('sceneWin', e=True, h=(499 + checkPermission()*39))
	else:
		mc.button('btnSvr', e=True, l='COPY TO %s SCENES' % dept, c=lambda event:copyToServer())
		mc.button('btnSvr', e=True, en=checkPermission())
		mc.window('sceneWin', e=True, h=(459 + checkPermission()*39*2))



def ShotManager():
	
	def setNumOfFrames():
		if mc.playbackOptions(max=True, q=True) > 100:
			return (mc.playbackOptions(max=True, q=True) - 100)
		else:
			return mc.playbackOptions(max=True, q=True)
	
	
	global util
	util = Utils.utils()
	util.setDeptVars()
	
	if mc.window('sceneWin', ex=True):	mc.deleteUI('sceneWin', wnd=True)
	if mc.windowPref('sceneWin', ex=True):	mc.windowPref('sceneWin', r=True)
	
	mc.window('sceneWin', t='Shot Manager: ' + mc.menu('projMenu', q=True, l=True).upper())
	mc.columnLayout('lytMain', cat=('left', 15))
	mc.separator(h=5, hr=1, st='none')
	
	mc.rowColumnLayout(nc=1, cw=[(1,230)])
	mc.text('txtDept', l='STAGING', al='center', fn='boldLabelFont', bgc=(0,1,1), h=20)
	mc.setParent('..')
	mc.separator(h=10, hr=1, st='none')
	
	mc.rowColumnLayout(nc=2, cw=[(1,130),(2,100)], cs=[(1,5)])
	mc.text(l='Open from / Save in :')
	mc.optionMenu('optDept')
	mc.menuItem(l='STAGING')
	mc.menuItem(l='ANIMATION')
	mc.menuItem(l='SHOTFINAL')
	mc.menuItem(l='LIGHTING')
	mc.setParent('..')
	mc.separator(h=5, hr=1, st='none')
	
	mc.rowColumnLayout(nc=1, cw=[(1,230)])
	mc.frameLayout( label='', labelAlign='bottom', borderStyle='etchedOut' )
	mc.rowColumnLayout(cw=[(1,260)])
	
	mc.rowColumnLayout(nc=4, cw=[(1,55),(2,50),(3,35),(4,50)], cs=[(1,10),(3,20)])
	mc.text(l='Episode :'  if (util.epOrSeq == 'ep') else  'Sequence:')
	mc.optionMenu('optEpi')
	[ mc.menuItem(l=str(x).zfill(3)) for x in xrange(1, int(util.episodes)+1) ]
	mc.text('txtLbl', l='Shot :')
	mc.optionMenu('optShot')
	mc.separator(h=5, hr=1, st='none')
	
	mc.setParent('lytMain')
	
	mc.separator(h=10, hr=1, st='none')
	mc.rowColumnLayout(nc=2, cw=[(1,200),(2,50)], cs=[(1,15)])
	mc.checkBox('chkRef', l='Load NO references on Create/Open', v=True)
	mc.setParent('..') 
	mc.separator(h=15, hr=1, st='none')
	
	mc.rowColumnLayout(nc=1, cw=[(1,230)])
	mc.button('btnCreate', l='CREATE IN STAGING WORKSPACE', c=lambda event:saveScene(0), h=30)
	mc.setParent('..')
	mc.separator(h=5, hr=1, st='none')
	
	mc.rowColumnLayout(nc=1, cw=[(1,230)])
	mc.button('btnOpen', l='OPEN FROM STAGING WORKSPACE', c=lambda event:openScene(0), h=30)
	mc.setParent('..')
	mc.separator(h=5, hr=1, st='none')
	
	mc.rowColumnLayout(nc=5, cw=[(1,25),(2,45),(3,25),(4,30),(5,105)])
	mc.text(l=' Ver:')
	mc.optionMenu('optVers')
	mc.text('lblRtk', l=' Rtk:')
	mc.text('txtRtk', l='0')
	mc.button(l='OPEN VERSION', c=lambda event:openScene(1), h=20)
	mc.setParent('..')
	mc.separator(h=5, hr=1, st='none')
	
	mc.rowColumnLayout(nc=1, cw=[(1,230)])
	mc.button(l='OPEN PLAYBLAST FROM WORKSPACE', c=lambda event:openPlayblast(), h=30)
	mc.setParent('..')
	mc.separator(h=10, hr=1, st='none')
	
	mc.rowColumnLayout(nc=1, cw=[(1,230)])
	mc.button(l='SAVE TO LOCAL AS...', c=lambda event:saveToLocal(), h=30)
	mc.setParent('..')
	mc.separator(h=10, hr=1, st='none')
	
	mc.rowColumnLayout(nc=1, cw=[(1,230)])
	mc.frameLayout( label='', labelAlign='bottom', borderStyle='etchedOut' )
	mc.rowColumnLayout(cw=[(1,270)])
	
	mc.rowColumnLayout(nc=2, cw=[(1,160),(2,100)], cs=[(1,50)])
	mc.checkBox('chkPly', l='Save with PLAYBLAST', v=True)
	mc.setParent('..')
	mc.separator(h=5, hr=1, st='none')
	
	mc.rowColumnLayout(nc=2, cw=[(1,160),(2,100)], cs=[(1,50)])
	mc.checkBox('chkRtk', l='Increment RETAKE', v=False)
	mc.setParent('..')
	mc.separator(h=5, hr=1, st='none')
	
	mc.rowColumnLayout(nc=1, cs=[(1,5)], cw=[(1,215)])
	mc.button('btnWrkspc', l='SAVE TO STAGING WORKSPACE', c=lambda event:saveScene(1), h=30, ann='Check Episode and Shot above before save')
	mc.separator(h=5, hr=1, st='none')
	
	mc.setParent('lytMain')
	
	mc.separator(h=10, hr=1, st='none')
	mc.rowColumnLayout(nc=1, cw=[(1,230)])
	mc.button('btnSvr', l='COPY TO STAGING SCENES', c=lambda event:copyToServer(), h=30, en=checkPermission(), \
				ann='No need to open scene. Just enter Episode and Shot above and Click this')
	mc.setParent('..')
	
	mc.separator(h=5, hr=1, st='none')
	mc.rowColumnLayout(nc=1, cw=[(1,230)])
	mc.button('btnSmry', l='SHOT SUMMARY', c=lambda event:showSummary(), h=30, en=checkPermission(), \
				ann='Showing Shots summary window')
	mc.setParent('..')
	
	mc.separator(h=10, hr=1, st='none')
	
	fullPath = mc.file(q=True, sn=True, shn=True)
	dept = None
	if fullPath:
		if '_an_' in fullPath:
			dept = 'ANIMATION'
			mc.text('txtDept', e=True, h=20, l=dept, bgc=(1,1,0))
			mc.button('btnCreate', e=True, l='COPY FROM STAGING SCENES')
			mc.text('lblRtk', e=True, vis=True)
			mc.text('txtRtk', e=True, vis=True)
			mc.checkBox('chkRtk', e=True, vis=True)
			mc.checkBox('chkPly', e=True, v=True, en=True)
		
		elif '_sf_' in fullPath:
			dept = 'SHOTFINAL'
			mc.text('txtDept', e=True, h=20, l=dept, bgc=(1,0,1))
			mc.button('btnCreate', e=True, l='COPY FROM ANIMATION SCENES')
			mc.text('lblRtk', e=True, vis=False)
			mc.text('txtRtk', e=True, vis=False)
			mc.checkBox('chkRtk', e=True, vis=False)
			mc.checkBox('chkPly', e=True, v=True, en=True)
		
		elif '_li_' in fullPath:
			dept = 'LIGHTING'
			mc.text('txtDept', e=True, h=20, l=dept, bgc=(1,1,1))
			mc.button('btnCreate', e=True, l='COPY FROM SHOTFINAL SCENES')
			mc.text('lblRtk', e=True, vis=False)
			mc.text('txtRtk', e=True, vis=False)
			mc.checkBox('chkRtk', e=True, vis=False)
			mc.checkBox('chkPly', e=True, v=False, en=False)
		
		else:	dept = 'STAGING'
		
		mc.optionMenu('optDept', e=True, v=dept)
		mc.button('btnOpen', e=True, l='OPEN FROM %s WORKSPACE' % dept)
		mc.button('btnWrkspc', e=True, l='SAVE TO %s WORKSPACE' % dept)
		if dept == 'LIGHTING':
			mc.button('btnSvr', e=True, l='COPY TO MUSTER', c=lambda event:copyToMuster())
		else:
			mc.button('btnSvr', e=True, l='COPY TO %s SCENES' % dept, c=lambda event:copyToServer())
	
	util.setDeptVars( mc.optionMenu('optDept', q=True, v=True) )
	
	mc.optionMenu('optEpi', e=True, cc=lambda event:loadShots(showErr=False))
	mc.optionMenu('optShot', e=True, cc=lambda event:displayLastVersion())
	mc.optionMenu('optDept', e=True, cc=lambda event:doDeptChanges())
	mc.optionMenu('optVers', e=True, cc=lambda event:displayRetake())
	
	episod, shot = util.getEpiAndShot()
	if episod and shot:
		mc.optionMenu('optEpi', e=True, v=episod)
		loadShots(shot)
	else:
		loadShots()
	
	if dept and (dept == 'LIGHTING'):
		mc.window('sceneWin', e=True, wh=(267, 499 + checkPermission()*39))
	else:
		mc.window('sceneWin', e=True, wh=(267, 459 + checkPermission()*39*2))
	mc.showWindow('sceneWin')
