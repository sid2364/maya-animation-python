#save this as a shelf script.. it has UI!
import maya.cmds as cmds
import functools


def createUI( window_title, function_to_execute ):
	windowID = 'SIDWindow'
    
	if cmds.window( windowID, exists=True ):
		cmds.deleteUI( windowID )
    #UI creation!       
	cmds.window( windowID, minimizeButton=False , maximizeButton=False, title=window_title, sizeable=False, resizeToFitChildren=True )
    cmds.rowColumnLayout( numberOfColumns=2, columnWidth=[(1,90),(2,100)])
    cmds.text( label='No. of particles:' )
	n = cmds.intField( value=50 )
		
	cmds.text( label='Scale-X:' )
	x = cmds.intField( value=10 )
	cmds.text( label='Scale-Y:' )
	y = cmds.intField( value=10 )
	cmds.text( label='Scale-Z:' )
	z = cmds.intField( value=10 )
    
    
	"""
	cmds.separator( h=10, style='none' )
	cmds.separator( h=10, style='none' )
    
	cmds.separator( h=10, style='none' )
	"""
    
	cmds.text( label='Volume Shape:' )
	objectList = cmds.optionMenu("objects", width=100)
	cmds.menuItem(label = "Cube", parent="objects")
	cmds.menuItem(label = "Sphere", parent="objects")
	cmds.menuItem(label = "Cylinder", parent="objects")
	cmds.menuItem(label = "Cone", parent="objects")
	cmds.menuItem(label = "Torus", parent="objects")       
	
	cmds.separator( h=10, style='none')
	cmds.separator( h=10, style='none') 
	cmds.separator( h=10, style='none') 
	
	
	#cmds.button(label = "Print selected option", command = functools.partial(PrintObject, objectList))
	cmds.button( label='Create Field', command=functools.partial(function_to_execute, x, y, z, n, objectList) )
	
	def cancelCallback( *args ):
		if cmds.window( windowID, exists=True ):
			cmds.deleteUI( windowID )
	cmds.separator( h=10, style='none' )
	cmds.button( label='Close', command=cancelCallback )
	
	cmds.showWindow() #finally show the window
	"""    
	def PrintObject(objectList, *args):
	selectedMenuItem = cmds.optionMenu(objectList, query = True, value = True)
	print selectedMenuItem
	"""
	
def swarmfunc(x, y, z, n, objectList, *args): #simply for parsing arguments and passing to the swarm function!
	shape = cmds.optionMenu( objectList, query = True, value = True)
	n=cmds.intField( n, query=True, value=True )
	x=cmds.intField( x, query=True, value=True )
	y=cmds.intField( y, query=True, value=True )
	z=cmds.intField( z, query=True, value=True )
	
	#this will call the swarm function
	print ('Calling swarm function with the following params:-')
	print ('No. of particles: %s' % n)
	print ('Dimensions(x, y, z): (%s, %s, %s)' % (x, y, z))
	#print n
	s=1
	if shape=='Cube':
		s=1
	elif shape=='Sphere':
		s=2
	elif shape=='Cylinder':
		s=3
	elif shape=='Cone':
		s=4
	elif shape=='Torus':
		s=5
	print ('Shape: %s\nCorresponding value: %s \n' % (shape, s))
	cmds.swarm(np=n, dim=(x, y, z), sv=s)
	#print n, x, y, z, s
	    
createUI( 'Swarm', swarmfunc )