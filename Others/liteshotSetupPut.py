import maya.cmds as mc
import maya.mel as mel
import os
import pipeline.Utils as Utils
util = None

def liteShotSetupUI():
    global charnames, propnames, setnames, adcharnames, adpropnames, adsetnames
    charnames, propnames, setnames, adcharnames, adpropnames, adsetnames = [], [], [], [], [], []
    
    #window setup
    
    if mc.window('liteshot', exists = True):
        mc.deleteUI('liteshot')
    mc.window('liteshot', title = 'Scene Lighting Setup - Purple Turtle', wh = (450,300))
    mc.columnLayout()
    
    
    #buttons for setting up ground and matte objects, button for removing bg

    mc.columnLayout(co = ('left', 45))
    mc.separator(h = 10, w = 500, st = 'none')
    mc.rowLayout(nc = 3, cw3 = (150, 150, 100), cl3 = ("both", "both", "both"))
    mc.button('setgrnd', l = "Setup Ground Object", w = 120, c = lambda event:setupGndMte("Grp_Ground"))
    mc.button('setmtte', l = "Setup Matte Object", w = 120, c = lambda event:setupGndMte("Grp_Matte"))
    mc.button('rembg', l = "Remove BG", w = 80, c = lambda event:remBg())
    mc.setParent('..')
    mc.setParent('..')

    
    #buttons for setting no of layer grps, scan for assets and resetting UI

    mc.columnLayout(co = ('left', 35))
    mc.separator(h = 10, w = 500, st = 'none')
    mc.separator(h = 10, w = 500, st = 'none')
    mc.rowLayout(nc = 3, cw3 = (200, 110, 100))
    mc.intFieldGrp("numgrps", numberOfFields=1, label='Number of Render layer grps', v1 = 1, cw2 = (150, 30))
    mc.button('scanbtn', l = "   Scan Scene", w = 80, c = lambda event:scanScene())
    mc.button('rsetbtn', l = "     Reset UI", w = 80, c = lambda event:liteShotSetupUI())
    mc.setParent('..')
    mc.setParent('..')

    
    #scroll layout placeholder for the assets dynamic menu

    mc.separator(h = 10, w = 500, st = 'none')
    mc.columnLayout(co = ('left', 15))
    mc.scrollLayout('scrll', h = 200, vis = 0, hst = 0)
    mc.setParent('..')

    
    #column layout placeholder for the light options menu
    
    mc.separator(h = 10, w = 500, st = 'none')
    mc.columnLayout("ltopts", co = ('left', 5), h = 120)    
    mc.setParent('..')
    
    
    #scene setup button
    
    mc.separator(h = 20, w = 450, st = 'in')
    mc.columnLayout(co = ('left', 75), h = 50)    
    mc.button(l = "SETUP SCENE", w = 300, h = 30, al = "center", c = lambda event:setupScene())
    mc.setParent('..')
    
    mc.separator(h = 10, w = 500, st = 'none')
    mc.setParent('..')
    mc.showWindow('liteshot')
    mc.window('liteshot', e = True, wh = (483, 125))


    
#setting up scene. exports selected assets to a _cl_v00 file, opens that file set's up the render layers, globals and lights    

def setupScene():
    global util
    errormsgs = []
    util = Utils.utils()
    
    chks = ['keychk', 'rimchk','colchk','occchk','rgbachk','gshchk','matchk']
    chkstats = [mc.checkBox(x, q = True, v = True) for x in chks]
    if not 1 in chkstats:
        mc.confirmDialog(t='Warning', m = 'No layers are selected', b='OK', ma = "center")
        return    
    
    #get dict of assets in their respective render layer groups
    
    grpDict = findGrpDict()
    layergrps = grpDict.keys()
    layergrps.sort()
    
    
    #find the path of the file, check naming of file and query the timeline
 
    filepath = mc.file(q = True, sn = True)
    filename = os.path.basename(filepath)
    fildir = os.path.dirname(filepath)
    refcut = mc.checkBox("refchk", q = True, v = True)
    try:
        shotname = filename.split("_")[1]
    except:
        mc.confirmDialog(t='Warning', m = 'Scene name is not correct', b='OK', ma = "center")
        return
    shstart = mc.playbackOptions(q = True, ast = True)
    shend = mc.playbackOptions(q = True, aet = True)
    
    
    #query the camera and the camera group
    
    cam = mc.optionMenu('camlite', q = True, v = True)
    
    #setup the name of the new files
    
    clfile = filename[:-9] + "cl" + filename[-7:]
    #check the file exists, then change to vesion folder
    curr_path = fildir+'/'
    clfilepath=curr_path+clfile
    if mc.file(clfilepath,q=1,ex=1):
        Overrite = mc.confirmDialog(
                title='Confirm ',
                message='Overwrite the existing file? ',
                button=['Yes', 'No'],
                defaultButton='Yes',
                cancelButton='No',
                dismissString='No') 
        if Overrite =='No':   
            return
        
    chkpath=mc.getFileList (folder=curr_path)
    ver_count=chkpath.count('ver')
    verpath= curr_path+'ver/'
    if not ver_count:
        mc.sysFile(verpath,makeDir=1)      
