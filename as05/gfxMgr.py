import os

import ogre.renderer.OGRE as ogre
# import ogre.sound.OgreAL as OgreAl

class GfxMgr:

    def __init__(self, engine):
        self.engine = engine
        self.entityMgr = engine.entityMgr
        self.configPath = ""
        self.pluginsPath =  os.path.join(self.configPath, "plugins.cfg")
        self.resourcesPath = os.path.join(self.configPath, "resources.cfg")
        print "__init__ GfxMgr"

    def init(self):
        self.createRoot()
        self.defineResources()
        self.setupRenderSystem()
        self.createRenderWindow()
        self.initializeResourceGroups()
        self.setupScene()

    # The Root constructor for the ogre
    def createRoot(self):
        self.root = ogre.Root(self.pluginsPath)

    def defineResources(self):
        cf = ogre.ConfigFile()
        cf.load(self.resourcesPath)
        seci = cf.getSectionIterator()

        while seci.hasMoreElements():
            secName = seci.peekNextKey()
            settings = seci.getNext()
            
            for item in settings:
                typeName = item.key
                archName = item.value
                ogre.ResourceGroupManager.getSingleton().addResourceLocation(archName, typeName, secName)

    # Create and configure the rendering system (either DirectX or OpenGL) here
    def setupRenderSystem(self):
        print "setupRenderSystem"
        if not self.root.restoreConfig() and not self.root.showConfigDialog():
            raise Exception("User canceled the config dialog -> Application.setupRenderSystem()")

    # Create the render window
    def createRenderWindow(self):
        self.root.initialise(True, "Tutorial Render Window")
        self.renderWindow = self.root.getAutoCreatedWindow()

    # Initialize the resources here (which were read from resources.cfg in defineResources()
    def initializeResourceGroups(self):
        ogre.TextureManager.getSingleton().setDefaultNumMipmaps(5)
        ogre.ResourceGroupManager.getSingleton().initialiseAllResourceGroups()

    # Now, create a scene here. Three things that MUST BE done are sceneManager, camera and
    # viewport initializations
    def setupScene(self):
        self.createSceneManager()
        self.createCamera()
        self.createViewport()
        self.createWorld()


    def createSceneManager(self):
        self.sceneManager = self.root.createSceneManager(ogre.ST_GENERIC, "Default SceneManager")

    def createCamera(self):
        self.camera = self.sceneManager.createCamera("Camera")
        self.camera.nearClipDistance = 10
        yawNode = self.sceneManager.getRootSceneNode().createChildSceneNode("RTSCamNode", (0, 250, 1200))
        yawNode.yaw(ogre.Degree(0))
        yawNode.createChildSceneNode("RTSPitchNode").attachObject(self.camera)
        self.camera.lookAt = (0, 0, 0)
        
         
    def createViewport(self):
        viewPort = self.root.getAutoCreatedWindow().addViewport(self.camera)

    def createWorld(self):
        # surfaceHeight = -15
        plane = ogre.Plane ((0, 1, 0), -5)
        meshManager = ogre.MeshManager.getSingleton ()
        meshManager.createPlane ('Ground', 'General', plane,
                                     10000, 10000, 20, 20, True, 1, 5, 5, (0, 0, 1))
        groundEnt = self.sceneManager.createEntity('GroundEntity', 'Ground')
        self.sceneManager.getRootSceneNode().createChildSceneNode().attachObject(groundEnt)
        groundEnt.setMaterialName ('Ocean2_Cg')
        groundEnt.castShadows = False

        self.sceneManager.setSkyDome(True, "Examples/CloudySky", 5, 8)
        self.waterPlane = plane
 
    def tick(self, dt):
        self.root.renderOneFrame()

    def stop(self):
        pass


