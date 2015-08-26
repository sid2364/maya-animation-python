'''
Created on Apr 21, 2014

@author: suneeth
'''

import os, re, shutil, datetime, socket
import maya.cmds as mc
import maya.mel as mel
import pipeClasses as ppc
import lib.xlrd as xlrd
import maya.OpenMaya as om
import xml.etree.ElementTree as ET

drvPathDict = {"i":"//192.168.3.232/SkullCoastRum"}
camPath = "//192.168.3.250/scripts$/tonPipe/cams"

def msgWin(title = 'test', msg = 'This is a test message??', silent = False):
    if silent== "disabled":
        pass
    elif silent == True:
        print msg
    else:
        mc.confirmDialog(title = title, message = msg, button = ['OK'], defaultButton = 'OK', cancelButton = 'OK', dismissString = 'OK')

class analyseFileName:
    """Class Variables : "projShort", "epsq", "epsqNum", "shot", "deptShort", "deptVer", "ver", "ext" """
    def __init__(self, fileName):
        self.validShot = True
        if "/" in fileName:
            fileName = fileName.split("/")[-1]
        if "\\" in fileName:
            fileName = fileName.split("\\")[-1]
        self.fileName = fileName
#         self.pattern = '^[a-z]{3}_(ep|sq)[0-9]{3}sh[0-9]{3}([a-z]{1})?_[a-z]{2}([0-9]{2})_v[0-9]{2}.*[.](ma|mb)$'
        self.pattern = '^[a-z]{3}[0-9]{2}_(ep|sq)[0-9]{3}_sh[0-9]{3}([a-z]{1})?_[a-z]{2}([0-9]{2})_v[0-9]{2}.*[.](ma|mb)$'
        matchObj = re.match(self.pattern, fileName)
        if matchObj:
            verPattern = '_v[0-9]{2}.'
            self.verObj = re.search(verPattern, fileName)
            if self.verObj:
                self.ver = self.verObj.group(0)[-3:-1]
            else:
                self.validShot = False  
            eqshPattern = '_(ep|sq)[0-9]{3}_sh[0-9]{3}([a-z]{1})?_'
            self.eqshObj = re.search(eqshPattern, fileName)
            if self.eqshObj:
                eqshStr = self.eqshObj.group(0)
                self.epsq = eqshStr[1:3]
                self.epsqNum = eqshStr[3:6]
                self.shot = eqshStr[9:-1]
            else:
                self.validShot = False
            deptPattern = '_[a-z]{2}([0-9]{2})_'
            self.deptObj = re.search(deptPattern, fileName)
            if self.deptObj:
                deptStr = self.deptObj.group(0)
                self.deptShort = deptStr[1:3]
                self.deptVer = deptStr[-3:-1]
            else:
                self.validShot = False
            projPattern = '[a-z]{3}[0-9]{2}_'
            self.projObj = re.search(projPattern, fileName)
            if self.projObj: 
                self.projShort = self.projObj.group(0)[:-3]
            else:
                self.validShot = False
            extStr = fileName.split(".")
            if len(extStr) > 1:
                self.ext = extStr[-1]
            else:
                self.validShot = False
        else:
            self.validShot = False
            
    def replaceString(self, replaceDict):
        """replaceDict={"ver":"00","epsq":"sq","epsqNum":"001","shot":"001","deptShort":"st","deptVer":"01","projShort":"ccy"}"""        
        newName = self.fileName
        validName = True
        for strType in replaceDict.keys():
            replaceStr = replaceDict[strType]
            if strType == "ext":
                if "." in newName:
                    fSplit = newName.split(".")
                    newName = "%s.%s" % (fSplit[0], replaceStr)
                else:
                    validName = False            
            if strType == "ver":
                if len(self.ver) == len(replaceStr):
                    newMatch = self.verObj.group(0).replace(self.ver, replaceStr)
                    newName = newName.replace(self.verObj.group(0), newMatch)
                else:
                    validName = False
            if strType == "epsq" or strType == "epsqNum" or strType == "shot":
                curMatch = self.eqshObj.group(0)
                if strType == "epsq":
                    if len(self.epsq) == len(replaceStr):
                        newMatch = curMatch[0] + replaceStr + curMatch[3:]
                        newName = newName.replace(curMatch, newMatch)
                    else:
                        validName = False
                elif strType == "epsqNum":
                    if len(self.epsqNum) == len(replaceStr):
                        newMatch = curMatch[:3] + replaceStr + curMatch[6:]
                        newName = newName.replace(curMatch, newMatch)
                    else:
                        validName = False
                else: #strType == "shot":
                    if len(self.shot) == len(replaceStr):
                        newMatch = curMatch[:9] + replaceStr + curMatch[12:]
                        newName = newName.replace(curMatch, newMatch)
                    else:
                        validName = False
            if strType == "deptShort" or strType == "deptVer":
                curMatch = self.deptObj.group(0)
                if strType == "deptShort":
                    if len(self.deptShort) == len(replaceStr):
                        newMatch = curMatch[0] + replaceStr + curMatch[3:]
                        newName = newName.replace(curMatch, newMatch)
                    else:
                        validName = False
                else: #strType == "deptVer"
                    if len(self.deptVer) == len(replaceStr):
                        newMatch = curMatch[:3] + replaceStr + curMatch[5:]
                        newName = newName.replace(curMatch, newMatch)
                    else:
                        validName = False
            if strType == "projShort":
                curMatch = self.projObj.group(0)
                if len(self.projShort) == len(replaceStr):
                    newMatch = replaceStr + curMatch[3:]
                    newName = newName.replace(curMatch, newMatch)
                else:
                    validName = False
        if self.validShot and validName:
            return newName
        else:
            return None