#    else:
#        verpath= curr_path+'ver/'
    files = [ f for f in os.listdir(verpath) if (os.path.isfile (os.path.join(verpath,f))) and f[len(f)-3:len(f)]=='.ma']
    if files:
        ver = str(len(files)+1)
    else:
        ver='01'
    newpath=verpath+clfile
    mc.sysFile(filepath,copy=newpath)
    newname=clfile[:19]+'%s.ma'%ver.zfill(2)
    chgname=verpath+newname
    mc.sysFile(newpath,rename=chgname)
    
    #select all the assets specified in the setup window to export to a new file
    
    selasts = []
    refcutmiss = []
    for each in layergrps:
        for ast in grpDict[each]:
            selasts.append(ast)
    
            
    #add the camera to the selection
    
    selasts.append(cam)
    
    
    #add the ground and matte groups to the selection if they exist, else warn that they have not been setup
    
    gndmteobjs = ["Grp_Ground", "Grp_Matte"]
    if mc.objExists("Grp_Ground"):
            gndmteobjs.pop(gndmteobjs.index("Grp_Ground"))
            selasts.append("Grp_Ground")
    if mc.objExists("Grp_Matte"):
            gndmteobjs.pop(gndmteobjs.index("Grp_Matte"))
            selasts.append("Grp_Matte")
    if gndmteobjs:
        gndmtemsg = "\n".join(gndmteobjs)
        rslt = mc.confirmDialog(t='Warning', m="Ground/Matte Objects dont\nexist or havent been set up", b=['Continue', 'Cancel'], db='Continue', cb='Cancel', ds='Cancel', ma = 'center')
        if rslt == 'Cancel':
            return
        else:
            pass
            
    mc.select(selasts, r = True)
    
    

    #cmfile = filename[:-9] + "cm" + filename[-7:]
    

    #export all selected assets, cameras and ground/matte groups to a new _cl_v00 file
    
    mc.file((fildir + "/" + clfile), op = "v=0", typ = "mayaAscii", pr = True, es = True, f=True )

    #force open the new _cl_v00 file without saving the old one
    
    mc.file((fildir + "/" + clfile), op = "v=0", typ = "mayaAscii", lrd = "all", o = True, f = True)
    
    #select camera and export selected camera to a new _cm_v00 file
    
    #mc.select(cam, r = True) 
    #mc.file((fildir + "/" + cmfile), op = "v=0", typ = "mayaAscii", pr = True, es = True)
    mc.select(cl = True)
    
    #set the timeline and render globals, and move assets to their respective groups
    
    mc.playbackOptions(e = True, ast = shstart)
    mc.playbackOptions(e = True, aet = shend)
    setrendglobals(shotname, shstart, shend)
    try:
        Utils.moveAssetsToGrps()
    except:
        pass
    
        
    #setup the useBackground shader and assign it to the ground/matte objects if they exist
    
    gndusebg = "groundmatteuseBGshader"
    if mc.objExists(gndusebg):
        mc.delete(gndusebg)
    gndusebg = mc.shadingNode("useBackground", asShader = True, n = gndusebg)
    mc.setAttr((gndusebg + ".specularColor"), 0, 0, 0, type = "double3")
    mc.setAttr((gndusebg + ".reflectivity"), 0)
    mc.setAttr((gndusebg + ".reflectionLimit"), 0)
    mc.setAttr((gndusebg + ".shadowMask"), 0)
    if mc.objExists("Grp_Ground"):
        mc.select("Grp_Ground", r = True)
        mc.hyperShade(assign = gndusebg)
    if mc.objExists("Grp_Matte"):
        mc.select("Grp_Matte", r = True)
        mc.hyperShade(assign = gndusebg)
        
    
    #query the rim/key light required and import the relevant light file from /assets/lighting
    locquery  = mc.optionMenu('Location', q = True, v = True)
    rmkylight = mc.optionMenu('Time', q = True, v = True)
    camquery  = mc.optionMenu('camlite', q = True, v = True)
    rmkyfile = "%s/%s/Location/%s/%s_rimkey.ma"%(util.path, util.litePath,locquery,rmkylight)
    rimliteL = "%s:rimL"%rmkylight
    rimliteR = "%s:rimR"%rmkylight
    #refdoom  = "%s:ref_doom"%rmkylight
    keylite  = "%s:key"%rmkylight
    #fillite  = "%s:fill"%rmkylight
    #eyespec  = "%s:eyespc"%rmkylight
    if os.path.exists(rmkyfile):
        if mc.objExists(rimliteL):
            mc.delete(rimliteL)
        if mc.objExists(rimliteR):
            mc.delete(rimliteR)
        #if mc.objExists(fillite):
            #mc.delete(fillite)
        if mc.objExists(keylite):
            mc.delete(keylite)   
        mc.file(rmkyfile, i = True, typ = "mayaAscii", ra = True, ns = rmkylight, op = "v=0;p=17", pr = True)
    else:
        mc.confirmDialog(t='Warning', m = '%s file is not accessible'%rmkylight, b='OK', ma = "center")
        return
        
    #find the names of the imported rim/key lights in the scene and parent them to the 'Rim_key' group
    
    if mc.objExists("LIGHTS"):
            mc.delete("LIGHTS")
            
    sclites = mc.ls(type = "light")
    for each in sclites:
        if ":rimL" in each:
            rimliteL = mc.listRelatives(each, p = True)[0]
        elif ":rimR" in each:
            rimliteR = mc.listRelatives(each, p = True)[0]
        #elif ":fill" in each:
            #fillite  = mc.listRelatives(each, p = True)[0]
        elif ":key" in each:
            keylite = mc.listRelatives(each, p = True)[0]
    keygrp = "%s:key_set"%rmkylight
    mc.group(n = "LIGHTS", em = True)
    mc.parent(keygrp,"LIGHTS" )
                    
    #query common lights required and import the relevant light file from /assets/lighting/commonlights
    
    commonfile = "%s/%s/common_lights/common_lights.ma"%(util.path, util.litePath)
    commonlight="commonlight"
    #litequery=mc.optionMenu('amblite',q=True,v=True) 
    #GIrAMB = "%s:%s"%(commonlight,litequery)
    if os.path.exists(commonfile):
        if mc.objExists(commonlight):
            mc.delete(commonlight)
        mc.file(commonfile, i = True, typ = "mayaAscii", ra = True, ns = commonlight, op = "v=0;p=17", pr = True)
    else:
        mc.confirmDialog(t='Warning', m = '%s file is not accessible'%commonlight, b='OK', ma = "center")
        return        
  
    #mc.parent("commonlight:commonLight_sets","LIGHTS" )
    #spclite_parnt=mc.parent(spclite,camquery)
    #find shape node of key light
    
    if mc.objExists(keylite):
        keyliteshp = mc.listRelatives(keylite, c = True, s = True)
    
        
    #setup the mat shaders
    
    rgbashaders = rgbashader(shotname)
    mc.select(cl = True)
    myShader = mc.shadingNode('lambert', asShader=True)
    mc.setAttr (myShader+".colorR", 0.886)
    mc.setAttr (myShader+".colorG" ,0.961)
    mc.setAttr (myShader+".colorB" ,0.961)
    
    # assign cam folder 
    
    if camquery[14:] =='Ct':
        camname = "Center"
    elif camquery[14:]=='Lt':
        camname = "Left"
    else:
        camname = "Right"
    
    #remove all existing render layers
    
    mc.editRenderLayerGlobals(crl = "defaultRenderLayer")
    renlyrs = mc.ls(type = "renderLayer")
    for each in renlyrs:
        if not "defaultRenderLayer" in each:
            mc.delete(each)
    
            
    #cut the references of all assets if marked so in the light setup options            
    
    for each in layergrps:
        for ast in grpDict[each]:
            if refcut:
                try:
                    cutref(ast)
                except:
                    refcutmiss.append(ast)
    
                    
    #main loop for creating all the render layers with their respective settings working on each render layer group per loop                

    sqname = shotname[:5]
    shname = shotname[5:]    
    matindex = 0
    for lyr in layergrps:
        asts = grpDict[lyr]
        
          
        #create key layer, add key light
        
        if mc.checkBox("keychk", q = True, v = True):
            keylayer = (lyr + 'key')
            mc.select(asts, r = True)
            mc.select(keylite, add = True)
            #mc.select(refdoom, add = True)
            #mc.select(eyespec, add = True)
            if mc.objExists("Grp_Ground"):
                mc.select("Grp_Ground", add = True)
            if mc.objExists("Grp_Matte"):
                mc.select("Grp_Matte", add = True)
            mc.createRenderLayer(mc = True, n = keylayer)
            mc.editRenderLayerAdjustment(gndusebg + ".shadowMask")
            mc.setAttr(gndusebg + ".miOcclusionMask", 0)
            mc.connectAttr(keylayer+'.renderPass', 'diff.owner',nextAvailable=True)
            mc.connectAttr(keylayer+'.renderPass', 'amb.owner', nextAvailable=True)
            mc.connectAttr(keylayer+'.renderPass', 'sha.owner', nextAvailable=True)
            mc.connectAttr(keylayer+'.renderPass', 'spc.owner', nextAvailable=True)
            mc.connectAttr(keylayer+'.renderPass', 'inc.owner',nextAvailable=True)
            fileprefix = "%s/%s/%s/ch/%s/<RenderLayer>/<RenderPass>/%s%s_<RenderLayer>_<RenderPass>_v01"%(sqname,shname,camname,lyr,sqname,shname)
            mc.editRenderLayerAdjustment ("defaultRenderGlobals.imageFilePrefix")            
            mc.setAttr("defaultRenderGlobals.imageFilePrefix", fileprefix, type = "string")
            mc.editRenderLayerAdjustment('miDefaultOptions.rayTracing')
            mc.setAttr('miDefaultOptions.rayTracing',1)            
            mc.editRenderLayerAdjustment( 'miDefaultOptions.maxReflectionRays' )
            mc.setAttr('miDefaultOptions.maxReflectionRays', 3)
            mc.editRenderLayerAdjustment( 'miDefaultOptions.maxRefractionRays' )
            mc.setAttr('miDefaultOptions.maxRefractionRays', 0)
            mc.editRenderLayerAdjustment( 'miDefaultOptions.maxRayDepth')
            mc.setAttr('miDefaultOptions.maxRayDepth',20)            
            
        #create rim layer, add rimlight
        
        if mc.checkBox("rimchk", q = True, v = True):
            rimlayer = (lyr + 'rim')
            mc.select(asts, r = True)
            mc.select(rimliteL, add = True)
            mc.select(rimliteR, add = True)
            mc.createRenderLayer(mc = True, n = rimlayer)
            rimsh='%s:Rimshader'%commonlight
            #mc.shadingNode("lambert", asShader = True, n = rimsh )
            #mc.setAttr((rimsh+'.color'),1, 1, 1, type = "double3")
            #mc.setAttr((rimsh+'.diffuse'),1)
            mc.select(rimsh)
            mel.eval('hookShaderOverride("%s","","%s")'%(rimlayer,rimsh))
            fileprefix = "%s/%s/%s/ch/%s/<RenderLayer>/%s%s_<RenderLayer>_v01"%(sqname, shname,camname,lyr, sqname, shname)
            mc.editRenderLayerAdjustment ("defaultRenderGlobals.imageFilePrefix")            
            mc.setAttr("defaultRenderGlobals.imageFilePrefix", fileprefix, type = "string")
            mc.editRenderLayerAdjustment('miDefaultOptions.rayTracing')
            mc.setAttr('miDefaultOptions.rayTracing',0)
            
        #create col layer,add amb light
        
        if mc.checkBox("colchk",q= True,v = True):
            collayer= (lyr+ 'col')
            mc.select(asts, r = True)
            Col_light='%s:colLight'%commonlight 
            mc.select(Col_light,add=True)
            mc.createRenderLayer(mc = True, n = collayer)
            mc.editRenderLayerAdjustment ("defaultRenderGlobals.imageFilePrefix")            
            mc.setAttr("defaultRenderGlobals.imageFilePrefix", fileprefix, type = "string")
      
        #create occ layer
        
        if mc.checkBox("occchk",q=True,v=True):
            occlayer = (lyr + 'occ')
            mc.select(asts,r=True)
            if mc.objExists("Grp_Ground"):
                mc.select("Grp_Ground", add = True)
            if mc.objExists("Grp_Matte"):
                mc.select("Grp_Matte", add = True)
            mc.createRenderLayer(mc = True, n = occlayer)
            mel.eval("renderLayerBuiltinPreset occlusion %s "%occlayer)
            ShaderList=mc.ls (sl=1)
            Mib_Amb=mc.listConnections(ShaderList,t='mib_amb_occlusion')
            mc.setAttr(Mib_Amb[0]+'.samples',64)
            mc.setAttr(Mib_Amb[0]+'.spread',0.8)
            mc.setAttr(Mib_Amb[0]+'.max_distance',20)
            fileprefix = "%s/%s/%s/ch/%s/<RenderLayer>/%s%s_<RenderLayer>_v01"%(sqname, shname,camname,lyr, sqname, shname)
            mc.editRenderLayerAdjustment ("defaultRenderGlobals.imageFilePrefix")            
            mc.setAttr("defaultRenderGlobals.imageFilePrefix", fileprefix, type = "string")
            
            
        #create mat layer and assign r, g and b shaders in turn using matindex, turn off raytracing using layer override
        
        if mc.checkBox("rgbachk", q = True, v = True):
            rgbalayer = (lyr + 'rgba')
            mc.select(asts, r = True)
            mc.createRenderLayer(mc = True, n = rgbalayer)
            for i in range(len(asts)):
                shindex = matindex%4
                matindex += 1
                mc.select(asts[i], r = True)
                mc.hyperShade(assign = rgbashaders[shindex])
            fileprefix = "%s/%s/%s/ch/%s/<RenderLayer>/%s%s_<RenderLayer>_v01"%(sqname, shname,camname,lyr, sqname, shname)
            mc.editRenderLayerAdjustment ("defaultRenderGlobals.imageFilePrefix")            
            mc.setAttr("defaultRenderGlobals.imageFilePrefix", fileprefix, type = "string")
            mc.setAttr('miDefaultOptions.rayTracing',0)
            
        #create ground shadow layer, add key light and turn on shadow mask of useBG shader using layer override
        
        if mc.checkBox("gshchk", q = True, v = True):
            gshlayer = (lyr + 'gsh')
            mc.select(asts, r = True)
            mc.select(keylite, add = True)        
            if mc.objExists("Grp_Ground"):
                mc.select("Grp_Ground", add = True)
            if mc.objExists("Grp_Matte"):
                mc.select("Grp_Matte", add = True)
            mc.createRenderLayer(mc = True, n = gshlayer)
            mc.editRenderLayerAdjustment(gndusebg + ".shadowMask")
            mc.setAttr(gndusebg + ".shadowMask", 1)
            fileprefix = "%s/%s/%s/ch/%s/<RenderLayer>/%s%s_<RenderLayer>_v01"%(sqname, shname,camname,lyr, sqname, shname)
            mc.editRenderLayerAdjustment ("defaultRenderGlobals.imageFilePrefix")            
            mc.setAttr("defaultRenderGlobals.imageFilePrefix", fileprefix, type = "string")
            mc.editRenderLayerAdjustment('miDefaultOptions.rayTracing')
            mc.setAttr('miDefaultOptions.rayTracing',1) 
            mc.editRenderLayerAdjustment( 'miDefaultOptions.maxReflectionRays' )
            mc.setAttr('miDefaultOptions.maxReflectionRays', 0)
            mc.editRenderLayerAdjustment( 'miDefaultOptions.maxRefractionRays' )
            mc.setAttr('miDefaultOptions.maxRefractionRays', 0)
            mc.editRenderLayerAdjustment( 'miDefaultOptions.maxRayDepth')
            mc.setAttr('miDefaultOptions.maxRayDepth',20)

            #turn off receive shadows and primary visibility of the all the assets using changespreadattr()
            for ast in asts:
                changespreadattr(ast, "receiveShadows", 0)
                changespreadattr(ast, "primaryVisibility", 0)
                
        #create mat layer
        
        if mc.checkBox("matchk",q= True, v = True):
            matlayer = (lyr + 'mat')
            mc.select(asts, r = True)
            Zdep='%s:Zdepthshader'%commonlight            
            mc.select(asts, r = True)
            mc.createRenderLayer(mc = True, n = matlayer)
            mc.select(Zdep)
            mel.eval('hookShaderOverride("%s","","%s")'%(matlayer,Zdep))
            mc.connectAttr(matlayer+'.renderPass', 'camnml.owner', nextAvailable=True)
            mc.connectAttr(matlayer+'.renderPass', 'nml.owner', nextAvailable=True)
            fileprefix = "%s/%s/%s/ch/%s/<RenderLayer>/<RenderPass>/%s%s_<RenderLayer>_<RenderPass>_v01"%(sqname,shname,camname,lyr,sqname,shname)
            mc.editRenderLayerAdjustment ("defaultRenderGlobals.imageFilePrefix")            
            mc.setAttr("defaultRenderGlobals.imageFilePrefix", fileprefix, type = "string")
            mc.editRenderLayerAdjustment('miDefaultOptions.rayTracing')
            mc.setAttr('miDefaultOptions.rayTracing',0) 
            mc.editRenderLayerAdjustment( 'miDefaultOptions.maxReflectionRays' )
            mc.setAttr('miDefaultOptions.maxReflectionRays', 1)
            mc.editRenderLayerAdjustment( 'miDefaultOptions.maxRefractionRays' )
            mc.setAttr('miDefaultOptions.maxRefractionRays', 1)
            mc.editRenderLayerAdjustment( 'miDefaultOptions.maxRayDepth')
            mc.setAttr('miDefaultOptions.maxRayDepth',1)                 
    mc.editRenderLayerGlobals(crl = "defaultRenderLayer")
    mc.setAttr("defaultRenderLayer.renderable",0)
    mc.select(cl = True)
    
