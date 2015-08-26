import maya.cmds as mc
import maya.mel as mel
import subprocess 
import os
from functools import partial

def AnimPoseLib():
    global tabs,Animation,Poses,pathfolders,pathfolder,savepathini,User_Name,tmpfile,seltabs,seltab
    if mc.window ('MainWin',q=True,exists =1):
        mc.deleteUI ('MainWin')
    if mc.windowPref ('MainWin',q=True,exists = 1):
        mc.windowPref ('MainWin',remove = 1)
    posewin=mc.window('MainWin',menuBar=True, title="SR_AnimPoseLib",width=400,mxb=0)
    User_Name = os.getenv('USERNAME')
    savepathini='C:/Documents and Settings/'+ User_Name + '/My Documents/'
    mc.menu( label='File', tearOff=True )
    mc.menuItem( label='Open Savepose Folder',c=lambda event:openfolder(savepathini))
    mc.menuItem( label='Refresh',c=lambda event:Refresh_UI(savepathini))
    mc.menu( label='Tabs', tearOff=True )
    mc.menuItem( label='New Tab',c=partial(Newtab)) 
    mc.menuItem( label='Delete Tab',c=partial(deletetab))
    mc.menuItem( label='Rename Tab',c=partial(renametab))
    mc.menuItem( label='Clear All ',c=partial(clear))
    mc.menu('chgFld',label='Folder',tearOff=True)
    mc.menuItem(label='Change Savepose Folder ',c=lambda event:savefolder(savepathini))
    mc.menuItem(d=True)
    newpath=[savepathini]
    mc.menuItem( label='My Douments ',c=partial(changepath,newpath))       
    mc.menu( label='Help', helpMenu=True,tearOff=True )
    mc.menuItem( label='About..!' ,c=partial(About))
    mc.frameLayout( label='',fn='boldLabelFont', borderStyle='etchedIn')
    mc.separator(style='none',height = 2 )
    mc.rowColumnLayout(numberOfColumns=5,cw=[(1,70),(2,60),(3,70),(4,40),(5,125)],cs=[(1,30),(5,40)])
    mc.text('ST',label='Start frame:')
    Start_F = mc.floatField('Start_F',precision=2)
    mc.text( 'ET',label='End frame:')
    End_F   = mc.floatField('End_F',precision=2)
    mc.floatField('Start_F', edit=True, enterCommand=('mc.setFocus(\"' + End_F + '\")') )
    mc.floatField('End_F', edit=True, enterCommand=('mc.setFocus(\"' + Start_F + '\")') )
    mc.button(label='Save (Anim/Pose)',c=partial(savepose),h=35 )
    mc.setParent( '..' )
    mc.rowColumnLayout(numberOfColumns=2,cw=[(1,130)])
    mc.text(label='Location : ',align='right',fn='boldLabelFont')
    mc.text('Path',label=' Local Folder',align='left',fn='smallFixedWidthFont') 
    mc.setParent( '..' )
    form = mc.formLayout()
    tabs = mc.shelfTabLayout('tabs',innerMarginWidth=5, innerMarginHeight=5,cc=partial(vis))
    mc.formLayout(form,edit=True, attachForm=((tabs, 'top', 0), (tabs, 'left', 15), (tabs, 'bottom', 15), (tabs, 'right', 15)) )
    Animation = mc.shelfTabLayout('Animation',innerMarginWidth=5, innerMarginHeight=5,bgc=(0.3,0.3,0.3),h=237)
    mc.setParent('..')
    Poses = mc.shelfTabLayout('Poses',innerMarginWidth=5, innerMarginHeight=5,bgc=(0.3,0.3,0.3),h=237,p=tabs)
    mc.setParent('..')
    mc.setParent('..')
    mc.setParent('..')    
    mc.text(l='Sreekanth.S.R  ',fn="smallBoldLabelFont",al='right')
    mc.window (posewin,e=1,wh=(500,410))
    mc.showWindow()
    shelfpath=[]
    posepath=[]
    savepath =(savepathini + 'SavePose/')
    mc.sysFile(savepath, makeDir=True )
    shelfpath= mc.getFileList (folder=savepath)
    Anim_count=shelfpath.count('Animation')
    Pose_count=shelfpath.count('Poses')
    Tmp_count =shelfpath.count('tmp.anim')
    if not Tmp_count:
        tmpfile=savepath+'tmp.anim'
        field=open(tmpfile,'w')
        field.write('Currnt dir \n'+savepathini)
        field.close()
    if Tmp_count:
        tmpfile=savepath+'tmp.anim'
        field=open(tmpfile,'r+')
        line=field.readline()
        if line[0:3]=='Cur' :
            line=field.readline()
            savepathini=line.strip()
            line=field.readline()
            if line[0:3]=='Run':
                line=field.readline()
                while(line != '}'):
                    mc.menuItem(label=line.strip(),p='chgFld',c=partial(savedpath,line))    
                    line=field.readline()
                field.close()
    Refresh_UI(savepathini)
             
def Refresh_UI(savepathini,*args):
    mc.text('Path',e=1,l=savepathini)
    S_val=mc.playbackOptions(q=1,min=1)
    E_val=mc.playbackOptions(q=1,max=1)
    mc.floatField('End_F',e=1,v=E_val)
    mc.floatField('Start_F',e=1,v=S_val)
    savepath =(savepathini + 'SavePose/')
    #imgpath  = savepath + 'tmp_images/'
    mc.sysFile(savepath, makeDir=True )    
    posepath = (savepath + 'Animation/')
    posepath1= (savepath + 'Poses/')
    shelfpath= mc.getFileList (folder=savepath)
    Anim_count=shelfpath.count('Animation')
    Pose_count=shelfpath.count('Poses')
    if Anim_count==0 or Pose_count==0:
        mc.confirmDialog (title='Warning',message='No saved poses exist. A Default folders will\n    be created when you save for the first time', button='OK',defaultButton='Yes')
    tabsanim,tabsanim1=[],[]
    tabsanim=mc.getFileList(folder=posepath)
    tabsanim1=mc.getFileList(folder=posepath1)
    Anim_tabs=mc.shelfTabLayout('Animation',q=1,ca=1) 
    Pose_tabs=mc.shelfTabLayout('Poses',q=1,ca=1)
    if Anim_tabs or Pose_tabs :
        mc.deleteUI(Anim_tabs,Pose_tabs) 
    if tabsanim:
        for each in tabsanim:
            sh=mc.shelfLayout(each,p=Animation,st="iconAndTextVertical")
            mc.setParent('..')
            posetabs=(posepath + each + "/")
            poses = mc.getFileList (fld =posetabs,fs="*.anim")
