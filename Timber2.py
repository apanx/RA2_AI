from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics

class Timber2(AI.SuperAI):
    "AI that stops moving forward while the weapon is retracting (because Timber II's driving applies force to the chassis which hinders retracting)."
    # Set the amount of ticks it takes for the weapon to make one complete downward swing with 'FiringTime'.  The AI will continue driving during this time.
    # Set the amount of ticks it takes to retract the weapon with 'RetractingTime'.  This time starts once the FiringTime is over.  The AI will not drive forwards during this time.
    # 1 tick = 1/8 second
    name = "Timber2"

    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)

        self.zone = "weapon"
        self.triggers = ["Fire"]
        self.trigger2 = ["Srimech"]
        self.reloadTime = 0
        self.reloadDelay = 3
        self.stopFunction = self.Stop
        self.spin_range = 3.0
        self.firing = 0
        self.retracting = 0
        self.fireTime = 4
        self.retractTime = 8
        self.didFire = 0

        if 'range' in args:
            self.spin_range = args.get('range')
        if 'FiringTime' in args:
            self.fireTime = args.get('FiringTime')
        if 'RetractingTime' in args:
            self.retractTime = args.get('RetractingTime')

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
        else:
            # get rid of reference to self
            self.stopFunction = None

        return AI.SuperAI.Activate(self, active)

    def Tick(self):
        # fire srimech here - allows us to be invertible and use srimech at the same time
        if self.IsUpsideDown():
            for trigger in self.trigger2:
                self.Input(trigger, 0, 1)

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

            # Don't try to fire weapon before it's fully retracted
            if len(targets) > 0 and self.retracting == 0:
                self.didFire = 1
                try:
                    trigger = self.triggerIterator.next()
                except StopIteration:
                    self.triggerIterator = iter(self.triggers)
                    trigger = self.triggerIterator.next()
                self.Input(trigger, 0, 1)

        bReturn = AI.SuperAI.Tick(self)

        # call this now so it takes place after other driving commands
        if self.stopFunction: self.stopFunction(len(targets) > 0)

        return bReturn

    def Stop(self, bTarget):
        if self.didFire == 1:
            self.firing += 1
        if self.firing >= self.fireTime and self.retracting < self.retractTime:
            # stop driving while weapon is retracting
            self.Throttle(0)
            self.retracting += 1
        if self.retracting >= self.retractTime:
            self.firing = 0
            self.retracting = 0
            self.didFire = 0

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

AI.register(Timber2)