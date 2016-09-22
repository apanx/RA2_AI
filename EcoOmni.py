from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics

class EcoOmni(AI.SuperAI):
    "Energy-efficient, environmentally friendly, 100% organic (okay maybe not that last) Omni."
    name = "EcoOmni"
    # Has the option of using a smart zone for spinner activation.  Name this zone "spin" and then put 'UseSpinZone':1 in Bindings.  Set 'range' to something high like 99.
    # 'StartSpinup' is the time at the beginning of the match for which the AI should spin its weapons, to get them going.  Measured in seconds.  Default is 2.  Some bots can't move unless this is greater than 0.
    # Has the option for pulsing a spinner, rather than running it constantly, if the enemy is outside of a certain range.  Good for shell spinners that can't drive straight when the weapon is running.
    # 'Pulse' is the number of ticks the active weapon should stay on PLUS the number of ticks it stays off.  A tick is 1/8 second.
    # 'Coast' is the number of ticks the active weapon should turn off and coast for.  This should be less than the Pulse value.  For equal times on/off, set Coast equal to half of Pulse.
    # 'PulseRange' is the range within which the weapon should spin constantly.  A 0 value makes it always pulse.

    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)
               
        self.zone = "weapon"
        self.zone2 = "spin"
        self.zone3 = "weapon2"
        self.triggers = ["Fire"]
        self.trigger2 = ["Srimech"]
        self.reloadTime = 0
        self.reloadDelay = 3
        self.goodFunction = self.GoodStuckHandler
        self.wiggletimer = -8
        self.srimechtimer = 0
        self.srispintimer = 0
        self.botinzone1 = 0
        self.botinzone2 = 0
        self.botinzone3 = 0
        self.usespinzone = 0
        if 'UseSpinZone' in args: self.usespinzone = args.get('UseSpinZone')
        
        self.spin_range = 3.0
        
        if 'range' in args:
            self.spin_range = args.get('range')
      
        if 'triggers' in args: self.triggers = args['triggers']
        if 'reload' in args: self.reloadDelay = args['reload']
        
        self.pulsetime = 0
        if 'Pulse' in args: self.pulsetime = args.get('Pulse')
        self.pulse = self.pulsetime
        self.pulsetime2 = self.pulsetime/2
        if 'Coast' in args: self.pulsetime2 = args.get('Coast')
        self.pulse_range = 0
        if 'PulseRange' in args: self.pulse_range = args.get('PulseRange')
        self.spinup = 2
        if 'StartSpinup' in args: self.spinup = args.get('StartSpinup')
        
        self.triggerIterator = iter(self.triggers)
 
        self.tactics.append(Tactics.Engage(self))
        
    def Activate(self, active):
        if active:
            if AI.SuperAI.debugging:
                self.debug = Gooey.Plain("watch", 0, 75, 512, 75)
                tbox = self.debug.addText("line0", 0, 0, 100, 15)
                tbox.setText("Throttle")
                tbox = self.debug.addText("line1", 0, 15, 100, 15)
                tbox.setText("Turning")
                tbox = self.debug.addText("line2", 0, 30, 100, 15)
                tbox.setText("")
                tbox = self.debug.addText("line3", 0, 45, 100, 15)
                tbox.setText("")
                tbox = self.debug.addText("line4", 10, 60, 512, 15)
                tbox.setText("")
            
            self.RegisterSmartZone(self.zone, 1)
            self.RegisterSmartZone(self.zone2, 2)
            self.RegisterSmartZone(self.zone3, 3)
            
        else:
            # get rid of reference to self
            self.goodFunction = None
            
        return AI.SuperAI.Activate(self, active)

    def Tick(self):
        #self.DebugString(4, str(self.zone2))
        # spin weapons briefly at start because for some dumb reason we can't move otherwise.
        if plus.getTimeElapsed() <= self.spinup:
            self.Input("Spin", 0, 100)
                
        # spin up depending on enemy's range
        enemy, range = self.GetNearestEnemy()
        if enemy is not None:
            heading = self.GetHeadingToID(enemy, False)
        
        # spin weapons only when necessary, and don't waste battery on them when we're being counted out!
        if enemy is not None and self.weapons and range < self.spin_range and not self.bImmobile and (self.botinzone2 == 1 or self.usespinzone == 0):
            if self.pulsetime > 0 and range > self.pulse_range:
                # Pulse spinner
                self.pulse -= 1
                if self.pulsetime2 < self.pulse < self.pulsetime:
                    self.Input("Spin", 0, 100)
                if 0 < self.pulse < self.pulsetime2:
                    self.Input("Spin", 0, 0)
                if self.pulse <= 0:
                    self.pulse = self.pulsetime
            else:
                self.Input("Spin", 0, 100)
        else:
            if plus.getTimeElapsed() > self.spinup:
                self.Input("Spin", 0, 0)
        
        targets = [x for x in self.sensors.itervalues() if x.contacts > 0 \
            and not plus.isDefeated(x.robot)]
        
        # slight delay between firing
        if self.reloadTime > 0: self.reloadTime -= 1
        
        if self.botinzone1 == 1 and self.reloadTime <= 0:
            try:
                trigger = self.triggerIterator.next()
            except StopIteration:
                self.triggerIterator = iter(self.triggers)
                trigger = self.triggerIterator.next()
            
            self.Input(trigger, 0, 1)
            self.reloadTime = self.reloadDelay
            
        if self.botinzone3 == 1:
            self.Input("Fire2", 0, 1)
            
        bReturn = AI.SuperAI.Tick(self)
            
        # call this now so it takes place after other driving commands
        if self.goodFunction: self.goodFunction(len(targets) > 0)
        
        return bReturn

    def InvertHandler(self):
        # fire all weapons once per second (until we're upright!)
        while 1:
            for trigger in self.trigger2:
                self.Input(trigger, 0, 1)
            
            for i in range(0, 8):
                yield 0
                
    def StuckHandler(self):
        "Do nothing because the GoodStuckHandler function is better."
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
                self.Input("Fire2", 0, 1)
                if self.srispintimer < 7:
                    self.Input("Spin", 0, -100)
                if self.srispintimer >= 7:
                    self.Input("Spin", 0, 100)
                if self.srispintimer == 15:
                    self.srispintimer = 0
        else:
            self.srimechtimer = 0
            self.srispintimer = 0
            self.wiggletimer = -8
                
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
            elif id == 4: self.debug.get("line4").setText(string)
            
    def SmartZoneEvent(self, direction, id, robot, chassis):
        if id == 1:
            if robot > 0:
                if direction == 1:
                    self.botinzone1 = 1
                if direction == -1:
                    self.botinzone1 = 0
        elif id == 2:
            if robot > 0:
                if direction == 1:
                    self.botinzone2 = 1
                if direction == -1:
                    self.botinzone2 = 0
        elif id == 3:
            if robot > 0:
                if direction == 1:
                    self.botinzone3 = 1
                if direction == -1:
                    self.botinzone3 = 0
        return True
    
AI.register(EcoOmni)
