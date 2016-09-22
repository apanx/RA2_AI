from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics

class InvertOmni(AI.SuperAI):
    "Drive inverted when the srimech breaks."
    name = "InvertOmni"

    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)

        self.zone = "weapon"
        self.triggers = ["Fire"]
        self.trigger2 = ["Srimech"]
        self.reloadTime = 0
        self.reloadDelay = 3
        self.notMoving = 0
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
            if self.spin_range == math.pi*100:
                plus.emitSmoke(100, (plus.getLocation(self.GetID())), (0, 0, 0), (5, 5, 5))
                CompList = plus.describe(self.GetID())
                for comp in xrange(0,CompList.count(" ")): plus.show(self.GetID(),comp,0)

            self.RegisterSmartZone(self.zone, 1)

        return AI.SuperAI.Activate(self, active)

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

        # fire weapon
        if self.weapons:

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
        if id in self.sweapons: self.sweapons.remove(id)

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

AI.register(InvertOmni)