def loadGeoVisXML(xmlPath):
    errorLog = []
    xmlTree = ET.parse(xmlPath)
    dynVisXml = xmlTree.find('dynamicVisData')
    for node in dynVisXml.getchildren():
        errorLog.extend(loadAnimXML(xmlTree, node))
    return errorLog

def loadAnimXML(xmlTree, ctrl, targRes = "texture", obj = None):
    errorLog = []
    ctrlObjColon = ctrl.tag.replace(".", ":")
    ctrlObj = convertName(ctrlObjColon, targRes)
    objName = obj if obj else ctrlObj
    if not mc.objExists(objName):
        errorLog.append("Object does not exist : %s"%objName)
    else:
        for attr in ctrl.getchildren():
            ctrlAttrib = attr.tag
            curAttr = '%s.%s'%(objName, ctrlAttrib)
            try:
                mc.getAttr(curAttr, l = 1)
            except:
                errorLog.append("Attribute missing : %s"%curAttr)
                continue
            animType = attr.attrib['Type']
            if animType == 'static':
                attrValue = attr.attrib['valueStatic']
                if attrValue == "True":
                    attrValue = True
                elif attrValue == "False":
                    attrValue = False
                else:
                    attrValue = float(attrValue)
                mc.setAttr(curAttr, attrValue)
            elif animType == 'anim':
                attrBd      = attr.attrib['breakDown']
                attrPreIn   = attr.attrib['preInfinity']
                attrPosIn   = attr.attrib['postInfinity']
                attrWeight  = attr.attrib['weightedTangents']
                breakDn     = False
                for key in  attr.getchildren():
                    keytim  = key.tag
                    time    = keytim.split('key')[1]
                    inAng   = key.attrib['inAngle'] 
                    outAng  = key.attrib['outAngle']
                    inTan   = key.attrib['inTangent']
                    outTan  = key.attrib['outTangent']
                    inWei   = float(key.attrib['inWeight'])
                    outWei  = float(key.attrib['outWeight'])
                    tanLok  = key.attrib['tanLock']
                    weiLok  = key.attrib['weightLock']
                    keyVal  = key.attrib['valueChange']
                    breakDn = False
                    bd_itm  = str(attrBd)
                    if bd_itm != 'None':
                        breakDn = True
                    mc.setKeyframe(curAttr, time = time, value = float(keyVal), bd = breakDn)
                    mc.keyTangent(curAttr, lock = bool(tanLok), t = (time,time))
                    if attrWeight == 'True':
                        try:
                            mc.keyTangent(curAttr, t = (time,time), weightLock = weiLok)
                        except:
                            pass
                    if inTan != "fixed" and outTan != "fixed":
                        mc.keyTangent(curAttr, e = 1, a = 1, t = (time,time), itt = inTan, ott = outTan)
                    if inTan == "fixed" and outTan != "fixed":
                        mc.keyTangent(curAttr, e = 1, a = 1, t = (time,time), inAngle = inAng, inWeight = inWei, itt = inTan, ott = outTan) 
                    if inTan != "fixed" and outTan == "fixed":
                        mc.keyTangent(curAttr, e = 1, a = 1, t = (time,time), outAngle = outAng, inWeight = inWei, itt = inTan, ott = outTan)
                    if inTan == "fixed" and outTan == "fixed":
                        mc.keyTangent(curAttr, e = 1, a = 1, t = (time,time), inAngle = inAng, inWeight = inWei, outAngle = outAng, outWeight = outWei, itt = inTan, ott = outTan)
                mc.setInfinity(curAttr, poi = attrPosIn, pri = attrPreIn)
    return errorLog

