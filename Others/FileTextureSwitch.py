import maya.cmds as mc
import os 
from functools import partial
def FileTextureSwitch():
    #global TextFormat
    if mc.window('FileTextureSwitch', exists = True):
        mc.deleteUI('FileTextureSwitch')
    mc.window('FileTextureSwitch', title = 'FileTextureSwitch', wh = (450,280))
    mc.columnLayout()
    #mc.frameLayout(l='',w=268)
    Format=['jpg','iff','tga','png','tif']
    mc.columnLayout(co = ('left', 10))
    mc.separator(h = 5, st = 'none')
    mc.frameLayout(l='Texture File Format Switch',w=270)    
    mc.separator(h = 5, st = 'none')
    mc.rowColumnLayout(nc=3,cw=[(1,100),(3,100)])
    mc.text(l='Selected objects to: ')
    mc.optionMenu('texfrmt')
    for each in Format:
        mc.menuItem(l=each)
    mc.button(l='Convert',c=partial(convert))
    mc.setParent('..')
    mc.separator(h = 2, st = 'none')
    mc.setParent('..')
    mc.showWindow('FileTextureSwitch')
    mc.window('FileTextureSwitch', e = True, wh = (292, 100))
def convert(*args):
    sel_obj  = mc.ls(sl=1,l=1)
    if sel_obj:
        frmt=mc.optionMenu('texfrmt',q=1,v=1)
        for each in sel_obj:
            texNodes = mc.listRelatives(each,c=1,s=1,ni=1,f=1)
            #print texNodes
            ShaderNam= mc.listConnections(texNodes[0])
            #print ShaderNam
            Files=mc.listHistory(ShaderNam[0])
            TexFiles=[]
            for file in Files:
                if mc.nodeType(file) == 'file':
                    TexFiles.append(file)
            for j in range(len(TexFiles)):
                file_tex = mc.getAttr(TexFiles[j] + '.fileTextureName')
                filename = os.path.basename(file_tex)
                pathname = os.path.dirname(file_tex)
                print filename
                Filefrt=filename.split('.')
                Fulpath=pathname+'\\'+Filefrt[0]+'.'+frmt
                mc.setAttr((TexFiles[j] + '.fileTextureName'),(Fulpath),type='string')
        mc.confirmDialog(t='Message', m= 'Selected are successfully converted to '+frmt+' format', b='OK', ma = "center")
    else:
        mc.confirmDialog(t='Message', m = 'Please select any objects....', b='OK', ma = "center")
        
FileTextureSwitch()       
