from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics
from Omni import Omni

class InvertOmni(Omni):
    "Drive inverted when the srimech breaks."
    name = "InvertOmni"

    def __init__(self, **args):
        Omni.__init__(self, **args)

        self.notMoving = 0
    def Tick(self):
        # drive inverted
        if not self.sweapons:
            self.bInvertible = True

        #detect when bot is not moving
        if abs(self.GetSpeed()) < 0.5:
            self.notMoving = 1
        else:
            self.notMoving = 0

        #drive backwards when upside down
        if self.weapons and self.IsUpsideDown() and self.notMoving == 0:
            self.Input("DriveBack", 0, 100)

        if self.weapons and self.IsUpsideDown() and self.notMoving == 1:
            self.Input("DriveBack", 0, -100)

        if not self.IsUpsideDown():
            self.Input("DriveBack", 0, 0)

        bReturn = Omni.Tick(self)
        return bReturn

    def LostComponent(self, id):
        if id in self.sweapons: self.sweapons.remove(id)
        bReturn = Omni.LostComponent(self, id)
        return bReturn

AI.register(InvertOmni)
