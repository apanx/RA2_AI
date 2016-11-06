from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics

class ServoClampHammer(AI.SuperAI):
    "Uses servo motor(s) to clamp enemy bot and Hammer on Spinmotor to smash. \
    Variables are the servo ID and the start/end angles of servo movement. \
    Can wait for chassis to be in smartzone like Popup.py"
    # Use list ServoIDs to set servos used to clamp
    # Use list ServoStartAngles to set starting position of servos
    # Use list ServoStopAngles to set clamping position of servos
    # Use variable 'NoChassisTime' in Bindings.py to set the amount of time in half-seconds the AI will wait to find the chassis before giving up and firing, when there are components in the smart zone.
    # Use variable 'ServoID' to set ID of Hammer motor.
    # Use variable 'MotorStartAngle' to set the angle the hammer will revert to when not in use.  For best results, this should be a multiple of pi/2.
    # Use variable 'SwingTime' to tell the AI how long in ticks it should take to retract the hammer.  A tick is 1/8 second.
    name = "ServoClampHammer"

    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)
        self.zone1 = "weapon"
        self.triggers1 = ["Fire"]
        self.triggers2 = ["Srimech"]
        self.servos = [1, 2]
        self.botinzone = 0
        self.compinzone = 0
        self.comptimer = 0
        self.NoChassisTime = 8
        self.servostartangles = [-math.pi * 0.5, -math.pi * 0.5]
        self.servostopangles = [math.pi * 0.5, math.pi * 0.5]
        if 'ServoIDs' in args: self.servos = args.get('ServoIDs')
        if 'ServoStartAngles' in args: self.servostartangles = args.get ('ServoStartAngles')
        if 'ServoStopAngles' in args: self.servostopangles = args.get ('ServoStopAngles')

        self.motor = 8
        self.motorstartangle = math.pi
        self.retract = 0
        self.retracttime = 5
        self.hittime = 0
        if 'zone' in args: self.zone1 = args['zone']
        if 'triggers' in args: self.triggers1 = args['triggers']
        if 'srimech' in args: self.triggers2 = args['srimech']
        if 'NoChassisTime' in args: self.NoChassisTime = args.get('NoChassisTime') * 4
        if 'MotorID' in args: self.motor = args.get('MotorID')
        if 'MotorStartAngle' in args: self.motorstartangle = args.get('MotorStartAngle')
        if 'SwingTime' in args: self.retracttime = args.get('SwingTime')

        self.retracttimer = self.retracttime

        self.tactics.append(Tactics.Engage(self))

    def Activate(self, active):
        if active:
            if AI.SuperAI.debugging:
                self.debug = Gooey.Plain("watch", 0, 150, 250, 165)
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
                tbox = self.debug.addText("line6", 0, 90, 250, 15)
                tbox.setText("")
                tbox = self.debug.addText("line7", 0, 105, 250, 15)
                tbox.setText("")
                tbox = self.debug.addText("line8", 0, 120, 250, 15)
                tbox.setText("")
                tbox = self.debug.addText("line9", 0, 135, 250, 15)
                tbox.setText("")

            self.RegisterSmartZone(self.zone1, 1)

        return AI.SuperAI.Activate(self, active)

    def Tick(self):
        # fire weapon

        targets = [x for x in self.sensors.itervalues() if x.contacts > 0 \
                and not plus.isDefeated(x.robot)]

        self.DebugString(6, "No Hammer")
        self.DebugString(7, str(self.GetMotorAngle(self.motor)))
        # retract hammer when not in use
        if self.botinzone == 0 or self.comptimer <= self.NoChassisTime or self.retract == 1:
            self.DebugString(6, "R Hammer")
            if abs(self.motorstartangle - self.GetMotorAngle(self.motor)) > math.pi/2:
                if self.IsUpsideDown() and self.bInvertible:
                    self.Input("Hammer", 0, 100)
                else:
                    self.Input("Hammer", 0, -100)
            else:
                self.DebugString(6, "Hammer Ready")
                self.Input("Hammer", 0, 0)
                self.retract = 0
                self.retracttimer = 0

        # if a component is in the smart zone but not the chassis, wait to find chassis before firing weapons
        if self.compinzone == 1 and self.botinzone == 0:
            self.comptimer += 1

        if self.botinzone == 1:
            self.comptimer = 0

        if (self.weapons and (self.botinzone == 1 or (self.comptimer >= self.NoChassisTime and self.compinzone == 1))) or self.bImmobile or (self.IsUpsideDown() and not self.bInvertible):
            self.DebugString(6, "Hammer")
            if self.retract == 0:
                self.DebugString(6, "HammerStrike")
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

        if self.weapons and (self.botinzone == 1 or (self.comptimer >= self.NoChassisTime and self.compinzone == 1)):
            if not self.IsUpsideDown():
                for i in range(len(self.servos)):
                    self.DebugString(8, "Clamping")
                    ServoAngle = self.servostopangles[i] - self.GetMotorAngle(self.servos[i])
                    self.TurnToAngle(ServoAngle, i)


        if self.botinzone == 0 and (self.comptimer < self.NoChassisTime or self.compinzone == 0):
            #retract arms on servos when not in use
            self.DebugString(8, "No Clamping")
            for i in range(len(self.servos)):
                ServoAngle = self.servostartangles[i] - self.GetMotorAngle(self.servos[i])
                self.TurnToAngle(ServoAngle, i)

        bReturn = AI.SuperAI.Tick(self)

        return bReturn

    def TurnToAngle(self, heading, id):
        THRESHOLD = .05
        dreh = 0

        if heading > math.pi: heading -= 2 * math.pi
        elif heading < -math.pi: heading += 2 * math.pi

        if (heading < -THRESHOLD or heading > THRESHOLD):

            dir = -1
            if heading < 0: dir = 1

            h = min(abs(heading), 1.75)
            dreh = dir * (int((h / 1.5) * 100)+50)
            dreh = min(max(dreh, -100), 100)

            self.Input("Servo" + str(id + 1), 0, dreh)
            return False
        else:
            self.Input("Servo" + str(id + 1), 0, 0)
            return True

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
            elif id == 4: self.debug.get("line4").setText(string)
            elif id == 5: self.debug.get("line5").setText(string)
            elif id == 6: self.debug.get("line6").setText(string)
            elif id == 7: self.debug.get("line7").setText(string)
            elif id == 8: self.debug.get("line8").setText(string)
            elif id == 9: self.debug.get("line9").setText(string)

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

AI.register(ServoClampHammer)