# Assignment 3
# Daniel Sanchez

import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS
import SampleFramework as sf

from ent import Entity

class ControlFrameListener(ogre.FrameListener):
    """To call the ent's tick and copy ent's new position to corresponding 
    scene node"""

    def __init__(self, entityMgr):
        ogre.FrameListener.__init__(self)
        self.entityMgr = entityMgr
        
    def frameStarted(self, frameEvent):
        for entity in self.entityMgr.entities:
            entity.tick(frameEvent.timeSinceLastFrame)

        return True
 
class TutorialFrameListener(sf.FrameListener):
    """A FrameListener class that handles basic user input."""
 
    def __init__(self, renderWindow, camera, sceneManager, entityMgr):
        # Subclass any Python-Ogre class and you must call its constructor.
        sf.FrameListener.__init__(self, renderWindow, camera)

        # Key and mouse state tracking.
        self.toggle = 0
        self.mouseDown = False
 
        # Populate the camera and scene manager containers.
        self.camNode = camera.parentSceneNode.parentSceneNode
        self.sceneManager = sceneManager

#--------------------------------------------
        self.entityMgr = entityMgr
        self.index = 0
#--------------------------------------------
 
        # Set the rotation and movement speed.
        self.rotate = 0.13
        self.move = 800
 
    def frameStarted(self, frameEvent):
        # If the render window has been closed, end the program.
        if(self.renderWindow.isClosed()):
            return False
 
        # Capture and update each input device.
        self.Keyboard.capture()
        self.Mouse.capture()
 
        # Get the current mouse state.
        currMouse = self.Mouse.getMouseState()
 
        # Use the Left mouse button to turn Light1 on and off.         
        if currMouse.buttonDown(OIS.MB_Left) and not self.mouseDown:
            light = self.sceneManager.getLight('Light1')
            light.visible = not light.visible
 
        # Update the mouseDown boolean.            
        self.mouseDown = currMouse.buttonDown(OIS.MB_Left)
 
        # Update the toggle timer.
        if self.toggle >= 0:
            self.toggle -= frameEvent.timeSinceLastFrame
 
 
        # Move the camera using keyboard input.
        transVector = ogre.Vector3(0, 0, 0)
        # Move Forward.
        if self.Keyboard.isKeyDown(OIS.KC_W):
           transVector.z -= self.move
        # Move Backward.
        if self.Keyboard.isKeyDown(OIS.KC_S):
            transVector.z += self.move
        # Strafe Left.
        if self.Keyboard.isKeyDown(OIS.KC_A):
            transVector.x -= self.move
        # Strafe Right.
        if self.Keyboard.isKeyDown(OIS.KC_D):
           transVector.x += self.move
        # Move Up.        
        if self.Keyboard.isKeyDown(OIS.KC_E):
            transVector.y += self.move
        # Move Down.
        if self.Keyboard.isKeyDown(OIS.KC_F):
            transVector.y -= self.move
 
        # Translate the camera based on time.
        self.camNode.translate(self.camNode.orientation
                              * transVector
                              * frameEvent.timeSinceLastFrame)
 
        # Rotate the camera when the Right mouse button is down.
        if currMouse.buttonDown(OIS.MB_Right):
           self.camNode.yaw(ogre.Degree(-self.rotate 
                            * currMouse.X.rel).valueRadians())
           self.camNode.getChild(0).pitch(ogre.Degree(-self.rotate
                                          * currMouse.Y.rel).valueRadians())

        self.handleShip(frameEvent)
 
        # If the escape key is pressed end the program.
        return not self.Keyboard.isKeyDown(OIS.KC_ESCAPE)


    def handleShip(self, frameEvent):
        '''Needs to set ent's velocity based on keypres'''

  
        sushilsBoat = self.entityMgr.entities[self.index]

        print "Selected", str(sushilsBoat.id)
        print "Velocity", str(sushilsBoat.vel)
        print "Pos", str(sushilsBoat.pos)
        # print "Heading", str(sushilsBoat.heading), str(sushilsBoat.desiredHeading)

