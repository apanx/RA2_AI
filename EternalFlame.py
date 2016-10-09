from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics
from Omni import Omni

class EternalFlame(Omni):
    "Has a totally awesome name!  Oh, and there's some stuff about holding down the flamethrower control so the flame doesn't die down, or something."
    name = "EternalFlame"
    #Basically Omni.py with a constantly activated forwards analog control named "Flame", specially for flamethrowers. Brought to you by Clickbeetle, improvement on original FlameOmni.py by Naryar.
    #Accepts the same controls as Omni, but you MUST wire your flamethrower to the forward position of an analog named "Flame" to make it work.
    #And yes, it has an awesome name.

    def __init__(self, **args):
        Omni.__init__(self, **args)

    def Activate(self, active):
        # Activate flame control at the start of the match, leaving it alone in def Tick
        self.Input("Flame", 0, 100)
        bReturn = Omni.Activate(self, active)

        return bReturn

AI.register(EternalFlame)