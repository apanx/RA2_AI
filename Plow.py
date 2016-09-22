from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics

class Plow(AI.SuperAI):
    "Plows opponent!"
    name = "Plow"

    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)

        self.tactics.append(Tactics.Charge(self))
        self.tactics.append(Tactics.Shove(self))

    def Activate(self, active):
        if active:
            if AI.SuperAI.debugging:
                self.debug = Gooey.Plain("watch", 0, 75, 100, 75)
                tbox = self.debug.addText("line0", 0, 0, 100, 15)
                tbox.setText("Throttle")
                tbox = self.debug.addText("line1", 0, 15, 100, 15)
                tbox.setText("Turn")
                tbox = self.debug.addText("line2", 0, 30, 100, 15)
                tbox.setText("")
                tbox = self.debug.addText("line3", 0, 45, 100, 15)
                tbox.setText("")

        return AI.SuperAI.Activate(self, active)


    def LostComponent(self, id):
        # if we lose all our weapons, stop using the Engage tactic and switch to Shove
        if id in self.weapons: self.weapons.remove(id)

        if not self.weapons:
            tactic = [x for x in self.tactics if x.name == "Engage"]
            if len(tactic) > 0:
                self.tactics.remove(tactic[0])

                self.tactics.append(Tactics.Charge(self))
                self.tactics.append(Tactics.Shove(self))

        return AI.SuperAI.LostComponent(self, id)

    def Disable(self,btarget):
        # Disables opponent by charging it at an angle
        # we use a different angle (depending on the size of the opponent!)
        # if target is equal in size, the plow weapon charges are more direct

        if btarget > self: self.Turn(79)
        else: self.Turn(-79)
        if btarget < self: self.Turn(35)
        else: self.Turn(-35)
        if btarget == self: self.Turn(90)
        else: self.Turn(-90)
        if self.target: self.Turn(360)

        return AI.SuperAI.Disable(self, btarget)

AI.register(Plow)
