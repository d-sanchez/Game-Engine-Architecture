# Simple Physics for 38Engine
# vel is rate of change of pos

import math

class Physics:
    def __init__(self, ent, node=None):
        self.ent = ent

    def tick(self, dtime):
        # print "Physics tick", str(self.ent.id)

        errorRange = 0.4
        self.dt = dtime

        self.checkRange = abs(self.ent.desiredSpeed - self.ent.speed)
 
        if self.checkRange < errorRange:
            self.ent.speed = self.ent.desiredSpeed

        if self.ent.speed < self.ent.desiredSpeed:
            self.ent.speed += self.ent.acceleration * self.dt

        if self.ent.speed > self.ent.desiredSpeed:
            self.ent.speed -= self.ent.acceleration * self.dt

#-------------------------------------------------------------------

        self.checkRange = abs(self.ent.desiredHeading - self.ent.heading)

        if self.checkRange < errorRange: 
            self.ent.heading = self.ent.desiredHeading

        if self.ent.heading < self.ent.desiredHeading:
            self.ent.heading += self.ent.turningRate * self.dt
        
        if self.ent.heading > self.ent.desiredHeading:
            self.ent.heading -= self.ent.turningRate * self.dt 

        self.ent.vel.x = ((math.cos(math.radians(self.ent.heading))) * self.ent.speed)
        self.ent.vel.z = ((math.sin(math.radians(self.ent.heading))) * self.ent.speed) *-1

#-------------------------------------------------------------------

        self.ent.pos = self.ent.pos + (self.ent.vel * self.dt)