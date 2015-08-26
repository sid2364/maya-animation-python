'''
Created on May 30, 2014

@author: suneeth
'''

import os
import maya.cmds as mc
import maya.mel as mel
import pipeUtilities as utils
reload(utils)
import pipeClasses as ppc
reload(ppc)
import createMayaShot as cms
reload(cms)
deptDict = {}
deptDict["ly"] = ["layout", "Layout"]
deptDict["bk"] = ["blocking", "Blocking"]
deptDict["an"] = ["animation", "Animation"]
deptDict["cl"] = ["lighting", "CL"]
deptDict["bl"] = ["lighting", "BL"]
deptDict["cc"] = ["chf", "Cloth"]
deptDict["ch"] = ["chf", "HairFur"]
deptDict["cf"] = ["chf", "Foliage"]
deptDict["fx"] = ["effects", "Effects"]
deptDict["ff"] = ["effects", "Fluid"]
deptDict["fm"] = ["effects", "Misc"]
deptShortDict = {"layout":"ly", "blocking":"bk", "animation":"an", "lighting":"cl", "chf":"cc", "effects":"fx"}
midAstDepts = ["ly", "bk", "an"]
lightDict = {"CL":"cl", "BL":"bl"}
chfDict = {"Cloth":"cc", "HairFur":"ch", "Foliage":"cf"}
fxDict = {"Effects":"fx", "Fluid":"ff", "Misc":"fm"}
shotUi = '//192.168.3.250/scripts$/tonPipe/mayaPipe/ShotManager.ui'
#breakDown = "inputs/breakdownlist"

