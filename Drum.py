from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics

class Drum(AI.SuperAI):
    "When inverted, changes the spinner's direction "
    name = "Drum"

    #Intended for invertible bots (notably drums and invertible face spinners) that should still spin their weapon upwards when inverted.
    #You must use an ANALOG CONTROL to wire your spinner, with Positive axis being the upward spinning direction when your bot isn't inverted.
    #The AI will use the Negative axis when inverted, so your spinner will spin upwards, as it should for good gut ripping capability.
    #Not intended for hybrids, and there is no srimech command.
    #Brought to you by Naryar and ripped off Click's VertSpinner.py.


    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)

        self.spin_range = 30.0

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

        return AI.SuperAI.Activate(self, active)

    def Tick(self):

        # fire weapon
        if self.weapons:

            # spin up depending on enemy's range
            enemy, range = self.GetNearestEnemy()

            if enemy is not None and range < self.spin_range and self.weapons and not self.IsUpsideDown():
                self.Input("Spin", 0, 100)
            elif self.GetInputStatus("Spin", 0) != 0:
                self.Input("Spin", 0, 0)

            if self.IsUpsideDown():
                self.Input("Spin", 0, -100)

            targets = [x for x in self.sensors.itervalues() if x.contacts > 0 \
                and not plus.isDefeated(x.robot)]

        return AI.SuperAI.Tick(self)


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

AI.register(Drum)
