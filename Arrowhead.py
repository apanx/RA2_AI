from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics

class Arrowhead(AI.SuperAI):
    "Spinner AI that backs up if the opponent gets under it."
    name = "Arrowhead"

    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)

        self.zone1 = "Zone1"
        self.zone2 = "Zone2"
        self.triggers2 = ["Srimech"]
        self.botinzone1 = 0
        self.botinzone2 = 0
        self.backupFunction = self.Backup

        self.spin_range = 3.0

        if 'range' in args:
            self.spin_range = args.get('range')

        if 'zone1' in args: self.zone1 = args['zone1']
        if 'zone2' in args: self.zone2 = args['zone2']

        if 'srimech' in args: self.triggers2 = args['srimech']

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
        else:
            # get rid of reference to self
            self.backupFunction = None

        return AI.SuperAI.Activate(self, active)

    def Tick(self):
        # fire weapon
        targets = []
        targets = [x for x in self.sensors.itervalues() if x.contacts > 0 \
                and not plus.isDefeated(x.robot)]

        if self.weapons:
            # spin up depending on enemy's range
            enemy, range = self.GetNearestEnemy()

            if enemy is not None and range < self.spin_range:
                self.Input("Spin", 0, 1)
            elif self.GetInputStatus("Spin", 0) != 0:
                self.Input("Spin", 0, 0)

        bReturn = AI.SuperAI.Tick(self)

        # call this now so it takes place after other driving commands
        if self.backupFunction: self.backupFunction(len(targets) > 0)

        return bReturn

    def Backup(self, bTarget):
        # back up if a bot gets under us
        if self.botinzone1 == 1:
            self.Throttle(0)
            self.Input("Fire1", 0, 100)
        else:
            self.Input("Fire1", 0, 0)

        if self.botinzone2 == 1:
            self.Throttle(0)
            self.Input("Fire2", 0, 100)
        else:
            self.Input("Fire2", 0, 0)

    def InvertHandler(self):
        # fire all weapons once per second (until we're upright!)
        while 1:
            for trigger in self.triggers2:
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
                    self.botinzone1 = 1
                if direction == -1:
                    self.botinzone1 = 0
        elif id == 2:
            if robot > 0:
                if direction == 1:
                    self.botinzone2 = 1
                if direction == -1:
                    self.botinzone2 = 0
        return True

AI.register(Arrowhead)