class ShotManageUI:
    
    def __init__(self):
        self.projInfo = ppc.ProjectInfo()
        if not self.projInfo.validProject:
            utils.msgWin("Error", "Not a valid Project", False)
            return
        self.cachePipe = True if self.projInfo.pipelineType == "cache" else False
        if mc.window('shotManager', exists = 1): mc.deleteUI('shotManager')
        if mc.windowPref('shotManager', exists = 1): mc.windowPref('shotManager', r = 1)
        if mc.dockControl ('shotDock', q = True, exists = 1): mc.deleteUI ('shotDock')
        if mc.tabLayout("mainShotTab", ex = True): mc.deleteUI("mainShotTab")
        mel.eval("global string $gMainWindow;tabLayout -parent $gMainWindow mainShotTab")
        self.win = mc.loadUI(f = shotUi)
        mc.control(self.win, e = 1, ebg = 1, p = "mainShotTab")
        mc.tabLayout("mainShotTab", e = 1, tv = 0)
        mc.dockControl('shotDock', w = 375, a = 'right', con = "mainShotTab", aa = ['right', 'left'], l ='Toonz Shot Manager', vcc = self.clearDock)
        eporsq = "Episode : " if self.projInfo.epOrSeq == "ep" else "Sequence : "
        mc.text("lblEpisode", e = True, l = eporsq)
        breakDown = self.projInfo.breakDown
        self.breakDownPath = "%s/%s"%(self.projInfo.mapDrive, breakDown)
        self.setDept()
        self.deptChange()
        mc.optionMenu('cmbDepts', e = 1, cc = lambda event:self.deptChange())
        mc.optionMenu('cmbEpisode',e = 1,cc = lambda event:self.loadShots())
        mc.optionMenu('cmbShot',e = 1,cc = lambda event:self.selectDeptVer())
        mc.optionMenu('cmbDeptVer',e = 1,cc = lambda event:self.loadVersions())
        mc.optionMenu('cmbRetake',e = 1,cc = lambda event:self.loadVersions())
        mc.optionMenu('cmbCategory',e = 1,cc = lambda event:self.fgbgSwitch())
        mc.button('btnOpen',e = 1,c = lambda event:self.openFile("file"))
        mc.button('btnOpenVer',e = 1,c = lambda event:self.openFile("ver"))
        mc.button('btnImpCam',e = 1,c = lambda event:self.importCamera())
        mc.button('btnOpenBlast',e = 1,c = lambda event:self.openBlast())
        mc.button('btnCreateWs',e = 1,c = lambda event: self.createWs())
        mc.button('btnSaveToWs',e = 1, c = lambda event:self.saveFile())
        mc.button('btnSaveToLocal',e = 1, c = lambda event:self.saveFile(True))
        mc.checkBox('chkPlayblast', e = 1, cc = lambda event:self.toggleCache())
        mc.checkBox('chkCache', e = 1, cc = lambda event:self.togglePb())
        
    def toggleCache(self):
        pbChk = mc.checkBox("chkPlayblast", q = True, v = True)
        if pbChk:
            mc.checkBox("chkCache", e = True, v = 0)
            mc.button('btnSaveToWs', e = True, l = "Save and Playblast")
        else:
            mc.button('btnSaveToWs', e = True, l = "Save to Workspace")
                
    def togglePb(self):
        chChk = mc.checkBox("chkCache", q = True, v = True)
        if chChk:
            mc.checkBox("chkPlayblast", e = True, v = 0)
            mc.button('btnSaveToWs', e = True, l = "Save and Cache")
        else:
            mc.button('btnSaveToWs', e = True, l = "Save to Workspace")
        
    def createWs(self):
        astTypes = []
        loadRefChk = mc.checkBox("chkLoadRef", q = True, v = True)
        loadRef = "all" if loadRefChk else "none"
        if mc.checkBox("chkChar", q = True, v = True): astTypes.append("char")
        if mc.checkBox("chkProp", q = True, v = True): astTypes.append("prop")
        if mc.checkBox("chkSets", q = True, v = True): astTypes.append("sets")
        targRes =  mc.optionMenu('cmbSceneRes', q = 1, v = True)
        cmsObj = self.getCmsObj()
        if cmsObj.deptShort == "ly":
            cmsObj.createShot()
        elif cmsObj.deptShort == "bk":
            cmsObj.copyShot("ly", opnFile = True, loadRef = loadRef)
        elif cmsObj.deptShort == "an":
            cmsObj.copyShot("bk", opnFile = True, loadRef = loadRef)
        elif cmsObj.deptShort in ["cl", "bl"]:
            if self.cachePipe:
                cmsObj.createShot(astTypes)
            else:
                cmsObj.copyShot("an", opnFile = True, loadRef = loadRef)
        else:
            if targRes == "texture" and self.cachePipe:
                cmsObj.createShot(astTypes)
            else:
                cmsObj.copyShot("an", opnFile = True, loadRef = loadRef)
        self.loadVersions()

    def getCmsObj(self, res = None, curDeptShort = None, pb = False):
        curEpsq = mc.optionMenu('cmbEpisode', q = 1, v = True)
        curShot = mc.optionMenu('cmbShot', q = 1, v = True)
        curDept = str(mc.optionMenu('cmbDepts', q = 1, v = True))
        if curDept in ["LAYOUT", "BLOCKING", "ANIMATION"] or pb:
            deptVer = int(mc.optionMenu('cmbRetake', q = 1, v = True))
        else:
            deptVer = int(mc.optionMenu('cmbDeptVer', q = 1, v = True))
        if not curDeptShort:
            curDeptShort = self.getCurDeptShort()
        if not res:
            res = "rig" if curDeptShort in midAstDepts else "texture"
        cmsObj = cms.CreateMayaShot(epsq = curEpsq, shot = curShot, deptShort = curDeptShort, res = res, deptVer = deptVer)
        return cmsObj
    
    def setDept(self, fromScene = True):
        self.mayaShot = ppc.MayaShot(silent = "disabled")
        if self.mayaShot.validShot and fromScene:
            curDeptShort = self.mayaShot.deptShort
            if curDeptShort in deptDict.keys():
                curDept = deptDict[curDeptShort][0].upper()
                mc.optionMenu('cmbDepts', e = 1, v = curDept)
                
    def getCurDeptShort(self):
        curDeptShort = None
        curDept = mc.optionMenu('cmbDepts', q = 1, v = 1)
        if curDept in ["LAYOUT", "BLOCKING", "ANIMATION"]:
            curDeptShort = deptShortDict[curDept.lower()]
        else:
            curDeptCat = str(mc.optionMenu('cmbCategory', q = 1, v = True))
            if curDept == "LIGHTING":
                curDeptShort = lightDict[curDeptCat]
            elif curDept == "CHF":
                curDeptShort = chfDict[curDeptCat]
            else:
                if curDept == "EFFECTS":
                    curDeptShort = fxDict[curDeptCat]
        return curDeptShort

    def deptChange(self):
        self.curDept = mc.optionMenu('cmbDepts', q = 1, v = 1)
        mc.optionMenu('cmbRetake', e = 1, sl = 1)
        mc.optionMenu('cmbDeptVer', e = 1, sl = 1)
        mc.checkBox("chkCache", e = 1, en = 0)
        if self.curDept in ["LAYOUT", "BLOCKING", "ANIMATION"]:
            mc.control("grpAssetOpts", e = 1, vis = False)
            mc.control("grpSaveOpts", e = 1, vis = True)
            mc.optionMenu('cmbSceneRes', e = 1, v = "rig")
            mc.button('btnImpCam', e = 1, vis = 0)
            pbChk = mc.checkBox("chkPlayblast", q = True, v = True)
            if pbChk:
                mc.button('btnSaveToWs', e = True, l = "Save and Playblast")
            else:
                mc.button('btnSaveToWs', e = True, l = "Save and Cache")
            if self.curDept == "LAYOUT":
                crBtnText = "Create Layout Workspace"
                mc.checkBox("chkCache", e = 1, v = 0)
            elif self.curDept == "BLOCKING":
                crBtnText = "Copy from Layout Scenes"
                mc.checkBox("chkCache", e = 1, v = 0)
            else:
                crBtnText = "Copy from Blocking Scenes"
                mc.checkBox("chkCache", e = 1, en = 1)
        else:
            mc.button('btnSaveToWs', e = True, l = "Save to Workspace")
            menuItems = mc.optionMenu('cmbCategory', q = True, ill = True)
            if menuItems: mc.deleteUI(menuItems)
            if self.cachePipe:
                mc.optionMenu("cmbSceneRes", e = 1, v = "texture")
            else:
                mc.optionMenu('cmbSceneRes', e = 1, v = "rig")
            mc.button('btnImpCam', e = 1, vis = 1, en = 1)
            mc.control("grpAssetOpts", e = 1, vis = True)
            if self.curDept == "LIGHTING":
                for ky in reversed(sorted(lightDict.keys())): 
                    mc.menuItem(label = ky, p = 'cmbCategory')
                mc.control("grpSaveOpts", e = 1, vis = False)
                mc.optionMenu("cmbSceneRes", e = 1, en = 0)
            elif self.curDept == "CHF":
                for ky in sorted(chfDict.keys()): 
                    mc.menuItem(label = ky, p = 'cmbCategory')
                mc.control("grpSaveOpts", e = 1, vis = False)
                if self.cachePipe:
                    mc.optionMenu("cmbSceneRes", e = 1, en = 1)
                else:
                    mc.optionMenu("cmbSceneRes", e = 1, en = 0)
            else:
                if self.curDept == "EFFECTS":
                    for ky in sorted(fxDict.keys()): 
                        mc.menuItem(label = ky, p = 'cmbCategory')
                    mc.control("grpSaveOpts", e = 1, vis = False)
                    if self.cachePipe:
                        mc.optionMenu("cmbSceneRes", e = 1, en = 1)
                    else:
                        mc.optionMenu("cmbSceneRes", e = 1, en = 0)
            if self.cachePipe:
                crBtnText = "Create %s Workspace"%(self.curDept).capitalize()
            else:
                crBtnText = "Copy From Animation Scene"
                mc.optionMenu("cmbSceneRes", e = 1, en = 0)
        mc.button("btnCreateWs", e = 1, l = crBtnText)
        self.loadEpSqs()
        
    def importCamera(self):
        cmsObj = self.getCmsObj()
        if mc.objExists("CAM"):
            msg = "A camera already exists in the scene.\nDo you want to replace it?"
            conf=mc.confirmDialog(t='Warning',m=msg,b=['Replace','Cancel'],cb='Cancel',ds='Cancel' )
            if conf=='Replace':
                utils.importCamera(cmsObj.epsq, cmsObj.shot)
            else:
                return
            projInfo = ppc.ProjectInfo()
            mapDrive = projInfo.mapDrive
            cacheXmlPath = "%s/data/cache/%s/%s/%s/"%(mapDrive, cmsObj.epsq, cmsObj.shot, "anim")
            xmlFile = None
            if os.path.exists(cacheXmlPath):
                files = os.listdir(cacheXmlPath)
                for fil in files:
                    if fil.lower().endswith(".xml"):
                        xmlFile = fil
            if not xmlFile:
                utils.msgWin("Error", "Animation file has not been cached yet\nOr error retrieving cache xml file.", False)
                return
            self.cacheDataObj = ppc.CacheDataXml()
            self.cacheDataObj.readXML(os.path.join(cacheXmlPath, xmlFile))
            for camXMLNode in self.cacheDataObj.cameraXMLNodes:
                utils.loadAnimXML(self.cacheDataObj.xmlTree, camXMLNode)
            camName = self.cacheDataObj.cameraName
            camAttrs = mc.listAttr(camName, k = 1)
            for attr in camAttrs:
                mc.setAttr("%s.%s"%(camName, attr), l = 1)
        else:
            utils.msgWin("Error", "Couldn't find the camera. Contact R&D with the error", False)
        
    def chkFromScene(self):
        mayaShot = ppc.MayaShot(silent = "disabled")
        fromScene = False
        if mayaShot.validShot:
            fromScene = True
            curDeptShort = mayaShot.deptShort
            curDept = deptDict[curDeptShort][0]
            uiDept = mc.optionMenu('cmbDepts', q = 1, v = 1).lower()
            if not curDept == uiDept:
                fromScene = False
            curEpsq = mayaShot.epsqNum
            uiEpsq = mc.optionMenu('cmbEpisode', q = 1, v = 1)
            if not curEpsq == uiEpsq:
                fromScene = False
            curShot = mayaShot.shot
            uiShot = mc.optionMenu('cmbShot', q = 1, v = 1)
            if not curShot == uiShot:
                fromScene = False
        return fromScene
            
    def loadEpSqs(self):
        epsqIndex = 1
        epsqNums = []
        if self.mayaShot.validShot:
            self.epsqNum = self.mayaShot.epsqNum
        else:
            self.epsqNum = mc.optionMenu('cmbEpisode', q = 1, v = 1)
            if not self.epsqNum: self.epsqNum = "001"
        if os.path.exists(self.breakDownPath):
            xlFiles = [x for x in os.listdir(self.breakDownPath) if x.lower().endswith(".xls")]
        else:
            utils.msgWin("Error", "No breakdownlist created yet", False)
            return
        for xlFile in xlFiles:
            epsqName = xlFile.split("_")[1] if "_" in xlFile else None
            if epsqName:
                try:
                    epsqNums.append(epsqName[2:])
                except:
                    utils.msgWin("Warning", "Failed to read EP/SQ num from %s"%xlFile, True)
                    continue
        menuItems = mc.optionMenu('cmbEpisode', q = True, ill = True)
        if menuItems: mc.deleteUI(menuItems)
        if epsqNums:
            for i in range(len(sorted(epsqNums))):
                mc.menuItem(label = sorted(epsqNums)[i], p = 'cmbEpisode')
                if self.epsqNum == sorted(epsqNums)[i]: 
                    epsqIndex = i + 1
        else:
            utils.msgWin("Error", "No breakdownlist created yet", False)
            return
        mc.optionMenu('cmbEpisode', e = 1, sl = epsqIndex)
        self.loadShots()
        
    def loadShots(self):
        self.mayaShot = ppc.MayaShot(silent = "disabled")
        if self.mayaShot.validShot:
            self.shotNum = self.mayaShot.shot
        else:
            self.shotNum = mc.optionMenu('cmbShot', q = 1, v = 1)
            if not self.shotNum: self.shotNum = "001"
        menuItems = mc.optionMenu('cmbShot', q = True, ill = True)
        if menuItems: mc.deleteUI(menuItems)
        epsqNum = mc.optionMenu('cmbEpisode', q = 1, v = True)
        excelPath = '%s/%s_%s%s_bld.xls'%(self.breakDownPath, self.projInfo.projShort, self.projInfo.epOrSeq, epsqNum)
        xlShots = utils.getXLShots(excelPath)
        shotIndex = 1
        if xlShots:
            xlShotList = sorted(xlShots.keys())
            for i in range(len(xlShotList)):
                mc.menuItem(label = xlShotList[i], p = 'cmbShot')
                if self.shotNum == xlShotList[i]: 
                    shotIndex = i + 1
            mc.optionMenu('cmbShot', e = 1, sl = shotIndex)
        self.selectDeptVer()
        
    def selectDeptVer(self, direct = False):
        fromScene = self.chkFromScene()
        self.curDept = mc.optionMenu('cmbDepts', q=1, v=1)
        mc.optionMenu('cmbDeptVer', e = 1, sl = 1)
        mc.optionMenu('cmbRetake', e = 1, sl = 1)
        if not self.curDept in ["LAYOUT", "BLOCKING", "ANIMATION"] and not direct:
            mc.optionMenu('cmbCategory', e = 1, sl = 1)
        if fromScene:
            self.mayaShot = ppc.MayaShot(silent = "disabled")
            if not self.curDept in ["LAYOUT", "BLOCKING", "ANIMATION"] and not direct:
                curDeptCat = deptDict[self.mayaShot.deptShort][1]
                mc.optionMenu('cmbCategory', e = 1, v = curDeptCat)
            if self.mayaShot.validShot:
                curDeptVer = int(self.mayaShot.deptVer)
                curDeptShort = self.mayaShot.deptShort
                curCategory = deptDict[curDeptShort][1]
                uiCategory = mc.optionMenu('cmbCategory', q = 1, v = 1)
                if self.curDept in ["LAYOUT", "BLOCKING", "ANIMATION"]:
                    mc.optionMenu('cmbRetake', e = 1, v = curDeptVer)
                else:
                    if curCategory == uiCategory:
                        mc.optionMenu('cmbDeptVer', e = 1, v = curDeptVer)
            wsPath = self.mayaShot.shotPath
        else:
            curDeptShort = self.getCurDeptShort()
            res = "rig" if curDeptShort in midAstDepts else "texture"
            cmsObj = self.getCmsObj(res, curDeptShort)
            wsPath = cmsObj.wsPath
        if self.curDept in ["LAYOUT", "BLOCKING", "ANIMATION"]:
            retakes = utils.findLastRetake(wsPath, "ma", True)
            if retakes:
                mc.optionMenu('cmbRetake', e = 1, v = retakes[-1])
        self.loadVersions()
        
    def loadVersions(self):
        menuItems = mc.optionMenu('cmbVer', q = True, ill = True)
        if menuItems: mc.deleteUI(menuItems)
        curDept = str(mc.optionMenu('cmbDepts', q = 1, v = True)).lower()
        curDeptShort = self.getCurDeptShort()
        res = "rig" if curDeptShort in midAstDepts else "texture"
        cmsObj = self.getCmsObj(res, curDeptShort)
        wsPath = cmsObj.wsPath
        wsMayaFile = "%s.%s"%(cmsObj.fileName, cmsObj.ext)
        if curDept == "layout":
            wsBlstFile = "%s.avi"%cmsObj.fileName
            self.wsBlstFilePath = os.path.join(wsPath, wsBlstFile)
        elif curDept == "blocking":
            cmsBlastObj = self.getCmsObj("rig", "bk", pb = True)
            wsBlastPath = cmsBlastObj.wsPath
            wsBlstFile = "%s.avi"%cmsBlastObj.fileName
            self.wsBlstFilePath = os.path.join(wsBlastPath, wsBlstFile)
        else:
            cmsBlastObj = self.getCmsObj("rig", "an", pb = True)
            wsBlastPath = cmsBlastObj.wsPath
            wsBlstFile = "%s.avi"%cmsBlastObj.fileName
            self.wsBlstFilePath = os.path.join(wsBlastPath, wsBlstFile)
        if os.path.exists(os.path.join(wsPath, wsMayaFile)):
            mc.button("btnOpen", e = 1, en = 1)
            mc.button("btnOpen", e = 1, en = 1)
        else:
            mc.button("btnOpen", e = 1, en = 0)
        if os.path.exists(self.wsBlstFilePath):
            mc.button("btnOpenBlast", e = 1, en = 1)
        else:
            mc.button("btnOpenBlast", e = 1, en = 0)
        versions = utils.findLastVersion(wsPath, self.projInfo.mayaExt, True, wsMayaFile)
        if versions:
            for ver in versions:
                mc.menuItem(label = ver, p = 'cmbVer')
            mc.optionMenu('cmbVer', e = 1, v = versions[-1])
            mc.optionMenu('cmbVer', e = 1, en = 1)
            mc.button("btnOpenVer", e = 1, en = 1)
        else:
            mc.button("btnOpenVer", e = 1, en = 0)
            mc.optionMenu('cmbVer', e = 1, en = 0)
            
    def openFile(self, mode = "file"):
        cmsObj = self.getCmsObj()
        if mode == "file":
            mayaPath = os.path.join(cmsObj.wsPath, "%s.%s"%(cmsObj.fileName, cmsObj.ext))
        else:
            ver = mc.optionMenu("cmbVer", q = 1, v = 1)
            fileName = cmsObj.fileName[:-2] + str(ver).zfill(2) + ".%s"%cmsObj.ext
            mayaPath = os.path.join(cmsObj.wsPath, "ver", fileName)
        loadRef = mc.checkBox("chkLoadRef", q = 1, v = 1)
        loadRefDepth = "all" if loadRef else "none"
        mc.file(mayaPath, f=1, o=1, lrd = loadRefDepth)
        if not loadRef: mc.ReferenceEditor()
        
    def saveFile(self, local = False):
        pBlast, cchChk, pbStat = False, False, True
        cmsObj = self.getCmsObj()
        if cmsObj.deptShort in ["ly", "bk", "an"]:
            pBlast = mc.checkBox("chkPlayblast", q = 1, v = 1)
            if pBlast:
                viewport = utils.getActiveViewport()
                if not viewport:
                    utils.msgWin("Error", "Couldn't get active viewport. Please\nactivate viewport and try again.", False)
                    return
            cchChk = mc.checkBox("chkCache", q = 1, v = 1)
            if cchChk:
                cacheDataObj = ppc.CacheDataXml()
                cacheExportError = cacheDataObj.checkExportErrors(False)
                if cacheExportError:
                    return
        mayaShot = ppc.MayaShot(silent = "disabled")
        if not mayaShot.validShot:
            utils.msgWin("Error", "Not a valid shot", False)
            return
        if not (mayaShot.deptShort == cmsObj.deptShort):
            msg = "Scene department does not match the dept selected in manager."
            utils.msgWin("Error", msg, False)
            return
        if not(mayaShot.epSqName == cmsObj.epsq and mayaShot.shName == cmsObj.shot):
            msg = "Scene shot number does not match the shot selected in manager."
            msg += "\nDo you want to save using the shot number selected in manager?"
            msg += "\nThis will rename camera and obtain frames from breakdown list."
            conf = mc.confirmDialog(t = "Warning", m = msg, button = ['Save', 'Cancel'], cancelButton = 'Cancel', dismissString = 'Cancel')
            if conf == 'Cancel':
                return
        if local:
            wsFileFldr = mc.fileDialog2(dialogStyle = 1, fm = 3)
            if wsFileFldr:
                newFilePath = os.path.join(wsFileFldr[0], "%s.%s"%(cmsObj.fileName, cmsObj.ext))
                if os.path.exists(newFilePath):
                    utils.saveVersion(newFilePath)
                mc.file(rename = newFilePath)
                mc.file(save = True)
                blastPath = newFilePath.replace(".%s"%cmsObj.ext, ".avi")
            else:
                utils.msgWin("Error", "No folder selected", True)
                return
        else:
            wsFilePath = os.path.join(cmsObj.wsPath, "%s.%s"%(cmsObj.fileName, cmsObj.ext))
            utils.saveVersion(wsFilePath)
            mc.file(rename = wsFilePath)
            utils.sceneCleanup()
            mc.file(save = True)
            blastPath = None
        msg = "File successfully Saved"
        if pBlast:
            pbStat = utils.takePlayblast(True, False, blastPath)
        mc.refresh()
        if cchChk and not local:
            cacheDataObj = ppc.CacheDataXml()
            cacheDataObj.writeXML()
            msg = "File successfully Saved and Cached"
        if not pbStat: msg = msg + "\n\nThere were errors while taking the playblast.\nPlease check the script editor for details."
        utils.msgWin("Success", msg, False)
        self.loadVersions()
            
    def openBlast(self):
        curDept = str(mc.optionMenu('cmbDepts', q = 1, v = True)).lower()
        if curDept == "layout":
            cmsObj = self.getCmsObj()
        elif curDept == "blocking":
            cmsObj = self.getCmsObj(curDeptShort = "bk", pb = True)
        else:
            cmsObj = self.getCmsObj(curDeptShort = "an", pb = True)
        wsBlstFilePath = os.path.join(cmsObj.wsPath, "%s.avi"%cmsObj.fileName)
        os.startfile(wsBlstFilePath)
            
    def fgbgSwitch(self):
        curDept = mc.optionMenu('cmbDepts', q = 1, v = 1)
        if curDept == "LIGHTING":
            fgbg = mc.optionMenu('cmbCategory', q = 1, v = 1)
            if fgbg == "CL":
                mc.checkBox("chkChar", e = 1, v = 1)
                mc.checkBox("chkProp", e = 1, v = 1)
                mc.checkBox("chkSets", e = 1, v = 0)
            else:
                mc.checkBox("chkChar", e = 1, v = 0)
                mc.checkBox("chkProp", e = 1, v = 0)
                mc.checkBox("chkSets", e = 1, v = 1)
        self.selectDeptVer(direct = True)
        
    def clearDock(self, k = False):
        obscured = mc.dockControl('shotDock', q = True, io = True)
        if obscured:
            mc.evalDeferred(self.deleteDock)
            
    def deleteDock(self):
        obscured = mc.dockControl('shotDock', q = True, io = True)
        docked = mc.dockControl('shotDock', q = True, fl = True)
        if obscured and not docked:
            try:
                mc.evalDeferred("mc.deleteUI('shotDock')")
                print "Cleared Dock"
            except:
                pass            
