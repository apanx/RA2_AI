from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics
from Omni import Omni

class OmniVSpinner(Omni):
    "Omni strategy + Vertical spinner strategy"
    name = "OmniVSpinner"

    def __init__(self, **args):
        Omni.__init__(self, **args)

    def Tick(self):
        bReturn = Omni.Tick(self)
        # fire weapon
        if self.weapons:

            # spin up depending on enemy's range
            enemy, range = self.GetNearestEnemy()

            if enemy is not None and range < self.spin_range and self.weapons and not self.IsUpsideDown():
                self.Input("Spin", 0, 100)
            elif self.GetInputStatus("Spin", 0) != 0:
                self.Input("Spin", 0, 0)

            if self.IsUpsideDown():
                self.Input("Spin", 0, -100)

        return bReturn

AI.register(OmniVSpinner)