#            imges = mc.getFileList (fld =posetabs,fs="*.bmp")
            icon_name='ghost.xpm'
            for j in range(len(poses)):
                butname = poses[j].replace(".anim","")
                img_name=poses[j].replace(".anim",".bmp")
                icon_name=posetabs + img_name
                posefile = posetabs + poses[j]
                mc.setParent()                
                mc.shelfButton(i1=icon_name,w=110,h=80,l=butname,bgc=(.2,.6,.3),st='iconAndTextVertical',p=each,c=partial(Importanim,posefile))
                mc.popupMenu()
                mc.menuItem(l='Import anim',en=1,c=partial(Importanim,posefile))
                mc.menuItem(d=True)
                mc.menuItem(l='Rename anim',en=1,c=partial(Renameanim,posefile))
                mc.menuItem(d=True)
                mc.menuItem(l='Delete anim',en=1,c=partial(Deleteanim,posefile))
                mc.setParent('..')   
    else:
        if mc.shelfLayout('Default',q=True,exists=True):
            mc.deleteUI ('Default')    
        shelftmp = mc.shelfLayout('Default',w=450,h=200,bgc=(0.3,0.3,0.3),p=Animation)
        mc.sysFile(posepath+'Default/', makeDir=True )         
    if tabsanim1:
        for each in tabsanim1:
            sh=mc.shelfLayout(each,p=Poses,st="iconAndTextVertical")
            mc.setParent('..')
            posetabs1 = (posepath1 + each + "/")
            poses1 = mc.getFileList (fld =posetabs1,fs="*.anim")
            icon_name1='ghostOff.xpm'
            for j in range(len(poses1)):
                butname1 = poses1[j].replace(".anim","")
                img_name1= poses1[j].replace(".anim",".bmp")
                icon_name1=posetabs1 + img_name1
                posefile1 = posetabs1 + poses1[j]
                mc.setParent()
                mc.shelfButton(i1=icon_name1,w=110,h=80,l=butname1,fn=  "fixedWidthFont" ,bgc=(.9, .4, .0),st='iconAndTextVertical',p=each,c=partial(Pose_rtn,posefile1))
                mc.popupMenu()
                mc.menuItem(l='Import Pose',en=1,c=partial(Pose_rtn,posefile1))
                mc.menuItem(d=True)
                mc.menuItem(l='Rename Pose',en=1,c=partial(Renamepose,posefile1))
                mc.menuItem(d=True)
                mc.menuItem(l='Delete Pose',en=1,c=partial(Deletepose,posefile1))
                mc.setParent('..')
    else:
        if mc.shelfLayout('Default1',q=True,exists=True):
            mc.deleteUI ('Default1') 
        shelftmp1 = mc.shelfLayout('Default1',w=450,h=200,bgc=(0.3,0.3,0.3),p=Poses)
        mc.sysFile(posepath1+'Default1/', makeDir=True )

def Newtab(*args):
    sel_tab = mc.shelfTabLayout('tabs',q=1,st=1)
    crnt_tab= mc.shelfTabLayout(sel_tab,q=1,ca=1)
    Newtab = mc.promptDialog(
                    title='Create New Tab',
                    message='New Tab Name:',
                    button=['OK', 'Cancel'],
                    defaultButton='OK',
                    cancelButton='Cancel',
                    dismissString='Cancel')    
    if Newtab == 'OK':
        n_text = mc.promptDialog(query=True, text=True)
        if n_text == '':
            mc.confirmDialog (title='Error' ,message= 'Sorry, The name entered is not valid', button=['OK'] ,defaultButton='Yes')      
        else:
            if crnt_tab:
                for each in crnt_tab:
                    if each == n_text:
                        mc.confirmDialog (title='Error' ,message= 'Sorry, The name entered is already exists', button=['OK'] ,defaultButton='Yes')
                        return 
            #else:     
            if sel_tab == 'Animation':
                Nw_tab=savepathini+'Savepose/Animation/'+n_text+'/'
                mc.shelfLayout(n_text,w=450,h=200,bgc=(0.3,0.3,0.3),p=Animation)
                mc.sysFile(Nw_tab, makeDir=True )
                     
            else:
                mc.shelfLayout(n_text,w=450,h=200,bgc=(0.3,0.3,0.3),p=Poses)
                Nw_tab=savepathini+'Savepose/Poses/'+n_text+'/' 
                mc.sysFile(Nw_tab, makeDir=True )
            mc.shelfTabLayout(sel_tab,e=1,st=n_text)
                    
def deletetab(*args):
    alltabs = mc.tabLayout ('tabs',q=1,st=1)
    chktabs = mc.tabLayout ('Animation',q=1,st=1)
    chktabs1= mc.tabLayout ('Poses',q=1,st=1)
    if alltabs == 'Animation':
        seltab = mc.tabLayout('Animation',q=1,st=1) 
        mc.deleteUI(seltab)
        Del_tab=savepathini+'Savepose/Animation/'+seltab
        Del1_in=Del_tab+'/'
        list_in=mc.getFileList(fld=Del1_in)
        for i in range(len(list_in)):
            mc.sysFile(Del1_in+'/'+list_in[i],delete=1)
        mc.sysFile(Del_tab,red=1)
        if chktabs=='':
            mc.confirmDialog (title='Error',message='No tabs to delete', button='OK',defaultButton='Yes')    
#        else :
#            return
    else :
        seltab = mc.tabLayout('Poses',q=1,st=1) 
        mc.deleteUI(seltab)
        Del_tab=savepathini+'Savepose/Poses/'+seltab
        Del1_in=Del_tab+'/'
        list_in=mc.getFileList(fld=Del1_in)
        for i in range(len(list_in)):
            mc.sysFile(Del1_in+'/'+list_in[i],delete=1)
        mc.sysFile(Del_tab,red=1)
        if chktabs1=='':
            mc.confirmDialog (title='Error',message='No tabs to delete', button='OK',defaultButton='Yes')    
        else :
            return          
    
