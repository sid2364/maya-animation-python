#this code randomises a selected instance
#select one object to scatter it around randomly
import maya.cmds as cmds
import random

#random.seed(90) - if you want the same random pattern
cubeList = cmds.ls( '*SID*' )
if len(cubeList)!=0:
	cmds.delete(cubeList)
	
sel=cmds.ls(orderedSelection=1)
item=sel[0]

obj_group = cmds.group( empty=True, name='RandomInstanceGrp#')

for i in range(0,50): #50 instances of obj
    curr = cmds.instance(item, name='instance#')
    cmds.parent(curr, obj_group)
    x=random.uniform(-10,10)
    y=random.uniform(0,20)
    z=random.uniform(-10,10)
    cmds.move(x, y, z, curr)
    
    xRot = random.uniform(0,360)
    yRot = random.uniform(0,360)#add random spin..
    zRot = random.uniform(0,360)
    
    cmds.rotate(xRot, yRot, zRot, curr) #move to location!
