#PySide example that creates a simple GUI for generating polygons in Maya 2014

from PySide import QtCore
from PySide import QtGui

from shiboken import wrapInstance

import maya.cmds as cmds
import maya.OpenMayaUI as omui

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtGui.QWidget)
    
class PrimitiveUi(QtGui.QDialog):
    
    def __init__(self, parent=maya_main_window()):
        super(PrimitiveUi, self).__init__(parent)
        
        self.setWindowTitle("Primitives_SID")
        self.setWindowFlags(QtCore.Qt.Tool)
        
        #delete UI on close to avoid winEvent error
	#in PySide if we open too many instances of a widget, then Maya crashes (no solution for this bug so far)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        
        self.create_layout()
        self.create_connections() #to create connections between the buttons and the functions called
        
    def create_layout(self):
        self.cube_btn = QtGui.QPushButton("Cube")
        self.sphere_btn = QtGui.QPushButton("Sphere")
        self.cone_btn = QtGui.QPushButton("Cone")
        self.cylinder_btn = QtGui.QPushButton("Cylinder")
        
        main_layout = QtGui.QVBoxLayout()
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(2)
        main_layout.addWidget(self.cube_btn)
        main_layout.addWidget(self.sphere_btn)
        main_layout.addWidget(self.cone_btn)
        main_layout.addWidget(self.cylinder_btn)
        main_layout.addStretch() #so the buttons float up, on one side
        
        self.setLayout(main_layout)
        
    def create_connections(self):
	#adding responses to button clicks
        self.cube_btn.clicked.connect(PrimitiveUi.make_cube)
        self.sphere_btn.clicked.connect(PrimitiveUi.make_sphere)
        self.cone_btn.clicked.connect(PrimitiveUi.make_cone)
        self.cylinder_btn.clicked.connect(PrimitiveUi.make_cylinder)

    def make_cube(cls):
        cmds.polyCube()
   
    def make_sphere(cls):
        cmds.polySphere()

    def make_cone(cls):
        cmds.polyCone()

    def make_cylinder(cls):
        cmds.polyCylinder()
        
        
   
    # development workaround for winEvent error when running
    # the script multiple times
try:
    ui.close()
except:
    pass

ui = PrimitiveUi()
ui.show()
    
    