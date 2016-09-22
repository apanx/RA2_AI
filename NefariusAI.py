from __future__ import generators
import math
import random

import plus
import AI
import Arenas
import Gooey

# FIX: Gets stuck on 441 of Ram when upside down...

class NefariusAI(AI.SuperAI):
    "An AI specially designed to complement Trovaner's AW-NefariusBeing."
    # A more universally friendly version will be released on a later date.
    # I just wanted to get my bot working before the Robo Zone 2 deadline.
    name = "NefariusAI"

    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)

        self.__setattr__tickInterval__(0.01)

        self.teamedup = False

        self.collection = []
        self.lastLoc = (0,0,0)
        self.oldTime = 0.0
        self.curSpeed = 0.0
        self.avgSpeed = 0.0
        self.maxCollection = 20
        if 'samplesize' in args:
            self.maxCollection = min(1,args['samplesize'])

        self.sources = ['Tactics','NefariusTactics']
        if 'additionalsources' in args:
            self.sources.extend(list(args['additionalsources']))

        if 'teamtactics' in args:
            self.teamtactics = list(args['teamtactics'])
        else: self.teamtactics = []

        if 'primarytactics' in args:
            self.primarytactics = list(args['primarytactics'])
        else: self.primarytactics = ["Engage"]

        if 'secondarytactics' in args:
            self.secondarytactics = list(args['secondarytactics'])
        else: self.secondarytactics = ["Evasion"]

        self.teamedUpTactics = []
        self.noWeaponTactics = []

        for source in self.sources:
            source = __import__(source, globals(), locals())

            #Psuedocode:
            # for every variable in the given source
            #   check if type is class
            #     check if class is a Tactic class
            #       check if tactic is in our list
            #         add tactic to our list

            self.tactics.extend([eval("source.%s(self)" %x) for x in dir(source) \
                                 if isinstance(eval("source.%s" %x), type(AI.Tactic)) \
                                 if issubclass(eval("source.%s" %x), AI.Tactic) \
                                 if eval("source.%s.name" %x) in self.primarytactics])

            self.noWeaponTactics.extend([eval("source.%s(self)" %x) for x in dir(source) \
                                         if isinstance(eval("source.%s" %x), type(AI.Tactic)) \
                                         if issubclass(eval("source.%s" %x), AI.Tactic) \
                                         if eval("source.%s.name" %x) in self.secondarytactics])

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

            allyIDs = [playerid for playerid in plus.getPlayers() if not playerid in self.GetEnemies() and playerid != self.GetID()]
            if allyIDs > 0: # Is there anyone else on my team?
                allyAIs = [b for b in AI.running_ai if b.GetID() in allyIDs]

                if allyAIs: #if there are other AI bots
                    self.teamedup = True
                    for source in self.sources:
                        source = __import__(source, globals(), locals())
                        self.tactics.extend([eval("source.%s(self, allyAIs)" %x) for x in dir(source) \
                                             if isinstance(eval("source.%s" %x), type(AI.Tactic)) \
                                             if issubclass(eval("source.%s" %x), AI.Tactic) \
                                             if eval("source.%s.name" %x) in self.teamtactics])

        return AI.SuperAI.Activate(self, active)

    def Tick(self):
        self.updateSpeed()
        return AI.SuperAI.Tick(self)

    def updateSpeed(self):
        newLoc = self.GetLocation()
        if newLoc[0] != self.lastLoc[0]: #no need to compare more than the x-coordinate
            #the geometry updates roughly every 0.03 seconds on my computer
            newTime = plus.getTimeElapsed()
            deltaTime = (newTime-self.oldTime)

            deltaPos = ((newLoc[0]-self.lastLoc[0])**2+\
                        (newLoc[1]-self.lastLoc[1])**2+\
                        (newLoc[2]-self.lastLoc[2])**2)**.5

            if deltaTime: #if not zero
                self.curSpeed = deltaPos/deltaTime
            else: self.curSpeed = 0

            self.oldTime = newTime
            self.lastLoc = newLoc

            self.collection.append(self.curSpeed)
            if len(self.collection) > self.maxCollection:
                self.collection = self.collection[1:]
            # progressive averaging
            self.avgSpeed += (self.curSpeed-self.avgSpeed)/len(self.collection)

    def GetSpeed(self):
        #True Speed (the original GetSpeed actually calculated the velocity)
        #Unfortunately, the original wasn't compatible with my bot.
        #TODO: Convert this to velocity so that we have a direction (for compatability reasons)
        return self.avgSpeed

    def IsUpsideDown(self):
        return (self.GetDirection()[1] < 0)

    def GetDirection(self): #fixes issues with stuck handling and ram
        heading = self.GetHeading(False)
        x = math.sin(heading)
        y = AI.SuperAI.GetDirection(self)[1]
        z = math.cos(heading)
        return (x,y,z)

    def StuckHandler(self):
        "This default generator is called when the bot is almost immobile."
        while 1:
            # back up for 2 seconds (will stop once we're not immobile)
            for i in range(0, 2/self.tickInterval):
                pos = AI.vector3(self.GetLocation())
                dir = AI.vector3(self.GetDirection())
                self.DriveToLocation((pos - dir * 3).asTuple(), True)
                yield 0
            # go forward for 2 seconds
            for i in range(0, 2/self.tickInterval):
                pos = AI.vector3(self.GetLocation())
                dir = AI.vector3(self.GetDirection())
                self.DriveToLocation((pos + dir * 3).asTuple())
                yield 0

    def LostComponent(self, id):
        if id in self.weapons: self.weapons.remove(id)

        if not self.weapons:
            if self.teamedup:
                self.tactics = [x for x in self.tactics if not x.name in self.teamtactics]
            self.tactics = [x for x in self.tactics if not x.name in self.primarytactics]
            self.tactics.extend(self.noWeaponTactics)

        return AI.SuperAI.LostComponent(self, id)

    def DebugString(self, id, string):
        if self.debug:
            if id == 0: self.debug.get("line0").setText(string)
            elif id == 1: self.debug.get("line1").setText(string)
            elif id == 2: self.debug.get("line2").setText(string)
            elif id == 3: self.debug.get("line3").setText(string)

AI.register(NefariusAI)
