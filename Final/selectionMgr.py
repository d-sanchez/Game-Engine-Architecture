import ogre.io.OIS as OIS
    
class SelectionMgr:

    def __init__(self, engine):
        self.engine = engine

    def init(self):
        self.keyboard = self.engine.inputMgr.keyboard
        self.toggle = 0.1
        self.onTeamScreen = False

        # buttonPositions
        self.buttonStartX = self.engine.guiMgr.buttonStartX
        self.buttonStartY = self.engine.guiMgr.buttonStartY
        self.buttonInstructY = self.engine.guiMgr.buttonInstructY
        self.buttonCreditsY = self.engine.guiMgr.buttonCreditsY
        self.buttonTeamSelectionY = self.engine.guiMgr.buttonTeamSelectionY
        
        #changed 
        self.windowWidth  = self.engine.gfxMgr.renderWindow.getWidth()
        self.windowHeight = self.engine.gfxMgr.renderWindow.getHeight()

    def tick(self, dt):
        if self.toggle >=0:
            self.toggle -= dt
        selectedEntIndex = self.engine.entityMgr.selectedEntIndex
        #print "selected: ", str(selectedEntIndex)


        if self.toggle < 0 and self.keyboard.isKeyDown(OIS.KC_TAB):
            self.toggle = 0.4
            #print "tab test"
            self.selectNextEnt(2)

            # ent = self.engine.entityMgr.selectedEnt
            # ent.node.showBoundingBox(False)
            # ent = self.engine.entityMgr.getNextEnt()
            # self.engine.entityMgr.selectedEntities = []            
            # ent.node.showBoundingBox(True)


    def selectNextEnt(self, team):
        if (team == 1):
            for key, ent in self.engine.entityMgr.team1.iteritems():
                #ent.node.showBoundingBox(False)
                ent.circle.hide()
        else:
            for key, ent in self.engine.entityMgr.team2.iteritems():
                #ent.node.showBoundingBox(False)
                ent.circle.hide()
        ent = self.engine.entityMgr.getPlayerClosestToBall(team)
        #ent.node.showBoundingBox(True)
        ent.circle.show()
        
    def stop(self):
        pass
    
    def checkPointAt(self, x, y):
        if (self.teamCheck(x, y)):
            self.engine.gameMgr.teamCheck = True
            self.onTeamScreen = True 
            print True

        elif (self.instructionCheck(x, y)):
            self.engine.gameMgr.instructionsCheck = True
            #change overlay
            print True

        elif (self.creditCheck(x, y)):
            self.engine.gameMgr.creditsCheck = True
            #change overlay
            print True
        
        elif (self.backCheck(x, y)):
            self.engine.gameMgr.backCheck = True
            self.onTeamScreen = False
        
        elif (self.p1LCheck(x, y) and self.onTeamScreen == True):
            cursor = self.engine.gameMgr.p1Team
            cursor -= 1

            if (cursor < 0):
   
            #change to number of teams
                cursor = 4

            self.engine.gameMgr.p1Team = cursor  
            print "Cursor - " + str (cursor)
            #scroll between available teams
           
            #Show Flag
            self.showFlag(cursor)
            print "1Left"

        elif (self.p2LCheck(x, y) and self.onTeamScreen == True ):
            cursor = self.engine.gameMgr.p2Team
            cursor -= 1

            #change to number of teams
            if (cursor < 0):
                cursor = 4

            self.engine.gameMgr.p2Team = cursor  
            print "Cursor - " + str (cursor)
            #Show Flag
            self.showFlagP2(cursor)
            
            print "2Left"
        
        elif (self.p1RCheck(x, y) and self.onTeamScreen == True ):
            cursor = self.engine.gameMgr.p1Team
            cursor += 1

            if (cursor > 4):
   
            #change to number of teams
                cursor = 0

            self.engine.gameMgr.p1Team = cursor  
            print "Cursor - " + str (cursor)
            #scroll between available teams

            #Show Flag
            self.showFlag(cursor)
            print "1Right"

        elif (self.p2RCheck(x, y) and self.onTeamScreen == True ):
            cursor = self.engine.gameMgr.p2Team
            cursor += 1

            #change to number of teams
            if (cursor > 4):
                cursor = 0

            self.engine.gameMgr.p2Team = cursor  
            print "Cursor - " + str (cursor)
            #Show Flag
            self.showFlagP2(cursor)
            print "2Right"
   
        elif (self.startCheck(x,y)):
            self.engine.gameMgr.startCheck = True

    def backCheck(self, x, y):
        return x > 0 and x < 100  and y >  self.windowHeight - 100 and y < self.windowHeight 

    def startCheck(self, x, y):
        return x > self.buttonStartX and x < self.buttonStartX+300  and \
               y > self.buttonStartY and y < self.buttonStartY+40 

    def instructionCheck(self, x, y):
        return x > self.buttonStartX and x < self.buttonStartX+300  and \
               y > self.buttonInstructY and y < self.buttonInstructY+40 

    def creditCheck(self, x, y):
        return x > self.buttonStartX and x < self.buttonStartX+300  and \
               y > self.buttonCreditsY and y < self.buttonCreditsY+40 

    def teamCheck(self, x, y):
        return x > self.buttonStartX and x < self.buttonStartX+300  and \
               y > self.buttonTeamSelectionY and y < self.buttonTeamSelectionY+40 
   
