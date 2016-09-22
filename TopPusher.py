from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics

class TopPusher(AI.SuperAI):
    "Uses a smart zone to keep pushing bots even when they are on top of this bot."
    name = "TopPusher"
    # Needs a separate analog control named "Push" wired to the drive, and a smart zone named "Push".
    # Put 'tactic':"Ram" (or "Charge") in Bindings to make the AI use rammer/pusher tactics.

    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)

        self.zone = "Push"
        self.triggers = ["Fire"]
        self.trigger2 = ["Srimech"]
        self.reloadTime = 0
        self.reloadDelay = 3
        self.compinzone = 0
        self.spin_range = 3.0

        if 'range' in args:
            self.spin_range = args.get('range')

        if 'triggers' in args: self.triggers = args['triggers']
        if 'reload' in args: self.reloadDelay = args['reload']

        self.triggerIterator = iter(self.triggers)

        if 'tactic' in args:
            self.theTactic = args['tactic']
            if   self.theTactic  == "Charge" : self.tactics.append(Tactics.Charge(self))
            elif self.theTactic  == "Ram" : self.tactics.append(Tactics.Ram(self))
            elif self.theTactic  == "Shove" : self.tactics.append(Tactics.Shove(self))
            elif self.theTactic  == "Engage" : self.tactics.append(Tactics.Engage(self))
            else: self.tactics.append(Tactics.Engage(self))
        else: self.tactics.append(Tactics.Engage(self))

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
        # Push when a bot is in the smart zone
        if self.compinzone == 1 and not self.bImmobile:
            self.Input("Push", 0, 100)
        else:
            self.Input("Push", 0, 0)

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

    def SmartZoneEvent(self, direction, id, robot, chassis):
        if id == 1:
            if robot > 0:
                if direction == 1:
                    self.compinzone = 1
                elif direction == -1:
                    self.compinzone = 0

        return True

AI.register(TopPusher)
