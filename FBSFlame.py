from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics
from FBS import FBS

class FBSFlame(FBS):
    "Like FBS, but with flamethrower control"
    name = "FBSFlame"
    #Normal FBS with EternalFlame.py-style flamethrower control. For the ones who don't want to bother to see how Octane.py works but want good flame FBS.
    def __init__(self, **args):
        FBS.__init__(self, **args)

    def Activate(self, active):
        self.Input("Flame", 0, 100)
        FBS.Activate(self, active)

        return plus.AI.Activate(self, active)

AI.register(FBSFlame)
