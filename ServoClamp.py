from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics

class ServoClamp(AI.SuperAI):
    "Uses servo motor(s) to clamp enemy bot. Variables are the servo ID and the start/end angles of servo movement. Must also pick up the servo's ID number. Can wait for chassis to be in smartzone like Popup.py"
    # Use variable 'NoChassisTime' in Bindings.py to set the amount of time in seconds the AI will wait to find the chassis before giving up and clamping, when there are components in the smart zone.
    # Brought to you by Naryar and shamelessly ripped off Clickbeetle's Kheper.py.
    name = "ServoClamp"

    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)

        self.zone1 = "weapon"
        self.triggers1 = ["Fire"]
        self.servo = 9001
        self.botinzone = 0
        self.compinzone = 0
        self.comptimer = 0
        self.NoChassisTime = 2
        self.servostartangle = -math.pi*0.5
        self.servostopangle = math.pi*0.5
        if 'ServoID' in args: self.servo = args.get('ServoID')
        if 'StartAngle' in args: self.servostartangle = args.get ('StartAngle')
        if 'StopAngle' in args: self.servostopangle = args.get ('StopAngle')

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

            self.RegisterSmartZone(self.zone1, 1)

        return AI.SuperAI.Activate(self, active)

    def Tick(self):
        # fire weapon

        targets = [x for x in self.sensors.itervalues() if x.contacts > 0 \
                and not plus.isDefeated(x.robot)]

        # if a component is in the smart zone but not the chassis, wait to find chassis before firing weapons
        if self.compinzone == 1 and self.botinzone == 0:
            self.comptimer += 1

        if self.botinzone == 1:
            self.comptimer = 0

        if self.weapons and (self.botinzone == 1 or (self.comptimer >= self.NoChassisTime and self.compinzone == 1)):
            if not self.IsUpsideDown():
                if self.GetMotorAngle(self.servo) <= self.servostopangle:
                    self.Input("Servo", 0, 100)
                else:
                    self.Input("Servo", 0, 0)


        if self.botinzone == 0 and (self.comptimer < self.NoChassisTime or self.compinzone == 0):
            #retract servo arm when not in use
                if self.GetMotorAngle(self.servo) >= self.servostopangle or self.GetMotorAngle(self.servo) <= -math.pi*0.5:
                    self.Input("Servo", 0, 100)
                if 0 > self.GetMotorAngle(self.servo) >= -math.pi*0.2 or 0 < self.GetMotorAngle(self.servo) <= self.servostopangle:
                    self.Input("Servo", 0, -100)
                if self.servostopangle >= self.GetMotorAngle(self.servo) >= self.servostartangle:
                    self.Input("Servo", 0, 0)

        bReturn = AI.SuperAI.Tick(self)

        return bReturn

    def InvertHandler(self):
        # fire all weapons once per second (until we're upright!)
        while 1:
            for trigger in self.triggers2:
                self.Input(trigger, 0, 1)

            for i in range(0, 8):
                yield 0

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

AI.register(ServoClamp)