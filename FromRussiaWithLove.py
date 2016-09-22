from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics

class FRWL(AI.SuperAI):
    "The Clamp/Spin AI for From Russia With Love!"
    name = "FRWL"

    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)

        self.tactics.append(Tactics.Charge(self))
        self.tactics.append(Tactics.Shove(self))

        self.spin_range = 3.0

        if 'range' in args:
            self.spin_range = args.get('range')

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

            self.RegisterSmartZone("squeeze", 1)

        return AI.SuperAI.Activate(self, active)

    def Tick(self):
        targets = [x for x in self.sensors.itervalues() if x.contacts > 0]
        if len(targets) > 0:
            self.Input("Clamp", 0, 100)
        else:
            self.Input("Clamp", 0, 0)

        if self.weapons:
            # spin up depending on enemy's range
            enemy, range = self.GetNearestEnemy()

            if enemy is not None and range < self.spin_range:
                self.Input("Spin", 0, 1)
            elif self.GetInputStatus("Spin", 0) != 0:
                self.Input("Spin", 0, 0)

        return AI.SuperAI.Tick(self)

    def RobotInRange(self, robot_id):
        "Return tuple of (part-of-robot-in-range, chassis-in-range)"
        # GetLastDamage returns:  component damaged, amount, at time, by player, by component
        range = self.GetDistanceToID(robot_id)
        if range < self.spin_range:
            damage = self.GetLastDamageReceived()
            if damage[3] == robot_id and (plus.getTimeElapsed() - damage[2] < 1.0):
                return (True, True)

        return (False, False)

    def LostComponent(self, id):
        #print "Lost Component!"
        return AI.SuperAI.LostComponent(self, id)

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


AI.register(FRWL)
