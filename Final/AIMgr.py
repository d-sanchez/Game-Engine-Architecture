import AIaction as action
class AIMgr:
	#AI Mgr will manager FSM of team 
	#AI aspect will manage FSM of players
    def __init__(self, engine):
        self.engine = engine
        self.ball = self.engine.entityMgr.ball
        self.team1 = self.engine.entityMgr.team1
        self.team2 = self.engine.entityMgr.team2
        self.half = self.engine.gameMgr.half
        self.whoHasBall = 0
        self.entityMgr = self.engine.entityMgr
        self.simpleAI = True

    def init(self):

    	pass

    def tick(self, dt):
        if (self.simpleAI):
            self.BennyHillAI()
        else :
            self.BennyHillAI()
            pass
        pass

    def BennyHillAI(self):
        ball = self.engine.entityMgr.ball
        
        if (ball.attachEnt):
            self.whoHasBall = ball.attachEnt.team
        #self.whoHasBall = 0

        if (self.whoHasBall == 1):
            for ent in self.entityMgr.team2.values():
                ent.aspects[2].clear()
             
                if (ent != self.engine.entityMgr.selectedEntP2 and ent != self.engine.entityMgr.GKP2):
                    #print 'assign behavior'
                    self.entityMgr.addAction(ent, action.Intercept(ent,  ball.attachEnt))
            
            
            for ent in self.entityMgr.team1.values():
                ent.aspects[2].clear()

                if (ent != self.engine.entityMgr.selectedEntP1 and ent != self.engine.entityMgr.GKP1):
                    self.entityMgr.addAction(ent, action.Intercept(ent, self.engine.entityMgr.GKP2))
                 

        elif (self.whoHasBall == 2):
            for ent in self.entityMgr.team1.values():
                ent.aspects[2].clear()

                if (ent != self.engine.entityMgr.selectedEntP1 and ent != self.engine.entityMgr.GKP1):
                    self.entityMgr.addAction(ent, action.Intercept(ent, ball.attachEnt))

            for ent in self.entityMgr.team2.values():
                ent.aspects[2].clear()

                if (ent != self.engine.entityMgr.selectedEntP2 and ent != self.engine.entityMgr.GKP2):
                    self.entityMgr.addAction(ent, action.Intercept(ent, self.engine.entityMgr.GKP1))


        self.goalKeeping()            
        pass


    def goalKeeping(self):
        GKP1 = self.engine.entityMgr.GKP1
        GKP2 = self.engine.entityMgr.GKP2
        ball = self.engine.entityMgr.ball

        self.entityMgr.addAction(GKP1, action.TrackBall(GKP1, ball))
        self.entityMgr.addAction(GKP2, action.TrackBall(GKP2, ball))
        


        pass
