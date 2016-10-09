from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics
from Omni import Omni

class SZSpinner(Omni):
    "Like Omni, but does not use a range value for a spinning weapon ; instead uses a smartzone"
    name = "SZSpinner"

    #IMPORTANT NOTE: This is a WIP and it might not work properly.
    #Just like said, this is an Omni AI that activates it's spinning weapon via a smartzone (that you need to name "spinner") rather than a range value.
    #For very short spinup time robots (jugglers, drums, face spinners, etc) that only really need to spin their weapons when the opponent is on them.
    #Brought to you by Naryar and inspired by Madiaba's Arrowhead.py.

    def __init__(self, **args):
        Omni.__init__(self, **args)

        self.spinzone = "spinner"
        self.botinspinzone = 0

    def Activate(self, active):
        bReturn = Omni.Activate(self, active)
        if active:
            self.RegisterSmartZone(self.spinzone, 2)

        return bReturn

    def Tick(self):
        # fire weapon
        if self.weapons:
            # spin up if enemy is in smartzone.
            if self.botinspinzone == 1:
                self.Input("Spin", 0, 100)
            else:
                self.Input("Spin", 0, 0)
        bReturn = Omni.Tick(self)
        return bReturn

    def SmartZoneEvent(self, direction, id, robot, chassis):
        if id == 2 and self.weapons:
            if robot > 0:
                if direction == 1:
                    self.botinspinzone = 1
                if direction == -1:
                    self.botinspinzone = 0
        return True

AI.register(SZSpinner)
