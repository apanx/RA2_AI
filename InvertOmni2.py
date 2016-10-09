from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics
from Omni import Omni

class InvertOmni2(Omni):
    "Omni that can be invertible and fire a srimech at the same time."
    name = "InvertOmni2"

    def __init__(self, **args):
        Omni.__init__(self, **args)

    def Tick(self):
        # be self righteous even if we're invertible
        if self.IsUpsideDown():
            for trigger in self.trigger2:
                self.Input(trigger, 0, 1)

        bReturn = Omni.Tick(self)
        return bReturn

AI.register(InvertOmni2)