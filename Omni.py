from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics

class Omni(AI.SuperAI):
    "Omni strategy"
    name = "Omni"
    # This is a newer version with the ability to select tactics.  Simply put 'tactic':"Ram" (or "Charge") in Bindings to make the AI use rammer/pusher tactics.  No more need for OmniRam.py or any of those!

    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)

        self.zone = "weapon"
        self.sweapons = []               # used to track our secondary weapons
        self.tweapons = []               # used to track our tertiary weapons
        self.qweapons = []               # used to track our quaternary weapons

        self.triggers = ["Fire"]
        self.trigger2 = ["Srimech"]
        self.reloadTime = 0
        self.reloadDelay = 3

        self.spin_range = 3.0

        self.theTactic = "Engage"

        if 'sweapons' in args: self.sweapons = list(args['sweapons'])
        if 'tweapons' in args: self.tweapons = list(args['tweapons'])
        if 'qweapons' in args: self.qweapons = list(args['qweapons'])

        if 'range' in args:
            self.spin_range = args.get('range')

        if 'triggers' in args: self.triggers = args['triggers']
        if 'reload' in args: self.reloadDelay = args['reload']

        self.triggerIterator = iter(self.triggers)

        if 'tactic' in args:
            self.theTactic = args['tactic']

        self.tactics.append(getattr(Tactics, self.theTactic)(self))

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

AI.register(Omni)
