'''
Created on Apr 24, 2014

@author: suneeth
'''

import maya.cmds as mc
import os, re, datetime, shutil
import pipeUtilities as utils
reload(utils)
import xml.etree.ElementTree as ET

deptDict = {}
deptDict["st"] = "staging"
deptDict["an"] = "animation"
deptDict["cl"] = "lighting"
deptDict["bl"] = "lighting"
deptDict["cc"] = "chf"
deptDict["ch"] = "chf"
deptDict["cf"] = "chf"
deptDict["fx"] = "fx"
deptDict["ff"] = "fx"
deptDict["fm"] = "fx"

deptShortDict = {"modelling":"md", "texturing":"tx", "rigging":"ri", "chf":"cc", "publish":"pb"}

projectPathsXml = '//192.168.3.250/scripts$/config/projectPaths.xml'
astGrpDict = {"char":"CHARACTERS", "prop":"PROPS", "elms":"PROPS", "sets":"SETS"}
pubFolder = "/assets/publish/"

class AssetFile:
    
    def __init__(self, astPath):
#       J:\assets\modeling\char\kms001_alienhand00c_m\kms001_alienhand00c_m_md000.ma
#       V:\abn\assets\Modeling\Char\BirdRocAdult00c\abn01_BirdRocAdult00c_md01_v000.ma
        self.astPatrnDict = {"projShort":None, "epsqNum":None, "astName":None, "astVer":None, "astType":None, "astRes":None, "deptShort":None, "deptVer":None, "version":None, "mayaExt":None}
        self.projInfo = ProjectInfo()
        self.astPath = astPath.replace("\\", "/")
        self.validAsset = True
        self.astNameConv = self.projInfo.astNameConv
        self.analyseAstPattern()
#         self.pattern = "%s[0-9]{3}_[a-z]{2}[a-z]*[0-9]{2}(c|s|p)_(p|m|h)_[a-z]{2}[0-9]{3}.%s"%(self.projInfo.projShort, self.projInfo.mayaExt)
        self.pattern = "%s[0-9]{2}_[a-z,A-Z]{2}[a-z,A-Z]*[0-9]{2}(c|s|p)_[a-z]{2}[0-9]{2}_v[0-9]{3}.%s"%(self.projInfo.projShort, self.projInfo.mayaExt)
#         self.patters = "%s[0-9]{2}_[a-z,A-Z]{2}[a-z,A-Z]*[0-9]{2}(c|s|p)_[a-z]{2}[0-9]{2}_v[0-9]{3}.%s"
        self.area = "workspace"
        self.analyseAstName()
        if "/assets/" in self.astPath:
            if "/assets/publish" in self.astPath:
                self.area = "publish"
            else:
                self.area = "assets"
        else:
            self.area = "workspace"
        
    def analyseAstPattern(self):
#abn~projShort~[0-9]{2}~epsqNum~_[a-z,A-Z]{2}[a-z,A-Z]*~astName~[0-9]{2}~astVer~(c|s|p)~astType~_[a-z]{2}~deptShort~[0-9]{2}~deptVer~_v[0-9]{3}~version~.ma~mayaExt~
#kms~projShort~[0-9]{3}~epsqNum~_[a-z]{2}[a-z]*~astName~[0-9]{2}~astVer~(c|s|p)~astType~_(p|m|h)~astRes~_[a-z]{2}~deptShort~[0-9]{3}~version~.ma~mayaExt~
        patrnSplit = self.astNameConv.split("~")
        self.infCatLst, self.infPatLst = [], []
        while patrnSplit:
            infPat = patrnSplit.pop(0)
            infCat = patrnSplit.pop(0)
            if infCat in self.astPatrnDict.keys():
                self.infPatLst.append(infPat)
                self.infCatLst.append(infCat)
                self.astPatrnDict[infCat] = infPat
            else:
                print "Could not find category : %s"%infCat
        print "\n\n"
        print os.path.basename(self.astPath)
        print "".join(self.infPatLst)
        for ky in self.astPatrnDict.keys():
            print ky, self.astPatrnDict[ky]
           
    def analyseAstName(self):
        self.fileName = os.path.basename(self.astPath)
        if not re.match(self.pattern, self.fileName):
            self.validAsset = False
            return
        astNameSplit = self.fileName.split("_")
        self.epsqNum = astNameSplit[0][3:]
        self.astShortName = astNameSplit[1]
        astTypeAlph = astNameSplit[1][-1]
        if astTypeAlph == "s":
            self.astType = "sets"
        elif astTypeAlph == "p":
            self.astType = "prop"
        else:
            self.astType = "char"
        self.astVer = astNameSplit[1][-3:-1]
        self.res = astNameSplit[2]
        self.deptShort = astNameSplit[3][:2]
        self.version = astNameSplit[3][2:]
        self.astFldr = os.path.dirname(self.astPath)
        self.versions = utils.findLastAstVersion(self.astFldr, self.projInfo.mayaExt, True, self.fileName)
        
    def getAstName(self, deptShort = None, res = None, epsqNum = None, version = None):
        if not deptShort:
            deptShort = self.deptShort
        if not res:
            res = self.res
        if not epsqNum:
            epsqNum = self.epsqNum
        if not version:
            version = self.version
        fileName = "%s%s_%s_%s_%s%s.%s"%(self.projInfo.projShort, epsqNum, self.astShortName, res, deptShort, version, self.projInfo.mayaExt)
        return fileName
    