def renametab(*args):
    seltab = mc.tabLayout('tabs',q=1,st=1) 
    alltabs = mc.tabLayout('Animation',q=1,st=1)
    alltabs1 = mc.tabLayout('Poses',q=1,st=1)
    if seltab == 'Animation':        
        if alltabs=='':
            mc.confirmDialog (title='Error',message='No tabs to rename', button='OK',defaultButton='Yes')
        else:
            newname = mc.promptDialog(
                    text=alltabs,
                    title='Rename Tab',
                    message='New Tab Name:',
                    button=['OK', 'Cancel'],
                    defaultButton='OK',
                    cancelButton='Cancel',
                    dismissString='Cancel')
            if newname == 'OK':
                newtabname = mc.promptDialog (query=True, text=True)
                if newtabname =='':
                    mc.confirmDialog (title='Error' ,message= 'Sorry, The name entered is not valid', button=['OK'] ,defaultButton='Yes')
                    return
                else :
                    oldname = mc.tabLayout('Animation',q=1,st=1)
                    mc.tabLayout ('Animation',e=True,tl=((oldname, newtabname)))
                    Ren_tab =savepathini+'Savepose/Animation/'+oldname
                    Ren_tab1=savepathini+'Savepose/Animation/'+newtabname
                    mc.sysFile(Ren_tab,rename=Ren_tab1)
                    return
            else:
                return        
    else:
        if alltabs1 == '':
            mc.confirmDialog (title='Error',message='No tabs to rename', button='OK',defaultButton='Yes')    
        else:
            newname = mc.promptDialog(
                    title='Rename Tab',
                    message='New Tab Name:',
                    tx = alltabs1,
                    button=['OK', 'Cancel'],
                    defaultButton='OK',
                    cancelButton='Cancel',
                    dismissString='Cancel')
            if newname == 'OK':
                newtabname = mc.promptDialog (query=True, text=True)       
                if newtabname =='':
                    mc.confirmDialog (title='Error' ,message= 'Sorry, The name entered is not valid', button=['OK'] ,defaultButton='Yes')
                    return
                else:
                    oldname = mc.tabLayout('Poses',q=1,st=1)
                    mc.tabLayout ('Poses',e=True,tl=((oldname, newtabname)))
                    Ren_tab =savepathini+'Savepose/Poses/'+oldname
                    Ren_tab1=savepathini+'Savepose/Poses/'+newtabname
                    mc.sysFile(Ren_tab,rename=Ren_tab1)
                    return
            else:
                return

def savepose(*args):
    alltab  = mc.tabLayout('tabs',q=1,st=1)
    chktabs = mc.tabLayout ('Animation',q=1,st=1)
    chktabs1= mc.tabLayout ('Poses',q=1,st=1)
    sel_obj = mc.ls(sl=1)
    if len(sel_obj)==0:
        mc.confirmDialog (title = "Error",message ="Nothing is selected",button= "OK",defaultButton ="Yes")
    else :
        if alltab=='Animation':
            if chktabs=='':
                mc.confirmDialog (title = "Error",message ="Please create a tab first",button= "OK",defaultButton ="Yes")
            else:
                Animname = mc.confirmDialog(
                title='Frame chk',
                message='Pls chk : Start frame and End frame ',
                button=['OK', 'Cancel'],
                defaultButton='OK',
                cancelButton='Cancel',
                dismissString='Cancel')
                if Animname =='OK': 
                    Animposecam(sel_obj)  
        else:
            if chktabs1=='':
                mc.confirmDialog (title = "Error",message ="Please create a tab first",button= "OK",defaultButton ="Yes")
            else:
                Animposecam(sel_obj)
def Animposecam(sel_obj):
#    if mc.objExists('poseLibCaptureCamera'):
#        mc.delete('poseLibCaptureCamera')
    if not mc.objExists('poseLibCaptureCamera'):
        CurrentPanel  = mc.getPanel(withFocus=True)
        #print CurrentPanel
        if mc.getPanel(to=CurrentPanel!= "modelPanel") :   
            visPanel  = mc.getPanel(vis=True)    
            for name in visPanel:
                modelPanels= mc.getPanel(type= 'modelPanel')    
                if mc.getPanel (to = name == "modelPanel"):
                    mc.setFocus(name)
                    CurrentPanel = name
                    break
        if mel.eval('catch(`modelPanel -q -cam %s`)'%CurrentPanel):
            CurrentCamera = "persp"
        else:
            CurrentCamera = mc.modelPanel(CurrentPanel,q=1,cam=1)
        
        campos= mc.camera(CurrentCamera,q=1,position=1)
        camrot= mc.camera(CurrentCamera,q=1,rotation=1) 
        camwup= mc.camera(CurrentCamera,q=1,worldUp =1)
        camcoi= mc.camera(CurrentCamera,q=1,coi=1)
        focal = mc.camera(CurrentCamera,q=1,fl=1) 
        camShapeNode = mc.createNode("camera")
        camTopNode   = mc.listRelatives(camShapeNode,p=1) 
        mc.rename (camTopNode[0] ,'poseLibCaptureCamera')
        mc.hide('poseLibCaptureCamera')
        focalLengthTmp = 200
        nearClipTmp = .1
        farClipTmp = 10000
        mc.camera('poseLibCaptureCamera',e=1,
                position =[campos[0],campos[1],campos[2]],
                rotation =[camrot[0],camrot[1],camrot[2]],                 
                worldUp  =[camwup[0],camwup[1],camwup[2]],
                fl = focalLengthTmp,
                nearClipPlane = nearClipTmp,
                farClipPlane = farClipTmp)
    AnimposeCreateWindow(sel_obj)
    
