import maya.cmds as mc
import maya.mel as mel
def GrpEdgstoVertx():
    sel=mc.ls(sl=True)
    if sel:
        if (mc.filterExpand(sel[0], sm = 32)):
            if not len(sel)==1:
                seled = flatten(sel)
                seled1 = seled[:]
                edgGrps = []
                comEdges = []
                for i in range(len(seled1)):
                    if len(seled) > 1:
                        if seled1[i] in comEdges:
                            continue
                        mc.select(seled1[i], r = 1)
                        mel.eval('polySelectEdges edgeLoopOrBorder')
                        loopEdges = flatten(mc.ls(sl=1))
                        comEdges = list(set(seled).intersection(set(loopEdges)))
                        #edgGrps.append(comEdges)
                        print comEdges
                        if comEdges not in edgGrps :
                            edgGrps.append(comEdges)
                            mc.select(cl=1)
                            for each in comEdges:
                                mc.select(each,add=True)
                            mel.eval('polyToCurve -form 2 -degree 3')
            else:
                mel.eval('polyToCurve -form 2 -degree 3')
            mc.select(cl=1) 
        else:
            mc.confirmDialog (title='Error' ,message= 'Please Select Edges', button=['OK'] ,defaultButton='Yes')
    else:
            mc.confirmDialog (title='Error' ,message= 'Nothing Selected..Please Select any Edges', button=['OK'] ,defaultButton='Yes')
def flatten(List):
    mc.select(List, replace = True)
    NewList = mc.ls(sl = True, fl = True)
    return NewList
#GrpEdgstoVertx()                
