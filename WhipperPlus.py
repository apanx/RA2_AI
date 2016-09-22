from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics

class WhipperPlus(AI.SuperAI):
    "WhipperPlus strategy Whipper + FBS immobility management"
    name = "WhipperPlus"

    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)
               
        self.zone = "whipzone"
                
        self.tactics.append(Tactics.Engage(self))
        
        self.whipTimer = 0
        self.whipDir = 1
        self.whipDirCount = 2

        self.ImmobileCounter = 0
        self.ThisAI_bImmobile = 0
        self.BU_ImmobileTimer_A = 0        
        self.BU_ImmobileTimer_B = 0 
        self.ReMobilizeRoutineTime = 40
        self.ThisAIBot_XFactorA = 0
        self.ThisAIBot_ZFactorA = 0
        self.ThisAIBot_XFactorB = 0
        self.ThisAIBot_ZFactorB = 0
        
        self.whipFunction = self.WhipAround
        
        if 'zone' in args: self.zone = args['zone']
        
        if 'whip' in args:
            if args['whip'] !=  "around": self.whipFunction = self.WhipBackAndForth
        
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
        if self.whipFunction and self.ThisAI_bImmobile == 0: self.whipFunction(len(targets) > 0)
		
        if self.ThisAI_bImmobile == 1: # If Immobility is on:  -------------------------------------
            self.ImmobileCounter += 1  # Then start counting....
            
            if self.ImmobileCounter >= self.ReMobilizeRoutineTime*0.2:   # go backward for a designated time.    
                self.Throttle(100)
                self.Input("LeftRight", 0, 0)
                self.Input("Forward", 0, -100)
            
            if self.ImmobileCounter >= self.ReMobilizeRoutineTime*0.6:  # go forward for a designated time.    
                self.Input("LeftRight", 0, 0)
                self.Throttle(100)
                self.Input("Forward", 0, 100)

            if self.ImmobileCounter >= self.ReMobilizeRoutineTime:  # Reset everything:    
                self.ThisAI_bImmobile = 0 # default Reset (if timer goes too long).
                self.ImmobileCounter = 1
        else:
            self.ThisAI_bImmobile = 0
            self.ImmobileCounter = 0     



        # BackUp Immobile routine (continually running).... calculate difference of position between 2 calls
        self.BU_ImmobileTimer_A +=1        
        if self.BU_ImmobileTimer_A >= 1:        
            self.ThisAIBot_XFactorA =  plus.getLocation(self.GetID())[0] # 
            self.ThisAIBot_ZFactorA =  plus.getLocation(self.GetID())[2]
        if self.BU_ImmobileTimer_A == 16:        
            self.ThisAIBot_XFactorB =  plus.getLocation(self.GetID())[0] 
            self.ThisAIBot_ZFactorB =  plus.getLocation(self.GetID())[2]
            self.BU_ImmobileTimer_A = 0 # Reset.       

        if   self.ThisAIBot_XFactorA > self.ThisAIBot_XFactorB - .07 and   self.ThisAIBot_XFactorA < self.ThisAIBot_XFactorB + .07 and    self.ThisAIBot_ZFactorA > self.ThisAIBot_ZFactorB - .07 and   self.ThisAIBot_ZFactorA < self.ThisAIBot_ZFactorB + .07:
            self.BU_ImmobileTimer_B +=1       
            if self.BU_ImmobileTimer_B ==50:       
                self.ThisAI_bImmobile = 1
                self.BU_ImmobileTimer_B = 0
        else:
            self.BU_ImmobileTimer_B = 0 # Reset
        
        return bReturn
        
    def WhipBackAndForth(self, bTarget):
        if bTarget and self.whipTimer == 0: self.whipTimer = 4
        
        if self.whipTimer > 0:
            # Whip back and forth!
            if self.whipDir > 0: self.Turn(100)
            else: self.Turn(-100)
            self.Throttle(0)
            
            self.whipDirCount -= 1
            if self.whipDirCount < 0:
                self.whipDirCount = 2
                self.whipDir = -self.whipDir
            
            self.whipTimer -= 1
            
    def WhipAround(self, bTarget):
        if bTarget and self.whipTimer == 0: self.whipTimer = 4
        elif self.whipTimer == 0: 
            self.whipDir = -self.whipDir
            if bTarget: self.ThisAI_bImmobile = 1 #: force motion

        if self.whipTimer > 0:
            # Whip around!
            if self.whipDir > 0: self.Turn(100)
            else: self.Turn(-100)
            self.Throttle(0)
            
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

    def ImmobilityWarning(self, id, on): # keep track of our own immobility warning
        if on and  id == 0 or id == 1 or id == 2 or id == 3:
            if  id == self.GetID():               
                self.ThisAI_bImmobile = 1

        if self.ImmobileCounter == 0:  # ID protector(Keeps other bots from changing "self.ThisAI_bImmobile = 1", until it runs its course of 'freeing' this AI.
            if not id == self.GetID(): 
                self.ThisAI_bImmobile = 0

				
AI.register(WhipperPlus)
