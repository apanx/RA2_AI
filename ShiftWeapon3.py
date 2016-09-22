from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics


class ShiftWeapon3(AI.SuperAI):
    "the servo has 2, 3 or 4 'fixed' angle position. It shifts periodically from these"
    # usage : see joe bloe stock showcase in gametehcmods for sample usage.
    # otherwise, mount protection (snow plow) and shift them, mount tribar, with a 2 position shifting, weapon may be straight to bot nose or may
    # flank opponent.... etc
    name = "ShiftWeapon3"
    # brought  to you by PhiletBabe from an idea of JoeBloe
    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)
        self.zone = "weapon"
        self.triggers1 = ["ServoFire"]
        self.spin_range = 99
        self.reloadTime = 0
        self.reloadDelay = 3

        self.servospeed = 100
        self.servoNose = 1 # servoNose is a factor from -1 to 1 that take into account the fact that the components attached to the
                           # servo motor are not always attached to its straight heading
        self.servoTimer = 15 # rate of shifting, the higher -> the longer between 2 shifts
        self.servoCountDown = self.servoTimer # count down before shifting
        self.servoNumberOfPosition = 2 # number of position
        self.servoAimAngle = 0 # angle the servo try to aim , each shift change this angle of 2*math.pi / (servoNumberOfPosition)
        self.delta = 0.05 #; error angle tolerance
        self.wellPositionned = True #:  if True, aiming angle reached : no more servo move until next shift
        self.Motor = 0
        self.flipflop= True

        if 'range' in args:       self.spin_range = args.get('range')
        if 'zone'  in args:       self.zone = args['zone']
        if 'servodelta' in args:  self.delta=args['servodelta']
        if 'servospeed' in args:  self.servospeed=args['servospeed']
        if 'servonose'  in args:  self.servoNose = args['servonose']
        if 'servoNbPos' in args:  self.servoNumberOfPosition = args['servoNbPos']
        if 'servoTimer' in args:  self.servoTimer = args['servoTimer']
        # to display the current angle of the servo motor uncomment thoses lines :
        self.debug = False
        AI.SuperAI.debugging = False
        self.tactics.append(Tactics.Engage(self))

    def Activate(self, active):
        if active:
            if AI.SuperAI.debugging:
                self.debug = Gooey.Plain("watch", 0, 150, 250, 240)
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
                tbox = self.debug.addText("line10", 0, 150, 250, 15)
                tbox.setText("")
            #define identifier of servo-motor
            goon = 1
            i = 0
            while goon == 1:
                if i  == self.GetNumComponents(): break
                currentType =  self.GetComponentType(i)
                if currentType == "ServoMotor": self.Motor = i
                i = i+ 1

            self.RegisterSmartZone(self.zone, 1)
        return AI.SuperAI.Activate(self, active)

    def Tick(self):

        enemy, range = self.GetNearestEnemy()
        # if  spinner in range :  do spin :
        if enemy is not None and range < self.spin_range:
            self.Input("Spin", 0, 1)
        elif self.GetInputStatus("Spin", 0) != 0:
            self.Input("Spin", 0, 0)

        self.flipflop = True #: not used indeed

        if  self.flipflop :
            targets = [x for x in self.sensors.itervalues() if x.contacts > 0 \
            and not plus.isDefeated(x.robot)]
            if len(targets) > 0 : self.Input("Fire", 0, 1)


        if self.ShiftConditionOk() and self.flipflop : #Time to shift ?
            # new angle to reach :
            self.servoAimAngle = self.servoAimAngle + (math.pi * 2 / self.servoNumberOfPosition)
            if (self.servoAimAngle > math.pi) :  self.servoAimAngle =  self.servoAimAngle - (2 * math.pi)
            self.wellPositionned = False

        if  not self.wellPositionned  :
            # go to servoAimAngle :
            selfangle = self.GetMotorAngle(self.Motor)
            Winkel = selfangle - self.servoAimAngle
            self.wellPositionned = self.AimTowards(Winkel)

        return AI.SuperAI.Tick(self)

    def AimTowards(self, heading):
        THRESHOLD = self.delta
        dreh = 0

        if heading > math.pi: heading -= 2 * math.pi
        elif heading < -math.pi: heading += 2 * math.pi

        if (heading < -THRESHOLD or heading > THRESHOLD):

            dire = -1
            if heading < 0: dire = 1

            h = min(abs(heading), 1.75)
            dreh = self.servoNose * dire * (int((h / 1.5) * 100)+20)

            # servo must turn :
            dreh = min(max(dreh, -self.servospeed), self.servospeed)
            self.Input('Servo', 0, dreh)
            return False
        else:
            # servo has not to turn, return True -> well positionned.
            self.Input('Servo', 0, 0)
            return True

    def InvertHandler(self):
        # fire weapon once per second (until we're upright!)
        while 1:
            self.Input("Srimech", 0, 2)

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
            elif id == 4: self.debug.get("line4").setText(string)
            elif id == 5: self.debug.get("line5").setText(string)
            elif id == 6: self.debug.get("line6").setText(string)
            elif id == 7: self.debug.get("line7").setText(string)
            elif id == 8: self.debug.get("line8").setText(string)
            elif id == 9: self.debug.get("line9").setText(string)
            elif id == 10: self.debug.get("line10").setText(string)


    def ShiftConditionOk(self):
        #test condition to turn servo
        # true : turn servo, may 'restart' different counter for next test
        # false : condition not meet.
        # in this version, turn condition depends of timer.
        #return False
        self.servoCountDown -= 1    # count down
        if self.servoCountDown <= 0 : #Time to shift !
            self.servoCountDown  =    self.servoTimer
            return True
        else:
            return False


AI.register(ShiftWeapon3)