def writeAnimXML(obj, elmRoot, attrs = [], saveName = None):
    if saveName:
        objDotName = saveName.replace(':', '.') if ":" in obj else obj
    else:
        objDotName = obj.replace(':', '.') if ":" in obj else obj
    allChannels = []
    if attrs:
        allChannels.extend(attrs)
    else:
        if mc.listAttr(obj, k = 1): allChannels.extend(mc.listAttr(obj, k = 1, v = 1))
        if mc.listAttr(obj, cb = 1): allChannels.extend(mc.listAttr(obj, cb = 1))
    if allChannels:
        root = ET.SubElement(elmRoot, objDotName)
        for channel in allChannels:
            animKey = mc.listConnections('%s.%s' % (obj, channel), type = 'animCurve', d = 0)
            if animKey:
                animValues = ET.SubElement(root, channel, Type = 'anim')
                for each in ['preInfinity', 'postInfinity', 'weightedTangents']:
                    animValues.attrib['%s' % each] = str(mc.getAttr('%s.%s'% (animKey[0], each)))
                tmpKeyVal = mc.keyframe(animKey[0], q = 1)
                tmpVCVal = mc.keyframe(animKey[0], q = 1, vc = 1)
                animValues.attrib['breakDown'] = str(mc.keyframe(animKey[0], q = 1, bd = 1))
                inTan = mc.keyTangent(animKey[0], q = 1, itt = 1)
                outTan = mc.keyTangent(animKey[0], q = 1, ott = 1) 
                tanLock = mc.keyTangent(animKey[0], q = 1, lock = 1)
                weightLock = mc.keyTangent(animKey[0], q = 1, weightLock = 1)
                inAngle = mc.keyTangent(animKey[0], q = 1, inAngle = 1)
                outAngle = mc.keyTangent(animKey[0], q = 1, outAngle = 1)
                inWeight = mc.keyTangent(animKey[0], q = 1, inWeight = 1)
                outWeight = mc.keyTangent(animKey[0], q = 1, outWeight = 1)
                for i in range (len(tmpKeyVal)):
                    ET.SubElement(animValues, 'key%s'%(tmpKeyVal[i]), valueChange = str(tmpVCVal[i]), inTangent = str(inTan[i]), outTangent = str(outTan[i]), tanLock = str(tanLock[i]), weightLock = str(weightLock[i]), inAngle = str(inAngle[i]), outAngle = str(outAngle[i]), inWeight = str(inWeight[i]), outWeight = str(outWeight[i]))
            else:
                channelValue = None
                try:
                    channelAttrVal = mc.getAttr('%s.%s'% (obj, channel))
                    channelValue = str(channelAttrVal)
                except:
                    continue
                if channelValue:
                    attrValues = ET.SubElement(root, channel, Type = 'static')
                    attrValues.attrib['valueStatic'] = channelValue

def importAudio(silent = False):
    mayaShot = ppc.MayaShot()
    if not mayaShot.validShot:
        msgWin("Error", "Invalid Shot or Project", silent)
        return False
    audioNodes = mc.ls(typ = "audio")
    if audioNodes:
        for aud in audioNodes:
            mc.delete(aud)
    audFilePath = os.path.join((mayaShot.projInfo.mapDrive + "/"), mayaShot.projInfo.soundFldr, mayaShot.epSqName, "sc-%s.wav"%mayaShot.shot)
    if os.path.exists(audFilePath):
        audnode = mc.sound(file = audFilePath, offset = 101, n = "%s%s_aud"%(mayaShot.epSqName, mayaShot.shName))
        setAudio = 'global string $gPlayBackSlider; timeControl -e -ds 1 -s "%s" $gPlayBackSlider;' % audnode
        mel.eval("%s" % setAudio)
        msgWin("Message", "Successfully imported audio : %s"%audFilePath, silent)
        return True
    else:
        msgWin("Error", "Audio file does not exist : %s"%audFilePath, silent)
        return False

