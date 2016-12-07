import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS
import random as rand
import pygame
import utils
import AIaction as action

class ControlMgr:

    def __init__(self, engine):
        #print "__init__ ControlMgr"
        self.engine = engine
        self.entityMgr = engine.entityMgr
        self.Keyboard = engine.inputMgr.keyboard
        self.sceneManager = engine.gfxMgr.sceneManager
        self.pressed = False 
        self.heldTime = 0
        self.timer = .1
        #for select
        self.toggle = 0.1
            
    def init(self):
        pygame.joystick.init()
        self.num_joysticks = pygame.joystick.get_count()
        self.debug = 0
        self.js = []
        self.p1UseJoystick = False
        self.p2UseJoystick = False
        self.teamball = 9999
        self.slideToggle = 0.0
        
        for i in range(self.num_joysticks):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            self.js.append(joystick)
        
        if self.num_joysticks == 1:
            self.p1UseJoystick = True
        
        elif self.num_joysticks == 2:
            self.p2UseJoystick = True
        #print "num joysticks ", self.num_joysticks

    def tick(self, dt):
        for event in pygame.event.get():
            pass

        for i in range(self.num_joysticks):
            print self.engine.entityMgr.getSelected(i+1)
            ent  = self.engine.entityMgr.getSelected(i+1)
            self.handleJoystickController(dt, ent, self.js[i])

        if (self.p2UseJoystick == False):
            self.handleKeyboardController(dt)


    def handleKeyboardController(self, dt):
        ent = self.entityMgr.selectedEntP2
        team2  = self.entityMgr.team2 

        if self.Keyboard.isKeyDown(OIS.KC_NUMPAD8) or self.Keyboard.isKeyDown(OIS.KC_I):
            for key, ent in team2 .iteritems():
                if (ent == self.entityMgr.selectedEntP2):
                    ent.desiredSpeed += 100 * dt
                else:
                    ent.desiredSpeed = 0
        
        if not self.Keyboard.isKeyDown(OIS.KC_NUMPAD8) and not self.Keyboard.isKeyDown(OIS.KC_I):
            ent = self.entityMgr.selectedEntP2
            
            if (ent != None):
                ent.desiredSpeed = 0.0


        if self.Keyboard.isKeyDown(OIS.KC_NUMPAD4) or self.Keyboard.isKeyDown(OIS.KC_J):
            ent = self.entityMgr.selectedEntP2
            
            ent.desiredHeading += 100 * dt
                
            # Ensure we work with angles 0 to 360
            if ent.desiredHeading > 360:
            # Heading is also decrease by 360 for simpler physics logic 
                ent.desiredHeading -= 360  
                ent.heading -= 360      
            
        if self.Keyboard.isKeyDown(OIS.KC_NUMPAD6) or self.Keyboard.isKeyDown(OIS.KC_L):
            ent = self.entityMgr.selectedEntP2
            ent.desiredHeading -= 100 * dt
                
            # Ensure we work with angles 0 to 360
            if ent.desiredHeading < 0:
                # Heading is also decrease by 360 for simpler physics logic 
                ent.desiredHeading += 360  
                ent.heading += 360 
                #  if ent.heading < 0:
                #     ent.heading += 360
        
        if self.Keyboard.isKeyDown(OIS.KC_SPACE):
            self.pressed = True
            #print "pressed"
            self.teamball = ent.team
            self.heldTime += 2.0 * dt
            if self.heldTime > 2.0:  
                self.heldTime = 2.0
            pass

        if self.Keyboard.isKeyDown(OIS.KC_M):
            ent = self.entityMgr.selectedEntP2
            self.slideToggle = .5
            if ent:
                ent.slide = True
                ent.desiredSpeed = 0
                    
        if self.Keyboard.isKeyDown(OIS.KC_N):
            if (self.timer < 0.0):
                self.engine.paused = not self.engine.paused
                self.timer = .5
            else:
                self.timer -= dt

        if not self.Keyboard.isKeyDown(OIS.KC_M):
            ent = self.entityMgr.selectedEntP2

            if ent:
                ent.slide = False 

            if (self.slideToggle < 0.0):
                self.slideToggle = 0.0
            else:
                self.slideToggle -= dt

        if (not self.Keyboard.isKeyDown(OIS.KC_SPACE) and self.pressed and ent.team == self.teamball):
            ent = self.entityMgr.ball
            if (ent.attachEnt != None):
                
                teammate = ent.attachEnt.nearestTeamate()
                distance = 1000000 # 
                
                if (teammate):
                    distance = utils.distance(ent.attachEnt, teammate)
                    #distance = 1000000
                
                #1/4 s short pass
                if (self.heldTime < .5 and distance < 1200.0):
                    #print "short pass"
                    self.engine.entityMgr.addAction(ent, action.Intercept(ent, teammate))
                    pass
                else:    
                    ent.heading = ent.attachEnt.heading
                    ent.desiredHeading = ent.heading + rand.uniform(-20*self.heldTime, 20*self.heldTime)
                    #print "Here2"
                    #1/2 s or longer and the ball will rise
                    if self.heldTime > 1.1:
                        ent.speed = ent.maxSpeed * self.heldTime
                    #print "Here3" 
                        ent.vel.y = 1000.0 * self.heldTime / 2.0
                    else:
                    #print "Here4"
                        ent.speed = ent.maxSpeed * 2.0 * self.heldTime

                    # team mate will try to interscept
                    #if (teammate):
                    #   self.engine.entityMgr.addAction(teammate, action.Intercept(teammate, ent))
                                
                #print ent.speed
                ent.desiredSpeed = 0
                self.heldTime = 0
                ent.attachEnt = None
                ent.toggle = .2
                self.teamball = 9999
            
                self.pressed = False

            else:
            #print "Here5"
                pass
       
    def handleJoystickController(self, dt, ent, js):
        buttons = js.get_numbuttons()
        axis = js.get_numaxes()

        if (js.get_axis(0) and js.get_axis(0) < 0 ):
            #print "left"
            ent.desiredHeading += 100 * dt
            if ent.desiredHeading > 360:
                ent.desiredHeading -= 360  
                ent.heading -= 360     

        if (js.get_axis(0) and js.get_axis(0) > 0 ):
            #print "right"
            ent.desiredHeading -= 100 * dt
            if ent.desiredHeading < 360:
                ent.desiredHeading += 360  
                ent.heading += 360     

        if (js.get_axis(1) and js.get_axis(1) < 0 ):
            #print "up"
            ent.desiredSpeed += 100 * dt
            ent.speed += ent.maxSpeed * dt

        else:
            if(ent != None):
                ent.desiredSpeed = 0

        if (js.get_button(1)):
            self.teamball = ent.team
            self.pressed = True
            self.heldTime += 2.0 * dt
            if self.heldTime > 2.0:  
                self.heldTime = 2.0
            #self.JS_Pressed_A = someJoyButton

        #button: b
        if (js.get_button(2)):
            self.slideToggle = .5
            if ent:
                ent.slide = True
                ent.desiredSpeed = 0
            pass

        if (not js.get_button(2)):
            if ent:
                ent.slide = False 

            if (self.slideToggle < 0.0):
                self.slideToggle = 0.0
            else:
                self.slideToggle -= dt

        #button: select
        if self.toggle >=0:
            self.toggle -= dt

        if self.toggle < 0 and js.get_button(8):
            self.toggle = 0.4
            self.engine.selectionMgr.selectNextEnt(ent.team)

        #button: start
        if (js.get_button(9)):
            if (self.timer < 0.0):
                self.engine.paused = not self.engine.paused
                self.timer = .5
            else:
                self.timer -= dt
                pass

        if ((not js.get_button(1)) and self.pressed and ent.team == self.teamball):
            ent = self.entityMgr.ball
            if (ent.attachEnt != None):
                
                teammate = ent.attachEnt.nearestTeamate()
                distance = 1000000 # 
                
                if (teammate):
                    distance = utils.distance(ent.attachEnt, teammate)
                    #distance = 1000000
                
                #1/4 s short pass
                if (self.heldTime < .5 and distance < 1200.0):
                    #print "short pass"
                    self.engine.entityMgr.addAction(ent, action.Intercept(ent, teammate))
                    pass
                else:    
                    ent.heading = ent.attachEnt.heading
                    ent.desiredHeading = ent.heading + rand.uniform(-20*self.heldTime, 20*self.heldTime)
                    #print "Here2"
                    #1/2 s or longer and the ball will rise
                    if self.heldTime > 1.1:
                        ent.speed = ent.maxSpeed * self.heldTime
                    #print "Here3" 
                        ent.vel.y = 1000.0 * self.heldTime / 2.0
                    else:
                    #print "Here4"
                        ent.speed = ent.maxSpeed * 2.0 * self.heldTime

                    # team mate will try to interscept
                    #if (teammate):
                    #   self.engine.entityMgr.addAction(teammate, action.Intercept(teammate, ent))
                                
                #print ent.speed
                ent.desiredSpeed = 0
                self.heldTime = 0
                ent.attachEnt = None
                ent.toggle = .2
                self.teamball = 9999
            
                self.pressed = False

            else:
            #print "Here5"
                pass

    def stop(self):
        pass