#    mc.checkBoxGrp ('enableColorProfile',e=1,v1=1)
#    mc.optionMenuGrp('inputColorProfile',e=1,enable=1)
#    mc.optionMenuGrp('outputColorProfile',e=1,enable=1)
#    mc.optionMenuGrp('inputColorProfile',e=1 ,sl=1 )
#    mc.optionMenuGrp('outputColorProfile',e=1 ,sl=2)
#    mc.setAttr ("defaultRenderGlobals.inputColorProfile",1) 
#    mc.setAttr ("defaultRenderGlobals.outputColorProfile",2) 
    mc.confirmDialog(t='Message', m = 'Scene setup completed successfully', b='OK', ma = "center")

#mass changing atttributes(attrname) for all objects under a parent object(root) to value(val)
    
def changespreadattr(root, attrname, val):
    missedobjs = []
    objs = mc.listRelatives(root, ad = True, pa = True)
    for each in objs:
        try:
            mc.setAttr("%s.%s"%(each, attrname), val)
        except:
            missedobjs.append(each)
    
            
#return a dictionary of assets associated with each render layer group
#example {group1 : [asset1, asset2], group2 : [asset3,asset4],.....}            
            
def findGrpDict():
    global charnames, propnames, setnames, charopt, propopt, setopt
    #query number of render layer groups needed from UI
    rendgrps = mc.intFieldGrp("numgrps", q = True, v1 = True)
    grpdict = {}
    #loop thorugh each layer group, find assets marked to those layers in UI, assign to dict value under the layer group key
    for i in range(rendgrps):
        key = "ch%s"%str(i + 1).zfill(2)
        grpassets = []
        for k in range(len(charopt)):
            if mc.optionMenu(charopt[k], q = True, v = True) == key:
                grpassets.append(charnames[k])
        for l in range(len(propopt)):
            if mc.optionMenu(propopt[l], q = True, v = True) == key:
                grpassets.append(propnames[l])
        for m in range(len(setopt)):
            if mc.optionMenu(setopt[m], q = True, v = True) == key:
                grpassets.append(setnames[m])
        if grpassets:                
            grpdict[key] = grpassets
    return grpdict

    
    