def sceneCleanup(silent = True):
    mc.displayColor('headsUpDisplayLabels', 16, dormant=True)
    namespaces = mc.namespaceInfo(lon = True)
    if "Suleiman00s_pr01" in namespaces:
        mc.namespace(ren = ("Suleiman00s_pr01", "Suleiman00p_pr01"), f = True)
    mayaShot = ppc.MayaShot()
    if not mayaShot.validShot:
        msgWin("Error", "Invalid Shot or Project", silent)
        return False
    epsq = mayaShot.epSqName
    shot = mayaShot.shName
    stereoCams = []
    mc.setAttr("defaultResolution.width", mayaShot.projInfo.resWidth)
    mc.setAttr("defaultResolution.height", mayaShot.projInfo.resHeight)
    mc.setAttr("defaultResolution.deviceAspectRatio", mayaShot.projInfo.aspectRatio)
    camPattern = "(ep|sq)[0-9]{3}sh[0-9]{3}([a-b]{1})?_camCt"
    camName = "%s%s_camCt" % (epsq, shot)
    scCams = mc.ls(type = "camera")
    renCams = []
    for cam in scCams:
        camTr = mc.listRelatives(cam, p = True)
        pMatch = re.search(camPattern, camTr[0])
        if pMatch:
            renCams.append(camTr[0])
    if not renCams:
        msgWin("Error", "Couldn't find a valid camera", silent)
        return False
    if len(renCams) > 1:
        msgWin("Error", "Too many cameras in the scene.\nPlease delete unwanted cameras", silent)
        return False
    if not renCams[0] == camName:
        mc.rename(renCams[0], camName)
    if mayaShot.projInfo.stereo:
        stereoCams = mc.listRelatives(camName, c = 1, typ = 'transform')
        for stCam in stereoCams:
            nodeTyp = mc.nodeType(stCam, i = True)
            if "constraint" in nodeTyp:
                continue
            if mc.getAttr(stCam + ".tx") < 0:
                mc.rename(stCam, camName.replace("_camCt", "_camLt"))
            else:
                mc.rename(stCam, camName.replace("_camCt", "_camRt"))
        camShape = "%sCenterCamShape" % camName
    else:
        camShape = "%sShape" % camName
    camShps = mc.listRelatives(camName, c = True, s = True)
    for shp in camShps:
        sMatch = re.search(camPattern, shp)
        if sMatch:
            mc.rename(shp, shp.replace(sMatch.group(0), camName))
        else:
            print "Unable to find correct name for %s" % shp
    camParent = mc.listRelatives(camName, p = True)
    if camParent:
        camParent = camParent[0]
    if not camParent in ["CAM", "Aim_camera", "Ctl_Camera", "camera_group"]:
        if not mc.objExists("CAM"):
            mc.group(n = "CAM", em = True)
        try:
            mc.parent(camName, "CAM")
        except:
            pass
    camTopGrp = mc.listRelatives("CAM", p = True)
    if not camTopGrp == "CAMERAS":
        if not mc.objExists("CAMERAS"):
            mc.group(n = "CAMERAS", em = True)
        try:
            mc.parent("CAM", "CAMERAS")
        except:
            pass
    huds = ["HUDShotName", "HUDUserName", "HUDfocalLength", "HUDFrameNo"]
    for hud in huds:
        if mc.headsUpDisplay(hud, ex = True):
            mc.headsUpDisplay(hud, rem = True)
    focLen = mc.getAttr("%s.focalLength" % camShape)
    mc.headsUpDisplay('HUDfocalLength', s = 5, b = 1, bs = 'small', l = 'focalLength: %s' % focLen, lfs = 'large')
    mc.headsUpDisplay('HUDShotName', s = 6, b = 1, bs = 'small', l = 'shot: %s%s' % (epsq, shot), lfs = 'large')
    #username = os.environ['USERNAME']
    #mc.headsUpDisplay('HUDUserName', s = 7, b = 1, bs = 'small', l = 'user: %s' % username, lfs = 'large')
    mc.headsUpDisplay('HUDFrameNo', s = 8, b = 1, bs = 'small', l = 'frame: ', lfs = 'large', c = 'import maya.cmds as mc; mc.currentTime(q = True)', atr = True)
    scnCameras = [camName]
    if stereoCams: scnCameras.extend(mc.listRelatives(camName, c = 1, typ = 'transform'))
    for scnCam in scnCameras:
        mc.camera(scnCam, e = 1, dfg = 0, dgm = 1, dr = 1, ovr = 1.1)
        if mayaShot.projInfo.stereo and scnCam.endswith("_camCt"):
            scnCam = scnCam + "CenterCam"
        mc.setAttr('%sShape.displayGateMaskOpacity' % scnCam, l = 0)
        mc.setAttr('%sShape.displayGateMaskOpacity' % scnCam, 1)
        mc.setAttr ('%sShape.displayGateMaskColor' % scnCam, l = 0)
        mc.setAttr ('%sShape.displayGateMaskColor' % scnCam, 0, 0, 0)
    if mc.objExists('hudFix_node'):
        mc.delete('hudFix_node')
    mayaShot.moveAssetsToGrps()
    shotFrames = mayaShot.frames
    mc.playbackOptions(min=101, max=100+int(shotFrames), ast=101, aet=100+int(shotFrames))
    om.MGlobal.displayInfo("Scene cleaned up.")
    
def replaceCam():
    main_win = 'replaceCamWin'
    if mc.window (main_win, exists = 1): mc.deleteUI (main_win)
    if mc.windowPref (main_win, exists = 1): mc.windowPref (main_win, remove = 1)
    win = mc.loadUI(f = '//192.168.3.250/scripts$/toonzPipe/mayaPipe/replaceCamWin.ui')
    mc.window(win, e = 1, tlc = [350,350])
    mc.showWindow(win)
    mc.button('btn_importCam', e = 1, c = lambda event: importCam())
    
def importCam():
    epsq = "sq000"
    shot = "sh000"
    stereo = False
    sel_cam = mc.optionMenu('cmb_camList',q=1,v=1)
    typ = sel_cam[-1]
    mayaShot = ppc.MayaShot()
    if not mayaShot.validShot:
        msgWin("Error", "Invalid Shot or Project", True)
    else:
        epsq = mayaShot.epSqName
        shot = mayaShot.shName
        stereo = mayaShot.projInfo.stereo
    importCamera(epsq, shot, stereo, typ)

