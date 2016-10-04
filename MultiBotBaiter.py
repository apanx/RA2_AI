from __future__ import generators
import plus
from plus import *
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics
import MadTactics

#    list.append(("FBS_Roud-a-Bout-2","FBS_1",{ 'PreSpinEntrance':20, 'SpinDirection(1/-1)':1, 'ReMobilizeRoutineTime(10-60)':30, 'range':99, 'radius':0.1, 'topspeed':100, 'throttle':130, 'turn':30, 'turnspeed':1.5, 'weapons':(11,)}))


class MultiBotBaiter(AI.SuperAI):
    "MultiBotBaiter strategy"
    name = "MultiBotBaiter"

    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)
               
        self.zone = "Zone1"
        self.triggers = ["Fire1"]
        self.trigger2 = ["Srimech"]
        self.reloadTime = 0
        self.reloadDelay = 3
        
        self.spin_range = 3.0
        
        if 'range' in args:
            self.spin_range = args.get('range')
      
        if 'triggers' in args: self.triggers = args['triggers']
        if 'reload' in args: self.reloadDelay = args['reload']
        
        self.triggerIterator = iter(self.triggers)
 
        self.tactics.append(Tactics.Engage(self)) # Main Tactic here.

        self.Timer_A = 10 # NOTE that this timer is starting at '10'.
        self.Timer_B = 0

        self.An_Enemy = 5
        self.Enemy_1 = 5
        self.Enemy_2 = 5
        self.Enemy_3 = 5
        self.Bot_ID_Locker_A = False
        self.Bot_ID_Locker_B = False
        self.Bot_ID_Locker_C = False
        self.Bot_ID_Locker_D = False

        self.List_Of_Bots = []
        self.ALLY = 5


        
    def Activate(self, active):
        if active:
            if AI.SuperAI.debugging:
                self.debug = Gooey.Plain("watch", 10, 175, 750, 175)
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
                tbox = self.debug.addText("line9", 10, 135, 750, 15)
                tbox.setText("")
                tbox = self.debug.addText("line10", 10, 150, 250, 15)
                tbox.setText("")
            
            self.RegisterSmartZone(self.zone, 1)

            self.LiftTing = plus.createSound("Sounds/LiftTing.wav", True, (0,0,0)) 
            self.EVADE_Mode = plus.createSound("Sounds/match_countdown.wav", True, (0,0,0)) 

        return AI.SuperAI.Activate(self, active)




    def Tick(self):
        self.DebugString(4, "self.Timer_A: "+  str(self.Timer_A))
#        self.DebugString(5, "self.Timer_B: "+ str(self.Timer_B))
        self.DebugString(9, "self.Enemy_1: "+ str(self.Enemy_1))
        self.DebugString(10, "self.ALLY: "+ str(self.ALLY))


        ####--- Find out who's who: (Friend or Foe) -------------------------------------
        if self.ALLY > 3:  # If our ALLY is NOT FOUND yet.
            enemy, e_range = self.GetNearestEnemy()

            if self.Bot_ID_Locker_A == False:  # Find Enemy_1
                self.Enemy_1 = enemy  
                self.Bot_ID_Locker_A = True

            if enemy  is not  self.Enemy_1:      # Find Enemy_2
                if self.Bot_ID_Locker_B == False:
                    self.Enemy_2 = enemy 
                    self.Bot_ID_Locker_B = True

                    self.List_Of_Bots = list(plus.getPlayers())  # Find out who your friend is.
                    self.List_Of_Bots.remove(self.Enemy_1)
                    self.List_Of_Bots.remove(self.Enemy_2)
                    self.List_Of_Bots.remove(self.GetID())
                    for lastbot in self.List_Of_Bots:
                        self.ALLY = lastbot




       ############--- MAIN BOT CONTROL -------#############---
        self.Timer_A += 1  


        ####---  Reset to MAIN TACTIC (Initially skipped) -------------------------------------
        if self.Timer_A == 9:  # This Timer was initially started at '10' (Default).
            #plus.playSound(self.LiftTing) 
            self.RemoveTactic("DeBaiter")
            self.tactics.append(Tactics.Engage(self))








        ####--- AVOIDING FRIENDLY FIRE  -------------------------------------
        if self.Timer_A >= 15:            
            if self.ALLY < 4: # If our ALLY is FOUND, then AVOID him.
                if self.GetDistanceToID(self.ALLY) < 3:  # Try to avoid your Friend.
                    self.RemoveTactic("Engage")
                    self.tactics.append(MadTactics.DeBaiter(self))
                    self.Timer_A = 0  # Reset Timer smaller to include "Reset to MAIN TACTIC".
                    #plus.playSound(self.EVADE_Mode) 




            # Evade-----
            if plus.getHealth(self.GetID(), 0) < .1:
                self.RemoveTactic("Engage")
                self.tactics.append(MadTactics.Evade(self))
                plus.playSound(self.LiftTing) 





#        if plus.getGameType() == "TEAM MATCH":
#            plus.playSound(self.LiftTing) 

#            plus.getLocation(self.GetID()) #  Get this AI's location.
#            plus.getLocation(self.ALLY) #  Get ALLY's location.

#        if plus.getGameType() == "TABLETOP":
#           self.tactics.append(Tactics.AvoidEdges(self))
 #            self.king_of_hill = (plus.getGameType() == "TEAM MATCH")

#            plus.getLocation(self.GetID()) #  Get this AI's location.
#            self.ThisAI = self.GetID()
#
#            #e_range = self.GetDistanceToID(enemy)
#            if enemy  e_range < 3





        ####--- WEAPONS -------------------------------------
#        if self.GetDistanceToID(self.ALLY) > 1:  # Do NOT attack your Friend.
        if self.weapons:

            # spin up depending on enemy's range
            enemy, range = self.GetNearestEnemy()
            
            if enemy is not None and range < self.spin_range:
                self.Input("Spin", 0, 1)
            elif self.GetInputStatus("Spin", 0) != 0:
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
                
#        else:
#            self.Input("Spin", 0, 0)

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



    
AI.register(MultiBotBaiter)