# Tweak this so that we have team selection working

    def p1LCheck(self, x, y):
        #print "p1LCheck"
        return x > 170 and x < 310  and y > 250 and y < 375

    def p1RCheck(self, x, y):
        #print "p1RCheck"
        return x > 1540 and x < 1700  and y > 250 and y < 375
 
    def p2LCheck(self, x, y):
        #print "p2LCheck"
        return x > 170 and x < 310  and y > 755 and y < 880

    def p2RCheck(self, x, y):
        #print "p2RCheck"
        return x > 1540 and x < 1700  and y > 755 and y < 880

    def showFlag (self, cursor): 
        if cursor == 0:
                self.engine.guiMgr.flagRed.hide()
                self.engine.guiMgr.flagBlue.hide()
                self.engine.guiMgr.flagGreen.hide()
                self.engine.guiMgr.flagPurple.hide()
                self.engine.guiMgr.flagYellow.show()

                self.engine.guiMgr.flagRedL.hide()
                self.engine.guiMgr.flagBlueL.hide()
                self.engine.guiMgr.flagGreenL.hide()
                self.engine.guiMgr.flagPurpleL.show()
                self.engine.guiMgr.flagYellowL.hide()

                self.engine.guiMgr.flagRedR.hide()
                self.engine.guiMgr.flagBlueR.show()
                self.engine.guiMgr.flagGreenR.hide()
                self.engine.guiMgr.flagPurpleR.hide()
                self.engine.guiMgr.flagYellowR.hide()
        elif cursor == 1:
                self.engine.guiMgr.flagRed.hide()
                self.engine.guiMgr.flagBlue.show()
                self.engine.guiMgr.flagGreen.hide()
                self.engine.guiMgr.flagPurple.hide()
                self.engine.guiMgr.flagYellow.hide()

                self.engine.guiMgr.flagRedL.hide()
                self.engine.guiMgr.flagBlueL.hide()
                self.engine.guiMgr.flagGreenL.hide()
                self.engine.guiMgr.flagPurpleL.hide()
                self.engine.guiMgr.flagYellowL.show()

                self.engine.guiMgr.flagRedR.show()
                self.engine.guiMgr.flagBlueR.hide()
                self.engine.guiMgr.flagGreenR.hide()
                self.engine.guiMgr.flagPurpleR.hide()
                self.engine.guiMgr.flagYellowR.hide()
        elif cursor == 2:

                self.engine.guiMgr.flagRed.show()
                self.engine.guiMgr.flagBlue.hide()
                self.engine.guiMgr.flagGreen.hide()
                self.engine.guiMgr.flagPurple.hide()
                self.engine.guiMgr.flagYellow.hide()

                self.engine.guiMgr.flagRedL.hide()
                self.engine.guiMgr.flagBlueL.show()
                self.engine.guiMgr.flagGreenL.hide()
                self.engine.guiMgr.flagPurpleL.hide()
                self.engine.guiMgr.flagYellowL.hide()

                self.engine.guiMgr.flagRedR.hide()
                self.engine.guiMgr.flagBlueR.hide()
                self.engine.guiMgr.flagGreenR.show()
                self.engine.guiMgr.flagPurpleR.hide()
                self.engine.guiMgr.flagYellowR.hide()

        elif cursor == 3:

                self.engine.guiMgr.flagRed.hide()
                self.engine.guiMgr.flagBlue.hide()
                self.engine.guiMgr.flagGreen.show()
                self.engine.guiMgr.flagPurple.hide()
                self.engine.guiMgr.flagYellow.hide()

                self.engine.guiMgr.flagRedL.show()
                self.engine.guiMgr.flagBlueL.hide()
                self.engine.guiMgr.flagGreenL.hide()
                self.engine.guiMgr.flagPurpleL.hide()
                self.engine.guiMgr.flagYellowL.hide()

                self.engine.guiMgr.flagRedR.hide()
                self.engine.guiMgr.flagBlueR.hide()
                self.engine.guiMgr.flagGreenR.hide()
                self.engine.guiMgr.flagPurpleR.show()
                self.engine.guiMgr.flagYellowR.hide()
        elif cursor == 4:

                self.engine.guiMgr.flagRed.hide()
                self.engine.guiMgr.flagBlue.hide()
                self.engine.guiMgr.flagGreen.hide()
                self.engine.guiMgr.flagPurple.show()
                self.engine.guiMgr.flagYellow.hide()

                self.engine.guiMgr.flagRedL.hide()
                self.engine.guiMgr.flagBlueL.hide()
                self.engine.guiMgr.flagGreenL.show()
                self.engine.guiMgr.flagPurpleL.hide()
                self.engine.guiMgr.flagYellowL.hide()

                self.engine.guiMgr.flagRedR.hide()
                self.engine.guiMgr.flagBlueR.hide()
                self.engine.guiMgr.flagGreenR.hide()
                self.engine.guiMgr.flagPurpleR.hide()
                self.engine.guiMgr.flagYellowR.show()

    def showFlagP2 (self, cursor): 
        if cursor == 0:
                self.engine.guiMgr.flagRedP2.hide()
                self.engine.guiMgr.flagBlueP2.hide()
                self.engine.guiMgr.flagGreenP2.hide()
                self.engine.guiMgr.flagPurpleP2.hide()
                self.engine.guiMgr.flagYellowP2.show()

                self.engine.guiMgr.flagRedLP2.hide()
                self.engine.guiMgr.flagBlueLP2.hide()
                self.engine.guiMgr.flagGreenLP2.hide()
                self.engine.guiMgr.flagPurpleLP2.show()
                self.engine.guiMgr.flagYellowLP2.hide()

                self.engine.guiMgr.flagRedRP2.hide()
                self.engine.guiMgr.flagBlueRP2.show()
                self.engine.guiMgr.flagGreenRP2.hide()
                self.engine.guiMgr.flagPurpleRP2.hide()
                self.engine.guiMgr.flagYellowRP2.hide()
        elif cursor == 1:
                self.engine.guiMgr.flagRedP2.hide()
                self.engine.guiMgr.flagBlueP2.show()
                self.engine.guiMgr.flagGreenP2.hide()
                self.engine.guiMgr.flagPurpleP2.hide()
                self.engine.guiMgr.flagYellowP2.hide()

                self.engine.guiMgr.flagRedLP2.hide()
                self.engine.guiMgr.flagBlueLP2.hide()
                self.engine.guiMgr.flagGreenLP2.hide()
                self.engine.guiMgr.flagPurpleLP2.hide()
                self.engine.guiMgr.flagYellowLP2.show()

                self.engine.guiMgr.flagRedRP2.show()
                self.engine.guiMgr.flagBlueRP2.hide()
                self.engine.guiMgr.flagGreenRP2.hide()
                self.engine.guiMgr.flagPurpleRP2.hide()
                self.engine.guiMgr.flagYellowRP2.hide()
        elif cursor == 2:

                self.engine.guiMgr.flagRedP2.show()
                self.engine.guiMgr.flagBlueP2.hide()
                self.engine.guiMgr.flagGreenP2.hide()
                self.engine.guiMgr.flagPurpleP2.hide()
                self.engine.guiMgr.flagYellowP2.hide()

                self.engine.guiMgr.flagRedLP2.hide()
                self.engine.guiMgr.flagBlueLP2.show()
                self.engine.guiMgr.flagGreenLP2.hide()
                self.engine.guiMgr.flagPurpleLP2.hide()
                self.engine.guiMgr.flagYellowLP2.hide()

                self.engine.guiMgr.flagRedRP2.hide()
                self.engine.guiMgr.flagBlueRP2.hide()
                self.engine.guiMgr.flagGreenRP2.show()
                self.engine.guiMgr.flagPurpleRP2.hide()
                self.engine.guiMgr.flagYellowRP2.hide()

        elif cursor == 3:

                self.engine.guiMgr.flagRedP2.hide()
                self.engine.guiMgr.flagBlueP2.hide()
                self.engine.guiMgr.flagGreenP2.show()
                self.engine.guiMgr.flagPurpleP2.hide()
                self.engine.guiMgr.flagYellowP2.hide()

                self.engine.guiMgr.flagRedLP2.show()
                self.engine.guiMgr.flagBlueLP2.hide()
                self.engine.guiMgr.flagGreenLP2.hide()
                self.engine.guiMgr.flagPurpleLP2.hide()
                self.engine.guiMgr.flagYellowLP2.hide()

                self.engine.guiMgr.flagRedRP2.hide()
                self.engine.guiMgr.flagBlueRP2.hide()
                self.engine.guiMgr.flagGreenRP2.hide()
                self.engine.guiMgr.flagPurpleRP2.show()
                self.engine.guiMgr.flagYellowRP2.hide()
        elif cursor == 4:

                self.engine.guiMgr.flagRedP2.hide()
                self.engine.guiMgr.flagBlueP2.hide()
                self.engine.guiMgr.flagGreenP2.hide()
                self.engine.guiMgr.flagPurpleP2.show()
                self.engine.guiMgr.flagYellowP2.hide()

                self.engine.guiMgr.flagRedLP2.hide()
                self.engine.guiMgr.flagBlueLP2.hide()
                self.engine.guiMgr.flagGreenLP2.show()
                self.engine.guiMgr.flagPurpleLP2.hide()
                self.engine.guiMgr.flagYellowLP2.hide()

                self.engine.guiMgr.flagRedRP2.hide()
                self.engine.guiMgr.flagBlueRP2.hide()
                self.engine.guiMgr.flagGreenRP2.hide()
                self.engine.guiMgr.flagPurpleRP2.hide()
                self.engine.guiMgr.flagYellowRP2.show()



