from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics

class Frenzy(AI.SuperAI):
    "Hammer strategy"
	#Somehow like Whipper.py but is intended for special use on spin motor hammers (the only legal one being the geared Beta burst)
	#Self-rights with the hammer.
	#Note: To use only if the hammer uses spin motors, and it is NOT compatible with other weapons.
	#Use normal bindings, and wire the hammer with an analog control named "Hammer"
    
    name = "Frenzy"

    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)
               
        self.zone = "weapon"
                
        self.tactics.append(Tactics.Engage(self))
        
        self.whipTimer = 0
        self.whipDir = 1
        self.whipDirCount = 4
        
        self.whipFunction = self.WhipBackAndForth
        
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
        else:
            # get rid of reference to self
            self.whipFunction = None
            
        return AI.SuperAI.Activate(self, active)

    def Tick(self):
        # fire weapon
        targets = []
        
        if self.weapons:
            targets = [x for x in self.sensors.itervalues() if x.contacts > 0 \
                and not plus.isDefeated(x.robot)]
                       
        bReturn = AI.SuperAI.Tick(self)
            
        # call this now so it takes place after other driving commands
        if self.whipFunction: self.whipFunction(len(targets) > 0)
        
        return bReturn
        
    def InvertHandler(self):
        # fire weapon once per second (until we're upright!)
        while 1:
            if self.whipDir > 0:
                self.Input("Hammer", 0, -100)
            else:
                self.Input("Hammer", 0, 100)

            self.whipDirCount -= 1
            if self.whipDirCount < 0:
                self.whipDirCount = 4
                self.whipDir = -self.whipDir
            
            self.whipTimer -= 1
            
            for i in range(0, 8):
                yield 0

    def WhipBackAndForth(self, bTarget):
        if bTarget: self.whipTimer = 8
        
        if self.whipTimer > 0:
            # Whip back and forth!
            if self.whipDir > 0:
                self.Input("Hammer", 0, -100)
            else:
                self.Input("Hammer", 0, 100)
            self.Throttle(0)
            
            self.whipDirCount -= 1
            if self.whipDirCount < 0:
                self.whipDirCount = 4
                self.whipDir = -self.whipDir
            
            self.whipTimer -= 1
            
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
            
    def SmartZoneEvent(self, direction, id, robot, chassis):
        if id == 1:
            if robot == 0:
                self.Input("Hammer", 0, -100)
            elif robot > 0:
                if direction == 1:
                    AI.SuperAI.SmartZoneEvent(self, direction, id, robot, chassis)
                    
        return True
        
AI.register(Frenzy)