def importCamera(epsq, shot, stereo = False, typ = "A"):
    """ epsq = "sq001", shot = "sh001" """    
    if mc.objExists('CAMERAS'):
        mc.delete('CAMERAS')
    camNames = ["camCt", "camLt", "camRt"]
    if stereo:
        camFileName = "cam%s.ma" % typ
        camNodes = ["stereoCamera", "stereoCameraLeft", "stereoCameraRight"]
    else:
        camFileName = "cam%s.ma" % (typ * 2)
        camNodes = ["normalCamera"]
    camFilePath = os.path.join(camPath, camFileName)
    mc.file(camFilePath, i = True, gr = True, gn = 'CAMERAS')
    camName = "%s%s" % (epsq, shot)
    for i in range(len(camNodes)):
        try:
            mc.rename(camNodes[i], "%s_%s" % (camName, camNames[i]))
        except:
            print "Unable to rename %s to %s" % (camNodes[i], "%s_%s" % (camName, camNames[i]))
            continue

def setStaticAttr():
    selObj = mc.ls(sl = 1, l = 1)
    if selObj:
        targ = selObj[0]
        if "|" in targ:
            targName = targ.split("|")[-1]
        else:
            targName = targ
        if not targName == "GEO":
            msgWin("Warning", "Please Select 'GEO' group", False)
            return
    else:
        msgWin("Warning", "Nothing selected", False)
        return
    if not mc.listAttr(targ, st = "Static"):
        mc.addAttr(targ, ln = "Static", at = "bool", k = 1)
    mc.setAttr("%s.Static"%targ, 1)

def getXLShots(excelPath):
    xlShots = {}
    wb = None
    try:
        wb = xlrd.open_workbook(excelPath)
    except:
        return {}
    sh = wb.sheet_by_index(0)
    for rownum in range(1, sh.nrows):
        curRow = sh.row_values(rownum)
        xlShotRowTxt = str(curRow[0])
        expr1 = "([0-9]{1})?([0-9]{1})?[0-9]{1}([a-z]{1})?"
        expr2 = "([0-9]{1})?([0-9]{1})?[0-9]{1}"
        expr3 = "[a-z]{1}"
        if re.search(expr1, xlShotRowTxt):
            numPart = re.search(expr2, xlShotRowTxt)
            xlShot = str(numPart.group(0)).zfill(3)
            alpPart = re.search(expr3, xlShotRowTxt)
            xlShot = xlShot + alpPart.group(0) if alpPart else xlShot
        else:
            continue
        xlShots[xlShot] = curRow
    return xlShots

def isNumber(txt):
    try:
        float(txt)
        return True
    except:
        return False
            
def getXLShotDetails(excelPath, shot):
    xlShotDict = {}
    xlShots = getXLShots(excelPath)
    if shot in xlShots.keys():
        shotRow = xlShots[shot]
        xlShotDict["char"] = [str(c) for c in shotRow[1].split('\n')] if shotRow[1] else []
        xlShotDict["prop"] = [str(p) for p in shotRow[2].split('\n')] if shotRow[2] else []
        xlShotDict["sets"] = [str(s) for s in shotRow[3].split('\n')] if shotRow[3] else []
        xlShotDict["frames"] = int(shotRow[6])
        return xlShotDict
    else:
        msgWin("Error", "Error reading details for shot number %s from %s"%(shot, excelPath), True)
        return {}
    
def getActiveViewport(silent = True):
    viewport = mc.getPanel(wf = True)
    if not viewport:
        msgWin('Error', 'Couldn\'t get active viewport', silent)
        return False
    if not viewport.startswith('modelPanel'):
        try:
            viewport = [x for x in mc.getPanel(vis=True) if x.startswith('modelPanel')][0]
        except:
            msgWin('Error', 'Couldn\'t get active viewport', silent)
            return False
    return viewport
    
