import ent
from vector import MyVector

class EntityMgr:
    def __init__(self, engine):
        print "__init__ EntityMgr"
        self.engine = engine

    def init(self):
        self.entities = {}
        self.nEnts = 0

        self.selectedEnt = None
        self.selectedEntIndex = 0
        self.selectedEntities = []

        #-----------------------------------------------------------------------------------------
        self.musicVolume = 1.0
        self.soundManager = None
        #-----------------------------------------------------------------------------------------
        
        # self.entTypes = [ent.Ddg51, ent.Cvn,]
        self.entTypes = [ent.Cvn, ent.Sleek, ent.Ddg51, ent.Watercr,
                         ent.Monterey, ent.Boat5086, ent.Cigarette,
                         ent.Alienship, ent.Boat, ent.Sailboat, ]

    def createEnt(self, entType, pos = MyVector(0,0,0), yaw = 0):
        ent = entType(self.engine, self.nEnts, pos = pos, yaw = yaw)
        ent.init()
        self.entities[self.nEnts] = ent
        self.selectedEnt = ent
        self.selectedEntIndex = self.nEnts;

        self.nEnts = self.nEnts+1        
        return ent


    def getNextEnt(self):
        if self.selectedEntIndex >= self.nEnts - 1:
            self.selectedEntIndex = 0
        else:
            self.selectedEntIndex += 1

        self.selectedEnt = self.entities[self.selectedEntIndex]
        #print "EntMgr selected: ", str(self.selectedEnt)
        return self.selectedEnt

    def getSelected(self):
        return self.selectedEnt

    def tick(self, dt):
        for eid, entity in self.entities.iteritems():
            entity.tick(dt)
