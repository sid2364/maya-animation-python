import maya.cmds as cmds
import random
from math import sqrt, atan2, cos, sin
import maya.mel as mel

def mandel(x0, y0, z0):
	x, y, z = 0.0, 0.0, 0.0
	n=8
	for i in range(32):
		r = sqrt(x*x + y*y + z*z)
		theta = atan2(sqrt(x*x + y*y), z)
		phi = atan2(y, x)
		
		x = r**n * sin(theta*n) * cos(phi*n) + x0
		y = r**n * sin(theta*n) * sin(phi*n) + y0
		z = r**n * cos(theta*n)              + z0
		if x**2 + y**2 + z**2 > 2:
			return False
		else:
			return True
def draw(x, y, z):
	sphereobj=cmds.polySphere(n=thename+'_Sphere#', r=0.05)
	cmds.move( x, y, z, sphereobj )
	print "Placed."
random.seed(1234) #remove and check later

result = cmds.promptDialog(
		title='Mandelbulb Gen.',
		message='Enter no. of iterations.',
		button=['OK', 'Cancel'],
		defaultButton='OK',
		cancelButton='Cancel',
		dismissString='Cancel')

if result == 'OK':
	thename='Sid_Mandelbulb'
	sphereList = cmds.ls( '*Sid*' ) #if already exists, delete
	if len(sphereList)!=0:
		cmds.delete(sphereList)
	iterations = int(cmds.promptDialog(query=True, text=True))
	radius=0.25
	vtxPos=[]
	vtxPos=getArbitraryPos()
	maxiteration=10
	#instanceGroupName = cmds.group( empty=True, name=thename + '_instance_grp#' )
SIZE=3
layer = {}

for xx in range(-SIZE, SIZE):
	layer[xx] = {}
	for yy in range(-SIZE, SIZE):
		for zz in range(-SIZE, SIZE):
			x = xx * 0.5
			y = yy * 0.5
			z = zz * 0.5
			print "Processing: ", x, y, z
			if mandel(x, y, z):
				layer[xx][yy,zz] = True
	tx = xx - 1
	for zz in range(-SIZE, SIZE):
            if not layer[tx].get((yy, zz)):
                continue
            if layer[tx - 1].get((yy, zz)) and \
               layer[tx].get((yy - 1, zz)) and \
               layer[tx].get((yy + 1, zz)) and \
               layer[tx].get((yy, zz - 1)) and \
               layer[tx].get((yy, zz + 1)) and \
               layer[tx + 1].get((yy, zz)):
                surrounded_count += 1
            else:
                x = tx
                y = yy
                z = zz
                
                box(x, y, z)
    
    del layer[tx - 1]