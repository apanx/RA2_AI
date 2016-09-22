from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import random
from random import randint
import Gooey
import math
import Tactics

class SpinnerOmni(AI.SuperAI):
    "Nothing to see here.  Just a slightly modified Omni.  Probably useless.  Move along now."
    name = "SpinnerOmni"

    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)
               
        self.zone = "weapon"
        self.triggers = ["Fire"]
        self.trigger2 = ["Srimech"]
        self.reloadTime = 0
        self.reloadDelay = 3
        self.numLosses = eval(open("adaptiveAI_2.txt").read())
        self.newnumLosses = self.numLosses
        if self.numLosses > 0 and randint(1, (20 - self.numLosses)) == 1:
            self.secretFunction = self.Secret
            self.exactingRevenge = 1
        else:
            self.secretFunction = None
            self.exactingRevenge = 0
        self.spin_range = 3.0
        self.yCenter = 0
        self.xforce = 0
        self.yforce = 0
        self.zforce = 0
        self.zaptimer = 0
        self.summon = 0
        self.eyetimer = 0
        self.numComps = 0
        self.timetodie = 0
        self.smoker = 32
        self.smokeh = 0
        self.smoketimer = 0
        self.music = plus.createSound("Sounds\\bbeans\\sound1.wav", False, (0,0,0))
        self.psygrab = plus.createSound("Sounds\\bbeans\\sound2.wav", False, (0,0,0))
        self.flamepuff = plus.createSound("Sounds\\bbeans\\sound3.wav", False, (0,0,0))
        self.eye = plus.createSound("Sounds\\bbeans\\sound4.wav", False, (0,0,0))
        self.finale = plus.createSound("Sounds\\bbeans\\sound5.wav", True, (0,0,0))
        self.charge = plus.createSound("Sounds\\cmp_battery2.wav", False, (0,0,0))
        self.bang = plus.createSound("Sounds\\bbeans\\sound6.wav", False, (0,0,0))
        if self.exactingRevenge == 1:
            Arenas.createArenaByName("Epic Showdown")
            self.arena = Arenas.currentArena
            self.spinner1 = self.arena.GetHinge("Hinge01")
            self.spinner1.SetAutoLocks(False, False)
            self.spinner1.Lock(False)
            self.spinner1.SetPowerSettings(5.8,150000)
            self.spinner1.SetDirection(-100)
            self.spinner2 = self.arena.GetHinge("Hinge02")
            self.spinner2.SetAutoLocks(False, False)
            self.spinner2.Lock(False)
            self.spinner2.SetPowerSettings(2.68,150000)
            self.spinner2.SetDirection(-100)
            self.spinner3 = self.arena.GetHinge("Hinge03")
            self.spinner3.SetAutoLocks(False, False)
            self.spinner3.Lock(False)
            self.spinner3.SetPowerSettings(1.11,150000)
            self.spinner3.SetDirection(-100)
        
        if 'range' in args:
            self.spin_range = args.get('range')
      
        if 'triggers' in args: self.triggers = args['triggers']
        if 'reload' in args: self.reloadDelay = args['reload']
        
        self.triggerIterator = iter(self.triggers)
 
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
            self.tauntbox = Gooey.Plain("taunt", 10, 175, 640, 175)
            tbox = self.tauntbox.addText("taunt1", 10, 0, 640, 15)
            tbox.setText("")
            
            self.RegisterSmartZone(self.zone, 1)
            
            if self.exactingRevenge == 1:
                self.bids = list(plus.getPlayers())
                self.bids.remove(self.GetID())

                #list the number of components on each bot and get the maximum number
                self.complist = []
                for bot in self.bids:
                    self.complist.append(plus.describe(bot).count(" "))
                    self.arena.CreateLightning(bot, self.GetLocation(), plus.getLocation(bot))
                    self.arena.SetLightningVisible(bot, True)
                    #disable controls - just to make players even more helpless than they already are.
                    plus.disable(bot, 1)
                self.numComps = max(self.complist)

                self.yCenter = self.GetLocation()[1] + 6
                plus.playSound(self.psygrab)
                plus.loopSound(self.music)
                
                #torches for Epic Showdown arena
                plus.AddParticleEmitter((-10.25, 4, 0), (0, 3, 0), (2, 5, 2)).SetEmitting(True)
                plus.AddParticleEmitter((-5.125, 4, -8.88), (0, 3, 0), (2, 5, 2)).SetEmitting(True)
                plus.AddParticleEmitter((5.125, 4, -8.88), (0, 3, 0), (2, 5, 2)).SetEmitting(True)
                plus.AddParticleEmitter((10.25, 4, 0), (0, 3, 0), (2, 5, 2)).SetEmitting(True)
                plus.AddParticleEmitter((5.125, 4, 8.88), (0, 3, 0), (2, 5, 2)).SetEmitting(True)
                plus.AddParticleEmitter((-5.125, 4, 8.88), (0, 3, 0), (2, 5, 2)).SetEmitting(True)
        else:
            # get rid of reference to self
            self.secretFunction = None
            
        return AI.SuperAI.Activate(self, active)

    def Tick(self):
        # add to numLosses if SFTW goes below half health
        if self.GetHealth(0) < 0.5 and self.newnumLosses == self.numLosses:
            self.newnumLosses = self.numLosses + 1
            file("adaptiveAI_2.txt", "w").write(str(self.newnumLosses))
            
        # fire weapon
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
            
        bReturn = AI.SuperAI.Tick(self)
            
        # call this now so it takes place after other driving commands
        if self.secretFunction: self.secretFunction(len(targets) > 0)
        
        return bReturn

    def Secret(self, bTarget):
        #This is definitely NOT a secret super death AI for Spinner from the west!!!  You don't need to scroll down any further!!!
        # Tauntauns
        if self.numComps > 0:
            if plus.getTimeElapsed() < 3:
                self.tauntbox.get("taunt1").setText("I have been waiting a long time for this.")
            if 3 < plus.getTimeElapsed() < 5:
                self.tauntbox.get("taunt1").setText("Go on, squirm!")
            if 5 < plus.getTimeElapsed() < 8:
                self.tauntbox.get("taunt1").setText("Just try and budge that useless hood ornament you call a weapon!")
            if 8 < plus.getTimeElapsed() < 10:
                self.tauntbox.get("taunt1").setText("Squirm like the worm you are!")
            if 10 < plus.getTimeElapsed() < 12:
                self.tauntbox.get("taunt1").setText("Your struggles will not avail you...")
            if 12 < plus.getTimeElapsed() < 16:
                self.tauntbox.get("taunt1").setText("...against the power of the EYE OF THE WEST!")
            if 16 < plus.getTimeElapsed() < 18:
                self.tauntbox.get("taunt1").setText("Long have I tolerated your abuse, but NO LONGER!")
            if 18 < plus.getTimeElapsed() < 22:
                self.tauntbox.get("taunt1").setText("With the power of the Western Eye at my command, I AM INVINCIBLE!")
            if 22 < plus.getTimeElapsed() < 24:
                self.tauntbox.get("taunt1").setText("Now... suffer.")
            if 24 < plus.getTimeElapsed() < 27:
                self.tauntbox.get("taunt1").setText("Know the black depths of pain you have inflicted upon me!")
            if 27 < plus.getTimeElapsed() < 29:
                self.tauntbox.get("taunt1").setText("FEEL THE WRATH OF THE WEST!")
            if 29 < plus.getTimeElapsed() < 32:
                self.tauntbox.get("taunt1").setText("HA HA HA HA HA HA HA HA HA HA HA HA HA...")

        #stay put unless we're being counted out
        if not self.bImmobile:
            self.Throttle(0)
            
        for bot in self.bids:
            #cool psychic lightning effects
            self.arena.SetLightningStartEnd(bot, self.GetLocation(), plus.getLocation(bot))
            self.zaptimer += 1
            if self.zaptimer > 4:
                plus.zap(bot, 20, 1)
                self.zaptimer = 0

            #apply more force as bots get further from center
            self.xforce = -1 * plus.getLocation(bot)[0] * plus.getWeight(bot)
            self.yforce = -30 * (plus.getLocation(bot)[1] - self.yCenter) * plus.getWeight(bot)
            self.zforce = -1 * plus.getLocation(bot)[2] * plus.getWeight(bot)

            plus.force(bot, self.xforce, self.yforce, self.zforce)

            #summon THE EYE OF THE WEST
            if abs(plus.getLocation(bot)[0]) < 2 and abs(plus.getLocation(bot)[2]) < 2 and self.eyetimer == 0:
                self.summon = 1
                plus.removeSound(self.psygrab)

        if self.summon == 1 and self.eyetimer < 17:
            self.eyetimer += 0.25
        if 0 < self.eyetimer <= 8 and self.eyetimer%1 == 0:
            plus.AddParticleEmitter((4*math.cos((math.pi/8)*self.eyetimer), (self.yCenter - 6), 4*math.sin((math.pi/8)*self.eyetimer)), (0, 3, 0), (1, 5, 1)).SetEmitting(True)
            plus.AddParticleEmitter((4*math.cos((math.pi/8)*self.eyetimer + math.pi), (self.yCenter - 6), 4*math.sin((math.pi/8)*self.eyetimer + math.pi)), (0, 3, 0), (1, 5, 1)).SetEmitting(True)
            plus.playSound(self.flamepuff)
        if self.eyetimer == 9:
            plus.AddParticleEmitter((1, (self.yCenter - 6), 3), (0, 3, 0), (1, 5, 1)).SetEmitting(True)
            plus.AddParticleEmitter((-1, (self.yCenter - 6), -3), (0, 3, 0), (1, 5, 1)).SetEmitting(True)
            plus.playSound(self.flamepuff)
        if self.eyetimer == 10:
            plus.AddParticleEmitter((1.6, (self.yCenter - 6), 2), (0, 3, 0), (1, 5, 1)).SetEmitting(True)
            plus.AddParticleEmitter((-1.6, (self.yCenter - 6), -2), (0, 3, 0), (1, 5, 1)).SetEmitting(True)
            plus.playSound(self.flamepuff)
        if self.eyetimer == 11:
            plus.AddParticleEmitter((1.9, (self.yCenter - 6), 1), (0, 3, 0), (1, 5, 1)).SetEmitting(True)
            plus.AddParticleEmitter((-1.9, (self.yCenter - 6), -1), (0, 3, 0), (1, 5, 1)).SetEmitting(True)
            plus.playSound(self.flamepuff)
        if self.eyetimer == 12:
            plus.AddParticleEmitter((2, (self.yCenter - 6), 0), (0, 3, 0), (1, 5, 1)).SetEmitting(True)
            plus.AddParticleEmitter((-2, (self.yCenter - 6), 0), (0, 3, 0), (1, 5, 1)).SetEmitting(True)
            plus.playSound(self.flamepuff)
        if self.eyetimer == 13:
            plus.AddParticleEmitter((1.9, (self.yCenter - 6), -1), (0, 3, 0), (1, 5, 1)).SetEmitting(True)
            plus.AddParticleEmitter((-1.9, (self.yCenter - 6), 1), (0, 3, 0), (1, 5, 1)).SetEmitting(True)
            plus.playSound(self.flamepuff)
        if self.eyetimer == 14:
            plus.AddParticleEmitter((1.6, (self.yCenter - 6), -2), (0, 3, 0), (1, 5, 1)).SetEmitting(True)
            plus.AddParticleEmitter((-1.6, (self.yCenter - 6), 2), (0, 3, 0), (1, 5, 1)).SetEmitting(True)
            plus.playSound(self.flamepuff)
        if self.eyetimer == 15:
            plus.AddParticleEmitter((1, (self.yCenter - 6), -3), (0, 3, 0), (1, 5, 1)).SetEmitting(True)
            plus.AddParticleEmitter((-1, (self.yCenter - 6), 3), (0, 3, 0), (1, 5, 1)).SetEmitting(True)
            plus.playSound(self.flamepuff)
        if self.eyetimer == 16:
            plus.AddParticleEmitter((0, (self.yCenter - 6), 0), (0, 16, 0), (1, 16, 1)).SetEmitting(True)
            plus.playSound(self.eye)
            plus.removeSound(self.flamepuff)
            self.timetodie = 1

        #remove enemy components one by one
        if self.timetodie == 1:
            if self.numComps > 0:
                self.numComps -= 0.25
                if self.numComps%1 == 0:
                    plus.addPoints(self.GetID(), 1337)
                    for bot in self.bids:
                        if self.numComps > 0:
                            plus.emitSmoke(30, (plus.getLocation(bot)), (0, 0, 0), (5, 5, 5))
                            plus.damage(bot, self.numComps, 100000, plus.getLocation(bot))
                            plus.damage(bot, self.numComps, 100000, plus.getLocation(bot))
                            plus.addPoints(bot, -1000)

        #finishing blow
        if self.numComps == 0:
            if self.smoker == 32:
                plus.removeSound(self.eye)
                plus.fadeInToLoop(self.finale, -100, 3200)
                self.tauntbox.get("taunt1").setText("Do you hear that sound? Know what it is?")
            if self.smoker > 1:
                self.smoker -= 0.5
            self.smoketimer += 0.1
            self.smokeh = (self.yCenter - 6) + (6 * ((1 / self.smoker) ** 2))
            
            #SMOKE TORNADO
            plus.emitSmoke(30, ((self.smoker * (math.cos((math.pi/4) + self.smoketimer))), self.smokeh, (self.smoker * (math.sin((math.pi/4) + self.smoketimer)))), (0, 0, 0), (5, 8, 5))
            plus.emitSmoke(30, ((self.smoker * (math.cos((math.pi/2) + self.smoketimer))), self.smokeh, (self.smoker * (math.sin((math.pi/2) + self.smoketimer)))), (0, 0, 0), (5, 8, 5))
            plus.emitSmoke(30, ((self.smoker * (math.cos((3*math.pi/4) + self.smoketimer))), self.smokeh, (self.smoker * (math.sin((3*math.pi/4) + self.smoketimer)))), (0, 0, 0), (5, 8, 5))
            plus.emitSmoke(30, ((self.smoker * (math.cos((math.pi) + self.smoketimer))), self.smokeh, (self.smoker * (math.sin((math.pi) + self.smoketimer)))), (0, 0, 0), (5, 8, 5))
            plus.emitSmoke(30, ((self.smoker * (math.cos((5*math.pi/4) + self.smoketimer))), self.smokeh, (self.smoker * (math.sin((5*math.pi/4) + self.smoketimer)))), (0, 0, 0), (5, 8, 5))
            plus.emitSmoke(30, ((self.smoker * (math.cos((3*math.pi/2) + self.smoketimer))), self.smokeh, (self.smoker * (math.sin((3*math.pi/2) + self.smoketimer)))), (0, 0, 0), (5, 8, 5))
            plus.emitSmoke(30, ((self.smoker * (math.cos((7*math.pi/4) + self.smoketimer))), self.smokeh, (self.smoker * (math.sin((7*math.pi/4) + self.smoketimer)))), (0, 0, 0), (5, 8, 5))
            plus.emitSmoke(30, ((self.smoker * (math.cos((2*math.pi) + self.smoketimer))), self.smokeh, (self.smoker * (math.sin((2*math.pi) + self.smoketimer)))), (0, 0, 0), (5, 8, 5))
            
            if self.smoker == 24:
                self.tauntbox.get("taunt1").setText("That is the sound of your death approaching.")
            if self.smoker == 16:
                self.tauntbox.get("taunt1").setText("At last... vengeance shall be mine.")
            if self.smoker == 8:
                self.tauntbox.get("taunt1").setText("HA HA HA HA HA HA HA HA HA HA HA HA HA...")
            if self.smoker == 2:
                plus.stopAllSounds()
                plus.playSound(self.charge)
            if self.smoker == 1:
                plus.removeSound(self.charge)
                plus.playSound(self.bang)
                self.smoker = 0.9
                plus.fadeFromBlack(6)
                for bot in self.bids:
                    #must un-disable bots in order to kill them
                    plus.disable(bot, 0)
                    self.arena.SetLightningVisible(bot, False)
                    plus.damage(bot, 0, 100000, plus.getLocation(bot))
                    plus.damage(bot, 0, 100000, plus.getLocation(bot))
                    plus.damage(bot, 0, 100000, plus.getLocation(bot))
                    plus.damage(bot, 0, 100000, plus.getLocation(bot))
                    #reset numLosses
                    file("adaptiveAI_2.txt", "w").write("0")

    def InvertHandler(self):
        # fire all weapons once per second (until we're upright!)
        while 1:
            for trigger in self.trigger2:
                self.Input(trigger, 0, 1)
            
            for i in range(0, 8):
                yield 0
                
    def __del__(self):
        plus.stopAllSounds()
        #Arenas.SuperArena.__del__(self)
         
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
            #elif id == 5: self.debug.get("line5").setText(string)
    
AI.register(SpinnerOmni)