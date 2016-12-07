import ogre.renderer.OGRE as ogre
import thickCircle as tc

class Renderer:
    def __init__(self, ent):
        self.ent = ent
        self.entOgre = self.ent.engine.gfxMgr.sceneManager.createEntity(self.ent.uiname + str(self.ent.engine.entityMgr.nEnts), self.ent.mesh)
        
        self.node = self.ent.engine.gfxMgr.sceneManager.getRootSceneNode().createChildSceneNode(self.ent.uiname +'node', self.ent.pos)

        self.node.attachObject(self.entOgre)


        if (self.ent.mesh == "ninja.mesh"):
            if (self.ent.team == 1):
                self.ent.color = "RedCircle"
            if (self.ent.team == 2):
                self.ent.color = "BlueCircle"

            self.ent.circle = tc.ThickCircle(self.ent.uiname + ".sc", self.ent.engine.gfxMgr.sceneManager, parentNode = self.node)
            self.ent.circle.setup(color = self.ent.color, radius = 70, thickness = 25)
            self.ent.circle.hide()
        
        #yuck spagetti code :(
        if (self.ent.mesh == "sphere.mesh"):
            self.entOgre.setMaterialName ("Ball")
        elif (self.ent.hasAnimation and self.ent.material):
            self.entOgre.setMaterialName (self.ent.material)

        
        self.ent.node = self.node
        
        self.node.scale(self.ent.scale)   
        if (self.ent.mesh == "goals.mesh"):
            self.ent.node.showBoundingBox(False)

        
        wakeOffsetz = self.entOgre.getBoundingBox().getSize().z / 2
        wakeOffsetx = self.entOgre.getBoundingBox().getSize().x / 2
                
        if self.ent.offset != 0:
            #add wake and offset 3rd person camera because lookat won't work
            self.wakeNode = self.node.createChildSceneNode(ogre.Vector3(0, 0, -wakeOffsetz))
            
            camNode = self.node.createChildSceneNode(self.ent.uiname +'camNode', ogre.Vector3(0, 2 * wakeOffsetx, -3 * wakeOffsetz))
            camNode.yaw(ogre.Degree(180))
        else:
                     
            self.wakeNode = self.node.createChildSceneNode(ogre.Vector3(-wakeOffsetx, 0, 0))
            
            #adjust yaw and pitch because lookat isn't working
            camNode = self.node.createChildSceneNode(self.ent.uiname +'camNode', ogre.Vector3( -3 * wakeOffsetx, 2 * wakeOffsetz, 0))         
            camNode.yaw(ogre.Degree(-90))

        self.wakeParticle = self.ent.engine.gfxMgr.sceneManager.createParticleSystem(self.ent.uiname + str(self.ent.engine.entityMgr.nEnts) + "_wake", 'Water/Wake' + self.ent.wakeSize)
        self.wakeNode.attachObject(self.wakeParticle)

    def tick(self, dtime):
        if (self.ent.mesh == "sphere.mesh"):
            self.entOgre.setMaterialName ("Ball")
        elif (self.ent.hasAnimation and self.ent.material):
            self.entOgre.setMaterialName (self.ent.material)

        self.ent.node.setPosition(self.ent.pos)

        self.ent.node.resetOrientation()
        #for jetski
        self.wakeNode.yaw(self.ent.offset);
        self.ent.node.yaw(self.ent.offset);
        self.ent.node.yaw(ogre.Degree(self.ent.heading))  
        
        
        if (self.ent.mesh == "post.mesh"):
            #self.ent.node.pitch(200)
            
            #self.ent.node.roll(90)
            #self.ent.node.yaw(90)
            pass
                 
        if (self.ent.slide):
            if (self.ent.heading > 180):
                self.node.roll(80)

            if (self.ent.heading <= 180):
                self.node.roll(-80)
                

        if (self.ent.hasAnimation):
            if self.ent.speed > 0:
                self.wakeNode.setVisible(True)
                self.animationState = self.entOgre.getAnimationState('Walk')
                self.animationState.setLoop(True)
                self.animationState.setEnabled(True)
                self.animationState.addTime(2 *dtime)
            
            else: 
                self.wakeNode.setVisible(False)
                self.animationState = self.entOgre.getAnimationState('Idle1')
                self.animationState.setLoop(True)
                self.animationState.setEnabled(True)
                self.animationState.addTime(dtime)
        else:
            if self.ent.speed > 0: 
                ent = self.ent
                self.ent.node.pitch(ent.vel.x)
                #self.ent.node.roll(ent.vel.z)


                