def takePlayblast(silent = True, custom = False, customPath = None):
    renWidth = mc.getAttr("defaultResolution.width")
    renHeight = mc.getAttr("defaultResolution.height")
    aspRatio = renWidth/float(renHeight)
    width = renWidth/2 if renWidth > 960 else renWidth
    height = renHeight/2 if renWidth > 960 else renHeight
    mayaShot = ppc.MayaShot()
    if not mayaShot.validShot:
        msgWin("Warning", "Invalid Shot or Project", True)
        if not custom:
            return False
        else:
            viewport = getActiveViewport(silent)
            if not viewport: return False
            mc.setFocus(viewport)
            scCam = mc.modelPanel(viewport, q = True, cam = True)
            scCamSshp = mc.listRelatives(scCam, c = 1, s = 1, ni = 1)
            stereo = True if mc.nodeType(scCamSshp == "stereoRigCamera") else False
            soundName = "NoIdea"
    else:
        if round(aspRatio, 2) ==  1.78:
            width = 960
            height = 540
        else:
            width = mayaShot.projInfo.resWidth/2 if mayaShot.projInfo.resWidth > 1280 else mayaShot.projInfo.resWidth
            height = mayaShot.projInfo.resHeight/2 if mayaShot.projInfo.resWidth > 1280 else mayaShot.projInfo.resHeight
        soundName = "%s%s_aud"%(mayaShot.epSqName, mayaShot.shName)
        scCam = mayaShot.getSceneCamera(False)
        stereo = mayaShot.projInfo.stereo
        sceneCleanup(True)
    if not scCam or not mc.objExists(scCam):
        msgWin('Error', "Couldn't find a valid camera in the scene", silent)
        return False
    if stereo and custom:
        getCam = mc.confirmDialog(title = 'Select Camera', message = 'Which Stereo Camera do you want to take Playblast from?', button = ['Left','Center','Right','Cancel'], cb = 'Cancel', ds = 'Cancel')
        if getCam == 'Left':
            scCam = scCam.replace("_camCt", "_camLt")
        elif getCam == 'Right':
            scCam = scCam.replace("_camCt", "_camRt")
        elif getCam == 'Cancel':
            return False
    if mc.window('playBlastWindow', exists = 1): mc.deleteUI('playBlastWindow')
    if mc.windowPref ('playBlastWindow', exists = 1): mc.windowPref ('playBlastWindow', remove = 1)
    pbTmp = mc.window("playBlastWindow", wh = (1000, 700), te = 50, le = 50)
    mc.paneLayout()
    modPane = mc.modelPanel()
    mc.showWindow(pbTmp)
    mc.lookThru(scCam, modPane)
    mc.modelEditor(modPane, e=True, allObjects=0)
    mc.modelEditor(modPane, e=True, nurbsSurfaces=1, polymeshes=1,fluids=1,strokes=1)
    mc.modelEditor(modPane, e=True, da='smoothShaded')
    mc.modelEditor(modPane, e=True, av = True)
    sounds = mc.ls('%s*'%soundName, typ='audio')
    if not sounds:
        sounds = mc.ls(typ='audio')
    sound = sounds[0]  if sounds else ''
    st = mc.playbackOptions(q = True, ast = True)
    en = mc.playbackOptions(q = True, aet = True)
    blastPath = os.path.join(os.environ['TMP'], 'tempPlayblast.avi')
    if custom:
#        Find the highlighted range on timeSlider (if any)..
        aPlayBackSlider = mel.eval('$tmpVar=$gPlayBackSlider')
        times = mc.timeControl(aPlayBackSlider, q=True, rng=1)
        times = times.replace('"', '').split(':')
        if int(times[1]) != int(times[0]) +1 :  # 'll be currentTime & currentTime+1 evenif no range selected ==> Exclude that case!
            st = int(times[0])
            en = int(times[1]) -1
        finalPath = None
    else:
        st = 101
        en = 100 + mayaShot.frames
        finalPath = customPath if customPath else mayaShot.shotPath.replace(".%s"%mayaShot.projInfo.mayaExt, ".avi")
        saveVersion(finalPath)
    width = width*2
    height = height*2
    mc.playblast(st = st, et = en, fmt = 'movie', f = blastPath, s = sound, c = 'Lagarith', fo = True, orn = True, p = 50, qlt = 100, w = width, h = height)
    if finalPath:
        try:
            shutil.copyfile(blastPath, finalPath)
        except:
            msgWin("Error", "Error copying %s to %s"%(blastPath, finalPath), False)
    mc.deleteUI(pbTmp)
    return True
    
def viewportDisplay(modPane, typ = "bounding"):
    if typ == "bounding":
        mc.modelEditor(modPane, e=True, allObjects=1)
        shading = 'boundingBox'
    elif typ == "geometry":
        mc.modelEditor(modPane, e=True, allObjects=0)
        mc.modelEditor(modPane, e=True, nurbsSurfaces=1, polymeshes=1)
        shading = 'smoothShaded'
    else:
        return
    mc.modelEditor(modPane, e=True, da=shading)
    
def findLastVersion(path, typ = "ma", listVersions = False, filename = ""):
    """ path = "R:/workspace/animation/sq014/sh016/ or R:/workspace/animation/sq014/sh016/ver",
    filename = "ccy_sq999sh001_st01_v00.ma" """
    versions = [] if listVersions else [0]
    if not os.path.exists(path):
        msgWin("Error", "Folder %s does not exist" % path, True) 
        return None
    pattern = "_v[0-9][0-9][0-9].%s$" % typ
    if not filename == "":
        matchObj = re.search(pattern, filename)
        if matchObj:
            pattern = filename.replace(matchObj.group(0), pattern)
    if not "ver" in path:
        path = os.path.join(path, "ver")
    if os.path.exists(path):
        verFiles = sorted([f for f in os.listdir(path) if re.search(pattern, f)])
        if verFiles:
            versions = sorted([int(verFile.split(".")[0][-3:]) for verFile in verFiles])
    if listVersions:
        return versions
    else:
        return versions[-1]
    
