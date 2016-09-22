from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics

class ElectricHammer(AI.SuperAI):
    "Swings a hammer on a spin motor back and forth."
    # Use variable 'NoChassisTime' in Bindings.py to set the amount of time in half-seconds the AI will wait to find the chassis before giving up and firing, when there are components in the smart zone.
    # Use variable 'StartAngle' to set the angle the hammer will revert to when not in use.  For best results, this should be a multiple of pi/2.
    # Use variable 'SwingTime' to tell the AI how long in ticks it should take to retract the hammer.  A tick is 1/8 second.
    name = "ElectricHammer"

    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)

        self.zone1 = "weapon"
        self.triggers1 = ["Fire"]
        self.triggers2 = ["Srimech"]
        self.botinzone = 0
        self.compinzone = 0
        self.comptimer = 0
        self.NoChassisTime = 8
        self.motor = 8
        self.startangle = math.pi
        self.retract = 0
        self.retracttime = 5
        self.hittime = 0

        if 'zone' in args: self.zone = args['zone']

        if 'triggers' in args: self.triggers1 = args['triggers']
        if 'srimech' in args: self.triggers2 = args['srimech']
        if 'NoChassisTime' in args: self.NoChassisTime = args.get('NoChassisTime') * 4
        if 'MotorID' in args: self.motor = args.get('MotorID')
        if 'StartAngle' in args: self.startangle = args.get('StartAngle')
        if 'SwingTime' in args: self.retracttime = args.get('SwingTime')

        self.retracttimer = self.retracttime

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
            # self.tauntbox = Gooey.Plain("taunt", 10, 175, 640, 175)
            # tbox = self.tauntbox.addText("taunt1", 10, 0, 640, 15)
            # tbox.setText("")

            self.RegisterSmartZone(self.zone1, 1)

        return AI.SuperAI.Activate(self, active)

    def Tick(self):
        #self.tauntbox.get("taunt1").setText(str(self.GetMotorAngle(self.motor)))
        # fire weapon

        targets = [x for x in self.sensors.itervalues() if x.contacts > 0 \
                and not plus.isDefeated(x.robot)]

        # retract hammer when not in use
        if self.botinzone == 0 or self.comptimer <= self.NoChassisTime or self.retract == 1:
            if abs(self.GetMotorAngle(self.motor) - self.startangle) > math.pi/2:
                if self.IsUpsideDown() and self.bInvertible:
                    self.Input("Hammer", 0, 100)
                else:
                    self.Input("Hammer", 0, -100)
            else:
                self.Input("Hammer", 0, 0)
                self.retract = 0
                self.retracttimer = 0

        # if a component is in the smart zone but not the chassis, wait to find chassis before firing weapons
        if self.compinzone == 1 and self.botinzone == 0:
            self.comptimer += 1

        if self.botinzone == 1:
            self.comptimer = 0

        if (self.weapons and (self.botinzone == 1 or (self.comptimer >= self.NoChassisTime and self.compinzone == 1))) or self.bImmobile or (self.IsUpsideDown() and not self.bInvertible):
            if self.retract == 0:
                if self.retracttimer < self.retracttime:
                    self.retracttimer += 1
                if self.IsUpsideDown() and self.bInvertible:
                    self.Input("Hammer", 0, -100)
                else:
                    self.Input("Hammer", 0, 100)
                # retract weapon as soon as we hit something
                if self.GetLastDamageDone()[0] in self.weapons and self.GetLastDamageDone()[2] > self.hittime and self.retracttimer > 0:
                    self.retract = 1
                    self.hittime = self.GetLastDamageDone()[2]
                if plus.getTimeElapsed() - self.hittime > self.retracttime*0.375 and self.retracttimer == self.retracttime:
                    self.retract = 1
        #*** Old timer-based code ***#
            # if self.swingtimer == -1:
                # self.swingtimer = 0
        # if 0 <= self.swingtimer <= self.swingtime/2:
            # self.swingtimer += 1
            # if self.IsUpsideDown() and self.bInvertible:
                # self.Input("Hammer", 0, -100)
            # else:
                # self.Input("Hammer", 0, 100)
        # if self.swingtimer > self.swingtime/2:
            # self.swingtimer += 1
            # if self.IsUpsideDown() and self.bInvertible:
                # self.Input("Hammer", 0, 100)
            # else:
                # self.Input("Hammer", 0, -100)
        # if self.swingtimer >= self.swingtime:
            # self.swingtimer = -1

        bReturn = AI.SuperAI.Tick(self)

        return bReturn

    def InvertHandler(self):
        # fire all weapons once per second (until we're upright!)
        while 1:
            for trigger in self.triggers2:
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

    def SmartZoneEvent(self, direction, id, robot, chassis):
        if id == 1 and self.weapons:
            if robot > 0:
                if direction == 1:
                    self.compinzone = 1
                    if chassis:
                        self.botinzone = 1
                if direction == -1:
                    self.compinzone = 0
                    if chassis:
                        self.botinzone = 0
        return True

AI.register(ElectricHammer)