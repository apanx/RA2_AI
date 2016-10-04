from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics
from Bee import Bee

class BeeCC(Bee):
    "Bee Counter-Clockwise SpinWhip strategy"
    name = "BeeCC"

    def __init__(self, **args):
        Bee.__init__(self, **args)

    def WhipAround(self, bTarget):
        if bTarget: self.whipTimer = 3
        elif self.whipTimer == 0: self.whipDir = self.whipDir

        if self.whipTimer > 0:
            # Whip around!
            if self.whipDir > 0: self.Turn(-100)
            else: self.Turn(100)
            self.Throttle(0)

            self.whipTimer -= 1

AI.register(BeeCC)
