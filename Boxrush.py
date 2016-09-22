from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics

class Boxrush(AI.SuperAI):
    "Slam em and hold em"
    name = "Boxrush"



    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)
        
        self.spin_range = 3.0
        self.prevx = 0
        self.prevy = 0
        self.watermelon = 0
        self.immocounter = 0
        
        if 'range' in args: self.spin_range = args.get('range')

        self.triggerSRM = "Srimech"
        self.TESTER = False

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

            #self.SRM_Indicator = plus.createSound("Sounds/snowplow_hit.wav", True, (0,0,0)) # Indicator.
            
        return AI.SuperAI.Activate(self, active)



    def Tick(self):
        if self.weapons:
            # spin up depending on enemy's range
            if self.watermelon == 0:
                self.prevx = self.GetLocation()[0]
                self.prevy = self.GetLocation()[2]
                self.watermelon = 1

            if self.watermelon == 1:
                self.immocounter += 1

            if self.GetLocation()[0] > self.prevx + 2 or self.GetLocation()[0] < self.prevx - 2 or self.GetLocation()[2] > self.prevy + 2 or self.GetLocation()[2] < self.prevy - 2:
                self.immocounter = 0
                self.watermelon = 0

            enemy, range = self.GetNearestEnemy()
            
            if enemy is not None and range < self.spin_range and self.weapons and self.bImmobile == False and self.immocounter < 50:
                self.Input("Shove", 0, 100)
            else:
                self.Input("Shove", 0, 0)

            if enemy is not None and range < self.spin_range and self.weapons and self.bImmobile == False:
                self.Input("Spin", 0, 100)
                #plus.playSound(self.SRM_Indicator) # Let me know if it's working...
            else:
                self.Input("Spin", 0, 0)



#        if self.TESTER == True:
#            plus.playSound(self.SRM_Indicator) # Let me know if it's working...

            
        return AI.SuperAI.Tick(self)



    def ImmobilityWarning(self, id, on):
        if on:
            self.Input("Shove", 0, 0)
            self.immobile_list[id] = plus.getTimeElapsed()
        elif id in self.immobile_list:
            self.Input("Shove", 0, 0)
            del self.immobile_list[id]
            
        if id == self.GetID():
            # keep track of our own immobility warning
            self.Input("Shove", 0, 0)
            self.bImmobile = on

        plus.AI.ImmobilityWarning(self, id, on)




    def InvertHandler(self):
        # fire weapon once per second (until we're upright!)
        while 1:
            for trigger in self.triggerSRM: self.Input(trigger, 0, 1)
            #self.TESTER = True
            #plus.playSound(self.SRM_Indicator) # Let me know if it's working...
            
            for i in range(0, 8):
                yield 0






    def StuckHandler(self):
        "This default generator is called when the bot is almost immobile."
        while 1:
            self.Input("Shove", 0, 0)
            # go forward for ?? seconds
            for i in range(0, 22):
                self.Input("Shove", 0, 0)
                pos = vector3(self.GetLocation())
                dir = vector3(self.GetDirection())
                self.DriveToLocation((pos + dir * 3).asTuple())
                yield 0
            # back up for ?? seconds (will stop once we're not immobile)
            for i in range(0, 6):
                self.Input("Shove", 0, 0)
                pos = vector3(self.GetLocation())
                dir = vector3(self.GetDirection())
                self.DriveToLocation((pos - dir * 3).asTuple(), True)
                yield 0	


        
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
        if self.debug:
            if id == 0: self.debug.get("line0").setText(string)
            elif id == 1: self.debug.get("line1").setText(string)
            elif id == 2: self.debug.get("line2").setText(string)
            elif id == 3: self.debug.get("line3").setText(string)



AI.register(Boxrush)
