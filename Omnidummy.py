from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics
from Omni import Omni

class Omnidummy(Omni):
    "Omnidummy strategy"
    name = "Omnidummy"

    def __init__(self, **args):
        Omni.__init__(self, **args)

    def Tick(self):
        bReturn = Omni.Tick(self)
        if self.weapons:
            if enemy is not None and range < self.spin_range:
                self.Input("Spin80", 0, 80)
            elif self.GetInputStatus("Spin", 0) != 0:
                self.Input("Spin80", 0, 0)
            if enemy is not None and range < self.spin_range:
                self.Input("Spin", 0, 100)
            elif self.GetInputStatus("Spin", 0) != 0:
                self.Input("Spin", 0, 0)

        return bReturn

AI.register(Omnidummy)
