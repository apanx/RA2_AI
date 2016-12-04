from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics
from Omni import Omni

class OmniSwitch(Omni):
    "OmniSwitch strategy"
    name = "OmniSwitch"

    def __init__(self, **args):
        Omni.__init__(self, **args)

    def Tick(self):

        self.Input("Spin", 0, 1)

        return AI.SuperAI.Tick(self)

    def InvertHandler(self):
        # fire weapon once per second (until we're upright!)
        while 1:
            for trigger in self.triggers: self.Input(trigger, 0, 1)

            for i in range(0, 8):
                yield 0

AI.register(OmniSwitch)
