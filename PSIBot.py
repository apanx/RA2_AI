#from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics


class PSIBot(AI.SuperAI):
    "PSIBot strategy"
    name = "PSIBot"

    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)
        #self.tactics.append(Tactics.Flee(self))

    def Activate(self, active):
        plus.damage(1, 0, 50000, plus.getLocation(1))
        plus.damage(1, 0, 50000, plus.getLocation(1))
        plus.damage(1, 0, 50000, plus.getLocation(1))
        if active:
            #if AI.SuperAI.debugging:
                self.debug = Gooey.Plain("watch", 0, 75, 200, 105)
                tbox = self.debug.addText("line0", 0, 0, 200, 15)
                tbox.setText("Throttle")
                tbox = self.debug.addText("line1", 0, 15, 200, 15)
                tbox.setText("Turning")
                tbox = self.debug.addText("line2", 0, 30, 200, 15)
                tbox.setText("")
                tbox = self.debug.addText("line3", 0, 45, 200, 15)
                tbox.setText("")
                tbox = self.debug.addText("line4", 0, 60, 200, 15)
                tbox.setText("")
                tbox = self.debug.addText("line5", 0, 75, 200, 15)
                tbox.setText("")
                tbox = self.debug.addText("line6", 0, 90, 200, 15)
                tbox.setText("")


        return AI.SuperAI.Activate(self, active)

    def Tick(self):
        Me = self.GetID()
        plus.force(Me, 0, 85 * plus.getWeight(Me), 0)
        self.DebugString(6, str(self.GetLocation()))
        return AI.SuperAI.Tick(self)


    def DebugString(self, id, string):
        #if self.debug:
            if id == 0: self.debug.get("line0").setText(string)
            elif id == 1: self.debug.get("line1").setText(string)
            elif id == 2: self.debug.get("line2").setText(string)
            elif id == 3: self.debug.get("line3").setText(string)
            elif id == 4: self.debug.get("line4").setText(string)
            elif id == 5: self.debug.get("line5").setText(string)
            elif id == 6: self.debug.get("line6").setText(string)

AI.register(PSIBot)
