#from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics

class Dual(AI.SuperAI):
    "Dual strategy"
    name = "Dual"

    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)

        self.zone = "fire1"
        self.zone1 = "fire2"
        self.triggers = ["Fire1"]
        self.reloadTime = 0
        self.reloadDelay = 4
        self.reloadTime2 = 0
        self.reloadDelay2 = 4

        if 'triggers' in args: self.triggers = args['triggers']
        if 'reload' in args: self.reloadDelay = args['reload']
        if 'reload2' in args: self.reloadDelay2 = args['reload2']

        self.triggerIterator = iter(self.triggers)

        self.tactics.append(Tactics.Engage(self))

    def Activate(self, active):
        if active:
            #if AI.SuperAI.debugging:
                self.debug = Gooey.Plain("watch", 0, 75, 250, 90)
                tbox = self.debug.addText("line0", 0, 0, 250, 15)
                tbox.setText("Throttle")
                tbox = self.debug.addText("line1", 0, 15, 250, 15)
                tbox.setText("Turning")
                tbox = self.debug.addText("line2", 0, 30, 250, 15)
                tbox.setText("")
                tbox = self.debug.addText("line3", 0, 45, 250, 15)
                tbox.setText("")
                tbox = self.debug.addText("line4", 0, 60, 250, 15)
                tbox.setText("")
                tbox = self.debug.addText("line5", 0, 75, 250, 15)
                tbox.setText("")
                self.RegisterSmartZone(self.zone, 1)


        return AI.SuperAI.Activate(self, active)

    def CheckSensors(self):
        if self.zone:
            self.sensors = {}
            results = self.GetZoneContents(self.zone)
            #print results
            for reading in results:
                self.SmartZoneEvent(1, 1, reading[0], reading[1])
        if self.zone1:
            result = self.GetZoneContents(self.zone1)
            for readings in result:
                if readings[0]> 0: b = readings[0] - 1

                if self.reloadTime2 > 0: self.reloadTime2 -= 1

                if not plus.isDefeated(b) and self.reloadTime2 <= 0:
                   self.Input("Fire2", 0, 1)
                   self.reloadTime2 = self.reloadDelay2
    def Tick(self):
        # fire weapon
        if self.weapons:
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
        # fire all weapons once per two second (until we're upright!)
        while 1:
            for trigger in self.triggers:
                self.Input("Fire2", 0, 1)
                self.Input(trigger, 0, 1)
                self.Input("SRM", 0, 1)
            for i in range(0, 16):
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
        #if self.debug:
            if id == 0: self.debug.get("line0").setText(string)
            elif id == 1: self.debug.get("line1").setText(string)
            elif id == 2: self.debug.get("line2").setText(string)
            elif id == 3: self.debug.get("line3").setText(string)
            elif id == 4: self.debug.get("line4").setText(string)
            elif id == 5: self.debug.get("line5").setText(string)


AI.register(Dual)