#scan the scene, sort the assets into chars, props and sets, create dynamic menu listing all assets in categories
#also add drop down list to select the render layer group in which the asset needs to be put in
#add dropdown list to select type of ambient light, bg rim key light file and show the renderable camera for verification
#buttons to select the asset for checking and buttons to add any asset that was not caught during scan 
    
def scanScene():
    global util, charnames, propnames, setnames, adcharnames, adpropnames, adsetnames, charopt, propopt, setopt
    util = Utils.utils()
    #declaring and initialising variables
    charnames, propnames, setnames, miscnames, charopt, propopt, setopt = [], [], [], [], [], [], []
    
    
    #find rim/key light folder path from config.xml
    
    rmkyfldr = "%s/%s/Location"%(util.path, util.litePath)
    rmkyfiles = os.listdir(rmkyfldr)
    ltbgs = [x.replace('', '') for x in rmkyfiles]
    unrefs = []
    
    #find time  folder path from config.xml
    try:
        litefldr = "%s/%s/Location/%s"%(util.path, util.litePath,rmkyfiles[0])
    except:
        mc.error("Please set the correct project")
        return
    Litefiles = os.listdir(litefldr) 
    ltlites = [x.replace('_rimkey.ma', '') for x in Litefiles]
    
    
    #list all reference nodes in scene and list all unloaded references
    
    refs = mc.ls(type = "reference")
    if refs:
        for each in refs:
            if each != "sharedReferenceNode" and each != "_UNKNOWN_REF_NODE_":
                try:
                    nodes = mc.referenceQuery(each, nodes = True)
                    if not nodes:
                        unrefs.append(each)
                except:
                    pass
    else:
        print '\nNo valid References found.\n'
    
    #prompt to load all unloaded references for the scan to proceed, cancel will still show assets but setup will not work                
                
    if unrefs:
        nonrefassets = "Following references are unloaded\nLoad all the references?\n\n" + "\n".join(unrefs) + "\n"
        rslt = mc.confirmDialog(t='Warning', m=nonrefassets, b=['Continue', 'Cancel'], db='Continue', cb='Cancel', ds='Cancel', ma = 'center')
        if rslt == 'Cancel':
            pass
        else:
            for refs in unrefs:
                refpath = mc.referenceQuery(refs, f = True)
                mc.file(refpath, lr = True)
                
                
    #list all assets in the scenes using Utils.listAssets()                
                
    charnames, propnames, setnames, miscnames = Utils.listAssets()
    if adcharnames:
        for each in adcharnames:
            if not each in charnames: 
                charnames.append(each)
    if adpropnames:
        for each in adpropnames:
            if not each in propnames:
                propnames.append(each)
    if adsetnames:
        for each in adsetnames:
            if not each in setnames:
                setnames.append(each)
                
                
    #set the scroll menu placeholder in main UI as the parent menu of the dynamic that we're about to create                
                
    mc.setParent('scrll')
    numlayers = mc.intFieldGrp("numgrps", q = True, v1 = True)
    
    
    #column layout for the dynamic menu
    
    if mc.columnLayout("assetcol", ex = True):
        mc.deleteUI("assetcol")
    mc.columnLayout("assetcol")
    
    
    #listing the characters in the scene
    mc.separator(h = 5, w = 470, st = 'in')
    mc.text(l = "         CHARACTERS  ", fn = "boldLabelFont")
    mc.separator(h = 5, w = 470, st = 'in')
    mc.columnLayout(co = ('left', 10))
    mc.separator(h = 5, w = 470, st = 'none')
    
    
    #creating the menu for each of the characters in the scene
    
    for i in range(len(charnames)):
        mc.rowLayout(nc = 3, cw3 = (200, 150, 50))
        #name of the character
        mc.text(l = charnames[i])
        #select button command
        com = "mc.select(\"%s\", r = True)"%charnames[i]
        menulabel = "chmenu%s"%str(i).zfill(2)
        charopt.append(menulabel)
        #dropdown list for selecting the render layer group that the character will go into
        mc.optionMenu(menulabel, label = 'Render Grp : ')
        for ii in range(numlayers):
            mc.menuItem( label="ch%s"%str(ii + 1).zfill(2))
        mc.menuItem( label="None")
        #button for selecting the character
        mc.button(l = "Select", c = com)
        mc.setParent('..')
    mc.separator(h = 5, w = 470, st = 'none')
    mc.rowLayout(nc = 2, cw2 = (100, 300))
    #button to add a character that didn't show up in the scan
    mc.button(l = " Add Character", w = 80, al = "center", c = lambda event:addAsset(0))
    mc.text(label = "Select a group and press button to add the character")
    mc.setParent('..')
    mc.separator(h = 5, w = 400, st = 'none')        
    mc.setParent('..')

    
    #listing the props in the scene
    
    mc.separator(h = 5, w = 470, st = 'in')
    mc.text(l = "          PROPS  ", fn = "boldLabelFont")
    mc.separator(h = 5, w = 470, st = 'in')
    mc.columnLayout(co = ('left', 10))        
    mc.separator(h = 5, w = 470, st = 'none')
    
    
    #creating the menu for each of the props in the scene
    
    for k in range(len(propnames)):
        mc.rowLayout(nc = 3, cw3 = (200, 150, 50))
        #name of the prop
        mc.text(l = propnames[k])
        #select button command
        com = "mc.select(\"%s\", r = True)"%propnames[k]
        menulabel = "prmenu%s"%str(k).zfill(2)
        propopt.append(menulabel)
        #dropdown list for selecting the render layer group that the prop will go into
        mc.optionMenu(menulabel, label = 'Render Grp : ')
        for kk in range(numlayers):
            mc.menuItem( label="ch%s"%str(kk + 1).zfill(2))
        mc.menuItem( label="None")
        #button for selecting the prop
        mc.button(l = "Select", c = com)
        mc.setParent('..')
    mc.separator(h = 5, w = 470, st = 'none')        
    mc.rowLayout(nc = 2, cw2 = (100, 300))
    #button to add a prop that didn't show up in the scan
    mc.button(l = "     Add Prop", w = 80, al = "center", c = lambda event:addAsset(1))
    mc.text(label = "Select a group and press button to add the prop")
    mc.setParent('..')
    mc.separator(h = 5, w = 470, st = 'none')
    mc.setParent('..')    
    
    
    #listing the bgs in the scene

    mc.separator(h = 5, w = 470, st = 'in')
    mc.text(l = "          SETS  ", fn = "boldLabelFont")
    mc.separator(h = 5, w = 470, st = 'in')
    mc.columnLayout(co = ('left', 10))
    mc.separator(h = 5, w = 470, st = 'none')
    
    
    #creating the menu for each of the bgs in the scene
    
    for l in range(len(setnames)):
        mc.rowLayout(nc = 3, cw3 = (200, 150, 50))
        #name of the bg
        mc.text(l = setnames[l])
        #select button command
        com = "mc.select(\"%s\", r = True)"%setnames[l]
        menulabel = "bgmenu%s"%str(l).zfill(2)
        setopt.append(menulabel)
        #dropdown list for selecting the render layer group that the bg will go into
        mc.optionMenu(menulabel, label = 'Render Grp : ')
        for ll in range(numlayers):
            mc.menuItem( label="ch%s"%str(ll + 1).zfill(2))
        mc.menuItem( label="None")
        #button for selecting the bg
        mc.button(l = "Select", c = com)
        mc.setParent('..')
    mc.separator(h = 5, w = 470, st = 'none')        
    mc.rowLayout(nc = 2, cw2 = (100, 300))
    #button to add a bg that didn't show up in the scan
    mc.button(l = "       Add Set", w = 80, al = "center", c = lambda event:addAsset(2))
    mc.text(label = "Select a group and press button to add the set")
    mc.setParent('..')
    mc.separator(h = 5, w = 470, st = 'none')
    mc.setParent('..')
    mc.separator(h = 5, w = 470, st = 'in')

    
    #creating the light options menu
    
    mc.setParent('ltopts')
    if mc.columnLayout("ltopscol", ex = True):
        mc.deleteUI("ltopscol")
    mc.columnLayout('ltopscol')
    mc.rowLayout(nc = 2)
    mc.rowLayout(nc = 4, cw4 = (39, 39, 39, 39))
    mc.checkBox("selchk", label = "all", v = 1, w = 50, cc = lambda event:chkchange())
    mc.checkBox("keychk", label = "key", v = 1, w = 39)
    mc.checkBox("rimchk", label = "rim", v = 1, w = 39)
    mc.checkBox("colchk", label = "col", v = 1, w = 39)

    mc.setParent('..')
    mc.rowLayout(nc = 4, cw4 = (39, 39, 39,39))
    mc.checkBox("occchk", label = "occ", v = 1, w = 39)
    mc.checkBox("rgbachk",label = "rgba",v = 1, w = 43)
    mc.checkBox("gshchk", label = "gsh", v = 1, w = 39)
    mc.checkBox("matchk", label = "mat", v = 1, w = 39)
    mc.setParent('..')
    mc.setParent('..')
    mc.separator(h = 15, w = 470, st = 'none')
    mc.rowLayout(nc = 3, cw3 = (30,250, 150))
    mc.text(label='')
    #checkbox to query whether the references need to be cut
    mc.checkBox("refchk", label = "Import all references(Cut the references)", v = 0)
    #checkbox to query whether the cameras need to be exported
    mc.checkBox("camchk", label = "Export cameras", v = 0)
    mc.setParent('..')
    mc.separator(h = 15, w = 470, st = 'none')    
    mc.rowLayout(nc = 4, cw4 = (80,90,110,125))
    mc.text(label = "Ambient Light")
    mc.text(label = "     Location")
    mc.text(label = "       Time")
    mc.text(label = "   Render Scene Camera")
    mc.setParent('..')
    mc.separator(h = 5, w = 470, st = 'none')    
    mc.rowLayout(nc = 4, cw4 = (80,100,110,145))
    #dropdown to query what kind of ambient light to use
    mc.optionMenu('amblite', label = '')
    mc.menuItem( label="None")
    mc.menuItem( label="GI")
    mc.menuItem( label="ambient")
    
    #mc.menuItem( label="GILight")
    #dropdown to query which rim/key file to use
    mc.optionMenu('Location', label = '',cc=lambda event:locc())
    for each in ltbgs:
        mc.menuItem( label = each)
    #dropdown to query which time lights to use
    mc.optionMenu('Time', label = '')
    for each in ltlites:
        mc.menuItem( label = each)   
    #list all cameras in the scene to find out renderable camera
    cams = mc.ls(type = "camera")
    rencams = []
    epcams = []
    #list all cameras that are children of 'CAMERAS' group
    if mc.objExists('CAMERAS'):
        epcams = mc.listRelatives('CAMERAS', c = True, ad = True, type = 'camera')
    #find out the scene camera and set it to renderable
    if epcams:
        for each in cams:
            if each in epcams:
                rencams.append(each)
                mc.setAttr((each + ".renderable"), 1)
    if not rencams:
        rencams = cams
    #dropdown to show renderable cameras in the scene. the scene camera will be selected by default
    mc.optionMenu('camlite', label = '',)
    renParentCams = [mc.listRelatives(x, p = True)[0] for x in rencams]
    for each in renParentCams:
        mc.menuItem( label=each)
    mc.optionMenu('camlite', e = True, v = (renParentCams[0]))
    mc.setParent('..')
    #calculate optimum height of UI window based on the number of assets to be processed
    numasts = len(charnames) + len(propnames) + len(setnames)
    if numasts > 12:
        numasts = 12
    scrht = 300 + numasts*25
    winht = 590 + numasts*25
    #edit the window and scrolllayout heights to be the optimum value
    mc.window('liteshot', e = True, wh = (483, winht))
    mc.scrollLayout('scrll',e = True, h = scrht, w = 450, vis = True)



