import maya.cmds as cmds
import random
import math


def frange(x, y, jump):
	while x < y:
		yield x
		x += jump

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
	sphereList = cmds.ls( '*Sid_Mandelbulb*' ) #if already exists, delete
	if len(sphereList)!=0:
		cmds.delete(sphereList)
	iterations = int(cmds.promptDialog(query=True, text=True))
	#area=(0.8, 0.8, 0.8) #initial growth area
	radius=0.5
	mandelbulbInstanceGrp=cmds.group(empty=True,name=thename+'_InstanceGrp#')
	mainSphereInstance=cmds.polySphere(n=thename+'_SphereMain', r=radius)
	
	itertemp=iterations
	newx=newy=newz=0
	for x in frange(0.5, 10, 0.5 ):
		for y in frange(0.5, 10, 0.5):
			for z in frange( 0.5, 10, 0.5):
				while(iterations):
					r = (x*x + y*y + z*z )**0.5
					theta = math.atan2((x*x + y*y)**0.5 , z)
					phi = math.atan2(y,x)
		
					newx = r**iterations * math.sin(theta*iterations) * math.cos(phi*iterations)
					newy = r**iterations * math.sin(theta*iterations) * math.sin(phi*iterations)
					newz = r**iterations * math.cos(theta*iterations)
					print "Processing: ", x, y, z, "for ", newx, newy, newz
					if (newx**2 + newy**2 + newz**2) < 8:
						break
					iterations=iterations-1
				currInstance=cmds.instance(mainSphereInstance, name=thename+'_Instance#')
				cmds.parent(currInstance, mandelbulbInstanceGrp)
				cmds.move( x, y, z, currInstance )
				newx=newy=newz=0
				iterations=itertemp
				
	