#     def analyseAstName(self):
# #         abn01_BirdRocAdult00c_md01_v000.ma
#         self.fileName = os.path.basename(self.astPath)
#         if not re.match(self.pattern, self.fileName):
#             self.validAsset = False
#             return
#         astNameSplit = self.fileName.split("_")
#         self.epsqNum = astNameSplit[0][3:]
#         self.astShortName = astNameSplit[1]
#         astTypeAlph = astNameSplit[1][-1]
#         if astTypeAlph == "s":
#             self.astType = "sets"
#         elif astTypeAlph == "p":
#             self.astType = "prop"
#         else:
#             self.astType = "char"
#         self.astVer = astNameSplit[1][-3:-1]
#         self.deptShort = astNameSplit[2][:2]
#         self.deptVersion = astNameSplit[2][2:]
#         self.version = astNameSplit[3].split(".")[0][1:]
#         self.astFldr = os.path.dirname(self.astPath)
#         self.versions = utils.findLastAstVersion(self.astFldr, self.projInfo.mayaExt, True, self.fileName)    
# 
#     def getAstName(self, deptShort = None, epsqNum = None, deptVer = None, version = None):
#         if not deptShort:
#             deptShort = self.deptShort
#         if not deptVer:
#             deptVer = self.deptVersion
#         if not epsqNum:
#             epsqNum = self.epsqNum
#         if not version:
#             version = self.version
#         fileName = "%s%s_%s_%s%s_v%s.%s"%(self.projInfo.projShort, epsqNum, self.astShortName, deptShort, deptVer, version, self.projInfo.mayaExt)
#         return fileName
        
    def getAstPath(self, area = "workspace", deptShort = None, res = "m"):
        if not deptShort:
            deptShort = self.deptShort   
        mapPath = "%s:"%self.projInfo.mapDrive
        if area == "assets":
            stPath = "%s/assets"%mapPath
        elif area == "publish":
            stPath = "%s/assets/publish"%mapPath
        else:
            stPath = "%s/workspace"%mapPath
        deptShortDictInv = dict((v,k) for k, v in deptShortDict.iteritems())
        return "%s/%s/%s/%s"%(stPath, deptShortDictInv[deptShort], self.astType, self.astFldr)

class MayaAsset:
    
    def __init__(self, refNode, silent = True):
        self.validAsset = True
        self.refNode = refNode
        self.silent = silent
        self.validAsset = True
        self.defineAsset()
        
    def defineAsset(self):
        self.assetType, self.topGrp, self.astRes = None, None, None
        self.refObjs = []
        if not mc.referenceQuery(self.refNode,il=1):
            utils.msgWin("Warning", "Reference not loaded for %s"%self.refNode, self.silent)
            self.refLoaded = False
        else:
            self.refLoaded = True
        self.assetPath = mc.referenceQuery(self.refNode, f = True, wcn = True)
        self.assetPathCopyNum = mc.referenceQuery(self.refNode, f = True, wcn = False)
        self.namespace = mc.file(self.assetPathCopyNum, q = 1, ns = 1)
        if "/char/" in self.assetPath: self.assetType = "char" 
        if "/prop/" in self.assetPath: self.assetType = "prop"
        if "/sets/" in self.assetPath: self.assetType = "sets"
        if not self.assetType:
            utils.msgWin("Error", "Error identifying asset type from asset path for %s"%self.refNode, self.silent)
            self.validAsset = False
        if self.refLoaded:
            self.refObjs = mc.referenceQuery(self.refNode,n=1)
            if not self.refObjs:
                utils.msgWin("Error", "Couldn't find any referenced objects", self.silent)
                self.validAsset = False
            self.topGrp = self.refObjs[0]
            if self.assetType == "prop":
                topGrpAttrs = mc.listAttr(self.topGrp,ud=1)
                if topGrpAttrs:
                    if ('Elements' in topGrpAttrs):
                        self.assetType = 'elms'
            self.astRes = str(utils.findObjRes(self.topGrp))
            
    def importAssetCache(self, cacheXmlLt, cacheErrorCheck = False):
        """ cacheXmlLt = "R:/data/cache/sq001/sh001/light/char/ben00c_ben/ben00c_ben.xml" """
        if os.path.exists(cacheXmlLt):
            cacheChannels = mc.cacheFile(fileName=cacheXmlLt,q=1,channelName=1)
            cacheGeos = self.getCacheGeos()
            cacheGeoDict, cacheChannelsTmp = {}, []
            for chn in cacheChannels:
                for geo in cacheGeos:
                    baseChn = utils.stripNames(utils.convertName(chn, "texture"))
                    baseGeo = utils.stripNames(utils.stripNames(geo, ":"), "|")
                    if baseChn in baseGeo:
                        cacheGeoDict[chn] = geo
                        cacheChannelsTmp.append(chn)
                        continue
        else:
            utils.msgWin("Error", "File does not exist : %s"%cacheXmlLt, self.silent)
            return False
        if cacheErrorCheck:
            missedChannels = list(set(cacheChannels).difference(set(cacheGeoDict.keys())))
            if len(missedChannels) > 0:
                msg = "Cache geometry missing\n"
                msg += "\n".join(missedChannels)
                utils.msgWin("Error", msg, self.silent)
                return missedChannels
            else:
                return False
        for chNode in self.getCacheNodes():
            mc.delete(chNode)
        for chn in cacheGeoDict.keys():
            deformShp = cacheGeoDict[chn]
            try:
                shpSwitch = mc.deformer(deformShp, type="historySwitch")
            except:
                continue
            shpHist = mc.listHistory(deformShp, pdo=1)
            if shpHist:
                for hist in shpHist:
                    if mc.nodeType(hist) == "tweak":
                        dblList = mc.listAttr("%s.plist"%hist, m= 1)
                        fltList = mc.listAttr("%s.vlist"%hist, m= 1)
                        dbCon, flCon = False, False
                        if dblList:
                            if len(dblList) > 1: dbCon = True
                        if fltList:
                            if len(fltList) > 1: flCon = True
                        if not(dbCon or flCon):
                            mc.delete(hist)
                        break
            conns = mc.listConnections("%s.ip[0].ig"%shpSwitch[0], p=1)
            mc.connectAttr(conns[0], "%s.ug[0]"%shpSwitch[0])
            mc.setAttr("%s.playFromCache"%shpSwitch[0], 1)
            mc.getAttr("%s.op[0]"%shpSwitch[0], sl = 1)
            mc.setAttr("%s.playFromCache"%shpSwitch[0], 0)
            mc.disconnectAttr(conns[0], "%s.ug[0]"%shpSwitch[0])
            switch = mc.rename(shpSwitch[0],'cacheSwitch#')
            mc.setAttr(switch+'.ihi',0)
            cacheNode = mc.cacheFile(f = cacheXmlLt, attachFile = True, ia = '%s.inp[0]'%switch, cnm = chn)
            mc.connectAttr(cacheNode+".inRange", switch + '.playFromCache')
        utils.msgWin("Message", "Cache loaded successfully for %s"%self.namespace, self.silent)
        return True
    
    def exportAssetCache(self, cacheXmlAn):
        """ cacheXmlAn = "R:/data/cache/sq999/sh001" """
        self.animCachePath=self.getAstCacheFldr(cacheXmlAn, "anim")
        stF = mc.playbackOptions(q=1,ast=1)
        edF = mc.playbackOptions(q=1,aet=1)
        if os.path.exists(self.animCachePath):
            shutil.rmtree(self.animCachePath,ignore_errors=True)
        os.makedirs(self.animCachePath)
        pts = self.getCacheGeos()
        if pts:
            mc.cacheFile(pts=pts,f=self.astCacheName,directory=self.animCachePath,cacheFormat="mcc",st=stF,et=edF,fm='OneFile',sch=1)
        utils.msgWin("Message", "Cache exported successfully for %s"%self.namespace, self.silent)
        return True
        
    def getAstCacheFldr(self, shotCacheFldr, typ = "anim"):
        self.astCacheName = utils.convertName(self.topGrp, "rig").replace(':','_')
        animCachePath='%s/%s/%s/%s' %(shotCacheFldr,typ,self.assetType,self.astCacheName)
        return animCachePath
    
    def getAstCacheXML(self, shotCacheFldr, typ = "anim"):
        self.astCacheFldr = self.getAstCacheFldr(shotCacheFldr, typ)
        astXmlName = "%s.xml"%self.astCacheName
        astCacheXml = os.path.join(self.astCacheFldr, astXmlName)
        return astCacheXml
            
    def getCacheGeos(self):
        geoGrp = self.getGrp('GEO')
        if not geoGrp:
            return []
        cacheGeos = []
        if mc.listAttr(geoGrp, st = "Static"):
            if mc.getAttr("%s.Static"%geoGrp):
                return []
        geoTransforms=mc.listRelatives(geoGrp,c=1,ad=1,ni=1,type='transform',f=1)
        if geoTransforms:
            for eachTrans in geoTransforms:
                shpNode=mc.listRelatives(eachTrans,s=1,c=1,type='mesh',ni=1,f=1)
                if shpNode:
                    vtxCheck=mc.polyEvaluate(shpNode,v=1)
                    if vtxCheck:
                        cacheGeos.append(str(shpNode[0]))
        if cacheGeos:
            return cacheGeos
        else:
            utils.msgWin("Warning", "No cacheable geomtry found", self.silent)
            return []
        
    def getCacheNodes(self):
        cacheGeos = self.getCacheGeos()
        cacheNodes = []
        for geo in cacheGeos:
            geoHist = mc.listHistory(geo)
            for his in geoHist:
                if mc.nodeType(his) == "cacheFile":
                    cacheNodes.append(his)
        return cacheNodes
    
    def getVisGeo(self):
        modelsGrp = self.getGrp('MODELS')
        if not modelsGrp:
            return [], []
        geoBake, geoInvis = [], []
        geoTransforms=mc.listRelatives(modelsGrp,ad=1,type='transform')
        geoTransforms.append(self.topGrp)
        if geoTransforms:
            for eachTrans in geoTransforms:
                conns = mc.listConnections("%s.visibility"%eachTrans, d=0, s=1)
                if conns:
                    geoBake.append(eachTrans)
                else:
                    if not mc.getAttr("%s.visibility"%eachTrans):
                        geoInvis.append(eachTrans)
        return geoBake, geoInvis
    
    def getGrp(self, grpName = 'GEO'):
        for obj in self.refObjs:
            if obj.endswith(grpName):
                return obj
        utils.msgWin("Error", "Couldn't find %s group"%grpName, self.silent)
        return None
    
