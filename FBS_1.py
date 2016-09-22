from __future__ import generators
import plus
from plus import *
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics


class FBS_1(AI.SuperAI):
    "For SnS's, with improved Immobility handling."
    name = "FBS_1"
	#Made by Madiaba

    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)
        
        self.ENEMY = 0        
        self.ENEMY = 1        
        self.ENEMY = 2        
        self.ENEMY = 3
        self.Angle = 0

        self.ThisAIBot_XFactorA = 0
        self.ThisAIBot_ZFactorA = 0
        self.ThisAIBot_XFactorB = 0
        self.ThisAIBot_ZFactorB = 0

        self.ImmobileCounter = 0
        self.ThisAI_bImmobile = 0

        self.TESTER = 0

        self.PreSpinEntrance = 0
        if 'PreSpinEntrance' in args: self.PreSpinEntrance = args.get('PreSpinEntrance')
        self.PreSpinEntranceTimer = 0

        self.SD = 1
        if 'SpinDirection(1/-1)' in args: self.SD = args.get('SpinDirection(1/-1)')
       
        self.ReMobilizeRoutineTime = 40
        if 'ReMobilizeRoutineTime(10-60)' in args: self.ReMobilizeRoutineTime = args.get('ReMobilizeRoutineTime(10-60)')


        self.spin_range = 3.0
        if 'range' in args: self.spin_range = args.get('range')

        self.tactics.append(Tactics.Engage(self))

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
                tbox = self.debug.addText("line6", 10, 90, 250, 15) 
                tbox.setText("")
                tbox = self.debug.addText("line7", 10, 105, 250, 15)
                tbox.setText("")
                tbox = self.debug.addText("line8", 10, 120, 250, 15)
                tbox.setText("")
                tbox = self.debug.addText("line9", 10, 135, 250, 15)
                tbox.setText("")
                tbox = self.debug.addText("line10", 10, 150, 250, 15)
                tbox.setText("")
            
#            self.SAY_1 = plus.createSound("Sounds/Count_1.wav", True, (0,0,0)) # Indicator.
#            self.SAY_2 = plus.createSound("Sounds/Count_2.wav", True, (0,0,0)) # Indicator.
#            self.SAY_3 = plus.createSound("Sounds/Count_3.wav", True, (0,0,0)) # Indicator.
#            self.SAY_4 = plus.createSound("Sounds/Count_4.wav", True, (0,0,0)) # Indicator.
#            self.SAY_5 = plus.createSound("Sounds/Count_5.wav", True, (0,0,0)) # Indicator.

        return AI.SuperAI.Activate(self, active)






    def Tick(self):
#        self.DebugString(4, "self.ThisAI_bImmobile: "+  str(self.ThisAI_bImmobile))
#        self.DebugString(5, "self.ImmobileCounter: "+ str(int(self.ImmobileCounter)))
#        self.DebugString(7, "self.BU_ImmobileTimer_A(1-12): "+ str(int(self.BU_ImmobileTimer_A)))
#        self.DebugString(8, "self.BU_ImmobileTimer_B(1-50): "+ str(int(self.BU_ImmobileTimer_B)))
#        self.DebugString(9, "self.Angle: "+ str(self.Angle))
#        self.DebugString(10, "STILL_ImmobleChecker : "+ str(self.STILL_ImmobileChecker))


        # ---- Front/Back NAVIGATION ----
        # This replaces the "Forward" command in controller (must still use "LeftRight' command to turn).
        enemy, range = self.GetNearestEnemy()       # Check range from enemy all of the time.
        if enemy == 0: self.ENEMY = 0 # Convert 'enemy ' to  'self.ENEMY ' (else quits during immobile count).
        if enemy == 1: self.ENEMY = 1
        if enemy == 2: self.ENEMY = 2
        if enemy == 3: self.ENEMY = 3
        self.Angle = self.GetHeadingToID(self.ENEMY, False) # Check heading toward enemy.



        if self.ThisAI_bImmobile == 0: # If Immobility is off:   -------------------------------------

            if self.PreSpinEntranceTimer < self.PreSpinEntrance:  # Jut out initially.
                self.PreSpinEntranceTimer += 1        
                if self.Angle < 1 and self.Angle > -1: # If pointed toward enemy...
                    self.Input("LeftRight", 0, 0)
                    self.Input("Ahead", 0, 100) # then Go.
                    self.Input("Spin", 0, 0)

            if self.PreSpinEntranceTimer >= self.PreSpinEntrance:  # Start Spinning.
                if enemy is not None    and range < self.spin_range    and self.weapons: 
                    self.Input("LeftRight", 0, 0)
                    self.Input("Ahead", 0, 0) 
                    self.Input("Spin", 0, -120*self.SD) # Spin


 
        if self.ThisAI_bImmobile == 1: # If Immobility is on:  -------------------------------------

            self.ImmobileCounter += 1  # Then start counting....

            if self.ImmobileCounter == 1:   # Stop Spinning.   
                self.Input("Spin", 0, 120*self.SD)
                #self.Input("LeftRight", 0, -100)
                
            if self.ImmobileCounter >= self.ReMobilizeRoutineTime*0.2:   # go backward for a designated time.    
                self.Input("Spin", 0, 0)
                self.Input("LeftRight", 0, 0)
                self.Input("Ahead", 0, -100)
            
            if self.ImmobileCounter >= self.ReMobilizeRoutineTime*0.6:  # go forward for a designated time.    
                self.Input("Spin", 0, 0)
                self.Input("LeftRight", 0, 0)
                self.Input("Ahead", 0, 100)
                    
            if self.ImmobileCounter >= self.ReMobilizeRoutineTime:  # Reset everything:    
                self.ImmobileCounter = 0

        else:
            self.ThisAI_bImmobile = 0
            self.ImmobileCounter = 0     


        return AI.SuperAI.Tick(self)




    def ImmobilityWarning(self, id, on): 
        if id == self.GetID():
            if on:
                self.ThisAI_bImmobile = 1

            if not on:
                self.ThisAI_bImmobile = 0



#        self.DebugString(9, "id : "+ str(id))
#        self.DebugString(10, "self.ThisAI_bImmobile : "+ str(self.ThisAI_bImmobile))

        plus.AI.ImmobilityWarning(self, id, on)







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
            elif id == 5: self.debug.get("line5").setText(string)
            elif id == 6: self.debug.get("line6").setText(string) 
            elif id == 7: self.debug.get("line7").setText(string)
            elif id == 8: self.debug.get("line8").setText(string)
            elif id == 9: self.debug.get("line9").setText(string)
            elif id == 10: self.debug.get("line10").setText(string)


AI.register(FBS_1)
