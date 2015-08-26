#for activating this plug-in, put this python file in C:\Program Files\Autodesk\Maya2013\bin\plug-ins
#or whereever your bin/plug-ins folder is
#then from Maya, go to Window .. Preferences .. Plug-in Manager, and load this file
#you will not be able to call maya.cmds.swarm()

import sys
import random
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMayaFX as OpenMayaFX

#the name of the command to be executed! Use "maya.cmds.swarm(np=##, dim=(#, #, #), sv=#)"
#SYNTAX!!
cmd = 'swarm'
#class def
class swarm_cmd( OpenMayaMPx.MPxCommand ):
    
    instanceid=0
    '''
    default_numparticles=50
    default_dimensions=(5,5,5)
    #NOT REQUIRED
    '''
        
    def __init__(self):
        #constructor
        OpenMayaMPx.MPxCommand.__init__(self)
        #give a unique name to this command instance.
        self.instancename=cmd + str( swarm_cmd.instanceid ) #if more tha one exist!!
        swarm_cmd.instanceid+= 1
        #particle system instance variables
        self.particle_system_name= self.instancename + '_Particles'
        self.numParticles=50
        self.particlePositions= OpenMaya.MPointArray()
        
        #turbulence field instance variables
        self.tur_field_name=self.instancename + '_Turbulence'
        self.size_x=5
        self.size_y=5
        self.size_z=5
        
        self.dagModifier=OpenMaya.MDagModifier()
	self.volShapeNum=1 #TEST!
    
    
    def isUndoable(self):
        #determines whether or not this command is undoable within Maya
        return True
    
    
    def parseArgs(self, args):
        #parse the command's arguments
        #create an argument parser object.
        argData = OpenMaya.MArgParser( self.syntax(), args )
        
        #check if each flag is set, and store its value.
        if argData.isFlagSet('np'):
            self.numParticles=argData.flagArgumentInt('np',0)
        
        if argData.isFlagSet('dim'):
            self.size_x=argData.flagArgumentDouble('dim',0)
            self.size_y=argData.flagArgumentDouble('dim',1)
            self.size_z=argData.flagArgumentDouble('dim',2)
	if argData.isFlagSet('sv'):
	    self.volShapeNum=argData.flagArgumentInt('sv',0 )
	#print self.volShapeNum
        
    def doIt(self, args):
        #command's first-time execution
        #parse the flags and the arguments!!
        try:
            self.parseArgs(args)
        except Exception:
            #an exception should be thrown here if the argument/flag syntax is wrong.
            print('Invalid flag syntax for parse command!' )
            return #END EXECUTION!! dont carry on..
        
        #clear the current selection list to avoid any wrong grouping.
        OpenMaya.MGlobal.clearSelectionList()
        
        #create the "turbulence field". got help online for these!
        self.dagModifier.commandToExecute( 'turbulence -name "' + self.tur_field_name + '"' )
        self.dagModifier.commandToExecute( 'scale ' + str( 0.5*self.size_x )+' '+str(0.5 * self.size_y )+' '+str( 0.5* self.size_z ) +' '+self.tur_field_name )
        self.dagModifier.commandToExecute( 'setAttr "' + self.tur_field_name + '.volumeShape" '+str(self.volShapeNum) ) # 1 for cube, 2 for sphere ... check maya doc for more (goes uptil 5)
        self.dagModifier.commandToExecute( 'setAttr "' +self.tur_field_name +'.magnitude" 100' )
        self.dagModifier.commandToExecute( 'setAttr "' + self.tur_field_name + '.attenuation" 0.1' )
        self.dagModifier.commandToExecute( 'setAttr "' + self.tur_field_name + '.frequency" 4' )
        self.dagModifier.commandToExecute( 'setAttr "'+ self.tur_field_name +'.interpolationType" 1' )
        self.dagModifier.commandToExecute( 'setAttr "'+self.tur_field_name +'.noiseLevel" 8' )
        self.dagModifier.commandToExecute( 'setAttr "'+self.tur_field_name +'.noiseRatio" 1' )
        self.dagModifier.commandToExecute( 'setAttr "'+self.tur_field_name +'.trapInside" 1' )
        self.dagModifier.commandToExecute( 'setAttr "'+self.tur_field_name + '.trapRadius" 1' )
        
        # create the particle system of "bees" or particles
        self.dagModifier.commandToExecute( 'particle -name "' + self.particle_system_name + '"' )
        self.dagModifier.commandToExecute( 'setAttr "' + self.particle_system_name + 'Shape.conserve" 1.00' )
        self.dagModifier.commandToExecute( 'setAttr "' + self.particle_system_name + 'Shape.particleRenderType" 6' ) # 3 for points, 6 for streaks
        
        #connect the particle system to the turbulence field.
        #COPIED!!
        self.dagModifier.commandToExecute( 'connectDynamic -f '+self.tur_field_name+' '+self.particle_system_name+'Shape' )
        self.dagModifier.doIt()
        particleShapeDagPath = self.getDagPathToObject( self.particle_system_name + 'Shape' )
        particleSystemFn = OpenMayaFX.MFnParticleSystem( particleShapeDagPath )
        
        #randomly generate the positions of the particles within the volume.
        for i in range( 0, self.numParticles ):
            self.particlePositions.append(random.uniform(0.5*-self.size_x, 0.5*self.size_x), random.uniform(0.5*-self.size_y, 0.5* self.size_y), random.uniform(0.5*-self.size_z, 0.5*self.size_z))
        
        #emit means to display the particles at those positions
        particleSystemFn.emit( self.particlePositions )
        particleSystemFn.saveInitialState()
        
    
    def redoIt(self):
        #re-do the work performed by the commmand.. when user presses redo!
        self.dagModifier.doIt()
        
        
    def undoIt(self):
        #undo the work performed, put it on the undo stack..
        self.dagModifier.undoIt()
    def getDagPathToObject(self, objectName ):
        #COPIED!!
        selectionList = OpenMaya.MSelectionList()
        OpenMaya.MGlobal.getSelectionListByName( objectName, selectionList )
        dagPath = OpenMaya.MDagPath()
        selectionList.getDagPath( 0, dagPath )
        return dagPath
    
    

