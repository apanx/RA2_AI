from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics
from Omni import Omni

class FlameOmni(Omni):
    "Omni strategy for bots with flamethrowers"
    name = "FlameOmni"
    # NOTES: This AI is specially designed for flamethrower bots. It will work for all bots that work with Omni, it justs adds special flamethrower lines.
    # It uses the flamethrower glitch, aka a flamethrower on an analog control does not weaken as long as you hold the analog control.
    # Proper bindings: The flamethrower's activation must be on the positive value of an Analog control that must be named Flame. Also you can add the 'flamerange' value in the bindings.
    # That 'flame_range' is the max distance to an opponent the flamethrower will activate, like 'range' on spinners (you still have the range command)
    # Brought to you by Naryar

    def __init__(self, **args):
        Omni.__init__(self, **args)
        self.flame_range = 30.0

        if 'flamerange' in args:
            self.flame_range = args.get('flamerange')

    def Tick(self):
        bReturn = Omni.Tick(self)
        # fire weapon
        if self.weapons:
            # flame on depending on enemy's range
            enemy, range = self.GetNearestEnemy()

            if enemy is not None and range < self.flame_range:
                self.Input("Flame", 0, 100)
            elif self.GetInputStatus("Flame", 0) != 0:
                self.Input("Flame", 0, 0)

        return bReturn

AI.register(FlameOmni)
