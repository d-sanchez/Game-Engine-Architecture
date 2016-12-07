from vector import MyVector
import time
import AIaction as action

import ogre.renderer.OGRE as ogre


class GameMgr:
    def __init__(self, engine):
        self.engine = engine
        self.guiMgr = self.engine.guiMgr
        self.sfxMgr = self.engine.soundMgr
        self.half = 1
        self.scoreOne = 0
        self.scoreTwo = 0
        self.startCheck = False
        self.instructionsCheck = False
        self.creditsCheck = False
        self.backCheck = False
        self.teamCheck = False
        self.scored = False
        self.celebrating = False

        self.gameTime = 0
        self.start = time.time()
       
        self.teamList = self.engine.entityMgr.entTypes
        self.chantList = self.engine.soundMgr.musicList
        self.p1Team = 0
        self.p2Team = 0
        
        self.teamSize = 5
        self.reset = False
        self.loadGameAsset()

        print "starting Game mgr"
        pass

    def init(self):
        self.guiMgr.createMainMenu()
        self.guiMgr.createHud()
        self.sfxMgr.playMusic("Champions_League_theme")
        #self.sfxMgr.playMusic("bvb")
        #self.sfxMgr.playMusic("liverpool")
        #self.sfxMgr.playMusic("arsenal")

    def loadGameAsset(self):
        
        self.loadTeam1()
        self.loadTeam2()
        self.loadBall()
        self.loadStad()
       
        
    def loadBall(self):
        self.engine.entityMgr.createEnt(self.engine.entityMgr.ballEnt, pos = MyVector(0, 0, 0))  

    def loadTeam1(self):
        x = 600
        ent = self.engine.entityMgr.createEnt(self.teamList[self.p1Team], pos = ogre.Vector3(x, 0, 0), team = 1)
        self.engine.entityMgr.selectedEntP1 = ent
        #ent.node.showBoundingBox(True)
        ent.circle.show()
        x += 600
        ent = self.engine.entityMgr.createEnt(self.teamList[self.p1Team], pos = ogre.Vector3(x, 0, 600), team = 1)
        
        ent = self.engine.entityMgr.createEnt(self.teamList[self.p1Team], pos = ogre.Vector3(x, 0, -600), team = 1)
        x += 600
        ent = self.engine.entityMgr.createEnt(self.teamList[self.p1Team], pos = ogre.Vector3(x, 0, 0), team = 1)
        x += 600
        ent = self.engine.entityMgr.createEnt(self.teamList[self.p1Team], pos = ogre.Vector3(x, 0, 0), team = 1)

        self.engine.entityMgr.GKP1 = ent
        
        for en in self.engine.entityMgr.team1.values():
            en.desiredHeading = 180
            en.heading = 180
        
        
    def loadTeam2(self):
        x = -600
        ent = self.engine.entityMgr.createEnt(self.teamList[self.p2Team], pos = ogre.Vector3(x, 0, 0), team = 2)
        self.engine.entityMgr.selectedEntP2 = ent
        #ent.node.showBoundingBox(True)
        ent.circle.show()
       
        x -= 600
        ent = self.engine.entityMgr.createEnt(self.teamList[self.p2Team], pos = ogre.Vector3(x, 0, 600), team = 2)
        
        ent = self.engine.entityMgr.createEnt(self.teamList[self.p2Team], pos = ogre.Vector3(x, 0, -600), team = 2)
        x -= 600
        ent = self.engine.entityMgr.createEnt(self.teamList[self.p2Team], pos = ogre.Vector3(x, 0, 0), team = 2)
        x -= 600
        ent = self.engine.entityMgr.createEnt(self.teamList[self.p2Team], pos = ogre.Vector3(x, 0, 0), team = 2)
       

        self.engine.entityMgr.GKP2 = ent        

    def loadStad(self):
        self.engine.entityMgr.createStad()

    def tick(self, dt):
        if (not self.engine.paused):
            self.updateTime() 
            if (self.startCheck):
                self.startCheck = False
                self.startGame()
            #print self.teamList[self.p1Team] , self.teamList[self.p2Team]
       
            if (self.reset):
                self.resetPlayers()
       
            if (self.gameTime >= 5400):
                self.gameOver()
        
        if (self.scored):
            self.celebration()
        
        #print self.engine.soundMgr.soundBusy()

        pass

    def stop(self):
        pass

    def updateTimeDown(self):
        self.end = time.time()
        #print self.backCheck
        if (self.end - self.start) > 1 :
            #print (self.end - self.start) 
            self.start = self.end
            self.gameTime-=1
            #print self.gameTime

    def updateTime(self):
        self.end = time.time()
        #print self.backCheck
        if (self.end - self.start) > 1 :
            #print (self.end - self.start) 
            self.start = self.end
            self.gameTime += 9
            #print self.gameTime

    

    def startGame(self):
        self.sfxMgr.stopMusic("Champions_League_theme")

        if (self.engine.aiMgr.simpleAI):
             self.sfxMgr.playMusic("Benny_Hill")
             self.sfxMgr.setVolume(100)
        else:
            self.sfxMgr.playMusic(self.chantList[self.p1Team])

        #self.sfxMgr.setVolume(5)
        self.gameTime = 0
        self.loadTeamColors()
        self.start = time.time()
        self.engine.guiMgr.overlay.hide()
        self.engine.guiMgr.hud2.show()
        self.resetPlayers()

    def loadTeamColors(self):
        for ent in self.engine.entityMgr.team1.values():
            ent.material = self.teamList[self.p1Team].defaultMat

        for ent in self.engine.entityMgr.team2.values():
            ent.material = self.teamList[self.p2Team].defaultMat

        pass
    
    def gameOver(self):
        #These flags don't work in game
        #self.backCheck = True
        #self.startCheck = False

        #declare winner 

        if ( self.scoreOne > self.scoreTwo):
                self.engine.guiMgr.playerOneWin.show()
        elif ( self.scoreTwo > self.scoreOne ):
                self.engine.guiMgr.playerTwoWin.show()
        else:
                self.engine.guiMgr.tieGame.show()

        #pause game 

        #show pause menu

        #go to main menu if exit game
        if (self.gameTime >= 5415):
            self.engine.guiMgr.playerTwoWin.hide()
            self.engine.guiMgr.playerOneWin.hide()
            self.engine.guiMgr.tieGame.hide()
            
            self.engine.soundMgr.stopMusic("Benny_Hill")
            self.startCheck = False
            self.mainMenu()
            

        #restart if restart
        #self.startCheck = True
        pass

    def pauseMenu(self):
        #put code to show pause menu here
        #paused binded to keyboard N for now
        pass

    def celebration(self):
        
        if (self.scored and not self.celebrating):
            self.engine.soundMgr.stopMusic(self.chantList[self.p1Team])
            self.engine.soundMgr.playACelebration()
            self.celebrating = True
        elif (self.scored and self.celebrating):
            if (not self.engine.soundMgr.musicBusy()):
                self.scored = False
                self.celebrating = False
                self.engine.paused = False
                self.engine.soundMgr.playMusic(self.chantList[self.p1Team])

    def mainMenu(self):
        self.engine.guiMgr.overlay.show()
        self.engine.guiMgr.hud2.hide()
        self.sfxMgr.playMusic("Champions_League_theme")
        self.sfxMgr.setVolume(100)
        pass
        ## Code to load sound here

    # this is for resetting player positions after a goal
    def resetPlayers(self):
        self.reset = False
        for ent in self.engine.entityMgr.entities.values():
                    ent.aspects[2].clear()
                    ent.speed = 0
                    ent.desiredSpeed = 0

        for ent in self.engine.entityMgr.team1.values():
            self.engine.entityMgr.addAction(ent, action.GoHome(ent, ent.home))

        

        for ent in self.engine.entityMgr.team2.values():
            self.engine.entityMgr.addAction(ent, action.GoHome(ent, ent.home))
        


    