# plug-in init
def cmdcreator():
    #return an instance of the command 
    return OpenMayaMPx.asMPxPtr( swarm_cmd() )


def syntaxcreator():
    #define the syntax of the command
    
    #create an instance of MSyntax which will contain our command's syntax definition.
    syntax = OpenMaya.MSyntax()
    
    #add the flags to the MSyntax object
    syntax.addFlag( 'np',  'numParticles', OpenMaya.MSyntax.kDouble ) #one num
    syntax.addFlag( 'dim', 'dimensions', OpenMaya.MSyntax.kDouble, OpenMaya.MSyntax.kDouble, OpenMaya.MSyntax.kDouble )#x, y, z
    syntax.addFlag( 'sv', 'shapeVolume', OpenMaya.MSyntax.kDouble) #one num!
    return syntax

#COPIED!!
def initializePlugin( obj ):
    #initialize the plug-in when Maya loads it
    plugin = OpenMayaMPx.MFnPlugin( obj )
    try:
        plugin.registerCommand( cmd, cmdcreator, syntaxcreator )
    except:
        sys.stderr.write( 'Failed to register command: ' + cmd )


def uninitializePlugin( obj ):
    #uninitialize the plug-in when Maya un-loads it
    plugin = OpenMayaMPx.MFnPlugin( obj )
    try:
        plugin.deregisterCommand( cmd )
    except:
        sys.stderr.write( 'Failed to unregister command: ' + cmd )
        
        

#copy the following lines and run them in Maya's script editor
#import maya.cmds as cmds
#cmds.swarm( np=50, dim=( 10, 9, 10 ) )

#will now work on developing a UI for this
#refer to swarmCommand_shelfScript_SID.py for the code..
