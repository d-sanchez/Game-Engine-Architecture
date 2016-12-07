import ogre.io.OIS as OIS
    
class SelectionMgr:

    def __init__(self, engine):
        self.engine = engine

    def init(self):
        self.keyboard = self.engine.inputMgr.keyboard
        self.toggle = 0.1

    def tick(self, dt):
        if self.toggle >=0:
            self.toggle -= dt
        selectedEntIndex = self.engine.entityMgr.selectedEntIndex
        #print "selected: ", str(selectedEntIndex)

        if self.toggle < 0 and self.keyboard.isKeyDown(OIS.KC_TAB):
            self.toggle = 0.4
            #print "tab test"

            if self.keyboard.isKeyDown(OIS.KC_LSHIFT):
                self.addNextEnt()
            else:
                self.selectNextEnt()

            # ent = self.engine.entityMgr.selectedEnt
            # ent.node.showBoundingBox(False)
            # ent = self.engine.entityMgr.getNextEnt()
            # self.engine.entityMgr.selectedEntities = []            
            # ent.node.showBoundingBox(True)


    def addNextEnt(self):
        ent = self.engine.entityMgr.getNextEnt()
        ent.node.showBoundingBox(True)
        self.engine.entityMgr.selectedEntities.append(ent)

    def selectNextEnt(self):
        for ent in self.engine.entityMgr.selectedEntities:
            ent.node.showBoundingBox(False)
        self.engine.entityMgr.selectedEntities = []
        self.addNextEnt()


    def stop(self):
        pass
