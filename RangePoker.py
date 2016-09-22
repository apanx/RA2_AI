from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics

class RangePoker(AI.SuperAI):
    "Poker strategy"
    name = "RangePoker"

    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)
               
        self.zone = "weapon"
        self.triggers = ["Fire"]
        self.reloadTime = 0
        self.reloadDelay = 4
        self.mayFire = True
        self.range = 6 
        self.delta = 0.5 #tolerance between full Aim
        
        if 'triggers' in args: self.triggers = args['triggers']
        if 'reload' in args: self.reloadDelay = args['reload']
        if 'delta' in args: self.delta = args['delta']
        
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
            
        return AI.SuperAI.Activate(self, active)

    def Tick(self):
        # fire weapon
        enemy, range = self.GetNearestEnemy()
                
        if enemy != None :
            # time to move or fire the laser Guided (ser -motor mounted) gun : 
            enemyHead = self.GetHeadingToID(enemy, False)
            if self.debug : 
                self.DebugString(1, "enemyHead : " + str(enemyHead))
                self.DebugString(2, "range : " + str(range))
            if ( enemyHead >= -self.delta and  enemyHead <= self.delta):
                # if range <=  range of the mounted gun 
                # LaserGuided gun aim ennemy : par Saint Georges ! Montjoie ! Saint Denis ! pas de quartier !
                if range <= self.range and self.mayFire : self.Input("Fire", 0, 1)

        return AI.SuperAI.Tick(self)
        

    def InvertHandler(self):
        # fire all weapons once per second (until we're upright!)
        while 1:
            for trigger in self.triggers:
                self.Input(trigger, 0, 1)
            
            for i in range(0, 8):
                yield 0
                
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
    
AI.register(RangePoker)
