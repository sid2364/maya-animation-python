#SHOT MANAGER SID
import maya.cmds as cmds
import os, os.path
import string, collections
from functools import partial
import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import re
import csv

global deptList, filepathnew

pluginCmdName = "shotmanager_sid"

windowID = 'Shot_Manager_Sid'
rootpath = 'D:\Work.Area\Siddharth-ShotManager' #as root for testing

class scriptedCommand(OpenMayaMPx.MPxCommand):
	def __init__(self):
		OpenMayaMPx.MPxCommand.__init__(self)
        

	def doIt(self,argList):
		print "Shot Manager Sid -- Initialising."
		obj = shotManager_SID()
		print "Ready."

def cmdCreator():
	return OpenMayaMPx.asMPxPtr( scriptedCommand() )


def initializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject)
	try:
		mplugin.registerCommand( pluginCmdName , cmdCreator )
	except:
		sys.stderr.write( "Failed to register command: %s\n" % pluginCmdName  )
		raise


def uninitializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject)
	try:
		mplugin.deregisterCommand( pluginCmdName )
	except:
		sys.stderr.write( "Failed to unregister command: %s\n" % pluginCmdName )

class shotManager_SID:
	def __init__(self):
	
		
		#these functions are needed to call functions not possible to call by changeCommand, or command
		#it is not possible to call multiple functions with cc or c (and calling through self)
		def runPutDeptComponentsAndInvisible(*args):
			self.putDeptComponents()
			self.makeSaveInvisible()
			self.makeModelSceneInvisible()
			self.comboVersionLoad()
			self.changeRequests()
				
		def runCreateAsset(*pargs):
			self.createAsset()
			self.putDeptComponents()
			self.makeSaveVisible()
			
		def runchangeCharBgComboAndInvisible(*args):
			self.changeCharBgCombo()
			self.makeSaveInvisible()
			self.comboVersionLoad()
			self.makeModelSceneVisible()

		def runchangeCharBgComboAndInvisibleFromCharBg(*args):
			self.makeSaveInvisible()
			self.comboVersionLoad()
			self.makeModelSceneVisible()		
				
		def runLoadAndVisible(*args):
			self.loadFile()
			self.makeSaveVisible()
		
		def runLoadLatestAndVisible(*args):
			self.loadLatestFile()
			self.makeSaveVisible()
		
		def runChangeVersionList(*pargs):
			self.makeModelSceneVisible()
		
		def saveToNWFunction(*args):
			self.saveToNW()
		def saveToWorkspaceFunction(*args):
			self.saveToWorkspace()
			
		def cancelCallback( *args ):
			if cmds.window( windowID, exists=True ):
				cmds.deleteUI( windowID )
	
		if cmds.window( windowID, exists=True ): cmds.deleteUI( windowID )
		mainWindow = cmds.window( windowID, title='Shot Manager -- Sid',minimizeButton=False , \
					maximizeButton=False, sizeable=False, resizeToFitChildren=True)
		
		self.filepathnew = None
		self.dictModelName = {}
		
		#first row - character or background modeling		
		cmds.frameLayout(borderStyle='out', lv=0 , fn='boldLabelFont', mh=10, mw=10)
		cmds.rowColumnLayout( numberOfColumns=3, rowSpacing=(10, 10), columnWidth=[(1,100)], cal=[50, "center"])
		cmds.separator( w=5, style="none")
		deptList = cmds.optionMenu("deptList", w=150, h=20 , changeCommand=runPutDeptComponentsAndInvisible)
		cmds.menuItem(label = "Character Modeling", parent="deptList")
		#add items to the deptList
		cmds.menuItem(label = "Background Modeling", parent="deptList")
		cmds.separator( w=1, style='none'); cmds.separator( w=1, style='none')
		chkLoadRef = cmds.checkBox("chkLoadRef", label='Load References', align='right' )
		cmds.setParent( '..' ); cmds.setParent( '..' )
		#traversing to the above level of control

		
		#second row - for newly requested assets by the production management
		cmds.frameLayout(borderStyle='etchedIn', l='New Asset', mh=10, mw=10)
		cmds.rowColumnLayout( numberOfColumns=5, rowSpacing=(10, 10), columnWidth=[(1,10),(2,150),\
						(3,10), (4, 150), (5, 10)])
		cmds.separator( w=5, style='none' )
		cmds.optionMenu('assetsList', w=150)
		cmds.separator( w=5, style='none' )
		cmds.button("btnNewFile", label='Create Requested Asset', w=150, command=runCreateAsset)
		#the function in 'command' will call the previously defined functions
		#button will create version _v000 of the asset in the required scene
		cmds.separator( w=5, style='none' )
		map(lambda x: cmds.separator( w=x, style='none') , [3]*3)
		#map and lambda will replicate the cmds.separator command array length number of times
		cmds.setParent( '..' ); cmds.setParent( '..' )		
		
		
		#third row - contains the already available assets
		#can be selected to edit/proceed with previous work
		cmds.frameLayout(borderStyle='etchedIn', l='Model & Scene', mh=10, mw=10)
		cmds.rowColumnLayout( numberOfColumns=5, rowSpacing=(10, 10), columnWidth=[(1,10),(2,150), \
						(3,10), (4, 150), (5, 10)])
		map(lambda x: cmds.separator( w=x, style='none') , [5]*5)
		#replicates the call to separator 5 times with h=5
		cmds.separator( w=5, style='none' )
		cmds.optionMenu("charBgList", w=150, changeCommand=runchangeCharBgComboAndInvisibleFromCharBg)
		cmds.separator( w=5, style='none' )
		sceneList = cmds.optionMenu("sceneList", changeCommand=runchangeCharBgComboAndInvisible, w=150)
		cmds.separator( w=5, style='none' )
		map(lambda x: cmds.separator( w=x, style='none') , [3]*3)
		cmds.setParent( '..' ); cmds.setParent( '..' )		
		
		#fourth row - every model has versions, so restoring to any point is much easier
		#the selected model's versions will be listed in the versionList for the user to choose from
		cmds.frameLayout(borderStyle='etchedIn', l='Versions Of The Model' , fn='boldLabelFont', mh=10, mw=10)
		cmds.rowColumnLayout(numberOfColumns=5, rowSpacing=(10, 10), columnWidth=[(1,10),(2,150), (3,10), (4, 150), (5, 10)])
		cmds.separator( w=5, style='none' )
		cmds.optionMenu("versionList", w=150, changeCommand=runChangeVersionList)
		cmds.separator( w=5, style='none' )
		cmds.button("btnLoadVersion", label='Load Version',  w=150, command=runLoadAndVisible)
		#for loading up the selected version
		map(lambda x: cmds.separator( w=x, style='none'), [5]*4)
		cmds.button("btnLoadLatest", label='Load Latest Version', command=runLoadLatestAndVisible)
		#btnLoadLatest will load the latest file version
		cmds.setParent( '..' ); cmds.setParent( '..' )
		

		#fifth row - for different save options
		cmds.frameLayout(borderStyle='etchedIn', l='Save' , fn='boldLabelFont', mh=10, mw=10)
		cmds.rowColumnLayout(numberOfColumns=5, rowSpacing=(10, 10), columnWidth=[(1,10),(2,150), (3,10), (4, 150), (5, 10)])
		cmds.separator( h=5, style='none' ) 
		cmds.button("btnSaveNetwork", label='Save To N/W', command=saveToNWFunction)
		#save to default space in the network - version will be incremented
		cmds.separator( h=5, style='none' )
		cmds.button("btnSaveWs", label='Save To Workspace', command=saveToWorkspaceFunction	)
		#show file dialog box and ask user to specify location for local save i.e. save to workspace
		cmds.separator( h=5, style='none' ) 	
		map(lambda x: cmds.separator( h=x, style='none') , [5]*3)
		cmds.setParent( '..' ); cmds.setParent( '..' )
		
		
		#sixth row - a simple cancel button
		cmds.button( label='X', command=cancelCallback , h=17)
		#UI init end


		csvfile = open('D:\Work.Area\Siddharth-ShotManager\data.csv', 'rb')
		#data for new requests of assets
		reader = csv.reader(csvfile, delimiter=',')
		self.list = []
		for row in reader:
			self.list.append(row)
		#add all data to assetsList
		
		#call after all UI initialisation else the objects will be unknown
		#for content initialisation in the UI combo boxes
		self.comboSceneLoad('char') #for entering values into the scene combo box
		self.changeCharBgCombo() # enter values into the model combo box
		self.comboVersionLoad() #for versionList initialisation
		self.makeSaveInvisible() #for making save buttons inactive - cannot save until you open a file
		self.makeModelSceneInvisible() #cannot load a file until you select from the list menu
		self.changeRequests() #for loading the newly requested assets
		
		cmds.showWindow()
		
	def createAsset(self):
		f = cmds.optionMenu("assetsList", q=1, value=1)
		#to create the selected asset in the required scene folder - will be mentioned in csv file
		for i in range(len(self.list)):
			if self.list[i][1]==f:
				dept=self.list[i][0]
				scenenum=self.list[i][2].zfill(3) #make sure its always 3 digits
				del self.list[i]
				break
		pathf = os.path.join(rootpath, dept, 'scene'+scenenum)
		path = os.path.join(pathf, f.replace(" ", "_")+'_v000.ma') #to create version _v000
		bool = cmds.sysFile( pathf,  makeDir=True ) #make it a directory
		cmds.file(rn=path); cmds.file(save=1) #renaming and saving have to be done seperately
		csvfile = open('D:\Work.Area\Siddharth-ShotManager\data.csv', 'wb')
		#open csv in write mode - will overwrite the file's contents
		#this is to rewrite the file to erase the already opened file
		writer = csv.writer(csvfile, delimiter=',')
		for row in self.list:
			writer.writerow(row)
		self.changeRequests() #show change in the list
		
	def changeRequests(self):
		(deptCmb, charBgCmb, sceneCmb, loadRef) = self.getData() #get data from ui
		if deptCmb=='Character Modeling': foldername='char'
		else: foldername='bg'
		#enumerate items in the assetsList
		menuItems = cmds.optionMenu("assetsList", q = True, ill = True)
		if menuItems: cmds.deleteUI(menuItems)
		for row in self.list:
			if row[0]==foldername:
				cmds.menuItem(l=row[1], p='assetsList')
		#will add the name of file to list - present at index 1
		
	def loadLatestFile(self, *args):
		#loading the latest version of the file - btnLoadLatest
		self.versions = sorted(self.versions) #sort the existing versions
		theversionToOpen = self.versions[len(self.versions)-1] #and pick the last one
		subs = cmds.optionMenu( "charBgList", query = True, value = True)
		temp=self.nameOfCurr[-6:-3] #overwrite the file name's version part
		subs = self.nameOfCurr.replace(temp, theversionToOpen) #replace it with the latest
		chkLoadRef = cmds.checkBox("chkLoadRef", q = True, v = True)
		loadRef = "all" if chkLoadRef else "none"
		cmds.file(subs, f=1, o=1, lrd = loadRef) #and open the file

	def comboVersionLoad(self, *pargs):
		#for adding items to the versionList - will get called after loading models combo box
		self.nameOfCurr = self.getNameOfFile()
		filen = self.nameOfCurr[(self.nameOfCurr.rindex('\\'))+1:] #get the file name
		#will be incomplete as extension and version are not there (for more user readability)
		curr = self.dictModelName[filen] #look up actual fullname in the dictionary
		self.nameOfCurr = self.nameOfCurr.replace(self.nameOfCurr[(self.nameOfCurr.rindex('\\'))+1:], curr)
		#replace the incomplete file name with the complete one from the dict
		self.filepathnew = os.path.dirname(self.nameOfCurr) #find the directory its present in
		this = []
		menuItems = cmds.optionMenu("versionList", q = True, ill = True)
		if menuItems: cmds.deleteUI(menuItems)
		#to delete existing items if called twice
		matchObj = re.match( r'.*\\(.+)\..+', self.nameOfCurr, re.M|re.I)
		#to get the all actual file names in the folder
		if matchObj:
			substringForName=matchObj.group(1)[:-5] #take last five characters (this includes the version)
		for f in os.listdir(self.filepathnew):
			if substringForName in f:
				addThis = f[-6:-3] #add only the version part of each file in the versionList
				cmds.menuItem(label = addThis, p = "versionList")
				this.append(addThis)
		self.versions = this	
		
	def getData(self, *pArgs):
		#to get data from combo boxes
		deptCmb = cmds.optionMenu( "deptList", query = True, value = True)
		charBgCmb = cmds.optionMenu( "charBgList", query = True, value = True)
		sceneCmb = cmds.optionMenu( "sceneList", query = True, value = True)
		chkLoadRef = cmds.checkBox("chkLoadRef", q = True, v = True)
		loadRef = "all" if chkLoadRef else "none"
		if not (deptCmb and charBgCmb and  sceneCmb): cmds.warning("Please select valid options!")
		else: return (deptCmb, charBgCmb, sceneCmb, loadRef)#return as data tuple
	
	def loadFile(self, *pArgs):
		#open requested file - selected version
		self.makeSaveVisible()
		(deptCmb, charBgCmb, sceneCmb, loadRef) = self.getData()
		if deptCmb=='Character Modeling': foldername='char'
		else: foldername='bg'
		pathToFile = self.nameOfCurr
		pathToFile = pathToFile.replace(pathToFile[-6:-3], cmds.optionMenu("versionList", query=1, v=1))
		#for requested version
		chkLoadRef = cmds.checkBox("chkLoadRef", q = True, v = True)
		loadRef = "all" if chkLoadRef else "none"
		cmds.file(pathToFile, f=1, o=1, lrd = loadRef)
		#force=True (f=1) will save and then continue to load the new file
		
		##eg. D:\Work.Area\Siddharth-ShotManager\bg\scene007\sidbg.ma
		##eg. D:\Work.Area\Siddharth-ShotManager\char\scene001\sidchar.ma
				
	def getNameOfFile(self, *pargs):
		#get the whole name of the file
		deptCmb = cmds.optionMenu("deptList", query=True, value=True)
		if deptCmb=='Character Modeling': foldername='char'
		else: foldername='bg'
		charBg = cmds.optionMenu( "charBgList", query = True, value = True)
		scenenum = cmds.optionMenu( "sceneList", query = True, value = True)
		filename=os.path.join(rootpath, foldername, 'scene'+scenenum, charBg)
		#os.path.join intelligently connects the required folders and outputs the required path
		return filename
		
	def comboChBgLoad(self, deptCmb, sceneNum):
		#for loading the models combobox
		self.makeSaveInvisible()
		self.dictModelName.clear() #reset the model names dictionary
		#to load the combo box in the main UI fucntion for Characters and Bgs according to the main Char/Backgrounds 
		menuItems = cmds.optionMenu('charBgList', q = True, ill = True)
		if menuItems: cmds.deleteUI(menuItems) #to delete existing items if called twice
		if deptCmb=='Character Modeling': deptChoice='char'
		else: deptChoice='bg'
		for root, dir , files in os.walk(os.path.join(rootpath, deptChoice, 'scene'+sceneNum)):
			#os.walk iterated the entire folder passed as arg, in this case the whole scene folder
			for f in files: #it returns a list of files, so iterate through that
				fullpath = os.path.join(root, f)
				if os.path.splitext(fullpath)[1] == '.ma' or os.path.splitext(fullpath)[1] == '.mb':
					#if its a Maya file, then display it
					self.dictModelName[f[0:(f.rindex("_v"))]]= f #last index of "_v" (from the right)
		for key in self.dictModelName:
			cmds.menuItem(label = key, p = 'charBgList') #add to UI component
		self.comboVersionLoad() #for enumerating the version, only after model's has loaded up
		
	def comboSceneLoad(self, *pargs):
		#load scene combobox
		self.makeSaveInvisible()
		temp,vals={},[]
		deptCmb = cmds.optionMenu( "deptList", query = True, value = True)
		if deptCmb=='Character Modeling': deptChoice='char'
		else: deptChoice='bg'
		menuItems = cmds.optionMenu('sceneList', q = True, ill = True)
		if menuItems: cmds.deleteUI(menuItems) #to delete existing items if called twice
		for root, dir , files in os.walk(os.path.join(rootpath, deptChoice)):
			if 'scene' in root: #if folder is a scene folder
				num=root[-3:] #take the exact scene number
				temp[num]='1' #mark the scene to display
		for v in temp:
			vals.append(v) #pass the marked scenes
		for v in sorted(vals):
			cmds.menuItem(label = v, p = 'sceneList') #show the marked scenes in UI
		self.changeCharBgCombo(deptChoice) #go on to initialising the models combobox
		
	def changeCharBgCombo(self, *pArgs):
		#helps load the models combobox from some locations
		#gives the exact scene and dept presently selected
		self.makeSaveInvisible()
		deptCmb = cmds.optionMenu( "deptList", query = True, value = True)
		sceneCmb = cmds.optionMenu( "sceneList", query = True, value = True)
		self.comboChBgLoad(deptCmb, sceneCmb)
		
	def saveToNW(self, *pArgs):
		#save the current file with the version incremented in the network
		self.filepathnew = (cmds.file(query=1, sn=1)).replace("/","\\") #get current file
		subs = self.filepathnew[0:self.filepathnew.rindex('\\')+1] #get the filename containing version
		versionslocal = []
		matchObj = re.match( r'.*\\(.+)\..+', self.filepathnew, re.M|re.I)
		if matchObj:
			substringForName=matchObj.group(1)[:-5]
		for f in os.listdir(subs):
			if substringForName in f:
				addThis = f[-6:-3]
				versionslocal.append(addThis)
		#getting the number part of the string and adding that to versionList
		versionslocal = sorted(versionslocal)
		theversionToOpen = versionslocal[len(versionslocal)-1]
		temp = str((int(theversionToOpen)+1)).zfill(3)
		#incrementing version number and then converting back to a string
		subs = self.filepathnew.replace(self.filepathnew[-6:-3], temp)
		cmds.file(rename = subs); cmds.file(save = True) #'save as' is not an option; so rename and save
		dept=cmds.optionMenu( "deptList", query = True, value = True)
		scene=cmds.optionMenu( "sceneList", query = True, value = True)
		self.comboChBgLoad(dept, scene)
		#to reload all other combo boxes according to the new information
		self.makeSaveVisible()
		
	def saveToWorkspace(self, *pArgs):
		#to show file dialog and save in the user specified folder
		multipleFilters = "Maya ASCII (*.ma);;Maya Binary (*.mb);;All Files (*.*)"
		filepath=cmds.fileDialog2(fileFilter=multipleFilters, dialogStyle=3)
		try:
			if filepath: #'if' not req
				newFilePath = filepath[0]
		        cmds.file(rename = newFilePath); cmds.file(save = True)
		        print "Saved to: %s" % newFilePath
		except:
			cmds.warning("You did not select a file.")	
		
	def putDeptComponents(self, *pArgs):
		#load scene folder after department is changed
		self.makeSaveInvisible()
		deptCmb = cmds.optionMenu("deptList", query = True, value = True)
		self.comboSceneLoad()
		
	#these functions make the save buttons active and inactive
	def makeSaveInvisible(self, *pArgs):
		cmds.button("btnSaveNetwork", e=1, en = 0)
		cmds.button("btnSaveWs", e=1, en = 0)
	
	def makeSaveVisible(self):
		cmds.button("btnSaveNetwork", e=1, en = 1)
		cmds.button("btnSaveWs", e=1, en = 1)

	#these functions make the load version and load latest buttons inactive
	def makeModelSceneVisible(self):
		cmds.button("btnLoadLatest", e=1, en = 1)
		cmds.button("btnLoadVersion", e=1, en = 1)

	def makeModelSceneInvisible(self):
		cmds.button("btnLoadLatest", e=1, en = 0)
		cmds.button("btnLoadVersion", e=1, en = 0)

if __name__=="__main__": #works both as a shelf script and a plug in
	obj = shotManager_SID()