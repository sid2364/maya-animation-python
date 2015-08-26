#cmds.setAttr(mainSphereInstance, subdivisionX=radius*10)
import maya.cmds as cmds
import random, math
import maya.mel as mel

def getVtxPos( shapeNode ) :
	vtxWorldPosition=[]    # will contain positions un space of all object vertex
	vtxIndexList=cmds.getAttr( shapeNode+".vrts", multiIndices=True )
	for i in vtxIndexList :
		curPointPosition=cmds.xform(str(shapeNode)+".pnts["+str(i)+"]", query=True, translation=True, worldSpace=True )    # [1.1269192869360154, 4.5408735275268555, 1.3387055339628269]
		curPointPosition.append(i)
		vtxWorldPosition.append(curPointPosition)
	return vtxWorldPosition

def getArbitraryPos():
	pos=[]
	for i in range(20):
		for j in range(20):
			pos.append([i-10, j-10])
	return pos

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
	z=0
	vtxPos=getArbitraryPos()
	
	#instanceGroupName = cmds.group( empty=True, name=thename + '_instance_grp#' )
	for i in range(len(vtxPos)):
		x, y = vtxPos[i]
		iteration=0
		maxiteration=10
		x0 = ( (x - -20) / (9 - -20) ) * (1 - (-2.5)) + (-2.5)
		y0 = ( (y - -20) / (9 - -20) ) * (1 - (-2.5)) + (-2.5)
		print "Processing: ", x, y, " --> ", x0, y0
		
		while((x*x+y*y)<4 and iteration<maxiteration):
			xtemp = x*x - y*y + x0
			y = 2*x*y + y0
			x = xtemp
			iteration = iteration + 1
		
		sphereobj=cmds.polySphere(n=thename+'_Sphere#', r=iteration*0.25)
		cmds.move( x, y, 0, sphereobj )	