class MayaShot:
    
    def __init__(self, filename = None, silent = True):
        self.validShot, self.mapDrive = True, None
        self.silent = silent
        self.assets, self.chars, self.props, self.sets, self.elms, self.namespaces = [], [], [], [], [], []
        self.projInfo = ProjectInfo()
        if self.projInfo.validProject:
            self.mapDrive = self.projInfo.mapDrive
        else:
            utils.msgWin("Error", "Error getting project information", self.silent)
            self.validShot = False
            return
        if not self.mapDrive:
            self.validShot = False
        self.shotPath = mc.file(q = True, sn = True)
        if filename:
            self.filename = filename
        else:
            curFile = os.path.basename(self.shotPath)
            self.filename = curFile.replace("_tmp", "") if "_tmp" in curFile else curFile
        if not self.defineShot():
            self.validShot = False
        
    def defineShot(self):
        """ self.filename = ctr_sq001sh001_st_v00.ma|ccy_sq100sh002a_an_v00.ma """
        self.startF = mc.playbackOptions(q=1,ast=1)
        self.endF = mc.playbackOptions(q=1,aet=1)
        fObj = utils.analyseFileName(self.filename)
        if fObj.validShot:
            self.ext = fObj.ext
            self.projShort = fObj.projShort
            self.epsq = fObj.epsq
            self.epsqNum = fObj.epsqNum
            self.epSqName = '%s%s' % (self.epsq,self.epsqNum)
            self.shot = fObj.shot
            self.shName = 'sh%s' % (self.shot)
            self.deptShort = fObj.deptShort
            self.deptVer = fObj.deptVer
            self.xlPath = '%s/inputs/breakdownlist/%s_%s_bld.xls'%(self.projInfo.mapDrive,self.projInfo.projShort,self.epSqName)
            self.xlShotDict = None
            if os.path.exists(self.xlPath):
                self.xlShotDict = utils.getXLShotDetails(self.xlPath, self.shot)
            if not self.xlShotDict:
                utils.msgWin("Error", "Invalid breakdown excel file %s"%self.xlPath, self.silent)
                return False
            self.frames = self.xlShotDict["frames"]
            self.cacheFldr = "%s/data/cache/%s/%s"%(self.mapDrive, self.epSqName, self.shName)
            self.refNodes = []
            for ref in mc.ls(typ = "reference"):
                try:
                    mc.referenceQuery(ref, inr=1)
                except:
                    continue
                try:
                    mc.referenceQuery(ref, f = 1,wcn = 1)
                except:
                    continue
                topRef = mc.referenceQuery(ref, rfn = True, tr = True)
                if not topRef in self.refNodes:
                    self.refNodes.append(topRef)
            self.namespaces = []
            for ref in self.refNodes:
                ast = MayaAsset(ref)
                if ast.validAsset:
                    self.assets.append(ast)
                    self.namespaces.append(ast.namespace)
                    if ast.assetType == "char": self.chars.append(ast)
                    if ast.assetType == "prop": self.props.append(ast)
                    if ast.assetType == "sets": self.sets.append(ast)
                    if ast.assetType == "elms": self.elms.append(ast)
            return True
        else:
            utils.msgWin("Error", "Invalid shot name %s"%self.filename, self.silent)
            return False
        
    def getSceneCamera(self, silent = True):
        camPattern = "(ep|sq)[0-9]{3}sh[0-9]{3}([a-z]{1})?_camCt"
        camName = "%s%s_camCt" % (self.epSqName, self.shName)
        scCams = mc.ls(type = "camera")
        renCams = []
        for cam in scCams:
            camTr = mc.listRelatives(cam, p = True)
            pMatch = re.search(camPattern, camTr[0])
            if pMatch:
                renCams.append(camTr[0])
        if not renCams:
            utils.msgWin("Error", "Couldn't find a valid camera", silent)
            return None
        if len(renCams) > 1:
            utils.msgWin("Error", "Too many cameras in the scene.\nPlease delete unwanted cameras", silent)
            return None
        if not renCams[0] == camName:
            utils.msgWin("Error", "Camera has wrong name. Please run Scene Cleanup", silent)
            return None
        return camName
        
    def moveAssetsToGrps(self):
        for astType in astGrpDict.keys():
            grp = astGrpDict[astType]
            if mc.objExists(grp):
                grpPrnt = mc.listRelatives(grp, p = True)
                if grpPrnt:
                    mc.parent(grp, w = True)
        mc.select(cl = True)
        for ast in self.assets:
            parentGrp = astGrpDict[ast.assetType]
            if not mc.objExists(parentGrp):
                mc.group(n = parentGrp, em = True)
            try:
                mc.parent(ast.topGrp, parentGrp)
            except:
                pass
        
    def getShotFldr(self, dept = "an", area = "workspace"):
        areas = ["workspace", "scenes"]
        if not dept in deptDict.keys():
            utils.msgWin("Error", "Unknown department short %s"%dept, self.silent)
            return None
        if not area in areas:
            utils.msgWin("Error", "Unknown area %s"%area, self.silent)
            return None
        return "%s/%s/%s/%s/%s"%(self.mapDrive, area, deptDict[dept], self.epSqName, self.shName)
    
    def getCacheFldr(self, typ = "anim"):
        types = ["anim", "light", "shot"]
        if not typ in types:
            utils.msgWin("Error", "Unknown cache folder type %s"%typ, self.silent)
            return None
        if typ == "shot":
            return "%s/data/cache/%s/%s"%(self.mapDrive, self.epSqName, self.shName)
        else:
            return "%s/data/cache/%s/%s/%s"%(self.mapDrive, self.epSqName, self.shName, typ)
        
    def getCacheXmlFile(self, typ = "anim"):
        types = ["anim", "light"]
        if not typ in types:
            utils.msgWin("Error", "Unknown cache folder type %s"%typ, self.silent)
            return None
        pattern = "_%s([0-9]{2})?_"%self.deptShort
        matchObj = re.search(pattern, self.filename.split(".")[0])
        if matchObj:
            xmlFileName = (self.filename.split(".")[0]).replace(matchObj.group(0), "_an_")
            return "%s/data/cache/%s/%s/%s/%s.xml"%(self.mapDrive, self.epSqName, self.shName, typ, xmlFileName)
        else:
            return None
    
