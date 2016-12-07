import ent
import ogre.renderer.OGRE as ogre

class EntityMgr:
    def __init__(self):
        self.entities = []
        self.selectedEntities = None
        #self.entType = [ent.Cigarette,]
        self.entType = [ent.Missile, ent.Cvn, ent.Sleek, ent.Ddg51, ent.Watercr,
                        ent.Monterey, ent.Boat5086, ent.Cigarette,
                        ent.Alienship, ent.Boat, ent.Sailboat, ]

    def createEntity(self, ent, index):
        i = index
        sushilEnt = ent(id = 'boat'+str(i), pos = ogre.Vector3(i*300, 0, 0))
        self.entities.append(sushilEnt)

    def initSelect(self):
        self.selectedEntities = self.entities[0]

