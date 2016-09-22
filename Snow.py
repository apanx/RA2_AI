from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics
import random

class Snow(AI.SuperAI):
    "Two wedges slide together or apart, plus some wonky self-righteous coding. Really just special for Seism 13."
    name = "Snow"

    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)
        
        self.snowcount = 0
        self.randcheck = 0
        self.worn = 0
        self.memory = eval(open("adaptiveAI.txt").read())
        self.botinzone = 0
        self.undered = 0
        self.newopponent=0

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
            
            self.RegisterSmartZone("weapon", 1)
            self.RegisterSmartZone("under", 2)
            self.bids = list(plus.getPlayers())
            self.bids.remove(self.GetID())

            #list the number of components on each bot to identify opponents
            self.complist = []
            for bot in self.bids:
                self.complist.append(plus.describe(bot).count(" "))
            #turn things default if it's a new opponent
            if self.complist!=self.memory[2]:
                self.memory[0]=1
                self.memory[1]=0
                self.memory[2]=self.complist
                file("adaptiveAI.txt", "w").write(str(self.memory))
            
        return AI.SuperAI.Activate(self, active)

    def Tick(self):
        #self righteous- fire weapons if balanced on rear end
        if list(plus.getDirection(self.GetID(),0))[1]>0.9:
            self.Input("Fire", 0, 1)
        #self.memory = eval(open("adaptiveAI.txt").read())
        # fire weapon

        targets = [x for x in self.sensors.itervalues() if x.contacts > 0 \
                and not plus.isDefeated(x.robot)]

        if self.weapons and self.botinzone == 1:
            self.Input("Fire", 0, 1)
            
        #if poo:
            #a= str([blah])
            #output1 = file("adaptiveAI.txt", "w")
            #output1.write(a)
            #output1.close
            
        #decide how to shift wedges- wide or narrow
        if self.randcheck == 0:
            if self.memory[0]==0:
                a = 1-self.memory[1]
                if self.undered==0:
                    self.memory[1]=a
                    self.memory[0]=1
                    file("adaptiveAI.txt", "w").write(str(self.memory))
            else:
                a = self.memory[1]
            self.worn = a*14
            #self.worn = random.randint(0, 31)
            self.snowcount=0
            self.randcheck = 1
        if self.snowcount >= 6:
            self.Input("Shift", 0, 0)
            self.Input("Shift", 1, 0)
        if self.snowcount<6:
            if self.worn<13:
                self.Input("Shift", 0, -100)
                self.snowcount += 1
            if self.worn>=13:
                self.Input("Shift", 1, 100)
                self.snowcount += 1
                
        return AI.SuperAI.Tick(self)

    def InvertHandler(self):
        # fire all weapons once per second (until we're upright!)
        while 1:
            self.Input("Srimech", 0, 1)
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

    def SmartZoneEvent(self, direction, id, robot, chassis):
        if id == 1 and self.weapons:
            if chassis:
                if direction == 1:
                    self.botinzone = 1
                if direction == -1:
                    self.botinzone = 0
        if id == 2:
            if robot > 0:
                if self.undered==0:
                    self.memory[0]=0
                    file("adaptiveAI.txt", "w").write(str(self.memory))
                    self.randcheck=0
                    self.undered=1
        return True
    
AI.register(Snow)
