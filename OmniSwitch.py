from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics

class OmniSwitch(AI.SuperAI):
    "OmniSwitch strategy"
    name = "OmniSwitch"

    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)
               
        self.zone = "weapon"
        self.triggers = ["Fire"]
        
        if 'triggers' in args: self.triggers = args['triggers']
        
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
            
            self.RegisterSmartZone(self.zone, 1)
            
        return AI.SuperAI.Activate(self, active)

    def Tick(self):

        self.Input("Spin", 0, 1)

        return AI.SuperAI.Tick(self)

    def InvertHandler(self):
        # fire weapon once per second (until we're upright!)
        while 1:
            for trigger in self.triggers: self.Input(trigger, 0, 1)
            
            for i in range(0, 8):
                yield 0

    def LostComponent(self, id):
        # if we lose all our weapons, stop using the Engage tactic and switch to Shove
        if id in self.weapons: self.weapons.remove(id)
        
        if not self.weapons:
            self.RemoveTactic("Engage")
            
                
            self.tactics.append(Tactics.Shove(self))
            self.tactics.append(Tactics.Charge(self))
            
        return AI.SuperAI.LostComponent(self, id)
        
    def DebugString(self, id, string):
        if self.debug:
            if id == 0: self.debug.get("line0").setText(string)
            elif id == 1: self.debug.get("line1").setText(string)
            elif id == 2: self.debug.get("line2").setText(string)
            elif id == 3: self.debug.get("line3").setText(string)
    
AI.register(OmniSwitch)
