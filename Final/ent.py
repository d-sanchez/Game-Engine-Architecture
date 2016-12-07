# Entity class to hold information about entities for 38Engine
# Daniel Sanchez

import ogre.renderer.OGRE as ogre
from physics import Physics
from renderer import Renderer
from vector import MyVector
from playerAI import PlayerAI
import utils 
import math
# import time


class Entity:
    def __init__(self, engine, id, pos = MyVector(0,0,0), mesh = 'robot.mesh', 
                                  vel = MyVector(0,0,0), yaw = 0):
        self.engine = engine
        self.id = id
        self.pos = pos
        self.vel = ogre.Vector3(0, 0, 0)
        self.mesh = mesh
        self.node  = None
        self.yaw = 0
        self.deltaSpeed = 5
        self.deltaYaw = 0.0
        self.speed = 0.0
        self.heading = 0.0
        self.aspectTypes = [Physics, Renderer, PlayerAI]
        self.aspects = []
        self.scale = ogre.Vector3(1, 1, 1)
        self.wakeSize = 'Small'
        self.hasAnimation = False

        #Make jet ski face the same way
        self.offset = 0
        self.team = 0

        #home is init start
        self.home = pos
        self.slide = False

    def init(self):
        self.initAspects()


    def initAspects(self):
        for aspType in self.aspectTypes:
            self.aspects.append(aspType(self))

    def tick(self, dtime):
        for aspect in self.aspects:
            aspect.tick(dtime)


    def __str__(self):
        x = "Entity: %s \nPos: %s, Vel: %s, yaw: %f" % (self.id, str(self.pos), str(self.vel), self.yaw)
        return x

    def nearestTeamate(self):
        team = self.team
        teamList = []
        teamList.append(self.engine.entityMgr.team1)
        teamList.append(self.engine.entityMgr.team2)
        closestTeammate = None
        length = 10000000 #infinity

        for ent in teamList[team - 1].values():
            if (ent != self):
                x = 1200.0 * math.cos(self.heading)
                z = 1200.0 * math.sin(self.heading)
           # print x
           # print z
            #weird vector 2 bug
                vecA = ogre.Vector3( x - self.pos.x , z - self.pos.z, 0)
                vecB = ogre.Vector3(ent.pos.x - self.pos.x, ent.pos.z - self.pos.z, 0)

                dAngle = vecA.angleBetween(vecB).valueDegrees()      
            #print ent.uiname, ",", dAngle
                if (float(math.fabs(dAngle)) < 50.0):
                #store good teammates to array

                    if (vecB.length() < length):
                        length = vecB.length()
                        if (ent != self):
                            closestTeammate = ent

             
        return closestTeammate
                             


        pass

    

class Ball(Entity):
    id = 0
    def __init__(self, engine, id, pos = MyVector(0,0,0), vel = MyVector(0,0,0), yaw = 0, team = 0):
        Entity.__init__(self, engine, id, pos = MyVector(0,25,0), vel = vel, yaw = yaw) 
        self.mesh = 'sphere.mesh'
        self.uiname = 'Ball' + str(Ball.id)
        Ball.id += 1
        self.acceleration = 250
        self.turningRate = 30
        self.maxSpeed = 1000
        self.desiredSpeed = 0
        self.desiredHeading = 90
        self.speed = 0
        self.heading = 90    
        self.wakeSize = 'Large'
        self.scale = ogre.Vector3(.5, .5, .5)
        self.wakeSize = 'Large'
        self.pitch = 0.0
        self.spin = 0.0
        self.attachEnt = None
        self.toggle = 0.0
        self.radiiNorm = 25.0
        self.radiiSlide = 25.0
        #self.tackleToggle = 0.0
        

class Arsenal(Entity):
    id = 0
    defaultMat = "Examples/RedTeam"

    def __init__(self, engine, id, pos = MyVector(0, 0 ,0), vel = MyVector(0, 0, 0), yaw = 0, team = 0):
        self.team = team
        Entity.__init__(self, engine, id, pos = pos, vel = vel, yaw = yaw)
        print "player init"
        self.mesh = 'ninja.mesh'
        self.uiname = 'Arsenal' + str(Arsenal.id)
        Arsenal.id += 1
        self.acceleration = 360
        self.turningRate = 120
        self.maxSpeed = 400
        self.desiredSpeed = 0
        self.desiredHeading = 0
        self.speed = 0
        self.heading = 0
        self.wakeSize = 'Large'
        self.offset = ogre.Degree(-90)
        self.hasAnimation = True
        self.scale = ogre.Vector3(.5, .5, .5)
        #changed
        self.material = "Examples/RedTeam"
        self.color = "RedCircle"
        self.circle = None
        self.team = team

        self.radiiNorm = 115.0
        self.radiiSlide = 200.0


