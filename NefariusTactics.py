import math
import plus
import AI
import Arenas
import Tactics

class PreBattleSetup(AI.Tactic):
    name = "PreBattleSetup"

    def __init__(self, ai):
        AI.Tactic.__init__(self, ai)

        list = [x for x in AI.ai_bindings if x[0] == self.ai.botName]
        self.setupTime = list[0][2].get('SetupTime')
        if self.setupTime == None: self.setupTime = 0
        self.setupControl = list[0][2].get('SetupControl')
        if self.setupControl == None: self.setupControl = 'Forward'
        self.setupDirection = list[0][2].get('SetupDirection') #1 to -1
        if self.setupDirection == None: self.setupDirection = 1

        self.setupDirection = min(max(self.setupDirection, 1), -1)

        self.exactTime = 0

        # TODO: Add support for more than one action

    def Evaluate(self): #Called Every 8th Tick
        if self.exactTime != 0:
            pass
        elif self.setupTime != 0:
            self.exactTime = plus.getTimeElapsed() + self.setupTime
            self.priority = 1000
            self.setupTime = 0
        else:
            self.priority = -1000

    def Execute(self): #Called Every Tick
        if plus.getTimeElapsed() < self.exactTime:
            self.ai.Input(self.setupControl, 0, 100 * self.setupDirection)
            return True
        self.exactTime = 0
        return False