def Anim_obj1(Animpose_name,currentImagePath):
    Val1=mc.floatField('Start_F',q=1,v=1)
    Val2=mc.floatField('End_F',q=1,v=1)
    Val1=str(Val1);Val2=str(Val2)
    frm_rang="("+str(Val1)+'-'+str(Val2)+")"
    frameNumber = mc.currentTime(q=1)
    frameNumber =int(frameNumber)
    iconTmp = currentImagePath + "iconTmp." + str(frameNumber)+ ".bmp" 
    print ("\niconTmp = " + iconTmp)
    Currnt_path=savepathini+'SavePose/'
    Anim_newname=Animpose_name+frm_rang
    testpath = savepathini
    seltab5  = mc.shelfTabLayout('Animation',q=1,st=1)
    animpath = (testpath + 'SavePose/Animation/'+seltab5+'/')               
    animpath1= animpath 
    animpath2= animpath1 + Anim_newname + '.anim'
    newAnimIconFile = animpath1 + Anim_newname +".bmp"
    if mc.file(animpath2,q=1,ex=1):
        Overrite = mc.confirmDialog(
                title='Confirm Save Anim',
                message='Overwrite the existing anim: '+Anim_newname+'?',
                button=['Yes', 'No'],
                defaultButton='Yes',
                cancelButton='No',
                dismissString='No') 
        if Overrite =='No':   
            return
    mc.sysFile(iconTmp,copy=newAnimIconFile)
    
    
    sel_obj  = mc.ls(sl=1) 
    chkanim=mc.listConnections(sel_obj,t='animCurve',d=0)
    if chkanim==None:
        mc.confirmDialog (title='Error' ,message= 'Selected object has no anim', button=['OK'] ,defaultButton='Yes')
        return    
    print '\nWriting Animation Curves...\n'
    fileID = open(animpath2,'w')
    fileID.write('#Generated by Anim_Poselib.py\n#\n#poselib written by Sreekanth.S.R\n#sree.animator@gmail.com\n#\n')
    if ":" in sel_obj[0]: 
        ref_name = sel_obj[0].split(':')[0]
    else:
        ref_name = sel_obj[0]
    fileID.write('Asst_name '+ ref_name+'\n')
    fileID.write('frameRange '+Val1+'\n')
    for item in sel_obj:
        shortItem= mc.ls(item,sl=1)
        channels = mc.listConnections(item,t='animCurve', d = 0)
        if channels:
            for chan in channels:
                connects= mc.listConnections(chan,p=1)
                curattr = connects[0].split('.')
                num = len(curattr)
                buffer=curattr
                num = num - 1
                node=''
                for i in range(num):
                    if i==0:
                        node=buffer[i]
                    else:
                        node=node+'.'+buffer[i]
                nodeTemp=[]
                nodeTemp = mc.ls(node)
                attr = buffer[num]
                node = nodeTemp[0]
                nodeTemp = mc.listRelatives(node,p=1)
                if nodeTemp != None :
                    parent1 = 1
                elif nodeTemp == None :
                    parent1 = 0
                testit =mc.listAnimatable(connects)
#                if Val1==Val2:   
#                    testit2=mc.keyframe(chan,q=1)
#                else:
                testit2=mc.keyframe(chan,q=1,time=(Val1,Val2))
                if testit and testit2:
                    evalme = mc.getAttr(chan + '.preInfinity')       
                    if evalme == 0:
                        preIn = 'constant'
                    if evalme == 1:
                        preIn = 'linear'
                    if evalme == 2:
                        preIn = 'constant'
                    if evalme == 3:
                        preIn = 'cycle'
                    if evalme == 4:
                        preIn = 'cycleRelative'
                    if evalme == 5:
                        preIn = 'oscillate'
                    evalme = mc.getAttr (chan + '.postInfinity')
                    if evalme == 0:
                        postIn = 'constant'
                    if evalme == 1:
                        postIn = 'linear'
                    if evalme == 2:
                        postIn = 'constant'
                    if evalme == 3:
                        postIn = 'cycle'
                    if evalme == 4:
                        postIn = 'cycleRelative'
                    if evalme == 5:
                        postIn = 'oscillate'
                    evalme = mc.getAttr (chan + '.weightedTangents')
                    weighted = evalme
                    fileID.write('anim ' + attr + ' ' + attr + ' ' + node + ' ' + str(parent1) + ' 0 0\n' )
                    fileID.write('animData \n')
                    fileID.write('  weighted ' + str(weighted) + '\n')
                    fileID.write('  preInfinity ' + preIn  + '\n')
                    fileID.write('  postInfinity ' + postIn + '\n')
                    fileID.write('  keys {\n')
                    
                    breakDown=[]
#                    if Val1==Val2:
#                        keys   = mc.keyframe(chan,q=1)
#                        values = mc.keyframe (chan,q=1,vc=1)
#                        inTan  = mc.keyTangent(chan,q=1,itt=1)
#                        outTan = mc.keyTangent(chan,q=1,ott=1) 
#                        tanLock= mc.keyTangent (chan,q=1,lock=1)
#                        weightLock=mc.keyTangent(chan,q=1,weightLock=1)
#                        breakDown= mc.keyframe (chan,q=1,breakdown=1)
#                        inAngle= mc.keyTangent (chan,q=1,inAngle=1)
#                        outAngle= mc.keyTangent (chan,q=1,outAngle=1)
#                        inWeight= mc.keyTangent (chan,q=1,inWeight=1)
#                        outWeight= mc.keyTangent (chan,q=1,outWeight=1)
#                    else:
                    keys   = mc.keyframe(chan,q=1,time=(Val1,Val2))
                    values = mc.keyframe (chan,q=1,vc=1,time=(Val1,Val2))
                    inTan  = mc.keyTangent(chan,q=1,itt=1,time=(Val1,Val2))
                    outTan = mc.keyTangent(chan,q=1,ott=1,time=(Val1,Val2)) 
                    tanLock= mc.keyTangent (chan,q=1,lock=1,time=(Val1,Val2))
                    weightLock=mc.keyTangent(chan,q=1,weightLock=1,time=(Val1,Val2))
                    breakDown= mc.keyframe (chan,q=1,breakdown=1,time=(Val1,Val2))
                    inAngle= mc.keyTangent (chan,q=1,inAngle=1,time=(Val1,Val2))
                    outAngle= mc.keyTangent (chan,q=1,outAngle=1,time=(Val1,Val2))
                    inWeight= mc.keyTangent (chan,q=1,inWeight=1,time=(Val1,Val2))
                    outWeight= mc.keyTangent (chan,q=1,outWeight=1,time=(Val1,Val2))                                
                        
                    for i in range (len(keys)):
                        bd=0
                        if breakDown!=None:
                            for bd_item in breakDown:
                                if bd_item == keys[i]:
                                    bd=1
                        fileID.write('    ' + str(keys[i]) + ' ' + str(values[i])+ ' ' + str(inTan[i]) + ' ' + str(outTan[i]) + ' ' + str(tanLock[i]) + ' ' + str(weightLock[i]) + ' ' + str(bd))
                        if inTan[i]=='fixed':
                            fileID.write(' ' + str(inAngle[i]) + ' ' + str(inWeight[i])) 
                        if outTan[i]=='fixed':
                            fileID.write(' ' + str(outAngle[i]) + ' ' + str(outWeight[i]))
                        fileID.write('\n')
                    fileID.write('  }\n}\n')
        staticChans = mc.listAnimatable(item)
        for staticChan in staticChans:
            curAttr =  staticChan
            curattr = curAttr.split('.')
            num = len(curattr)
            buffer=curattr
            num = num - 1
            node=''
            for i in range(num):
                if i==0:
                    node=buffer[i]
                else:
                    node=node+'.'+buffer[i]
            nodeTemp=[]
            nodeTemp = mc.ls(node)
            attr = buffer[num]
            node = nodeTemp[0]
            nodeTemp = mc.listRelatives(node,p=1)
            if nodeTemp != None :
                    parent1 = 1
            elif nodeTemp == None :
                    parent1 = 0
            staticChan = (node + "." + attr)
            testit = mc.keyframe (staticChan,q=1)
            connected = mc.listConnections(staticChan,d=0)              
            if not testit and not connected : 
                fileID.write('static ' + attr + ' ' + attr + ' ' + node + ' ' + str(parent1) + ' ' + str(mc.getAttr(staticChan)) + '\n')                
    fileID.write('End of Anim')
    fileID.close()
    mc.select(clear = True)
    for item in sel_obj:
        mc.select(item, toggle = True)
    print "\nDone Writing Animation Curves\n"
    #print frm_rang
    mc.shelfButton(Anim_newname,i1=newAnimIconFile,w=110,h=80,l=Anim_newname,bgc=(.2,.6,.3),st='iconAndTextVertical',p=(seltab5),c=partial(Importanim,animpath2))
    Refresh_UI(savepathini)
    mc.shelfTabLayout('tabs',e=1,st=Animation)   
    mc.shelfTabLayout('Animation',e=1,st=seltab5)
    animposewinclose()
