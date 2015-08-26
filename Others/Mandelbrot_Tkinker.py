import Tkinter
from Tkinter import *


print "\t\tTkinker 2D Mandelbrot Demo\n"
WIDTH = int(raw_input("Width (920 recommended): "))
HEIGHT = int(raw_input("Height (840 recommended): "))
xa = -2.0; xb = 1.0
ya = -1.5; yb = 1.5
maxIt = int(raw_input("Maximum iterations (32 recommended): "))
power = int(raw_input("Power (2-64): "))

window = Tk()
canvas = Canvas(window, width = WIDTH, height = HEIGHT, bg = "#000000")
img = PhotoImage(width = WIDTH, height = HEIGHT)
canvas.create_image((0, 0), image = img, state = "normal", anchor = Tkinter.NW)

print "\nWorking. Please wait..."
for ky in range(HEIGHT):
    for kx in range(WIDTH):
        c = complex(xa + (xb - xa) * kx / WIDTH, ya + (yb - ya) * ky / HEIGHT)
        z = complex(0.0, 0.0)
        if(ky%10==0):print "\r", str((ky*kx*100)/(WIDTH*HEIGHT)), "% complete!",
        for i in range(maxIt):
            z = z ** power + c
            if abs(z) >= 2.0:
                break
        rd = hex(i % 4 * 64)[2:].zfill(2)
        gr = hex(i % 8 * 32)[2:].zfill(2)
        bl = hex(i % 16 * 16)[2:].zfill(2)
        img.put("#" + rd + gr + bl, (kx, ky))

print "\r100% complete!\nDone."
canvas.pack()
mainloop()