# Entity class to hold information about entities for 38Engine
# Daniel Sanchez

import ogre.renderer.OGRE as ogre
from physics import Physics
from renderer import Renderer
from vector import MyVector
# import math
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
        self.aspectTypes = [Physics, Renderer]
        self.aspects = []
        self.scale = ogre.Vector3(1, 1, 1)
        self.wakeSize = 'Small'
        
        #Make jet ski face the same way
        self.offset = 0

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

class Ddg51(Entity):
    def __init__(self, engine, id, pos = MyVector(0,0,0), vel = MyVector(0,0,0), yaw = 0):
        Entity.__init__(self, engine, id, pos = pos, vel = vel, yaw = yaw) 
        #print "ddg51 init"
        self.mesh = 'ddg51.mesh'
        self.uiname = 'DDG51'
        self.acceleration = 7
        self.turningRate = 15
        self.maxSpeed = 150
        self.desiredSpeed = 0
        self.desiredHeading = 0
        self.speed = 0
        self.heading = 0    
        self.wakeSize = 'Large'



class Cvn(Entity):
    def __init__(self, engine, id, pos = MyVector(0,0,0), vel = MyVector(0, 0, 0), yaw = 0):
        Entity.__init__(self, engine, id, pos = pos, vel = vel, yaw = yaw)
        self.mesh = 'cvn68.mesh'
        self.uiname = 'CVN68'
        self.acceleration = 5
        self.turningRate  = 5
        self.maxSpeed = 250
        self.desiredSpeed = 0
        self.desiredHeading = 0
        self.speed = 0
        self.heading = 0    
        self.wakeSize = 'Large'

class Sleek(Entity):
    def __init__(self, engine, id, pos = MyVector(0,0,0), vel = MyVector(0, 0, 0), yaw = 0):
        Entity.__init__(self, engine, id, pos = pos, vel = vel, yaw = yaw)        
        print "sleek init"
        self.mesh = 'sleek.mesh'
        self.uiname = 'SLEEK'
        self.acceleration = 12
        self.turningRate = 12
        self.maxSpeed = 120
        self.desiredSpeed = 0
        self.desiredHeading = 0
        self.speed = 0
        self.heading = 0    
        self.wakeSize = 'Large'

class Monterey(Entity):
    def __init__(self, engine, id, pos = MyVector(0,0,0), vel = MyVector(0, 0, 0), yaw = 0):
        Entity.__init__(self, engine, id, pos = pos, vel = vel, yaw = yaw)
        print "MONTEREY INIT"
        self.mesh = '3699_Monterey_189_92.mesh'
        self.uiname = 'MONTEREY'
        self.acceleration = 7
        self.turningRate = 35
        self.maxSpeed = 60
        self.desiredSpeed = 0
        self.desiredHeading = 0
        self.speed = 0
        self.heading = 0
        self.scale = ogre.Vector3(2, 2, 2)
        self.offset = ogre.Degree(90)
   
            
        self.wakeSize = 'Medium'

class Watercr(Entity):
    def __init__(self, engine, id, pos = MyVector(0,0,0), vel = MyVector(0, 0, 0), yaw = 0):
        Entity.__init__(self, engine, id, pos = pos, vel = vel, yaw = yaw)
        print "Watercr init"
        self.mesh = '4685_Personal_Watercr.mesh'
        self.uiname = 'JETSKI'
        self.acceleration = 10
        self.turningRate = 35
        self.maxSpeed = 40
        self.desiredSpeed = 0
        self.desiredHeading = 0
        self.speed = 0
        self.heading = 0
        self.offset = ogre.Degree(90)
        self.scale = ogre.Vector3(.5, .5, .5)    
        
            
        self.wakeSize = 'Medium'

class Boat5086(Entity):
    def __init__(self, engine, id, pos = MyVector(0,0,0), vel = MyVector(0, 0, 0), yaw = 0):
        Entity.__init__(self, engine, id, pos = pos, vel = vel, yaw = yaw)
        print "Boat5086 init"
        self.mesh = '5086_Boat.mesh'
        self.uiname = 'BOAT2'
        self.acceleration = 10
        self.turningRate = 30
        self.maxSpeed = 50
        self.desiredSpeed = 0
        self.desiredHeading = 0
        self.speed = 0
        self.heading = 0
        self.scale = ogre.Vector3(2, 2, 2)
    
class Alienship(Entity):
    def __init__(self, engine, id, pos = MyVector(0,0,0), vel = MyVector(0, 0, 0), yaw = 0):
        Entity.__init__(self, engine, id, pos = pos, vel = vel, yaw = yaw)
        print "alienship init"
        self.mesh = 'alienship.mesh'
        self.uiname = 'ALIEN'
        self.acceleration = 150
        self.turningRate = 25
        self.maxSpeed = 700
        self.desiredSpeed = 0
        self.desiredHeading = 0
        self.speed = 0
        self.heading = 0
        self.scale = ogre.Vector3(15, 15, 15)
        
            
        self.wakeSize = 'Large'

class Cigarette(Entity):
    def __init__(self, engine, id, pos = MyVector(0,0,0), vel = MyVector(0, 0, 0), yaw = 0):
        Entity.__init__(self, engine, id, pos = pos, vel = vel, yaw = yaw)
        print "cigarette init"
        self.mesh = 'cigarette.mesh'
        self.uiname = 'CIGARETTE'
        self.acceleration = 30
        self.turningRate = 45
        self.maxSpeed = 150
        self.desiredSpeed = 0
        self.desiredHeading = 0
        self.speed = 0
        self.heading = 0
        
            
        self.wakeSize = 'Medium'

class Boat(Entity):
    def __init__(self, engine, id, pos = MyVector(0,0,0), vel = MyVector(0, 0, 0), yaw = 0):
        Entity.__init__(self, engine, id, pos = pos, vel = vel, yaw = yaw)
        print "boat init"
        self.mesh = 'boat.mesh'
        self.uiname = 'BOAT'
        self.acceleration = 10
        self.turningRate = 10
        self.maxSpeed = 30
        self.desiredSpeed = 0
        self.desiredHeading = 0
        self.speed = 0
        self.heading = 0
        
        self.wakeSize = 'Medium'

class Sailboat(Entity):
    def __init__(self, engine, id, pos = MyVector(0, 0 ,0), vel = MyVector(0, 0, 0), yaw = 0):
        Entity.__init__(self, engine, id, pos = pos, vel = vel, yaw = yaw)
        print "sailboat init"
        self.mesh = 'sailboat.mesh'
        self.uiname = 'SAILBOAT'
        self.acceleration = 2
        self.turningRate = 25
        self.maxSpeed = 36
        self.desiredSpeed = 0
        self.desiredHeading = 0
        self.speed = 0
        self.heading = 0

