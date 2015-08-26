#this is a code for generating a mandelbulb
#here, instead of colors, i've used sphere's instead.
#if a point does not escape the region, after being incremented by a 
#particular fn, then a sphere is placed at that point..

import random
import maya.cmds as cmds
from math import sqrt, atan2, cos, sin

s = 0.1 #size
n = 3 #power
thename='Sid'

def mandel(x0, y0, z0):
    
	x, y, z = 0.0, 0.0, 0.0
    
	for i in range(8):#32 iterations
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
print "Done."
