from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics

class SnS_2Invertible(AI.SuperAI):
    "For single-direction sit and spinners with active or static weapons, with improved immobility handling."
    # Uses standard 'LeftRight' control for spinning.  'Spin' button for active weapons.
    ### BINDINGS SETTINGS ###
    # 'range' is the range for active spinning weapons (used for HS hybrids).
    # 'fbs_range' is the range for full-body spinning.
    # 'PreSpinEntrance' is a time at the beginning of the match the AI won't spin, to get further in the arena.
    # 'right' value of 1 makes the full-body spin direction right/clockwise.  Any other value makes it left/counterclockwise.
    # 'chase_time' is the time interval in seconds with no hits after which the AI will stop spinning temporarily and chase down the opponent.
    # 'invertible' spin opposite direction if inverted.
    name = "SnS_2Invertible"
    #Made by Madiaba, edited by apanx


    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)
               
        self.tactics.append(Tactics.Engage(self))
        
        self.spin_range = 50
        self.turn_range = 3

        self.PreSpinEntrance = 0
        if 'PreSpinEntrance' in args: self.PreSpinEntrance = args.get('PreSpinEntrance')
        self.PreSpinEntranceTimer = 0

        self.TimeSinceHit = 0
        self.ChaseTime = 60
        if 'chase_time' in args:
            self.ChaseTime = args.get('chase_time')
        
        if 'range' in args:
            self.spin_range = args.get('range')
        if 'fbs_range' in args:
            self.turn_range = args.get('fbs_range')
        
        self.thwackFunction = self.ThwackLeft
        
        if 'right' in args:
            if args['right'] == "1": self.thwackFunction = self.ThwackRight
            else: self.thwackFunction = self.ThwackLeft
        
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
        else:
            # get rid of reference to self
            self.thwackFunction = None
            
        return AI.SuperAI.Activate(self, active)

    def Tick(self):
        #self.DebugString(4, "self.TimeSinceHit: "+  str(self.TimeSinceHit))

        # Jut out initially.
        if self.PreSpinEntranceTimer < self.PreSpinEntrance:
            self.PreSpinEntranceTimer += 1

        # Count time since last hit
        self.TimeSinceHit = plus.getTimeElapsed() - self.timeOfLastGoodHit

        # define targets
        targets = []
        
        if self.weapons:
            targets = [x for x in self.sensors.itervalues() if x.contacts > 0 \
                and not plus.isDefeated(x.robot)]
                       
        bReturn = AI.SuperAI.Tick(self)
            
        # call this now so it takes place after other driving commands
        if self.thwackFunction: self.thwackFunction(len(targets) > 0)
        
        return bReturn
        
    def ThwackLeft(self, bTarget):
        if self.weapons:

            # spin up depending on enemy's range
            enemy, range = self.GetNearestEnemy()
            
            if enemy is not None and range < self.spin_range:
                self.Input("Spin", 0, 1)
            elif self.GetInputStatus("Spin", 0) != 0:
                self.Input("Spin", 0, 0)

            # Full body spin if we're in range, not immobile, out of our starting spot, and still hitting stuff.
            if enemy is not None and range < self.turn_range and self.bImmobile == False and self.PreSpinEntranceTimer >= self.PreSpinEntrance and self.TimeSinceHit <= self.ChaseTime:
                if self.bInvertible and self.IsUpsideDown(): self.Turn(100)
                else: self.Turn(-100)
            
    def ThwackRight(self, bTarget):
        if self.weapons:

            # spin up depending on enemy's range
            enemy, range = self.GetNearestEnemy()
            
            if enemy is not None and range < self.spin_range:
                self.Input("Spin", 0, 1)
            elif self.GetInputStatus("Spin", 0) != 0:
                self.Input("Spin", 0, 0)

            # Full body spin if we're in range, not immobile, out of our starting spot, and still hitting stuff.
            if enemy is not None and range < self.turn_range and self.bImmobile == False and self.PreSpinEntranceTimer >= self.PreSpinEntrance and self.TimeSinceHit <= self.ChaseTime:
                if self.bInvertible and self.IsUpsideDown(): self.Turn(-100)
                else: self.Turn(100)
            
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
    
AI.register(SnS_2Invertible)