class EgbertTeam(Entity):
    id = 0
    defaultMat = "Examples/EgbertTeam"

    def __init__(self, engine, id, pos = MyVector(0, 0 ,0), vel = MyVector(0, 0, 0), yaw = 0, team = 0):
        Entity.__init__(self, engine, id, pos = pos, vel = vel, yaw = yaw)
        print "player init"
        self.mesh = 'ninja.mesh'
        self.uiname = 'EgbertTeam' + str(EgbertTeam.id)
        EgbertTeam.id += 1
        self.acceleration = 360
        self.turningRate = 120
        self.maxSpeed = 400
        self.desiredSpeed = 0
        self.desiredHeading = 0
        self.speed = 0
        self.heading = 0
        self.wakeSize = 'Large'
        self.offset = ogre.Degree(-90)
        self.hasAnimation = True
        self.scale = ogre.Vector3(.5, .5, .5)
        #changed
        self.material = "Examples/EgbertTeam"
        self.color = "RedCircle"
        self.circle = None
        self.team = team

        self.radiiNorm = 115.0
        self.radiiSlide = 200.0


class Liverpool(Entity):
    id = 0
    defaultMat = "Examples/SushilTeam"

    def __init__(self, engine, id, pos = MyVector(0, 0 ,0), vel = MyVector(0, 0, 0), yaw = 0, team = 0):
        Entity.__init__(self, engine, id, pos = pos, vel = vel, yaw = yaw)
        print "player init"
        self.mesh = 'ninja.mesh'
        self.uiname = 'Liverpool' + str(Liverpool.id)
        Liverpool.id += 1
        self.acceleration = 360
        self.turningRate = 120
        self.maxSpeed = 400
        self.desiredSpeed = 0
        self.desiredHeading = 0
        self.speed = 0
        self.heading = 0
        self.wakeSize = 'Large'
        self.offset = ogre.Degree(-90)
        self.hasAnimation = True
        self.scale = ogre.Vector3(.5, .5, .5)
        #changed
        self.material = "Examples/SushilTeam"
        self.color = "RedCircle"
        self.circle = None
        self.team = team

        
        self.radiiNorm = 115.0
        self.radiiSlide = 200.0

class Chelsea(Entity):
    id = 0
    defaultMat = "Examples/BlueTeam"

    def __init__(self, engine, id, pos = MyVector(0, 0 ,0), vel = MyVector(0, 0, 0), yaw = 0, team = 0):
        self.team = team
        Entity.__init__(self, engine, id, pos = pos, vel = vel, yaw = yaw)
        print "player init"
        self.mesh = 'ninja.mesh'
        self.uiname = 'Chelsea' + str(Chelsea.id)
        Chelsea.id += 1
        self.acceleration = 360
        self.turningRate = 120
        self.maxSpeed = 400
        self.desiredSpeed = 0
        self.desiredHeading = 0
        self.speed = 0
        self.heading = 0
        self.wakeSize = 'Large'
        self.offset = ogre.Degree(-90)
        self.hasAnimation = True
        self.scale = ogre.Vector3(.5, .5, .5)
        #changed
        self.material = "Examples/BlueTeam"
        self.color = "RedCircle"
        self.circle = None
        self.team = team


        self.radiiNorm = 115.0
        self.radiiSlide = 200.0

   
class BVB(Entity):
    id = 0
    defaultMat = "Examples/YellowTeam"
    
    def __init__(self, engine, id, pos = MyVector(0, 0 ,0), vel = MyVector(0, 0, 0), yaw = 0, team = 0):
        self.team = team
        Entity.__init__(self, engine, id, pos = pos, vel = vel, yaw = yaw)
        print "player init"
        self.mesh = 'ninja.mesh'
        self.uiname = 'BVB' + str(BVB.id)
        BVB.id += 1
        self.acceleration = 360
        self.turningRate = 120
        self.maxSpeed = 400
        self.desiredSpeed = 0
        self.desiredHeading = 0
        self.speed = 0
        self.heading = 0
        self.wakeSize = 'Large'
        self.offset = ogre.Degree(-90)
        self.hasAnimation = True
        self.scale = ogre.Vector3(.5, .5, .5)
        self.material = "Examples/YellowTeam"
        self.color = "RedCircle"
        self.circle = None
        self.team = team        
        
        
        self.radiiNorm = 115.0
        self.radiiSlide = 200.0


