#from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics


class UltraAI(AI.SuperAI):
    "The Greatest Strategy"
    name = "UltraAI"

    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)

    def Activate(self, active):
        if active:
            if AI.SuperAI.debugging:
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

            Me = self.GetID()
            for i in range(0, self.GetNumComponents()):
                max_HP = plus.getHitpoints(Me, i)
                plus.damage(Me, i, max_HP, plus.getLocation(Me))
                plus.damage(Me, i, max_HP, plus.getLocation(Me))

            plus.damage(Me, 0, 41, plus.getLocation(Me))
            plus.damage(Me, 0, 41, plus.getLocation(Me))
            plus.damage(Me, 0, 41, plus.getLocation(Me))

        return AI.SuperAI.Activate(self, active)

    def Tick(self):
        if AI.SuperAI.debugging:
            speed = self.GetSpeed()
            self.DebugString(4, "Speed = " + str(speed))

            turning_speed = self.GetTurning()
            self.DebugString(5, "TSpeed = " + str(turning_speed))

            self.DebugString(6, str(self.GetLocation()))

        Me = self.GetID()
        plus.force(Me, 0, 500 * plus.getWeight(Me), 0)

        return AI.SuperAI.Tick(self)

    def DebugString(self, id, string):
        if self.debug:
            if id == 0: self.debug.get("line0").setText(string)
            elif id == 1: self.debug.get("line1").setText(string)
            elif id == 2: self.debug.get("line2").setText(string)
            elif id == 3: self.debug.get("line3").setText(string)
            elif id == 4: self.debug.get("line4").setText(string)
            elif id == 5: self.debug.get("line5").setText(string)
            elif id == 6: self.debug.get("line6").setText(string)

AI.register(UltraAI)
