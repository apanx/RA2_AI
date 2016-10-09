from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics
from Omni import Omni

class OmniRam(Omni):
    "OmniRam strategy"
    name = "OmniRam"

    def __init__(self, **args):
        Omni.__init__(self, **args)

        tactic = [x for x in self.tactics if x.name == "Engage"]
        if len(tactic) > 0:
            self.tactics.remove(tactic[0])
        self.tactics.append(Tactics.Charge(self))
        self.tactics.append(Tactics.Shove(self))

AI.register(OmniRam)
