import maya.cmds as cmds
WIDTH = 64; HEIGHT = 48
xa = -2.0; xb = 1.0
ya = -1.5; yb = 1.5
maxIt = 256/10

for ky in range(HEIGHT):
    for kx in range(WIDTH):
        c = complex(xa + (xb - xa) * kx / WIDTH, ya + (yb - ya) * ky / HEIGHT)
        z = complex(0.0, 0.0)
        for i in range(maxIt):
            z = z * z + c
            if abs(z) >= 2.0:
                break
        '''        
        rd = hex(i % 4 * 64)[2:].zfill(2)
        gr = hex(i % 8 * 32)[2:].zfill(2)
        bl = hex(i % 16 * 16)[2:].zfill(2)
        img.put("#" + rd + gr + bl, (kx, ky))
		'''
        thename="Sid"
        sphereobj=cmds.polySphere(n=thename+'_Sphere#', r=i%4 * 64)
        cmds.move( kx, ky, 0, sphereobj )
        print kx, ky