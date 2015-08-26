# expandFromFirst.py
import maya.cmds as cmds

selectionList = cmds.ls( orderedSelection=True, type='transform' ) #only capture objects in the selection that are transformable
if len( selectionList ) >= 2:
    targetName = selectionList[0]
    selectionList.remove( targetName ) #so object does not expand away from itself
    
    locatorGroupName = cmds.group( empty=True, name='expansion_locator_grp#' ) #for all the point constraints
    maxExpansion = 100 #for the new attribute, the max value will be 100
    
    newAttributeName = 'expansion' #name of new attribute
    if not cmds.objExists( '%s.%s' % ( targetName, newAttributeName ) ):
        cmds.select( targetName )
        cmds.addAttr( longName=newAttributeName, shortName='exp', #this will add the attribute
                      attributeType='double', min=0, max=maxExpansion,
                      defaultValue=maxExpansion, keyable=True ) #keyable means it will appear in the attribute list 
    
    for objectName in selectionList: #this will add a point constraint to each object in the selection and also add the expansion attribute
        coords = cmds.getAttr( '%s.translate' % ( objectName ) )[0]
        locatorName = cmds.spaceLocator( position=coords, name='%s_loc#' % ( objectName ) )[0]
        cmds.xform( locatorName, centerPivots=True ) #turn centre pivot on
        
        cmds.parent( locatorName, locatorGroupName ) #add it to the locator group
        pointConstraintName = cmds.pointConstraint( [ targetName, locatorName ], objectName, name='%s_pointConstraint#' % ( objectName ) )[0]
        #for adding the point constraints to each object

        cmds.expression( alwaysEvaluate=True,
                         name='%s_attractWeight' % ( objectName ),
                         object=pointConstraintName,
                         string='%sW0=%s-%s.%s' % ( targetName, maxExpansion, targetName, newAttributeName ) )
        #this will add an expression in the object descriptor that tells it to behave according to its 'expansion' value
        
        cmds.connectAttr( '%s.%s' % ( targetName, newAttributeName ), 
                          '%s.%sW1' % ( pointConstraintName, locatorName ) )
        #bind the point constraint and expansion value
        
    cmds.xform( locatorGroupName, centerPivots=True )
    
else:
    print 'Please select two or more objects.'