class CacheDataXml:
    
    def __init__(self, silent = True):
        """ cacheXmlPath = "R:/data/cache/sq001/sh002/anim/char/ben00c_ben/ben00c_ben.xml" """
        self.silent = silent
        self.valid = True
        self.user = ''
        self.date = ''
        self.time = ''
        self.stF = ''
        self.edF = ''
        self.characters = []
        self.props = []
        self.sets = []
        self.elms = []
        self.msg = "\n"
        self.shotCacheFldr = None
        self.shotCacheXmlAn = None
        self.shotCacheXmlLt = None
        self.fileName = None
        self.importErrorLog = []
        self.exportErrorLog = []
        if mc.objExists("sn_comments"):
            self.comments = mc.getAttr("sn_comments.comments")
        else:
            self.comments = ""
        self.mayaShot = MayaShot()
        if self.mayaShot.validShot:
            self.shotPath = os.path.dirname(self.mayaShot.shotPath)
            self.shotCacheFldr = self.mayaShot.getCacheFldr("shot")
            self.shotCacheXmlAn = self.mayaShot.getCacheXmlFile("anim")
            self.shotCacheXmlLt = self.mayaShot.getCacheXmlFile("light")
            self.fileName = self.mayaShot.filename.split(".")[0] + ".xml"
        else:
            self.valid = False
        
    def checkExportErrors(self, silent = True):
        errorLog = []
        if not os.path.exists(self.shotCacheFldr):
            try:
                os.makedirs(self.shotCacheFldr)
            except:
                utils.msgWin("Error", "Unable to create folder %s"%self.shotCacheFldr, silent = True)
                errorLog.append("Unable to create folder %s"%self.shotCacheFldr)
        if not utils.writePermission(self.shotCacheFldr):
            utils.msgWin("Error", "No write permission in %s"%self.shotCacheFldr, silent = True)
            errorLog.append("No write permission in %s"%self.shotCacheFldr)
        if not os.path.exists(self.shotPath):
            try:
                os.makedirs(self.shotPath)
            except:
                utils.msgWin("Error", "Unable to create folder %s"%self.shotPath, silent = True)
                errorLog.append("Unable to create folder %s"%self.shotPath)
        if not utils.writePermission(os.path.dirname(self.shotPath)):
            utils.msgWin("Error", "No write permission in %s"%os.path.dirname(self.shotPath), silent = True)
            errorLog.append("No write permission in %s"%os.path.dirname(self.shotPath))
        if errorLog:
            self.exportErrorLog = errorLog
            utils.msgWin("Export Errors", "\n".join(errorLog), silent)
            return True
        else:
            return False
    
    def checkImportErrors(self, silent = True, update = False, refNodes = []):
        errorLog = []
        if self.checkExportErrors():
            errorLog.extend(self.exportErrorLog)
        if not os.path.exists(self.shotCacheXmlAn):
            utils.msgWin("Error", "XML file does not exist : %s"%self.shotCacheXmlAn, True)
            errorLog.append("XML file does not exist : %s"%self.shotCacheXmlAn)
        else:
            self.readXML()
            cacheNotFound = []
            animFldr = os.path.join(self.shotCacheFldr, "anim")
            liteFldr = os.path.join(self.shotCacheFldr, "light")
            if refNodes:
                asts = refNodes
                refRes = "texture"
            else:
                asts = self.assets.keys()
                refRes = "rig"
            for ast in asts:
                if refRes == "texture":
                    astObj = MayaAsset(ast)
                    if astObj.validAsset:
                        scNamespace = astObj.namespace
                        namespace = utils.convertName(scNamespace, "rig", True)
                        topNode = astObj.topGrp
                        if not mc.objExists(topNode):
                            errorLog.append("Missing reference/assets in scene : %s"%topNode)
                            continue
                    else:
                        continue
                else:
                    namespace = self.assets[ast]['namespace']
                    scNamespace = utils.convertName(namespace, "texture", True)
                    topName = self.assets[ast]['name']
                    topNode = "%s:%s"%(scNamespace, topName)
                    if mc.objExists(topNode):
                        try:
                            refNode = mc.referenceQuery(topNode, rfn = True)
                        except:
                            print "Reference has been cut for : %s"%topNode
                            continue
                    else:
                        errorLog.append("Missing reference/asset in scene : %s"%topNode)
                        continue
                    astObj = MayaAsset(refNode)
                if not os.path.exists(astObj.assetPath):
                    errorLog.append("Missing High Asset : %s"%astObj.assetPath)
                    utils.msgWin("Error", "Missing High Asset : %s"%astObj.assetPath, True)
                astType = astObj.assetType
                cacheName = (utils.convertName(topNode, "rig", False)).replace(":", "_")
                cacheFldrAn = os.path.join(animFldr, astType, cacheName)
                cacheFldrLt = os.path.join(liteFldr, astType, cacheName)
                cacheFile = os.path.join(cacheFldrAn, "%s.mc"%cacheName)
                if astObj.getCacheGeos():
                    if not os.path.exists(cacheFile):
                        cacheFile = os.path.join(cacheFldrLt, "%s.mc"%cacheName)
                        if not os.path.exists(cacheFile):
                            print "missing", cacheFile
                            cacheNotFound.append(cacheFile.replace("\\", "/"))
                missedChn = astObj.importAssetCache(cacheFile, True) 
                if missedChn:
                    errorLog.append("Cache Geometry missing for %s"%astObj.namespace)
                    print "\nCache Geometry missing for %s:"%astObj.namespace
                    for chn in missedChn:
                        print "Channel mismatch for %s"%chn
                    print "\n"
            if cacheNotFound:
                errorLog.append("\nThe following animation cache files do not exist:\n")
                utils.msgWin("Error", "\nThe following animation cache files do not exist:\n", True)
                for cchNotF in cacheNotFound:
                    errorLog.append("%s"%cchNotF)
                    utils.msgWin("Error", "%s"%cchNotF, True)
            if os.path.exists(os.path.dirname(self.shotCacheXmlLt)):
                lockedFiles = utils.checkLockedFiles(os.path.dirname(self.shotCacheXmlLt), "mc")
                if lockedFiles:
                    msg = "Following Light cache files are in use. Please close\nallother maya files that might be accessing this cache folder\n"
                    for lckFil in lockedFiles:
                        msg += "%s\n"%lckFil
                    utils.msgWin("Error", msg, True)
                    errorLog.append(msg)
        if update:
            if not os.path.exists(self.shotCacheXmlLt):
                utils.msgWin("Error", "Light XML not found : %s"%self.shotCacheXmlLt, True)
                errorLog.append("Light XML not found : %s"%self.shotCacheXmlLt)
        if errorLog:
            errorLog.append("\nImport Cache Operation Aborted\n")
            self.importErrorLog = errorLog
            utils.msgWin("Cache Scene Errors", "\n".join(errorLog), silent)
            return True
        else:
            return False
        
    def readXML(self, cacheXmlPath = None):
        if not cacheXmlPath:
            cacheXmlPath = self.shotCacheXmlAn
        if os.path.exists(cacheXmlPath):
            self.xmlTree = ET.parse(cacheXmlPath)
            self.user = self.xmlTree.find('user').text
            self.date = self.xmlTree.find('date').text
            self.time = self.xmlTree.find('time').text
            self.stF = self.xmlTree.find('startFrame').text
            self.edF = self.xmlTree.find('endFrame').text
            cameraXMLNode = self.xmlTree.find('camera')
            camDict = cameraXMLNode.attrib
            self.cameraName = camDict["cameraName"]
            commsNode = self.xmlTree.find('comments')
            if commsNode == None:
                self.comments = ""
            else:
                self.comments = commsNode.text
            self.invisObjs = []
            statVisXml = self.xmlTree.find('staticInvisData')
            for node in statVisXml.getchildren():
                self.invisObjs.append(node.tag)
            self.dynVisXMLNodes = []
            dynVisXml = self.xmlTree.find('dynamicVisData')
            for node in dynVisXml.getchildren():
                self.dynVisXMLNodes.append(node)
            self.cameraXMLNodes = []
            for node in cameraXMLNode.getchildren():
                self.cameraXMLNodes.append(node)
            self.assets = {}
            getAssetXml = self.xmlTree.find('assets')
            for node in getAssetXml.getchildren():
                self.assets[node.tag] = node.attrib
                if node.attrib["assettype"] == 'char':
                    self.characters.append(node.tag)
                elif node.attrib["assettype"] == 'prop':
                    self.props.append(node.tag)
                elif node.attrib["assettype"] == 'sets':
                    self.sets.append(node.tag)
                elif node.attrib["assettype"] == 'elms':
                    self.elms.append(node.tag)
            return True
        else:
            utils.msgWin("Error", "XML file does not exist : %s"%cacheXmlPath, self.silent)
            return False
                    
    def writeXML(self, cacheXmlPath = None):
        if self.checkExportErrors(self.silent):
            return False
        if not cacheXmlPath:
            cacheXmlPath = self.shotCacheXmlAn
        xmlRoot = ET.Element(self.fileName)
        assetRefs = self.mayaShot.refNodes
        self.commonData(xmlRoot)
        assets = ET.SubElement(xmlRoot,'assets')
        self.createAssetsXML(assetRefs, assets)
        self.msg += '\nScene Asset Info exported'
        tree = ET.ElementTree(xmlRoot)
        tree.write(cacheXmlPath)
