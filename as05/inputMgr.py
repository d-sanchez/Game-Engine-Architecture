import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS

class InputMgr(OIS.KeyListener, OIS.MouseListener):
    def __init__(self, engine):
        print "__init__ InputMgr"
        self.engine = engine
        OIS.KeyListener.__init__(self)
        OIS.MouseListener.__init__(self)
        self.transVector = ogre.Vector3(0, 0, 0)
        self.toggle = 0.1
        self.rotate = 0.01
        self.yaw = 0.0
        self.pitch = 0.0
        self.move = 500


    def init(self):
        windowHandle = 0
        renderWindow = self.engine.gfxMgr.root.getAutoCreatedWindow()
        windowHandle = renderWindow.getCustomAttributeUnsignedLong("WINDOW")
        paramList = [("WINDOW", str(windowHandle))]

        t = [("x11_mouse_grab", "false"), ("x11_mouse_hide", "false")]
        paramList.extend(t)
        self.inputManager = OIS.createPythonInputSystem(paramList)
        self.keyboard = None
        self.mouse = None

        try:
            self.keyboard = self.inputManager.createInputObjectKeyboard(OIS.OISKeyboard, True)
            self.mouse = self.inputManager.createInputObjectMouse(OIS.OISMouse, True )
        except Exception, e:
            print "No Keyboard or Mouse!!!!"
            raise e

        # if self.mouse:
        self.mouse.setEventCallback(self)
        self.keyboard.setEventCallback(self) 

        self.RTSCamNode = self.engine.gfxMgr.sceneManager.getSceneNode("RTSCamNode")
        self.camPitchNode = self.engine.gfxMgr.sceneManager.getSceneNode("RTSPitchNode")
        self.usingRTSCam = True

    def tick(self, dt):
        self.keyboard.capture()
        self.mouse.capture()
        self.keyPressed(dt)

        self.currMouse = self.mouse.getMouseState()

        # Translate the camera based on time.
        if (self.usingRTSCam):
            
            self.RTSCamNode.resetOrientation()
            self.camPitchNode.resetOrientation()

            self.RTSCamNode.yaw(ogre.Radian(self.yaw))
            self.camPitchNode.pitch(ogre.Radian(self.pitch))
            self.RTSCamNode.translate(self.RTSCamNode.orientation
                              * self.transVector
                              * dt)

    def keyPressed(self, frameEvent):
        #print "in keypressed funtion"

        # Move the camera using keyboard input.
        self.transVector = ogre.Vector3(0, 0, 0)
        
        # Move Forward.
        if self.keyboard.isKeyDown(OIS.KC_W):
            self.transVector.z -= self.move
        
        # Move Backward.
        if self.keyboard.isKeyDown(OIS.KC_S):
            self.transVector.z += self.move
        
        # Strafe Left.
        if self.keyboard.isKeyDown(OIS.KC_A):
            self.transVector.x -= self.move
        
        # Strafe Right.
        if self.keyboard.isKeyDown(OIS.KC_D):
            self.transVector.x += self.move

        if self.keyboard.isKeyDown(OIS.KC_Q):
            self.yaw += self.rotate
            
        if self.keyboard.isKeyDown(OIS.KC_E):
            self.yaw -= self.rotate
        
        if self.keyboard.isKeyDown(OIS.KC_Z):
            self.pitch += self.rotate
        
        if self.keyboard.isKeyDown(OIS.KC_X):
            self.pitch -= self.rotate    

        # Move Up.        
        if self.keyboard.isKeyDown(OIS.KC_PGUP):
            self.transVector.y += self.move
        # Move Down.
        if self.keyboard.isKeyDown(OIS.KC_PGDOWN):
            self.transVector.y -= self.move


        self.shiftKeyDown = self.keyboard.isKeyDown(OIS.KC_LSHIFT)

        if self.keyboard.isKeyDown(OIS.KC_1):
            print "YO CAMERA 1"
            # Update the toggle timer.
            self.toggle = 0.1

            # Attach the camera to RTS camera
            self.engine.gfxMgr.camera.parentSceneNode.detachObject(self.engine.gfxMgr.camera)
            self.camPitchNode = self.engine.gfxMgr.sceneManager.getSceneNode("RTSPitchNode")
            self.camPitchNode.attachObject(self.engine.gfxMgr.camera)
            #self.engine.gfxMgr.camera.lookAt = (0, 0, 0)
            self.usingRTSCam = True

        if self.keyboard.isKeyDown(OIS.KC_2):
            print "YO CAMERA 2"
            # Update the toggle timer.
            self.toggle = 0.1

            # Attach the camera to 3rd person camera
            self.engine.gfxMgr.camera.parentSceneNode.detachObject(self.engine.gfxMgr.camera)
            self.camPitchNode = self.engine.gfxMgr.sceneManager.getSceneNode(self.engine.entityMgr.selectedEntities[0].uiname + 'camNode')
            
            self.camPitchNode.attachObject(self.engine.gfxMgr.camera)
            self.usingRTSCam = False

        if self.keyboard.isKeyDown(OIS.KC_ESCAPE):
            #print "escape key pressed"
            self.engine.stop()
        
        return not self.keyboard.isKeyDown(OIS.KC_ESCAPE)

    def keyReleased(self, frameEvent):
        return True

    def mouseMoved(self, frameEvent):
        return True
 
    def mousePressed(self, frameEvent, id):
        if id == OIS.MB_Left:
            self.mouseSelectEntity()
        return True
 
    def mouseReleased(self, frameEvent, id):
        return True

    def stop(self):
        pass

    def mouseSelectEntity(self):
        self.mouse.capture()
        self.currMouse = self.mouse.getMouseState()

        if not self.shiftKeyDown:
            for ent in self.engine.entityMgr.selectedEntities:
                ent.node.showBoundingBox(False)
                self.engine.entityMgr.selectedEntities = []
        
        pos, ents = self.castRay(self.currMouse)

        for ent in ents:
            self.engine.entityMgr.selectedEntities.append(ent)
            ent.node.showBoundingBox(True)


    def castRay(self, currMouse):
        currMouse.width = self.engine.gfxMgr.renderWindow.getWidth()
        currMouse.height = self.engine.gfxMgr.renderWindow.getHeight()
        mouseRay = self.engine.gfxMgr.camera.getCameraToViewportRay(currMouse.X.abs/float(currMouse.width), 
                                                                    currMouse.Y.abs/float(currMouse.height))
        result  =  mouseRay.intersects(self.engine.gfxMgr.waterPlane)        

        if result.first:
            pos =  mouseRay.getPoint(result.second)
            return self.checkForEntsInRadius(pos, 23000)


    def checkForEntsInRadius(self, pos, radiusSquared):
        entities = []
        #for name, ent in self.engine.entityMgr.entities.iteritems():
        for ent in self.engine.entityMgr.entities.values():
            dist = ent.pos.squaredDistance(pos)
            if dist < radiusSquared:
                entities.append(ent)
        return (pos, entities)
            
