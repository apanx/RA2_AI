from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics
from Omni import Omni

class Evade(AI.Tactic):
    name = "Evade"

    def __init__(self, ai):
        AI.Tactic.__init__(self, ai)

    def Evaluate(self):
        self.priority = 0
        id, range = self.ai.GetNearestEnemy()

    def Execute(self):
        # get information about self and ennemy :
        id, range = self.ai.GetNearestEnemy() # Find Nearest Enemy.

        if id != None:
            a = Arenas.currentArena

        if id is not None:
            h = self.ai.GetHeadingToID(id, False) # Find HEADING to Nearest Enemy.

            if self.ai.GetLocation()[0] <= abs(4) or self.ai.GetLocation()[2] <= abs(4): # If AI is NOT too far from middle of arena..
                if abs(h) >= .4:
                    self.ai.AimToHeading(h) # Point nose toward opponent...
                elif abs(h) < .4  and  range < 4:
                    self.ai.Throttle(-100)       # Then Back up.


            if self.ai.GetLocation()[0] >= abs(4) or self.ai.GetLocation()[2] >= abs(4): # If AI is TOO FAR from middle of arena..
                self.ai.DriveToLocation((0,0,0))
                self.ai.Throttle(100)

        return True

class WimpOmni(Omni):
    "WimpOmni strategy"
    name = "WimpOmni"
    #Modified Omni.py. When the robot runs out of weapons, it will run away from the other robot. Requires Tactics2.py.

    def __init__(self, **args):
        Omni.__init__(self, **args)

    def LostComponent(self, id):
        # if we lose all our weapons, stop using the Engage tactic and switch to Shove
        if id in self.weapons: self.weapons.remove(id)

        if not self.weapons:
            tactic = [x for x in self.tactics if x.name == self.theTactic]
            if len(tactic) > 0:
                self.tactics.remove(tactic[0])

                self.tactics.append(Evade(self))

        return AI.SuperAI.LostComponent(self, id)

AI.register(WimpOmni)
