import ogre.renderer.OGRE as ogre

class Renderer:
    def __init__(self, ent):
        self.ent = ent
        self.entOgre = self.ent.engine.gfxMgr.sceneManager.createEntity(self.ent.uiname + str(self.ent.engine.entityMgr.nEnts), self.ent.mesh)
        
        self.node = self.ent.engine.gfxMgr.sceneManager.getRootSceneNode().createChildSceneNode(self.ent.uiname +'node', self.ent.pos)
        
        self.node.attachObject(self.entOgre)
        self.ent.node = self.node
        
        self.node.scale(self.ent.scale)   
        
        wakeOffsetz = self.entOgre.getBoundingBox().getSize().z / 2
        wakeOffsetx = self.entOgre.getBoundingBox().getSize().x / 2
                
        #for jetski and models that are not facing right
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
        self.ent.node.setPosition(self.ent.pos)

        self.ent.node.resetOrientation()
        #for jetski
        self.wakeNode.yaw(self.ent.offset);
        self.ent.node.yaw(self.ent.offset);
        self.ent.node.yaw(ogre.Degree(self.ent.heading))   
        
        if self.ent.speed > 0:
            self.wakeNode.setVisible(True)
        else: 
            self.wakeNode.setVisible(False)
          
