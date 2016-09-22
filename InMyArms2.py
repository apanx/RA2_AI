from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics


class InMyArms2(AI.SuperAI):
    "take foe into its arms"
    name = "InMyArms2"
    # brought  to you by PhiletBabe
    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)
        self.zone = "servozone"
        self.spin_range = 99

        self.servospeed = 100
        self.servoNose = 1 # servoNose is a factor from -1 to 1 that take into account the fact that the components attached to the
                           # servo motor are not always attached to its straight heading
        self.delta = 0.1   #; error angle tolerance
        self.MotorOne =     0
        self.MotorTwo =     0
        self.MotorFound =   0

        self.isOpenArms1  = False
        self.isCloseArms1 = False
        self.isOpenArms2  = False
        self.isCloseArms2 = False
        self.haveToOpenArms = True
        self.counterRecheck = 3

        self.servoCloseArmsAngle =  2.5   # near angle 0
        self.servoOpenArmsAngle = 0.2     # near math.pi

        if 'range' in args:       self.spin_range = args['range']
        if 'servodelta' in args:  self.delta      = args['servodelta']
        if 'servospeed' in args:  self.servospeed = args['servospeed']
        if 'servonose'  in args:  self.servoNose  = args['servonose']      # value 1 / -1
        if 'servoopenangle'  in args:  self.servoOpenArmsAngle  = args['servoopenangle']
        if 'servocloseangle' in args:  self.servoCloseArmsAngle = args['servocloseangle']

        self.servoAngleFactor = self.servoNose / abs (self.servoNose) #: 1 ou -1
        # to display the current angle of the servo motor uncomment thoses lines :
        #self.debug = True
        #AI.SuperAI.debugging = True
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
                tbox.setText("isop1")
                tbox = self.debug.addText("line9", 0, 135, 250, 15)
                tbox.setText("isClos1")
                tbox = self.debug.addText("line10", 0, 150, 250, 15)
                tbox.setText("")
            #define identifier of servo-motor
            goon = 1
            i = 0
            while goon == 1:
                if i  == self.GetNumComponents(): break
                currentType =  self.GetComponentType(i)
                if currentType == "ServoMotor":
                    self.MotorFound += 1
                    if self.MotorFound == 1 : self.MotorOne = i
                    else:
                        self.MotorTwo = i
                        break
                i = i+ 1

            self.RegisterSmartZone(self.zone, 1)
        return AI.SuperAI.Activate(self, active)

    def Tick(self):

        enemy, range = self.GetNearestEnemy()
        # if  spinner in range :  do spin :
        if enemy is not None and range < self.spin_range:
            self.Input("Spin",  0   , 1)
        elif self.GetInputStatus("Spin",  0   ) !=   0  :
            self.Input("Spin", 0   ,   0  )

        self.counterRecheck  -= 1   #we check if we need to open/close arms only from time to time
        if self.counterRecheck == 0 : self.haveToOpenArms = True # force to open arms

        targets = [x for x in self.sensors.itervalues() if x.contacts >  0    \
        and not plus.isDefeated(x.robot)]
        if len(targets) >    0  :
            self.Input("Fire",   0  , 1)
            if self.counterRecheck == 0: self.haveToOpenArms = False # recheck if must close

        if self.counterRecheck <= 0 : self.counterRecheck = 3

        if  self.haveToOpenArms  :
            if self.debug : self.DebugString(8, "must OPEN  ARMS")
            self.isOpenArms1 = self.openArms(self.MotorOne, "Servo1",1 )
            self.isOpenArms2 = self.openArms(self.MotorTwo, "Servo2",-1 )
        else :
            if self.debug :self.DebugString(8, "must CLOSE ARMS")
            self.isCloseArms1 = self.closeArms(self.MotorOne, "Servo1",1)
            self.isCloseArms2 = self.closeArms(self.MotorTwo, "Servo2",-1)
            if self.isCloseArms1 :  self.Input("ServoFire1",   0  , 1)
            if self.isCloseArms2 :  self.Input("ServoFire2",   0  , 1)
        return AI.SuperAI.Tick(self)

    def AimTowards(self, heading, CtrlName):
        if (heading < -self.delta or heading > self.delta):
            dire = -self.servoAngleFactor
            dreh = 0
            if heading < 0: dire = -dire  #dire is direction of turn 1  is  clock -1 is the opposite !
            amplificator = 70             # servo must turn, but not automaically at full speed, speed will depend of angle to reach (heading).
            dreh = min(max(dire * abs(heading) * amplificator, -self.servospeed), self.servospeed)
            if self.debug :
                if CtrlName == "Servo1" : self.DebugString(6, "Speed for ctrl1:" + str(dreh))
                else: self.DebugString(7, "Speed for ctrl2:" + str(dreh))

            self.Input(CtrlName,0, dreh) #: dreh
            return False
        else:
            self.Input(CtrlName, 0,0 )
            # servo has not to turn, return True -> well positionned.
            if self.debug :
                if CtrlName == "Servo1" : self.DebugString(6, "Speed for ctrl1:0      ")
                else: self.DebugString(7, "Speed for ctrl2:0      ")
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


    def openArms(self, idMotor, CtrlServo, correctif ):
        # try to reach angle self.servoOpenArmsAngle
        selfangle = self.servoNose * self.GetMotorAngle(idMotor)
        winkel    = correctif * self.servoOpenArmsAngle - selfangle
        if self.debug :
            if CtrlServo == "Servo1" : self.DebugString(9, "winkel 1:" + str(winkel))
            else: self.DebugString(10, "winkel 2:" + str(winkel))
        return  self.AimTowards(winkel, CtrlServo)

    def closeArms(self, idMotor, CtrlServo,correctif ):
        # try to reach angle self.servoClosenArmsAngle
        selfangle = self.servoNose * self.GetMotorAngle(idMotor)
        winkel    = correctif * self.servoCloseArmsAngle - selfangle
        if self.debug :
            if CtrlServo == "Servo1" : self.DebugString(9, "winkel 1:" + str(winkel))
            else: self.DebugString(10, "winkel 2:" + str(winkel))
        return  self.AimTowards(winkel, CtrlServo)


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


AI.register(InMyArms2)

