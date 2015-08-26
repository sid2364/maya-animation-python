#mandelbulb with UI

import random
import maya.cmds as cmds
from math import sqrt, atan2, cos, sin
import functools

def createUI( window_title, function_to_execute ):
	windowID = 'SIDWindow'
    
	if cmds.window( windowID, exists=True ):
		cmds.deleteUI( windowID )
	#UI creation!
	def printItemsSelected(*pargs):
		power = cmds.optionMenu( powerList, query = True, value = True)
		iter = cmds.optionMenu( iterList, query = True, value = True)
		size = cmds.optionMenu( sizeList, query = True, value = True)
		print "\nSelected params:-\nPower - ", power, "\nIterations - ", iter, "\nSize - ", size
		
	cmds.window( windowID, minimizeButton=False , maximizeButton=False, title=window_title, sizeable=False, resizeToFitChildren=True )
	cmds.rowColumnLayout( numberOfColumns=4, columnWidth=[(1,5),(2,110),(3,120), (4,5)])
	cmds.separator( h=5, style='none' )#for beautification
	cmds.separator( h=5, style='none' )#will add spacing/padding around the UI entities
	cmds.separator( h=5, style='none' )
	cmds.separator( h=5, style='none' )
	cmds.separator( h=5, style='none' )
	cmds.text( label='Power:' )
	powerList = cmds.optionMenu("power", width=100, changeCommand=printItemsSelected)
	cmds.menuItem(label = "3", parent="power")
	cmds.menuItem(label = "4", parent="power")
	cmds.menuItem(label = "5", parent="power")
	cmds.menuItem(label = "6", parent="power")
	cmds.menuItem(label = "7", parent="power")
	cmds.menuItem(label = "8", parent="power")  
	cmds.menuItem(label = "9", parent="power")
	cmds.menuItem(label = "10", parent="power")
	cmds.menuItem(label = "16", parent="power")
	cmds.menuItem(label = "32", parent="power")
	cmds.menuItem(label = "40", parent="power")
	cmds.separator( h=5, style='none' )
	
	cmds.separator( h=5, style='none' )
	cmds.text( label='Sphere size:' )
	sizeList = cmds.optionMenu("size", width=100, changeCommand=printItemsSelected)
	cmds.menuItem(label = "0.1", parent="size")
	#cmds.menuItem(label = "0.01", parent="size") TAKES TOO LONG!
	#cmds.menuItem(label = "0.02", parent="size")
	cmds.menuItem(label = "0.05", parent="size")
	cmds.menuItem(label = "0.09", parent="size")
	cmds.menuItem(label = "0.2", parent="size")
	cmds.menuItem(label = "0.5", parent="size")
	cmds.separator( h=5, style='none' )
	
	#cmds.separator( h=10, style='none' )
	#cmds.separator( h=10, style='none' )
    #cmds.separator( h=10, style='none' )
	
	cmds.separator( h=5, style='none' )
	cmds.text( label='Iterations:' )
	iterList = cmds.optionMenu("iter", width=100, changeCommand=printItemsSelected)
	cmds.menuItem(label = "8", parent="iter")
	cmds.menuItem(label = "1", parent="iter")
	cmds.menuItem(label = "2", parent="iter")
	cmds.menuItem(label = "4", parent="iter")
	cmds.menuItem(label = "10", parent="iter")
	cmds.menuItem(label = "16", parent="iter")
	cmds.menuItem(label = "32", parent="iter")
	cmds.menuItem(label = "40", parent="iter")
	cmds.menuItem(label = "50", parent="iter")
	cmds.menuItem(label = "64", parent="iter")       
	cmds.separator( h=5, style='none' )
	cmds.separator( h=10, style='none')
	cmds.separator( h=10, style='none') 
	cmds.separator( h=10, style='none')
	cmds.separator( h=10, style='none') 
	
	
	power = cmds.optionMenu( powerList, query = True, value = True)
	iter = cmds.optionMenu( iterList, query = True, value = True)
	size = cmds.optionMenu( sizeList, query = True, value = True)
	print "Selected params:-\nPower - ", power, "\nIterations - ", iter, "\nSize - ", size
	
	def getdata(*pargs): #get data from options
		power = cmds.optionMenu( powerList, query = True, value = True)
		iter = cmds.optionMenu( iterList, query = True, value = True)
		size = cmds.optionMenu( sizeList, query = True, value = True)
		print "\nSelected params:-\nPower - ", power, "\nIterations - ", iter, "\nSize - ", size
		#return functools.partial(function_to_execute, int(power), float(size), int(iter))
		mandelbulb(int(power), float(size), int(iter))
	cmds.separator( h=5, style='none' )
	cmds.separator( h=5, style='none' )
	cmds.button( label='Create Mandelbulb', command=getdata)
	
	def cancelCallback( *args ):
		if cmds.window( windowID, exists=True ):
			cmds.deleteUI( windowID )
	cmds.separator( h=10, style='none' )
	cmds.separator( h=5, style='none' )
	cmds.separator( h=5, style='none' )
	cmds.button( label='Close', command=cancelCallback )
	cmds.separator( h=5, style='none' )
	
	cmds.separator( h=10, style='none' )
	cmds.separator( h=10, style='none' )
	cmds.separator( h=10, style='none' )
	cmds.separator( h=10, style='none' )
	
	cmds.showWindow() #finally show the window
	    
