from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics

class PusherPiston(AI.SuperAI):
    "Pushes! with the help of pistons"
    name = "PusherPiston"

    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)
        self.zone = "weapon"
        self.triggers = ["Fire"]
        self.reloadTime = 0
        self.reloadDelay = 3        
        self.triggerIterator = iter(self.triggers)
        self.tactics.append(Tactics.Charge(self))
        self.tactics.append(Tactics.Shove(self))


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
 
    def LostComponent(self, id):
        #print "Lost Component!"
        return AI.SuperAI.LostComponent(self, id)

    def DebugString(self, id, string):
        if self.debug:
            if id == 0: self.debug.get("line0").setText(string)
            elif id == 1: self.debug.get("line1").setText(string)
            elif id == 2: self.debug.get("line2").setText(string)
            elif id == 3: self.debug.get("line3").setText(string)

    def SmartZoneEvent(self, direction, id, robot, chassis):
        if id == 1:
            if direction == 1:
                self.Input("Fire", 0, 100)
                AI.SuperAI.SmartZoneEvent(self, direction, id, robot, chassis)

        return True
            
AI.register(PusherPiston)
