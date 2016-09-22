from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics

class Smashbox(AI.SuperAI):
    "peshull ai for smashbocks too"
    name = "Smashbox"

    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)

        self.zone = "weapon"
        self.triggers = ["Fire"]
        self.trigger2 = ["Srimech"]
        self.reloadTime = 0
        self.reloadDelay = 3

        self.spin_range = 3.0

        if 'range' in args:
            self.spin_range = args.get('range')

        if 'triggers' in args: self.triggers = args['triggers']
        if 'reload' in args: self.reloadDelay = args['reload']

        self.triggerIterator = iter(self.triggers)

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

        return AI.SuperAI.Activate(self, active)

    def Tick(self):
        if not self.weapons or not self.sweapons or not self.tweapons or not self.qweapons:
            self.bInvertible = True

        # fire weapon
        if (self.weapons or self.sweapons or self.tweapons or self.qweapons) and not self.IsUpsideDown():

            # spin up depending on enemy's range
            enemy, range = self.GetNearestEnemy()

            if enemy is not None and range < self.spin_range:
                self.Input("Spin", 0, 1)
            elif self.GetInputStatus("Spin", 0) != 0:
                self.Input("Spin", 0, 0)

            targets = [x for x in self.sensors.itervalues() if x.contacts > 0 \
                and not plus.isDefeated(x.robot)]

            # slight delay between firing
            if self.reloadTime > 0: self.reloadTime -= 1

            if len(targets) > 0 and self.reloadTime <= 0:
                try:
                    trigger = self.triggerIterator.next()
                except StopIteration:
                    self.triggerIterator = iter(self.triggers)
                    trigger = self.triggerIterator.next()

                self.Input(trigger, 0, 1)
                self.reloadTime = self.reloadDelay

        return AI.SuperAI.Tick(self)

    def InvertHandler(self):
        # fire all weapons once per second (until we're upright!)
        while 1:
            for trigger in self.trigger2:
                self.Input(trigger, 0, 1)

            for i in range(0, 8):
                yield 0

    def LostComponent(self, id):
        # if we lose all our weapons, stop using the Engage tactic and switch to Shove
        if id in self.weapons: self.weapons.remove(id)

        if not self.weapons and not self.sweapons and not self.tweapons and not self.qweapons:
            self.top_speed = 100
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

AI.register(Smashbox)