def AnimposeCreateWindow(sel_obj):
    alltab  = mc.tabLayout('tabs',q=1,st=1)
    if mc.window ('AnimposeCreateWindow',q=True,exists =1):
        mc.deleteUI ('AnimposeCreateWindow')
        
    AnimposeCreateWindow=mc.window('AnimposeCreateWindow',menuBar=True, title="AnimPoseCreate",width=302,h=100)
    poseLibCaptureCamera='poseLibCaptureCamera'
    
    mc.columnLayout ()   
    mc.rowLayout('iconCaptureRL',nc=4,cw4=[150,1,1,150])
    captureCamFrame=mc.frameLayout(borderStyle="etchedOut" ,cl=False,cll=False,labelVisible=False,m=True,w=150,h=100) 
    
    if not mc.modelPanel('plCaptureMP',q=1,ex=1):
        mc.modelPanel('plCaptureMP',parent=captureCamFrame,mbv=0,cam=poseLibCaptureCamera)
    else:
        mc.modelPanel('plCaptureMP',e=1,parent=captureCamFrame,mbv=0,cam=poseLibCaptureCamera)
        
    barLayout = mc.modelPanel('plCaptureMP',q=1,barLayout=1)
    if ("" != barLayout and mc.frameLayout(barLayout,q=1,exists=1)):
        mc.frameLayout(barLayout,e=1,collapse=1) 
        mc.control(barLayout,e=1,m=0) 
    modelEditor = mc.modelPanel('plCaptureMP',q=1,me=1)
    mc.modelEditor(modelEditor,e=1,da="smoothShaded",grid=False,hud=False,manipulators=False,displayTextures=True ,ha=0,j=0,dim=0,nc=0,wos=0,dl="default" )
    mc.setParent('..')
    mc.setParent('..')
    mc.frameLayout('glRenderFrame',borderStyle="etchedOut",cl=False,cll=False,m=0,labelVisible=False)
    mc.glRenderEditor('hardwareRenderViewBis')
    mc.setParent ('..')
    mc.frameLayout(borderStyle="etchedIn" ,cl=False,cll=False,labelVisible=False,m=True,w=200,h=100)
    mc.rowLayout(nc=2,cw2=[50,100])
    mc.text(l='   Name :',)
    Anim_name=mc.textField('Anim_name',w=140)
    mc.setParent('..')
    mc.button(l='Create '+alltab[:4],al='center',w=150,c=creation)
    mc.button(l='Cancel',c=partial(animposewinclose))
    mc.setParent('..')
    mc.modelEditor(modelEditor,e=1,camera=poseLibCaptureCamera) 
    mc.setAttr("poseLibCaptureCameraShape.displayFilmGate", 1)
    mc.setAttr("poseLibCaptureCameraShape.verticalFilmAperture",1.1)

    mc.glRenderEditor('hardwareRenderViewBis',e=1,lt=poseLibCaptureCamera) 
    #if not mc.objExists(poseLibCaptureCamera):
       #poseLibCaptureCamera='persp'
        
    mc.showWindow(AnimposeCreateWindow)
    mc.window(AnimposeCreateWindow,e=1,w=300,h=100)
    mc.select(sel_obj)
def creation(tst):
    createIcon()
    mc.evalDeferred(partial(AnimposeLibCreate))
def AnimposeLibCreate():
    alltab  = mc.tabLayout('tabs',q=1,st=1)
    Animpose_name=mc.textField('Anim_name',q=1,tx=1)
    current_img_path=mc.workspace(q=1,fullName=1)
    imagesDir = mc.workspace('images',q=1,renderTypeEntry=1)
    numTokens = len(imagesDir.split( ":"))
    if numTokens == 1:
        currentImagePath = current_img_path + "/" + imagesDir + "/"   
    else:
        currentImagePath = imagesDir + "/"
    if Animpose_name:
        if alltab == 'Animation':
            #createIcon(Animpose_name,alltab)
            Anim_obj1(Animpose_name,currentImagePath)
        else:
            #createIcon(Animpose_name)
            Pose_obj1(Animpose_name,currentImagePath)
    else:
        mc.confirmDialog (title='Error' ,message= 'Sorry, The name entered is not valid', button=['OK'] ,defaultButton='Yes')
