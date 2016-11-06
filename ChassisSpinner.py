from __future__ import division
from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics

class ChassisSpinner(AI.SuperAI):
    "For Bots that spins chassis as weapon"
    name = "ChassisSpinner"

    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)
        self.motor = 1
        self.motor_direction = 1
        self.inverted_dir = False
        self.tickInterval = 1/30
        self.tickInterval_factor = 0.125 / self.tickInterval

        if 'motor' in args: self.motor = args['motor']
        if 'inverted_dir' in args:
            if args['inverted_dir']:
                self.motor_direction = -1;
        if 'tickInterval' in args: self.tickInterval = args['tickInterval']

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

        return AI.SuperAI.Activate(self, active)

    def Tick(self):
        if AI.SuperAI.debugging:
            speed = self.GetSpeed()
            self.DebugString(4, "Speed = " + str(speed))

            turning_speed = self.GetTurning()
            self.DebugString(5, "TSpeed = " + str(turning_speed))

            Target, range = self.GetNearestEnemy()
            if Target != None: self.DebugString(6, str(self.GetHeadingToID(Target, False)))
            self.DebugString(7, str(-self.GetMotorAngle(self.motor)))

        bReturn = AI.SuperAI.Tick(self)
        self.Spin(100)

        return bReturn

    def AimToHeading(self, heading, in_reverse = False):
        THRESHOLD = .05
        turn = 0
        heading -= self.GetMotorAngle(self.motor) * self.motor_direction

        if AI.SuperAI.debugging: self.DebugString(8, str(heading))

        if heading > math.pi: heading -= 2 * math.pi
        elif heading < -math.pi: heading += 2 * math.pi

        if (heading < -THRESHOLD or heading > THRESHOLD):

            dir = 1
            if heading < 0: dir = -1

            h = min(abs(heading), 1.75)
            turn = dir * int((h / 1.5) * 100)

            self.Turn(turn)
            return True
        else:
            self.Turn(0)
            return False

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

    def Spin(self, level):

        level = min(max(level, -100), 100)

        self.Input('Spin', 0, level)
        self.DebugString(9, "Spin = " + str(int(level)))

    def StuckHandler(self):
        "This default generator is called when the bot is almost immobile."
        while 1:
            # back up for 2 seconds (will stop once we're not immobile)
            for i in range(0, 16 * self.tickInterval_factor):
                pos = vector3(self.GetLocation())
                dir = vector3(self.GetDirection())
                self.DriveToLocation((pos - dir * 3).asTuple(), True)
                yield 0
            # go forward for 2 seconds
            for i in range(0, 16 * self.tickInterval_factor):
                pos = vector3(self.GetLocation())
                dir = vector3(self.GetDirection())
                self.DriveToLocation((pos + dir * 3).asTuple())
                yield 0

    def InvertHandler(self):
        # fire SRM once per two seconds (until we're upright!)
        while 1:
            self.Input("SRM", 0, 1)

            for i in range(0, 16 * self.tickInterval_factor):
                yield 0

AI.register(ChassisSpinner)