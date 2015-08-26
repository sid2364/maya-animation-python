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
	radius=10
	
	mainSphereInstance=cmds.polySphere(n=thename+'_SphereMain', r=radius, sx=radius*20, sy=radius*20)
	mel.eval('select -r '+thename+'_SphereMain.vtx[0:'+str(cmds.polyEvaluate(thename+'*', v=True))+']')
	selList=cmds.ls(sl=True, fl=True)
	#print selList
	if iterations:
		#for i in range(len(selList)/3):
		#	vtxSel=selList[random.randint(0, len(selList))]
		#	cmds.select(vtxSel, d=True)
		#selected = cmds.ls(selection=True)
		
		vtxPos=[]
		vtxPos=getVtxPos(thename+'_SphereMain')
		for _ in range(len(vtxPos)/5):
			x, y, z, ele = vtxPos[random.randint(0, len(vtxPos))]
			print "Processing coordinate: (%s, %s, %s) and vertex: Sid_Mandelbulb_SphereMain.vtx[%s]" % (str(x), str(y), str(z), str(ele))
			
			r=x*x + y*y + z*z
			r=r**0.5
			sqrtXY=(x*x+y*y)**0.5
			theta = math.atan2(sqrtXY , z)
			phi = math.atan2(y,x)
			
			newx = r**2 * math.sin(theta*n) * math.cos(phi*n)
			newy = r**2 * math.sin(theta*n) * math.sin(phi*n)
			newz = r**2 * math.cos(theta*n)
			
			cmds.move( newx, newy, newz, thename+'_SphereMain.vtx['+str(ele)+']' )
			
		# do something with the value. egs:
		iterations=iterations-1
		