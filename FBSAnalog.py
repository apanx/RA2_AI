from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics
from FBS import FBS

class FBSAnalog(FBS):
    "Spins!"
    name = "FBSAnalog"
    #Like FBS, but does not change the direction when inverted.
    #For Melty Brain type SnS that are more efficient when spinning in a certain direction.
    #Brought to you by Naryar and ripped off Apanx's FBS.py
    #Modified by Clickbeetle to reduce lag
    #Modified by 123STW to include spinning weapon.

    def __init__(self, **args):
        FBS.__init__(self, **args)
        self.spin_range = 99.0 #Range value (like spinner)
        if 'range' in args: self.spin_range = args.get('range')

    def Tick(self):
        bReturn = FBS.Tick(self)
        if self.weapons:
            # spin up depending on enemy's range
            enemy, range = self.GetNearestEnemy()

            if enemy is not None and range < self.spin_range:
                self.Input("Spin", 0, 100)
            elif self.GetInputStatus("Spin", 0) != 0:
                self.Input("Spin", 0, 0)
        return bReturn


    def Turn(self, turning):
        turning = min(max(turning, -100), 100)
        self.set_turn_throttle = turning
        self.Input('LeftRight', 0, -turning)
        self.Input('LeftRight', 1, turning)
        self.DebugString(1, "Turning = " + str(int(turning)))

AI.register(FBSAnalog)
