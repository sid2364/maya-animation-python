#SHOT MANAGER SID
import maya.cmds as cmds
import os, os.path
import string, collections
from functools import partial
from re import match, sub

global deptList, filepathnew

windowID = 'Shot_Manager_Sid'
rootpath = 'D:\Work.Area\Siddharth-ShotManager' #as root for testing

class shotManager_SID:
	def __init__(self):
		
		if cmds.window( windowID, exists=True ): cmds.deleteUI( windowID )
		
		mainWindow = cmds.window( windowID, title='Shot Manager -- Sid',minimizeButton=False , \
					maximizeButton=False, sizeable=False, resizeToFitChildren=True)
		####-1 for the dept combo (and change layout to more cols)

		def runPutDeptComponentsAndInvisible(*args): #needed to run both the functions with changeCommand
			self.putDeptComponents()
			self.makeSaveInvisible()
			self.comboVersionLoad()
		#
		#deptForm = cmds.formLayout( parent = mainWindow )
		
		#cmds.dockControl( area='right', content=mainWindow, allowedArea=['left'] )
		#
		self.filepathnew = None
		cmds.frameLayout(borderStyle='out', lv=0 , fn='boldLabelFont', mh=10, mw=10)
		
		cmds.rowColumnLayout( numberOfColumns=3, rowSpacing=(10, 10), columnWidth=[(1,100)], cal=[50, "center"])
				
		cmds.separator( w=5, style="none")
		deptList = cmds.optionMenu("deptList", w=150, h=20 , changeCommand=runPutDeptComponentsAndInvisible)
		cmds.menuItem(label = "Character Modeling", parent="deptList")
		cmds.menuItem(label = "Background Modeling", parent="deptList")
		#cmds.separator( h=10, style='none')
		####
		cmds.separator( w=1, style='none'); cmds.separator( w=1, style='none')
		cmds.checkBox("chkLoadRef", label='Load References', align='right' )
		#cmds.separator( h=5, style='none') #dummy
		cmds.setParent( '..' )
		cmds.setParent( '..' )
		####
		cmds.frameLayout(borderStyle='etchedIn', l='Model & Scene', mh=10, mw=10)
		cmds.rowColumnLayout( numberOfColumns=5, rowSpacing=(10, 10), columnWidth=[(1,10),(2,150), (3,10), (4, 150), (5, 10)])
		
		def runchangeCharBgComboAndInvisible(*args):
			self.changeCharBgCombo()
			self.makeSaveInvisible()
			self.comboVersionLoad()

		def runchangeCharBgComboAndInvisibleFromCharBg(*args):
			self.makeSaveInvisible()
			self.comboVersionLoad()
		####-2
		map(lambda x: cmds.separator( w=x, style='none') , [5]*5)
		
		cmds.separator( w=5, style='none' )
		charBgList = cmds.optionMenu("charBgList", w=150, changeCommand=runchangeCharBgComboAndInvisibleFromCharBg)
		cmds.separator( w=5, style='none' )
		sceneList = cmds.optionMenu("sceneList", changeCommand=runchangeCharBgComboAndInvisible, w=150)
		comboSceneLoad('char') #for entering values into the scene combo box
		cmds.separator( w=5, style='none' )
		map(lambda x: cmds.separator( w=x, style='none') , [3]*3)
		cmds.setParent( '..' )
		cmds.setParent( '..' )		
		changeCharBgCombo() # enter values into the model combo box
		####-3
		
		def runLoadAndVisible(*args):
			self.loadFile()
			self.makeSaveVisible()
		
		def runLoadLatestAndVisible(*args):
			self.loadLatestFile()
			self.makeSaveVisible()
		
		cmds.frameLayout(borderStyle='etchedIn', l='Versions Of The Model' , fn='boldLabelFont', mh=10, mw=10)
		cmds.rowColumnLayout(numberOfColumns=5, rowSpacing=(10, 10), columnWidth=[(1,10),(2,150), (3,10), (4, 150), (5, 10)])
		
		cmds.separator( w=5, style='none' )
		cmds.optionMenu("versionList", w=150)
		cmds.separator( w=5, style='none' )
		cmds.button( label='Load Version',  w=150, command=runLoadAndVisible) #for load file btn!
		map(lambda x: cmds.separator( w=x, style='none'), [5]*4)
		cmds.button( label='Load Latest Version', command=runLoadLatestAndVisible) #dont use functools.partial
		self.comboVersionLoad() #for version
		cmds.setParent( '..' ); cmds.setParent( '..' )
		####
		
		####-4
		cmds.frameLayout(borderStyle='in', l='Save' , fn='boldLabelFont', mh=10, mw=10)
		cmds.rowColumnLayout(numberOfColumns=5, rowSpacing=(10, 10), columnWidth=[(1,10),(2,150), (3,10), (4, 150), (5, 10)])
		
		def saveToNWFunction(*args):
			self.saveToNW()
		def saveToWorkspaceFunction(*args):
			self.saveToWorkspace()
		
		cmds.separator( h=5, style='none' ) 
		cmds.button("btnSaveNetwork", label='Save To N/W', command=saveToNWFunction) #save to default space
		cmds.separator( h=5, style='none' )
		cmds.button("btnSaveWs", label='Save To Workspace', command=saveToWorkspaceFunction	) #ask for dialog
		cmds.separator( h=5, style='none' ) 	
		####
		map(lambda x: cmds.separator( h=x, style='none') , [5]*4)
		
		cmds.setParent( '..' ); cmds.setParent( '..' )
		
		
		def cancelCallback( *args ):
			if cmds.window( windowID, exists=True ):
				cmds.deleteUI( windowID )
		#map(lambda x: cmds.separator( w=x, style='none') , [5]*4) # will replicate the statement 4 times with h=5!! 
		cmds.button( label='X', command=cancelCallback , h=17)
		#map(lambda x: cmds.separator( w=x, style='none') , [5]*5)
		
		self.makeSaveInvisible()
		cmds.showWindow()

	def loadLatestFile(self, *args):
		self.versions = sorted(self.versions)
		theversionToOpen = self.versions[len(self.versions)-1]
		subs = cmds.optionMenu( "charBgList", query = True, value = True)
		temp=subs[-6:-3]
		subs = self.nameOfCurr.replace(temp, theversionToOpen)
		chkLoadRef = cmds.checkBox("chkLoadRef", q = True, v = True)
		loadRef = "all" if chkLoadRef else "none"
		cmds.file(subs, f=1, o=1, lrd = loadRef)

	def comboVersionLoad(self, *pargs):
		self.nameOfCurr = self.getNameOfFile()
		self.filepathnew = os.path.dirname(self.nameOfCurr)
		#print filepath, nameOfCurr
		this = []
		menuItems = cmds.optionMenu('versionList', q = True, ill = True)
		if menuItems: cmds.deleteUI(menuItems) #to delete existing items if called twice
		matchObj = match( r'.*\\(.+)\..+', self.nameOfCurr, re.M|re.I)
		if matchObj:
			substringForName=matchObj.group(1)[:-5]
		for f in os.listdir(self.filepathnew):
			if substringForName in f:
				addThis = f[-6:-3]
				cmds.menuItem(label = addThis, p = 'versionList')
				this.append(addThis)
		self.versions = this	
				
	def getData(self, *pArgs): #to get data from combo boxes
		deptCmb = cmds.optionMenu( "deptList", query = True, value = True)
		charBgCmb = cmds.optionMenu( "charBgList", query = True, value = True)
		sceneCmb = cmds.optionMenu( "sceneList", query = True, value = True)
		chkLoadRef = cmds.checkBox("chkLoadRef", q = True, v = True)
		loadRef = "all" if chkLoadRef else "none"
		if not (deptCmb and charBgCmb and  sceneCmb): cmds.warning("Please select valid options!")
		else: return (deptCmb, charBgCmb, sceneCmb, loadRef)#return as data tuple
	
	def loadFile(self, *pArgs):
		self.makeSaveVisible()
		(deptCmb, charBgCmb, sceneCmb, loadRef) = self.getData() #get data from ui
		if deptCmb=='Character Modeling': foldername='char'
		else: foldername='bg'
		pathToFile=os.path.join(rootpath, foldername, 'scene'+sceneCmb, charBgCmb)
		pathToFile = pathToFile.replace(pathToFile[-6:-3], cmds.optionMenu("versionList", query=1, v=1))
		chkLoadRef = cmds.checkBox("chkLoadRef", q = True, v = True)
		loadRef = "all" if chkLoadRef else "none"
		cmds.file(pathToFile, f=1, o=1, lrd = loadRef)
		##eg. D:\Work.Area\Siddharth-ShotManager\bg\scene007\sidbg.ma
		##eg. D:\Work.Area\Siddharth-ShotManager\char\scene001\sidchar.ma
		
		
	def getNameOfFile(self, *pargs):
		deptCmb = cmds.optionMenu("deptList", query=True, value=True)
		if deptCmb=='Character Modeling': foldername='char'
		else: foldername='bg'
		charBg = cmds.optionMenu( "charBgList", query = True, value = True)
		scenenum = cmds.optionMenu( "sceneList", query = True, value = True)
		filename=os.path.join(rootpath, foldername, 'scene'+scenenum, charBg)
		return filename
		
	def comboChBgLoad(self, deptCmb, sceneNum):
		self.makeSaveInvisible()
		#to load the combo box in the main UI fucntion for Characters and Bgs according to the main Char/Backgrounds 
		menuItems = cmds.optionMenu('charBgList', q = True, ill = True)
		if menuItems: cmds.deleteUI(menuItems) #to delete existing items if called twice
		if deptCmb=='Character Modeling': deptChoice='char'
		else: deptChoice='bg'
		for root, dir , files in os.walk(os.path.join(rootpath, deptChoice, 'scene'+sceneNum)):
			for f in files:
				fullpath = os.path.join(root, f)
				if os.path.splitext(fullpath)[1] == '.ma': cmds.menuItem(label = f, p = 'charBgList')
		
	def comboSceneLoad(self, *pargs):
		self.makeSaveInvisible()
		temp={}
		deptCmb = cmds.optionMenu( "deptList", query = True, value = True)
		if deptCmb=='Character Modeling': deptChoice='char'
		else: deptChoice='bg'
		menuItems = cmds.optionMenu('sceneList', q = True, ill = True)
		if menuItems: cmds.deleteUI(menuItems) #to delete existing items if called twice
		
		for root, dir , files in os.walk(os.path.join(rootpath, deptChoice)):
			if 'scene' in root:
				num=root[-3:]
				temp[num]='1'
		for v in temp:cmds.menuItem(label = v, p = 'sceneList')
		self.changeCharBgCombo(deptChoice)
	
	
	def changeCharBgCombo(self, *pArgs):
		self.makeSaveInvisible()
		deptCmb = cmds.optionMenu( "deptList", query = True, value = True)
		sceneCmb = cmds.optionMenu( "sceneList", query = True, value = True)
		self.comboChBgLoad(deptCmb, sceneCmb)
		
	#def comboVersionLoad(deptChoice):
	def saveToNW(self, *pArgs):
		self.nameOfCurr = self.getNameOfFile()
		self.filepathnew = os.path.dirname(self.nameOfCurr)
		#print filepath, nameOfCurr
		versionslocal = []
		matchObj = re.match( r'.*\\(.+)\..+', self.nameOfCurr, re.M|re.I)
		if matchObj:
			substringForName=matchObj.group(1)[:-5]
		for f in os.listdir(self.filepathnew):
			if substringForName in f:
				addThis = f[-6:-3]
				versionslocal.append(addThis)
		versionslocal = sorted(versionslocal)
		theversionToOpen = versionslocal[len(versionslocal)-1]
		temp = str((int(theversionToOpen)+1)).zfill(3)
		subs = self.nameOfCurr.replace(self.nameOfCurr[-6:-3], temp)
		print subs
		print temp
		print theversionToOpen
		cmds.file(rename = subs)
		cmds.file(save = True)
		de=cmds.optionMenu( "deptList", query = True, value = True)
		sc=cmds.optionMenu( "sceneList", query = True, value = True)
		self.comboChBgLoad(de, sc)
		#print "Saved to: %s" % subs
		self.makeSaveVisible()
		
		"""
		newFilePath = self.getNameOfFile()
		cmds.file(rename = newFilePath)
		cmds.file(save = True)
		print "Saved to: %s" % newFilePath
		"""
	def saveToWorkspace(self, *pArgs):
		multipleFilters = "Maya ASCII (*.ma);;Maya Binary (*.mb);;All Files (*.*)"
		filepath=cmds.fileDialog2(fileFilter=multipleFilters, dialogStyle=3)
		try:
			if filepath: #if not req
				newFilePath = filepath[0]
		        cmds.file(rename = newFilePath)
		        cmds.file(save = True)
		        print "Saved to: %s" % newFilePath
		        print filepath[0]
		except:
			cmds.warning("You did not select a file.")	
	
	def putDeptComponents(self, *pArgs):
		self.makeSaveInvisible()
		deptCmb = cmds.optionMenu("deptList", query = True, value = True)
		self.comboSceneLoad()
	
	
	def makeSaveInvisible(self, *pArgs):
		cmds.button("btnSaveNetwork", e=1, en = 0)
		cmds.button("btnSaveWs", e=1, en = 0)
	
	def makeSaveVisible(self):
		cmds.button("btnSaveNetwork", e=1, en = 1)
		cmds.button("btnSaveWs", e=1, en = 1)

if __name__=="__main__":
	obj = shotManager_SID()