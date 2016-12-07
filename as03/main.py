import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS
import SampleFramework as sf

# DANIEL SANCHEZ
# danielsanchez@nevada.unr.edu
# CS 381
# ASSIGNMENT 3
# 2/18/15 
 
class TutorialFrameListener(sf.FrameListener):
    """A FrameListener class that handles basic user input."""
 
    def __init__(self, renderWindow, camera, sceneManager):
        # Subclass any Python-Ogre class and you must call its constructor.
        sf.FrameListener.__init__(self, renderWindow, camera)
 
        # Key and mouse state tracking.
        self.toggle = 0
        self.mouseDown = False
 
        # Populate the camera and scene manager containers.
        self.camNode = camera.parentSceneNode.parentSceneNode
        self.sceneManager = sceneManager

        self.cubeNode01 = sceneManager.getSceneNode("CubeNode0")
        self.cubeNode02 = sceneManager.getSceneNode("CubeNode1")
        self.entNode = self.cubeNode01

        self.entVector = ogre.Vector3(0, 0, 0)
        self.tempVector = ogre.Vector3(0, 0, 0)


        #EDITS

        # Set the rotation and movement speed.
        self.rotate = 0.13
        self.move = 10
        self.entNum = 0;
 
    def frameStarted(self, frameEvent):
        # If the render window has been closed, end the program.
        if(self.renderWindow.isClosed()):
            return False

        # Capture and update each input device.
        self.Keyboard.capture()

        # Update the toggle timer.
        if self.toggle >= 0:
            self.toggle -= frameEvent.timeSinceLastFrame

        if self.toggle < 0 and self.Keyboard.isKeyDown(OIS.KC_TAB):
            # self.entVector = ogre.Vector3(0, 0, 0)
            self.toggle = 0.1
            self.entNum += 1
            if self.entNum > 1:
                self.entNum = 0;
            self.entNode = self.sceneManager.getSceneNode("CubeNode" + str(self.entNum))

        ### ENTITY 
        if self.Keyboard.isKeyDown(OIS.KC_NUMPAD4):
            self.entVector.x -= self.move

        if self.Keyboard.isKeyDown(OIS.KC_NUMPAD6):
            self.entVector.x += self.move

        if self.Keyboard.isKeyDown(OIS.KC_NUMPAD8):
            self.entVector.z -= self.move

        if self.Keyboard.isKeyDown(OIS.KC_NUMPAD2):
            self.entVector.z += self.move

        if self.Keyboard.isKeyDown(OIS.KC_PGUP):
            self.entVector.y += self.move

        if self.Keyboard.isKeyDown(OIS.KC_PGDOWN):
            self.entVector.y -= self.move

        if self.Keyboard.isKeyDown(OIS.KC_SPACE):
            self.entVector = ogre.Vector3(0, 0, 0)

        ### CAMERA
        camVector = ogre.Vector3(0, 0, 0)
        
        if self.Keyboard.isKeyDown(OIS.KC_A):
            camVector.x -= self.move

        if self.Keyboard.isKeyDown(OIS.KC_D):
            camVector.x += self.move

        if self.Keyboard.isKeyDown(OIS.KC_W):
            camVector.z -= self.move

        if self.Keyboard.isKeyDown(OIS.KC_S):
            camVector.z += self.move

        if self.Keyboard.isKeyDown(OIS.KC_F):
            camVector.y -= self.move

        if self.Keyboard.isKeyDown(OIS.KC_E):
            camVector.y += self.move

        # Translate the entity based on time.
        self.camNode.translate(self.camNode.orientation
                              * camVector
                              * frameEvent.timeSinceLastFrame)

        # Translate the camera based on time.
        self.entNode.translate(self.entNode.orientation * self.entVector * frameEvent.timeSinceLastFrame)

        # If the escape key is pressed end the program.
        return not self.Keyboard.isKeyDown(OIS.KC_ESCAPE)
 
class TutorialApplication(sf.Application):
    """The Application class."""
 
    def _createScene(self):
        surfaceHeight = -50

        # Setup a scene with a low level of ambient light.
        sceneManager = self.sceneManager
        sceneManager.ambientLight = 0.25, 0.25, 0.25
 
        # Setup first cube entity and attach it to a scene node.
        cube_0 = sceneManager.createEntity('cube0', 'cube.mesh')
        node = sceneManager.getRootSceneNode().createChildSceneNode('CubeNode0', (0,200,0))
        cube_0.setMaterialName( 'Examples/Borg' )
        node.attachObject(cube_0)

        # Setup second cube entity and attach it to a scene node.
        cube_1 = sceneManager.createEntity('cube1', 'cube.mesh')
        node = sceneManager.getRootSceneNode().createChildSceneNode('CubeNode1', (300,200, 0))
        cube_1.setMaterialName( 'Examples/Borg' )
        node.attachObject(cube_1)

        # Setup sky plane
        plane = ogre.Plane ((0, -1, 0), -10)
        self.sceneManager.setSkyPlane (True, plane, "Examples/CloudySky", 100, 45, True, 0.5, 150, 150)

        # Setup a ground plane.
        plane = ogre.Plane ((0, 1, 0), surfaceHeight)
        meshManager = ogre.MeshManager.getSingleton ()
        meshManager.createPlane ('Ground', 'General', plane,
                                     10000, 10000, 20, 20, True, 1, 5, 5, (0, 0, 1))
        ent = sceneManager.createEntity('GroundEntity', 'Ground')
        sceneManager.getRootSceneNode().createChildSceneNode ().attachObject (ent)
        ent.setMaterialName ('Examples/Rockwall')
        ent.castShadows = False

        # Setup a White point light.
        light = sceneManager.createLight('Light1')
        light.type = ogre.Light.LT_POINT
        light.position = 250, 150, 250
        light.diffuseColour = 1, 1, 1
        light.specularColour = 1, 1, 1

        # Setup the first camera node and pitch node and aim it.
        node = sceneManager.getRootSceneNode().createChildSceneNode('CamNode1',(0, 400, 2000))
        node = node.createChildSceneNode('PitchNode1')
        node.attachObject(self.camera)
 
    def _createCamera(self):
        self.camera = self.sceneManager.createCamera('PlayerCam')
        self.camera.nearClipDistance = 5
 
    def _createFrameListener(self):
        self.frameListener = TutorialFrameListener(self.renderWindow,
                                                   self.camera,
                                                   self.sceneManager)
        self.root.addFrameListener(self.frameListener)
        self.frameListener.showDebugOverlay(True)
 
 
if __name__ == '__main__':
    try:
        ta = TutorialApplication()
        ta.go()
    except ogre.OgreException, e:
        print e
