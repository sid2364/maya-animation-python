import maya.cmds as cmds

def Mandelbrot():
	MAX_ITER = 57
	ZOOM = 15
	for y in range(80):
		for x in range(60):
			zx = zy = 0
			cX = (x - 40) / ZOOM
			cY = (y - 30) / ZOOM
			iter = MAX_ITER
			while (zx * zx + zy * zy < .4 && iter > 0) :
				tmp = zx * zx - zy * zy + cX
				zy = 2.0 * zx * zy + cY
				zx = tmp
				iter=iter-1
            
			sphereobj=cmds.polySphere(n=thename+'_Sphere#', r=iteration*0.25)
			cmds.move( x, y, 0, sphereobj )
Mandelbrot()