#to aim at first object
import maya.cmds as cmds

sel = cmds.ls( orderedSelection=True )
if len( sel ) >= 2:
    print 'Selected items: %s' % ( sel )
    target = sel[0]
    sel.remove( target ) #so that object does not aim at itself!!
    
    for obj in sel:
        print 'Constraining %s towards %s' % (obj, target )
        cmds.aimConstraint( target, obj, aim=[0,1,0] ) #trail and error
    
else:
    print 'Select two or more objects..'
    
    
    
    
    
    