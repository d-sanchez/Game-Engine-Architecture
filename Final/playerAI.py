class PlayerAI:
    def __init__(self, ent):
        self.ent = ent
        self.ActionList = []
        
    def tick(self, dtime):
        if len(self.ActionList) > 0:
            self.ActionList[0].tick(dtime)

    def clear(self):
    	del self.ActionList[:]