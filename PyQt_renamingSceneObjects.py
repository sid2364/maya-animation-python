"""
This code should be run in Maya!
It works as a utility for renaming mesh objects.
"""

from PyQt4 import QtCore #contains Qt's base classes
from PyQt4 import QtGui #contains functionalities for dialogs, windows, buttons, etc. Anything that is displayed on the screen.

import maya.cmds as mc

import maya.OpenMayaUI as omu #this import is for PySide apparently
import sip #used for wrapInstance

def maya_main_window():
    ptr = omu.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)
    
class RenamingDialog(QtGui.QDialog):
#self is used by a method to refer to its own class obj    
    def __init__(self, parent=maya_main_window()): #the parent attribute is required because without it,
						#if the user clicked into Maya, this window would go to the 
						#background, which is not what we want.
        #this is the constructor of the class
	QtGui.QDialog.__init__(self, parent)
        
        self.setWindowTitle("Renaming Dialog by Sid")
        self.setFixedSize(250, 200)
        
        self.create_layout()
        self.create_connections()
        
        self.refresh() #populate dialog automatically when its created
        
    def create_layout(self):
        #create the selected item list
        self.selection_list = QtGui.QListWidget()
        
        #create two buttons - refresh and cancel buttons
        self.refresh_button = QtGui.QPushButton("Refresh")
        self.cancel_button = QtGui.QPushButton("Cancel")        

        #create the button layout
        button_layout = QtGui.QHBoxLayout()
        button_layout.setSpacing(2)
        button_layout.addStretch()
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.cancel_button)        
        
        #create the main layout
        main_layout = QtGui.QVBoxLayout()
        main_layout.setSpacing(2)
        main_layout.setMargin(2)

        main_layout.addWidget(self.selection_list)
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
        
    def create_connections(self):
        
        #connect the selected item list widget
        self.connect(self.selection_list, QtCore.SIGNAL("currentItemChanged(QListWidgetItem*, QListWidgetItem*)"), self.set_current_item)
        self.connect(self.selection_list, QtCore.SIGNAL("itemChanged(QListWidgetItem*)"), self.update_name)
	
	#QtCore.SIGNAL specifies what fires the method, it can be something like (for a button) "clicked()"
        #connect the buttons, like "add" in Applets
        self.connect(self.refresh_button, QtCore.SIGNAL("clicked()"), self.refresh)
        self.connect(self.cancel_button, QtCore.SIGNAL("clicked()"), self.close_dialog)
        
    def update_selection(self):
        #remove all items from the list before repopulating
        self.selection_list.clear()
        
        #add the currently selected objects to the list
        selected = mc.ls(selection=True)
        for sel in selected:
            item = QtGui.QListWidgetItem(sel)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
            self.selection_list.addItem(item)
        
        
    def refresh(self):
        self.update_selection()   
             
    def close_dialog(self):
        self.close()
        
    def set_current_item(self, item):
        if (item):
            self.current_item_name = str(item.text())
        else:
            self.current_item_name = ""
            
    def update_name(self, item):
        new_name = str(item.text())
        
        #if the name hasn't change, then ignore it
        if new_name == self.current_item_name:
            return
            
        #restore the previous name if a new name isn't given
        if not new_name:
            item.setText(self.current_item_name)
            return
        
        #Update the name in Maya
        #maya may alter the name so update the list
        self.current_item_name = str(mc.rename(self.current_item_name, new_name))
        item.setText(self.current_item_name)
            

#'main' method        

dialog = RenamingDialog() #class object
dialog.show() #this is not a class method, but a Qt command/function for QtGui dialogs