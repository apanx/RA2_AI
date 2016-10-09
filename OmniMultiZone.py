from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics
from Omni import Omni

class OmniMultiZone(Omni):
    "Omni strategy, up to 4 zones and the classical Fire/Weapon/Srimech"
    name = "OmniMultiZone"
    # up to 4 zones named weapon1, weapon2, weapon3 and weapon4
    # and the associated triggers : Fire1, Fire2, fire3, Fire4
    # weaponX is associated with FireX ie : ennemy in customzone weapon3 -> do the action associated with Fire3
    # You may also change the default tactics (engage) by specify in the bindings.py 'tactic': XXX
    # with XXX = "Charge", "Engage", "Shove", "Ram"
    def __init__(self, **args):
        Omni.__init__(self, **args)

    def Activate(self, active):
        bReturn = Omni.Activate(self, active)
        if active:
            self.RegisterSmartZone("weapon1", 2)
            self.RegisterSmartZone("weapon2", 3)
            self.RegisterSmartZone("weapon3", 4)
            self.RegisterSmartZone("weapon4", 5)

        return bReturn

    def SmartZoneEvent(self, direction, id, robot, chassis):
        if id == 1:
            if direction == 1:
                AI.SuperAI.SmartZoneEvent(self, direction, id, robot, chassis)
        elif id == 2:
            if robot > 0:
                if direction == 1:
                    self.Input("Fire1", 0, 1)
        elif id == 3:
            if robot > 0:
                if direction == 1:
                    self.Input("Fire2", 0, 1)
        elif id == 4:
            if robot > 0:
                if direction == 1:
                    self.Input("Fire3", 0, 1)
        elif id == 5:
            if robot > 0:
                if direction == 1:
                    self.Input("Fire4", 0, 1)

        return True

AI.register(OmniMultiZone)
