from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics

class FireDelayStop(AI.SuperAI):
    "Delays initial weapon firing separate from reload and stops while weapon is firing."
    name = "FireDelayStop"

    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)

        self.zone = "weapon"
        self.zone2 = "alsoweapon"
        self.triggers = ["Fire"]
        self.trigger2 = ["Srimech"]
        self.reloadTime = 0
        self.reloadDelay = 3
        self.retractTime = 15

        self.botinzone = 0
        self.delaycount = 0
        self.initdelay = 3
        self.stopcheck = 0
        self.stopFunction = self.Stop

        if 'reload' in args: self.reloadDelay = args['reload']
        if 'firedelay' in args: self.initdelay = args['firedelay']
        if 'retract' in args: self.retractTime = args['retract']
        if 'zone' in args: self.zone = args['zone']
        if 'triggers' in args: self.triggers = args['triggers']

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

            self.RegisterSmartZone(self.zone, 1)
            self.RegisterSmartZone(self.zone2, 2)
        else:
            # get rid of reference to self
            self.stopFunction = None

        return AI.SuperAI.Activate(self, active)

    def Tick(self):
        # fire weapon
        targets = []

        if self.weapons:
            targets = [x for x in self.sensors.itervalues() if x.contacts > 0 \
                and not plus.isDefeated(x.robot)]

        bReturn = AI.SuperAI.Tick(self)

        # call this now so it takes place after other driving commands
        if self.stopFunction: self.stopFunction(len(targets) > 0)

        return bReturn

    def Stop(self, bTarget):
        # drive inverted
        if not self.sweapons:
            self.bInvertible = True

        # fire weapon
        if self.weapons:

            if self.botinzone == 1:
                self.delaycount += 1
            if self.botinzone == 0:
                self.delaycount = 0

            # slight delay between firing
            if self.reloadTime > 0: self.reloadTime -= 1

            if self.delaycount >= self.initdelay and self.reloadTime <= 0:
                for trigger in self.triggers: self.Input(trigger, 0, 1)
                self.reloadTime = self.reloadDelay

            #stop moving while firing weapon
            if self.delaycount > (self.initdelay - 3) and (self.reloadTime < 3 or self.reloadTime > (self.reloadDelay - self.retractTime)):
                self.Throttle(0)

    def InvertHandler(self):
        # fire weapon once per second (until we're upright!)
        while 1:
            for trigger in self.trigger2: self.Input(trigger, 0, 1)

            for i in range(0, 8):
                yield 0

    def LostComponent(self, id):
        # if we lose all our weapons, stop using the Engage tactic and switch to Shove
        if id in self.weapons: self.weapons.remove(id)
        if id in self.sweapons: self.sweapons.remove(id)

        if not self.weapons:
            tactic = [x for x in self.tactics if x.name == "Engage"]
            if len(tactic) > 0:
                self.tactics.remove(tactic[0])

                self.tactics.append(Tactics.Charge(self))
                self.tactics.append(Tactics.Shove(self))

        return AI.SuperAI.LostComponent(self, id)

    def DebugString(self, id, string):
        if self.debug:
            if id == 0: self.debug.get("line0").setText(string)
            elif id == 1: self.debug.get("line1").setText(string)
            elif id == 2: self.debug.get("line2").setText(string)
            elif id == 3: self.debug.get("line3").setText(string)

    def SmartZoneEvent(self, direction, id, robot, chassis):
        if id == 1 or id == 2:
            if robot > 0:
                if direction == 1:
                    self.botinzone = 1
            else:
                self.botinzone = 0
        return True

AI.register(FireDelayStop)
