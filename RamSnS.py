from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics

class RamSnS(AI.SuperAI):
    "Initially rams the opponent, then sit-and-spins continuously. No smartzone required"
    name = "RamSnS"

    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)
        
        self.spin_range = 3.0
        self.InitialRamTimer = 0        

        if 'range' in args: self.spin_range = args.get('range')

#        self.tactics.append(Tactics.Engage(self))
        self.tactics.append(Tactics.Charge(self))

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
#        if self.weapons:
        self.InitialRamTimer += 1        
        if self.InitialRamTimer >= 20:
            self.Input("Forward", 0, 0)
            self.Input("LeftRight", 0, 0)
            self.Input("Spin", 0, 100)
            
        return AI.SuperAI.Tick(self)


    def ImmobilityWarning(self, id, on):
        if on:
            self.Input("Spin", 0, 0)
            self.immobile_list[id] = plus.getTimeElapsed()
        elif id in self.immobile_list:
            self.Input("Spin", 0, 0)
            del self.immobile_list[id]
            
        if id == self.GetID():
            # keep track of our own immobility warning
            self.Input("Spin", 0, 0)
            self.bImmobile = on

        plus.AI.ImmobilityWarning(self, id, on)

    def StuckHandler(self):
        "This default generator is called when the bot is almost immobile."
        while 1:
            self.Input("Spin", 0, 0)
            # back up for 1 second (will stop once we're not immobile)
            for i in range(0, 8):
                self.Input("Spin", 0, 0)
                pos = vector3(self.GetLocation())
                dir = vector3(self.GetDirection())
                self.DriveToLocation((pos - dir * 3).asTuple(), True)
                yield 0
            # go forward for 1 second
            for i in range(0, 8):
                self.Input("Spin", 0, 0)
                pos = vector3(self.GetLocation())
                dir = vector3(self.GetDirection())
                self.DriveToLocation((pos + dir * 3).asTuple())
                yield 0
            self.InitialRamTimer = 1        
        
    def LostComponent(self, id):
        #print "Lost Component!"
        return AI.SuperAI.LostComponent(self, id)


    def DebugString(self, id, string):
        if self.debug:
            if id == 0: self.debug.get("line0").setText(string)
            elif id == 1: self.debug.get("line1").setText(string)
            elif id == 2: self.debug.get("line2").setText(string)
            elif id == 3: self.debug.get("line3").setText(string)

AI.register(RamSnS)