##


#the last argument here is can take 0-n number of arguments, any extra args basically
def mandelbulb(power, thesize, iterations, *pargs):
	#this is a code for generating a mandelbulb
	#here, instead of colors, i've used sphere's instead.
	#if a point does not escape the region, after being incremented by a 
	#particular fn, then a sphere is placed at that point..
	
	
	s = thesize #size 0.1
	n = power #power 3
	thename='Sid'
	
	def mandel(x0, y0, z0):
	    
		x, y, z = 0.0, 0.0, 0.0
	    
		for i in range(iterations):#32 iterations
			#more iterations will mean less spheres and a less dense object
			r = sqrt(x*x + y*y + z*z)
			theta = atan2(sqrt(x*x + y*y), z)
			phi = atan2(y, x)
	        
			x = r**n * sin(theta*n) * cos(phi*n) + x0
			y = r**n * sin(theta*n) * sin(phi*n) + y0
			z = r**n * cos(theta*n) + z0
			#incremental formula
			if x**2 + y**2 + z**2 > 2:
				return False
		else:
			return True
	
	
	def draw(x0, y0, z0):
		#draw a sphere in the spec coords	
		sphereobj=cmds.polySphere(n=thename+'_Sphere#', r=s*0.35)
		cmds.move( x0, y0, z0, sphereobj )
		print "Processing: (%s, %s, %s)" % (str(x0), str(y0), str(z0))
	
	sphereList=cmds.ls("*Sid*")
	if(len(sphereList)!=0):
		cmds.delete(sphereList)
		print "Previous spheres deleted."
	    
	size = int(1 / s)
	
	layer = {}
	#to keep track of previous placements
	
	for xx in range(-size, size):
		layer[xx] = {}
		for yy in range(-size, size):
			for zz in range(-size, size):
				x = xx * s
				y = yy * s
				z = zz * s
				
				if mandel(x, y, z):
					layer[xx][yy,zz] = True
	
		prevx = xx - 1
		if prevx not in layer or prevx - 1 not in layer:
			continue
		for yy in range(-size, size):
			for zz in range(-size, size):
				if not layer[prevx].get((yy, zz)):
					continue
				if not (layer[prevx - 1].get((yy, zz)) and \
					layer[prevx].get((yy - 1, zz)) and \
					layer[prevx].get((yy + 1, zz)) and \
					layer[prevx].get((yy, zz - 1)) and \
					layer[prevx].get((yy, zz + 1)) and \
					layer[prevx + 1].get((yy, zz))):
					#if point not surrounded, then place sphere
					x = prevx * s
					y = yy * s
					z = zz * s
	                #place sphere
					draw(x, y, z)
	    
		del layer[prevx - 1]
		#not required, but good to free memory
	print "\n\nMandelbulb created with the following parameters:-"
	print "Size: ", s
	print "Power: ", n
	print "Iterations: ", iterations
	

createUI('MandelbulbWindow_Sid', mandelbulb)