#add assets that weren't picked up in scanScene()
    
def addAsset(ast = 0):
    global adcharnames, adpropnames, adsetnames
    sel = mc.ls(sl = True)
    if not len(sel) == 1:
        mc.confirmDialog(t='Warning', m='Please select one object (only)', b='OK')
        return
    if ast == 0:
        adcharnames.append(sel[0])
    elif ast == 1:
        adpropnames.append(sel[0])
    elif ast == 2:
        adsetnames.append(sel[0])
    scanScene()
    return

    
    
#remove the reference of the BG from the scene    
    
def remBg():
    global charnames, propnames, setnames
    charnames, propnames, setnames = [], [], []
    charnames, propnames, setnames, miscnames = Utils.listAssets()
    for each in setnames:
        refrn = mc.referenceQuery(each, f = True)
        
        refNode=mc.referenceQuery(each,rfn=1)
        if refNode:
            mc.file(rfn=refNode,rr=1)
            refObjs=mc.ls('%s*' % refNode)
            if refObjs:mc.delete(refObjs)
        else:
            mc.file(refrn, rr = True)
    scanScene()  
        
    
def chkchange():
    chks = ['keychk','rimchk','colchk','occchk','rgbachk','gshchk','matchk']
    chkstat = mc.checkBox("selchk", q = True, v = True)
    for each in chks:
        mc.checkBox(each, e = True, v = chkstat)

    
