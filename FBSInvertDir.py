from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics
from FBS import FBS

class FBSInvertDir(AI.SuperAI):
    "Spins!"
    name = "FBSInvertDir"
        #Like FBS, but does not change the direction when inverted.
        #For Melty Brain type SnS that are more efficient when spinning in a certain direction.
        #Brought to you by Naryar

    def __init__(self, **args):
        FBS.__init__(self, **args)
    def Turn(self, turning):
        turning = min(max(turning, -100), 100)
        self.set_turn_throttle = turning
        self.Input('LeftRight', 0, -turning)
        self.Input('LeftRight', 1, turning)
        self.DebugString(1, "Turning = " + str(int(turning)))

AI.register(FBSInvertDir)