#         cleanLog = self.cleanCacheFolder("anim")
#         if cleanLog: self.msg += "\n\n%s"%cleanLog
        self.msg += '\n\nXML created successfully'
        utils.msgWin("Export Successful", "Scene file successfully cached\n%s"%self.msg, self.silent)
        self.msg = "\n"
        return True
    
    def updateXML(self, assetRefs = []):
        if self.checkExportErrors(self.silent):
            return False
        cacheXmlPath = self.shotCacheXmlAn
        xmlRead = self.readXML()
        if not xmlRead:
            return False
        xmlRefs = self.assets.keys()
        scnRefs = self.mayaShot.refNodes
        newRefs = list(set(scnRefs).difference(set(xmlRefs)))
        cchRefs = list(set(newRefs).union(set(assetRefs)))
        remRefs = list(set(xmlRefs).difference(set(scnRefs)))
        staticRefs = list(set(xmlRefs).difference(set(cchRefs).union(set(remRefs))))
        xmlRoot = ET.Element(self.fileName)
        self.commonData(xmlRoot)
        assets = ET.SubElement(xmlRoot,'assets')
        self.createAssetsXML(cchRefs, assets)
        for ref in staticRefs:
            refDict = self.assets[ref]
            asset = ET.SubElement(assets, ref, assettype = refDict["assettype"], name = refDict["name"], namespace = refDict["namespace"], date = refDict["date"], time = refDict["time"], path = refDict["path"]) #@UnusedVariable
        self.msg += '\nScene Asset Info exported'
        tree = ET.ElementTree(xmlRoot)
        tree.write(cacheXmlPath)
        cleanLog = self.cleanCacheFolder("anim")
        if cleanLog: self.msg += "\n\n%s"%cleanLog
        self.msg += '\n\nXML updated successfully'
        utils.msgWin("Export Successful", "Scene info successfully exported\n%s"%self.msg, self.silent)
        self.msg = "\n"
        return True
    
    def createAssetsXML(self, assetRefs, assetElm):
        now = datetime.datetime.now()
        self.msg += "\n"
        for ref in assetRefs:
            ast = MayaAsset(ref)
            assetName = ast.topGrp.split(":")[-1]
            astDate='%s-%s-%s' % (now.day,now.month,now.year)
            astTime ='%s:%s:%s' % (now.hour,now.minute,now.second)
            asset = ET.SubElement(assetElm, ref, assettype = ast.assetType, name = assetName, namespace = ast.namespace, date = astDate, time = astTime, path = ast.assetPath) #@UnusedVariable
            ast.exportAssetCache(self.shotCacheFldr)
            self.msg += "%s cache exported \n"%ast.namespace
    
    def cleanCacheFolder(self, typ = "anim"):
        cacheFldrs, curFldrs, cleanLog = [], [], []
        cacheFolder = self.mayaShot.getCacheFldr(typ)
        subFldrs = ["char", "prop", "sets", "elms"]
        for fldr in subFldrs:
            curAstTypeFldr = os.path.join(cacheFolder, fldr)
            if os.path.exists(curAstTypeFldr):
                curFldrPaths = [str(os.path.join(curAstTypeFldr, pth).replace("\\", "/")) for pth in os.listdir(curAstTypeFldr)]
                curFldrs.extend(curFldrPaths)
        mayaShot = MayaShot()
        if not mayaShot.validShot:
            return "Error getting shot info to remove redundant cache folders"
        scnRefs = mayaShot.refNodes
        for ref in scnRefs:
            if not mc.objExists(ref):
                continue
            ast = MayaAsset(ref)
            astCacheFldr = ast.getAstCacheFldr(self.shotCacheFldr, typ)
            cacheFldrs.append(str(astCacheFldr.replace("\\", "/")))
        fldrs2del = list(set(curFldrs).difference(set(cacheFldrs)))
        for fldr in fldrs2del:
            try:
                shutil.rmtree(fldr)
                utils.msgWin("Message", "Successfully removed redundant cache folder %s"%os.path.basename(fldr), True)
                cleanLog.append("Successfully removed redundant cache folder %s"%os.path.basename(fldr))
            except:
                utils.msgWin("Error", "Error removing redundant cache folder %s"%os.path.basename(fldr), True)
                cleanLog.append("Error removing redundant cache folder %s"%os.path.basename(fldr))
        if cleanLog:
            return "\n".join(cleanLog)
        return None
    
    def commonData(self, xmlRoot):
        user = ET.SubElement(xmlRoot,'user')
        user.text = os.environ['USERNAME']
        now = datetime.datetime.now()
        date = ET.SubElement(xmlRoot,'date')
        date.text = '%s-%s-%s' % (now.day,now.month,now.year)
        time = ET.SubElement(xmlRoot,'time')
        time.text = '%s:%s:%s' % (now.hour,now.minute,now.second)
        stF = mc.playbackOptions(q=1,ast=1)
        startFrame = ET.SubElement(xmlRoot,'startFrame')
        startFrame.text = '%d' % stF
        edF = mc.playbackOptions(q=1,aet=1)
        endFrame = ET.SubElement(xmlRoot,'endFrame')
        endFrame.text = '%d' % edF
        comments = ET.SubElement(xmlRoot,'comments')
        comments.text = self.comments
        statVis = ET.SubElement(xmlRoot,'staticInvisData')
        dynVis = ET.SubElement(xmlRoot,'dynamicVisData')
        self.writeObjVis(statVis, dynVis)
        self.msg += "Visibility Info exported\n"
        camera = self.mayaShot.getSceneCamera()
        cameraTmp = mc.rename(camera, "%s_TMP"%camera)
        cameraElement = ET.SubElement(xmlRoot,'camera', attrib = {'cameraName':camera})
        attrs = ['translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ', 'scaleX', 'scaleY', 'scaleZ']
        if mc.objExists(camera):
            mc.delete(camera)
        camLoc = mc.spaceLocator(name = camera)
        mc.parentConstraint(cameraTmp, camLoc,mo = 0)
        mc.scaleConstraint(cameraTmp, camLoc, mo = 0)
        mc.bakeResults(camLoc,at=attrs,sm=1,t=(stF,edF),sr=1,dic=1,pok=0,sac=0,ral=0,bol=0)
        utils.writeAnimXML(camera, cameraElement, attrs)
        mc.delete(camLoc)
        mc.rename(cameraTmp, camera)
        camShapes = mc.listRelatives(camera, s = True, c = True)
        for cam in camShapes:
            if "Shape" in cam:
                camShape = cam
                break
        if camShape:
            utils.writeAnimXML(camShape, cameraElement)
        self.msg += "Camera exported\n\n"
        
    def writeObjVis(self, statVis, dynVis):
        dynVisObject, staticVisObj, ast2BakeAttrs, attrTmpLocs = [], [], [], [] 
        assetRefs = self.mayaShot.refNodes
        for ref in assetRefs:
            ast = MayaAsset(ref)
            astGeoBake, astGeoInvis = ast.getVisGeo()
            dynVisObject.extend(astGeoBake)
            staticVisObj.extend(astGeoInvis)

        stF = mc.playbackOptions(q=1,ast=1)
        edF = mc.playbackOptions(q=1,aet=1)
        for obj in dynVisObject:
            if mc.objExists((obj + "_TMPLOC")):
                mc.delete((obj + "_TMPLOC"))
            mc.spaceLocator(name = (obj + "_TMPLOC"))
            attrTmpLocs.append((obj + "_TMPLOC"))
            mc.connectAttr((obj + ".v"), (obj + "_TMPLOC.v"), f = True)
            ast2BakeAttrs.append((obj + "_TMPLOC.v"))
        ast2BakeAttrs = list(set(ast2BakeAttrs))
        if ast2BakeAttrs:
            mc.bakeResults(ast2BakeAttrs,at=['v'],sm=1,t=(stF,edF),sr=1,dic=1,pok=0,sac=0,ral=0,bol=0)
            for bkAst in ast2BakeAttrs:
                conns = mc.listConnections(bkAst, d=0, s=1)
                if mc.nodeType(conns[0]) == "animCurveTU":
                    if utils.chkStaticCurve(conns[0]):
                        objName = bkAst.split("_TMPLOC.v")[0]
                        dynVisObject.pop(dynVisObject.index(objName))
                        if not mc.getAttr("%s.v"%objName):
                            staticVisObj.append(objName)
                    else:
                        mc.keyTangent(bkAst, itt = 'step', ott = 'step')
        for statV in staticVisObj:
            objDotName = statV.replace(":", ".") if ":" in statV else statV
            ET.SubElement(statVis, objDotName)
        for dynV in dynVisObject:
            utils.writeAnimXML("%s_TMPLOC"%dynV, dynVis, ["visibility"], dynV)
        for tmpLoc in attrTmpLocs:
            try:
                mc.delete(tmpLoc)
            except:
                pass

        self.msg += "Visibility baked for all geometry\n"
    