#set up the ground and matte groups    
    
def setupGndMte(grpname):
    objs = mc.ls(sl = True)
    if objs:
        if not mc.objExists(grpname):
            mc.group(n = grpname, em = True)
        for obj in objs:
            dupobj = mc.duplicate(obj, rr = True, n = ("%s_gndmte"%obj))
            attrs = mc.listAttr(dupobj, l = True)
            if attrs:
                for attr in attrs:
                    mc.setAttr((dupobj[0] + "." + attr), l = False)
            mc.parent(dupobj, grpname)
            objShp = mc.listRelatives(dupobj, ad = True, c = True)
            for shp in objShp:
                try:
                    #turn off cast shadows for the ground and matte objects
                    mc.setAttr((shp + ".castsShadows"), 0)
                except:
                    pass
    else:
        mc.confirmDialog(t='Warning', m='No Objects Selected', b='OK')
        return


    
#create red, green and blue matshaders    

def rgbashader(name = "shot"):
    redsh = name + "_redsurfaceshader"
    grnsh = name + "_greensurfaceshader"
    blush = name + "_bluesurfaceshader"
    alpsh = name + "_alphasurfaceshader"
    if not mc.objExists(redsh):
        mc.shadingNode("surfaceShader", asShader = True, n = redsh)
        mc.setAttr((redsh + ".outColor"), 1, 0, 0, type = "double3")
        mc.setAttr((redsh + ".outMatteOpacity"), 0, 0, 0, type = "double3")
    if not mc.objExists(grnsh):
        mc.shadingNode("surfaceShader", asShader = True, n = grnsh)
        mc.setAttr((grnsh + ".outColor"), 0, 1, 0, type = "double3")
        mc.setAttr((grnsh + ".outMatteOpacity"), 0, 0, 0, type = "double3")
    if not mc.objExists(blush):
        mc.shadingNode("surfaceShader", asShader = True, n = blush)
        mc.setAttr((blush + ".outColor"), 0, 0, 1, type = "double3")
        mc.setAttr((blush + ".outMatteOpacity"), 0, 0, 0, type = "double3")
    if not mc.objExists(alpsh):
        mc.shadingNode("surfaceShader",asShader = True, n = alpsh)
        mc.setAttr((alpsh + ".outColor"), 0, 0, 0, type = "double3")
        mc.setAttr((alpsh + ".outMatteOpacity"),1 ,1 ,1, type= "double3")
    return [redsh, grnsh, blush, alpsh]
    
    

