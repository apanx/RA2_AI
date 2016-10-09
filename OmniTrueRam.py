from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics
from Omni import Omni

class OmniTrueRam(Omni):
    "OmniRam strategy with the real Ram and not Push."
    name = "OmniTrueRam"

    def __init__(self, **args):
        Omni.__init__(self, **args)

        tactic = [x for x in self.tactics if x.name == "Engage"]
        if len(tactic) > 0:
            self.tactics.remove(tactic[0])

        self.tactics.append(Tactics.Ram(self))

    def Tick(self):
        # fire srimech here - allows us to be invertible and use srimech at the same time
        if self.IsUpsideDown():
            for trigger in self.trigger2:
                self.Input(trigger, 0, 1)

        bReturn = Omni.Tick(self)
        return bReturn

AI.register(OmniTrueRam)