class TopStad(Entity):
    id = 0
    def __init__(self, engine, id, pos = MyVector(0, 0 ,0), vel = MyVector(0, 0, 0), yaw = 0, team = 0):
        Entity.__init__(self, engine, id, pos = pos, vel = vel, yaw = yaw)
        print "player init"
        self.mesh = 'WireFrameTopStad.mesh'
        self.uiname = 'Top' + str(TopStad.id)
        TopStad.id += 1
        self.acceleration = 0
        self.turningRate = 0
        self.maxSpeed = 0
        self.desiredSpeed = 0
        self.desiredHeading = 0
        self.speed = 0
        self.heading = 0
        self.wakeSize = 'Large'
        self.offset = ogre.Degree(90)
        
        #self.scale = ogre.Vector3(1, 1, 1)

        self.scale = ogre.Vector3(50, 50, 50)


class Stands(Entity):
    id = 0
    def __init__(self, engine, id, pos = MyVector(0, 0 ,0), vel = MyVector(0, 0, 0), yaw = 0, team = 0):
        Entity.__init__(self, engine, id, pos = pos, vel = vel, yaw = yaw)
        print "player init"
        self.mesh = "Stands.mesh" 
        self.uiname = 'Stands' + str(Stands.id)
        Stands.id += 1
        self.acceleration = 0
        self.turningRate = 0
        self.maxSpeed = 0
        self.desiredSpeed = 0
        self.desiredHeading = 0
        self.speed = 0
        self.heading = 0
        self.wakeSize = 'Large'
        self.offset = ogre.Degree(90)
        
        #self.scale = ogre.Vector3(1, 1, 1)

        self.scale = ogre.Vector3(50, 50, 50)

class Entrance(Entity):
    id = 0
    def __init__(self, engine, id, pos = MyVector(0, 0 ,0), vel = MyVector(0, 0, 0), yaw = 0, team = 0):
        Entity.__init__(self, engine, id, pos = pos, vel = vel, yaw = yaw)
        print "player init"
        self.mesh = "entrance.mesh" 
        self.uiname = 'entrance' + str(Entrance.id)
        Entrance.id += 1
        self.acceleration = 0
        self.turningRate = 0
        self.maxSpeed = 0
        self.desiredSpeed = 0
        self.desiredHeading = 0
        self.speed = 0
        self.heading = 0
        self.wakeSize = 'Large'
        self.offset = ogre.Degree(90)
        
        #self.scale = ogre.Vector3(1, 1, 1)

        self.scale = ogre.Vector3(50, 50, 50)

class highWall(Entity):
    id = 0
    def __init__(self, engine, id, pos = MyVector(0, 0 ,0), vel = MyVector(0, 0, 0), yaw = 0, team = 0):
        Entity.__init__(self, engine, id, pos = pos, vel = vel, yaw = yaw)
        print "player init"
        self.mesh = "highWall.mesh"
        self.uiname = 'highWall' + str(highWall.id)
        highWall.id += 1
        self.acceleration = 0
        self.turningRate = 0
        self.maxSpeed = 0
        self.desiredSpeed = 0
        self.desiredHeading = 0
        self.speed = 0
        self.heading = 0
        self.wakeSize = 'Large'
        self.offset = ogre.Degree(90)
        
        #self.scale = ogre.Vector3(1, 1, 1)

        self.scale = ogre.Vector3(50, 50, 50)

class lowWall(Entity):
    id = 0
    def __init__(self, engine, id, pos = MyVector(0, 0 ,0), vel = MyVector(0, 0, 0), yaw = 0, team = 0):
        Entity.__init__(self, engine, id, pos = pos, vel = vel, yaw = yaw)
        print "player init"
        self.mesh = "lowWall.mesh"
        self.uiname = 'lowWall'  + str(lowWall.id)
        lowWall.id +=1
        self.acceleration = 0
        self.turningRate = 0
        self.maxSpeed = 0
        self.desiredSpeed = 0
        self.desiredHeading = 0
        self.speed = 0
        self.heading = 0
        self.wakeSize = 'Large'
        self.offset = ogre.Degree(90)
        
        #self.scale = ogre.Vector3(1, 1, 1)

        self.scale = ogre.Vector3(50, 50, 50)

