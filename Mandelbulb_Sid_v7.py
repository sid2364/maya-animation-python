import maya.cmds as cmds
import random
from math import sqrt, atan2, cos, sin

VOXEL_SIZE = 0.2
n = 8
thename='Sid'

def mandel(x0, y0, z0):
    
    x, y, z = 0.0, 0.0, 0.0
    
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


def box(x0, y0, z0):
    
    sphereobj=cmds.polySphere(n=thename+'_Sphere#', r=0.25)
    cmds.move( x, y, z, sphereobj )
    print "Placed at ", x, y, z
    
count = 0
surrounded_count = 0

SIZE = int(1.1 / VOXEL_SIZE)


layer = {}

for xx in range(-SIZE, SIZE):
    
    layer[xx] = {}
    
    for yy in range(-SIZE, SIZE):
        for zz in range(-SIZE, SIZE):
            x = xx * VOXEL_SIZE
            y = yy * VOXEL_SIZE
            z = zz * VOXEL_SIZE
            
            if mandel(x, y, z):
                count += 1
                layer[xx][yy,zz] = True
    
    tx = xx - 1
    if tx not in layer or tx - 1 not in layer:
        continue
    for yy in range(-SIZE, SIZE):
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
                x = tx * VOXEL_SIZE
                y = yy * VOXEL_SIZE
                z = zz * VOXEL_SIZE
                
                box(x, y, z)
    
    del layer[tx - 1]

