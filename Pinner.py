from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics

class Pinner(AI.SuperAI):
    "Pushes without backing up"
    name = "Pinner"
    # Designed for true pushers, though does NOT back up repeatedly like Pusher.py does.
    # In-built average Throttle, Topspeed, Turn and Turnspeed values for easier AI-ing. Also invertible.
    # Brought to you by Naryar
    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)

        self.tactics.append(Tactics.Engage(self))
        self.max_Throttle = 130
        self.top_speed = 99
        self.bInvertible = True
        self.max_turn = 40
        self.max_turn_speed = 3

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

    def LostComponent(self, id):
        #print "Lost Component!"
        return AI.SuperAI.LostComponent(self, id)

    def DebugString(self, id, string):
        if self.debug:
            if id == 0: self.debug.get("line0").setText(string)
            elif id == 1: self.debug.get("line1").setText(string)
            elif id == 2: self.debug.get("line2").setText(string)
            elif id == 3: self.debug.get("line3").setText(string)

AI.register(Pinner)
