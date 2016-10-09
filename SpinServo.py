from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics
from OmniServo import OmniServo
import time

class SpinServo(OmniServo):
    "Omni strategy with use of 1 servo motor"
    name = "SpinServo"
# ==============================================================
# class spin servo : like omni AI but allow the monitoring of 1 servo motor.
# the servo motor may be mount to spin horizontaly or verticvaly
# minimum binding.py declaration :    list.append(("mBotName","OmniServo",{'weapons':( 1)}))
# maximum binding.py declaration :   list.append(("myBotName","OmniServo",{'minangle':value, 'maxangle':value, 'servoVS':value,
#  'delta':value, 'servospeed':value,'weapons':(1)}))
# role of arguments and default value
#  minangle : angle the servo motor tries to reach when ennemy bot in custom zone named 'zoneservo2'. Default : 0 (radian)
#  maxangle : angle the servo motor tries to reach when ennemy bot in custom zone named 'zoneservo1'. Default: math.pi (radian)
# servospeed :  speed of the servo motor.  Default : 30 (hight for a servo !)
# delta :  servo motor is rarely equal to minangle or maxangle, so the servomotor oscillate widly  (like the beautiful music of 'the smiths'.) around theses angles
#           the value of delta define the tolerance arounf min/max angle to treat current angle as min/max angle
# servoVS : mostly use if the servo motor spin verticaly : may autorize only positive of negatives angles. Useful for the realistic rules.
#              servoVS = 1 : only positives angles / servoVS = -1 : only negatives values / ServoVS = 0 : no control. Default : 0
#             TO IMPROVE : problems when the bot is inverted
# bot construction : must have a servo-motor controler  named 'Servo'.
#                           must have 2 custom zones named 'zoneservo1' and 'zoneservo2'
#                           must have only 1 servo motor in its components, otherwise only the last one will be controlled.
#  note1 :  RA2 angles goes from -math.pi to Math.pi. spinning clockwise (positive servospeed) decrease angle.
#  note2:  sometime your bot may fly, lovely but fully useless
# note3: TO IMPROVE :give bad result when others custom zones (ie 'weapon'for piston or 'flip' )  exists
# author : PhiletBabe supported by the irreplaceable Madiaba. 2008
# ==============================================================

    def __init__(self, **args):
        OmniServo.__init__(self, **args)

        self.delta = 0.05


        # to display the current angle of the servo motor uncomment thoses lines :

        #AI.SuperAI.debugging = True

    def Tick(self):
        # fire weapon
        bReturn = Omni.Tick(self)
        if self.weapons:
            servoangle = self.GetMotorAngle(self.motor)
            self.DebugString(10, "Current servo motor angle : " + str(servoangle))

        # if angle must always be positive or negative, correct bad angle by reversing spin direction :
        servoangle = self.GetMotorAngle(self.motor)
        self.DebugString(10, "servo motor angle :" + str(servoangle))
        if ( self.servoVS == 1 ) and ( servoangle < 0.05):
            if ( servoangle > -math.pi/2):
                self.Input("Servo", 0, -20)
            else: 
                self.Input("Servo", 0, 20)
        elif ( self.servoVS == -1 ) and ( servoangle > -0.05):
            if ( servoangle > math.pi/2):
                self.Input("Servo", 0, -20)
            else: 
                self.Input("Servo", 0, 20)
        return bReturn

    def InvertHandler(self):
        # do not move servo if VS defined
        if ( self.servoVS  != 0 ): self.Input("Servo", 0, 0)
        # fire all weapons once per second (until we're upright!)
        while 1:
            for trigger in self.trigger2:
                self.Input(trigger, 0, 1)

            for i in range(0, 8):
                yield 0


    def SmartZoneEvent(self, direction, id, robot, chassis):
        if id == 1:
            if direction == 1:
                AI.SuperAI.SmartZoneEvent(self, direction, id, robot, chassis)
        elif id == 2:
            if robot > 0:
                if direction == 1:
                    # if not already well-positionned : move servo motor :
                    servoangle = self.GetMotorAngle(self.motor)
                    if servoangle < (self.maxangle -self.delta):
                        #next value after math.pi is -math.pi !
                        if servoangle > 0: self.Input("Servo", 0, -self.servospeed)
                        else: self.Input("Servo", 0, self.servospeed)
                    elif servoangle > (self.maxangle + self.delta): self.Input("Servo", 0, self.servospeed)
                    else: self.Input("Servo", 0, 0)
        elif id == 3:
            if robot > 0:
                if direction == 1:
                    # if not already well-positionned : move servo motor :
                    servoangle = self.GetMotorAngle(self.motor)
                    if servoangle > (self.minangle + self.delta): self.Input("Servo", 0, self.servospeed)
                    elif servoangle < (self.minangle - self.delta): self.Input("Servo", 0, -self.servospeed)
                    else: self.Input("Servo", 0, 0)


        return True

AI.register(SpinServo)
