from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics
from Omni import Omni

class OmniInverted(Omni):
    "Omni inverted strategy"
    name = "OmniInverted"
    # bot has to be invertible, not mandatory to mention it in your binding, it is force.
    # much like omni except that the bot use a button control called 'Inverter' to invert itself if it is not.
    def __init__(self, **args):
        Omni.__init__(self, **args)

        # force bot to be invertible :
        self.invertible = True
        self.InverterTime  = 3

    def Tick(self):
        bReturn = Omni.Tick(self)
        if self.weapons:
            # If the bot is not inverted, try to invert it : use the button control called 'Inverter' :
            # here again, slight delay before inverting
            if self.InverterTime > 0: self.InverterTime -= 1

            #if (not self.ai.IsUpsideDown()) and (self.InverterTime <= 0) :
            #if (self.InverterTime <= 0) :
            if (not self.IsUpsideDown()) and (self.InverterTime <= 0) :
                self.Input("Inverter", 0, 1)
                self.InverterTime = self.reloadDelay

        return bReturn


AI.register(OmniInverted)
