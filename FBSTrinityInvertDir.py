from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics
from FBS import FBS

class FBSTrinityInvertDir(FBS):
    "Spins!"
    name = "FBSTrinityInvertDir"
    #Like FBS, but does not change the direction when inverted.
    #Also supports pistons for Trinity effect.
    #For Melty Brain type SnS that are more efficient when spinning in a certain direction.
    #Brought to you by Naryar and ripped off Apanx's FBS.py

    def __init__(self, **args):
        FBS.__init__(self, **args)
        self.trinityrange = 40

    def Tick(self):
        FBS.Tick(self)
        # fire weapon
        if self.weapons:
            targets = [x for x in self.sensors.itervalues() if x.contacts > 0 \
                and not plus.isDefeated(x.robot)]

            # slight delay between firing
            if self.reloadTime > 0: self.reloadTime -= 1

            if len(targets) > 0 and self.reloadTime <= 0:
                try:
                    trigger = self.triggerIterator.next()
                except StopIteration:
                    self.triggerIterator = iter(self.triggers)
                    trigger = self.triggerIterator.next()

                self.Input(trigger, 0, 1)
                self.reloadTime = self.reloadDelay

        return plus.AI.Tick(self)

    def Turn(self, turning):
        turning = min(max(turning, -100), 100)

        self.set_turn_throttle = turning
        self.Input('LeftRight', 0, -turning)
        self.Input('LeftRight', 1, turning)
        self.DebugString(1, "Turning = " + str(int(turning)))

AI.register(FBSTrinityInvertDir)