# -------------------------------------------------------------------

        if self.toggle >= 0:
            self.toggle -= frameEvent.timeSinceLastFrame
        if self.toggle < 0 and self.Keyboard.isKeyDown(OIS.KC_TAB):
            sushilNode = self.sceneManager.getSceneNode(self.entityMgr.entities[self.index].id+'node')
            sushilNode.showBoundingBox(False)
            self.index += 1
            self.toggle = 0.4
            if self.index > 10:
                self.index = 0
            sushilsBoat = self.entityMgr.entities[self.index]
            self.entityMgr.selectedEntities = sushilsBoat
            sushilNode = self.sceneManager.getSceneNode(self.entityMgr.entities[self.index].id+'node')
            sushilNode.showBoundingBox(True)
#-----------------------------------------------------------------------

        if self.Keyboard.isKeyDown(OIS.KC_NUMPAD8) or self.Keyboard.isKeyDown(OIS.KC_I):
            sushilsBoat.desiredSpeed += .5

        if self.Keyboard.isKeyDown(OIS.KC_NUMPAD2) or self.Keyboard.isKeyDown(OIS.KC_K):
            sushilsBoat.desiredSpeed -= .5

        if self.Keyboard.isKeyDown(OIS.KC_NUMPAD4) or self.Keyboard.isKeyDown(OIS.KC_J):
            sushilsBoat.desiredHeading += .5

        if self.Keyboard.isKeyDown(OIS.KC_NUMPAD6) or self.Keyboard.isKeyDown(OIS.KC_L):
            sushilsBoat.desiredHeading -= .5

        if self.Keyboard.isKeyDown(OIS.KC_SPACE):
            sushilsBoat.desiredSpeed = 0.0

        return
 
class TutorialApplication(sf.Application):
    """The Application class."""
 
    def _createScene(self):
        # Setup a scene with a high level of ambient light.
        sceneManager = self.sceneManager
        sceneManager.ambientLight = 1.0, 1.0, 1.0
 

        surfaceHeight = -60
        # Setup a ground plane at -100 height so the entire cube shows up
        plane = ogre.Plane ((0, 1, 0), surfaceHeight)
        meshManager = ogre.MeshManager.getSingleton ()
        #large plane 10000x10000
        meshManager.createPlane ('Ground', 'General', plane,
                                     10000, 10000, 20, 20, True, 1, 5, 5, (0, 0, 1))
        groundEnt = sceneManager.createEntity('GroundEntity', 'Ground')
        sceneManager.getRootSceneNode().createChildSceneNode ().attachObject (groundEnt)
        groundEnt.setMaterialName ('Examples/TextureEffect2')
        groundEnt.castShadows = False
        #Like nice sky
        self.sceneManager.setSkyDome (True, "Examples/CloudySky", 5, 8)


        # Setup the first camera node and pitch node and aim it.
        camnode = sceneManager.getRootSceneNode().createChildSceneNode('CamNode1',
                                                               (0, 600, 700))
        camnode.pitch(ogre.Degree(-45))

        cnode = camnode.createChildSceneNode('PitchNode1')
        cnode.attachObject(self.camera)

#-------------------------------------------------------------------------------
        from manager import EntityMgr
        self.entityMgr = EntityMgr()
        i = 0;

        entType = self.entityMgr.entType    

        for ent in entType:
            self.entityMgr.createEntity (ent, i)
            entOgre = self.sceneManager.createEntity('boat'+str(i), self.entityMgr.entities[i].mesh)
            sushilNode = self.sceneManager.getRootSceneNode().createChildSceneNode('boat'+str(i)+'node', (i*300, 0, 0))
            sushilNode.attachObject(entOgre)
            self.entityMgr.entities[i].attachAspects(sushilNode)
            i+=1

        self.entityMgr.initSelect()
        sushilNode = self.sceneManager.getSceneNode(self.entityMgr.entities[0].id+'node')
        sushilNode.showBoundingBox(True)

#------------------------------------------------------------------------
 
    def _createCamera(self):
        self.camera = self.sceneManager.createCamera('PlayerCam')
        self.camera.nearClipDistance = 5
 
    def _createFrameListener(self):
        self.frameListener = TutorialFrameListener(self.renderWindow,
                                                   self.camera,
                                                   self.sceneManager, 
                                                   self.entityMgr)
        
        self.root.addFrameListener(self.frameListener)
        
        #add my ent frame listener
        self.controlFrameListener = ControlFrameListener(self.entityMgr)
        self.root.addFrameListener(self.controlFrameListener)

        self.frameListener.showDebugOverlay(True)
 
 
if __name__ == '__main__':
    try:
        ta = TutorialApplication()
        ta.go()
    except ogre.OgreException, e:
        print e
