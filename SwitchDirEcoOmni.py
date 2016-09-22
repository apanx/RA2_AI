from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics

class SwitchDirEcoOmni(AI.SuperAI):
    "EcoOmni that turns around and drives backward after the primary weapons break."
    name = "SwitchDirEcoOmni"

    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)
               
        self.zone = "weapon"
        self.triggers = ["Fire"]
        self.trigger2 = ["Srimech"]
        self.reloadTime = 0
        self.reloadDelay = 3
        self.goodFunction = self.GoodStuckHandler
        self.wiggletimer = -8
        self.srimechtimer = 0
        self.srispintimer = 0
        
        self.spin_range = 3.0
        
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
            
            self.RegisterSmartZone(self.zone, 1)
            
        else:
            # get rid of reference to self
            self.goodFunction = None
            
        return AI.SuperAI.Activate(self, active)

    def Tick(self):
        # spin weapons briefly at start because for some dumb reason we can't move otherwise.
        if plus.getTimeElapsed() <= 2:
            self.Input("Spin1", 0, 100)
                
        # spin up depending on enemy's range
        enemy, range = self.GetNearestEnemy()
        
        # spin weapons only when necessary, and don't waste battery on them when we're being counted out!
        if self.weapons:
            if enemy is not None and range < self.spin_range and not self.bImmobile:
                self.Input("Spin1", 0, 100)
            else:
                if plus.getTimeElapsed() > 2:
                    self.Input("Spin1", 0, 0)
                
        if not self.weapons:
            self.Input("Spin1", 0, 0)
            if enemy is not None and range < self.spin_range and not self.bImmobile:
                self.Input("Spin2", 0, 100)
            else:
                self.Input("Spin2", 0, 0)
        
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
            
        bReturn = AI.SuperAI.Tick(self)
            
        # call this now so it takes place after other driving commands
        if self.goodFunction: self.goodFunction(len(targets) > 0)
        
        return bReturn
        
    def Throttle(self, throttle):
        # if we're car steering and we're not moving much, throttle up
        if self.bCarSteering and self.last_turn_throttle != 0:
            speed = self.GetSpeed()
            if speed > 0 and speed < self.top_speed / 3: throttle = self.last_throttle + 10
            elif speed < 0 and speed > -self.top_speed / 3: throttle = self.last_throttle - 10

        throttle = min(max(throttle, -100), 100)

        if self.bInvertible and self.IsUpsideDown(): throttle = -throttle
        #reverse throttle if weapons break
        if not self.weapons: throttle = -throttle

        self.set_throttle = throttle
        self.Input('Forward', 0, throttle)
        self.DebugString(0, "Throttle = " + str(int(throttle)))
        
    def Turn(self, turning):
        turning = min(max(turning, -100), 100)

        if self.bInvertible and self.IsUpsideDown(): turning = -turning
        #reverse turning if weapons break
        if not self.weapons: turning = -turning

        self.set_turn_throttle = turning
        self.Input('LeftRight', 0, -turning)
        self.Input('LeftRight', 1, turning)
        self.DebugString(1, "Turning = " + str(int(turning)))

    def InvertHandler(self):
        # fire all weapons once per second (until we're upright!)
        while 1:
            for trigger in self.trigger2:
                self.Input(trigger, 0, 1)
            
            for i in range(0, 8):
                yield 0
                
    def StuckHandler(self):
        "Do nothing because this is a STUPID IDIOT FUNCTION THAT WON'T LET YOU DO A GET SPEED."
        while 1:
            for i in range(0, 16):
                yield 0
                
    def GoodStuckHandler(self, bTarget):
        if self.bImmobile:
            self.srimechtimer += 1
            # keep driving in one direction as long as we can
            if self.GetSpeed() > 0.5:
                self.Throttle(100)
            if self.GetSpeed() < -0.5:
                self.Throttle(-100)
            # if we're not moving very fast try wiggling back and forth
            if abs(self.GetSpeed()) <= 0.5:
                self.wiggletimer += 1
                if self.wiggletimer < 0:
                    self.Throttle(100)
                if self.wiggletimer >= 0:
                    self.Throttle(-100)
                if self.wiggletimer >= 8:
                    self.wiggletimer = -8
            # fire everything we have as a last-ditch effort if we're still not free after 5 seconds
            if self.srimechtimer >= 20:
                self.srispintimer += 1
                for trigger in self.triggers:
                    self.Input(trigger, 0, 1)
                for trigger in self.trigger2:
                    self.Input(trigger, 0, 1)
                if self.srispintimer < 7:
                    self.Input("Spin1", 0, -100)
                    self.Input("Spin2", 0, -100)
                if self.srispintimer >= 7:
                    self.Input("Spin1", 0, 100)
                    self.Input("Spin2", 0, 100)
                if self.srispintimer == 15:
                    self.srispintimer = 0
        else:
            self.srimechtimer = 0
            self.srispintimer = 0
            self.wiggletimer = -8
                
    def LostComponent(self, id):
        # if we lose all our weapons, ignore it because ram tactics in reverse don't work well.
        if id in self.weapons: self.weapons.remove(id)
            
        return AI.SuperAI.LostComponent(self, id)
                
    def DebugString(self, id, string):
        if self.debug:
            if id == 0: self.debug.get("line0").setText(string)
            elif id == 1: self.debug.get("line1").setText(string)
            elif id == 2: self.debug.get("line2").setText(string)
            elif id == 3: self.debug.get("line3").setText(string)
    
AI.register(SwitchDirEcoOmni)
