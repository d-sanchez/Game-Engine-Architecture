# Action.py

import ogre.renderer.OGRE as ogre
import math
import utils
import random as rand
class Action:
    def __init__(self, ent, targetLoc = ogre.Vector3( 0.0, 0.0, 0.0 )):
        self.ent = ent
        self.targetLoc = targetLoc
        self.maxSpeed = self.ent.maxSpeed
        self.entityMgr = self.ent.engine.entityMgr
        
    def tick(self, dt):
        pass

class GoHome(Action):
    def __init__(self, ent, targetLoc):

        Action.__init__(self, ent, targetLoc)
        pass

    def tick(self, dt):
        self.ent.pos.x = self.ent.home.x
        self.ent.pos.y = self.ent.home.y

        if self.ent.aspects[2].ActionList:
            self.ent.aspects[2].ActionList.pop(0)

class TrackBall(Action):
    def __init__(self, ent, targetEnt):

        Action.__init__(self, ent)
        self.targetEnt = targetEnt
        pass

    def tick(self, dt):
        self.ent.pos.z = self.targetEnt.pos.z + rand.randint(-25, 25)
        #print "here"

        if self.ent.aspects[2].ActionList:
            self.ent.aspects[2].ActionList.pop(0)


    
class Move( Action ):
    def __init__(self, ent, targetLoc):
        Action.__init__(self, ent, targetLoc)

    def tick(self, dt):
        if not self.targetLoc:
            return 
        diffZ = self.targetLoc.z - self.ent.pos.z
        diffX = self.targetLoc.x - self.ent.pos.x
        print "z", diffZ
        print "x", diffX


        self.distance = math.sqrt(diffZ**2 + diffX**2)
        if self.distance > 5:
            self.ent.desiredHeading = -math.atan2(diffZ, diffX)
            self.ent.desiredSpeed = self.maxSpeed
        else:
            self.ent.desiredSpeed = 0
            self.ent.speed = 0

            if self.ent.aspects[2].ActionList:
                    self.ent.aspects[2].ActionList.pop(0)
            
class Follow( Action ):
    def __init__(self, ent, targetEnt):
        Action.__init__(self, ent)
        self.targetEnt = targetEnt

    def tick(self, dt):
        if (not self.targetEnt):
            return
        self.targetLoc = self.targetEnt.pos
        
        diffZ = float(self.targetLoc.z - self.ent.pos.z)
        diffX = float(self.targetLoc.x - self.ent.pos.x)
        self.distance = math.sqrt(diffZ**2 + diffX**2)
        
        if self.distance > 25:
            self.ent.desiredHeading = -(math.atan2(diffZ, diffX) * 180.0/3.14) 

            if (self.ent.desiredHeading < 0 ):
                self.ent.desiredHeading += 360
                dAngle = math.fabs(self.ent.desiredHeading - self.ent.heading)
                if dAngle > 180:
                    self.ent.desiredHeading -= 360


            self.ent.desiredSpeed = self.maxSpeed
        else:
            self.ent.desiredHeading = -(math.atan2(diffZ, diffX) * 180.0/3.14)
            
            
            if (self.ent.desiredHeading < 0 ):
                self.ent.desiredHeading += 360
                dAngle = math.fabs(self.ent.desiredHeading - self.ent.heading)
                if dAngle > 180:
                    self.ent.desiredHeading -= 360

            #elif (self.ent.desiredHeading > 360):
             #   self.ent.desiredHeading -=360 
            self.ent.desiredSpeed = 0
            self.ent.speed = 0
        #print(self.ent.desiredHeading)
    
class Intercept( Action ):
    def __init__(self, ent, targetEnt):
        Action.__init__(self, ent)
        self.targetEnt = targetEnt

    def tick(self, dt):
        if (not self.targetEnt):
            
            return
        #print self.targetEnt.uiname
        self.targetLoc = self.targetEnt.pos
        
        #relativeSpeed = (ogre.Math.Abs(ogre.Vector3.length(self.targetEnt.vel - self.ent.vel))).valueRadians()
        
        #self.distance = (ogre.Math.Abs(ogre.Vector3.length( self.targetEnt.pos - self.ent.pos ))).valueRadians()

        relativeSpeedX = self.targetEnt.vel.x - self.ent.vel.x
        relativeSpeedZ = self.targetEnt.vel.z - self.ent.vel.z
        
        self.distX = self.targetLoc.x - self.ent.pos.x
        self.distZ = self.targetLoc.z - self.ent.pos.z

        self.distance = math.sqrt(self.distX**2 + self.distZ**2)
        relativeSpeed = math.sqrt(relativeSpeedX**2 + relativeSpeedZ**2)
        
        #print "relativeSpeed", relativeSpeed
        if relativeSpeed != 0:
            travelTime = (self.distance / relativeSpeed)
            
            self.predictiveLoc = self.targetLoc + (self.targetEnt.vel * travelTime)
            
            diffZ = self.predictiveLoc.z - self.ent.pos.z
            diffX = self.predictiveLoc.x - self.ent.pos.x
            
            print self.targetLoc, self.predictiveLoc
            
            if self.distance > 10:
                self.ent.desiredHeading = -math.atan2(diffZ, diffX) * 180 / 3.14 
                self.ent.desiredSpeed = self.maxSpeed
            else:
                self.ent.desiredHeading = -math.atan2(diffZ, diffX) * 180 / 3.14
                self.ent.desiredSpeed = 0

                if self.ent.aspects[2].ActionList:
                    self.ent.aspects[2].ActionList.pop(0)
