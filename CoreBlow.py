from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics

class CoreBlow(AI.SuperAI):
    "Why does Core Blow get its own AI Mommy?  Because it's a very special bot, little Billy.  Does Core Blow ride the short bus Mommy?  Yes, but we don't talk about things like that."
    name = "CoreBlow"

    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)

        self.zone1 = "PrimaryWep"
        self.triggers1 = ["PrimaryWep"]
        self.zone2 = "SecondaryWep"
        self.triggers2 = ["SecondaryWep"]
        self.triggers5 = ["Srimech"]

        self.sweapons = []               # used to track our secondary weapons

        self.notMoving = 0
        self.botinzone = 0
        self.spin_range = 3.0

        if 'sweapons' in args: self.sweapons = list(args['sweapons'])
        if 'range' in args:
            self.spin_range = args.get('range')

        if 'zone' in args: self.zone = args['zone']

        if 'triggers' in args: self.triggers1 = args['triggers']
        if 'triggers2' in args: self.triggers2 = args['triggers2']

        self.tactics.append(Tactics.Engage(self))

    def Activate(self, active):
        if active:
            if AI.SuperAI.debugging:
                self.debug = Gooey.Plain("watch", 10, 175, 250, 175)
                tbox = self.debug.addText("line0", 10, 0, 100, 15)
                tbox.setText("Throttle")
                tbox = self.debug.addText("line1", 10, 15, 100, 15)
                tbox.setText("Turning")
                tbox = self.debug.addText("line2", 10, 30, 100, 15)
                tbox.setText("")
                tbox = self.debug.addText("line3", 10, 45, 100, 15)
                tbox.setText("")
                tbox = self.debug.addText("line4", 10, 60, 250, 15)
                tbox.setText("")
                tbox = self.debug.addText("line5", 10, 75, 250, 15)
                tbox.setText("")

            self.RegisterSmartZone(self.zone1, 1)
            self.RegisterSmartZone(self.zone2, 2)

        return AI.SuperAI.Activate(self, active)

    def Tick(self):
        self.DebugString(4, "self.botinzone: "+  str(self.botinzone))
        self.DebugString(5, "self.notMoving: "+  str(self.notMoving))
        #drive inverted
        if not self.sweapons:
            self.bInvertible = True

        #keep track of when we're not moving
        if abs(self.GetSpeed()) < 1:
            self.notMoving = 1
        else:
            self.notMoving = 0

        # spin up depending on enemy's range
        enemy, range = self.GetNearestEnemy()

        if enemy is not None and range < self.spin_range:
            self.Input("Spin", 0, 1)
        elif self.GetInputStatus("Spin", 0) != 0:
            self.Input("Spin", 0, 0)

        # fire weapon

        targets = [x for x in self.sensors.itervalues() if x.contacts > 0 \
                and not plus.isDefeated(x.robot)]

        if self.sweapons and self.botinzone == 1 and self.notMoving == 1 and self.weapons:
            for trigger in self.triggers1: self.Input(trigger, 0, 1)

        if self.sweapons and self.botinzone == 1 and not self.weapons:
            for trigger in self.triggers1: self.Input(trigger, 0, 1)

        bReturn = AI.SuperAI.Tick(self)

        return bReturn

    def InvertHandler(self):
        # fire all weapons once per second (until we're upright!)
        while 1:
            for trigger in self.triggers5:
                self.Input(trigger, 0, 1)

            for i in range(0, 8):
                yield 0

    def LostComponent(self, id):
        # if we lose all our weapons, stop using the Engage tactic and switch to Shove
        if id in self.weapons: self.weapons.remove(id)
        if id in self.sweapons: self.sweapons.remove(id)

        if not self.weapons and not self.sweapons:
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
            elif id == 4: self.debug.get("line4").setText(string)
            elif id == 5: self.debug.get("line5").setText(string)

    def SmartZoneEvent(self, direction, id, robot, chassis):
        if id == 1 and self.weapons:
            if robot > 0:
                if chassis:
                    if direction == 1:
                        self.botinzone = 1
                    if direction == -1:
                        self.botinzone = 0
        elif id == 2 and self.sweapons and not self.weapons:
            if robot > 0:
                if chassis:
                    if direction == 1:
                        self.botinzone = 1
                    if direction == -1:
                        self.botinzone = 0
        return True

AI.register(CoreBlow)