import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics

class HorzSpinner(AI.SuperAI):
    "Spins!"
    name = "HorzSpinner"

    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)
        
        self.spin_range = 30.0
        self.zone = "weapon"
	self.triggers = ["Fire"]
	self.reloadTime = 0
	self.reloadDelay = 2
	              
        self.triggerIterator = iter(self.triggers)
        if 'range' in args:
            self.spin_range = args.get('range')
        if 'triggers' in args: self.triggers = args['triggers']
        if 'reload' in args: self.reloadDelay = args['reload']
        self.tactics.append(Tactics.Engage(self))

    def Activate(self, active):
        if active:
            #if AI.SuperAI.debugging:
                self.debug = Gooey.Plain("watch", 0, 75, 200, 105)
                tbox = self.debug.addText("line0", 0, 0, 200, 15)
                tbox.setText("Throttle")
                tbox = self.debug.addText("line1", 0, 15, 200, 15)
                tbox.setText("Turning")
                tbox = self.debug.addText("line2", 0, 30, 200, 15)
                tbox.setText("")
                tbox = self.debug.addText("line3", 0, 45, 200, 15)
                tbox.setText("")
                tbox = self.debug.addText("line4", 0, 60, 200, 15)
                tbox.setText("")       
                tbox = self.debug.addText("line5", 0, 75, 200, 15)
                tbox.setText("")  
                tbox = self.debug.addText("line6", 0, 90, 200, 15)
                tbox.setText("")  
                self.RegisterSmartZone(self.zone, 1)
        return AI.SuperAI.Activate(self, active)

    def Tick(self):
        if self.weapons:
            # spin up depending on enemy's range
            enemy, range = self.GetNearestEnemy()
            
            if enemy is not None and range < self.spin_range and not self.IsUpsideDown():
                self.Input("Spin", 0, 1)
                self.DebugString(6, "Spinning") 
            elif self.GetInputStatus("Spin", 0) != 0:
                self.Input("Spin", 0, 0)
	        self.DebugString(6, "Stopped")
	        
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
        # Wait 10 seconds for disc to stop spining then fire SRM once per three seconds (until we're upright!)
        self.DebugString(6, "Waiting")         
        for i in range(0, 80):
                yield 0
        while 1:
            self.Input("SRM", 0, 1)
            self.DebugString(6, "SRM") 
            
            for i in range(0, 24):
                yield 0

    def RobotInRange(self, robot_id):
        "Return tuple of (part-of-robot-in-range, chassis-in-range)"
        # GetLastDamage returns:  component damaged, amount, at time, by player, by component
        range = self.GetDistanceToID(robot_id)
        if range < self.spin_range:
            damage = self.GetLastDamageReceived()
            if damage[3] == robot_id and (plus.getTimeElapsed() - damage[2] < 1.0):
                return (True, True)
                
        return (False, False)
        
    def LostComponent(self, id):
        #print "Lost Component!"
        return AI.SuperAI.LostComponent(self, id)

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
        #if self.debug:
            if id == 0: self.debug.get("line0").setText(string)
            elif id == 1: self.debug.get("line1").setText(string)
            elif id == 2: self.debug.get("line2").setText(string)
            elif id == 3: self.debug.get("line3").setText(string)
            elif id == 4: self.debug.get("line4").setText(string)
            elif id == 5: self.debug.get("line5").setText(string)
            elif id == 6: self.debug.get("line6").setText(string)
AI.register(HorzSpinner)