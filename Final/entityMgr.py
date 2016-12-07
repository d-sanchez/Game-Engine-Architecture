import ent
from vector import MyVector
import random
import utils

class EntityMgr:
    def __init__(self, engine):
        #print "__init__ EntityMgr"
        self.engine = engine

    def init(self):
        self.entities = {}
        self.nEnts = 0

        self.selectedEntP1 = None
        self.selectedEntP2 = None
        self.GKP1 = None
        self.GKP2 = None

        self.selectedEnt = None
        
        self.selectedEntIndex = 0
        self.selectedEntIndexP1 = -1
        self.selectedEntIndexP2 = -1
        self.team1 = {}
        self.team2 = {}
        self.nP1 = 0
        self.nP2 = 0
        self.selectedEntities = []

        self.entTypes = [ent.Liverpool, ent.BVB, ent.Arsenal, ent.Chelsea, ent.EgbertTeam]
        self.ballEnt = ent.Ball
        self.ball = None
        self.stands = ent.Stands
        self.top = ent.TopStad
        self.lowWall = ent.lowWall
        self.stadiumParts = [ent.Stands, ent.TopStad, ent.lowWall, ent.Entrance, ent.highWall, ent.midWall, ent.postL, ent.RoofFrame, ent.stairs, ent.postR]

    def createEnt(self, entType, pos = MyVector(0,0,0), yaw = 0, team = 0):
        ent = entType(self.engine, self.nEnts, pos = pos, yaw = yaw, team = team)
        ent.init()
  
        self.entities[self.nEnts] = ent
        self.selectedEnt = ent
        self.selectedEntIndex = self.nEnts;
        
        self.nEnts = self.nEnts+1        
        
        if (team == 1):
            print ent
            self.team1[self.nP1] = ent 
            ent.team = 1
            self.nP1 +=1
        elif (team == 2): 
            self.team2[self.nP2] = ent
            self.nP2 +=1 
            ent.team = 2
        
        if (ent.mesh == "sphere.mesh"):
            self.ball = ent

        return ent
        
    def createStad(self):
        for entType in self.stadiumParts:
         
            ent = self.createEnt(entType)
            

    def getNextEnt(self, team):
        if (team == 1):
            if self.selectedEntIndexP1 >= self.nP1 - 1:
                self.selectedEntIndexP1 = 0
            else:
                self.selectedEntIndexP1 += 1
        
           # print self.team1
            self.selectedEntP1 = self.team1[self.selectedEntIndexP1]
            #print "EntMgr selected: ", str(self.selectedEnt)
            return self.selectedEntP1
        else:
            if self.selectedEntIndexP2 >= self.nP2 - 1:
                self.selectedEntIndexP2 = 0
            else:
                self.selectedEntIndexP2 += 1
        
            print self.team2
            self.selectedEntP2 = self.team2[self.selectedEntIndexP2]
            #print "EntMgr selected: ", str(self.selectedEnt)
            return self.selectedEntP2
    
    def getPlayerClosestToBall(self, team):
        teamList = []
        teamList.append(self.engine.entityMgr.team1)
        teamList.append(self.engine.entityMgr.team2)
        closestTeammate = None
        shortDist = 10000000 #infinity
        ball = self.ball
        index = -1
        
        for ent in teamList[team - 1].values():
            dist = utils.distance(ball, ent)
            index += 1
            if (shortDist > dist):
                shortDist = dist
                closestTeammate = ent
        

        if (team == 1):
            self.selectedEntP1 = closestTeammate
            self.selectedEntIndexP1 = index

        elif (team == 2):
            self.selectedEntP2 = closestTeammate
            self.selectedEntIndexP2 = index

        return closestTeammate

    def getSelected(self, team):
        if (team == 1):
            return self.selectedEntP1
        else:
            return self.selectedEntP2

    def tick(self, dt):
        #an entity that show up later in a list will alway win a tackle unless we randomize their order
        collisionList = self.entities.values()
        random.shuffle(collisionList)
        
        for entity in collisionList:
        
            entity.tick(dt)



    def addAction(self, entity, action):
        entity.aspects[2].ActionList.append(action)
    