class midWall(Entity):
    id = 0
    def __init__(self, engine, id, pos = MyVector(0, 0 ,0), vel = MyVector(0, 0, 0), yaw = 0, team = 0):
        Entity.__init__(self, engine, id, pos = pos, vel = vel, yaw = yaw)
        print "player init"
        self.mesh = "midWall.mesh"
        self.uiname = 'midWall' + str(midWall.id)
        midWall.id += 1
        self.acceleration = 0
        self.turningRate = 0
        self.maxSpeed = 0
        self.desiredSpeed = 0
        self.desiredHeading = 0
        self.speed = 0
        self.heading = 0
        self.wakeSize = 'Large'
        self.offset = ogre.Degree(90)
        
        #self.scale = ogre.Vector3(1, 1, 1)

        self.scale = ogre.Vector3(50, 50, 50)


class postL(Entity):
    id = 0
    def __init__(self, engine, id, pos = MyVector(0, 0 ,0), vel = MyVector(0, 0, 0), yaw = 0, team = 0):
        Entity.__init__(self, engine, id, pos = MyVector(-3300, 100, 0), vel = vel, yaw = yaw)
        print "player init"
        self.mesh = "goals.mesh"
        self.uiname = 'postL' + str (postL.id)
        postL.id += 1
        self.acceleration = 0
        self.turningRate = 0
        self.maxSpeed = 0
        self.desiredSpeed = 0
        self.desiredHeading = 0
        self.speed = 0
        self.heading = 0
        self.wakeSize = 'Large'
        self.offset = ogre.Degree(0)
        
        #self.scale = ogre.Vector3(1, 1, 1)

        self.scale = ogre.Vector3(50, 50, 50)


class RoofFrame(Entity):
    id = 0
    def __init__(self, engine, id, pos = MyVector(0, 0 ,0), vel = MyVector(0, 0, 0), yaw = 0, team = 0):
        Entity.__init__(self, engine, id, pos = pos, vel = vel, yaw = yaw)
        print "player init"
        self.mesh = "RoofFrame.mesh"
        self.uiname = 'RoofFrame' + str(RoofFrame.id)
        RoofFrame.id += 1
        self.acceleration = 0
        self.turningRate = 0
        self.maxSpeed = 0
        self.desiredSpeed = 0
        self.desiredHeading = 0
        self.speed = 0
        self.heading = 0
        self.wakeSize = 'Large'
        self.offset = ogre.Degree(90)
        
        #self.scale = ogre.Vector3(1, 1, 1)

        self.scale = ogre.Vector3(50, 50, 50)


class stairs(Entity):
    id = 0
    def __init__(self, engine, id, pos = MyVector(0, 0 ,0), vel = MyVector(0, 0, 0), yaw = 0, team = 0):
        Entity.__init__(self, engine, id, pos = pos, vel = vel, yaw = yaw)
        print "player init"
        self.mesh = "stairs.mesh"
        self.uiname = 'stairs' + str(stairs.id)
        stairs.id += 1
        self.acceleration = 0
        self.turningRate = 0
        self.maxSpeed = 0
        self.desiredSpeed = 0
        self.desiredHeading = 0
        self.speed = 0
        self.heading = 0
        self.wakeSize = 'Large'
        self.offset = ogre.Degree(90)
        
        #self.scale = ogre.Vector3(1, 1, 1)

        self.scale = ogre.Vector3(50, 50, 50)


class postR(Entity):
    id = 0
    def __init__(self, engine, id, pos = MyVector(0, 0 ,0), vel = MyVector(0, 0, 0), yaw = 0, team = 0):
        Entity.__init__(self, engine, id, pos = MyVector(3200, 100, 0), vel = vel, yaw = yaw)
        print "player init"
        self.mesh = "goals.mesh"
        self.uiname = 'postR' + str (postR.id)
        postR.id += 1
        self.acceleration = 0
        self.turningRate = 0
        self.maxSpeed = 0
        self.desiredSpeed = 0
        self.desiredHeading = 0
        self.speed = 0
        self.heading = 0
        self.wakeSize = 'Large'
        self.offset = ogre.Degree(180)
        
        #self.scale = ogre.Vector3(1, 1, 1)

        self.scale = ogre.Vector3(50, 50, 50)

