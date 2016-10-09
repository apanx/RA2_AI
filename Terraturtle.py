from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics
from Omni import Omni

class Terraturtle(Omni):
    "Slow OmniRam strategy"
    name = "Terraturtle"

    def __init__(self, **args):
        Omni.__init__(self, **args)

        tactic = [x for x in self.tactics if x.name == "Engage"]
        if len(tactic) > 0:
            self.tactics.remove(tactic[0])
        self.tactics.append(Tactics.Charge(self))
        self.tactics.append(Tactics.Shove(self))

    def Tick(self):
        bReturn = Omni.Tick(self)
        # fire weapon
        if self.weapons:
            if len(targets) > 0 and self.reloadTime <= 0:
                try:
                    trigger = self.triggerIterator.next()
                except StopIteration:
                    self.triggerIterator = iter(self.triggers)
                    trigger = self.triggerIterator.next()

                self.Input(trigger, 0, 1)
                self.Throttle(0)
                self.reloadTime = self.reloadDelay

        return bReturn
AI.register(Terraturtle)
