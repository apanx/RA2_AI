from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics

class VertSpinner(AI.SuperAI):
    "Self-rights by reversing the spinner direction and firing additional optional srimech."
    ###NOTE: You must wire your spinner with an ANALOG CONTROL to work!###
    ###NOTE2: When the 'sweapons' specified in Bindings.py break, the bot will become invertible.###
    ###So if your bot isn't ever invertible, you must add 'sweapons':(0,) to the Bindings.py!###
    #Update 5/31/11: added analog control for self righting ("Sriturn")
    #Update 6/29/12: added customizable feature 'TrollDanceZone'.  This makes the AI spin weapons in reverse for a longer time when self-righting, to avoid "Troll Dancing".  Set to a number between 0 and 1; lower numbers make the weapons spin in reverse for longer.  Default value is 1.
    name = "VertSpinner"

    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)
               
        self.zone = "weapon"
        self.triggers = ["Fire"]
        self.trigger2 = ["Srimech"]
        self.reloadTime = 0
        self.reloadDelay = 3
        
        self.spin_range = 3.0
        
        self.troll = 1
        if 'TrollDanceZone' in args: self.troll = args['TrollDanceZone']
        
        if 'range' in args:
            self.spin_range = args.get('range')
      
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
            #self.tauntbox = Gooey.Plain("taunt", 10, 175, 640, 175)
            #tbox = self.tauntbox.addText("taunt1", 10, 0, 640, 15)
            #tbox.setText("")
            
            self.RegisterSmartZone(self.zone, 1)
            
        return AI.SuperAI.Activate(self, active)

    def Tick(self):
        #self.tauntbox.get("taunt1").setText(str(list(plus.getDirection(self.GetID(),0))[1]))
        # drive inverted
        if not self.sweapons:
            self.bInvertible = True
        else:
            if self.IsUpsideDown():
                self.Input("Sriturn", 0, 100)
            else:
                self.Input("Sriturn", 0, 0)

        # spin up depending on enemy's range
        enemy, range = self.GetNearestEnemy()
        
        if enemy is not None and range < self.spin_range and self.weapons and abs(list(plus.getDirection(self.GetID(),0))[1]) < self.troll and not self.IsUpsideDown():
            self.Input("Spin", 0, 100)
        else:
            self.Input("Spin", 0, 0)
                
        # fire weapon
        if self.weapons:

            if self.IsUpsideDown() or abs(list(plus.getDirection(self.GetID(),0))[1]) > self.troll:
                self.Input("Spin", 0, -100)
            
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
    
AI.register(VertSpinner)
