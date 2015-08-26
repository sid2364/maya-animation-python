import maya.cmds as mc
sel=mc.ls(sl=1)
co=mc.polyEvaluate(sel[0],v=1)
mc.select(cl=1)
for each in sel:
    if mc.polyEvaluate(each,v=1)==co:
        mc.select(each,add=1)
