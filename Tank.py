import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics

class Annoy(AI.Tactic):
    name = "Annoy"
    def __init__(self, ai):
        AI.Tactic.__init__(self, ai)

        self.regroupPos = None
        self.regroupDir = True
        self.regroupTime = 0

    def Evaluate(self):
        self.priority = 0
        self.target_id, range = self.ai.GetNearestEnemy()

        if self.target_id != None:
            self.priority = 80
        else:
            self.priority -= 100

    def Execute(self):
        if self.target_id != None:
            self.ai.enemy_id = self.target_id

            clear_path = False

            if self.regroupTime <= 0:
                for r in (3, -3, 2, -2, 4, -4, 1, -1, 5, -5):
                    angle = self.ai.GetHeading(True) + r * (math.pi / 6)
                    new_dir = vector3(math.sin(angle), 0, math.cos(angle))
                    dest = vector3(self.ai.GetLocation()) + new_dir * 5

                    clear_path = self.ai.IsStraightPathClear(dest.asTuple(), self.ai.GetLocation())
                    if clear_path:
                        self.regroupPos = dest.asTuple()
                        self.regroupDir = (abs(r) <= 3)
                        self.regroupTime = 40
                        break

            self.ai.DriveToLocation(self.regroupPos, self.regroupDir)
            self.regroupTime -= 1

            return True
        else:
            return False

class Tank(AI.SuperAI):
    "Tank with turret"
    name = "Tank"

    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)
        self.triggers = ["Fire"]
        self.motor = 1
        self.motor_direction = 1
        self.inverted_servo = False
        self.tickInterval = 0.05
        self.tickInterval_factor = 0.125 / self.tickInterval

        if 'triggers' in args: self.triggers = args['triggers']
        if 'motor' in args: self.motor = args['motor']
        if 'inverted_servo' in args:
            if args['inverted_servo']:
                self.motor_direction = -1;
        if 'tickInterval' in args: self.tickInterval = args['tickInterval']
        self.triggerIterator = iter(self.triggers)
        self.tactics.append(Annoy(self))

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

        for trigger in self.triggers:
            self.Input(trigger, 0, 0)

        Target, range = self.GetNearestEnemy()
        if Target != None:
            Winkel = (self.GetHeadingToID(Target, False) + self.GetMotorAngle(self.motor) * self.motor_direction)
            self.DebugString(6, str(self.GetHeadingToID(Target, False)))
            self.DebugString(7, str(-self.GetMotorAngle(self.motor)))
            self.DebugString(8, str(Winkel))
            if self.AimTowards(Winkel):
                self.FireGun()

        return AI.SuperAI.Tick(self)

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

    def Aim(self, level):

        level = min(max(level, -100), 100)

        self.Input('Aim', 0, level)
        self.DebugString(9, "Aim = " + str(int(level)))

    def AimTowards(self, heading):
        THRESHOLD = .05
        dreh = 0

        if heading > math.pi: heading -= 2 * math.pi
        elif heading < -math.pi: heading += 2 * math.pi

        if (heading < -THRESHOLD or heading > THRESHOLD):

            dire = -1
            if heading < 0: dire = 1

            h = min(abs(heading), 1.75)
            dreh = dire * (int((h / 1.5) * 100)+50)

            self.Aim(dreh)
            return False
        else:
            self.Aim(0)
            return True

    def FireGun(self):
        for trigger in self.triggers:
            self.Input(trigger, 0, 1)

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

class FlameTank(Tank):
    "Tank with turret and always-on frontal flamethrower"
    name = "FlameTank"

    def __init__(self, **args):
        Tank.__init__(self, **args)
        self.secondary = ["Shoot"]
        if 'secondary' in args: self.secondary = args['secondary']
        tactic = [x for x in self.tactics if x.name == "Annoy"]
        self.tactics.remove(tactic[0])
        self.tactics.append(Tactics.Engage(self))

    def Activate(self, active):
        bReturn = Tank.Activate(self, active)
        for trigger in self.secondary:
            self.Input(trigger, 0, 100)

        return bReturn

class MGTank(Tank):
    "Machinegun Tank"
    name = "MGTank"

    def FireGun(self):
        try:
            trigger = self.triggerIterator.next()
        except StopIteration:
            self.triggerIterator = iter(self.triggers)
            trigger = self.triggerIterator.next()
        self.Input(trigger, 0, 1)

AI.register(Tank)
AI.register(FlameTank)
AI.register(MGTank)