class ProjectInfo:
    def __init__(self, silent = True):
        self.validProject = True
        self.silent = silent
        self.mapDrive, self.configXML, self.projShort, self.astNameConv, self.astFdrConv = None, None, None, None, None
        self.resWidth, self.resHeight, self.aspectRatio, self.stereo = 1920, 1080, 1.778, False
        self.epOrSeq, self.epsqNums, self.timeUnit, self.cameraType = "ep", 10, "pal", "normal"
        self.pipelineType, self.mayaVer, self.mayaExt = "cache", 2013, "ma"
        self.charPb = "assets/publish/char"
        self.propPb = "assets/publish/prop"
        self.bgPb = "assets/publish/sets"
        self.soundFldr = "inputs/audio"
        self.breakDown = "inputs/breakdownlist"
        self.durationLst = "inputs/breakdownlist/durationlist"
        self.pubFldr = "assets/publish"
        self.modelFldr = "workspace/model"
        self.modelFinl = "assets/model"
        self.texFldr = "workspace/texture"
        self.texFinl = "assets/texture"
        self.rigFldr = "workspace/rig"
        self.rigFinl = "assets/rig"
        self.chfAstFldr = "workspace/chfasset"
        self.chfAstFinl = "assets/chfasset"
        self.stageFldr = "workspace/staging"
        self.stageFinl = "scenes/staging"
        self.animFldr = "workspace/animation"
        self.animFinl = "scenes/animation"
        self.lightFldr = "workspace/lighting"
        self.lightFinl = "scenes/lighting"
        self.fxFldr = "workspace/fx"
        self.fxFinl = "scenes/fx"
        self.chfFldr = "workspace/chf"
        self.chfFinl = "scenes/chf"
        self.compInput = "renderScenes"
        self.compFldr = "workspace/compositing"
        self.compFinl = "output"
        currProj = None
        if mc.optionVar(ex = 'currentProject'):
            currProj = mc.optionVar(q = 'currentProject')
        else:
            self.validProject = False
            return
        projTree = ET.parse(projectPathsXml)
        projRoot = projTree.getroot()
        for node in projRoot:
            getPathAttr = node.attrib
            if currProj:
                if getPathAttr['nam'] == currProj:
                    self.mapDrive = getPathAttr['path']
                    break
            else:
                self.mapDrive = getPathAttr['path']
                break
        if not (os.path.exists(self.mapDrive)) or not (os.path.exists(os.path.join(self.mapDrive, "/config.xml"))):
            utils.msgWin("Error", "Project drive/config file not accessible", self.silent)
            self.validProject = False
        else:
            self.configXML = os.path.join(self.mapDrive, "/config.xml")
            xmlTree = ET.parse(self.configXML)
            projShortElm = xmlTree.find('project-short')
            if not projShortElm == None: self.projShort = projShortElm.text
            epOrSeqElm = xmlTree.find('ep-or-seq')
            if not epOrSeqElm == None: self.epOrSeq = epOrSeqElm.text
            epsqNumsElm = xmlTree.find('episodes')
            if not epsqNumsElm == None: self.epsqNums = epsqNumsElm.text
            mayaExtElm = xmlTree.find('maya-ext')
            if not mayaExtElm == None: self.mayaExt = mayaExtElm.text
            astNmCnvElm = xmlTree.find('asset-naming')
            if not astNmCnvElm == None: 
                self.astNameConv = astNmCnvElm.text
            else:
                self.astNameConv = "%s~projShort~[0-9]{2}~epsqNum~_[a-z,A-Z]{2}[a-z,A-Z]*~astName~[0-9]{2}~astVer~(c|s|p)~astType~_[a-z]{2}~deptShort~[0-9]{2}~deptVer~_v[0-9]{3}~version~.ma~mayaExt"%self.projShort
                print "Falling back to default asset naming convention"
            astfdrnvElm = xmlTree.find('asset-naming')
            if not astfdrnvElm == None: 
                self.astFdrConv = astfdrnvElm.text
            else:
                self.astFdrConv = "%s~projShort~[0-9]{3}~epsqNum~_[a-z,A-Z]{2}[a-z,A-Z]*~astName~[0-9]{2}~astVer~(c|s|p)~astType~_(p|m|h)~astRes"%self.projShort
                print "Falling back to default asset folder convention"
            resWidthElm = xmlTree.find('resol-width')
            if not resWidthElm == None: self.resWidth = int(resWidthElm.text)
            resHeightElm = xmlTree.find('resol-height')
            if not resHeightElm == None: self.resHeight = int(resHeightElm.text)
            aspectRatioElm = xmlTree.find('aspRto')
            if not aspectRatioElm == None: self.aspectRatio = float(aspectRatioElm.text)
            timeUnitElm = xmlTree.find('time-unit')
            if not timeUnitElm == None: self.timeUnit = timeUnitElm.text
            cameraTypeElm = xmlTree.find('camera-type')
            if not cameraTypeElm == None: 
                self.cameraType = cameraTypeElm.text
                self.stereo = True if self.cameraType == "stereo" else False
            pipeTypeElm = xmlTree.find('pipeline-type')
            if not pipeTypeElm == None: self.pipelineType = pipeTypeElm.text
            soundFldrElm = xmlTree.find("sound-folder")
            if not soundFldrElm == None: self.soundFldr = soundFldrElm.text
            mayaVerElm = xmlTree.find('maya-ver')
            if not mayaVerElm == None: self.mayaVer = mayaVerElm.text
            pubFldrElm = xmlTree.find('pub-folder')
            if not pubFldrElm == None: self.pubFldr = pubFldrElm.text
            charPbElm = xmlTree.find('char-folder')
            if not charPbElm == None: self.charPb = charPbElm.text
            propPbElm = xmlTree.find('prop-folder')
            if not propPbElm == None: self.propPb = propPbElm.text
            bgPbElm = xmlTree.find('bg-folder')
            if not bgPbElm == None: self.bgPb = bgPbElm.text
            soundFldrElm = xmlTree.find('sound-folder')
            if not soundFldrElm == None: self.soundFldr = soundFldrElm.text
            breakDownElm = xmlTree.find('breakdown-folder')
            if not breakDownElm == None: self.breakDown = breakDownElm.text
            durationLstElm = xmlTree.find('durationlist-folder')
            if not durationLstElm == None: self.durationLst = durationLstElm.text
            modelFldrElm = xmlTree.find('model-folder')
            if not modelFldrElm == None: self.modelFldr = modelFldrElm.text
            modelFinlElm = xmlTree.find('model-final')
            if not modelFinlElm == None: self.modelFinl = modelFinlElm.text
            texFldrElm = xmlTree.find('texture-folder')
            if not texFldrElm == None: self.texFldr = texFldrElm.text
            texFinlElm = xmlTree.find('texture-final')
            if not texFinlElm == None: self.texFinl = texFinlElm.text
            rigFldrElm = xmlTree.find('rig-folder')
            if not rigFldrElm == None: self.rigFldr = rigFldrElm.text
            rigFinlElm = xmlTree.find('rig-final')
            if not rigFinlElm == None: self.rigFinl = rigFinlElm.text
            chfAstFldrElm = xmlTree.find('chfasset-folder')
            if not chfAstFldrElm == None: self.chfAstFldr = chfAstFldrElm.text
            chfAstFinlElm = xmlTree.find('chfasset-final')
            if not chfAstFinlElm == None: self.chfAstFinl = chfAstFinlElm.text
            stageFldrElm = xmlTree.find('staging-folder')
            if not stageFldrElm == None: self.stageFldr = stageFldrElm.text
            stageFinlElm = xmlTree.find('staging-final')
            if not stageFinlElm == None: self.stageFinl = stageFinlElm.text
            blockFldrElm = xmlTree.find('blocking-folder')
            if not blockFldrElm == None: self.blockFldr = blockFldrElm.text
            blockingFinlElm = xmlTree.find('blocking-final')
            if not blockingFinlElm == None: self.blockingFinl = blockingFinlElm.text
            animFldrElm = xmlTree.find('anim-folder')
            if not animFldrElm == None: self.animFldr = animFldrElm.text
            animFinlElm = xmlTree.find('anim-final')
            if not animFinlElm == None: self.animFinl = animFinlElm.text
            lightFldrElm = xmlTree.find('light-folder')
            if not lightFldrElm == None: self.lightFldr = lightFldrElm.text
            lightFinlElm = xmlTree.find('light-final')
            if not lightFinlElm == None: self.lightFinl = lightFinlElm.text
            fxFldrElm = xmlTree.find('fx-folder')
            if not fxFldrElm == None: self.fxFldr = fxFldrElm.text
            fxFinlElm = xmlTree.find('fx-final')
            if not fxFinlElm == None: self.fxFinl = fxFinlElm.text
            chfFldrElm = xmlTree.find('chf-folder')
            if not chfFldrElm == None: self.chfFldr = chfFldrElm.text
            chfFinlElm = xmlTree.find('chf-final')
            if not chfFinlElm == None: self.chfFinl = chfFinlElm.text
            compInputElm = xmlTree.find('comp-input')
            if not compInputElm == None: self.compInput = compInputElm.text
            compFldrElm = xmlTree.find('comp-folder')
            if not compFldrElm == None: self.compFldr = compFldrElm.text
            compFinlElm = xmlTree.find('comp-final')
            if not compFinlElm == None: self.compFinl = compFinlElm.text