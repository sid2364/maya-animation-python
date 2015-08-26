#to rotate around first object!!
import maya.cmds as cmds

def rotation( obj, start, end, target ):
    cmds.cutKey( obj, time=(start, end), attribute=target )
    cmds.setKeyframe( obj, time=start, attribute=target, value=0 )
    cmds.setKeyframe( obj, time=end, attribute=target, value=360 )
    cmds.selectKey( obj, time=(start, end), attribute=target, keyframe=True )
    cmds.keyTangent( inTangentType='linear', outTangentType='linear' )
    
sel_list = cmds.ls( selection=True, type='transform' )
if len( sel_list ) >= 1:
    # print 'selected items: %s' % sel_list 
    start = cmds.playbackOptions( query=True, minTime=True )
    end = cmds.playbackOptions( query=True, maxTime=True )
    
    for obj in sel_list:
        # print '%s %s' % (obj, objectTypeResult)
        rotation( obj, start, end, 'rotateY' )

    
else:
    print 'Please select at least one object'