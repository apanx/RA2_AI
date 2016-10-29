from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics

class Batmobile(AI.SuperAI):
    "Like Popup but tweaked for BatmobileAI."
    name = "Batmobile"

    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)

        self.zone1 = "weapon"
        self.zone2 = "underweapon"
        self.sweapons = []               # used to track our secondary weapons
        self.tweapons = []               # used to track our tertiary weapons
        self.qweapons = []               # used to track our quaternary weapons
        self.triggers1 = ["PrimaryWep"]
        self.triggers2 = ["SecondaryWep"]
        self.triggers3 = ["Srimech"]
        self.triggers4 = ["HitUnder"]
        self.botinzone = 0
        self.botinzone2 = 0
        self.compinzone = 0
        self.comptimer = 0
        self.NoChassisTime = 8

        if 'sweapons' in args: self.sweapons = list(args['sweapons'])
        if 'tweapons' in args: self.tweapons = list(args['tweapons'])
        if 'qweapons' in args: self.qweapons = list(args['qweapons'])

        if 'NoChassisTime' in args: self.NoChassisTime = args.get('NoChassisTime') * 8

        self.tactics.append(Tactics.Engage(self))

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

            self.RegisterSmartZone(self.zone1, 1)
            self.RegisterSmartZone(self.zone2, 2)

        return AI.SuperAI.Activate(self, active)

    def Tick(self):
        # Don't try to self right if any part of the srimech breaks.
        if not self.weapons or not self.sweapons or not self.tweapons or not self.qweapons:
            self.bInvertible = True

        # fire weapon
        targets = [x for x in self.sensors.itervalues() if x.contacts > 0 \
                and not plus.isDefeated(x.robot)]

        # if a component is in the smart zone but not the chassis, wait to find chassis before firing weapons
        if self.compinzone == 1 and self.botinzone == 0:
            self.comptimer += 1

        if self.botinzone == 1:
            self.comptimer = 0

        if self.botinzone == 1 or (self.comptimer >= self.NoChassisTime and self.compinzone == 1):
            if self.weapons or self.sweapons:
                for trigger in self.triggers1: self.Input(trigger, 0, 1)
            else:
                for trigger in self.triggers2: self.Input(trigger, 0, 1)

        # Hit bots underneath
        if self.botinzone2 == 1:
            for trigger in self.triggers4: self.Input(trigger, 0, 1)

        bReturn = AI.SuperAI.Tick(self)

        return bReturn

    def InvertHandler(self):
        # fire all weapons once per second (until we're upright!)
        while 1:
            for trigger in self.triggers3:
                self.Input(trigger, 0, 1)

            for i in range(0, 8):
                yield 0

    def LostComponent(self, id):
        # if we lose all our weapons, stop using the Engage tactic and switch to Shove
        if id in self.weapons: self.weapons.remove(id)
        if id in self.sweapons: self.sweapons.remove(id)
        if id in self.tweapons: self.tweapons.remove(id)
        if id in self.qweapons: self.qweapons.remove(id)

        if not self.weapons and not self.sweapons and not self.tweapons and not self.qweapons:
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
            if robot > 0:
                if direction == 1:
                    self.compinzone = 1
                    if chassis:
                        self.botinzone = 1
                if direction == -1:
                    self.compinzone = 0
                    if chassis:
                        self.botinzone = 0
        elif id == 2:
            if robot > 0:
                if direction == 1:
                    self.botinzone2 = 1
                if direction == -1:
                    self.botinzone2 = 0
        return True

AI.register(Batmobile)