def createIcon():
    frameNumber = mc.currentTime (q=1)
    mc.setAttr("defaultHardwareRenderGlobals.startFrame",l=False)
    mc.setAttr("defaultHardwareRenderGlobals.endFrame",l=False)
    mc.setAttr("defaultHardwareRenderGlobals.byFrame",l=False)

    mc.setAttr("defaultHardwareRenderGlobals.startFrame",frameNumber)
    mc.setAttr("defaultHardwareRenderGlobals.endFrame" ,frameNumber)
    mc.setAttr("defaultHardwareRenderGlobals.extension",1)      
    mc.setAttr("defaultHardwareRenderGlobals.backgroundColor", 0.75 ,0.75 ,0.75,type='double3')
    mc.setAttr("defaultHardwareRenderGlobals.imageFormat",20)

    poseLibCaptureCameraBGColor = ( 0.75,0.75,0.75 )
    poseLibIconsSize = ( 104, 82 )
    poseLibIconsBGColor = (.4, .4, .5)
    
    currentBGColor = mc.displayRGBColor('background',q=1)
    mc.displayRGBColor('background',poseLibCaptureCameraBGColor[0],poseLibCaptureCameraBGColor[1],poseLibCaptureCameraBGColor[2])

    # Here we set the default hardware render globals resolution and aspect ratio.
    mc.setAttr('defaultHardwareRenderGlobals.filename',"iconTmp",type="string")
    mc.setAttr('defaultHardwareRenderGlobals.resolution','104x82 104 82 0',type="string")

    # Do the render.
    

    # Here we resize the gl frame to match the correct render resolution.
    mc.frameLayout('glRenderFrame',e=1,m=1,width=(poseLibIconsSize[0]+2),height=(poseLibIconsSize[1]+2))
    #mc.rowLayout(iconCaptureRL,e=1,cw=[2,106])

    # Look through the poseLib camera we just created.
    mc.glRenderEditor('hardwareRenderViewBis',e=1,lt='poseLibCaptureCamera')

    # Warning: This crashes Maya in certain scenes: 2600/4, or 1402/25, or 702/68.
    #mc.glRender(e=1,cf=frameNumber,accumBufferPasses=4,transformIcons= 0,edgeSmoothness=1.0,aam="gaussian")
    mc.glRender(rs='hardwareRenderViewBis')

    # Put back the background color the way it was.
    mc.displayRGBColor ("background",currentBGColor[0],currentBGColor[1],currentBGColor[2])
    print 'Icon Creation Done...'
    
    
#    if alltab == 'Animation':
#        Anim_obj1(Animpose_name)
#    else:
#        Pose_obj1(Animpose_name)
   # mc.window ('AnimposeCreateWindow',e=True,vis=0)
def animposewinclose(*args):
    if mc.window ('AnimposeCreateWindow',q=True,exists =1):
        mc.deleteUI ('AnimposeCreateWindow')
                    
def Pose_obj1(Animpose_name,currentImagePath):
    frameNumber = mc.currentTime(q=1)
    frameNumber =int(frameNumber)
    iconTmp = currentImagePath + "iconTmp." + str(frameNumber)+ ".bmp" 
    print ("\niconTmp = " + iconTmp)
    Currnt_path=savepathini+'SavePose/'
    newposename=Animpose_name
    seltab1 = mc.shelfTabLayout('Poses',q=1,st=1)
    posefold=savepathini+'SavePose/Poses/'+seltab1+'/'+ newposename+'.anim'
    poseimg_path=savepathini+'SavePose/Poses/'+seltab1+'/'
    newPoseIconFile = poseimg_path + newposename +".bmp"
    if mc.file(posefold,q=1,ex=1):
        Overrite = mc.confirmDialog(
                title='Confirm Save Pose',
                message='Overwrite the existing pose: '+newposename+'?',
                button=['Yes', 'No'],
                defaultButton='Yes',
                cancelButton='No',
                dismissString='No') 
        if Overrite =='No':   
            return
    mc.sysFile(iconTmp,copy=newPoseIconFile)  

    files=open(posefold,'w')
    sel_obj  = mc.ls(sl=1)
    for each in sel_obj:
        splitter = each.split(':')
        attrs =mc.listAttr(each,k=1,u=1)
        if(len(attrs)>0):
            if len(splitter)==1:
                files.write('obj '+splitter[0]+'\n')
            else:    
                files.write('obj '+splitter[1]+'\n')    
            for eachattr in attrs:
                locked = mc.getAttr((each+'.'+eachattr),l=1)
                if not locked:
                    valStr = mc.getAttr((each+'.'+eachattr))
                    files.write(eachattr + " " +str(valStr) + '\n')   
    files.close()
    print "Pose Saved" 
                         
    mc.shelfButton(newposename,i=newPoseIconFile,w=110,h=80,l=newposename,bgc=(.6, .2, .2),st='iconAndTextVertical',p=(seltab1),c=partial(Pose_rtn,posefold))
    Refresh_UI(savepathini)
    mc.shelfTabLayout('tabs',e=1,st=Poses)   
    mc.shelfTabLayout('Poses',e=1,st=seltab1)       
    animposewinclose()
            #return
def Pose_rtn(name,*args):
    lst=mc.ls(sl=1)
    if lst==[]:
        mc.confirmDialog (title='About' ,message= 'Nothing is selected',ma='center', button=['OK'] ,defaultButton='Yes')
    else:
        files=open(name,'r')
        nextLine=files.readline()
        sel_obj  = mc.ls(sl=1)
        char = sel_obj[0].split(':')
        while (len( nextLine ) > 0 ):
            splitter= nextLine.split(' ')    
            if splitter[0]=='obj':
                obj_name= splitter[1].strip() 
            else:
                attr = splitter[0]
                value= splitter[1].strip()
                if len(char)==1:
                    added=char[0]+ "." + attr        
                else:
                    added= (char[0] + ":" + obj_name + "." + attr)    
                setA = "mc.setAttr('"+added+"',"+ value+')'
                try:
                    eval(setA)
                except RuntimeError:
                    pass
            nextLine=files.readline()       
        files.close()
        print "Pose changed"
  
           
def NoTab(tabname):
    mc.confirmDialog (title = "Error",message ="No "+ tabname +" exist in the selected tab",button= "OK",defaultButton ="Yes")

