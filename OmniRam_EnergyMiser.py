from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics
from Omni import Omni
# Purpose:
    # For Bots with short spin-up time (Face Spinners, Top Spinners, Jugglers,...).
    # Saves energy by shutting off weapon motor(s) when NearestEnemy is not near.
# Instructions:
    # Use Analog control, and name "Spin".
    # Adjust turn-on 'range' in Bindings line (as normal):
    # list.append(("Topster", "OmniRam_EnergyMiser", {'invertible':True, 'range':5, 'turn':30, 'turnspeed':2.5, 'radius':1, 'topspeed':100, 'throttle':130, 'weapons':(1,2,3,4,5)}))

    # ('Srimech' invert handler)


class OmniRam_EnergyMiser(Omni):
    "OmniRam strategy, with Energy Saver Technology"
    name = "OmniRam_EnergyMiser"

    def __init__(self, **args):
        Omni.__init__(self, **args)

        tactic = [x for x in self.tactics if x.name == "Engage"]
        if len(tactic) > 0:
            self.tactics.remove(tactic[0])
        self.tactics.append(Tactics.Charge(self))
        self.tactics.append(Tactics.Shove(self))

    def Tick(self):
        bReturn = Omni.Tick(self)
        # fire weapon
        if self.weapons:
            # spin up depending on enemy's range
            enemy, range = self.GetNearestEnemy()

            if enemy is not None and range < self.spin_range:
                self.Input("Spin", 0, 100)
            elif self.GetInputStatus("Spin", 0) != 0:
                self.Input("Spin", 0, 0)

        return bReturn


AI.register(OmniRam_EnergyMiser)
