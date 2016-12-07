# Entity class to hold information about entities for 38Engine
# Daniel Sanchez

import ogre.renderer.OGRE as ogre
from physics import Physics
import math

class Renderable:
    def __init__(self, ent, node):
        self.node = node
        self.ent = ent

    def tick(self, dtime):
        self.node.position = self.ent.pos
        
        errorRange = 0.05
        x = abs(self.ent.desiredHeading - self.ent.heading)

        if x < errorRange:
            self.node.yaw(ogre.Degree(0))

        if x > errorRange:
            amountTurned = self.ent.turningRate * dtime

            if self.ent.heading < self.ent.desiredHeading:
                self.node.yaw(ogre.Degree(amountTurned))
            elif self.ent.heading > self.ent.desiredHeading:
                self.node.yaw(ogre.Degree(-amountTurned))
                
class Entity:
    def __init__(self, id, pos = ogre.Vector3(0,0,0), sceneNode = None,
                           mesh = '4685_Personal_Watercr.mesh',
                           acceleration = 10, turningRate = 10 ):

        self.id = id or "Sushil"+str(time.time())
        self.vel = ogre.Vector3(0, 0, 0)
        self.aspectTypes = [Physics, Renderable, ]
        self.aspects = []
        
        self.yaw = 0.0
        self.speed = 0
        self.heading = 0
        self.desiredSpeed = 0
        self.desiredHeading = 0
        
        self.pos = pos
        self.mesh = mesh
        self.sceneNode  = sceneNode
        self.acceleration = acceleration
        self.turningRate = turningRate

    def attachAspects(self, sceneNode):
        for aspType in self.aspectTypes:
            self.aspects.append(aspType(self,sceneNode))

    def tick(self, dtime):
        for aspect in self.aspects:
            aspect.tick(dtime)


    def __str__(self):
        x = "Entity: %s \nPos: %s, Vel: %s, yaw: %f" % (self.id, str(self.pos), str(self.vel), self.yaw)
        return x

class Missile(Entity):

    def __init__(self, id, pos):
        print "missile init"
        self.mesh = 'missile.mesh'
        self.id = id
        self.pos = pos
        self.acceleration = 14
        self.turningRate = 12
        Entity.__init__(self, id = self.id, pos = self.pos, mesh = self.mesh, 
            acceleration = self.acceleration, turningRate = self.turningRate)

    
class Cvn(Entity):

    def __init__(self, id, pos):
        print "cvn init"
        self.mesh = 'cvn68.mesh'
        self.id = id
        self.pos = pos
        self.acceleration = 6
        self.turningRate = 1
        Entity.__init__(self, id = self.id, pos = self.pos, mesh = self.mesh, 
            acceleration = self.acceleration, turningRate = self.turningRate)


class Sleek(Entity):

    def __init__(self, id, pos):
        print "sleek init"
        self.mesh =  'sleek.mesh'
        self.id = id
        self.pos = pos
        self.acceleration = 8
        self.turningRate = 6
        Entity.__init__(self, id = self.id, pos = self.pos, mesh = self.mesh, 
            acceleration = self.acceleration, turningRate = self.turningRate)


class Ddg51(Entity):

    def __init__(self, id, pos):
        print "ddg51 init"
        self.mesh = 'ddg51.mesh'
        self.id = id
        self.pos = pos
        self.acceleration = 10
        self.turningRate = 6
        Entity.__init__(self, id = self.id, pos = self.pos, mesh = self.mesh, 
            acceleration = self.acceleration, turningRate = self.turningRate)


class Monterey(Entity):

    def __init__(self, id, pos):
        print "MONTEREY INIT"
        self.mesh = '3699_Monterey_189_92.mesh'
        self.id = id
        self.pos = pos
        self.acceleration = 13
        self.turningRate = 12
        Entity.__init__(self, id = self.id, pos = self.pos, mesh = self.mesh, 
            acceleration = self.acceleration, turningRate = self.turningRate)


class Watercr(Entity):

    def __init__(self, id, pos):
        print "Watercr init"
        self.mesh = '4685_Personal_Watercr.mesh'
        self.id = id
        self.pos = pos
        self.acceleration = 10
        self.turningRate = 10
        Entity.__init__(self, id = self.id, pos = self.pos, mesh = self.mesh, 
            acceleration = self.acceleration, turningRate = self.turningRate)


class Boat5086(Entity):

    def __init__(self, id, pos):
        print "Boat5086 init"
        self.mesh = '5086_Boat.mesh'
        self.id = id
        self.pos = pos
        self.acceleration = 10
        self.turningRate = 10
        Entity.__init__(self, id = self.id, pos = self.pos, mesh = self.mesh, 
            acceleration = self.acceleration, turningRate = self.turningRate)


class Alienship(Entity):

    def __init__(self, id, pos):
        print "alienship init"
        self.mesh = 'alienship.mesh' 
        self.id = id
        self.pos = pos
        self.acceleration = 10
        self.turningRate = 10
        Entity.__init__(self, id = self.id, pos = self.pos, mesh = self.mesh, 
            acceleration = self.acceleration, turningRate = self.turningRate)

class Cigarette(Entity):

    def __init__(self, id, pos):
        print "cigarette init"
        self.mesh = 'cigarette.mesh'
        self.id = id
        self.pos = pos
        self.acceleration = 20
        self.turningRate = 12
        Entity.__init__(self, id = self.id, pos = self.pos, mesh = self.mesh, 
            acceleration = self.acceleration, turningRate = self.turningRate)

class Boat(Entity):

    def __init__(self, id, pos):
        print "boat init"
        self.mesh = 'boat.mesh'
        self.id = id
        self.pos = pos
        self.acceleration = 10
        self.turningRate = 10
        Entity.__init__(self, id = self.id, pos = self.pos, mesh = self.mesh, 
            acceleration = self.acceleration, turningRate = self.turningRate)

class Sailboat(Entity):

    def __init__(self, id, pos):
        print "sailboat init"
        self.mesh = 'sailboat.mesh' 
        self.id = id
        self.pos = pos
        self.acceleration = 10
        self.turningRate = 10
        Entity.__init__(self, id = self.id, pos = self.pos, mesh = self.mesh, 
            acceleration = self.acceleration, turningRate = self.turningRate)