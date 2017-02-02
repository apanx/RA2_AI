from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics
from Flipper2 import *

class Forklift(Flipper2):
    "Forklift strategy"
    name = "Forklift"

    def __init__(self, **args):
        Flipper2.__init__(self, **args)
        self.zone = "lift"
        self.trigger = "Lift"
        self.linacus = [1, 2]
        '''
        Stock
        60cm -0.45
        80cm -0.6
        100cm -0.8
        120cm -0.95

        DSL 2.2
        80 cm = -0.3
        100 cm = -0.5
        120 cm = -0.7
        '''
        self.linacuslength = [-0.95, -0.8, -0.6, -0.45]
        if 'LinAcus' in args: self.linacus = args.get('LinAcus')
        if 'LinAcusLength' in args: self.linacuslength = args.get('LinAcusLength')

    def Activate(self, active):
        if active:
            if AI.SuperAI.debugging:
                self.debug = Gooey.Plain("watch", 0, 150, 250, 165)
                tbox = self.debug.addText("line0", 0, 0, 250, 15)
                tbox.setText("Throttle")
                tbox = self.debug.addText("line1", 0, 15, 250, 15)
                tbox.setText("Turning")
                tbox = self.debug.addText("line2", 0, 30, 250, 15)
                tbox.setText("")
                tbox = self.debug.addText("line3", 0, 45, 250, 15)
                tbox.setText("")
                tbox = self.debug.addText("line4", 0, 60, 250, 15)
                tbox.setText("")
                tbox = self.debug.addText("line5", 0, 75, 250, 15)
                tbox.setText("")
                tbox = self.debug.addText("line6", 0, 90, 250, 15)
                tbox.setText("")
                tbox = self.debug.addText("line7", 0, 105, 250, 15)
                tbox.setText("")
                tbox = self.debug.addText("line8", 0, 120, 250, 15)
                tbox.setText("")
                tbox = self.debug.addText("line9", 0, 135, 250, 15)
                tbox.setText("")

            self.RegisterSmartZone(self.zone, 1)

        return AI.SuperAI.Activate(self, active)

    def Tick(self):


        bReturn = Flipper2.Tick(self)
        enemy, range = self.GetNearestEnemy()
        if self.weapons:
            fire = False

            if enemy is not None:
                if self.flip == 1 and self.CanDriveUpsideDown(enemy):
                    fire = True
            self.DebugString(4, str(fire))
            n = 0
            for linacu in self.linacus:
                self.DebugString(6, str(self.GetPistonPosition(linacu)))
                if fire:
                    if self.GetPistonPosition(linacu) > self.linacuslength[n]:
                        self.Input(self.trigger + str(n), 0, 100)
                        self.Input(self.trigger + str(n), 1, 0)
                        self.DebugString(7, "Lift")
                    else:
                        self.Input(self.trigger + str(n), 0, 0)
                        self.DebugString(7, "Stop")
                else:
                    if self.GetPistonPosition(linacu) < -0.05:
                        self.Input(self.trigger + str(n), 1, -100)
                        self.Input(self.trigger + str(n), 0, 0)
                        self.DebugString(7, "Descend")
                    else:
                        self.Input(self.trigger + str(n), 1, 0)
                        self.DebugString(7, "Stop")
                n += 1

        self.DebugString(5, str(self.GetInputStatus(self.trigger, 0)) + " " + str(self.GetInputStatus(self.trigger, 1)))
        return bReturn

    def DebugString(self, id, string):
        if self.debug:
            if id == 0: self.debug.get("line0").setText(string)
            elif id == 1: self.debug.get("line1").setText(string)
            elif id == 2: self.debug.get("line2").setText(string)
            elif id == 3: self.debug.get("line3").setText(string)
            elif id == 4: self.debug.get("line4").setText(string)
            elif id == 5: self.debug.get("line5").setText(string)
            elif id == 6: self.debug.get("line6").setText(string)
            elif id == 7: self.debug.get("line7").setText(string)
            elif id == 8: self.debug.get("line8").setText(string)
            elif id == 9: self.debug.get("line9").setText(string)

AI.register(Forklift)
