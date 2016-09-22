from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics

class FBSpinner(AI.SuperAI):
    "FBSpinner strategy"
    name = "FBSpinner"

    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)

        self.zone = "fbs"

        self.tactics.append(Tactics.Engage(self))

        self.whipTimer = 0
        self.whipDir = 3
        self.whipDirCount = 3

        self.whipFunction = self.WhipBackAndForth

        if 'zone' in args: self.zone = args['zone']

        if 'whip' in args:
            if args['whip'] == "around": self.whipFunction = self.WhipAround
            else: self.whipFunction = self.WhipBackAndForth

    def Activate(self, active):
        if active:
            if AI.SuperAI.debugging:
                self.debug = Gooey.Plain("watch", 0, 75, 100, 75)
                tbox = self.debug.addText("line0", 0, 0, 100, 15)
                tbox.setText("Throttle")
                tbox = self.debug.addText("line1", 0, 15, 100, 15)
                tbox.setText("Turning")
                tbox = self.debug.addText("line2", 0, 30, 100, 15)
                tbox.setText("")
                tbox = self.debug.addText("line3", 0, 45, 100, 15)
                tbox.setText("")

            self.RegisterSmartZone(self.zone, 1)
        else:
            # get rid of reference to self
            self.whipFunction = None

        return AI.SuperAI.Activate(self, active)

    def Tick(self):
        # fire weapon
        targets = []

        if self.weapons:
            targets = [x for x in self.sensors.itervalues() if x.contacts > 0 \
                and not plus.isDefeated(x.robot)]

        bReturn = AI.SuperAI.Tick(self)

        # call this now so it takes place after other driving commands
        if self.whipFunction: self.whipFunction(len(targets) > 0)

        return bReturn

    def WhipBackAndForth(self, bTarget):
        if bTarget: self.whipTimer = 16

        if self.whipTimer > 0:
            # Spin in one direction and wait for contact!
            if self.whipDir > 0: self.Turn(-3000)
            self.Throttle(0)

            self.whipDirCount -= 1
            if self.whipDirCount < 0:
                self.whipDirCount = 1
                self.whipDir = -self.whipDir

            self.whipTimer -= 1

    def WhipAround(self, bTarget):
        if bTarget: self.whipTimer = 1
        elif self.whipTimer == 0: self.whipDir = -self.whipDir

        if self.whipTimer > 0:
            # Move when being touched or targeted! Keep weapon facing towards opponent.
            if self.whipDir > 0: self.Turn(-1000)
            self.Throttle(1)

            self.whipTimer -= 0.5

    def LostComponent(self, id):
        # if we lose all our weapons, stop using the Engage tactic and switch to Shove
        if id in self.weapons: self.weapons.remove(id)

        if not self.weapons:
            tactic = [x for x in self.tactics if x.name == "Engage"]
            if len(tactic) > 0:
                self.tactics.remove(tactic[0])

                self.tactics.append(Tactics.Shove(self))
                self.tactics.append(Tactics.Charge(self))

        return AI.SuperAI.LostComponent(self, id)

    def DebugString(self, id, string):
        if self.debug:
            if id == 0: self.debug.get("line0").setText(string)
            elif id == 1: self.debug.get("line1").setText(string)
            elif id == 2: self.debug.get("line2").setText(string)
            elif id == 3: self.debug.get("line3").setText(string)

AI.register(FBSpinner)
