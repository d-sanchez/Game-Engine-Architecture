import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS

class InputMgr(OIS.KeyListener, OIS.MouseListener):
    def __init__(self, engine):
        #print "__init__ InputMgr"
        self.engine = engine
        OIS.KeyListener.__init__(self)
        OIS.MouseListener.__init__(self)
        self.transVector = ogre.Vector3(0, 0, 0)
        self.toggle = 0.1
        self.rotate = 0.01
        self.yaw = 0.0
        self.pitch = 0.0
        self.move = 1000
        self.heldTime = 0.0


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
        self.usingRTSCam = False

    def tick(self, dt):
        self.dt = dt
        self.keyboard.capture()
        self.mouse.capture()
        self.keyPressed(dt)
        self.keyReleased(dt)

        #self.currMouse = self.mouse.getMouseState()

        # Translate the camera based on time.

        if (self.usingRTSCam):
            
            self.RTSCamNode.resetOrientation()
            self.camPitchNode.resetOrientation()

            self.RTSCamNode.yaw(ogre.Radian(self.yaw))
            self.camPitchNode.pitch(ogre.Radian(self.pitch))
            self.RTSCamNode.translate(self.RTSCamNode.orientation
                              * self.transVector
                              * dt)
            #print self.RTSCamNode.orientation
        else:
            ball = self.engine.entityMgr.ball
            #if (ball.attachEnt):
            pos = self.RTSCamNode.getPosition()
            self.RTSCamNode.setPosition(ogre.Vector3(ball.pos.x, pos.y, pos.z));
    

    def keyPressed(self, frameEvent):
        #print "in keypressed funtion"
        #print dt
        # Move the camera using keyboard input.
        self.transVector = ogre.Vector3(0, 0, 0)

        if self.keyboard.isKeyDown(OIS.KC_SPACE):
            self.heldTime += self.dt

        # Move Forward.
        if self.keyboard.isKeyDown(OIS.KC_W):
            self.transVector.z -= self.move
            #print self.transVector.z
        
        # Move Backward.
        if self.keyboard.isKeyDown(OIS.KC_S):
            self.transVector.z += self.move
            #print self.transVector.z
        # Strafe Left.
        if self.keyboard.isKeyDown(OIS.KC_A):
            self.transVector.x -= self.move
            #print self.transVector.x
        # Strafe Right.
        if self.keyboard.isKeyDown(OIS.KC_D):
            self.transVector.x += self.move
            #print self.transVector.x
        if self.keyboard.isKeyDown(OIS.KC_Q):
            self.yaw += self.rotate
            
        if self.keyboard.isKeyDown(OIS.KC_E):
            self.yaw -= self.rotate
        
        if self.keyboard.isKeyDown(OIS.KC_Z):
            self.pitch += self.rotate
            #print self.pitch
        if self.keyboard.isKeyDown(OIS.KC_X):
            self.pitch -= self.rotate    
            #print self.pitch
        # Move Up.        
        if self.keyboard.isKeyDown(OIS.KC_PGUP):
            self.transVector.y += self.move
        # Move Down.
        if self.keyboard.isKeyDown(OIS.KC_PGDOWN):
            self.transVector.y -= self.move

        if self.keyboard.isKeyDown(OIS.KC_7):
            #print "yeyo"
            self.engine.aiMgr.simpleAI = False
        


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

        if self.keyboard.isKeyDown(OIS.KC_3):
            self.usingRTSCam = not self.usingRTSCam

        if self.keyboard.isKeyDown(OIS.KC_2):
            print "YO CAMERA 2"
            # Update the toggle timer.
            self.toggle = 0.1

            # add case of no selection
            if self.engine.entityMgr.selectedEntities != []:
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
        if not self.keyboard.isKeyDown(OIS.KC_SPACE):
            #print self.heldTime
            self.heldTime = 0.0
        return True

    def mouseMoved(self, frameEvent):
        return True
 
    def mousePressed(self, frameEvent, id):
        if id == OIS.MB_Left:
            self.mouse.capture()
            currMouse = self.mouse.getMouseState()
   
            self.engine.selectionMgr.checkPointAt(currMouse.X.abs, currMouse.Y.abs)
            
            print str(currMouse.X.abs) + "," + str(currMouse.Y.abs)
            
            
        return True
 
    def mouseReleased(self, frameEvent, id):
        return True

    def stop(self):
        pass

  