#cut reference for the specified node    
    
def cutref(node):
    refnode = mc.referenceQuery(node, rfn = True)
    if refnode:
        reffile = mc.referenceQuery(refnode, f = True)
        mc.file(reffile, ir = True)
    
def setrendglobals(shotname, st, end):
    
    tablayout=mc.setAttr('defaultRenderGlobals.currentRenderer', "mentalRay", type = "string") 
    mel.eval("unifiedRenderGlobalsWindow")
    tablayout = mel.eval('rendererTabLayoutName("mentalRay")')
    mc.tabLayout(tablayout, e = True, sti = 4)
    mel.eval('fillSelectedTabForTabLayout("%s")'%tablayout)
    
    #amb renderpass settings
    mc.createNode('renderPass')
    mel.eval('applyAttrPreset "renderPass1" "C:/Program Files/Autodesk/Maya2011/presets/attrPresets/renderPass/ambient.mel" 1;')
    mc.rename('renderPass1', 'amb')
    mc.setAttr('amb.renderable', 1)
    mc.setRenderPassType('amb', type='AMB')

    #camml renderpass settings
    mc.createNode('renderPass')
    mel.eval('applyAttrPreset "renderPass1" "C:/Program Files/Autodesk/Maya2012/presets/attrPresets/renderPass/incidenceCamNorm.mel" 1;')
    mc.rename('renderPass1', 'camnml')
    mc.setAttr('camnml.renderable', 1)
    mc.setRenderPassType('camnml', type='INCICN')

    
    #diff renderpass settings
    mc.createNode('renderPass')
    mel.eval('applyAttrPreset "renderPass1" "C:/Program Files/Autodesk/Maya2011/presets/attrPresets/renderPass/diffuse.mel" 1;')
    mc.rename('renderPass1', 'diff')
    mc.setAttr('diff.renderable', 1)
    mc.setRenderPassType('diff', type='DIFF')
    

    #nml renderpass settings
    mc.createNode('renderPass')
    mel.eval('applyAttrPreset "renderPass1" "C:/Program Files/Autodesk/Maya2011/presets/attrPresets/renderPass/normalCam.mel" 1;')
    mc.rename('renderPass1', 'nml')
    mc.setAttr('nml.renderable', 1)
    mc.setRenderPassType('nml', type='NORMAL')
    

    #spc renderpass settings
    mc.createNode('renderPass')
    mel.eval('applyAttrPreset "renderPass1" "C:/Program Files/Autodesk/Maya2011/presets/attrPresets/renderPass/specular.mel" 1;')
    mc.rename('renderPass1', 'spc') 
    mc.setAttr('spc.renderable', 1)
    mc.setRenderPassType('spc', type='SPEC')
    
    #sha renderpass settings
    mc.createNode('renderPass')
    mel.eval('applyAttrPreset "renderPass1" "C:/Program Files/Autodesk/Maya2011/presets/attrPresets/renderPass/shadow.mel" 1;')
    mc.rename('renderPass1', 'sha')
    mc.setAttr('sha.renderable', 1)
    mc.setRenderPassType('sha', type='SHD')
    
    #inc renderpass settings
    mc.createNode('renderPass')
    mel.eval('applyAttrPreset "renderPass1" "C:/Program Files/Autodesk/Maya2011/presets/attrPresets/renderPass/incandescence.mel" 1;')
    mc.rename('renderPass1','inc')
    mc.setAttr('inc.renderable',1)
    mc.setRenderPassType('inc',type='INC')

    #Render Globals File ouput settings
    
    mc.setAttr("defaultRenderGlobals.imageFormat", 32)
    mc.setAttr("defaultRenderGlobals.outFormatControl",0)
    mc.setAttr("defaultRenderGlobals.animation",1)
    mc.setAttr("defaultRenderGlobals.putFrameBeforeExt",1)    
    mc.setAttr("defaultRenderGlobals.extensionPadding", 3)
        
    #Render Globals Frame range settings
    
    mc.setAttr("defaultRenderGlobals.startFrame", st)
    mc.setAttr("defaultRenderGlobals.endFrame", end)
    mc.setAttr("defaultRenderGlobals.byFrameStep", 1)
    mc.setAttr ('miDefaultOptions.filter',2)
    mc.setAttr ('miDefaultOptions.rayTracing', 1)
    mc.setAttr ('miDefaultOptions.finalGather', 0)
    mc.setAttr ('miDefaultOptions.jitter', 0)
    mc.setAttr ('mentalrayGlobals.accelerationMethod',3)
    mc.setAttr ('miDefaultOptions.maxSamples',2)
    mc.setAttr ('miDefaultFramebuffer.datatype', 16)
    #Render Globals Renderable camera settings
    
    cam = mc.optionMenu('camlite', q = True, v = True)
    camShp = mc.listRelatives(cam, c = True, s = True)[0]
    for each in mc.ls(type = 'camera'):
        if each == camShp:
            mc.setAttr((each + ".renderable"), 1)
        else:
            mc.setAttr((each + ".renderable"), 0)

            
    #Render Globals Image size settings
    
    mc.setAttr("defaultResolution.width", util.resolWidth)
    mc.setAttr("defaultResolution.height", util.resolHeight)
    mc.setAttr("defaultResolution.deviceAspectRatio", util.aspRto)
    
    
def locc():
    z=mc.optionMenu('Location',q=1,v=1)
    litefldr1 = "%s/%s/Location/%s"%(util.path, util.litePath,z)
    Litefiles1 = os.listdir(litefldr1) 
    ltlites1 = [x.replace('_rimkey.ma', '') for x in Litefiles1]
    list_items = mc.optionMenu('Time',q=1,ils=1)
    for list_it  in list_items :
        mc.deleteUI(list_it)
    for ltl in ltlites1:
        mc.menuItem(label=ltl,p='Time')
#liteShotSetupUI()