def findLastAstVersion(path, typ = "ma", listVersions = False, filename = ""):
    """ #       V:/abn/assets/Modeling/Char/BirdRocAdult00c/ver",
    filename = "abn01_BirdRocAdult00c_md01_v000.ma" """
    versions = [] if listVersions else [0]
    if not os.path.exists(path):
        msgWin("Error", "Folder %s does not exist" % path, True) 
        return None
    pattern = "_v[0-9]{3}.%s$" % typ
    if not filename == "":
        matchObj = re.search(pattern, filename)
        if matchObj:
            pattern = filename.replace(matchObj.group(0), pattern)
    if not "ver" in path:
        path = os.path.join(path, "ver")
    if os.path.exists(path):
        verFiles = sorted([f for f in os.listdir(path) if re.search(pattern, f)])
        if verFiles:
            versions = sorted([int(verFile.split(".")[0][-3:]) for verFile in verFiles])
    if listVersions:
        return versions
    else:
        return versions[-1]
    
def findLastRetake(path, typ = "ma", listRetakes = False):
    """ path = "R:/workspace/animation/sq014/sh016/ or R:/workspace/animation/sq014/sh016/ver",
    filename = "ccy_sq999sh001_st01_v00.ma" """
    retakes = [] if listRetakes else [0]
    if not os.path.exists(path):
        msgWin("Error", "Folder %s does not exist" % path, True) 
        return None
    pattern = "_([a-z]{2})([0-9]{2})_v([0-9]{2})"
    if not "ver" in path:
        path = "%s/ver"%path
    if os.path.exists(path):
        rtkFiles = sorted([f for f in os.listdir(path) if re.search(pattern, f) and f.endswith(".%s"%typ)])
        if rtkFiles:
            retakes = []
            for rtkFile in rtkFiles:
                matchObj = re.search(pattern, rtkFile)
                retake = matchObj.group(0)[3:5]
                retakes.append(int(retake))
    if listRetakes:
        return sorted(retakes)
    else:
        return sorted(retakes)[-1]
    
def saveVersion(filePath = None):
    """ path = "R:/workspace/animation/sq014/sh016/ccy_sq014sh016_an_v00.ma" """
    if not filePath:
        filePath = mc.file(q = 1, sn = 1)
    fileName = os.path.basename(filePath)
    fileExt = fileName.split(".")[-1]
    fileDir = os.path.dirname(filePath)
    verFldr = os.path.join(fileDir, "ver")
    if os.path.exists(verFldr):
        nextVer = findLastVersion(verFldr, fileExt, filename = fileName) + 1
    else:
        nextVer = 1
        os.makedirs(verFldr)
    verFileName = fileName.replace("_v000.%s" % fileExt, "_v%s.%s" % (str(nextVer).zfill(3), fileExt))
    try:
        shutil.copy2(filePath, os.path.join(verFldr, verFileName))
    except:
        print "Error copying %s to %s" % (filePath, verFldr)
        return False
    return True

