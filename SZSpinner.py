from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics

class SZSpinner(AI.SuperAI):
    "Like Omni, but does not use a range value for a spinning weapon ; instead uses a smartzone"
    name = "SZSpinner"
    
    #IMPORTANT NOTE: This is a WIP and it might not work properly.
    #Just like said, this is an Omni AI that activates it's spinning weapon via a smartzone (that you need to name "spinner") rather than a range value.
    #For very short spinup time robots (jugglers, drums, face spinners, etc) that only really need to spin their weapons when the opponent is on them.
    #Brought to you by Naryar and inspired by Madiaba's Arrowhead.py.
    
    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)
               
        self.zone = "weapon"
        self.zone1 = "spinner"
        self.triggers = ["Fire"]
        self.trigger2 = ["Srimech"]
        self.reloadTime = 0
        self.reloadDelay = 3
        self.botinzone1 = 0
        
      
        if 'triggers' in args: self.triggers = args['triggers']
        if 'reload' in args: self.reloadDelay = args['reload']
        
        self.triggerIterator = iter(self.triggers)
 
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
            self.RegisterSmartZone(self.zone1, 2)
            
        return AI.SuperAI.Activate(self, active)

    def Tick(self):
        # fire weapon
        if self.weapons:
            # spin up if enemy is in smartzone.
            if self.botinzone1 == 1:
                self.Input("Spin", 0, 100)
            else:
                self.Input("Spin", 0, 0)
            
            
            targets = [x for x in self.sensors.itervalues() if x.contacts > 0 \
                and not plus.isDefeated(x.robot)]
            
            # slight delay between firing
            if self.reloadTime > 0: self.reloadTime -= 1
            
            if len(targets) > 0 and self.reloadTime <= 0:
                try:
                    trigger = self.triggerIterator.next()
                except StopIteration:
                    self.triggerIterator = iter(self.triggers)
                    trigger = self.triggerIterator.next()
                
                self.Input(trigger, 0, 1)
                self.reloadTime = self.reloadDelay
            
        return AI.SuperAI.Tick(self)

    def InvertHandler(self):
        # fire all weapons once per second (until we're upright!)
        while 1:
            for trigger in self.trigger2:
                self.Input(trigger, 0, 1)
            
            for i in range(0, 8):
                yield 0
                
    def LostComponent(self, id):
        # if we lose all our weapons, stop using the Engage tactic and switch to Shove (absolutely worthless, that said)
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
            
AI.register(SZSpinner)
