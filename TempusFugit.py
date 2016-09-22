from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics

class TempusFugit(AI.SuperAI):
    "WHY AM I EVEN BOTHERING TO MAKE CUSTOM AI FOR AN OLD OUTDATED VERSION OF TEMPUS FUGIT."
    #NOTE: You must wire your spinner with an ANALOG CONTROL to work!###
    #NOTE2: When the 'sweapons' specified in Bindings.py break, the bot will become invertible.###
    #So if your bot isn't ever invertible, you must add 'sweapons':(0,) to the Bindings.py!###
    name = "TempusFugit"

    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)
               
        self.zone = "weapon"
        self.triggers = ["Fire"]
        self.trigger2 = ["Srimech"]
        self.reloadTime = 0
        self.reloadDelay = 3
        self.contact = 0
        
        self.spin_range = 3.0
        
        if 'range' in args:
            self.spin_range = args.get('range')
      
        if 'triggers' in args: self.triggers = args['triggers']
        if 'reload' in args: self.reloadDelay = args['reload']
        
        self.triggerIterator = iter(self.triggers)
 
        self.tactics.append(Tactics.Charge(self))
        self.tactics.append(Tactics.Shove(self))
        
    def Activate(self, active):
        if active:
            if AI.SuperAI.debugging:
                self.debug = Gooey.Plain("watch", 10, 175, 250, 175)
                tbox = self.debug.addText("line0", 10, 0, 100, 15)
                tbox.setText("Throttle")
                tbox = self.debug.addText("line1", 10, 15, 100, 15)
                tbox.setText("Turning")
                tbox = self.debug.addText("line2", 10, 30, 100, 15)
                tbox.setText("")
                tbox = self.debug.addText("line3", 10, 45, 100, 15)
                tbox.setText("")
                tbox = self.debug.addText("line4", 10, 60, 250, 15)
                tbox.setText("")
                tbox = self.debug.addText("line5", 10, 75, 250, 15)
                tbox.setText("")
            
            self.RegisterSmartZone(self.zone, 1)
            
        return AI.SuperAI.Activate(self, active)

    def Tick(self):
        #self.DebugString(4, "getContacts: "+  str(len(plus.getContacts(self.GetID()))))
        #self.DebugString(5, "self.contact: "+  str(self.contact))
        # drive inverted
        if not self.sweapons:
            self.bInvertible = True

        # monitor when our wheels leave the ground
        if not 1 in plus.getContacts(self.GetID()):
            self.contact += 1
        else:
            self.contact = 0
            
        # fire weapon
        if self.weapons:

            # spin up depending on enemy's range
            enemy, range = self.GetNearestEnemy()
            
            if enemy is not None and range < self.spin_range and self.weapons and self.contact < 20:
                self.Input("Spin", 0, 100)
                self.Input("Spin2", 0, 0)
            elif self.GetInputStatus("Spin", 0) != 0:
                self.Input("Spin", 0, 0)

            if self.contact >= 20:
                self.Input("Spin", 0, 0)
                self.Input("Spin2", 0, 100)
            
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
        # if we lose all our weapons, stop using the Engage tactic and switch to Shove
        if id in self.weapons: self.weapons.remove(id)
        if id in self.sweapons: self.sweapons.remove(id)
        
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
            elif id == 4: self.debug.get("line4").setText(string)
            elif id == 5: self.debug.get("line5").setText(string)
    
AI.register(TempusFugit)