def writePermission(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except:
            return False
    try:
        os.mkdir(os.path.join(path, "TestFolder"))
        os.rmdir(os.path.join(path, "TestFolder"))
        return True
    except:
        return False

def convertName(objName, targType = "texture", nameSpace = False):
    resTypes = ["proxy", "rig", "texture"]
    if not targType in resTypes:
        print "Unknown resolution %s" % targType
        return None
    endChar = "$" if nameSpace else ":"
    objRes = findObjRes(objName, nameSpace)
    pattern = "_p(%s)01%s" % ("p|r|t", endChar)
#     pattern = "._(%s)[0-9]?[0-9]?%s" % ("p|m|h", endChar)
    pMatch = re.search(pattern, objName)
    if pMatch:
        curMatch = pMatch.group(0)
        targName = curMatch.replace("_p%s01" % objRes, "_p%s01" % targType[0])
        return objName.replace(curMatch, targName)
    else:
        return objName
    
def convert1001Name(objName, targType = "texture", nameSpace = False):
    resTypes = ["proxy", "rig", "texture"]
    if not targType in resTypes:
        print "Unknown resolution %s" % targType
        return None
    endChar = "$" if nameSpace else "_"
    objRes = findObjRes(objName)
    pattern = "_p(%s)01%s" % ("p|r|t", endChar)
#     pattern = "._(%s)[0-9]?[0-9]?%s" % ("p|m|h", endChar)
    pMatch = re.search(pattern, objName)
    if pMatch:
        curMatch = pMatch.group(0)
        targName = curMatch.replace("_p%s01" % objRes, "_p%s01" % targType[0])
        return objName.replace(curMatch, targName)
    else:
        return objName
    
def find1001ObjRes(objName):
    objRes = "r"
    pattern = "_p(%s)01_" % ("p|r|t")
    pMatch = re.search(pattern, objName)
    if pMatch:
        objRes = (pMatch.group(0)[2]).lower()
    return objRes    
    
def convertAssetName(objName, targType = "texture"):
    resTypes = ["proxy", "rig", "texture"]
    if not targType in resTypes:
        print "Unknown resolution %s" % targType
        return None
    pattern = "_p(%s)01%s" % ("p|r|t")
#     pattern = "_(%s)_"%("p|m|h")
    pMatch = re.search(pattern, objName)
    if pMatch:
        curMatch = pMatch.group(0)
        targName = "_p%s01"%(targType[0])
        return objName.replace(curMatch, targName)
    else:
        return objName
    
def findObjRes(objName, nameSpace = False):
    ns = "$" if nameSpace else ":"
    objRes = "r"
    pattern = "_p(%s)01%s" % ("p|r|t", ns)
    pMatch = re.search(pattern, objName)
    if pMatch:
        objRes = (pMatch.group(0)[2]).lower()
    return objRes

def stripNames(objName, strip = ":"):
    if strip in objName:
        return objName.split(strip)[-1]
    else:
        return objName
    
def chkStaticCurve(animCurve):
    val = mc.keyframe(animCurve, q = 1, vc = 1)
    if (max(val) - min(val)) > 0.0001:
        return False
    else:
        return True

def removeStaticKeyframes(obj):
    conns = mc.listConnections(obj, t = "animCurve", d = 0)
    for conn in conns:
        if chkStaticCurve(conn):
            mc.delete(conn)
            
def checkLockedFiles(path, ext):
    lockedFiles = []
    if not os.path.exists(path):
        print "Path does not exist %s"%path
        return []
    cchDict = cachePath2Dict()
    for fil in listAllFiles(path, ext):
        try:
            k = open(fil, 'w')
            k.close()
        except:
            lockedFiles.append(fil)
    dict2CachePath(cchDict)
    return lockedFiles

def cachePath2Dict(disable = True, cacheNodes = []):
    if cacheNodes:
        cchNodes = cacheNodes
    else:
        cchNodes = mc.ls(type = "cacheFile")
    cchPathDict={}
    for i in range(len(cchNodes)):
        path = mc.getAttr((cchNodes[i] + ".cachePath"))
        cchPathDict[str(cchNodes[i])] = str(path)
        if disable:
            mc.setAttr((cchNodes[i] + ".cachePath"), "C:/", type = "string")
    return cchPathDict

def dict2CachePath(cchDict):
    for cch in cchDict.keys():
        if mc.objExists(cch):
            mc.setAttr((cch + ".cachePath"), cchDict[cch], type = "string")
            
def fixPathsIP():            
    ccNodes = mc.ls(typ = "cacheFile")
    flNodes = mc.ls(type='file')
    chNodes = ccNodes + flNodes
    if not chNodes:
        msgWin("Warning", "No cache/texture nodes found in the scene", False)
        return
    fixedNodes, missedNodes, = [], []
    for chNod in chNodes:
        if mc.nodeType(chNod) == "cacheFile":
            chPath = str(mc.getAttr("%s.cachePath"%chNod))
        else:
            chPath = str(mc.getAttr("%s.fileTextureName"%chNod))
        if ":" in chPath:
            print chNod,chPath
            chPathSplit = chPath.split(":")
            driveLetter = chPathSplit[0].lower()
            chPath = drvPathDict[driveLetter] + chPathSplit[1]
            if mc.nodeType(chNod) == "cacheFile":
                mc.setAttr("%s.cachePath"%chNod, chPath, type = "string")
            else:
                mc.setAttr("%s.fileTextureName"%chNod, chPath, type = "string")
        rootFldr = os.path.basename(findRootFldr(chPath))
        ipMatch = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", rootFldr)
        if not ipMatch:
            try:
                ipAddr = socket.gethostbyname(rootFldr)
            except:
                missedNodes.append(chPath)
                continue
            newChPath = chPath.replace(rootFldr, ipAddr)
            if mc.nodeType(chNod) == "cacheFile":
                mc.setAttr("%s.cachePath"%chNod, newChPath, type = "string")
            else:
                mc.setAttr("%s.fileTextureName"%chNod, newChPath, type = "string")
            fixedNodes.append(chPath)
    if fixedNodes:
        msg = "Fixed paths for %s cache/texture nodes"%len(fixedNodes)
    else:
        msg = "All paths are already correct"
    msgWin("Message", msg, False)
    
def findRootFldr(path):
    while True:
        dirParent = os.path.dirname(path)
        if dirParent == "//" or len(dirParent) <= 3:
            return path
            break
        else:
            path = os.path.dirname(path)            
            
def sceneDupObjs(objs = None):
    if not objs:
        objs = mc.ls(l = True)
    dupObjs = []
    for i in range(len(objs)):
        for j in range(i+1, len(objs)):
            if stripNames(objs[i], "|") == stripNames(objs[j], "|"):
                dupObjs.append([objs[i], objs[j]])
    return dupObjs

def listAllFiles(path, ext):
    if not os.path.exists(path):
        print "Path does not exist %s"%path
        return []
    filePaths = []
    for (dirpath, dirnames, filenames) in os.walk(str(path)): #@UnusedVariable
        for filename in filenames:
            if filename.endswith(".%s"%ext):
                filePaths.append(os.path.join(dirpath, filename))
    return filePaths

def fileTimeStamp(path):
    t = os.path.getmtime(path)
    tStamp = datetime.datetime.fromtimestamp(t)
    return tStamp.strftime("%d-%m-%Y %H:%M")