def vis(*args):
    select_tab=mc.shelfTabLayout('tabs',q=1,sti=1)
    
    if select_tab==2:
        mc.text('ST',e=1,en=0)
        mc.text('ET',e=1,en=0)
        mc.floatField('Start_F',e=1,en=0)
        mc.floatField('End_F',e=1,en=0)
        
    else:
        mc.text('ST',e=1,en=1)
        mc.text('ET',e=1,en=1)
        mc.floatField('Start_F',e=1,en=1)
        mc.floatField('End_F',e=1,en=1)
        
def clear(*args):
    posesel=[]
    seltab = mc.shelfTabLayout('tabs',q=1,st=1)
    seltab1= mc.shelfTabLayout(seltab,q=1,st=1)
    seltab2= mc.shelfLayout(seltab1,q=1,ca=1)
    
    if seltab2==None :
        NoTab(seltab)
    else:
        confirm=mc.confirmDialog(message='Do you want to delete all '+seltab+' in the selected tab ?', 
            ma='center', button=['Yes','No'] ,defaultButton='Yes',cancelButton='No',dismissString='No')
        if confirm=='Yes':
            seltab1= mc.shelfTabLayout(seltab,q=1,st=1)
            #seltab2= mc.shelfLayout(seltab1,q=1,ca=1)
            posesel= mc.shelfLayout(seltab1,q=1,ca=1)
            for i in range (len(posesel)):
                    print posesel[i]            
                    mc.deleteUI(posesel[i])
                #return
            deletefold=savepathini+'savepose/'+seltab+'/'+seltab1+'/'
            seltab1= mc.shelfTabLayout(seltab,q=1,st=1)
            list_in=mc.getFileList(fld=deletefold)
            for i in range(len(list_in)):
                mc.sysFile(deletefold+list_in[i],delete=1)

def openfolder(savepathini,*args):
    open = savepathini
    fold = (open + 'SavePose')
    pathfold = fold.replace('/', '\\')             
    subprocess.Popen('explorer "%s"'%pathfold)
    
def About(*args):
    mc.confirmDialog (title='About' ,message= 'Script: SR_AnimPoseLib.py\nAuthor: SREEKANTH.S.R\nsree.animator@gmail.com\nCopyright 2013 (C) Sreekanth\nAll Rights Reserved.\nThanx to All Rnd Members',
        ma='center', button=['OK'] ,defaultButton='Yes')

def Importanim(posefile,*args):
    lst=mc.ls(sl=1)
    if lst==[]:
        mc.confirmDialog (title='About' ,message= 'Nothing is selected',ma='center', button=['OK'] ,defaultButton='Yes')
    else:
        Currnt_time = mc.currentTime(q = True)
        imp_name1=lst[0].split(':')[0]
        imp_name =imp_name1
        filename = open(posefile,'r+')
        lines = filename.readlines()
        astName=''
        for line in lines:
            if 'Asst_name' in line:
                astName=line.split(' ')[1].strip()
            elif 'frameRange' in line:
                range  =line.split(' ')[1].strip()
        filename.close()
        print 'range '+range
        offset = Currnt_time - float(range)
        print offset
        filename = open(posefile,'r+')                 
        print "\nReading Animation Curves\n"
        endit = 0
        line1 = filename.readline()
        postI='constant';preI='constant'
        while(line1 != 'End of Anim'):
            line1 = filename.readline()
            wrd=line1.split()
            if line1 [0:5] == "anim " or line1 [0:6]== "static":
                repl_wrd=wrd[3].replace(astName,imp_name)
                curAttr=repl_wrd+'.'+wrd[1]
                node=repl_wrd;attr=wrd[1];endit=0 
                curAttrLong = (node + "." + attr)
                if mc.objExists(node):
                    test2 = mc.ls (curAttrLong)
                    if len(test2)>0:
                        if line1 [0:6]== "static":
                            connected = mc.listConnections (curAttrLong,d=0)
                            if (mc.getAttr(curAttrLong,l=1)== 0 and connected == None):
                                setMe = ("mc.setAttr('" + curAttrLong + "'," + wrd[5] + ")")
                                eval(setMe)
                            else:
                                print ("Warning: Attribute is locked - " + curAttr + "\n")
                        elif line1 [0:5] == "anim ":
                            while (endit == 0):
                                line1 = filename.readline()
                                if line1 [2:11]=='weighted ':
                                    if line1 [11:12]=='T':
                                        weighted = mc.keyTangent(curAttr,e=1,weightedTangents=1) 
                                        weightState = 1
                                    else:
                                        weightState = 0
                                if line1 [2:7]=='preIn':
                                        wrd=line1.split()
                                        preI=wrd[1]
                                if line1 [2:8]=='postIn':
                                        wrd=line1.split()
                                        postI=wrd[1]
                                if line1 [2:6]=='keys':
                                        line1 = filename.readline()
                                        while (line1 != "}"):
                                            try:
                                                wrd=line1.split()
                                                if not wrd[0] == "}":
                                                    frameTime = float(wrd[0])                   
                                                timediff = offset + frameTime
                                                time = timediff   
                                                value = wrd[1]
                                                inType = wrd[2]
                                                outType = wrd[3]
                                                tanLock = wrd[4]
                                                weightLock = wrd[5]
                                                breakDown = 0
                                                tan1=0
                                                tan2=0
                                                weight1=0
                                                weight2=0
                                                wrd_len=len(wrd)
                                                if wrd_len==7:
                                                    breakDown = wrd[6]
                                                else:
                                                    breakDown = wrd[6]
                                                    if wrd_len>7:
                                                        tan1 = wrd[7]
                                                        weight1=wrd[8]
                                                    if wrd_len>9:
                                                        tan2 = wrd[9]
                                                        weight2=wrd[10]
                                                mc.setKeyframe(curAttr,time=time,value=float(value),bd=int(breakDown))
                                                mc.keyTangent(curAttr,lock=bool(tanLock),t=(time,time))
                                                if weightState == 1 :
                                                            mc.keyTangent(curAttr,t=(time,time),weightLock=int(weightLock))
                                                if inType != "fixed" and outType != "fixed":
                                                            mc.keyTangent(curAttr,e=1,a=1,t=(time,time),itt=inType,ott=outType)
                                                if inType == "fixed" and outType != "fixed":
                                                            mc.keyTangent(curAttr,e=1,a=1,t=(time,time),inAngle=tan1,inWeight=float(weight1),itt=inType,ott=outType) 
                                                if inType != "fixed" and outType == "fixed":
                                                            mc.keyTangent(curAttr,e=1,a=1,t=(time,time),outAngle=tan1,inWeight=float(weight1),itt=inType,ott=outType)
                                                if inType == "fixed" and outType == "fixed":
                                                            mc.keyTangent(curAttr,e=1,a=1,t=(time,time),inAngle=tan1,inWeight=float(weight1),outAngle=tan2,outWeight=float(weight2),itt=inType,ott=outType)
                                                line1 = filename.readline()
                                            except IndexError:
                                                break
                                        mc.setInfinity(curAttr,poi=postI,pri=preI)
                                        endit=1
                    else:
                        print 'Warning:'+curAttrLong+ ' Does not exist..Skipping'
                else:
                    print 'Warning:'+wrd[3]+ ' Does not exist..Skipping'                                                                                                  
            
        filename.close()
        mc.select(clear = True)
        print "\nDone Reading Animation Curves\n"
        
