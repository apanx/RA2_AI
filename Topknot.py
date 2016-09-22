from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics

class Topknot(AI.SuperAI):
    "Topknot strategy"
    name = "Topknot"

    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)

        self.zone = "whipzone"
        self.zone2 = "AxeF"
        self.triggers2 = ["FireF"]
        self.zone3 = "AxeB"
        self.triggers3 = ["FireB"]
        self.zone4 = "AxeL"
        self.triggers4 = ["FireL"]
        self.zone5 = "AxeR"
        self.triggers5 = ["FireR"]
        self.zone6 = "under"

        self.tactics.append(Tactics.Engage(self))

        self.whipTimer = 0
        self.whipDir = 1
        self.whipDirCount = 2

        self.whipFunction = self.WhipBackAndForth

        if 'zone' in args: self.zone = args['zone']

        if 'whip' in args:
            if args['whip'] == "around": self.whipFunction = self.WhipAround
            else: self.whipFunction = self.WhipBackAndForth

        if 'triggers' in args: self.triggers2 = args['triggers']
        if 'triggers' in args: self.triggers3 = args['triggers']
        if 'triggers' in args: self.triggers4 = args['triggers']
        if 'triggers' in args: self.triggers5 = args['triggers']

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
            self.RegisterSmartZone(self.zone2, 2)
            self.RegisterSmartZone(self.zone3, 3)
            self.RegisterSmartZone(self.zone4, 4)
            self.RegisterSmartZone(self.zone5, 5)
            self.RegisterSmartZone(self.zone6, 6)
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

    def InvertHandler(self):
        # fire weapon once per second (until we're upright!)
        while 1:
            for trigger in self.triggers2: self.Input(trigger, 0, 2)
            for trigger in self.triggers3: self.Input(trigger, 0, 3)
            for trigger in self.triggers4: self.Input(trigger, 0, 4)
            for trigger in self.triggers5: self.Input(trigger, 0, 5)

            for i in range(0, 8):
                yield 0

    def WhipBackAndForth(self, bTarget):
        if bTarget: self.whipTimer = 4

        if self.whipTimer > 0:
            # Whip back and forth!
            if self.whipDir > 0: self.Turn(100)
            else: self.Turn(-100)
            self.Throttle(0)

            self.whipDirCount -= 1
            if self.whipDirCount < 0:
                self.whipDirCount = 2
                self.whipDir = -self.whipDir

            self.whipTimer -= 1

    def WhipAround(self, bTarget):
        if bTarget: self.whipTimer = 4
        elif self.whipTimer == 0: self.whipDir = -self.whipDir

        if self.whipTimer > 0:
            # Whip around!
            if self.whipDir > 0: self.Turn(100)
            else: self.Turn(-100)
            self.Throttle(0)

            self.whipTimer -= 1

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

    def SmartZoneEvent(self, direction, id, robot, chassis):
        if id == 1:
            if direction == 1:
                AI.SuperAI.SmartZoneEvent(self, direction, id, robot, chassis)
        elif id == 2:
            if robot > 0:
                if direction == 1:
                    for trigger in self.triggers2: self.Input(trigger, 0, 2)
        elif id == 3:
            if robot > 0:
                if direction == 1:
                    for trigger in self.triggers3: self.Input(trigger, 0, 3)
        elif id == 4:
            if robot > 0:
                if direction == 1:
                    for trigger in self.triggers4: self.Input(trigger, 0, 4)
        elif id == 5:
            if robot > 0:
                if direction == 1:
                    for trigger in self.triggers5: self.Input(trigger, 0, 5)

        elif id == 6:
            if robot > 0:
                if direction == 1:
                    for trigger in self.triggers2: self.Input(trigger, 0, 2)
                    for trigger in self.triggers3: self.Input(trigger, 0, 3)
                    for trigger in self.triggers4: self.Input(trigger, 0, 4)
                    for trigger in self.triggers5: self.Input(trigger, 0, 5)
        return True

AI.register(Topknot)