def Renameanim(posefile,*args):
    filename = os.path.basename(posefile).split('.')[0]
    dirname  = os.path.dirname(posefile)
    seltab   = mc.shelfTabLayout('Animation',q=1,st=1)
    AnimRename = mc.promptDialog(
                    title='AnimRename',
                    message='AnimRename:',
                    text = filename,
                    button=['OK', 'Cancel'],
                    defaultButton='OK',
                    cancelButton='Cancel',
                    dismissString='Cancel') 
    if AnimRename=='OK':   
        newanimname = mc.promptDialog (query=True, text=True)         
        renamanim= dirname+'/'+ newanimname+'.anim'       
        renamimag= dirname+'/'+ newanimname+'.bmp'
        animimg  = posefile.replace('.anim','.bmp')
        print animimg
        mc.sysFile(posefile,rename= renamanim)
        mc.sysFile(animimg,rename= renamimag)
        Refresh_UI(savepathini)
        print'Anim name changed succesfully'
    else:
        return
    mc.shelfTabLayout('Animation',e=1,st=seltab)    

def Deleteanim(posefile,*args):
    confirm=mc.confirmDialog (title='Confirm Delete pose',message='    Are you sure......?',ma='right',button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No')
    if confirm=='Yes':
        seltab   = mc.shelfTabLayout('Animation',q=1,st=1)
        imgpose  = posefile.replace('.anim','.bmp')
        mc.sysFile(posefile,delete=1)
        mc.sysFile(imgpose,delete=1)
        filename = os.path.basename(posefile).split('.')[0]
        Refresh_UI(savepathini)
        print filename + ' anim deleted..'
        mc.shelfTabLayout('Animation',e=1,st=seltab)

def savefolder(savepathini):
    newpath=mc.fileDialog2(ds = 1, fm = 3)
    if newpath:
        chkpath= newpath[0]+'/'
        counts=mc.getFileList (folder=chkpath)
        nc=counts.count('SavePose')
        if not nc:
            cofirm_but=mc.confirmDialog( title='Confirm', message='Do u want to create a new library in '+newpath[0]+ '   ??', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
            if cofirm_but=='Yes':
                getMnuItms=mc.menu('chgFld',q=1,ia=1)
                if len(getMnuItms) >= 7:
                    mc.deleteUI(getMnuItms[3],mi=1)
                getMnuItms=mc.menu('chgFld',q=1,ia=1)    
                getItmLab=[]
                for each in getMnuItms:
                    lab=mc.menuItem(each,q=1,l=1)
                    getItmLab.append(lab)  
                if newpath:
                    if newpath[0] not in getItmLab:
                        mc.menuItem(label=newpath[0],p='chgFld',c=partial(changepath,newpath))
                savepathini=newpath[0]
            else:
                return
        else:
            savepathini=newpath[0]      
    else:
        return 
    Refresh_UI(savepathini)
    temp_path(savepathini)
        
def changepath(newpath,*args):
    savepathini=newpath[0] 
    Refresh_UI(savepathini)
    temp_path(savepathini)
    
def temp_path(savepathini):
    getMnuItms=mc.menu('chgFld',q=1,ia=1)
    updtd_fldr=[]
    for each in getMnuItms:
            lab=mc.menuItem(each,q=1,l=1)
            if not lab in updtd_fldr:
               updtd_fldr.append(lab)
    updatd_fldr=updtd_fldr[3:]
    files=open(tmpfile,'w')
    files.write('Currnt dir:\n'+savepathini+'\n')
    files.write('Runnng dir:\n')
    for each in updatd_fldr:
        files.write(each.strip() +'\n')
    files.write('}')    
    files.close()
    AnimPoseLib()
    
def savedpath(line,*args):
    savepathini=line.strip() 
    Refresh_UI(savepathini)
    temp_path(savepathini)

def Renamepose(read1,*args):
    filename = os.path.basename(read1).split('.')[0]
    print filename
    dirname  = os.path.dirname(read1)
    seltab   = mc.shelfTabLayout('Poses',q=1,st=1)
    PoseRename = mc.promptDialog(
                    title='PoseRename',
                    message='PoseRename:',
                    text = filename,
                    button=['OK', 'Cancel'],
                    defaultButton='OK',
                    cancelButton='Cancel',
                    dismissString='Cancel') 
    if PoseRename=='OK':   
        newposename = mc.promptDialog (query=True, text=True)         
        renampose= dirname+'/'+ newposename+'.anim'       
        renameimg= dirname+'/'+ newposename+'.bmp'
        read2=read1.replace('.anim','.bmp')
        mc.sysFile(read1,rename= renampose)
        mc.sysFile(read2,rename= renameimg)
        Refresh_UI(savepathini)
        print'Pose name changed successfully'
    else:
        return
    mc.shelfTabLayout('Poses',e=1,st=seltab)
    
def Deletepose(read1,*args):
    confirm=mc.confirmDialog (title='Confirm Delete pose',message='    Are you sure......?',ma='right',button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No')
    if confirm=='Yes':
        seltab = mc.shelfTabLayout('Poses',q=1,st=1)
        filename = os.path.basename(read1).split('.')[0]
        read2= read1.replace('.anim','.bmp')
        mc.sysFile(read2,delete=1)
        mc.sysFile(read1,delete=1)
        filename = os.path.basename(read1).split('.')[0]
        Refresh_UI(savepathini)
        print filename + ' Pose deleted..'
        mc.shelfTabLayout('Poses',e=1,st=seltab)
